# Data Dictionary — Week 10

## Outputs (data/week10/)
| File | Schema |
|------|--------|
| forecast_results.csv | vertical, product, model, MAPE, MASE, est_12m, est_24m, is_best, note |
| forecasts_<vertical>.csv | vertical, model, date (YYYY-MM), yhat |
| xgb_importances.csv | vertical, feature, importance |
| bass_humanoid.csv | year, annual_shipments, cumulative_installed |
| bass_params.txt | fitted p, q, M |

## Target & features
- **Target:** monthly search-interest momentum per vertical (Week 5 Google-Trends signal, 0-100, ~60 months).
- **Features (XGBoost):** own lags (1,2,3,6,12), rolling means (3,6), momentum (3m, 12m), calendar (month, sin/cos, trend),
  news volume/tone (Week 5, where available; median-filled + availability flag), static peer-funding intensity (Week 6).
- **Macro:** documented extension point (FRED) for a networked run — not fabricated here.

## Metrics
- **MAPE** = mean absolute percentage error on the 12-month holdout.
- **MASE** = MAE(test) / in-sample naive-1 MAE. MASE < 1 beats the naive benchmark.

## Bass diffusion (humanoid)
Cumulative F(t) = (1 - e^-(p+q)t)/(1 + (q/p)e^-(p+q)t); annual shipments = M·f(t). Fit in log-space to Goldman
anchors (2025≈20k, 2030≈250k, 2035≈1.4M). Source: Goldman Sachs Research, Jan 2024. Morgan Stanley (Apr 2025,
13M in service by 2035) used as an upper-scenario cross-check.

## Honesty
Series originate from Week 5 (real collectors + labelled synthetic fallbacks where live APIs were unreachable).
Forecasts are a relative demand read, not absolute unit/market forecasts.
