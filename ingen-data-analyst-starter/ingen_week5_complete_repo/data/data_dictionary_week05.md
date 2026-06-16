# Data Dictionary — Week 5

## Outputs (data/week05/)
| File | Schema | Notes |
|------|--------|-------|
| search_interest_long.csv | vertical, product, signal_type, date(YYYY-MM), value(0-100), source | Google Trends interest per vertical |
| news_signals_long.csv | vertical, product, signal_type{news_volume,news_tone}, date, value, source | GDELT volume + tone |
| pain_points_long.csv | vertical, product, theme_id, top_terms, size, example, mode | TF-IDF+KMeans themes per vertical |
| demand_signal_index.csv | vertical, product, *_raw, *_score, demand_index, rank | composite relative index |
| demand_signals_long.csv | vertical, product, signal_type, date, value, source | all raw signals concatenated |
| signal_manifest.jsonl | per source: task, source, mode, … | provenance + run mode |

## Sources (real, public)
| Source | Access | Used for |
|--------|--------|----------|
| Google Trends | pytrends client (trends.google.com) | search interest per vertical (US) |
| GDELT DOC 2.0 API | api.gdeltproject.org/api/v2/doc/doc (no key) | news volume (TimelineVolRaw) + tone (TimelineTone) |
| Review/comment corpora | per-vertical CSV (column: text) | voice-of-customer topic modelling |

## Index weights
search momentum 0.40 · news momentum 0.35 · news sentiment 0.25 (each min-max normalised across verticals to 0-100).

## Run modes (signal_manifest.jsonl `mode`)
- network — fetched live from the real API
- offline-fallback — clearly-labelled schema-correct synthetic sample (deterministic seeds)
- file — real reviews_<vertical>.csv supplied
- derived — computed from other signals (the index)

Notes: synthetic fallbacks are NOT real data and are labelled as such; set INGEST_ALLOW_NETWORK=1 and
supply real review files to populate live. The index is a relative demand read, not a forecast.
