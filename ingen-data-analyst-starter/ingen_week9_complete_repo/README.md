# ingen-data-analyst — Week 9

Data Analyst Internship · Ziheng Wang · inGen Dynamics Inc.
**Week 9 — Power BI, Mid-Internship Review & Documentation** (19–25 Jun 2026)

Closes the BI phase: an executive-scorecard spec + prototype (Power BI, third BI tool), 10 documented
DAX measures, repo housekeeping (top-level INDEX.md), and a 5-page mid-internship review packet.

## Deliverables
| Deliverable | File |
|-------------|------|
| Power BI scorecard spec + prototype | `reports/week09/spec_powerbi.pdf`, `prototype_powerbi_scorecard.png` |
| 10 DAX measures (documented) | `docs/dax_measures.md` |
| Repo INDEX (Weeks 1–9) | `INDEX.md` |
| Mid-internship review (5-page) | `reports/week09/mid_internship_review.pdf` |

## Build
```bash
pip install duckdb matplotlib reportlab
python -m src.powerbi.build_scorecard_prototype   # exec scorecard from real warehouse KPIs
python -m src.powerbi.build_reports               # Power BI spec + 5-page review packet
```

## Data integrity
- Scorecard KPIs are computed from the real Week 7 warehouse; prototype is labeled as rendered-from-data.
- DAX measures are generic (no hard-coded product/date) so they're reusable across pages.
- No `.pbix` is fabricated — it's assembled in Power BI Desktop from the spec + DAX (your Windows step).
