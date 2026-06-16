# src/financials — Peer Benchmark Model (Week 6)

Builds a financial peer-comp model for robotics & humanoid companies from public disclosures.

## Run
```bash
python -m src.financials.build_workbook    # -> reports/week06/peer_financial_workbook.xlsx
python -m src.financials.build_reports     # -> benchmark one-pager + methodology memo (PDF)
python -m pytest src/financials/tests -q   # 5 tests

# filing-exact 12-quarter history from SEC EDGAR (no key; needs User-Agent):
INGEST_ALLOW_NETWORK=1 python -m src.financials.edgar_fetch
```

## Modules
| File | Role |
|------|------|
| `peer_data.py` | REAL sourced anchors: public FY2024 financials + private funding rounds (source per row) |
| `edgar_fetch.py` | live SEC EDGAR companyfacts pull (exact quarterly revenue/GP/R&D/op income) |
| `build_workbook.py` | 4-sheet workbook: public_financials, private_funding, valuation_comps, summary |
| `build_reports.py` | benchmark one-pager (5 panels) + methodology & caveats memo |

## Data integrity
Public = SEC FY2024 filings/earnings; private = press-sourced rounds; every row carries its source. Estimated
cells are flagged yellow. EV/Revenue is left to compute at use-time from a live quote (never stale). Private
valuations are negotiated post-money figures, not market prices — see the memo's caveats.
