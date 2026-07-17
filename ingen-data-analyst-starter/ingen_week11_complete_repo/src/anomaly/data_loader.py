"""Week 11 — public anomaly-benchmark loaders (REAL data, downloaded from source).

Two public, licensed benchmarks relevant to Sentinel Prime AI / Aido Rover sensor telemetry:

  A) NAB — Numenta Anomaly Benchmark, realKnownCause/machine_temperature_system_failure.csv
     Real industrial machine temperature sensor, 22,695 points at 5-min cadence, with 4
     hand-labelled anomaly WINDOWS corresponding to a known machine failure.
     Source : https://github.com/numenta/NAB
     License: MIT (Copyright 2014-2024 Numenta Inc.)
     Why    : closest public analog to a single robot's telemetry channel degrading before failure.

  B) SKAB — Skoltech Anomaly Benchmark, data/valve1/*.csv
     Multivariate testbed rig: 8 sensors (accelerometers, current, pressure, temperature,
     thermocouple, voltage, flow) at 1-second cadence with per-point `anomaly` labels.
     Source : https://github.com/waico/SKAB
     License: GNU GPL v3
     Why    : multivariate sensor fusion — the shape of a real Sentinel/Rover sensor payload.

Both are cached under data/week11/raw/ after first download. Set INGEST_ALLOW_NETWORK=0 to force
cache-only. NO InGen data is used anywhere in this week (per the plan).
"""
from __future__ import annotations
import io
import json
import os
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "week11" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

NAB_BASE = "https://raw.githubusercontent.com/numenta/NAB/master"
SKAB_BASE = "https://raw.githubusercontent.com/waico/SKAB/master"

NAB_SERIES = "realKnownCause/machine_temperature_system_failure.csv"
SKAB_FILES = ["valve1/0.csv", "valve1/1.csv", "valve1/2.csv"]

DATASET_LICENSES = {
    "NAB": {
        "name": "Numenta Anomaly Benchmark (NAB)",
        "series": NAB_SERIES,
        "url": "https://github.com/numenta/NAB",
        "license": "MIT License (Copyright 2014-2024 Numenta Inc.)",
        "citation": "Lavin & Ahmad (2015), 'Evaluating Real-time Anomaly Detection Algorithms — "
                    "the Numenta Anomaly Benchmark', IEEE ICMLA.",
        "labels": "hand-labelled anomaly windows (combined_windows.json)",
    },
    "SKAB": {
        "name": "Skoltech Anomaly Benchmark (SKAB)",
        "series": ", ".join(SKAB_FILES),
        "url": "https://github.com/waico/SKAB",
        "license": "GNU General Public License v3 (GPL-3.0)",
        "citation": "Katser & Kozitsin (2020), 'Skoltech Anomaly Benchmark (SKAB)', Kaggle.",
        "labels": "per-point `anomaly` (0/1) and `changepoint` columns",
    },
}


def _fetch(url: str, dest: Path) -> Path:
    """Download to dest with caching. Raises if unavailable and not cached."""
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    if os.environ.get("INGEST_ALLOW_NETWORK", "1") != "1":
        raise RuntimeError(f"{dest.name} not cached and network disabled")
    req = urllib.request.Request(url, headers={"User-Agent": "ingen-intern-week11/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        dest.write_bytes(r.read())
    return dest


def load_nab() -> pd.DataFrame:
    """NAB machine temperature series -> DataFrame[timestamp, value, is_anomaly].

    NAB ships anomaly WINDOWS; we expand them to per-point binary labels.
    """
    data_p = _fetch(f"{NAB_BASE}/data/{NAB_SERIES}", RAW / "nab_machine_temperature.csv")
    lab_p = _fetch(f"{NAB_BASE}/labels/combined_windows.json", RAW / "nab_combined_windows.json")

    df = pd.read_csv(data_p, parse_dates=["timestamp"]).sort_values("timestamp").reset_index(drop=True)
    windows = json.loads(lab_p.read_text())[NAB_SERIES]
    df["is_anomaly"] = 0
    for start, end in windows:
        m = (df["timestamp"] >= pd.Timestamp(start)) & (df["timestamp"] <= pd.Timestamp(end))
        df.loc[m, "is_anomaly"] = 1
    df.attrs["windows"] = [(pd.Timestamp(s), pd.Timestamp(e)) for s, e in windows]
    return df


def load_skab() -> pd.DataFrame:
    """SKAB valve1 files -> DataFrame[datetime, <8 sensors>, is_anomaly].

    Files are concatenated in order; each is an independent experiment run, so a `run` column
    is kept to avoid treating the seams as real transitions.
    """
    frames = []
    for i, rel in enumerate(SKAB_FILES):
        p = _fetch(f"{SKAB_BASE}/data/{rel}", RAW / f"skab_{rel.replace('/', '_')}")
        d = pd.read_csv(p, sep=";", parse_dates=["datetime"])
        d["run"] = i
        frames.append(d)
    df = pd.concat(frames, ignore_index=True)
    df = df.rename(columns={"anomaly": "is_anomaly"})
    df["is_anomaly"] = df["is_anomaly"].fillna(0).astype(int)
    return df


def load_skab_clean() -> pd.DataFrame:
    """SKAB's shipped anomaly-free reference run — the intended clean TRAINING set.

    SKAB publishes data/anomaly-free/anomaly-free.csv specifically as a known-good baseline.
    Using it as the training set mirrors how a Sentinel unit is baselined on clean
    commissioning data before going live.
    """
    p = _fetch(f"{SKAB_BASE}/data/anomaly-free/anomaly-free.csv", RAW / "skab_anomaly_free.csv")
    d = pd.read_csv(p, sep=";", parse_dates=["datetime"])
    d["is_anomaly"] = 0
    return d


SKAB_SENSORS = ["Accelerometer1RMS", "Accelerometer2RMS", "Current", "Pressure",
                "Temperature", "Thermocouple", "Voltage", "Volume Flow RateRMS"]


def nab_features(df: pd.DataFrame) -> pd.DataFrame:
    """Turn the univariate NAB series into a small feature matrix.

    Anomaly detectors need context, not just the raw level: we add short/long rolling means,
    rolling std, and deltas — all causal (shift(1)) so no future information leaks.
    """
    x = df["value"]
    f = pd.DataFrame(index=df.index)
    f["value"] = x
    f["roll_mean_12"] = x.shift(1).rolling(12).mean()      # ~1 hour @5-min cadence
    f["roll_mean_288"] = x.shift(1).rolling(288).mean()    # ~1 day
    f["roll_std_12"] = x.shift(1).rolling(12).std()
    f["roll_std_288"] = x.shift(1).rolling(288).std()
    f["delta_1"] = x.diff(1)
    f["dev_from_day"] = x - f["roll_mean_288"]
    return f


def license_table() -> pd.DataFrame:
    rows = []
    for k, v in DATASET_LICENSES.items():
        rows.append({"dataset": k, "name": v["name"], "series_used": v["series"],
                     "url": v["url"], "license": v["license"], "labels": v["labels"],
                     "citation": v["citation"]})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    nab = load_nab()
    print(f"NAB : {len(nab):,} rows  {nab.timestamp.min()} .. {nab.timestamp.max()}  "
          f"anomaly points={int(nab.is_anomaly.sum()):,} ({nab.is_anomaly.mean()*100:.2f}%)  "
          f"windows={len(nab.attrs['windows'])}")
    skab = load_skab()
    print(f"SKAB: {len(skab):,} rows  {skab.datetime.min()} .. {skab.datetime.max()}  "
          f"anomaly points={int(skab.is_anomaly.sum()):,} ({skab.is_anomaly.mean()*100:.2f}%)  "
          f"sensors={len(SKAB_SENSORS)}  runs={skab.run.nunique()}")
    print("\nLicenses:")
    print(license_table()[["dataset", "license"]].to_string(index=False))
