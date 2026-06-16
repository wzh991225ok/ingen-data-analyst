# ingen-data-analyst — Week 6

Data Analyst Internship · Ziheng Wang · inGen Dynamics Inc.
**Week 6 — Financial Peer Benchmarking & Comparable Modeling** (29 May – 04 Jun 2026)

A reusable peer-comp model InGen can cite when investors/partners ask "how do you compare to peers on X".
Public financials are FY2024 from SEC filings/earnings; private rounds are press-sourced. Every figure carries provenance.

## Deliverables (this folder)
| Deliverable | File |
|-------------|------|
| Peer financial workbook | `reports/week06/peer_financial_workbook.xlsx` (public_financials, private_funding, valuation_comps, summary) |
| Benchmark one-pager (5 panels) | `reports/week06/benchmark_one_pager.pdf` |
| Methodology + caveats memo | `reports/week06/methodology_and_caveats.pdf` |
| Reusable model + tests | `src/financials/` (5 tests) |
| Analysis notebook | `notebooks/week06_peer_benchmark.ipynb` |

## Quick start
```bash
pip install -r requirements.txt
python -m src.financials.build_workbook
python -m src.financials.build_reports
python -m pytest src/financials/tests -q

# filing-exact 12-quarter financials from SEC EDGAR (no key):
INGEST_ALLOW_NETWORK=1 python -m src.financials.edgar_fetch
```

## Peer universe
- **Public:** iRobot (IRBT), Teradyne (TER), Cognex (CGNX), Symbotic (SYM)
- **Private:** Figure AI, Apptronik, Agility Robotics, 1X Technologies, Neura Robotics, Gecko Robotics (Week 2 dossier)

## Data-integrity stance
- Public figures are FY2024 from SEC 10-K/10-Q & earnings; private rounds each cite a public press source.
- Cells from partial-year data are flagged "approx/annualised" (yellow) and should be confirmed against the exact filing.
- `edgar_fetch.py` pulls filing-exact 12-quarter history live (no key, descriptive User-Agent).
- EV/Revenue is computed at use-time from a live quote, never hard-coded — avoids stale valuations.
- Private post-money valuations are negotiated round figures, not market-clearing prices (caveats in the memo).

Sources & definitions: `data/data_dictionary_week06.md`.
