"""Task 2 — News cadence & sentiment (GDELT DOC 2.0 API).

Real source: GDELT DOC 2.0 API (no key). For each vertical we query its keywords and
pull two monthly timelines:
  - TimelineVolRaw -> article counts per month (news cadence)
  - TimelineTone   -> average tone per month (news sentiment; negative=bad, positive=good)
Emitted long-format: vertical, signal_type in {news_volume, news_tone}, date, value, source.

Endpoint (real):
  https://api.gdeltproject.org/api/v2/doc/doc?query=<kw>&mode=TimelineVolRaw&format=json&timespan=24m
  https://api.gdeltproject.org/api/v2/doc/doc?query=<kw>&mode=TimelineTone&format=json&timespan=24m

Network: GDELT needs live access to api.gdeltproject.org. When unavailable, a
schema-correct synthetic series is produced (mode='offline-fallback' in the manifest).

Run live:  INGEST_ALLOW_NETWORK=1 python -m src.signals.gdelt_news
"""
from __future__ import annotations
import random, urllib.parse
import pandas as pd
from . import base

API = "https://api.gdeltproject.org/api/v2/doc/doc"


def _gdelt_timeline(keyword, mode, months):
    q = urllib.parse.quote(f'"{keyword}"')
    url = f"{API}?query={q}&mode={mode}&format=json&timespan={months}m"
    payload = base.http_get_json(url)
    # GDELT returns {"timeline":[{"series":..., "data":[{"date":"YYYYMMDDHHMMSS","value":N},...]}]}
    series = payload.get("timeline", [])
    if not series:
        raise RuntimeError("empty GDELT timeline")
    pts = series[0].get("data", [])
    rec = {}
    for p in pts:
        d = str(p.get("date", ""))[:6]  # YYYYMM
        if len(d) == 6:
            ym = f"{d[:4]}-{d[4:6]}"
            rec[ym] = rec.get(ym, 0) + float(p.get("value", 0))
    return rec


def _synth(months, seed, kind):
    rng = random.Random(seed)
    idx = base.month_range(months)
    out = {}
    if kind == "volume":
        base_n = rng.randint(40, 160); trend = rng.uniform(0.0, 0.6)
        for i, ym in enumerate(idx):
            out[ym] = max(0, round(base_n * (1 + trend * i / len(idx)) + rng.uniform(-15, 15)))
    else:  # tone, typically between -5 and +3
        center = rng.uniform(-2.5, 1.0)
        for ym in idx:
            out[ym] = round(center + rng.uniform(-1.2, 1.2), 2)
    return out


def collect(months: int = 24):
    rows = []
    mode_overall = "network"
    for vert, (product, kws) in base.VERTICALS.items():
        kw = kws[0]  # primary keyword for the vertical
        for signal, gmode, kind in (("news_volume", "TimelineVolRaw", "volume"),
                                     ("news_tone", "TimelineTone", "tone")):
            mode = "offline-fallback"; rec = None
            if base.ALLOW_NETWORK:
                try:
                    rec = _gdelt_timeline(kw, gmode, months); mode = "network"
                except Exception as e:  # noqa: BLE001
                    print(f"  [{vert}/{signal}] GDELT failed ({e}); offline fallback")
            if rec is None:
                rec = _synth(months, seed=base.stable_seed(vert + signal), kind=kind)
                mode_overall = "offline-fallback"
            for ym, val in sorted(rec.items()):
                rows.append({"vertical": vert, "product": product, "signal_type": signal,
                             "date": ym, "value": round(float(val), 2),
                             "source": "GDELT DOC 2.0 API"})
            base.record_manifest({"task": signal, "vertical": vert, "keyword": kw,
                                  "source": f"GDELT {gmode}", "mode": mode,
                                  "months": months, "rows": len(rec)})
    out = pd.DataFrame(rows)
    path = base.DATA / "news_signals_long.csv"
    out.to_csv(path, index=False)
    print(f"  news_signals -> {path.relative_to(base.ROOT)} ({len(out)} rows, mode={mode_overall})")
    return out


if __name__ == "__main__":
    collect()
