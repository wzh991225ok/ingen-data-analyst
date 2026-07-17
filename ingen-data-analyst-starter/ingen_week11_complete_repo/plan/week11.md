# Week 11 — Anomaly Detection: Sentinel Prime AI Use Case
**Dates:** 03 Jul – 09 Jul 2026 · **Phase 4 — Advanced Analytics** · 25 hrs

## Tasks
- Dataset selection: 2 public anomaly benchmarks relevant to security/perimeter robotics.
- Model comparison: Isolation Forest, One-Class SVM, LOF, AutoEncoder (PyOD) + control-chart baseline.
- Evaluation: precision, recall, F1, time-to-detection; confusion matrix per model; PR curve.
- Operational framing: threshold that minimises false-alarm fatigue while holding recall above a stated bar.
- Adaptive-threshold sketch (rolling quantile / EWMA) vs fixed, quantitatively compared.

## Deliverables
- [x] Anomaly-detection notebook -> notebooks/week11/week11_anomaly_detection.ipynb
- [x] Results table -> data/week11/results.csv (model, dataset, precision, recall, F1, TTD, +AP/FAR/confusion)
- [x] Sentinel Prime operational framing -> reports/week11/sentinel_operational_framing.pdf (2 pages)
- [x] Supporting: pr_curves.png, confusion_matrices.png, score_timeline.png, operational_frontier.png,
      adaptive_threshold.csv, operational_frontier.csv, dataset_licenses.csv

## Success criteria
- [x] At least 4 models compared on the same dataset with identical splits — **5 models**, both datasets, identical splits
- [x] Operational framing explicitly states the recall floor (80%) and false-alarm budget (5%)
- [x] Adaptive threshold prototype reproducible and quantitatively compared to the fixed baseline
- [x] Licence of every dataset documented — NAB (MIT), SKAB (GPL-3.0), with citations

## Data (REAL public benchmarks — no InGen data)
| Dataset | Series | Rows | Labels | Licence |
|---|---|---|---|---|
| NAB (Numenta) | realKnownCause/machine_temperature_system_failure | 22,695 | 4 labelled failure windows | MIT |
| SKAB (Skoltech) | valve1/0–2 + anomaly-free reference | 3,367 test / 9,405 clean train | per-point anomaly | GPL-3.0 |

## Headline findings
- **AutoEncoder** best on NAB (F1 0.555, AP 0.512); **LOF** best on SKAB (F1 0.545, AP 0.531). Both beat the control-chart baseline.
- **The 5% point-level false-alarm budget is NOT reachable at 80% recall** (bottoms out ~13%) — a model-quality ceiling, not a tuning problem. Documented honestly.
- **Persistence filtering is the win:** a 120-min sustained rule cuts false alerts 33× (16.35 → 0.50/day) while recall *rises* to 88% and all 4/4 true failures are still caught.
- **Adaptive thresholds lost** — and the reason is instructive: NAB's ~2-day windows contaminate any rolling baseline. Verified with a parameter sweep and a baseline-freeze diagnostic.

## Honesty note
Findings transfer to Sentinel Prime as a **method, not as calibrated constants** — thresholds are fitted to
NAB's machine-temperature signal and must be re-derived on real Sentinel telemetry before field use.
