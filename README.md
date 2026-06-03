# inGen Data Analyst Internship Repository
**Author:** Ziheng Wang  
**Program:** Futurenauts Internship Program — inGen Dynamics  
**Role:** Data Analyst Intern  
**Focus Areas:** Market Intelligence · Competitive Analysis · Business Intelligence · Robotics Industry Research · Data Engineering · Predictive Analytics

---

## Overview
This repository documents my internship work as a Data Analyst Intern at inGen Dynamics. The work focuses on analyzing AI, robotics, automation, education, security, and eldercare markets using publicly available datasets, industry reports, patents, employee data, and competitive intelligence.

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
│   └── week04/          # market-sizing assumptions register
├── reports/
│   ├── week01/          # product profiles, landscape report
│   ├── week02/          # competitive intelligence dossier, executive summary
│   ├── week03/          # data quality report (HTML)
│   └── week04/          # methodology memo, sizing workbook, tornado charts
├── notebooks/           # one analysis notebook per week
├── src/
│   └── ingest/          # 12 public-dataset ingestion modules + unit tests (Week 3)
├── docs/                # data_standards.md, schema_diagram.md
├── dashboards/          # BI dashboards (Phase 3)
├── requirements.txt
└── README.md
```

---

## Completed Deliverables

### Week 1 — Foundations & Robotics Industry Landscape
Topics covered:
- inGen product ecosystem profiling (Fari, Senpai, Sentinel Prime AI, Aido Rover, Aido Humanoid, Origami / PIC 2.0)
- Robotics market landscape mapping across five verticals
- Competitor identification
- Product positioning analysis
- Data source inventory & documentation
- Data dictionary construction

Deliverables:
✓ Product Profiles  
✓ Competitor Landscape Dataset  
✓ Data Dictionary  
✓ Market Mapping Notebook  
✓ Summary Reports

---

### Week 2 — Competitive Intelligence Deep Dive
Topics covered:
- Priority peer selection (15 competitors, 3 per vertical) with justification
- Competitive positioning & benchmarking
- Patent landscape review (real patent numbers per peer)
- R&D-scale analysis (real employee headcount + patent portfolio)
- Strategic positioning vs each inGen product
- Executive summary generation

Deliverables:
✓ Peer Positioning Dataset  
✓ Competitor Profiles  
✓ Patent Activity Tracking (with specific patent numbers)  
✓ R&D-Scale Dataset (real headcount + IP) and a dated hiring-snapshot template  
✓ Competitive Intelligence Dossier (cover + 15 peer pages)  
✓ Executive Summary

> Data-integrity note: patent numbers and employee counts are sourced from Justia / Google Patents, SEC filings, Wikipedia, Revelio Labs, and CB Insights. Real-time hiring counts were not fabricated — where they could not be verified to a single dated snapshot, R&D scale is shown via real headcount + patents instead.

---

### Week 3 — Public-Data Pipelines, Cleaning Standards & Warehouse
Topics covered:
- Public-dataset source inventory (12 datasets across verticals)
- Reusable, tested ingestion pipeline with raw-file hashing (SHA-256 versioning)
- Cleaning standards (snake_case, ISO dates, NULL handling, categorical normalization)
- DuckDB analytics warehouse with one schema per vertical
- Data-quality profiling and reporting

Deliverables:
✓ Ingestion Pipeline — 12 modules (Census, BLS, OECD, NCES, World Bank, FBI, OpenAlex, SEC EDGAR) + shared utilities  
✓ Unit Test Suite (15 tests)  
✓ DuckDB Warehouse (6 schemas, 12 tables + cross-cutting view)  
✓ Data Standards & Schema Documentation  
✓ Ingest Manifest (source, license, retrieval date, SHA-256, row/col counts per dataset)  
✓ Data Quality Report (row counts, null rates, dtypes, time coverage)  
✓ Pipeline & QA Notebook

---

### Week 4 — Market Sizing (TAM / SAM / SOM)
Topics covered:
- TAM / SAM / SOM definitions and segmentation per vertical
- Top-down sizing from published market estimates (low/high anchors)
- Bottom-up sizing (units × serviceable % × penetration % × ASP)
- Reconciliation of the two methods per vertical
- One-at-a-time sensitivity (tornado) analysis

Deliverables:
✓ Methodology Memo  
✓ Market-Sizing Workbook (tab per vertical: top-down + bottom-up + reconciliation + sources, plus summary)  
✓ Sensitivity Tornado Charts (5 — one per vertical)  
✓ Assumptions Register (every driver: low / base / high, with swings)  
✓ Market-Sizing Notebook

> Honesty note: published market estimates disagree widely (e.g., humanoid robots ~$290M–$4.89B; security robots ~$4.7B–$19B depending on scope), so every figure is a sourced range. Humanoid and outdoor-patrol sizes are presented as scenario ranges, not forecasts.

---

## Tools & Technologies
Languages:
- Python
- SQL
- R

Libraries:
- pandas
- numpy
- matplotlib
- openpyxl
- reportlab
- pyarrow
- pytest
- scikit-learn *(forecasting, upcoming)*
- statsmodels *(forecasting, upcoming)*

Data & Analytics:
- DuckDB
- Tableau *(Phase 3)*
- Power BI *(Phase 3)*
- Looker Studio *(Phase 3)*

Research Sources:
- U.S. Census Bureau
- Bureau of Labor Statistics (BLS)
- National Center for Education Statistics (NCES)
- OECD
- World Bank
- FBI Crime Data Explorer
- SEC EDGAR
- USPTO / Justia / Google Patents
- OpenAlex
- Crunchbase / CB Insights
- Public company websites & filings
- Industry market-research summaries

---

## Current Progress
Completed:
✓ Week 1 — Foundations & Robotics Industry Landscape  
✓ Week 2 — Competitive Intelligence Deep Dive  
✓ Week 3 — Public-Data Pipelines & Warehouse  
✓ Week 4 — Market Sizing (TAM / SAM / SOM)

In Progress:
→ Demand & adoption forecasting  
→ Dashboard development (Tableau / Power BI / Looker)  
→ Deeper market & competitive analytics

---

## How to Run (Week 3 pipeline)
```bash
pip install -r requirements.txt
python -m src.ingest.run_all            # ingest 12 datasets (offline fallbacks by default)
python -m src.ingest.build_warehouse    # build DuckDB warehouse (per-vertical schemas)
python -m src.ingest.quality_report     # generate the HTML data-quality report
python -m pytest src/ingest/tests -q    # run the 15-test suite

# to pull from live public APIs (Census/FBI require a key via env var):
INGEST_ALLOW_NETWORK=1 python -m src.ingest.run_all
```

---

## Guiding Principles
This repository follows:
- Reproducible workflows
- Source attribution and dated provenance
- Clear documentation
- Analytical rigor
- Ranges over false precision where evidence is uncertain
- Cautious interpretation of company-reported claims

---

## Disclaimer
This repository is intended for internship learning, public-data analytics practice, and structured market research. Analyses are based on publicly available information unless otherwise stated. Market-size figures are planning estimates (not investment advice); vendor market totals should be verified against the original reports before external use.

---
**Last Updated:** June 2026
