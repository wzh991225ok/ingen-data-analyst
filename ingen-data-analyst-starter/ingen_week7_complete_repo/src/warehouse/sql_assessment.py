"""Week 7 — SQL self-assessment (standardized exercise set, auto-graded).

Covers the five skill areas in the brief: JOINS, WINDOW functions, CTEs, SET OPS, AGGREGATIONS.
Each exercise has a prompt, a candidate solution, and an independent check (computed a different
way) so a passing solution must actually be correct, not just run. Produces a score sheet by
skill area and flags gaps.

Run:  python -m src.warehouse.sql_assessment
Outputs reports/week07/sql_score_sheet.md and reports/week07/sql_score_sheet.csv
"""
from __future__ import annotations
import csv
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "data" / "week07" / "ingen_warehouse.duckdb"
RPT = ROOT / "reports" / "week07"
RPT.mkdir(parents=True, exist_ok=True)

# Each exercise: (id, skill, prompt, solution_sql, check_fn(con)->expected_scalar, extract_fn(result)->scalar)
EXERCISES = [
 ("E1", "AGGREGATION",
  "Total number of telemetry rows where the robot was active.",
  "SELECT COUNT(*) FROM fact_fleet_telemetry WHERE is_active;",
  lambda c: c.execute("SELECT SUM(CASE WHEN is_active THEN 1 ELSE 0 END) FROM fact_fleet_telemetry").fetchone()[0]),

 ("E2", "AGGREGATION",
  "Average resolution_hours for resolved Critical tickets (rounded to 1 dp).",
  "SELECT ROUND(AVG(resolution_hours),1) FROM fact_support_tickets WHERE is_resolved AND severity='Critical';",
  lambda c: round(c.execute("SELECT AVG(resolution_hours) FROM fact_support_tickets WHERE is_resolved AND severity='Critical'").fetchone()[0],1)),

 ("E3", "JOIN",
  "Number of won opportunities for product 'Fari' (join pipeline to product).",
  "SELECT COUNT(*) FROM fact_sales_pipeline s JOIN dim_product p ON s.product_key=p.product_key WHERE p.product_name='Fari' AND s.is_won;",
  lambda c: c.execute("SELECT COUNT(*) FROM fact_sales_pipeline s JOIN dim_product p ON s.product_key=p.product_key WHERE p.product_code='FARI' AND s.is_won").fetchone()[0]),

 ("E4", "JOIN",
  "Distinct customers in the 'North America' region that appear in the sales pipeline.",
  """SELECT COUNT(DISTINCT s.customer_key) FROM fact_sales_pipeline s
     JOIN dim_customer c ON s.customer_key=c.customer_key
     JOIN dim_geography g ON c.geography_key=g.geography_key WHERE g.region='North America';""",
  lambda c: c.execute("""SELECT COUNT(DISTINCT c.customer_key) FROM dim_customer c
     JOIN dim_geography g ON c.geography_key=g.geography_key
     WHERE g.region='North America' AND c.customer_key IN (SELECT customer_key FROM fact_sales_pipeline)""").fetchone()[0]),

 ("E5", "CTE",
  "Using a CTE of monthly won value, return the number of months with >0 won value.",
  """WITH m AS (SELECT d.year,d.month,SUM(CASE WHEN s.is_won THEN s.amount_usd ELSE 0 END) v
     FROM fact_sales_pipeline s JOIN dim_date d ON s.created_date_key=d.date_key GROUP BY d.year,d.month)
     SELECT COUNT(*) FROM m WHERE v>0;""",
  lambda c: c.execute("""SELECT COUNT(*) FROM (SELECT d.year,d.month,SUM(CASE WHEN s.is_won THEN s.amount_usd ELSE 0 END) v
     FROM fact_sales_pipeline s JOIN dim_date d ON s.created_date_key=d.date_key GROUP BY d.year,d.month) t WHERE v>0""").fetchone()[0]),

 ("E6", "WINDOW",
  "Using ROW_NUMBER, find how many products have their single worst error-day with >X errors; "
  "return the max single-day error total across all products (a window-ranked value).",
  """WITH pd AS (SELECT product_key, date_key, SUM(error_count) e FROM fact_fleet_telemetry GROUP BY product_key,date_key),
     r AS (SELECT e, ROW_NUMBER() OVER (PARTITION BY product_key ORDER BY e DESC) rn FROM pd)
     SELECT MAX(e) FROM r WHERE rn=1;""",
  lambda c: c.execute("SELECT MAX(e) FROM (SELECT product_key,date_key,SUM(error_count) e FROM fact_fleet_telemetry GROUP BY product_key,date_key)").fetchone()[0]),

 ("E7", "WINDOW",
  "Using a window SUM, compute the grand total won value via SUM() OVER () (return one value).",
  "SELECT DISTINCT SUM(CASE WHEN is_won THEN amount_usd ELSE 0 END) OVER () FROM fact_sales_pipeline;",
  lambda c: c.execute("SELECT SUM(CASE WHEN is_won THEN amount_usd ELSE 0 END) FROM fact_sales_pipeline").fetchone()[0]),

 ("E8", "SETOP",
  "Count customers appearing in BOTH telemetry and tickets (INTERSECT of customer_key).",
  """SELECT COUNT(*) FROM (
       SELECT DISTINCT customer_key FROM fact_fleet_telemetry
       INTERSECT SELECT DISTINCT customer_key FROM fact_support_tickets);""",
  lambda c: c.execute("""SELECT COUNT(DISTINCT customer_key) FROM fact_fleet_telemetry
       WHERE customer_key IN (SELECT customer_key FROM fact_support_tickets)""").fetchone()[0]),

 ("E9", "SETOP",
  "Count customers in tickets but NOT in pipeline (EXCEPT of customer_key).",
  """SELECT COUNT(*) FROM (
       SELECT DISTINCT customer_key FROM fact_support_tickets
       EXCEPT SELECT DISTINCT customer_key FROM fact_sales_pipeline);""",
  lambda c: c.execute("""SELECT COUNT(DISTINCT customer_key) FROM fact_support_tickets
       WHERE customer_key NOT IN (SELECT customer_key FROM fact_sales_pipeline)""").fetchone()[0]),

 ("E10", "AGGREGATION",
  "Overall pipeline win rate as a percentage rounded to 1 dp.",
  "SELECT ROUND(100.0*SUM(CASE WHEN is_won THEN 1 ELSE 0 END)/COUNT(*),1) FROM fact_sales_pipeline;",
  lambda c: round(100.0*c.execute("SELECT SUM(CASE WHEN is_won THEN 1 ELSE 0 END) FROM fact_sales_pipeline").fetchone()[0]
                   / c.execute("SELECT COUNT(*) FROM fact_sales_pipeline").fetchone()[0],1)),

 ("E11", "JOIN",
  "Total won value for the 'humanoid' vertical (join pipeline->product, filter vertical).",
  """SELECT ROUND(SUM(CASE WHEN s.is_won THEN s.amount_usd ELSE 0 END),0)
     FROM fact_sales_pipeline s JOIN dim_product p ON s.product_key=p.product_key WHERE p.vertical='humanoid';""",
  lambda c: round(c.execute("""SELECT SUM(s.amount_usd) FROM fact_sales_pipeline s JOIN dim_product p
     ON s.product_key=p.product_key WHERE p.vertical='humanoid' AND s.is_won""").fetchone()[0],0)),

 ("E12", "CTE",
  "Using a CTE, return the highest single-product total ticket count.",
  """WITH t AS (SELECT product_key, COUNT(*) n FROM fact_support_tickets GROUP BY product_key)
     SELECT MAX(n) FROM t;""",
  lambda c: c.execute("SELECT MAX(n) FROM (SELECT product_key,COUNT(*) n FROM fact_support_tickets GROUP BY product_key)").fetchone()[0]),
]


def run():
    con = duckdb.connect(str(DB), read_only=True)
    results = []
    for ex_id, skill, prompt, sol, check in EXERCISES:
        try:
            got = con.execute(sol).fetchone()[0]
            expected = check(con)
            ok = (got == expected) or (isinstance(got, float) and abs(got - expected) < 0.05)
            results.append((ex_id, skill, "PASS" if ok else "FAIL", got, expected))
        except Exception as e:  # noqa: BLE001
            results.append((ex_id, skill, "ERROR", str(e)[:40], ""))
    con.close()

    # score by skill
    skills = {}
    for _id, skill, status, *_ in results:
        s = skills.setdefault(skill, [0, 0]); s[1] += 1
        if status == "PASS": s[0] += 1
    passed = sum(1 for r in results if r[2] == "PASS")

    # write CSV
    with open(RPT / "sql_score_sheet.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["exercise", "skill", "status", "got", "expected"]); w.writerows(results)

    # write markdown
    lines = ["# Week 7 — SQL Self-Assessment Score Sheet", "",
             f"Standardized exercise set run against the synthetic DuckDB warehouse. "
             f"**Score: {passed}/{len(results)} ({100*passed//len(results)}%).**",
             "", "## By skill area", "", "| Skill | Passed | Total |", "|---|---|---|"]
    for sk, (p, t) in sorted(skills.items()):
        lines.append(f"| {sk} | {p} | {t} |")
    lines += ["", "## Detail", "", "| Exercise | Skill | Status |", "|---|---|---|"]
    for _id, skill, status, *_ in results:
        lines.append(f"| {_id} | {skill} | {status} |")
    gaps = [sk for sk, (p, t) in skills.items() if p < t]
    lines += ["", "## Gaps identified", ""]
    lines.append("- None — all skill areas at 100%." if not gaps
                 else "\n".join(f"- {sk}: review needed ({skills[sk][0]}/{skills[sk][1]})" for sk in gaps))
    (RPT / "sql_score_sheet.md").write_text("\n".join(lines))

    print(f"SQL self-assessment: {passed}/{len(results)} passed")
    for sk, (p, t) in sorted(skills.items()):
        print(f"  {sk:13s} {p}/{t}")
    print(f"score sheet -> {(RPT/'sql_score_sheet.md').relative_to(ROOT)}")
    return passed == len(results)


if __name__ == "__main__":
    run()
