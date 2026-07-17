# HANDOFF

**From:** Ziheng Wang, Data Analyst Intern (Futurenauts) · 13-week internship, Weeks 1–13 complete
**To:** whoever picks this up next
**Repo:** https://github.com/wzh991225ok/ingen-data-analyst (`main`)

This is written so you can be useful on day one. Read §1 and §2 (10 minutes), then go to the
workstream you need in §4.

---

## 1. What this repository is

Thirteen weeks of public-data analytics on InGen's five-vertical robotics portfolio — Fari
(eldercare), Senpai (education), Sentinel Prime AI (indoor security), Aido Rover (outdoor patrol),
Aido Humanoid (humanoid).

**Everything rests on public data or clearly-labelled synthetic data. No InGen internal data was
used anywhere.** That's the single most important fact about this repo, and §3 is the list of things
that follow from it.

Each week is a self-contained module: `plan/weekNN.md` (what was asked), `src/<area>/` (the code),
`data/weekNN/` (outputs), `reports/weekNN/` (deliverables + `status.md`), and a test suite where
applicable.

**Start here:** `reports/week13/capstone_report.pdf` — 23 pages, everything in one place. If you
have three minutes instead of thirty, read its one-page executive summary, or
`reports/week13/Capstone_Executive_Deck.pdf` (15 slides).

---

## 2. Day one: get it running

```bash
git clone https://github.com/wzh991225ok/ingen-data-analyst.git
cd ingen-data-analyst
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Then, in order of "most likely to be useful":

```bash
# The analytics warehouse everything downstream depends on
python -m src.generator.generate_synthetic
python -m src.warehouse.build_warehouse
python -m src.queries.run_queries            # 15 reference queries, should all pass

# Anomaly detection — this one uses REAL public data and downloads it
python -m src.anomaly.run_all                # NAB + SKAB, cached after first run
python -m src.anomaly.build_report
python -m pytest src/anomaly/tests -q        # 12 tests

# Process optimisation (needs the Week 7 warehouse)
export WEEK7_DB=$(pwd)/data/week07/ingen_warehouse.duckdb
python -m src.process.stage_generator
python -m src.process.capacity_sim
python -m pytest src/process/tests -q        # 12 tests
```

If a test fails on a clean checkout, that's a bug — not you. See §5.

---

## 3. Known issues — read before trusting any number

These are ordered by how badly they'd bite you.

| # | Issue | What it affects | Fix |
|---|---|---|---|
| 1 | **No internal InGen data anywhere** | Everything. Market bottom-ups use assumed penetration, not observed conversion. Weeks 7–9 and 12 are synthetic. | Get read access to one real slice. See §6. |
| 2 | **Live API collectors were never run against the live APIs** | Weeks 3, 5, 6 ran on labelled offline fallbacks. The collector code is real and tested; the sandbox had no egress. | Run in a networked environment: `INGEST_ALLOW_NETWORK=1 python -m src.ingest.run_all`. Week 11 shows what changes when real data is reachable. |
| 3 | **Three dashboards are built but not published** | No live URLs exist. Specs, extracts and prototypes are complete. | Publish from `data/week08/extracts/` using your own Tableau/Google/Power BI accounts. ~1 afternoon. |
| 4 | **Executive scorecard KPI targets are my assumptions** | Every traffic light on the Power BI scorecard. Two sit amber; that's the mechanism, not a verdict. | Confirm the real targets with leadership, then edit `docs/dax_measures.md` + the spec. |
| 5 | **Week 12's findings are properties of a simulation** | The −23% parts-buffer number and everything in `reports/week12/`. The *method* is validated (7/9 generating effects recovered); the *numbers* need real tickets. | Point `src/process/` at real ticket data with stage timestamps. |
| 6 | **Week 11 thresholds are fitted to NAB, not to Sentinel** | The 120-min / score-2.16 operating point. It transfers as a **method, not as a constant**. | Re-derive on real Sentinel telemetry before any field use. |
| 7 | **Week 12 hardcodes a path to the Week 7 warehouse** | `src/process/stage_generator.py` `DEFAULT_DB`. | Set `WEEK7_DB` env var (supported), or fix the default to a repo-relative path. Small, worth doing. |
| 8 | **Bass curve inherits its anchors' uncertainty** | The humanoid adoption curve. Goldman and Morgan Stanley differ ~3× on 2035. | Nothing to fix — just never quote it as a point estimate. It's shape, not level. |

---

## 4. Picking up each workstream

### Market sizing (Week 4)
**State:** complete. Dual-method (top-down + bottom-up), reconciled, with a tornado sensitivity per vertical.
**Where:** `notebooks/week04_market_sizing.ipynb` · `reports/week04/market_sizing_workbook.xlsx` · `reports/week04/assumptions_register.csv`
**To update:** every assumption is a named row in the register with a source or a judgement flag. Change the assumption, re-run the notebook, the workbook and tornado charts regenerate.
**Careful:** the numbers are ranges. If someone asks you for "the" market size, the honest answer is a range plus the anchor behind each bound. Penetration rate dominates the sensitivity in every vertical — that's where to spend effort if you want to narrow the range.
**TODO:** re-run with InGen's actual conversion rates once available; that turns assumed penetration into observed penetration and collapses most of the range.

### Competitive intelligence (Weeks 1–2)
**State:** complete. 40+ landscape, 15 priority peers with real patents/headcounts, all dated.
**Where:** `data/week02/peers_positioning.csv` · `data/week02/patent_activity.csv` · `reports/week02/competitive_intelligence_dossier.pdf`
**To update:** `retrieved` column on every row is the retrieval date. Anything older than ~6 months in this industry is stale — re-check patents (Justia/Google Patents) and funding (press) first, since those move fastest.
**Careful:** I deliberately left out real-time hiring counts (no dated snapshot I could stand behind) and several vendor deployment claims (only source was their own marketing). If you add them, add a source column too.
**TODO:** the "funding ≠ IP" finding deserves a quantified version — a patent-density-per-dollar-raised metric across the 15 peers would make it a chart instead of an argument.

### Public-data pipeline (Week 3)
**State:** complete, 12 datasets, 15 tests passing, but **never run against live APIs** (issue #2).
**Where:** `src/ingest/` — one collector per source, all with an offline fallback and a manifest.
**To run live:** `INGEST_ALLOW_NETWORK=1 python -m src.ingest.run_all`. Census and FBI need API keys via env vars (`CENSUS_API_KEY`, `FBI_API_KEY`); no keys are committed.
**Careful:** every collector writes a manifest row with source URL, retrieval timestamp and row count. Keep that habit — it's what makes the whole thing auditable.
**TODO:** run it live, diff the outputs against the fallbacks, and see how much of Weeks 4–6 moves. That's the single fastest way to find out how much the fallbacks cost us.

### Demand signals (Week 5)
**State:** complete. Search 40% / news 35% / sentiment 25%, weights justified in the methodology PDF.
**Where:** `notebooks/week05_demand_signals.ipynb` · `data/week05/demand_signal_index.csv` · `reports/week05/demand_signal_methodology.pdf`
**Careful:** the index is **relative** — it compares our five verticals to each other, not to an external benchmark. Don't read 64 as "64% of something."
**TODO:** the weights are defensible but not empirical. Once there's real pipeline data, regress the index against actual lead volume and let the data set the weights.

### Financial benchmarking (Week 6)
**State:** complete. Real FY2024 filings for 4 public peers, sourced funding for 6 private ones.
**Where:** `src/financials/peer_data.py` (source + retrieval date per row) · `reports/week06/peer_financial_workbook.xlsx`
**To update:** FY2025 filings will land through 2026 — update `peer_data.py`, everything downstream regenerates.
**Careful:** EV/Revenue is deliberately **not** frozen into the workbook; it needs a live quote or it silently goes stale. Private "valuations" are negotiated post-money numbers, not market prices — the workbook doesn't treat them as comparable to public market caps, and neither should you.

### Warehouse + SQL (Week 7)
**State:** complete. Star schema, 3 facts / 4 dims, 100k telemetry + 5k tickets + 1k pipeline, fixed seed, FK integrity checked on every load.
**Where:** `src/warehouse/schema.sql` · `src/generator/generate_synthetic.py` · `src/queries/reference_queries.sql`
**This is the most reusable thing in the repo.** The schema mirrors what an InGen analytics team would actually hold, so real data slots in with minimal rework and every dashboard/query above it keeps working.
**TODO:** when real data arrives, keep the schema, swap the generator for a loader. The 15 reference queries become a regression suite for the real warehouse.

### Dashboards (Weeks 8–9)
**State:** specs + extracts + prototypes complete; **none published** (issue #3).
**Where:** `reports/week08/spec_*.pdf` · `reports/week09/spec_powerbi.pdf` · `docs/dax_measures.md` · `data/week08/extracts/` · `reports/week13/dashboard_pack.pdf` (how to read each one)
**To publish:** the extracts are upload-ready. Tableau Public → publish the workbook; Looker Studio → Sheets connector on the extract; Power BI → Desktop + a workspace.
**Careful:** keep the Okabe-Ito palette (an earlier red/green draft was rejected in review — `reports/week08/design_review_log.md` says why) and keep feeding pre-aggregated extracts, not raw 100k-row tables.

### Forecasting (Week 10)
**State:** complete. 5 models × 5 verticals, backtested on a held-out year, scored MAPE + MASE.
**Where:** `notebooks/week10_forecasting.ipynb` · `src/forecast/` · `data/week10/forecast_results.csv`
**The harness is the asset:** add a model to `src/forecast/models.py` and it's automatically scored against the naive baseline on the same splits. That's how you should evaluate anything new.
**Careful:** the target is **search-interest momentum (0–100), not units**. MASE < 1.0 = beats seasonal-naive. Fari sits at exactly 1.00 — no better than naive — and it's reported that way on purpose. Don't quietly drop it.
**TODO:** re-point at real sales/pipeline data. The harness doesn't care what the series is.

### Anomaly detection (Week 11)
**State:** complete, and **this one runs on real public data** (NAB — MIT; SKAB — GPL-3.0).
**Where:** `notebooks/week11/week11_anomaly_detection.ipynb` · `src/anomaly/` · `reports/week11/sentinel_operational_framing.pdf`
**Key results:** AutoEncoder best on NAB (F1 0.555), LOF best on SKAB (F1 0.545), both beat the control-chart baseline. The 5% false-alarm budget is **unreachable** at 80% recall (~13% floor) — that's a model-quality ceiling, not a tuning problem. The win is persistence filtering: 120-min sustained → 0.50 false alerts/day vs 16.35, recall 88%, 4/4 events caught.
**Careful:** issue #6 — thresholds are fitted to a machine-temperature signal. Method transfers; constants don't.
**TODO:** re-derive on real Sentinel telemetry; then implement the two-tier rule (fast tier for intrusion, sustained tier for degradation).

### Process optimisation (Week 12)
**State:** complete. DES of the support lifecycle replaying Week 7's real ticket stream; 5 scenarios × 8 replications.
**Where:** `notebooks/week12/week12_process_optimization.ipynb` · `src/process/` · `reports/week12/process_optimization_memo.pdf`
**Key results:** Parts & dispatch = 53% of process time and 100% waiting. Brief's drivers explain R²=0.04; adding the dispatch path → R²=0.72 (+578%). Parts buffer −23%, +1 Field FTE −8%, both −29%, reroute Tier-1 **not significant**.
**Careful:** issue #5 — these are simulation results. Team sizes (Tier1=1, Tier2=2, Field=1) were chosen to load the teams realistically against the observed ~6.8 tickets/day, **not observed from data**. No shift calendar is modelled, so the null weekday result isn't evidence weekday doesn't matter.
**TODO:** feed real tickets with stage timestamps; the reconciliation checks in `stage_generator.verify()` will tell you immediately if the join is wrong.

---

## 5. Conventions worth keeping

- **Sourced or not stated.** Every quantitative claim carries a source and a date. If you can't source it, leave it out — and say you left it out.
- **Ranges over false precision.** When published estimates disagree by an order of magnitude, a single number is a lie with a decimal point.
- **Label synthetic data every single time.** Never let a generated number travel without its label. The moment one does, the whole repo's credibility goes with it.
- **Seed everything.** Week 7 generator, Week 11 (`random_state=42`), Week 12 (`SEED=20260710`). Reproducibility is a feature.
- **Validate the method where ground truth exists.** Week 12's regression was checked against its own simulation's known parameters; Week 10's models against naive baselines; Week 11's detectors against a control chart. If you build something new, find its baseline.
- **Test the things that would silently break.** Causality (no look-ahead in rolling features), reconciliation (stage durations sum to cycle time), FK integrity (zero orphans). Those tests exist because those bugs are invisible otherwise.

## 6. If you do one thing

**Get read access to one small, anonymised slice of real InGen data** — fleet telemetry or sales
pipeline, a few thousand rows is plenty.

The synthetic warehouse already matches the intended schema, so real data slots in with minimal
rework, and it dissolves most of §3 at once: the warehouse becomes real, the dashboards become
operational, Week 12's diagnostic becomes a measurement instead of a simulation, and the forecasts
gain something to calibrate against.

Everything else in this repo is built and waiting for it.

---

*Ziheng Wang · wzh38098928@outlook.com · Weeks 1–13 complete.*
