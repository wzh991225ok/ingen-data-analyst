# Week 10 — Predictive Modeling: Adoption & Demand Forecasting
**Dates:** 26 Jun – 02 Jul 2026 · **Phase 4 — Advanced Analytics** · 25 hrs

## Tasks
- Problem framing: Week 5 demand signals → one forecasting task per vertical (search-interest momentum target).
- Baselines: seasonal-naive, ETS, ARIMA with train/test split + backtest.
- Stronger models: Prophet + XGBoost (engineered features: lags, search momentum, news cadence/tone, peer funding). Compare on MAPE + MASE.
- Adoption curve: Bass diffusion for humanoid, anchored to cited Goldman Sachs shipment guidance.
- Forecast report: 5 pages, one per vertical (point forecast, CI, drivers, analyst cross-check).

## Deliverables
- [x] Forecasting notebook -> notebooks/week10_forecasting.ipynb
- [x] Forecast results table -> data/week10/forecast_results.csv (vertical, model, MAPE, MASE, 12m, 24m)
- [x] 5-page forecast report -> reports/week10/forecast_report.pdf
- [x] Supporting: xgb_importances.csv, bass_humanoid.csv, per-vertical forecasts + charts

## Success criteria
- [x] Every forecast has a documented model, train/test split, validation metric (MAPE + MASE, 12-month holdout)
- [x] XGBoost feature importances reported and discussed (per vertical, in report + CSV)
- [x] Humanoid Bass-diffusion fit justified with cited shipment guidance (Goldman Sachs Jan 2024: 20k/2025 → 250k/2030 → 1.4M/2035)
- [x] Forecasts cross-checked against external analyst projections where they exist (humanoid: Goldman + Morgan Stanley)

## Honesty note
Target series come from Week 5 (real collectors + labelled synthetic fallbacks where live APIs were
unreachable). The forecasting methodology is real and reproducible; a live Week 5 run feeds the same
pipeline with real data. Forecasts are a RELATIVE demand-momentum read (search-interest index), not
absolute unit/market forecasts — validate against internal data before planning. Macro (FRED) features
are a documented extension point for a networked run, not fabricated here.
