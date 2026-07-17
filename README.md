# inGen Data Analyst Internship Repository
**Author:** Ziheng Wang  
**Program:** Futurenauts Internship Program — inGen Dynamics  
**Role:** Data Analyst Intern  
**Focus Areas:** Market Intelligence · Competitive Analysis · Business Intelligence · Robotics Industry Research · Data Engineering · Predictive Analytics · Anomaly Detection · Process Optimization

**Status: all 13 weeks complete.** ✅

---

## Start Here

| If you want... | Read |
|---|---|
| Everything in one place | `reports/week13/capstone_report.pdf` (23 pages) |
| The three-minute version | Page 2 of the capstone — the executive summary stands alone |
| The presentation | `reports/week13/Capstone_Executive_Deck.pdf` (15 slides) |
| To pick up the work | `HANDOFF.md` |
| The full file map | `INDEX.md` |
| The dashboards | `reports/week13/dashboard_pack.pdf` |

---

## Overview
This repository documents my internship work as a Data Analyst Intern at inGen Dynamics. The work analyzes AI, robotics, automation, education, security, and eldercare markets using publicly available datasets, industry reports, patents, employee data, and competitive intelligence — then turns that into a queryable analytics warehouse, dashboards, demand forecasts, an anomaly-detection prototype, and a process-optimization study, all synthesized in a final capstone report.

The objective is to translate open-source data into structured insights that support:
- Market understanding
- Competitive benchmarking
- Product ecosystem analysis
- Strategic research
- Business intelligence workflows
- Forecasting and predictive analytics
- Operational analytics (anomaly detection, process simulation)

All work emphasizes **reproducibility**, **clear documentation**, **verifiable provenance**, and **evidence-based analysis** — quantitative claims are sourced and dated, and where public estimates disagree, results are presented as ranges rather than single figures.

### The six findings (from the capstone)
1. **Funding is not a moat.** Capital raised and defensible IP diverge sharply; margin structure predicts durability (Teradyne 58.5% / Cognex 68% gross margins vs iRobot 20.9% and −15.1% operating in FY2024).
2. **The biggest near-term market is not the loudest one.** Indoor security (Sentinel Prime AI) has the clearest economics; humanoid attracts the capital and headlines while published estimates span an order of magnitude.
3. **Attention ≠ opportunity.** The demand-signal ranking is the near-inverse of market attractiveness — Sentinel is a strong asset with weak share of voice.
4. **Momentum is up in all five verticals**, and models beat seasonal-naive in four of five (MASE < 1.0). No single model wins everywhere.
5. **Sentinel's alert problem is solved by persistence, not by a better threshold.** A 120-minute persistence filter cuts false-alert load 33× (16.35 → 0.50/day) while recall *rises* to 88%, catching 4/4 real failures on real public benchmarks.
6. **Support cycle time is a parts problem, not a people problem.** Parts & dispatch is 53% of process time and 100% unstaffed waiting; a regional parts buffer buys −23% vs −8% for added headcount.

---

## Repository Structure
```txt
ingen-data-analyst/
├── data/
│   ├── week01/          # product profiles, competitor landscape, data dictionary
│   ├── week02/          # peer positioning, patents, R&D-scale datasets
│   ├── week03/          # raw/ + clean/ + analytics.duckdb + ingest_manifest.jsonl
│   ├── week04/          # market-sizing assumptions register
│   ├── week05/          # demand signals (search/news/VoC) + demand-signal index
│   ├── week06/          # peer financials (public FY24) + private funding
│   ├── week07/          # synthetic star-schema warehouse (DuckDB) + generator
│   ├── week08/          # dashboard-ready extracts (from Weeks 4–7)
│   ├── week10/          # forecast results, feature importances, Bass diffusion
│   ├── week11/          # anomaly results, PR curves, operational frontier, licences
│   └── week12/          # stage events, cycle-time decomposition, capacity-sim results
├── reports/
│   ├── week01/ … week04/  # profiles, dossier, DQ report, sizing workbook + tornados
│   ├── week05/          # demand-signal methodology, pain-point taxonomy
│   ├── week06/          # peer benchmark one-pager, methodology memo
│   ├── week07/          # ER diagram, SQL self-assessment score sheet
│   ├── week08/          # dashboard specs, prototypes, design-review log, publish guide
│   ├── week09/          # Power BI scorecard spec + prototype, mid-internship review
│   ├── week10/          # 5-page demand forecast report + charts
│   ├── week11/          # 2-page Sentinel operational framing + charts
│   ├── week12/          # 3-page process-optimization memo + charts
│   └── week13/          # capstone report (23pp), exec deck (.pptx + PDF), dashboard pack
├── notebooks/           # one analysis notebook per week
├── src/
│   ├── ingest/          # 12 public-dataset ingestion modules + tests (Week 3)
│   ├── signals/         # demand-signal pipeline (Week 5)
│   ├── financials/      # peer-benchmark model (Week 6)
│   ├── warehouse/       # star schema, synthetic generator, SQL assessment (Week 7)
│   ├── dashboards/      # dashboard prototype + spec builders (Week 8)
│   ├── powerbi/         # scorecard prototype + review builder (Week 9)
│   ├── forecast/        # baselines, Prophet, XGBoost, Bass diffusion (Week 10)
│   ├── anomaly/         # 5 detectors on NAB + SKAB benchmarks + tests (Week 11)
│   ├── process/         # DES process model, drivers, capacity sim + tests (Week 12)
│   └── capstone/        # capstone report, dashboard pack & exec-deck builders (Week 13)
├── docs/                # data_standards.md, dax_measures.md, data dictionaries
├── HANDOFF.md           # how the next analyst picks up each workstream
├── INDEX.md             # master index linking every week's deliverables
├── requirements.txt
└── README.md
```

---

## Completed Deliverables

### Phase 1 — Industry & Data Foundation

#### Week 1 — Foundations & Robotics Industry Landscape
inGen product ecosystem profiling (Fari, Senpai, Sentinel Prime AI, Aido Rover, Aido Humanoid, Origami / PIC 2.0); robotics market landscape across five verticals; competitor identification; product positioning; data-source inventory and data dictionary.
✓ Product Profiles ✓ Competitor Landscape Dataset ✓ Data Dictionary ✓ Market Mapping Notebook ✓ Summary Reports

#### Week 2 — Competitive Intelligence Deep Dive
Priority peer selection (15 competitors, 3 per vertical) with justification; positioning & benchmarking; patent landscape (real patent numbers); R&D-scale analysis (real headcount + IP); strategic positioning vs each inGen product.
✓ Peer Positioning Dataset ✓ Competitor Profiles ✓ Patent Activity Tracking ✓ R&D-Scale Dataset ✓ Competitive Intelligence Dossier ✓ Executive Summary

> Data-integrity note: patent numbers and employee counts are sourced from Justia / Google Patents, SEC filings, Wikipedia, Revelio Labs, and CB Insights. Where real-time hiring counts could not be verified to a single dated snapshot, R&D scale is shown via real headcount + patents rather than fabricated figures. Key finding: heavy funding ≠ defensible IP.

#### Week 3 — Public-Data Pipelines, Cleaning Standards & Warehouse
Public-dataset inventory (12 datasets); reusable, tested ingestion pipeline with SHA-256 raw-file hashing; cleaning standards (snake_case, ISO dates, NULL handling); DuckDB warehouse (one schema per vertical); data-quality profiling.
✓ Ingestion Pipeline (12 modules: Census, BLS, OECD, NCES, World Bank, FBI, OpenAlex, SEC EDGAR) ✓ Unit Test Suite (15 tests) ✓ DuckDB Warehouse (6 schemas, 12 tables) ✓ Data Standards & Schema Docs ✓ Ingest Manifest ✓ Data Quality Report ✓ Pipeline & QA Notebook

### Phase 2 — Market & Competitive Analytics

#### Week 4 — Market Sizing (TAM / SAM / SOM)
TAM/SAM/SOM per vertical; top-down (published anchors) + bottom-up (units × serviceable % × penetration % × ASP); reconciliation of both methods; one-at-a-time sensitivity (tornado) analysis.
✓ Methodology Memo ✓ Market-Sizing Workbook (tab per vertical) ✓ Tornado Charts (5) ✓ Assumptions Register ✓ Market-Sizing Notebook

> Honesty note: published estimates disagree widely (e.g., humanoid robots ~$290M–$4.89B; security robots ~$4.7B–$19B depending on scope), so every figure is a sourced range. Humanoid and outdoor-patrol sizes are scenario ranges, not forecasts. Sensitivity is consistent across verticals: penetration rate dominates, ASP second.

#### Week 5 — Demand Signals & Customer-Behavior Analysis
Three public signal families per vertical — Google Trends search interest, GDELT news volume/tone, and voice-of-customer review mining (TF-IDF + KMeans) — combined into a weighted demand-signal index; pain-point taxonomy per vertical.
✓ Demand-Signal Dataset (long format) ✓ Demand-Signal Index (documented weights) ✓ Pain-Point Taxonomy (5 themes/vertical, ≥3 examples each) ✓ Methodology PDF ✓ Tests ✓ Notebook

> Key finding: the demand ranking (Aido Rover 64.0 first, Sentinel Prime AI 40.7 last) is the near-inverse of the market-attractiveness ranking — attention and opportunity are not aligned.

#### Week 6 — Financial Peer Benchmarking & Comparable Modeling
Public FY2024 financials (iRobot, Teradyne, Cognex, Symbotic) from SEC filings/earnings; private funding rounds (Figure AI, Apptronik, Agility, 1X, Neura, Gecko) with a press source per row; valuation comparables + capital-efficiency proxies.
✓ Peer Financial Workbook (public / private / comps / summary) ✓ Benchmark One-Pager (5 panels) ✓ Methodology & Caveats Memo ✓ Live SEC EDGAR Fetcher ✓ Tests

> Data-integrity note: every public figure and every private round carries its source; estimated cells are flagged; EV/Revenue is left to compute from a live quote (not hard-coded). Private valuations are negotiated post-money figures, not market prices.

### Phase 3 — BI Development & Visualization

#### Week 7 — SQL Fluency & Simulated Analytics Warehouse
Star-schema warehouse in DuckDB (3 facts + 4 dimensions, surrogate keys) built from reproducible synthetic data (100k telemetry / 5k tickets / 1k pipeline rows, fixed seed); ER diagram; 15-query reference library; auto-graded SQL self-assessment.
✓ Star-Schema DDL + ER Diagram (PNG + source) ✓ Synthetic Data Generator ✓ 15 Reference Queries (all run clean) ✓ SQL Self-Assessment (12/12 across joins, windows, CTEs, set ops, aggregations) ✓ 6 Tests

> Synthetic data only — no real inGen data. Schema intentionally mirrors the data an inGen analytics team would hold, so the fluency transfers to real data.

#### Week 8 — Interactive Dashboards (Tableau + Looker Studio)
Two dashboards — a public Market & Competitive view (Weeks 4–6) and a Product Analytics view on the Week 7 warehouse — delivered as specs, upload-ready data extracts, high-fidelity prototypes (color-blind-safe Okabe-Ito palette), and a design-review log.
✓ Two Dashboard Specs (PDF) ✓ Upload-Ready Extracts (from real Week 4–7 outputs) ✓ High-Fidelity Prototypes ✓ Design-Review Log ✓ Publish Guide  
→ *Publishing to Tableau Public / Looker Studio (live URLs + screenshots) is the remaining manual step, done in my own accounts.*

#### Week 9 — Power BI, DAX & Mid-Internship Review
Executive-scorecard spec + prototype (traffic-light KPIs from the Week 7 warehouse); 10 documented, reusable DAX measures; repository housekeeping (master INDEX.md); 5-page mid-internship review.
✓ Power BI Scorecard Spec + Prototype ✓ 10 DAX Measures (`docs/dax_measures.md`) ✓ Master INDEX.md ✓ Mid-Internship Review (Weeks 1–9)  
→ *The .pbix is assembled in Power BI Desktop from the spec + DAX (Windows step). KPI targets are documented assumptions, not inGen's actual targets.*

### Phase 4 — Advanced Analytics

#### Week 10 — Predictive Modeling: Adoption & Demand Forecasting
24-month demand-momentum forecasts per vertical using baselines (seasonal-naive, ETS, ARIMA) and stronger models (Prophet, XGBoost with engineered features), backtested on a 12-month holdout (MAPE + MASE); Bass diffusion model for humanoid adoption anchored to cited analyst shipment guidance.
✓ Forecasting Notebook ✓ Forecast Results Table (vertical / model / MAPE / MASE / 12m / 24m) ✓ 5-Page Forecast Report ✓ XGBoost Feature Importances ✓ Bass Diffusion (humanoid)

> Best model by MASE: eldercare → ETS · education → Prophet · indoor_security → XGBoost · outdoor_patrol → Prophet · humanoid → ETS (MASE < 1 beats the naive benchmark; 4 of 5 clear it). Humanoid Bass fit hits Goldman Sachs anchors (~20k/2025 → 250k/2030 → 1.4M/2035); cross-checked vs Morgan Stanley (13M in service by 2035 — a ~3× spread that is itself the finding). Forecasts are a relative demand-momentum read from public signals, not absolute unit/market forecasts.

#### Week 11 — Anomaly Detection Prototype (Sentinel Prime AI)
Five detectors — Isolation Forest, One-Class SVM, LOF, AutoEncoder (PyOD), and an EWMA control-chart baseline — evaluated on **two real, licensed public sensor benchmarks** (NAB machine-temperature, MIT license; SKAB valve1, GPL-3.0), fitted unsupervised on a clean warm-up window with labels used only for evaluation; adaptive-threshold study; operational alert-load analysis.
✓ Anomaly Notebook ✓ Results Table (precision / recall / F1 / average precision per detector × dataset) ✓ PR Curves + Confusion Matrices + Score Timelines ✓ Adaptive-Threshold Study ✓ Operational Frontier (persistence × threshold) ✓ Dataset Licence Table ✓ 2-Page Sentinel Operational Framing ✓ 12 Tests (incl. causality / no-leakage checks)

> Key results: AutoEncoder best on NAB (F1 0.555), LOF best on SKAB (F1 0.545); both beat the control-chart baseline. The 5% false-alarm budget is **unreachable** at the 80% recall floor (point-level FAR bottoms out ~13% — a model-quality ceiling, not a tuning problem). The win: a 120-minute persistence filter cuts alert load **33×** (16.35 → 0.50 false alerts/day) while recall *rises* to 88% and all 4/4 labelled failures are still caught. Adaptive thresholds failed for a diagnosable reason (multi-day anomalies contaminate a rolling baseline). Recommendation: two-tier alerting. **This week runs on real public data** — thresholds transfer to Sentinel as a method, not as constants.

#### Week 12 — Business-Process Optimization & Workflow Analytics
Discrete-event model (simpy) of the fleet-support ticket lifecycle — Intake → Triage → Remote diagnosis → [Parts & dispatch → On-site repair] → Verification — **replaying Week 7's real ticket stream** with enforced, tested reconciliation (1:1 ticket join; stage durations sum exactly to cycle time); cycle-time decomposition + Pareto + control chart; driver regression with 95% CIs; capacity simulation (5 scenarios × 8 replications, paired deltas).
✓ Process-Analytics Notebook ✓ Stage-Event Dataset (23.8k rows, reconciled to Week 7) ✓ Pareto / Wait-vs-Service / Control Charts ✓ Driver Regression + Ground-Truth Recovery Validation (7/9 effect directions) ✓ Capacity-Simulation Model + Results ✓ 3-Page Recommendation Memo (explicit cost / cycle-time / service-level trade-offs) ✓ 12 Tests

> Key results: Parts & dispatch = 53% of all process time and 100% unstaffed waiting — headcount cannot touch it. The brief's drivers (product, severity, geography, weekday, workload) explain R² = 0.04; adding one structural fact — did the ticket need a part? — takes R² to 0.72 (dispatched +578%). Regional parts buffer −23% (P90 64h → 47h) vs +1 Field FTE −8%; both −29%; rerouting Tier-1 triage has **no measurable effect**. All numbers are properties of the documented model, not measurements of inGen's support org; what transfers is the validated method + pipeline.

### Phase 5 — Capstone & Handoff

#### Week 13 — Capstone Synthesis, Final Presentation & Handoff
All twelve weeks synthesized into one integrated artifact set. Every number in the capstone is **loaded at build time from the committed outputs of Weeks 4–12** — nothing retyped, so the report cannot drift from the data; every section cites its source notebook/workbook, with a full repo map and reproduction commands in the appendices.
✓ Capstone Report — *Public-Data Analytics on the InGen Robotics Portfolio: Market, Competition, BI, Forecasting & Operations* (23 pages, standalone one-page executive summary) ✓ Executive Deck (15 slides, .pptx + PDF, readable without the report) ✓ Dashboard Pack + one-page "how to read each one" ✓ HANDOFF.md (day-one quickstart, ranked known issues, per-workstream pickup notes) ✓ Final INDEX.md ✓ Final-Review Feedback Log

> The capstone report doubles as the consolidated internship report. Its §11 is an eight-item honest inventory of what public data could not answer — and the one ask that dissolves most of it: read access to a small anonymized slice of real inGen data.

---

## Tools & Technologies
Languages: Python · SQL · R · JavaScript (pptxgenjs)

Libraries: pandas · numpy · matplotlib · openpyxl · reportlab · pyarrow · pytest · scikit-learn · statsmodels · prophet · xgboost · scipy · faker · duckdb · pyod · torch · simpy

Data & Analytics: DuckDB · Tableau · Power BI · Looker Studio

Research Sources: U.S. Census Bureau · BLS · NCES · OECD · World Bank · FBI Crime Data Explorer · SEC EDGAR · USPTO / Justia / Google Patents · OpenAlex · GDELT · Google Trends · Crunchbase / CB Insights · Goldman Sachs & Morgan Stanley research (humanoid shipment guidance) · Numenta Anomaly Benchmark (MIT) · SKAB — Skoltech Anomaly Benchmark (GPL-3.0) · public company websites & filings · industry market-research summaries

---

## Current Progress
**All 13 weeks complete:**
✓ Week 1 — Foundations & Robotics Industry Landscape  
✓ Week 2 — Competitive Intelligence Deep Dive  
✓ Week 3 — Public-Data Pipelines & Warehouse  
✓ Week 4 — Market Sizing (TAM / SAM / SOM)  
✓ Week 5 — Demand Signals & Customer-Behavior Analysis  
✓ Week 6 — Financial Peer Benchmarking  
✓ Week 7 — SQL Fluency & Simulated Analytics Warehouse  
✓ Week 8 — Interactive Dashboards (specs, extracts, prototypes)  
✓ Week 9 — Power BI, DAX & Mid-Internship Review  
✓ Week 10 — Predictive Modeling: Adoption & Demand Forecasting  
✓ Week 11 — Anomaly Detection Prototype (Sentinel Prime AI)  
✓ Week 12 — Business-Process Optimization & Workflow Analytics  
✓ Week 13 — Capstone Synthesis, Final Presentation & Handoff

Remaining manual steps (documented in `HANDOFF.md` §3): publishing the three dashboards from personal Tableau / Google / Power BI accounts; running the Week 3/5/6 collectors against live APIs in a networked environment; confirming real KPI targets for the executive scorecard.

---

## How to Run

**Week 3 — data pipeline & warehouse**
```bash
pip install -r requirements.txt
python -m src.ingest.run_all            # ingest 12 datasets (offline fallbacks by default)
python -m src.ingest.build_warehouse    # build DuckDB warehouse (per-vertical schemas)
python -m src.ingest.quality_report     # generate the HTML data-quality report
python -m pytest src/ingest/tests -q    # run the 15-test suite
# live public APIs (Census/FBI require a key via env var):
INGEST_ALLOW_NETWORK=1 python -m src.ingest.run_all
```

**Week 7 — synthetic analytics warehouse**
```bash
python -m src.generator.generate_synthetic   # reproducible synthetic data (fixed seed)
python -m src.warehouse.build_warehouse       # load DuckDB + foreign-key integrity check
python -m src.warehouse.sql_assessment        # auto-graded SQL self-assessment
python -m src.queries.run_queries             # run all 15 reference queries
```

**Week 10 — demand & adoption forecasting**
```bash
python -m src.forecast.run_forecasts    # results CSV + forecasts + importances + Bass
python -m src.forecast.build_report     # 5-page forecast report + charts
```

**Week 11 — anomaly detection (downloads NAB + SKAB on first run, then caches)**
```bash
python -m src.anomaly.run_all           # 5 detectors × 2 benchmarks + adaptive + frontier
python -m src.anomaly.build_report      # 2-page Sentinel operational framing + charts
python -m pytest src/anomaly/tests -q   # 12 tests (incl. causality / no-leakage)
```

**Week 12 — process optimization (needs the Week 7 warehouse)**
```bash
export WEEK7_DB=$(pwd)/data/week07/ingen_warehouse.duckdb
python -m src.process.stage_generator   # replay Week 7 tickets → stage events (+ reconciliation)
python -m src.process.cycle_time        # decomposition, Pareto, control chart
python -m src.process.drivers           # regression + CIs + recovery validation
python -m src.process.capacity_sim      # 5 scenarios × 8 replications
python -m src.process.build_report      # scenario chart + 3-page memo
python -m pytest src/process/tests -q   # 12 tests
```

**Week 13 — capstone**
```bash
python -m src.capstone.build_capstone         # 23-page capstone report
python -m src.capstone.build_dashboard_pack   # dashboard pack + reading guide
node src/capstone/make_capstone_deck.js       # 15-slide exec deck (needs: npm install pptxgenjs)
```

---

## Guiding Principles
- Reproducible workflows (fixed seeds, committed manifests, pytest suites)
- Source attribution and dated provenance
- Clear documentation
- Analytical rigor
- Ranges over false precision where evidence is uncertain
- Cautious interpretation of company-reported claims
- Synthetic and fallback data always clearly labelled — never presented as real
- Methods validated against ground truth where it exists (naive baselines, control charts, known generating parameters)

---

## Disclaimer
This repository is intended for internship learning, public-data analytics practice, and structured market research. Analyses are based on publicly available information unless otherwise stated. Market-size figures and forecasts are planning estimates (not investment advice); vendor market totals should be verified against the original reports before external use. Weeks 7–9 and 12 use clearly-labelled synthetic data; Week 11 uses real licensed public benchmarks (NAB — MIT; SKAB — GPL-3.0); forecasts are relative demand reads, not absolute market predictions. Week 12's process findings are properties of a documented simulation, not measurements of inGen's operations.

---
**Last Updated:** July 2026 · **Weeks 1–13 complete**
