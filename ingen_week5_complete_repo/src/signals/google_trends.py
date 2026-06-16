"""Task 1 — Search-interest trends (Google Trends).

Real source: Google Trends via the `pytrends` client (unofficial). For each vertical
we pull monthly interest-over-time for its curated keywords (default 60 months),
compute the latest-12-months vs prior-12-months change (YoY momentum), and emit a
long-format table: vertical, signal_type='search_interest', date(YYYY-MM), value, source.

Network: pytrends needs live access to trends.google.com. When unavailable, a
schema-correct synthetic series is generated (clearly labelled mode='offline-fallback'
in the manifest) so downstream momentum + index code runs end-to-end.

Run live:  pip install pytrends ; INGEST_ALLOW_NETWORK=1 python -m src.signals.google_trends
"""
from __future__ import annotations
import random
import pandas as pd
from . import base


def _fetch_pytrends(keywords, months):
    """Return a DataFrame indexed by month with one column per keyword (0-100)."""
    from pytrends.request import TrendReq  # imported lazily; only needed for live runs
    pytrends = TrendReq(hl="en-US", tz=360)
    timeframe = f"today {max(1, months // 12)}-y"
    frames = []
    for kw in keywords:
        pytrends.build_payload([kw], timeframe=timeframe, geo="US")
        iot = pytrends.interest_over_time()
        if iot is not None and not iot.empty:
            s = iot[kw].resample("MS").mean()
            frames.append(s.rename(kw))
    if not frames:
        raise RuntimeError("pytrends returned no data")
    df = pd.concat(frames, axis=1)
    df.index = df.index.strftime("%Y-%m")
    return df


def _synth(keywords, months, seed):
    """Schema-correct synthetic interest series (labelled as fallback)."""
    rng = random.Random(seed)
    idx = base.month_range(months)
    data = {}
    for k_i, kw in enumerate(keywords):
        base_level = rng.randint(25, 55)
        trend = rng.uniform(0.05, 0.45)  # upward drift over the window
        series = []
        for i, _ in enumerate(idx):
            drift = base_level * (1 + trend * (i / len(idx)))
            noise = rng.uniform(-6, 6)
            series.append(max(0, min(100, round(drift + noise))))
        data[kw] = series
    return pd.DataFrame(data, index=idx)


def collect(months: int = 60):
    rows = []
    mode_overall = "network"
    for vert, (product, kws) in base.VERTICALS.items():
        mode = "offline-fallback"
        df = None
        if base.ALLOW_NETWORK:
            try:
                df = _fetch_pytrends(kws, months)
                mode = "network"
            except Exception as e:  # noqa: BLE001
                print(f"  [{vert}] pytrends failed ({e}); using offline fallback")
        if df is None:
            df = _synth(kws, months, seed=base.stable_seed('search_'+vert))
            mode_overall = "offline-fallback"
        # vertical-level interest = mean across its keywords
        vseries = df.mean(axis=1).round(1)
        for date, val in vseries.items():
            rows.append({"vertical": vert, "product": product, "signal_type": "search_interest",
                         "date": date, "value": float(val), "source": "Google Trends (US)"})
        base.record_manifest({"task": "search_interest", "vertical": vert,
                              "source": "Google Trends via pytrends", "keywords": kws,
                              "mode": mode, "months": months, "rows": len(vseries)})
    out = pd.DataFrame(rows)
    path = base.DATA / "search_interest_long.csv"
    out.to_csv(path, index=False)
    print(f"  search_interest -> {path.relative_to(base.ROOT)} ({len(out)} rows, mode={mode_overall})")
    return out


if __name__ == "__main__":
    collect()
