"""Week 10 — run all forecasts, produce the results table + saved forecasts + feature importances.

For each vertical: backtest each model on the last HOLDOUT months (MAPE, MASE), then fit on the full
series to produce 24-month forward point estimates. Best model per vertical (lowest MASE) is flagged.
Humanoid additionally gets the Bass-diffusion adoption projection.

Outputs to data/week10/:
  forecast_results.csv         (vertical, model, MAPE, MASE, est_12m, est_24m, is_best)
  forecasts_<vertical>.csv     (date, model, yhat) for plotting
  xgb_importances.csv          (vertical, feature, importance)
  bass_humanoid.csv            (year, annual_shipments, cumulative_installed)
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

from . import models as M
from .data_prep import VERTICALS, PRODUCT, load_target
from .bass import project as bass_project, fit_bass

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "week10"
DATA.mkdir(parents=True, exist_ok=True)
HOLDOUT, HORIZON = M.HOLDOUT, M.HORIZON


def run_vertical(vertical):
    y = load_target(vertical)
    train, test = y.iloc[:-HOLDOUT], y.iloc[-HOLDOUT:]
    results, forecasts, importances = [], [], None
    future_index = pd.date_range(y.index[-1] + pd.offsets.MonthBegin(1), periods=HORIZON, freq="MS")

    specs = [
        ("Seasonal naive", lambda: M.m_seasonal_naive(y, train, test)),
        ("ETS", lambda: M.m_ets(y, train, test)),
        ("ARIMA", lambda: M.m_arima(y, train, test)),
        ("Prophet", lambda: M.m_prophet(y, train, test)),
    ]
    for name, fn in specs:
        try:
            testp, fut = fn()
            results.append(_score(vertical, name, test, testp, train, fut))
            forecasts += _fc_rows(vertical, name, future_index, fut)
        except Exception as e:  # noqa: BLE001
            results.append({"vertical": vertical, "product": PRODUCT[vertical], "model": name,
                            "MAPE": np.nan, "MASE": np.nan, "est_12m": np.nan, "est_24m": np.nan,
                            "note": f"failed: {str(e)[:40]}"})
    # XGBoost (returns importances too)
    try:
        testp, fut, imp = M.m_xgboost(vertical, y, train, test)
        results.append(_score(vertical, "XGBoost", test, testp, train, fut))
        forecasts += _fc_rows(vertical, "XGBoost", future_index, fut)
        importances = imp
    except Exception as e:  # noqa: BLE001
        results.append({"vertical": vertical, "product": PRODUCT[vertical], "model": "XGBoost",
                        "MAPE": np.nan, "MASE": np.nan, "est_12m": np.nan, "est_24m": np.nan,
                        "note": f"failed: {str(e)[:40]}"})
    return results, forecasts, importances


def _score(vertical, name, test, testp, train, fut):
    testp = np.asarray(testp, float)[:len(test)]
    return {"vertical": vertical, "product": PRODUCT[vertical], "model": name,
            "MAPE": round(M.mape(test.values, testp), 2),
            "MASE": round(M.mase(test.values, testp, train.values), 3),
            "est_12m": round(float(fut[11]), 1) if len(fut) > 11 else np.nan,
            "est_24m": round(float(fut[23]), 1) if len(fut) > 23 else np.nan, "note": ""}


def _fc_rows(vertical, name, idx, fut):
    return [{"vertical": vertical, "model": name, "date": d.strftime("%Y-%m"), "yhat": round(float(v), 2)}
            for d, v in zip(idx, fut)]


def main():
    all_results, all_fc, all_imp = [], [], []
    for v in VERTICALS:
        print(f"forecasting {v} ...")
        res, fc, imp = run_vertical(v)
        # flag best by MASE (lower better)
        valid = [r for r in res if not np.isnan(r["MASE"])]
        best = min(valid, key=lambda r: r["MASE"])["model"] if valid else None
        for r in res:
            r["is_best"] = (r["model"] == best)
        all_results += res; all_fc += fc
        if imp is not None:
            for feat, val in imp.items():
                all_imp.append({"vertical": v, "feature": feat, "importance": round(float(val), 4)})
        pd.DataFrame(fc).to_csv(DATA / f"forecasts_{v}.csv", index=False)

    rdf = pd.DataFrame(all_results)[["vertical", "product", "model", "MAPE", "MASE", "est_12m", "est_24m", "is_best", "note"]]
    rdf.to_csv(DATA / "forecast_results.csv", index=False)
    pd.DataFrame(all_imp).to_csv(DATA / "xgb_importances.csv", index=False)

    params, rows = bass_project()
    bdf = pd.DataFrame(rows); bdf.to_csv(DATA / "bass_humanoid.csv", index=False)
    (DATA / "bass_params.txt").write_text(f"p={params['p']:.4f} q={params['q']:.3f} M={params['M']:.0f}\n")

    print("\n=== Forecast results (backtest on last 12 months) ===")
    print(rdf.to_string(index=False))
    print(f"\nBass humanoid: p={params['p']:.4f} q={params['q']:.3f} M={params['M']:,.0f}")
    print("Saved: forecast_results.csv, forecasts_<vertical>.csv, xgb_importances.csv, bass_humanoid.csv")
    return rdf


if __name__ == "__main__":
    main()
