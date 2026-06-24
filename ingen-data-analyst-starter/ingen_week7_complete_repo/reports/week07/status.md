# Week 7 — Status
**Phase 3 · 05–11 Jun 2026**

## Done
- [x] Star schema: 3 facts + 4 dims, surrogate keys, documented grain (schema.sql)
- [x] Synthetic generator (Faker, SEED=20260607): 100k telemetry / 5k tickets / 1k pipeline, reproducible
- [x] DuckDB warehouse built + foreign-key integrity check (0 orphans)
- [x] ER diagram as PNG + .dot source
- [x] SQL self-assessment 12/12 across JOIN/WINDOW/CTE/SETOP/AGGREGATION + score sheet
- [x] 15 reference queries, all run clean
- [x] 6 passing tests (schema, scale, unique keys, all queries, assessment, reproducibility)

## Run
```bash
python -m src.generator.generate_synthetic
python -m src.warehouse.build_warehouse
python -m src.warehouse.er_diagram
python -m src.warehouse.sql_assessment
python -m src.queries.run_queries
python -m pytest src/warehouse/tests -q
```

## Next (Week 8)
- Point Tableau Public + Looker Studio at this warehouse for two interactive dashboards.
