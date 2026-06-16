"""Task 4 — Demand-signal index synthesis.

Combines the three signal families into one comparable 0-100 index per vertical, with
explicit, documented weights:

  search_momentum  (40%): last-12-mo mean vs prior-12-mo mean of Google-Trends interest
  news_momentum    (35%): last-6-mo mean vs prior-6-mo mean of GDELT article volume
  news_sentiment   (25%): mean GDELT tone over the last 6 months (higher = more positive)

Each component is min-max normalised ACROSS verticals to 0-100 so the index is a relative
ranking of which vertical is heating up now (not an absolute forecast). Output:
  data/week05/demand_signal_index.csv  (vertical, product, component scores, index, rank)
  data/week05/demand_signals_long.csv  (concatenated long-format of all raw signals)

Weights live in WEIGHTS below and are echoed into the methodology PDF.
"""
from __future__ import annotations
import pandas as pd
from . import base

WEIGHTS = {"search_momentum": 0.40, "news_momentum": 0.35, "news_sentiment": 0.25}


def _ratio(series, half):
    """Ratio of mean(last `half`) to mean(prior `half`); 1.0 = flat. NaN-safe."""
    s = list(series)
    if len(s) < 2 * half:
        half = max(1, len(s) // 2)
    recent = s[-half:]; prior = s[-2 * half:-half]
    pm = sum(prior) / len(prior) if prior else 0
    rm = sum(recent) / len(recent) if recent else 0
    if pm == 0:
        return 1.0
    return rm / pm


def _minmax(d):
    vals = list(d.values())
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return {k: 50.0 for k in d}
    return {k: round((v - lo) / (hi - lo) * 100, 1) for k, v in d.items()}


def build():
    si = pd.read_csv(base.DATA / "search_interest_long.csv")
    news = pd.read_csv(base.DATA / "news_signals_long.csv")
    vol = news[news.signal_type == "news_volume"]
    tone = news[news.signal_type == "news_tone"]

    search_mom, news_mom, news_sent = {}, {}, {}
    for vert in base.VERTICALS:
        s = si[si.vertical == vert].sort_values("date")["value"]
        search_mom[vert] = _ratio(s, 12)
        v = vol[vol.vertical == vert].sort_values("date")["value"]
        news_mom[vert] = _ratio(v, 6)
        t = tone[tone.vertical == vert].sort_values("date")["value"].tail(6)
        news_sent[vert] = float(t.mean()) if len(t) else 0.0

    nsm = _minmax(search_mom); nnm = _minmax(news_mom); nns = _minmax(news_sent)
    rows = []
    for vert, (product, _) in base.VERTICALS.items():
        idx = (nsm[vert] * WEIGHTS["search_momentum"]
               + nnm[vert] * WEIGHTS["news_momentum"]
               + nns[vert] * WEIGHTS["news_sentiment"])
        rows.append({"vertical": vert, "product": product,
                     "search_momentum_raw": round(search_mom[vert], 3),
                     "news_momentum_raw": round(news_mom[vert], 3),
                     "news_sentiment_raw": round(news_sent[vert], 3),
                     "search_score": nsm[vert], "news_vol_score": nnm[vert],
                     "news_tone_score": nns[vert], "demand_index": round(idx, 1)})
    out = pd.DataFrame(rows).sort_values("demand_index", ascending=False).reset_index(drop=True)
    out["rank"] = out.index + 1
    out.to_csv(base.DATA / "demand_signal_index.csv", index=False)

    # also write a single concatenated long file of all raw signals
    longall = pd.concat([si, news], ignore_index=True)
    longall.to_csv(base.DATA / "demand_signals_long.csv", index=False)

    base.record_manifest({"task": "demand_index", "weights": WEIGHTS,
                          "source": "derived from search_interest + news_signals",
                          "mode": "derived", "verticals": len(out)})
    print(f"  demand_index -> {(base.DATA/'demand_signal_index.csv').relative_to(base.ROOT)}")
    print(f"  demand_signals_long -> {(base.DATA/'demand_signals_long.csv').relative_to(base.ROOT)} ({len(longall)} rows)")
    print("\n  Ranking (relative 'heating up now'):")
    for _, r in out.iterrows():
        print(f"    {r['rank']}. {r['product']:18s} index={r['demand_index']:5.1f}  "
              f"(search {r['search_score']:.0f} / news-vol {r['news_vol_score']:.0f} / tone {r['news_tone_score']:.0f})")
    return out


if __name__ == "__main__":
    build()
