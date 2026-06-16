# Week 6 — Status
**Phase 2 · 29 May – 04 Jun 2026**

## Done
- [x] Peer universe (4 public + 6 private), each row sourced
- [x] public_financials (FY2024: revenue, YoY, gross margin, R&D %, op margin, net margin)
- [x] private_funding (disclosed rounds, lead investors, post-money, press source per row)
- [x] valuation_comps (public growth/intensity; private funding-per-employee; caveats column)
- [x] summary sheet (peer read for InGen)
- [x] Benchmark one-pager (5 panels) + methodology & caveats memo
- [x] Live SEC EDGAR fetcher (edgar_fetch.py) for exact 12-quarter history
- [x] 5 passing tests; analysis notebook

## Run mode
- Offline anchors (FY2024) used here; each row carries its SEC/press source. Cells marked approx/annualised are
  flagged yellow. For filing-exact quarters: `INGEST_ALLOW_NETWORK=1 python -m src.financials.edgar_fetch`.

## To validate before external use
- Confirm flagged cells (Cognex FY, Symbotic GM/R&D) against exact filings.
- Compute EV/Revenue from a live quote on the date of use.
- Extend private table via Crunchbase free tier as new rounds are announced.
