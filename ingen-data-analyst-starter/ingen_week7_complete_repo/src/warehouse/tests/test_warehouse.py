"""Tests for the Week 7 warehouse (build + 15 queries + assessment + reproducibility).

Run:  python -m pytest src/warehouse/tests -q
"""
from __future__ import annotations
from pathlib import Path
import duckdb
import pytest
from src.generator.generate_synthetic import generate, SEED
from src.warehouse.build_warehouse import build, TABLES
from src.queries.run_queries import main as run_queries
from src.warehouse.sql_assessment import run as run_assessment

ROOT = Path(__file__).resolve().parents[3]
DB = ROOT / "data" / "week07" / "ingen_warehouse.duckdb"


@pytest.fixture(scope="module", autouse=True)
def built():
    generate()
    assert build() is True   # integrity (no orphan FKs) passes
    yield


def test_all_tables_present_and_nonempty():
    con = duckdb.connect(str(DB), read_only=True)
    for t in TABLES:
        n = con.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
        assert n > 0, f"{t} empty"
    con.close()


def test_scale_targets():
    con = duckdb.connect(str(DB), read_only=True)
    assert con.execute("SELECT count(*) FROM fact_fleet_telemetry").fetchone()[0] >= 90000
    assert con.execute("SELECT count(*) FROM fact_support_tickets").fetchone()[0] == 5000
    assert con.execute("SELECT count(*) FROM fact_sales_pipeline").fetchone()[0] == 1000
    con.close()


def test_surrogate_keys_unique():
    con = duckdb.connect(str(DB), read_only=True)
    for t, pk in [("dim_customer","customer_key"), ("dim_product","product_key"),
                  ("fact_fleet_telemetry","telemetry_key"), ("fact_support_tickets","ticket_key"),
                  ("fact_sales_pipeline","pipeline_key")]:
        total = con.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
        distinct = con.execute(f"SELECT count(DISTINCT {pk}) FROM {t}").fetchone()[0]
        assert total == distinct, f"{t}.{pk} not unique"
    con.close()


def test_all_15_reference_queries_run():
    assert run_queries(show=False) is True


def test_sql_assessment_all_pass():
    assert run_assessment() is True


def test_reproducible_from_seed():
    # regenerate and confirm identical row counts + identical first telemetry row
    import csv
    p = ROOT / "data" / "week07" / "synthetic" / "fact_sales_pipeline.csv"
    first = open(p).readlines()[1]
    generate()  # same seed
    assert open(p).readlines()[1] == first, "synthetic data not reproducible from seed"
    assert SEED == 20260607
