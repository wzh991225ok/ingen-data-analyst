# Week 10 — Status
**Phase 4 · 26 Jun – 02 Jul 2026**

## Done
- [x] Forecasting pipeline: 5 models × 5 verticals, backtested (MAPE + MASE on 12-month holdout)
- [x] Baselines (seasonal-naive, ETS, ARIMA) + Prophet + XGBoost with engineered features
- [x] XGBoost feature importances per vertical (reported + discussed)
- [x] Bass diffusion for humanoid, fit to cited Goldman anchors (20k/250k/1.4M), hits all three
- [x] Analyst cross-checks (humanoid: Goldman $38B/1.4M units 2035; Morgan Stanley 13M in service 2035)
- [x] 5-page forecast report (one per vertical) + results CSV + notebook

## Best model per vertical (by MASE)
- eldercare → ETS · education → Prophet · indoor_security → XGBoost · outdoor_patrol → Prophet · humanoid → ETS

## Run
```bash
python -m src.forecast.run_forecasts     # results CSV + forecasts + importances + bass
python -m src.forecast.build_report      # charts + 5-page PDF
```

## To strengthen (next / with resources)
- Feed a live Week 5 run (real Trends/GDELT) into the same pipeline.
- Add FRED macro features in a networked environment.
- Validate against internal sales/pilot data (the mid-internship ask).
