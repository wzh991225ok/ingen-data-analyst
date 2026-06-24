# src/warehouse — Simulated InGen Analytics Warehouse (Week 7)

Star-schema warehouse in DuckDB, built from reproducible synthetic data. Synthetic only — no real InGen data.

## Run
```bash
python -m src.generator.generate_synthetic   # synthetic CSVs (fixed seed)
python -m src.warehouse.build_warehouse       # load DuckDB + FK integrity check
python -m src.warehouse.er_diagram            # ER diagram PNG + .dot
python -m src.warehouse.sql_assessment        # auto-graded SQL self-assessment
python -m src.queries.run_queries             # run all 15 reference queries
python -m pytest src/warehouse/tests -q       # 6 tests
```

## Schema
- **Facts:** fact_fleet_telemetry (robot×day), fact_support_tickets (ticket), fact_sales_pipeline (opportunity)
- **Dims:** dim_date, dim_product, dim_customer, dim_geography
- Surrogate keys (*_key) on every table; natural keys kept separately; degenerate dims (robot_id, ticket_id, opportunity_id) on facts.

## Files
| File | Role |
|------|------|
| `schema.sql` | star-schema DDL |
| `er_diagram.py` / `er_diagram.dot` | ER diagram generator + committed source |
| `build_warehouse.py` | load DuckDB + foreign-key integrity check |
| `sql_assessment.py` | auto-graded SQL self-assessment + score sheet |
| `../generator/generate_synthetic.py` | Faker synthetic data (SEED=20260607) |
| `../queries/reference_queries.sql` | 15 documented reference queries |
| `../queries/run_queries.py` | runs & verifies all 15 |
