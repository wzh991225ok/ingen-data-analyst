"""Week 10 — forecasting models + validation.

Models per vertical: seasonal-naive, ETS, ARIMA (baselines); Prophet and XGBoost (stronger).
Validation: hold out the last HOLDOUT months; compute MAPE and MASE on that test window.
MASE denominator = in-sample naive-1 (random-walk) MAE, the standard scaling.

Everything is wrapped in try/except so one model failing never blocks the others; failures are
recorded rather than crashing the run.
"""
from __future__ import annotations
import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error
import xgboost as xgb

from .data_prep import build_features, load_target

HOLDOUT = 12
HORIZON = 24


def mape(y_true, y_pred):
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    mask = y_true != 0
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100)


def mase(y_true, y_pred, y_train):
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    naive = np.mean(np.abs(np.diff(np.asarray(y_train, float))))  # in-sample naive-1 MAE
    if naive == 0:
        return float("nan")
    return float(mean_absolute_error(y_true, y_pred) / naive)


# ---------- individual models: return (test_pred[HOLDOUT], future_pred[HORIZON]) ----------

def m_seasonal_naive(y, train, test):
    m = 12
    hist = list(train.values)
    testp = [hist[-m + i] if len(hist) >= m else hist[-1] for i in range(len(test))]
    full = list(y.values)
    fut = [full[-m + (i % m)] for i in range(HORIZON)]
    return np.array(testp), np.array(fut)


def m_ets(y, train, test):
    fit = ExponentialSmoothing(train, trend="add", seasonal="add", seasonal_periods=12,
                               initialization_method="estimated").fit()
    testp = fit.forecast(len(test)).values
    fitfull = ExponentialSmoothing(y, trend="add", seasonal="add", seasonal_periods=12,
                                   initialization_method="estimated").fit()
    fut = fitfull.forecast(HORIZON).values
    return testp, fut


def m_arima(y, train, test):
    order = (2, 1, 2)
    testp = ARIMA(train, order=order).fit().forecast(len(test)).values
    fut = ARIMA(y, order=order).fit().forecast(HORIZON).values
    return testp, fut


def m_prophet(y, train, test):
    from prophet import Prophet
    def fit_predict(train_series, periods):
        d = train_series.reset_index(); d.columns = ["ds", "y"]
        mdl = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False,
                      seasonality_mode="additive")
        mdl.fit(d)
        fut = mdl.make_future_dataframe(periods=periods, freq="MS")
        return mdl.predict(fut)["yhat"].values[-periods:]
    testp = fit_predict(train, len(test))
    fut = fit_predict(y, HORIZON)
    return testp, fut


def m_xgboost(vertical, y, train, test):
    feats = build_features(vertical).dropna()
    X = feats.drop(columns=["y"]); yv = feats["y"]
    split = yv.index[-len(test)] if len(test) < len(yv) else yv.index[len(yv) // 2]
    Xtr, ytr = X[X.index < split], yv[yv.index < split]
    Xte = X[X.index >= split]
    model = xgb.XGBRegressor(n_estimators=300, max_depth=3, learning_rate=0.05,
                             subsample=0.9, colsample_bytree=0.9, random_state=42)
    model.fit(Xtr, ytr)
    testp = model.predict(Xte)[:len(test)]
    # recursive multi-step future using the fitted model on full data
    modelf = xgb.XGBRegressor(n_estimators=300, max_depth=3, learning_rate=0.05,
                              subsample=0.9, colsample_bytree=0.9, random_state=42)
    modelf.fit(X, yv)
    importances = pd.Series(modelf.feature_importances_, index=X.columns).sort_values(ascending=False)
    fut = _recursive_future(vertical, modelf, X.columns)
    if len(testp) < len(test):
        testp = np.concatenate([testp, np.repeat(testp[-1], len(test) - len(testp))])
    return testp, fut, importances


def _recursive_future(vertical, model, cols):
    """Roll the target forward HORIZON steps, rebuilding features each step."""
    y = load_target(vertical).copy()
    news = None
    from .data_prep import load_news, FUNDING_INTENSITY
    news = load_news(vertical)
    nv = news["news_volume"].median() if "news_volume" in news else 0.0
    nt = news["news_tone"].median() if "news_tone" in news else 0.0
    fund = FUNDING_INTENSITY[vertical]
    preds = []
    hist = y.copy()
    for step in range(HORIZON):
        idx = hist.index[-1] + pd.offsets.MonthBegin(1)
        row = {}
        for lag in (1, 2, 3, 6, 12):
            row[f"lag_{lag}"] = hist.iloc[-lag] if len(hist) >= lag else hist.iloc[-1]
        row["roll_mean_3"] = hist.iloc[-3:].mean()
        row["roll_mean_6"] = hist.iloc[-6:].mean()
        row["momentum_3"] = hist.iloc[-1] - (hist.iloc[-4] if len(hist) >= 4 else hist.iloc[-1])
        row["momentum_12"] = hist.iloc[-1] - (hist.iloc[-13] if len(hist) >= 13 else hist.iloc[-1])
        row["month"] = idx.month
        row["month_sin"] = np.sin(2 * np.pi * idx.month / 12)
        row["month_cos"] = np.cos(2 * np.pi * idx.month / 12)
        row["trend"] = len(y) + step
        row["news_volume"] = nv; row["news_tone"] = nt; row["news_available"] = 0
        row["funding_intensity"] = fund
        xrow = pd.DataFrame([row])[list(cols)]
        pred = float(model.predict(xrow)[0])
        pred = max(0, min(100, pred))
        preds.append(pred)
        hist = pd.concat([hist, pd.Series([pred], index=[idx])])
    return np.array(preds)
