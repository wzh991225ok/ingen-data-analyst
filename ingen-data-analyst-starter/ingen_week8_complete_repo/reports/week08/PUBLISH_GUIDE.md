# Week 8 — How to Publish (Tableau Public & Looker Studio)

The specs + prototypes + extracts make these mechanical. These final steps run in **your own
accounts** (they can't be automated from the build environment, and no URL is auto-generated).

## Tableau Public — Market & Competitive
1. Open Tableau Public Desktop → Connect → Text file → load the four extracts from `data/week08/extracts/`
   (`demand_index.csv`, `peer_public_financials.csv`, `peer_private_funding.csv`, `market_sizing_summary.csv`).
2. Relate them on `vertical` / `product` where applicable.
3. Build the five tabs per `spec_market_competitive.pdf` (Overview first). Use the prototype PNG as the layout target.
4. Apply the Okabe-Ito palette (custom colors in Tableau preferences) — see design_review_log.md.
5. Add the global **Vertical** and **Wave** filters; set them to apply to all worksheets.
6. File → Save to Tableau Public → copy the public URL into `reports/week08/dashboard_urls.md`.
7. Take a screenshot of each tab → save to `reports/week08/screenshots_tableau/`.

## Looker Studio — Product Analytics
1. Looker Studio → Create → Data source → File upload → upload the four product-analytics extracts.
2. Create a report; add the KPI scorecards + six panels per `spec_product_analytics.pdf` (prototype as target).
3. Add a **Date-range** control and a **Product-line** filter control; confirm they drive every chart.
4. Apply the color-blind-safe theme.
5. Share → set link access → copy the share link into `reports/week08/dashboard_urls.md`.
6. Screenshot the report → `reports/week08/screenshots_looker/`.

## After publishing
- Fill in `dashboard_urls.md` with both links.
- Confirm each loads in <5s and answers its question on the first screen (success criteria).
