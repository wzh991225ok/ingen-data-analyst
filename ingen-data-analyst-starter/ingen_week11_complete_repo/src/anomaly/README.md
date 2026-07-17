# src/anomaly — Anomaly Detection for Sentinel Prime AI (Week 11)

Public-data prototype: 5 detectors on 2 real licensed benchmarks, evaluated the way a product team
would actually have to decide a shipping threshold. **No InGen data.**

## Run
```bash
pip install -r requirements.txt
python -m src.anomaly.data_loader     # fetch + cache NAB & SKAB, print licences
python -m src.anomaly.run_all         # fit all detectors, evaluate, adaptive study, frontier
python -m src.anomaly.build_report    # charts + 2-page operational framing PDF
python -m pytest src/anomaly/tests -q # 12 tests
```

## Modules
| File | Role |
|---|---|
| `data_loader.py` | download/cache NAB + SKAB; build causal features; licence table |
| `models.py` | IForest, OCSVM, LOF, AutoEncoder (PyOD) + EWMA control-chart baseline |
| `evaluate.py` | PR curve, precision/recall/F1/AP, TTD, confusion matrix, operating-point rule |
| `adaptive_threshold.py` | rolling-quantile, EWMA-sigma, baseline-freeze variants vs fixed |
| `operational.py` | persistence filter + alert-level frontier (false alerts/day) |
| `run_all.py` | orchestrates everything -> data/week11/*.csv |
| `build_report.py` | charts + 2-page Sentinel operational framing |

## Findings in one line
Fixed threshold + a 120-minute persistence filter → 4/4 real failures caught at 88% recall with
**0.50 false alerts/day** (33× fewer than unfiltered). Adaptive thresholds lose on sustained anomalies
because the anomaly contaminates its own rolling baseline.
