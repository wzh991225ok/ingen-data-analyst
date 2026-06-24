"""Build the DuckDB warehouse from schema.sql + synthetic CSVs.

Run:  python -m src.warehouse.build_warehouse
Creates data/week07/ingen_warehouse.duckdb with all dims + facts loaded, then runs basic
integrity checks (row counts, no orphan foreign keys).
"""
from __future__ import annotations
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "src" / "warehouse" / "schema.sql"
CSV = ROOT / "data" / "week07" / "synthetic"
DB = ROOT / "data" / "week07" / "ingen_warehouse.duckdb"

TABLES = ["dim_date", "dim_geography", "dim_product", "dim_customer",
          "fact_fleet_telemetry", "fact_support_tickets", "fact_sales_pipeline"]

FK_CHECKS = [
    ("fact_fleet_telemetry", "date_key", "dim_date", "date_key"),
    ("fact_fleet_telemetry", "product_key", "dim_product", "product_key"),
    ("fact_fleet_telemetry", "customer_key", "dim_customer", "customer_key"),
    ("fact_fleet_telemetry", "geography_key", "dim_geography", "geography_key"),
    ("fact_support_tickets", "opened_date_key", "dim_date", "date_key"),
    ("fact_support_tickets", "product_key", "dim_product", "product_key"),
    ("fact_support_tickets", "customer_key", "dim_customer", "customer_key"),
    ("fact_sales_pipeline", "created_date_key", "dim_date", "date_key"),
    ("fact_sales_pipeline", "product_key", "dim_product", "product_key"),
    ("fact_sales_pipeline", "customer_key", "dim_customer", "customer_key"),
]


def build():
    if DB.exists():
        DB.unlink()
    con = duckdb.connect(str(DB))
    con.execute(SCHEMA.read_text())
    for t in TABLES:
        con.execute(f"COPY {t} FROM '{CSV / (t + '.csv')}' (HEADER, NULLSTR '')")
    print(f"Loaded warehouse -> {DB.relative_to(ROOT)}")
    print("Row counts:")
    for t in TABLES:
        n = con.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
        print(f"  {t:26s} {n:>7,}")
    print("Foreign-key integrity (orphans should all be 0):")
    ok = True
    for ft, fk, dt, dk in FK_CHECKS:
        orphan = con.execute(
            f"SELECT count(*) FROM {ft} f LEFT JOIN {dt} d ON f.{fk}=d.{dk} "
            f"WHERE d.{dk} IS NULL AND f.{fk} IS NOT NULL").fetchone()[0]
        flag = "OK" if orphan == 0 else "FAIL"
        if orphan: ok = False
        print(f"  {ft}.{fk} -> {dt}.{dk}: {orphan} orphans [{flag}]")
    con.close()
    print("Integrity:", "ALL OK" if ok else "PROBLEMS FOUND")
    return ok


if __name__ == "__main__":
    build()
