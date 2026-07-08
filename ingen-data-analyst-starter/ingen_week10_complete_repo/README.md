# ingen-data-analyst — Week 10

Data Analyst Internship · Ziheng Wang · inGen Dynamics Inc.
**Week 10 — Predictive Modeling: Adoption & Demand Forecasting** (26 Jun – 02 Jul 2026)

First week of Phase 4. Projects 24-month demand momentum for each of the five verticals using baseline
and ML forecasters, and models humanoid adoption with a Bass diffusion curve anchored to cited analyst
shipment guidance.

## Deliverables
| Deliverable | File |
|-------------|------|
| Forecasting notebook | `notebooks/week10_forecasting.ipynb` |
| Forecast results table | `data/week10/forecast_results.csv` |
| 5-page forecast report | `reports/week10/forecast_report.pdf` |
| Feature importances / Bass / forecasts | `data/week10/xgb_importances.csv`, `bass_humanoid.csv`, `forecasts_*.csv` |

## Method
- **Target:** Week 5 search-interest momentum per vertical (~60 months).
- **Models:** seasonal-naive, ETS, ARIMA (baselines) + Prophet + XGBoost (engineered features). Backtest on the last 12 months (MAPE + MASE vs naive-1).
- **Humanoid:** Bass diffusion fit to Goldman Sachs shipment anchors (20k/2025 → 250k/2030 → 1.4M/2035); cross-checked vs Morgan Stanley (13M in service by 2035).

## Results (best model by MASE)
eldercare → ETS · education → Prophet · indoor_security → XGBoost · outdoor_patrol → Prophet · humanoid → ETS. MASE < 1 beats the naive benchmark.

## Data integrity
- Series come from Week 5 (real collectors + labelled synthetic fallbacks where live APIs were unreachable); the methodology is real and reproducible.
- Forecasts are a **relative demand-momentum read** (search-interest index), not absolute unit/market forecasts — validate against internal data before planning.
- Humanoid Bass anchors and analyst cross-checks are cited; macro (FRED) features are a documented extension point, not fabricated.

Details: `data/data_dictionary_week10.md`.
