# inGen Data Analyst Internship Repository
**Author:** Ziheng Wang  
**Program:** Futurenauts Internship Program — inGen Dynamics  
**Role:** Data Analyst Intern  
**Focus Areas:** Market Intelligence · Competitive Analysis · Business Intelligence · Robotics Industry Research · Data Engineering · Predictive Analytics

---

## Overview
This repository documents my internship work as a Data Analyst Intern at inGen Dynamics. The work focuses on analyzing AI, robotics, automation, education, security, and eldercare markets using publicly available datasets, industry reports, patents, employee data, and competitive intelligence — then turning that into a queryable analytics warehouse, dashboards, and demand forecasts.

The objective is to translate open-source data into structured insights that support:
- Market understanding
- Competitive benchmarking
- Product ecosystem analysis
- Strategic research
- Business intelligence workflows
- Forecasting and analytics development

All work emphasizes **reproducibility**, **clear documentation**, **verifiable provenance**, and **evidence-based analysis** — quantitative claims are sourced and dated, and where public estimates disagree, results are presented as ranges rather than single figures.

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
│   └── week10/          # forecast results, feature importances, Bass diffusion
├── reports/
│   ├── week01/ … week04/  # profiles, dossier, DQ report, sizing workbook + tornados
│   ├── week05/          # demand-signal methodology, pain-point taxonomy
│   ├── week06/          # peer benchmark one-pager, methodology memo
│   ├── week07/          # ER diagram, SQL self-assessment score sheet
│   ├── week08/          # dashboard specs, prototypes, design-review log, publish guide
│   ├── week09/          # Power BI scorecard spec + prototype, mid-internship review
│   └── week10/          # 5-page demand forecast report + charts
├── notebooks/           # one analysis notebook per week
├── src/
│   ├── ingest/          # 12 public-dataset ingestion modules + tests (Week 3)
│   ├── signals/         # demand-signal pipeline (Week 5)
│   ├── financials/      # peer-benchmark model (Week 6)
│   ├── warehouse/       # star schema, synthetic generator, SQL assessment (Week 7)
│   ├── dashboards/      # dashboard prototype + spec builders (Week 8)
│   ├── powerbi/         # scorecard prototype + review builder (Week 9)
│   └── forecast/        # baselines, Prophet, XGBoost, Bass diffusion (Week 10)
├── docs/                # data_standards.md, dax_measures.md, data dictionaries
├── dashboards/          # BI dashboards (Phase 3)
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

> Honesty note: published estimates disagree widely (e.g., humanoid robots ~$290M–$4.89B; security robots ~$4.7B–$19B depending on scope), so every figure is a sourced range. Humanoid and outdoor-patrol sizes are scenario ranges, not forecasts.

#### Week 5 — Demand Signals & Customer-Behavior Analysis
Three public signal families per vertical — Google Trends search interest, GDELT news volume/tone, and voice-of-customer review mining (TF-IDF + KMeans) — combined into a weighted demand-signal index; pain-point taxonomy per vertical.
✓ Demand-Signal Dataset (long format) ✓ Demand-Signal Index (documented weights) ✓ Pain-Point Taxonomy (5 themes/vertical, ≥3 examples each) ✓ Methodology PDF ✓ Tests ✓ Notebook

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
→ *The .pbix is assembled in Power BI Desktop from the spec + DAX (Windows step).*

### Phase 4 — Advanced Analytics

#### Week 10 — Predictive Modeling: Adoption & Demand Forecasting
24-month demand-momentum forecasts per vertical using baselines (seasonal-naive, ETS, ARIMA) and stronger models (Prophet, XGBoost with engineered features), backtested on a 12-month holdout (MAPE + MASE); Bass diffusion model for humanoid adoption anchored to cited analyst shipment guidance.
✓ Forecasting Notebook ✓ Forecast Results Table (vertical / model / MAPE / MASE / 12m / 24m) ✓ 5-Page Forecast Report ✓ XGBoost Feature Importances ✓ Bass Diffusion (humanoid)

> Best model by MASE: eldercare → ETS · education → Prophet · indoor_security → XGBoost · outdoor_patrol → Prophet · humanoid → ETS (MASE < 1 beats the naive benchmark). Humanoid Bass fit hits Goldman Sachs anchors (~20k/2025 → 250k/2030 → 1.4M/2035); cross-checked vs Morgan Stanley (13M in service by 2035). Forecasts are a relative demand-momentum read from public signals, not absolute unit/market forecasts.

---

## Tools & Technologies
Languages: Python · SQL · R

Libraries: pandas · numpy · matplotlib · openpyxl · reportlab · pyarrow · pytest · scikit-learn · statsmodels · prophet · xgboost · scipy · faker · duckdb

Data & Analytics: DuckDB · Tableau · Power BI · Looker Studio

Research Sources: U.S. Census Bureau · BLS · NCES · OECD · World Bank · FBI Crime Data Explorer · SEC EDGAR · USPTO / Justia / Google Patents · OpenAlex · GDELT · Google Trends · Crunchbase / CB Insights · Goldman Sachs & Morgan Stanley research (humanoid shipment guidance) · public company websites & filings · industry market-research summaries

---

## Current Progress
Completed:
✓ Week 1 — Foundations & Robotics Industry Landscape  
✓ Week 2 — Competitive Intelligence Deep Dive  
✓ Week 3 — Public-Data Pipelines & Warehouse  
✓ Week 4 — Market Sizing (TAM / SAM / SOM)  
✓ Week 5 — Demand Signals & Customer-Behavior Analysis  
✓ Week 6 — Financial Peer Benchmarking  
✓ Week 7 — SQL Fluency & Simulated Analytics Warehouse  
✓ Week 8 — Interactive Dashboards (specs, extracts, prototypes; publishing in progress)  
✓ Week 9 — Power BI, DAX & Mid-Internship Review  
✓ Week 10 — Predictive Modeling: Adoption & Demand Forecasting

In Progress / Upcoming:
→ Week 11 — Anomaly Detection (Sentinel Prime AI use case)  
→ Weeks 12–13 — Applied modeling on inGen use cases + capstone

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

---

## Guiding Principles
- Reproducible workflows
- Source attribution and dated provenance
- Clear documentation
- Analytical rigor
- Ranges over false precision where evidence is uncertain
- Cautious interpretation of company-reported claims
- Synthetic and fallback data always clearly labelled — never presented as real

---

## Disclaimer
This repository is intended for internship learning, public-data analytics practice, and structured market research. Analyses are based on publicly available information unless otherwise stated. Market-size figures and forecasts are planning estimates (not investment advice); vendor market totals should be verified against the original reports before external use. Weeks 7–10 use synthetic data where noted; forecasts are relative demand reads, not absolute market predictions.

---
**Last Updated:** July 2026
