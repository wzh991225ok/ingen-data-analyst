# ingen-data-analyst — Week 11

Data Analyst Internship · Ziheng Wang · inGen Dynamics Inc.
**Week 11 — Anomaly Detection: Sentinel Prime AI Use Case** (03–09 Jul 2026)

Prototypes the anomaly-detection workflow behind Sentinel Prime AI / Aido Rover using **two real,
licensed public benchmarks** — then translates the model results into a threshold a product could
actually ship. **No InGen data is used.**

## Deliverables
| Deliverable | File |
|---|---|
| Anomaly-detection notebook | `notebooks/week11/week11_anomaly_detection.ipynb` |
| Results table | `data/week11/results.csv` |
| Sentinel operational framing (2 pages) | `reports/week11/sentinel_operational_framing.pdf` |
| Charts | `reports/week11/pr_curves.png`, `confusion_matrices.png`, `score_timeline.png`, `operational_frontier.png` |

## Data (real, licensed)
| Dataset | Series | Licence |
|---|---|---|
| NAB (Numenta) | machine_temperature_system_failure — 22,695 readings, 4 labelled failure windows | MIT |
| SKAB (Skoltech) | valve1 (8 sensors) + anomaly-free reference | GPL-3.0 |

## Models (identical splits, unsupervised)
Isolation Forest · One-Class SVM · LOF · AutoEncoder (all PyOD) · EWMA control-chart baseline.

## Findings
- **AutoEncoder** best on NAB (F1 0.555, AP 0.512); **LOF** best on SKAB (F1 0.545, AP 0.531) — both beat the control-chart baseline.
- **The 5% point-level false-alarm budget is not reachable at 80% recall** (~13% floor). That's a model-quality ceiling, not a threshold-tuning problem — reported rather than hidden.
- **Persistence filtering is the real lever:** alert only after 120 min sustained → **0.50 false alerts/day** instead of 16.35, still catching 4/4 true failures at 88% recall.
- **Adaptive thresholds lost here** — long (~2-day) anomalies contaminate any rolling baseline. Verified by parameter sweep + a baseline-freeze diagnostic. Recommend fixed + persistence, re-baselined on a schedule.
- Recommend **two-tier alerting**: a fast tier for unambiguous intrusion, a sustained tier for degradation.

## Run
```bash
pip install -r requirements.txt
python -m src.anomaly.run_all
python -m src.anomaly.build_report
python -m pytest src/anomaly/tests -q    # 12 tests incl. causality/no-leakage checks
```

## Data integrity
Real public benchmarks with licences and citations documented. Detectors are unsupervised; labels are
used only for evaluation and operating-point selection. Rolling features and adaptive thresholds are
causal (tested). Thresholds transfer as a **method, not as constants** — they must be re-derived on real
Sentinel telemetry before any field use.
