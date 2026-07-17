# INDEX — inGen Data Analyst Internship (Weeks 1–13)

Ziheng Wang · Futurenauts Program · inGen Dynamics Inc.
**Status: all 13 weeks complete.**

**New here?** Read `reports/week13/capstone_report.pdf` (23pp — everything in one place), or its
one-page executive summary, or `reports/week13/Capstone_Executive_Deck.pdf` (15 slides).
**Picking up the work?** Read `HANDOFF.md`.

---

## Phase 5 — Capstone & Handoff

| Artifact | Path |
|---|---|
| **Capstone report** (23pp) — the consolidated internship report | `reports/week13/capstone_report.pdf` |
| **Executive deck** (15 slides) | `reports/week13/Capstone_Executive_Deck.pptx` · `.pdf` |
| **Dashboard pack + reading guide** | `reports/week13/dashboard_pack.pdf` |
| **Handoff** | `HANDOFF.md` |
| **Final review feedback log** | `reports/week13/feedback_log.md` |
| Builders | `src/capstone/build_capstone.py` · `build_dashboard_pack.py` · `make_capstone_deck.js` (all in `src/capstone/`) |

## Phase 1 — Foundation (Weeks 1–3)

| Week | Deliverables |
|---|---|
| **1** Product & competitor landscape | `notebooks/week01_market_mapping.ipynb` · `reports/week01/product_profiles.pdf` · `data/week01/competitor_landscape.csv` (40+) · `data/data_dictionary.md` |
| **2** Competitive intelligence | `notebooks/week02_competitive_intel.ipynb` · `data/week02/peers_positioning.csv` (15 peers) · `patent_activity.csv` · `reports/week02/competitive_intelligence_dossier.pdf` |
| **3** Public-data pipeline & warehouse | `src/ingest/` (12 collectors + manifests) · `data/week03/clean/` · `reports/week03/data_quality_report.pdf` · 15 tests |

## Phase 2 — Market Analytics (Weeks 4–6)

| Week | Deliverables |
|---|---|
| **4** Market sizing | `notebooks/week04_market_sizing.ipynb` · `reports/week04/market_sizing_workbook.xlsx` · `assumptions_register.csv` · `tornado_*.png` |
| **5** Demand signals | `notebooks/week05_demand_signals.ipynb` · `data/week05/demand_signal_index.csv` · `pain_points_long.csv` · `reports/week05/demand_signal_methodology.pdf` |
| **6** Financial benchmarking | `notebooks/week06_financial_benchmark.ipynb` · `src/financials/peer_data.py` (source per row) · `reports/week06/peer_financial_workbook.xlsx` · `benchmark_one_pager.pdf` |

## Phase 3 — BI Platform (Weeks 7–9)

| Week | Deliverables |
|---|---|
| **7** SQL & analytics warehouse | `src/warehouse/schema.sql` · `src/generator/generate_synthetic.py` · `src/queries/reference_queries.sql` (15) · `reports/week07/er_diagram.png` · `sql_score_sheet.md` (12/12) |
| **8** Tableau & Looker | `reports/week08/spec_market_competitive.pdf` · `spec_product_analytics.pdf` · `design_review_log.md` · `data/week08/extracts/` · `prototype_*.png` |
| **9** Power BI & mid-internship review | `reports/week09/spec_powerbi.pdf` · `docs/dax_measures.md` (10) · `prototype_powerbi_scorecard.png` · `Midterm_Review.pptx` |

## Phase 4 — Advanced Analytics (Weeks 10–12)

| Week | Deliverables |
|---|---|
| **10** Demand & adoption forecasting | `notebooks/week10_forecasting.ipynb` · `src/forecast/` · `data/week10/forecast_results.csv` · `bass_humanoid.csv` · `reports/week10/forecast_report.pdf` |
| **11** Anomaly detection (Sentinel) | `notebooks/week11/week11_anomaly_detection.ipynb` · `src/anomaly/` · `data/week11/results.csv` · `operational_frontier.csv` · `dataset_licenses.csv` · `reports/week11/sentinel_operational_framing.pdf` · 12 tests |
| **12** Process optimisation | `notebooks/week12/week12_process_optimization.ipynb` · `src/process/` · `data/week12/stage_decomposition.csv` · `capacity_sim_paired_deltas.csv` · `reports/week12/process_optimization_memo.pdf` · 12 tests |

---

## Data dictionaries
`data/data_dictionary.md` (Weeks 1–2) · `data/data_dictionary_week03.md` · `_week04.md` · `_week05.md` ·
`_week06.md` · `_week07.md` · `_week08.md` · `_week09.md` · `_week10.md` · `_week11.md` · `_week12.md`

## Tests
`src/ingest/tests` (15) · `src/financials/tests` · `src/warehouse/tests` · `src/forecast/tests` ·
`src/anomaly/tests` (12) · `src/process/tests` (12)

## Plans & status
`plan/week01.md` … `plan/week13.md` · `reports/weekNN/status.md` per week

---

## Data integrity — the one-line version
**Everything rests on public data or clearly-labelled synthetic data. No InGen internal data was
used anywhere.** Weeks 7–9 and 12 are synthetic (schema realistic, numbers generated). Week 11 uses
real licensed public benchmarks (NAB — MIT; SKAB — GPL-3.0). See `HANDOFF.md` §3 for the ranked list
of what that costs.
