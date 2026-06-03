# DuckDB Warehouse Schema (Week 3)

File: `data/week03/analytics.duckdb` — built by `src/ingest/build_warehouse.py`.
One schema per InGen vertical + `shared`. 12 base tables + 1 view + a load catalog.

```
analytics.duckdb
├── eldercare/                         (Fari)
│   ├── census_population_by_age       state, fips, total_population, pop_65_plus, year
│   ├── bls_home_health_aides          year, occupation, soc_code, employment, mean_annual_wage_usd
│   └── oecd_longterm_care_spend       country, iso3, year, ltc_spend_pct_gdp
├── education/                         (Senpai)
│   ├── nces_k12_enrollment            year, level, public_enrollment, private_enrollment
│   └── worldbank_education_spend      country, iso3, year, education_spend_pct_gdp
├── indoor_security/                   (Sentinel Prime AI)
│   ├── fbi_property_crime             year, population, property_crime, burglary, larceny_theft, motor_vehicle_theft
│   └── bls_security_guards            year, occupation, soc_code, employment, mean_annual_wage_usd
├── outdoor_patrol/                    (Aido Rover)
│   └── bls_warehousing_employment     year, industry, naics, employment_thousands
├── humanoid/                          (Aido Humanoid)
│   └── openalex_robotics_publications year, concept, works_count
└── shared/                            (cross-cutting)
    ├── worldbank_rnd_spend            country, iso3, year, rnd_spend_pct_gdp
    ├── worldbank_pop_65plus           country, iso3, year, pop_65plus_pct
    ├── sec_edgar_robotics_filings     company, cik, form, filing_date, fiscal_year
    ├── v_country_context  (VIEW)      iso3, country, year, pop_65plus_pct, rnd_spend_pct_gdp
    └── _load_catalog                  schema_name, table_name, rows
```

## Join keys
- Country-level sources join on `iso3` + `year`.
- US time-series (BLS/FBI/NCES/Census) join on `year`.

## Example queries
```sql
-- Eldercare demand context by country
SELECT * FROM shared.v_country_context ORDER BY pop_65plus_pct DESC;

-- US security-guard labor market trend (Sentinel Prime AI baseline)
SELECT year, employment, mean_annual_wage_usd
FROM indoor_security.bls_security_guards ORDER BY year;

-- Robotics research momentum (Aido Humanoid / PIC 2.0)
SELECT year, works_count FROM humanoid.openalex_robotics_publications ORDER BY year;
```
