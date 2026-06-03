"""Build the DuckDB analytics warehouse from cleaned datasets (Week 3).

Creates one schema per InGen vertical plus a `shared` schema, loads each cleaned
CSV into the matching schema as a table, and adds a couple of convenience views.

Usage:  python -m src.ingest.build_warehouse
Output: data/week03/analytics.duckdb
"""
from __future__ import annotations
import json
import duckdb
from . import base

# dataset -> (schema, table) derived from the manifest's vertical field
SCHEMA_FOR_VERTICAL = {
    "eldercare": "eldercare",
    "education": "education",
    "indoor_security": "indoor_security",
    "outdoor_patrol": "outdoor_patrol",
    "humanoid": "humanoid",
    "shared": "shared",
}


def _manifest_rows():
    if not base.MANIFEST.exists():
        raise SystemExit("No manifest found. Run `python -m src.ingest.run_all` first.")
    return [json.loads(l) for l in base.MANIFEST.read_text().splitlines() if l.strip()]


def main():
    rows = _manifest_rows()
    if base.WAREHOUSE.exists():
        base.WAREHOUSE.unlink()
    con = duckdb.connect(str(base.WAREHOUSE))

    schemas = sorted({SCHEMA_FOR_VERTICAL.get(r["vertical"], "shared") for r in rows})
    for s in schemas:
        con.execute(f'CREATE SCHEMA IF NOT EXISTS {s};')

    loaded = []
    for r in rows:
        name = r["dataset"]
        schema = SCHEMA_FOR_VERTICAL.get(r["vertical"], "shared")
        csv_path = base.CLEAN / f"{name}.csv"
        if not csv_path.exists():
            print(f"  ! missing clean file for {name}, skipping")
            continue
        con.execute(
            f'CREATE OR REPLACE TABLE {schema}."{name}" AS '
            f"SELECT * FROM read_csv_auto('{csv_path.as_posix()}', header=true);"
        )
        n = con.execute(f'SELECT COUNT(*) FROM {schema}."{name}";').fetchone()[0]
        loaded.append((schema, name, n))
        print(f"  ✓ {schema}.{name}  ({n} rows)")

    # convenience views joining shared aging + spend for quick eldercare sizing
    try:
        con.execute(
            'CREATE OR REPLACE VIEW shared.v_country_context AS '
            'SELECT a.iso3, a.country, a.year, a.pop_65plus_pct, r.rnd_spend_pct_gdp '
            'FROM shared.worldbank_pop_65plus a '
            'LEFT JOIN shared.worldbank_rnd_spend r '
            'ON a.iso3 = r.iso3 AND a.year = r.year;'
        )
        print("  ✓ view shared.v_country_context")
    except Exception as e:  # noqa: BLE001
        print(f"  ! view creation skipped: {e}")

    # a tiny catalog table recording what was loaded
    con.execute('CREATE OR REPLACE TABLE shared._load_catalog (schema_name VARCHAR, table_name VARCHAR, rows BIGINT);')
    con.executemany('INSERT INTO shared._load_catalog VALUES (?, ?, ?);', loaded)

    con.close()
    print(f"Warehouse built: {base.WAREHOUSE.relative_to(base.ROOT)}  ({len(loaded)} tables across {len(schemas)} schemas)")


if __name__ == "__main__":
    main()
