# src/ingest — Public-Data Ingestion Pipeline (Week 3)

Reusable, tested modules that pull 12 public datasets, hash + version them, clean to
shared standards, and load a DuckDB warehouse.

## Run
```bash
python -m src.ingest.run_all            # ingest (offline fallbacks by default)
python -m src.ingest.build_warehouse    # load DuckDB (per-vertical schemas)
python -m src.ingest.quality_report     # write reports/week03/data_quality_report.html
python -m pytest src/ingest/tests -q    # 15 tests

# live data:
INGEST_ALLOW_NETWORK=1 python -m src.ingest.run_all
```

## Module contract
Each `load_*` in `datasets.py`: fetch (or offline-fallback) → `standard_clean` →
`finalize` (save clean CSV/parquet + append a manifest row). Returns the clean CSV path.

## The 12 datasets (real sources)
| Module | Source (real API) | Vertical |
|--------|-------------------|----------|
| census_population_by_age | US Census ACS5 B01001 (api.census.gov) | eldercare |
| bls_home_health_aides | BLS OEWS SOC 31-1120 (api.bls.gov) | eldercare |
| oecd_longterm_care_spend | OECD SHA (sdmx.oecd.org) | eldercare |
| nces_k12_enrollment | NCES Digest | education |
| worldbank_education_spend | World Bank SE.XPD.TOTL.GD.ZS | education |
| fbi_property_crime | FBI Crime Data Explorer | indoor_security |
| bls_security_guards | BLS OEWS SOC 33-9032 | indoor_security |
| bls_warehousing_employment | BLS CES NAICS 493 | outdoor_patrol |
| worldbank_rnd_spend | World Bank GB.XPD.RSDV.GD.ZS | shared |
| worldbank_pop_65plus | World Bank SP.POP.65UP.TO.ZS | shared |
| openalex_robotics_publications | OpenAlex (concept: Robotics) | humanoid |
| sec_edgar_robotics_filings | SEC EDGAR submissions API | shared |

## Files
- `base.py` — paths, sha256, fetch/fallback, `standard_clean`, `finalize`, manifest
- `datasets.py` — the 12 loaders + `ALL_LOADERS`
- `run_all.py` / `build_warehouse.py` / `quality_report.py` — entry points
- `tests/test_ingest.py` — schema, null, year-range, manifest, sentinel-string checks

## Notes on run mode
Network is restricted in some environments; modules fall back to clearly-labelled
synthetic samples with the **real schema**, so everything runs end-to-end. The
manifest records `mode` (network vs offline-fallback) per dataset for transparency.
