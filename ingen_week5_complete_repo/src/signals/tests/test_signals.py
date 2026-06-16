"""Unit tests for the Week 5 demand-signal pipeline (offline fallbacks; no network).

Run:  python -m pytest src/signals/tests -q
"""
from __future__ import annotations
import json
import pandas as pd
import pytest
from src.signals import base, google_trends, gdelt_news, voc_reviews, demand_index


@pytest.fixture(scope="module", autouse=True)
def run_pipeline():
    base.reset_manifest()
    google_trends.collect(months=60)
    gdelt_news.collect(months=24)
    voc_reviews.mine()
    demand_index.build()
    yield


def test_search_interest_schema():
    df = pd.read_csv(base.DATA / "search_interest_long.csv")
    assert set(["vertical", "signal_type", "date", "value", "source"]).issubset(df.columns)
    assert df["value"].between(0, 100).all()
    # at least 60 months per vertical where available (success criterion)
    per = df.groupby("vertical")["date"].nunique()
    assert (per >= 60).all(), f"need >=60 months of search data: {per.to_dict()}"


def test_news_signals_schema():
    df = pd.read_csv(base.DATA / "news_signals_long.csv")
    assert set(df["signal_type"]) == {"news_volume", "news_tone"}
    assert (df[df.signal_type == "news_volume"]["value"] >= 0).all()


def test_pain_points_have_examples():
    df = pd.read_csv(base.DATA / "pain_points_long.csv")
    assert df["vertical"].nunique() == 5
    # spec: top 5 themes per vertical
    per = df.groupby("vertical")["theme_id"].nunique()
    assert (per == 5).all(), f"need 5 themes/vertical: {per.to_dict()}"
    # spec: >=3 example reviews per theme (allow a theme to have fewer only if cluster < 3 members)
    for _, r in df.iterrows():
        exs = [str(r.get(c, "")).strip() for c in ("example_1","example_2","example_3")]
        nonempty = [e for e in exs if e and e != "nan"]
        assert len(nonempty) >= min(3, int(r["size"])), f"theme has too few examples: {r.to_dict()}"
    assert df["top_terms"].str.len().gt(0).all()


def test_demand_index_ranks_all_verticals():
    df = pd.read_csv(base.DATA / "demand_signal_index.csv")
    assert len(df) == 5
    assert df["demand_index"].between(0, 100).all()
    assert sorted(df["rank"].tolist()) == [1, 2, 3, 4, 5]
    # index is monotonic with rank
    assert df.sort_values("rank")["demand_index"].is_monotonic_decreasing


def test_long_file_concatenates_all_signals():
    df = pd.read_csv(base.DATA / "demand_signals_long.csv")
    assert set(df["signal_type"]) == {"search_interest", "news_volume", "news_tone"}


def test_manifest_records_mode():
    rows = [json.loads(l) for l in base.MANIFEST.read_text().splitlines() if l.strip()]
    assert rows, "manifest empty"
    assert all("mode" in r for r in rows)
    # every collection task present
    tasks = {r["task"] for r in rows}
    for t in ["search_interest", "news_volume", "news_tone", "voice_of_customer", "demand_index"]:
        assert t in tasks, f"missing task {t} in manifest"
