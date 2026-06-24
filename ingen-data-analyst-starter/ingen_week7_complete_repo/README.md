# ingen-data-analyst — Week 7

Data Analyst Internship · Ziheng Wang · inGen Dynamics Inc.
**Week 7 — SQL Fluency & Simulated InGen Analytics Warehouse** (05–11 Jun 2026)

A star-schema analytics warehouse in DuckDB, built from reproducible synthetic data, with an
auto-graded SQL self-assessment and a 15-query reference library. The schema mirrors what an InGen
analytics team would actually hold (fleet telemetry, support tickets, sales pipeline), so the SQL
fluency transfers directly if real data access is later granted. **Synthetic only — no real InGen data.**

## Deliverables (this folder)
| Deliverable | File |
|-------------|------|
| SQL self-assessment notebook + score sheet | `notebooks/week07_sql_self_assessment.ipynb`, `reports/week07/sql_score_sheet.md` / `.csv` |
| Star-schema ER diagram (PNG) + DDL | `reports/week07/er_diagram.png`, `src/warehouse/schema.sql`, `src/warehouse/er_diagram.dot` |
| Synthetic dataset + generator | `data/week07/synthetic/*.csv`, `src/generator/generate_synthetic.py` |
| Reference query library (15) | `src/queries/reference_queries.sql` |

## Quick start
```bash
pip install -r requirements.txt           # needs the graphviz 'dot' binary for the ER diagram
python -m src.generator.generate_synthetic
python -m src.warehouse.build_warehouse
python -m src.warehouse.er_diagram
python -m src.warehouse.sql_assessment
python -m src.queries.run_queries
python -m pytest src/warehouse/tests -q
```

## Schema at a glance
- **Facts:** `fact_fleet_telemetry` (~100k, robot×day), `fact_support_tickets` (5k), `fact_sales_pipeline` (1k)
- **Dimensions:** `dim_date`, `dim_product`, `dim_customer`, `dim_geography`
- Surrogate keys on every table; clean fact/dimension separation; foreign-key integrity verified (0 orphans).

## Results
- SQL self-assessment: **12/12** across JOIN / WINDOW / CTE / SETOP / AGGREGATION.
- Reference library: **15/15** queries run clean.
- Synthetic data reproducible from `SEED=20260607`.

Schema details & conventions: `data/data_dictionary_week07.md`.
