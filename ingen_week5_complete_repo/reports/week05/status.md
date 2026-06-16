# Week 5 — Status

**Phase:** 2 (Market & Competitive Analytics) · **Dates:** 22–28 May 2026

## Done
- [x] Search-interest collector (Google Trends/pytrends) — 60-month interest + momentum per vertical
- [x] News collector (GDELT DOC 2.0 API) — monthly volume + tone per vertical
- [x] Voice-of-customer miner (TF-IDF + KMeans) — themes + pain-point examples per vertical
- [x] Demand-signal index (documented weights: search 40 / news 35 / sentiment 25), relative 0-100 ranking
- [x] Long-format dataset, methodology PDF, pain-point taxonomy markdown, 3 charts
- [x] Analysis notebook + 6 passing unit tests; deterministic offline runs

## Run mode (transparency)
- Ran in **offline-fallback** mode (network restricted here). Real APIs wired in each collector;
  fallbacks are clearly-labelled schema-correct samples; manifest records mode per source.
- Live: `pip install pytrends`, `INGEST_ALLOW_NETWORK=1 python -m src.signals.run_all`; drop real
  `data/week05/reviews_<vertical>.csv` for live voice-of-customer.

## Key reading
- The demand-signal index complements Week 4 market sizing: size says how big, this says what is
  heating up now. Read together for prioritisation.
- Pain-point taxonomy gives product/marketing concrete messaging angles per vertical.

## To validate before external use
- Replace synthetic fallbacks with live Google Trends + GDELT pulls and real review exports.
- Validate the relative ranking against internal pipeline/CRM demand data.
