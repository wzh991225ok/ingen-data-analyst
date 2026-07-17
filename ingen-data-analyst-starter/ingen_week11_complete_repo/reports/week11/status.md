# Week 11 — Status
**Phase 4 · 03–09 Jul 2026**

## Done
- [x] Two REAL public benchmarks downloaded from source with licences documented (NAB — MIT; SKAB — GPL-3.0)
- [x] 5 detectors on identical splits, both datasets (4 PyOD + EWMA control-chart baseline)
- [x] precision / recall / F1 / average-precision / false-alarm-rate / time-to-detection per model
- [x] Confusion matrix per model + PR curves
- [x] Adaptive threshold study: rolling quantile, EWMA-sigma, and a baseline-freeze variant vs fixed
- [x] Operational frontier (alert-level) + 2-page Sentinel operational framing PDF
- [x] 12 passing tests (incl. causality checks — no look-ahead leakage in rolling features/thresholds)

## Key numbers
- NAB: AutoEncoder F1 0.555 / AP 0.512 · SKAB: LOF F1 0.545 / AP 0.531 · both beat the baseline
- Recommended operating point: score >= 2.16 sustained for 120 min -> 4/4 events caught, 88% recall, **0.50 false alerts/day** (vs 16.35 unfiltered)
- Point-level 5% false-alarm budget unreachable at 80% recall (~13% floor) — reported as an honest gap

## Run
```bash
python -m src.anomaly.run_all        # downloads (cached), fits, evaluates, writes CSVs
python -m src.anomaly.build_report   # charts + 2-page PDF
python -m pytest src/anomaly/tests -q
```

## Next (Week 12)
- Business-process optimization on the Week 7 warehouse (cycle time, Pareto, driver regression, capacity simulation).
