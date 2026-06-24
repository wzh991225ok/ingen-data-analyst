# Week 7 — SQL Fluency & Simulated InGen Analytics Warehouse
**Dates:** 05 Jun – 11 Jun 2026 · **Phase 3 — BI Development & Visualization** · 25 hrs

## Tasks
- SQL self-assessment across joins, window functions, CTEs, set ops, aggregations (auto-graded).
- Star-schema design: facts fleet_telemetry / support_tickets / sales_pipeline; dims customers / products / geographies / dates; surrogate keys; ER diagram.
- Synthetic data (Faker + Python, fixed seed): ~100k telemetry, 5k tickets, 1k pipeline rows.
- 15 reference SQL queries answering real product-analytics questions.

## Deliverables
- [x] SQL self-assessment notebook + score sheet -> reports/week07/ (notebook + sql_score_sheet.md/.csv)
- [x] Star-schema ER diagram (PNG) + DDL (SQL) -> reports/week07/er_diagram.png, src/warehouse/schema.sql, er_diagram.dot
- [x] Synthetic dataset + generator -> data/week07/synthetic/*.csv, src/generator/generate_synthetic.py
- [x] Reference query library (15 documented) -> src/queries/reference_queries.sql

## Success criteria
- [x] Star schema has clearly separated facts and dimensions with surrogate keys
- [x] All 15 reference queries run without error against the synthetic warehouse
- [x] ER diagram committed as image AND source (.png + .dot)
- [x] Synthetic data reproducible from a fixed seed (SEED=20260607)

## Note
Synthetic only — no real InGen data. Schema intentionally mirrors the data an InGen analytics team
would hold (fleet telemetry, support tickets, sales pipeline) so the fluency transfers to real data.
