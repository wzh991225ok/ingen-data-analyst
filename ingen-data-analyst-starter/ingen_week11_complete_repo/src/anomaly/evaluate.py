"""Week 11 — evaluation layer.

Scores every detector on the same test split with:
  - precision / recall / F1 at a chosen operating point
  - PR curve + average precision (threshold-free, so models are compared fairly)
  - time-to-detection (TTD) per labelled anomaly EVENT
  - confusion matrix

Operating point (the operational rule, per the plan's 'operational framing' deliverable):
    Choose the threshold that MINIMISES false alarms subject to recall >= RECALL_FLOOR.
That is the real Sentinel trade-off: missing an intrusion is far worse than an extra alert, but
alert fatigue destroys the product if the false-alarm rate is unbounded. If no threshold reaches
the recall floor, we fall back to the max-recall threshold and flag it.

Time-to-detection is measured per contiguous anomaly EVENT (not per point): for each labelled
event, TTD = (first alert timestamp inside the event) - (event start). Events never flagged are
reported as misses and excluded from mean TTD (reported separately) so a model cannot look fast
by simply ignoring the hard events.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_curve, average_precision_score, confusion_matrix

RECALL_FLOOR = 0.80          # operational bar: catch >=80% of true anomaly points
FALSE_ALARM_BUDGET = 0.05    # stated budget: <=5% of normal points may raise an alert


def find_events(labels: np.ndarray) -> list[tuple[int, int]]:
    """Contiguous runs of 1s -> list of (start_idx, end_idx) inclusive."""
    labels = np.asarray(labels).astype(int)
    events, start = [], None
    for i, v in enumerate(labels):
        if v == 1 and start is None:
            start = i
        elif v == 0 and start is not None:
            events.append((start, i - 1)); start = None
    if start is not None:
        events.append((start, len(labels) - 1))
    return events


def choose_threshold(y_true, scores, recall_floor=RECALL_FLOOR):
    """Lowest-false-alarm threshold that still hits the recall floor.

    Returns (threshold, met_floor). If the floor is unreachable, returns the threshold that
    maximises recall and met_floor=False (flagged honestly rather than silently relaxed).
    """
    prec, rec, thr = precision_recall_curve(y_true, scores)
    # precision_recall_curve returns len(thr) = len(prec)-1
    prec, rec = prec[:-1], rec[:-1]
    ok = rec >= recall_floor
    if ok.any():
        # among thresholds meeting recall, the highest precision = fewest false alarms
        idx = np.argmax(np.where(ok, prec, -1))
        return float(thr[idx]), True
    return float(thr[int(np.argmax(rec))]), False


def time_to_detection(timestamps, y_true, y_pred):
    """Per-event TTD in seconds. Returns (mean_ttd_seconds, detected_events, total_events)."""
    ts = pd.to_datetime(pd.Series(timestamps)).reset_index(drop=True)
    events = find_events(y_true)
    ttds = []
    detected = 0
    for s, e in events:
        fired = np.where(np.asarray(y_pred)[s:e + 1] == 1)[0]
        if len(fired):
            detected += 1
            ttds.append((ts.iloc[s + fired[0]] - ts.iloc[s]).total_seconds())
    mean_ttd = float(np.mean(ttds)) if ttds else float("nan")
    return mean_ttd, detected, len(events)


def evaluate_model(name, dataset, timestamps, y_true, scores):
    """Full metric row for one model on one dataset."""
    y_true = np.asarray(y_true).astype(int)
    scores = np.asarray(scores, float)
    # guard against NaNs from rolling features
    finite = np.isfinite(scores)
    scores = np.where(finite, scores, np.nanmin(scores[finite]) if finite.any() else 0.0)

    thr, met = choose_threshold(y_true, scores)
    y_pred = (scores >= thr).astype(int)

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    far = fp / (fp + tn) if (fp + tn) else 0.0   # false-alarm rate on normal points
    ap = average_precision_score(y_true, scores)

    mean_ttd, det_events, tot_events = time_to_detection(timestamps, y_true, y_pred)

    return {
        "dataset": dataset, "model": name,
        "precision": round(precision, 4), "recall": round(recall, 4), "f1": round(f1, 4),
        "avg_precision": round(float(ap), 4),
        "false_alarm_rate": round(far, 4),
        "within_far_budget": bool(far <= FALSE_ALARM_BUDGET),
        "met_recall_floor": bool(met),
        "ttd_seconds": round(mean_ttd, 1) if np.isfinite(mean_ttd) else None,
        "events_detected": det_events, "events_total": tot_events,
        "threshold": round(thr, 6),
        "tp": int(tp), "fp": int(fp), "tn": int(tn), "fn": int(fn),
    }


def pr_curve_points(y_true, scores, n=200):
    """Downsampled PR curve for plotting."""
    prec, rec, _ = precision_recall_curve(y_true, scores)
    if len(prec) > n:
        idx = np.linspace(0, len(prec) - 1, n).astype(int)
        prec, rec = prec[idx], rec[idx]
    return rec, prec
