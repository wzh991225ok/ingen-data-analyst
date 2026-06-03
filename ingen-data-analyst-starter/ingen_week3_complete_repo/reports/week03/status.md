# Week 3 — Status

**Phase:** 1 (Foundations) · **Dates:** 08–14 May 2026

## Done
- [x] 12 public-dataset ingestion modules (`src/ingest/datasets.py`) — real APIs documented per source
- [x] Shared utilities: sha256 versioning, manifest, `standard_clean`, offline-fallback resilience
- [x] 15 unit tests passing (`src/ingest/tests`)
- [x] DuckDB warehouse `data/week03/analytics.duckdb` — 6 schemas (per vertical + shared), 12 tables + 1 view
- [x] Cleaning standards `docs/data_standards.md`; schema map `docs/schema_diagram.md`
- [x] Data-quality report `reports/week03/data_quality_report.html`
- [x] Pipeline+QA notebook `notebooks/week03_pipeline_and_quality.ipynb`

## Run mode (transparency)
- Pipeline ran in **offline-fallback** mode (network restricted here). Every fallback row is a
  clearly-labelled synthetic sample with the REAL schema, so the pipeline, warehouse, tests, and
  report all run end-to-end. Manifest records mode per dataset.
- To populate from live public APIs: `INGEST_ALLOW_NETWORK=1 python -m src.ingest.run_all`,
  then `build_warehouse` + `quality_report`.

## Hands-off for the analyst
- Add a Census/FBI/BLS API key where required (Census now mandates a key) via env var, then re-run.
- These cleaned, versioned tables are the inputs for Week 4 (TAM/SAM/SOM).
