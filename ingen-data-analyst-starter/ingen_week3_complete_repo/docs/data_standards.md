# Data Standards (Week 3)

Conventions applied to **every** dataset loaded into the warehouse. Implemented in
`src/ingest/base.py::standard_clean` and enforced by `src/ingest/tests`.

## Column naming
- `snake_case` only — lowercase, words joined by `_`, no spaces or hyphens.
- Shared dimensions use consistent names: `country`, `iso3`, `fips`, `year`, `vertical`.

## Dates / years
- Year stored as a nullable integer (`Int64`) named `year`.
- Full dates (e.g., SEC filing_date) stored ISO 8601 `YYYY-MM-DD`.

## Missing values
- Real `NULL` in the warehouse — never sentinel strings. `""`, `"N/A"`, `"n/a"`, `"-"`
  are converted to NULL during cleaning.

## Categorical normalization
- Vertical is one of: `eldercare`, `education`, `indoor_security`, `outdoor_patrol`,
  `humanoid`, `shared`.
- Country names kept as published; `iso3` is the join key across country-level sources.

## Versioning & provenance
- Every raw download is hashed (SHA-256) and recorded in `data/week03/ingest_manifest.jsonl`
  with source, URL, license, retrieval date, row/col counts, and run mode.
- `raw/` holds untouched downloads; `clean/` holds standardized CSV (+parquet). Raw is
  never edited in place; re-pulling appends a new manifest row.

## Run modes
- **network** — fetched from the live public API documented in the module.
- **offline-fallback** — a clearly-labelled synthetic sample with the SAME schema, used
  when network is unavailable so the pipeline/tests/warehouse run end-to-end.
  Set `INGEST_ALLOW_NETWORK=1` to populate from live sources.

## Warehouse
- Single DuckDB file: `data/week03/analytics.duckdb`.
- One schema per vertical + a `shared` schema for cross-cutting dimensions
  (population aging, R&D spend, SEC filings).
