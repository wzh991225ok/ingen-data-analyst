# ingen-data-analyst — Week 2

Data Analyst Internship · Ziheng Wang · inGen Dynamics Inc.
**Week 2 — Competitive Intelligence Deep Dive** (01–07 May 2026)

Builds on Week 1's landscape. Narrows to **15 priority peers** (3 per vertical) and produces
structured competitive intelligence: positioning, partnerships, **real patent activity**, and a
**verifiable R&D-scale read** (real headcount + real patent portfolio).

## Deliverables (this folder)

| Deliverable | File |
|-------------|------|
| Peer set + positioning (machine-readable) | `data/week02/peers_positioning.csv` |
| Competitor profiles (15 peers) | `data/week02/competitor_profiles.xlsx` |
| Patent activity (real, with numbers) | `data/week02/patents.xlsx` |
| R&D scale (real headcount + IP) + honest hiring template | `data/week02/rd_scale_and_hiring.xlsx` |
| Competitive Intelligence Dossier (cover + 15 peer pages) | `reports/week02/competitive_intelligence_dossier.pdf` |
| Executive Summary | `reports/week02/executive_summary.pdf` |
| Analysis notebook | `notebooks/week02_competitor_analysis.ipynb` |
| Week status | `reports/week02/status.md` |

## Data-integrity stance
- **Patent data is real.** Specific patent numbers (e.g., Knightscope US 9,329,597; Boston Dynamics
  US 10,266,220 / US 10,253,855; Agility US 11,928,638 and design D888120) were located via
  Justia Patents, Google Patents, GreyB and PatentVest landscapes, and SEC filings.
- **Headcounts are real.** Employee counts come from SEC filings, Wikipedia, LinkedIn, Revelio Labs,
  and CB Insights, each with a source and as-of date in `rd_scale_and_hiring.xlsx`.
- **Real-time AI-ML hiring shares were NOT fabricated.** Aggregator open-role counts for the same
  company varied too widely to verify as a single dated snapshot, so R&D scale is shown via real
  headcount + real patent portfolio. A blank dated-snapshot template is included for a future
  single-day pull.
- **Funding figures** are best-effort from public sources and flagged for verification.

All sources are public and listed in `data/data_dictionary_week02.md`. Patent/positioning retrieved 2026-05-31; headcount retrieved 2026-06-01.
