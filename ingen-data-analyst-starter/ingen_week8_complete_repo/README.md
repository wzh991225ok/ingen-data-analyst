# ingen-data-analyst — Week 8

Data Analyst Internship · Ziheng Wang · inGen Dynamics Inc.
**Week 8 — Interactive Dashboards (Tableau Public + Looker Studio)** (12–18 Jun 2026)

Two dashboards: a public **Market & Competitive** view (Tableau) from Weeks 4-6, and a **Simulated
Product Analytics** view (Looker Studio) on the Week 7 warehouse. This package contains the specs,
the upload-ready extracts from real data, high-fidelity prototypes, the design-review log, and a
step-by-step publish guide. Publishing to the live SaaS tools is the final step in your own accounts.

## Deliverables
| Deliverable | File |
|-------------|------|
| Dashboard specs (PDF) | `reports/week08/spec_market_competitive.pdf`, `spec_product_analytics.pdf` |
| Prototypes (from real data) | `reports/week08/prototype_market_competitive.png`, `prototype_product_analytics.png` |
| Upload-ready extracts | `data/week08/extracts/*.csv` |
| Design-review log | `reports/week08/design_review_log.md` |
| Publish guide + URL file | `reports/week08/PUBLISH_GUIDE.md`, `dashboard_urls.md` |

## Build
```bash
pip install pandas matplotlib reportlab duckdb
python -m src.dashboards.build_prototypes   # regenerate prototypes from extracts
python -m src.dashboards.build_specs        # regenerate the two spec PDFs
```

## Data integrity
- Product-analytics extracts are aggregated from the real Week 7 DuckDB warehouse; market/peer extracts
  are the real Week 5/6 outputs. Market-sizing dollars link to the Week 4 workbook (not re-keyed).
- Prototypes are clearly labeled as rendered-from-data, **not** screenshots of a live dashboard.
- No Tableau/Looker URL is fabricated — publishing happens in your accounts (PUBLISH_GUIDE.md).
