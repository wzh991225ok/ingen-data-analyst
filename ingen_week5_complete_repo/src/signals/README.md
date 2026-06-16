# src/signals — Demand-Signal Pipeline (Week 5)

Reusable, tested modules that collect three public signal families and combine them into one
comparable demand-signal index across the five InGen verticals.

## Run
```bash
python -m src.signals.run_all          # collect (offline fallbacks by default)
python -m src.signals.build_reports    # taxonomy md + charts + methodology PDF
python -m pytest src/signals/tests -q  # 6 tests

# live public sources:
pip install pytrends
INGEST_ALLOW_NETWORK=1 python -m src.signals.run_all
# live voice-of-customer: drop real data/week05/reviews_<vertical>.csv (column: text)
```

## Modules
| File | Task | Real source |
|------|------|-------------|
| `google_trends.py` | search interest + momentum | Google Trends (pytrends) |
| `gdelt_news.py` | news volume + tone | GDELT DOC 2.0 API (no key) |
| `voc_reviews.py` | review topic modelling -> pain points | review CSVs + TF-IDF/KMeans |
| `demand_index.py` | weighted composite index | derived |
| `build_reports.py` | taxonomy md, charts, methodology PDF | — |
| `base.py` | paths, manifest, verticals, helpers | — |
| `sample_reviews.py` | labelled SAMPLE corpus (fallback only) | synthetic |

## Index weights (documented)
search momentum 40% · news momentum 35% · news sentiment 25%. Each component is min-max
normalised across verticals to 0-100, so the index is a **relative** "heating up now" read,
not an absolute forecast.

## Run mode (transparency)
Each source records `mode` (network / offline-fallback / file / derived) in
`data/week05/signal_manifest.jsonl`. Offline fallbacks are clearly-labelled, schema-correct
synthetic samples so the whole pipeline, topic modelling, and index run without network.
Synthetic seeds are deterministic, so offline runs are reproducible.
