# src/forecast — Demand & Adoption Forecasting (Week 10)

Projects 24-month demand momentum per InGen vertical, plus a Bass diffusion model for humanoid adoption.

## Run
```bash
pip install -r requirements.txt
python -m src.forecast.run_forecasts   # -> data/week10/forecast_results.csv (+ forecasts, importances, bass)
python -m src.forecast.build_report    # -> reports/week10/forecast_report.pdf + charts
```

## Modules
| File | Role |
|------|------|
| `data_prep.py` | load Week 5 target series + engineer features |
| `models.py` | seasonal-naive, ETS, ARIMA, Prophet, XGBoost; MAPE/MASE; backtest |
| `bass.py` | Bass diffusion fit to cited Goldman humanoid shipment anchors |
| `run_forecasts.py` | orchestrate all models, write results CSV + importances |
| `build_report.py` | charts + 5-page forecast report |

## Notes
- Target = Week 5 search-interest momentum; backtest on last 12 months (MAPE + MASE vs naive-1).
- Best model varies by vertical (ETS / Prophet / XGBoost). Forecasts are a relative demand read, not absolute market numbers.
- Bass fit hits Goldman's 20k/2025, 250k/2030, 1.4M/2035 anchors; cross-checked vs Morgan Stanley.
