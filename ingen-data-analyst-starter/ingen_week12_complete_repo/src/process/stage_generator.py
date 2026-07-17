"""Week 12 — build the stage-level event table by replaying Week 7's real ticket stream.

Reads fact_support_tickets (+ dims) from the Week 7 DuckDB warehouse, replays every ticket through
the documented process model, and writes:

  data/week12/fact_ticket_stage_events.csv   one row per ticket x stage
  data/week12/ticket_cycle_times.csv         one row per ticket (total cycle time + attributes)

Reconciliation to Week 7 (success criterion: "process map is verifiable against the schema"):
  * every generated ticket_key exists in fact_support_tickets (1:1, no orphans)
  * per ticket, sum(wait_hours + service_hours) across stages == total cycle time exactly
  * the arrival stream (opened date, severity, category, product, geography) is Week 7's, unchanged

Run: python -m src.process.stage_generator
"""
from __future__ import annotations
import os
from pathlib import Path

import numpy as np
import pandas as pd
import duckdb

from .process_model import SupportProcess, Ticket, SEED

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "week12"
DATA.mkdir(parents=True, exist_ok=True)

# The Week 7 warehouse. Override with WEEK7_DB if the repo lives elsewhere.
DEFAULT_DB = Path("/home/claude/src12/ingen_week7_complete_repo/data/week07/ingen_warehouse.duckdb")
DB = Path(os.environ.get("WEEK7_DB", DEFAULT_DB))

EPOCH = pd.Timestamp("2024-06-01")


def load_week7_tickets() -> pd.DataFrame:
    """Real Week 7 tickets joined to their dimensions — this is the arrival stream."""
    con = duckdb.connect(str(DB), read_only=True)
    df = con.execute("""
        SELECT t.ticket_key, t.ticket_id, t.severity, t.category,
               d.full_date AS opened_date, p.product_name AS product,
               g.region, g.country, t.resolution_hours AS week7_resolution_hours,
               t.is_resolved
        FROM fact_support_tickets t
        JOIN dim_date d      ON t.opened_date_key = d.date_key
        JOIN dim_product p   ON t.product_key    = p.product_key
        JOIN dim_geography g ON t.geography_key  = g.geography_key
        ORDER BY d.full_date, t.ticket_key
    """).fetchdf()
    con.close()
    return df


def build(seed: int = SEED) -> tuple[pd.DataFrame, pd.DataFrame]:
    tickets_df = load_week7_tickets()
    rng = np.random.default_rng(seed)

    # Week 7 stores an opened DATE only; spread arrivals within the day (documented, seeded).
    offsets = rng.uniform(0, 24, len(tickets_df))
    arrival_h = ((pd.to_datetime(tickets_df["opened_date"]) - EPOCH).dt.total_seconds() / 3600.0
                 + offsets).to_numpy()

    tickets = [
        Ticket(ticket_key=int(r.ticket_key), ticket_id=r.ticket_id, arrival_h=float(a),
               severity=r.severity, category=r.category, product=r.product, region=r.region)
        for r, a in zip(tickets_df.itertuples(index=False), arrival_h)
    ]

    rows = SupportProcess(tickets, seed=seed).run()
    ev = pd.DataFrame(rows)

    # per-ticket totals
    ev["stage_hours"] = ev["wait_hours"] + ev["service_hours"]
    cycle = (ev.groupby("ticket_key")["stage_hours"].sum().rename("cycle_time_hours").reset_index())
    cycle = cycle.merge(tickets_df, on="ticket_key", how="left")
    cycle["opened_date"] = pd.to_datetime(cycle["opened_date"])
    cycle["weekday"] = cycle["opened_date"].dt.day_name()
    cycle["dispatched"] = cycle["ticket_key"].isin(
        ev.loc[ev["stage"] == "Parts & dispatch", "ticket_key"]).astype(int)

    # workload at assignment: open tickets in the same team queue when this ticket entered triage
    tri = ev[ev["stage"] == "Triage"][["ticket_key", "queue_len_on_entry"]]
    cycle = cycle.merge(tri.rename(columns={"queue_len_on_entry": "tier1_queue_on_entry"}),
                        on="ticket_key", how="left")
    cycle["tier1_queue_on_entry"] = cycle["tier1_queue_on_entry"].fillna(0).astype(int)

    ev.to_csv(DATA / "fact_ticket_stage_events.csv", index=False)
    cycle.to_csv(DATA / "ticket_cycle_times.csv", index=False)
    return ev, cycle


def verify(ev: pd.DataFrame, cycle: pd.DataFrame) -> dict:
    """Reconciliation checks against the Week 7 schema."""
    w7 = load_week7_tickets()
    checks = {}
    checks["all_tickets_replayed"] = bool(cycle["ticket_key"].nunique() == len(w7))
    checks["no_orphan_ticket_keys"] = bool(set(cycle["ticket_key"]).issubset(set(w7["ticket_key"])))
    recomputed = ev.groupby("ticket_key")["stage_hours"].sum().round(4)
    stated = cycle.set_index("ticket_key")["cycle_time_hours"].round(4)
    checks["stages_sum_to_cycle_time"] = bool(recomputed.reindex(stated.index).equals(stated))
    checks["every_ticket_has_intake"] = bool(
        ev[ev.stage == "Intake"]["ticket_key"].nunique() == cycle["ticket_key"].nunique())
    checks["attributes_match_week7"] = bool(
        cycle[["ticket_key", "severity", "category"]]
        .merge(w7[["ticket_key", "severity", "category"]], on="ticket_key", suffixes=("", "_w7"))
        .eval("severity == severity_w7 and category == category_w7").all())
    return checks


if __name__ == "__main__":
    ev, cycle = build()
    print(f"stage events : {len(ev):,} rows across {ev['stage'].nunique()} stages")
    print(f"tickets      : {len(cycle):,}")
    print(f"cycle time   : median {cycle['cycle_time_hours'].median():.1f}h  "
          f"mean {cycle['cycle_time_hours'].mean():.1f}h  p90 {cycle['cycle_time_hours'].quantile(0.9):.1f}h")
    print(f"dispatched   : {cycle['dispatched'].mean()*100:.1f}% of tickets needed a part/site visit")
    print("\nStage share of total time in process:")
    share = (ev.groupby("stage")["stage_hours"].sum() / ev["stage_hours"].sum() * 100).sort_values(ascending=False)
    for k, v in share.items():
        print(f"  {k:20s} {v:5.1f}%")
    print("\nReconciliation vs Week 7 schema:")
    for k, v in verify(ev, cycle).items():
        print(f"  {k:28s} {'PASS' if v else 'FAIL'}")
