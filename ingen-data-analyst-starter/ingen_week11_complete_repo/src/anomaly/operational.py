"""Week 11 — operational analysis: from model scores to a threshold a product can ship.

The point-level false-alarm rate is the wrong number to optimise for Sentinel Prime. An operator
does not experience "13% of readings were false positives" — they experience "my phone buzzed
N times today". So this module evaluates at the ALERT level:

  * a contiguous run of above-threshold readings = ONE alert (that's what a product pages on)
  * a persistence filter (debounce) requires N consecutive readings above threshold before alerting
  * the headline metric is FALSE ALERTS PER DAY, alongside how many true events were caught

The frontier function answers the plan's question directly: for a stated recall floor, which
(threshold, persistence) setting minimises operator alert load?

All functions are causal and deterministic.
"""
from __future__ import annotations
import numpy as np
import pandas as pd


def debounce(raw_flags: np.ndarray, n: int) -> np.ndarray:
    """Persistence filter: alert only after n consecutive above-threshold readings."""
    raw_flags = np.asarray(raw_flags).astype(int)
    if n <= 1:
        return raw_flags
    out = np.zeros_like(raw_flags)
    run = 0
    for i, v in enumerate(raw_flags):
        run = run + 1 if v == 1 else 0
        out[i] = 1 if run >= n else 0
    return out


def contiguous_runs(flags: np.ndarray) -> list[tuple[int, int]]:
    """Contiguous runs of 1s -> [(start, end)] inclusive."""
    flags = np.asarray(flags).astype(int)
    out, start = [], None
    for i, v in enumerate(flags):
        if v == 1 and start is None:
            start = i
        elif v == 0 and start is not None:
            out.append((start, i - 1)); start = None
    if start is not None:
        out.append((start, len(flags) - 1))
    return out


def alert_level_stats(y_true, y_pred, timestamps):
    """Alert-level view: true events caught, false alerts raised, false alerts per day."""
    true_events = contiguous_runs(y_true)
    alerts = contiguous_runs(y_pred)

    def overlaps(a, ev):
        return not (a[1] < ev[0] or a[0] > ev[1])

    true_alerts = sum(1 for a in alerts if any(overlaps(a, ev) for ev in true_events))
    false_alerts = len(alerts) - true_alerts
    caught = sum(1 for ev in true_events if any(overlaps(a, ev) for a in alerts))

    ts = pd.to_datetime(pd.Series(timestamps))
    days = max((ts.max() - ts.min()).total_seconds() / 86400, 1e-9)

    y_true = np.asarray(y_true).astype(int); y_pred = np.asarray(y_pred).astype(int)
    tp = int(((y_pred == 1) & (y_true == 1)).sum()); fn = int(((y_pred == 0) & (y_true == 1)).sum())
    point_recall = tp / (tp + fn) if (tp + fn) else 0.0

    return {"events_caught": caught, "events_total": len(true_events),
            "alerts_total": len(alerts), "false_alerts": false_alerts,
            "false_alerts_per_day": round(false_alerts / days, 3),
            "point_recall": round(point_recall, 4), "span_days": round(days, 1)}


def frontier(y_true, scores, timestamps, recall_floor=0.80,
             persistence_levels=(1, 3, 6, 12, 24), n_grid=150):
    """For each persistence level, the lowest-alert-load threshold that still meets the recall floor.

    Returns a DataFrame sorted by false_alerts_per_day (best operating point first).
    """
    scores = np.asarray(scores, float)
    finite = np.isfinite(scores)
    scores = np.where(finite, scores, np.nanmin(scores[finite]) if finite.any() else 0.0)
    y_true = np.asarray(y_true).astype(int)
    grid = np.quantile(scores, np.linspace(0.50, 0.999, n_grid))

    rows = []
    for n in persistence_levels:
        best = None
        for t in grid:
            pred = debounce((scores >= t).astype(int), n)
            tp = int(((pred == 1) & (y_true == 1)).sum())
            fn = int(((pred == 0) & (y_true == 1)).sum())
            rec = tp / (tp + fn) if (tp + fn) else 0.0
            if rec >= recall_floor:
                st = alert_level_stats(y_true, pred, timestamps)
                cand = {"persistence_readings": n, "threshold": round(float(t), 4), **st}
                if best is None or cand["false_alerts_per_day"] < best["false_alerts_per_day"]:
                    best = cand
                break  # grid ascends: first feasible t = highest recall for this n
        if best:
            rows.append(best)
    df = pd.DataFrame(rows)
    return df.sort_values("false_alerts_per_day").reset_index(drop=True) if len(df) else df
