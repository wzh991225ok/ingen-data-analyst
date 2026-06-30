# Week 8 — Design Review Log

Applied a design checklist to both dashboards before sign-off. Each item: what was checked, the
finding, and the change made.

## Checklist & changes

### 1. Color-blind-safe palette
- **Checked:** ran the palette against deuteranopia/protanopia/tritanopia (Color Oracle-style).
- **Finding:** an earlier draft used red/green for "good/bad" win-rate bars — indistinguishable for red-green color blindness.
- **Change:** switched the entire palette to **Okabe-Ito** (blue / orange / bluish-green / vermillion / reddish-purple / sky). All five product lines now use distinct Okabe-Ito hues that remain distinguishable under all three simulations. Severity uses an ordered sequential ramp, not red↔green.

### 2. Chart-type appropriateness
- **Checked:** each panel's chart type vs. the data it shows.
- **Finding:** a draft donut chart for win-rate-by-product; donuts make ordered comparison hard.
- **Change:** replaced with horizontal bars. Trends → lines; per-product comparison → bars; two continuous measures (margin↔R&D) → scatter; cumulative bookings → area. No pie/donut anywhere.

### 3. Label legibility
- **Checked:** axis labels, data labels, legend text at 100% and on a laptop screen.
- **Finding:** two products both abbreviated to "Aido", and the longest vertical label ("Sentinel Prime AI") was clipped on a narrow axis.
- **Change:** introduced explicit short labels ("Aido Rover", "Aido Hum.", "Sentinel") and widened the affected panel margins. Data values are labeled directly on bars to reduce reliance on gridlines.

### 4. Mobile / small-screen preview
- **Checked:** first-screen readability at a narrow width.
- **Finding:** the KPI band wrapped awkwardly when too many cards were forced onto one row.
- **Change:** capped the KPI band at five scorecards and kept panels in a 2-3 column grid that reflows; the headline question is answerable on the first screen without horizontal scrolling.

### 5. First-screen answerability (success criterion)
- **Checked:** can a viewer answer the dashboard's stated question without scrolling?
- **Finding:** OK for both — Market & Competitive leads with the demand-index ranking + attractiveness; Product Analytics leads with the KPI band + fleet/sales panels.

### 6. Performance (success criterion)
- **Checked:** extract sizes that drive load time.
- **Finding:** the raw warehouse is 100k+ rows; loading it directly would be slow.
- **Change:** dashboards are fed **pre-aggregated extracts** (largest is ~3.6k rows), so both load well under 5 seconds. Raw data stays in the warehouse; only aggregates are published.

## Residual notes
- Precise TAM/SAM/SOM dollars are linked to the Week 4 workbook rather than re-keyed, to avoid a second source of truth.
- EV/Revenue is intentionally left to compute live in the Peers tab, not baked into the extract (avoids staleness).
