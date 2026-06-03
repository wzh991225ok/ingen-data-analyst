# Week 3 — Public-Data Acquisition Pipelines & Cleaning Standards
**Dates:** 08 May – 14 May 2026 · **Phase 1 — Foundations** · 25 hrs

## Daily plan
- Day 1 — Source inventory: 12 public datasets across verticals, logged in the manifest/dictionary.
- Day 2-3 — Ingestion code: reusable `src/ingest/` modules, each hashing raw files; pytest per pipeline.
- Day 4 — Standards + warehouse: finalize `docs/data_standards.md`; load `analytics.duckdb` (schema per vertical).
- Day 5 — Quality report: profiling over the warehouse exported to HTML.

## Deliverables
- [x] Reusable ingestion package `src/ingest/` (12 modules + tests), documented in README
- [x] `data/week03/analytics.duckdb` warehouse + `docs/schema_diagram.md`
- [x] Data standards → `docs/data_standards.md`
- [x] Data-quality report → `reports/week03/data_quality_report.html`

## Success criteria
- [x] 12 datasets ingested via reusable, tested modules (15 tests pass)
- [x] Every dataset hashed (sha256) + dated in `data/week03/ingest_manifest.jsonl`
- [x] Warehouse loads cleanly with per-vertical schemas (6 schemas, 12 tables + view)
- [x] Quality report covers row counts, null rates, dtypes, year coverage for every table

## Note on run mode
Real public APIs are documented and wired in each module. In a network-restricted
environment the pipeline uses schema-correct offline fallbacks (clearly labelled in the
manifest); set INGEST_ALLOW_NETWORK=1 to populate from live sources.
