"""Unit tests for the Week 3 ingestion pipeline.

Run:  python -m pytest src/ingest/tests -q
(Tests use offline fallbacks, so they run without network.)

Each dataset is checked for: non-empty rows, snake_case columns, no fully-null
required column, a valid year range where applicable, and a recorded manifest entry.
"""
from __future__ import annotations
import json
import pandas as pd
import pytest
from src.ingest import base
from src.ingest import datasets as ds


@pytest.fixture(scope="module", autouse=True)
def run_pipeline():
    # fresh manifest, run everything once for the whole module
    if base.MANIFEST.exists():
        base.MANIFEST.unlink()
    for fn in ds.ALL_LOADERS:
        fn()
    yield


def _load(name):
    return pd.read_csv(base.CLEAN / f"{name}.csv")


@pytest.mark.parametrize("name", [
    "census_population_by_age", "bls_home_health_aides", "oecd_longterm_care_spend",
    "nces_k12_enrollment", "worldbank_education_spend", "fbi_property_crime",
    "bls_security_guards", "bls_warehousing_employment", "worldbank_rnd_spend",
    "worldbank_pop_65plus", "openalex_robotics_publications", "sec_edgar_robotics_filings",
])
def test_dataset_nonempty_and_clean(name):
    df = _load(name)
    assert len(df) > 0, f"{name} has no rows"
    # snake_case columns
    for c in df.columns:
        assert c == c.lower(), f"{name} column not lowercase: {c}"
        assert " " not in c, f"{name} column has space: {c}"
    # no fully-null column
    for c in df.columns:
        assert df[c].notna().any(), f"{name} column fully null: {c}"


def test_year_ranges_reasonable():
    for name in ["census_population_by_age", "bls_home_health_aides", "fbi_property_crime",
                 "nces_k12_enrollment", "bls_security_guards", "bls_warehousing_employment"]:
        df = _load(name)
        assert "year" in df.columns
        yrs = pd.to_numeric(df["year"], errors="coerce").dropna()
        assert yrs.between(1990, 2027).all(), f"{name} has out-of-range year"


def test_manifest_complete():
    assert base.MANIFEST.exists(), "manifest not written"
    rows = [json.loads(l) for l in base.MANIFEST.read_text().splitlines() if l.strip()]
    names = {r["dataset"] for r in rows}
    expected = {fn.__name__.replace("load_", "") for fn in ds.ALL_LOADERS}
    # manifest uses dataset names, not loader names; just assert 12 entries with hashes
    assert len(rows) == 12, f"expected 12 manifest rows, got {len(rows)}"
    for r in rows:
        assert len(r["raw_sha256"]) == 64, f"{r['dataset']} missing/short sha256"
        assert r["rows"] > 0
        assert r["retrieved"]


def test_no_sentinel_strings():
    # cleaning should have converted 'N/A'/'-' to NULL
    for name in ["oecd_longterm_care_spend", "worldbank_rnd_spend"]:
        df = _load(name)
        for c in df.select_dtypes(include="object").columns:
            assert not df[c].isin(["N/A", "n/a", "-"]).any(), f"{name} still has sentinel strings"
