# Data Dictionary — Week 6

## Workbook: reports/week06/peer_financial_workbook.xlsx
| Sheet | Columns |
|-------|---------|
| public_financials | Ticker, Company, FY, Revenue ($M), Rev YoY, Gross margin, R&D ($M), R&D % rev, Op margin, Net margin, Data quality, Source |
| private_funding | Company, Round, Date, Amount ($M), Post-money ($B), Lead investors, Employees, Source |
| valuation_comps | Company, Type, Rev growth/scale, Gross margin, R&D intensity, Capital efficiency, Caveat |
| summary | Topic, Read |

## Sources (real, public)
| Source | Access | Used for |
|--------|--------|----------|
| SEC EDGAR 10-K/10-Q + earnings | data.sec.gov companyfacts API (no key) | public financials (FY2024 anchors + exact quarters) |
| Company press releases / tech press | public URLs | private funding rounds (each row cited) |

## Definitions
- Rev YoY = revenue / prior-year revenue − 1.
- R&D % rev = R&D expense / revenue.
- Funding-per-employee = total disclosed raised / headcount (private capital-efficiency proxy).
- EV/Revenue = NOT hard-coded; compute from a live market cap (+ net debt) at use-time.

## Data-quality flags
Cells/rows marked "approx" or "annualised" (yellow) are estimates from partial-year data and should be confirmed
against the exact filing. Retrieved 2026-06-15. Every public row and every private round carries its source.
