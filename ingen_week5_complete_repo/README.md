# ingen-data-analyst — Week 5

Data Analyst Internship · Ziheng Wang · inGen Dynamics Inc.
**Week 5 — Demand Signals & Customer-Behavior Analysis** (22–28 May 2026)

Moves from Week 4's *market size* to *current demand momentum + voice-of-customer*: which vertical is
heating up right now, and what customers actually complain about. Builds a comparable demand-signal
index across the five verticals and a pain-point taxonomy.

## Deliverables (this folder)
| Deliverable | File |
|-------------|------|
| Demand-signal dataset (long format) | `data/week05/demand_signals_long.csv` |
| Search interest / news / index tables | `data/week05/{search_interest_long,news_signals_long,demand_signal_index}.csv` |
| Pain-point taxonomy (per vertical) | `reports/week05/pain_point_taxonomy.md` |
| Demand-signal index methodology | `reports/week05/demand_signal_methodology.pdf` |
| Charts | `reports/week05/{demand_index,demand_index_components,search_interest_trends}.png` |
| Reusable pipeline + tests | `src/signals/` (6 tests) |
| Analysis notebook | `notebooks/week05_demand_signals.ipynb` |
| Provenance + run mode | `data/week05/signal_manifest.jsonl` |

## Quick start
```bash
pip install -r requirements.txt
python -m src.signals.run_all          # collect 3 signal families (offline fallbacks by default)
python -m src.signals.build_reports    # taxonomy md + charts + methodology PDF
python -m pytest src/signals/tests -q  # 6 tests

# live public sources:
pip install pytrends
INGEST_ALLOW_NETWORK=1 python -m src.signals.run_all
# live voice-of-customer: drop real data/week05/reviews_<vertical>.csv (column: text)
```

## Method (one paragraph)
Three public signal families per vertical: **search interest** (Google Trends), **news cadence &
sentiment** (GDELT DOC 2.0 API), and **voice-of-customer** (review text -> TF-IDF + KMeans themes ->
most-negative review per theme as the pain point). These combine into a 0-100 **demand-signal index**
with documented weights (search momentum 40% / news momentum 35% / news sentiment 25%), each component
min-max normalised across verticals. The index is a **relative** read of which vertical is heating up
now — it complements, not replaces, Week 4's market sizing, and is not a forecast.

## Data-integrity stance
- Real public APIs are wired in every collector; specific endpoints are documented in `src/signals/`.
- Where network is unavailable, the pipeline uses **clearly-labelled, schema-correct** synthetic
  samples so it runs end-to-end; `signal_manifest.jsonl` records `mode` (network / offline-fallback /
  file / derived) per source. Synthetic seeds are deterministic, so offline runs are reproducible.
- Index weights are explicit and documented; the index is relative, not an absolute forecast.

Sources and schema: `data/data_dictionary_week05.md`.
