"""Week 10 — data prep & feature engineering for demand forecasting.

Target series: monthly Google-Trends search interest per vertical from Week 5 (the demand-momentum
signal), 0-100, ~60 months. Features for the ML model: own lags, rolling momentum, calendar, news
cadence/tone (Week 5, where available), and a static peer-funding intensity per vertical (Week 6).

Honesty: the Week 5 series were produced with real collectors against real APIs, using labelled
synthetic fallbacks where the sandbox couldn't reach the live sources. The forecasting methodology
here is real and reproducible; a live Week 5 run feeds the same pipeline with real data.
Macro (FRED) indicators are a documented extension point for a networked run — not fabricated here.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
W5 = Path("/home/claude/src8910/ingen_week5_complete_repo/data/week05")
DATA = ROOT / "data" / "week10"
DATA.mkdir(parents=True, exist_ok=True)

VERTICALS = ["eldercare", "education", "indoor_security", "outdoor_patrol", "humanoid"]
PRODUCT = {"eldercare": "Fari", "education": "Senpai", "indoor_security": "Sentinel Prime AI",
           "outdoor_patrol": "Aido Rover", "humanoid": "Aido Humanoid"}
# static peer-funding intensity proxy per vertical (Week 6): humanoid privates are funded far ahead
# of the others; used as a single static regressor. 0-1 scale, documented.
FUNDING_INTENSITY = {"humanoid": 1.00, "indoor_security": 0.45, "outdoor_patrol": 0.40,
                     "eldercare": 0.35, "education": 0.25}


def load_target(vertical: str) -> pd.Series:
    df = pd.read_csv(W5 / "search_interest_long.csv")
    s = df[df.vertical == vertical].copy()
    s["ds"] = pd.to_datetime(s["date"] + "-01")
    s = s.sort_values("ds").set_index("ds")["value"].astype(float)
    s.index.freq = "MS"
    return s


def load_news(vertical: str) -> pd.DataFrame:
    df = pd.read_csv(W5 / "news_signals_long.csv")
    n = df[df.vertical == vertical].copy()
    n["ds"] = pd.to_datetime(n["date"] + "-01")
    piv = n.pivot_table(index="ds", columns="signal_type", values="value")
    return piv  # columns: news_volume, news_tone (last ~24 months)


def build_features(vertical: str) -> pd.DataFrame:
    """Feature frame aligned to the target index for the ML model."""
    y = load_target(vertical).rename("y")
    df = y.to_frame()
    # own lags
    for lag in (1, 2, 3, 6, 12):
        df[f"lag_{lag}"] = y.shift(lag)
    # rolling momentum (search)
    df["roll_mean_3"] = y.shift(1).rolling(3).mean()
    df["roll_mean_6"] = y.shift(1).rolling(6).mean()
    df["momentum_3"] = y.shift(1) - y.shift(4)      # 3-month change
    df["momentum_12"] = y.shift(1) - y.shift(13)    # yoy change
    # calendar
    df["month"] = df.index.month
    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
    df["trend"] = np.arange(len(df))
    # news cadence / tone (where available; median-fill + availability flag)
    news = load_news(vertical)
    df = df.join(news)
    df["news_available"] = df["news_volume"].notna().astype(int)
    for c in ("news_volume", "news_tone"):
        if c in df:
            df[c] = df[c].fillna(df[c].median())
        else:
            df[c] = 0.0
    # static funding intensity
    df["funding_intensity"] = FUNDING_INTENSITY[vertical]
    return df


if __name__ == "__main__":
    for v in VERTICALS:
        y = load_target(v)
        print(f"{v:16s} {PRODUCT[v]:18s} months={len(y)}  range={y.index.min():%Y-%m}..{y.index.max():%Y-%m}  last={y.iloc[-1]:.0f}")
