# Week 6 — Financial Peer Benchmarking & Comparable Modeling
**Dates:** 29 May – 04 Jun 2026 · **Phase 2 — Market & Competitive Analytics** · 25 hrs

## Tasks
- Peer universe: public (iRobot, Teradyne, Cognex, Symbotic) + private (Figure, Apptronik, Agility, 1X, Neura, Gecko from Week 2 dossier).
- Public financials: last-12-quarter revenue, gross margin, R&D %, operating margin from SEC EDGAR (10-Q/10-K). FY2024 anchors hard-sourced; edgar_fetch.py pulls exact quarters live.
- Private funding history: round, date, amount, lead investor, post-money — press-sourced per row.
- Valuation comparables: revenue growth + margin/R&D intensity (public); funding-per-employee (private). Documented caveats.
- Benchmark one-pager: 5 panels (revenue scale, growth, gross margin, R&D intensity, capital raised).

## Deliverables
- [x] Peer financial workbook → reports/week06/peer_financial_workbook.xlsx (sheets: public_financials, private_funding, valuation_comps, summary)
- [x] Benchmark one-pager → reports/week06/benchmark_one_pager.pdf
- [x] Methodology + caveats memo → reports/week06/methodology_and_caveats.pdf

## Success criteria
- [x] Public-peer financials reconcile to source filings within rounding (FY2024 sourced; estimates flagged yellow; exact quarters via edgar_fetch.py)
- [x] Private-peer funding rows cite a public press source for every round
- [x] Valuation-comp table includes documented caveats about comparability
- [x] Benchmark one-pager readable in under 30 seconds

## Honesty note
Network-restricted here, so the workbook uses FY2024 anchors from SEC filings/earnings (each row sourced) and flags
any annualised/approx cell; run edgar_fetch.py with INGEST_ALLOW_NETWORK=1 for filing-exact 12-quarter data. Private
valuations are negotiated post-money figures, not market prices — caveats documented in the memo. EV/Revenue is computed
at use-time from a live quote, not hard-coded, to avoid staleness.
