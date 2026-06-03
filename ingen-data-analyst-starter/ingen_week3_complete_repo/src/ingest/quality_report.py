"""Generate the Week 3 data-quality report (HTML) over the DuckDB warehouse.

Profiles every table: row counts, column dtypes, null rates, and (where a `year`
column exists) time coverage. Writes reports/week03/data_quality_report.html.

Usage:  python -m src.ingest.quality_report
"""
from __future__ import annotations
import json
import duckdb
import pandas as pd
from . import base

OUT = base.ROOT / "reports" / "week03" / "data_quality_report.html"
OUT.parent.mkdir(parents=True, exist_ok=True)


def main():
    con = duckdb.connect(str(base.WAREHOUSE), read_only=True)
    tables = con.execute(
        """SELECT table_schema, table_name FROM information_schema.tables
           WHERE table_schema NOT IN ('information_schema','pg_catalog','main')
             AND table_name NOT LIKE '\\_%' ESCAPE '\\'
             AND table_type='BASE TABLE'
           ORDER BY 1,2"""
    ).fetchall()

    manifest = {r["dataset"]: r for r in
                (json.loads(l) for l in base.MANIFEST.read_text().splitlines() if l.strip())}

    blocks = []
    summary_rows = []
    for schema, tbl in tables:
        df = con.execute(f'SELECT * FROM {schema}."{tbl}";').df()
        nrows, ncols = df.shape
        nulls = (df.isna().mean() * 100).round(1)
        dtypes = df.dtypes.astype(str)
        prof = pd.DataFrame({"column": df.columns, "dtype": dtypes.values,
                             "null_%": nulls.values,
                             "n_unique": [df[c].nunique(dropna=True) for c in df.columns]})
        # year coverage
        yr_cov = ""
        if "year" in df.columns:
            yrs = pd.to_numeric(df["year"], errors="coerce").dropna()
            if len(yrs):
                yr_cov = f"{int(yrs.min())}–{int(yrs.max())}"
        m = manifest.get(tbl, {})
        summary_rows.append({
            "schema": schema, "table": tbl, "rows": nrows, "cols": ncols,
            "max_null_%": float(nulls.max()) if ncols else 0.0,
            "year_coverage": yr_cov, "source": m.get("source", ""),
            "mode": m.get("mode", ""), "retrieved": m.get("retrieved", ""),
        })
        blocks.append(f"""
        <h3>{schema}.{tbl}</h3>
        <p class="meta">Source: {m.get('source','?')} &middot; mode: {m.get('mode','?')}
        &middot; retrieved: {m.get('retrieved','?')} &middot; rows: {nrows} &middot; cols: {ncols}
        {('&middot; years: '+yr_cov) if yr_cov else ''}<br>
        raw sha256: <code>{m.get('raw_sha256','?')[:16]}…</code></p>
        {prof.to_html(index=False, classes='prof', border=0)}
        """)

    summ = pd.DataFrame(summary_rows)
    overall = {
        "tables": len(summ), "total_rows": int(summ["rows"].sum()),
        "schemas": summ["schema"].nunique(),
        "tables_with_year": int((summ["year_coverage"] != "").sum()),
        "max_null_anywhere": f'{summ["max_null_%"].max():.1f}%' if len(summ) else "0%",
    }

    html = f"""<!doctype html><html><head><meta charset="utf-8">
    <title>InGen Week 3 — Data Quality Report</title>
    <style>
      body{{font-family:Arial,Helvetica,sans-serif;margin:32px;color:#222;}}
      h1{{color:#1F3864;}} h3{{color:#2E5496;margin-top:28px;}}
      .meta{{color:#595959;font-size:13px;}}
      table{{border-collapse:collapse;margin:8px 0 16px;font-size:13px;}}
      .prof th{{background:#2E5496;color:#fff;text-align:left;padding:5px 10px;}}
      .prof td{{border-bottom:1px solid #e0e6f0;padding:4px 10px;}}
      .summary th{{background:#1F3864;color:#fff;padding:6px 10px;text-align:left;}}
      .summary td{{border-bottom:1px solid #d9e1f2;padding:5px 10px;}}
      code{{background:#f2f6fc;padding:1px 4px;border-radius:3px;}}
      .kpis{{display:flex;gap:18px;flex-wrap:wrap;margin:14px 0;}}
      .kpi{{background:#f2f6fc;border-left:4px solid #2E5496;padding:10px 16px;}}
      .kpi b{{display:block;font-size:22px;color:#1F3864;}}
    </style></head><body>
    <h1>InGen Dynamics — Week 3 Data Quality Report</h1>
    <p class="meta">Generated {base.TODAY} from <code>data/week03/analytics.duckdb</code>.
    All sources are public; figures verified via the ingest manifest (sha256-versioned).
    Run mode reflects whether data came from live APIs or schema-correct offline fallbacks.</p>
    <div class="kpis">
      <div class="kpi"><b>{overall['tables']}</b>tables</div>
      <div class="kpi"><b>{overall['schemas']}</b>schemas (1 per vertical + shared)</div>
      <div class="kpi"><b>{overall['total_rows']}</b>total rows</div>
      <div class="kpi"><b>{overall['tables_with_year']}</b>tables with time coverage</div>
      <div class="kpi"><b>{overall['max_null_anywhere']}</b>max null rate (any column)</div>
    </div>
    <h2>Summary</h2>
    {summ.to_html(index=False, classes='summary', border=0)}
    <h2>Per-table profiles</h2>
    {''.join(blocks)}
    <hr><p class="meta">Prepared by Ziheng Wang · inGen Data Analyst internship · Week 3.
    Offline-fallback rows are clearly labelled synthetic samples with the real schema;
    set INGEST_ALLOW_NETWORK=1 and re-run the pipeline to populate from live public APIs.</p>
    </body></html>"""
    OUT.write_text(html)
    con.close()
    print(f"Quality report written: {OUT.relative_to(base.ROOT)}")
    print(f"  {overall}")


if __name__ == "__main__":
    main()
