"""Tests for Week 11 anomaly detection.

Run: python -m pytest src/anomaly/tests -q
Data tests use the cached benchmark files (downloaded on first run).
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import pytest

from src.anomaly import data_loader as dl
from src.anomaly.evaluate import find_events, choose_threshold, time_to_detection
from src.anomaly.operational import debounce, contiguous_runs, alert_level_stats
from src.anomaly.adaptive_threshold import rolling_quantile_threshold, ewma_sigma_threshold
from src.anomaly.models import ControlChart


def test_licenses_documented_for_every_dataset():
    """Success criterion: license of every dataset used is documented."""
    lic = dl.license_table()
    assert len(lic) >= 2
    for _, r in lic.iterrows():
        assert r["license"] and str(r["license"]).strip(), f"{r['dataset']} missing license"
        assert str(r["url"]).startswith("https://")
        assert str(r["citation"]).strip()


def test_nab_loads_with_labelled_windows():
    df = dl.load_nab()
    assert len(df) > 20000
    assert set(df.columns) >= {"timestamp", "value", "is_anomaly"}
    assert df["is_anomaly"].isin([0, 1]).all()
    assert 0 < df["is_anomaly"].mean() < 0.5      # some but not most points are anomalous
    assert len(df.attrs["windows"]) == 4          # NAB labels 4 windows for this series


def test_skab_loads_multivariate_with_labels():
    df = dl.load_skab()
    assert len(df) > 1000
    for c in dl.SKAB_SENSORS:
        assert c in df.columns
    assert df["is_anomaly"].isin([0, 1]).all()


def test_skab_clean_reference_is_anomaly_free():
    clean = dl.load_skab_clean()
    assert len(clean) > 1000
    assert clean["is_anomaly"].sum() == 0         # it is the anomaly-free baseline


def test_nab_features_are_causal():
    """Rolling features must not leak the future: they are built from shift(1)."""
    df = dl.load_nab().head(500)
    f = dl.nab_features(df)
    # a rolling mean built causally cannot equal a centred window including the current point
    assert f["roll_mean_12"].isna().iloc[0]
    v = df["value"].to_numpy()
    # row 20's causal 12-mean equals mean of rows 8..19 (excludes row 20 itself)
    assert np.isclose(f["roll_mean_12"].iloc[20], v[8:20].mean())


def test_find_events_and_contiguous_runs_agree():
    y = np.array([0, 1, 1, 0, 0, 1, 0, 1, 1, 1])
    assert find_events(y) == [(1, 2), (5, 5), (7, 9)]
    assert contiguous_runs(y) == find_events(y)


def test_debounce_requires_consecutive_flags():
    raw = np.array([1, 0, 1, 1, 1, 0, 1, 1])
    out = debounce(raw, 3)
    # only the run of three 1s (idx 2..4) qualifies, and only from its 3rd element
    assert out.tolist() == [0, 0, 0, 0, 1, 0, 0, 0]
    # n=1 is a passthrough
    assert debounce(raw, 1).tolist() == raw.tolist()


def test_choose_threshold_respects_recall_floor():
    rng = np.random.default_rng(0)
    y = np.r_[np.zeros(900), np.ones(100)].astype(int)
    scores = np.r_[rng.normal(0, 1, 900), rng.normal(4, 1, 100)]
    thr, met = choose_threshold(y, scores, recall_floor=0.80)
    assert met
    recall = ((scores >= thr) & (y == 1)).sum() / (y == 1).sum()
    assert recall >= 0.80


def test_adaptive_thresholds_are_causal():
    """Threshold at t must not depend on score at t (no look-ahead)."""
    s = np.r_[np.ones(300), np.array([100.0]), np.ones(50)]
    rq = rolling_quantile_threshold(s, window=100, q=0.98)
    ew = ewma_sigma_threshold(s, alpha=0.05, k=3.0)
    # the spike at index 300 must not have already inflated its own threshold
    assert rq[300] < 100
    assert ew[300] < 100


def test_time_to_detection_counts_only_detected_events():
    ts = pd.date_range("2024-01-01", periods=10, freq="min")
    y = np.array([0, 1, 1, 0, 0, 1, 1, 0, 0, 0])
    pred = np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0])   # detects event 1 late, misses event 2
    mean_ttd, detected, total = time_to_detection(ts, y, pred)
    assert total == 2 and detected == 1
    assert mean_ttd == 60.0     # one minute after the event started


def test_control_chart_scores_higher_on_spikes():
    rng = np.random.default_rng(1)
    train = rng.normal(0, 1, (500, 2))
    test = np.vstack([rng.normal(0, 1, (100, 2)), np.full((5, 2), 12.0)])
    cc = ControlChart(alpha=0.05).fit(train)
    sc = cc.score(test)
    assert np.nanmean(sc[-5:]) > np.nanmean(sc[:100])   # spikes score higher


def test_alert_level_stats_counts_one_alert_per_run():
    ts = pd.date_range("2024-01-01", periods=10, freq="h")
    y = np.array([0, 1, 1, 0, 0, 0, 0, 0, 0, 0])
    pred = np.array([0, 1, 1, 0, 1, 1, 0, 0, 0, 0])   # 1 true alert + 1 false alert
    st = alert_level_stats(y, pred, ts)
    assert st["events_total"] == 1 and st["events_caught"] == 1
    assert st["alerts_total"] == 2 and st["false_alerts"] == 1
