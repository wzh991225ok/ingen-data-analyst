# Week 5 — Demand Signals & Customer-Behavior Analysis
**Dates:** 22 May – 28 May 2026 · **Phase 2 — Market & Competitive Analytics** · 25 hrs

## Daily plan
- Day 1 — Keyword design per vertical; wire Google Trends (pytrends) interest-over-time.
- Day 2 — GDELT DOC 2.0: monthly article volume + tone per vertical.
- Day 3 — Voice-of-customer: review ingestion + TF-IDF/KMeans topic modelling; pain-point taxonomy.
- Day 4 — Demand-signal index: normalise + weight components; rank verticals.
- Day 5 — Reports: taxonomy markdown, charts, methodology PDF; notebook + tests.

## Deliverables
- [x] Demand-signal dataset (long format) → data/week05/demand_signals_long.csv (vertical, signal_type, date, value, source)
- [x] Per-component tables → search_interest_long.csv, news_signals_long.csv, demand_signal_index.csv
- [x] Pain-point taxonomy per vertical (top themes + examples) → reports/week05/pain_point_taxonomy.md
- [x] Demand-signal index methodology → reports/week05/demand_signal_methodology.pdf
- [x] Reusable, tested pipeline (src/signals/, 6 tests) + analysis notebook

## Success criteria
- [x] >=60 months of search data per vertical where available
- [x] Reproducible, justified sentiment + index method (documented weights; deterministic offline runs)
- [x] >=3 example reviews/themes per vertical in the taxonomy
- [x] Defensible relative ranking of the five verticals from the index

## Honesty note
Google Trends and GDELT require live network; in a restricted environment the pipeline uses
clearly-labelled schema-correct samples and records mode per source in the manifest. Set
INGEST_ALLOW_NETWORK=1 (and supply real reviews_<vertical>.csv) to populate from live sources.
The index is a relative demand read, not a forecast.
