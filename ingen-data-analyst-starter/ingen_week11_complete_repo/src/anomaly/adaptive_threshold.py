"""Week 11 — adaptive threshold prototype vs the fixed baseline.

Why this matters for Sentinel Prime: a threshold calibrated at commissioning goes stale. Ambient
conditions drift (seasons, a new HVAC unit, a busier lobby), and a fixed cut-off that was well
tuned in March quietly turns into either an alert firehose or a blind spot by August. An adaptive
threshold re-baselines itself against recent behaviour, so the alert rate stays roughly stable
without an engineer re-tuning each site by hand.

Two adaptive schemes, both CAUSAL (only past data, shift(1)) so there is no look-ahead leakage:

  rolling_quantile : threshold_t = q-th quantile of the last W scores
  ewma_sigma       : threshold_t = ewma_t + k * ewma_sigma_t   (control-chart style, on scores)

Both are compared to the fixed threshold chosen by the operational rule in evaluate.py, on the
same model scores and the same labels — so the comparison is quantitative, not directional.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix

from .evaluate import time_to_detection


def rolling_quantile_threshold(scores, window=1000, q=0.98, warmup_value=None):
    """Causal rolling-quantile threshold."""
    s = pd.Series(np.asarray(scores, float))
    thr = s.shift(1).rolling(window, min_periods=max(30, window // 10)).quantile(q)
    fill = warmup_value if warmup_value is not None else s.iloc[:max(30, window // 10)].quantile(q)
    return thr.fillna(fill).to_numpy()


def ewma_sigma_threshold(scores, alpha=0.01, k=3.0, warmup=200):
    """Causal EWMA + k-sigma threshold on the score stream."""
    s = pd.Series(np.asarray(scores, float))
    ewma = s.shift(1).ewm(alpha=alpha, adjust=False).mean()
    ewsd = s.shift(1).ewm(alpha=alpha, adjust=False).std()
    thr = ewma + k * ewsd
    fill = float(s.iloc[:warmup].mean() + k * s.iloc[:warmup].std())
    return thr.fillna(fill).to_numpy()


def freeze_baseline_threshold(scores, window=1000, q=0.98, warmup=200):
    """Rolling-quantile threshold whose baseline EXCLUDES points it flagged.

    Motivation: the naive rolling quantile silently absorbs long anomalies into its own baseline
    (NAB's windows are ~2 days = ~576 readings), so the threshold rises exactly when it should
    stay put. Freezing the baseline during an alert removes that self-contamination. Returns
    hard predictions (the threshold is state-dependent, so it cannot be precomputed as an array).
    """
    scores = np.asarray(scores, float)
    n = len(scores)
    clean = list(scores[:warmup])
    base = float(np.quantile(clean, q)) if clean else 0.0
    pred = np.zeros(n, int)
    for t in range(n):
        thr = float(np.quantile(clean[-window:], q)) if len(clean) >= 30 else base
        if scores[t] >= thr:
            pred[t] = 1            # flagged -> withhold from the baseline
        else:
            clean.append(scores[t])
    return pred


def _metrics(timestamps, y_true, y_pred, label):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    far = fp / (fp + tn) if (fp + tn) else 0.0
    mean_ttd, det, tot = time_to_detection(timestamps, y_true, y_pred)
    return {"scheme": label, "precision": round(precision, 4), "recall": round(recall, 4),
            "f1": round(f1, 4), "false_alarm_rate": round(far, 4),
            "ttd_seconds": round(mean_ttd, 1) if np.isfinite(mean_ttd) else None,
            "events_detected": det, "events_total": tot,
            "tp": int(tp), "fp": int(fp), "tn": int(tn), "fn": int(fn)}


def compare(timestamps, y_true, scores, fixed_threshold, window=1000, q=0.98, alpha=0.01, k=3.0):
    """Fixed vs rolling-quantile vs EWMA-sigma on identical scores/labels."""
    scores = np.asarray(scores, float)
    y_true = np.asarray(y_true).astype(int)
    rows = [
        _metrics(timestamps, y_true, (scores >= fixed_threshold).astype(int), "Fixed threshold"),
        _metrics(timestamps, y_true,
                 (scores >= rolling_quantile_threshold(scores, window, q)).astype(int),
                 f"Adaptive — rolling quantile (W={window}, q={q})"),
        _metrics(timestamps, y_true,
                 (scores >= ewma_sigma_threshold(scores, alpha, k)).astype(int),
                 f"Adaptive — EWMA + {k}sigma (alpha={alpha})"),
        _metrics(timestamps, y_true,
                 freeze_baseline_threshold(scores, window, q),
                 f"Adaptive — rolling quantile + baseline freeze (W={window}, q={q})"),
    ]
    return pd.DataFrame(rows)
