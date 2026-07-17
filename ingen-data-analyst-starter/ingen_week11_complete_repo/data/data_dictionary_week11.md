# Data Dictionary — Week 11

## Sources (REAL public data — no InGen data used)
| Dataset | URL | Licence | Labels |
|---|---|---|---|
| NAB (Numenta Anomaly Benchmark) | https://github.com/numenta/NAB | MIT (Copyright 2014-2024 Numenta Inc.) | hand-labelled anomaly windows (combined_windows.json) |
| SKAB (Skoltech Anomaly Benchmark) | https://github.com/waico/SKAB | GNU GPL v3 | per-point `anomaly` + `changepoint` |

Cached raw files land in `data/week11/raw/` on first run.

## Outputs (data/week11/)
| File | Schema |
|---|---|
| results.csv | dataset, model, precision, recall, f1, avg_precision, false_alarm_rate, within_far_budget, met_recall_floor, ttd_seconds, events_detected, events_total, threshold, tp, fp, tn, fn |
| pr_curves.csv | dataset, model, recall, precision |
| adaptive_threshold.csv | dataset, model, scheme, precision, recall, f1, false_alarm_rate, ttd_seconds, events_detected, events_total, tp, fp, tn, fn |
| operational_frontier.csv | dataset, model, persistence_readings, threshold, events_caught, events_total, alerts_total, false_alerts, false_alerts_per_day, point_recall, span_days |
| dataset_licenses.csv | dataset, name, series_used, url, license, labels, citation |
| scores_nab.csv / scores_skab.csv | timestamp, is_anomaly, <one column of scores per model> |

## Splits (identical for every model)
- **NAB:** train = all readings BEFORE the first labelled window (clean warm-up, mirrors commissioning); test = the rest.
- **SKAB:** train = the shipped anomaly-free reference run; test = valve1 experiment runs.
- Detectors are **unsupervised** — labels are used only to evaluate and to pick the operating point.

## Metrics
- **precision / recall / F1** at the chosen operating point; **average precision** is threshold-free (fair model comparison).
- **false_alarm_rate** = FP / (FP + TN) on normal points.
- **ttd_seconds** = mean time from a labelled event's start to the first alert inside it (missed events excluded and reported separately).
- **false_alerts_per_day** = alert-level metric: one alert per contiguous run, the number an operator actually experiences.

## Operating-point rule
Minimise false alarms subject to **recall >= 80%** (RECALL_FLOOR). Stated **false-alarm budget = 5%** (FALSE_ALARM_BUDGET).
Determinism: random_state=42 throughout.
