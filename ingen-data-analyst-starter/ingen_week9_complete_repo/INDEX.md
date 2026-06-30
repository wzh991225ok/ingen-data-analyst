# inGen Data Analyst Internship — Repository Index

Ziheng Wang · inGen Dynamics (Futurenauts) · 13-week analytics plan.
Each week is a self-contained module with a README; deliverables are linked below.

## Phase 1 — Industry & Data Foundation
| Week | Focus | Key deliverables |
|------|-------|------------------|
| **1** | Product & competitor landscape | product profiles, competitor landscape (40+), data dictionary |
| **2** | Competitive intelligence | 15 priority peers, real patents & headcounts, IP-vs-funding analysis |
| **3** | Data pipeline & warehouse | 12-dataset ingestion pipeline, DuckDB warehouse, 15 tests, data-quality report |

## Phase 2 — Market & Competitive Analytics
| Week | Focus | Key deliverables |
|------|-------|------------------|
| **4** | Market sizing | TAM/SAM/SOM (5 verticals), dual-method, tornado sensitivity, market_sizing_workbook.xlsx |
| **5** | Demand signals | search/news/VoC signals, demand-signal index, pain-point taxonomy, methodology PDF |
| **6** | Financial benchmarking | public FY24 financials + private funding (sourced), benchmark one-pager, methodology memo |

## Phase 3 — BI Development & Visualization
| Week | Focus | Key deliverables |
|------|-------|------------------|
| **7** | SQL & warehouse | star-schema DuckDB warehouse, 100k-row synthetic data, ER diagram, 15 queries, SQL self-assessment (12/12) |
| **8** | Tableau + Looker dashboards | 2 dashboard specs, upload-ready extracts, prototypes, design-review log, publish guide |
| **9** | Power BI + review | exec-scorecard spec + prototype, 10 DAX measures (docs/dax_measures.md), this INDEX, mid-internship review |

## Phase 4 — Advanced Analytics (upcoming)
| Week | Focus |
|------|-------|
| **10–13** | Forecasting (adoption & demand), applied modeling on InGen use cases, capstone |

## Cross-cutting
- **Data dictionaries:** per-week `data/data_dictionary_weekNN.md`.
- **DAX measures:** `docs/dax_measures.md` (Week 9).
- **Tests:** pytest suites in Weeks 3, 5, 6, 7.
- **Data integrity:** real sourced data throughout; ranges over false precision; clearly-labelled
  synthetic fallbacks where live sources were unreachable; provenance recorded per source.

## How to read a week
Each `ingen_weekNN_complete_repo` has: `README.md` (overview + quick start), `plan/weekNN.md`
(tasks + success criteria), `reports/weekNN/` (deliverables + status), `src/` (code), and where
relevant `data/` and `notebooks/`.
