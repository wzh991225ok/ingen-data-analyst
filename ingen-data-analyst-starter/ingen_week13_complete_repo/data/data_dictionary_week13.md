# Data Dictionary — Week 13 (Capstone)

Week 13 produces **no new data**. It synthesises Weeks 1–12 into reports.
Every number in the capstone is loaded at build time from the committed outputs below — nothing is
retyped, so the report cannot drift from the data.

## Inputs read by `src/capstone/build_capstone.py`
| Source file | Feeds |
|---|---|
| `data/week05/demand_signal_index.csv` | §5 demand ranking table + the inversion finding |
| `data/week10/forecast_results.csv` | §8 best-model table (MAPE, MASE, 24-month estimates) |
| `data/week10/bass_humanoid.csv` · `bass_params.txt` | §8 Bass diffusion figures and cumulative installed base |
| `data/week11/results.csv` | §9 five-detector comparison |
| `data/week11/operational_frontier.csv` | §9 persistence / alerts-per-day finding |
| `data/week11/dataset_licenses.csv` | §9 + Appendix B licence tables |
| `data/week12/stage_decomposition.csv` | §10 where-the-time-goes table |
| `data/week12/capacity_sim_paired_deltas.csv` | §10 scenario deltas + CIs |
| `data/week12/driver_effects.csv` | §10 dispatch-path effect |
| `src/financials/peer_data.py` (Week 6) | §6 public peer financials + private funding |
| `data/week02/peers_positioning.csv` | §4 the 15 priority peers |

## Figures embedded (all real artifacts from the week that produced them)
`tornado_sentinel.png` (W4) · `demand_index.png` (W5) · `er_diagram.png` (W7) ·
`prototype_market_competitive.png` · `prototype_product_analytics.png` (W8) ·
`prototype_powerbi_scorecard.png` (W9) · `fc_humanoid.png` · `bass_humanoid.png` (W10) ·
`pr_curves.png` · `operational_frontier.png` (W11) · `wait_vs_service.png` · `scenario_comparison.png` (W12)

## Outputs
| File | What |
|---|---|
| `reports/week13/capstone_report.pdf` | 23-page capstone (= the consolidated internship report) |
| `reports/week13/Capstone_Executive_Deck.pptx` / `.pdf` | 15-slide executive deck |
| `reports/week13/dashboard_pack.pdf` | Dashboard pack + one-page reading guide |
| `reports/week13/feedback_log.md` | Final review agenda, expected Q&A, feedback template |
| `HANDOFF.md` · `INDEX.md` | Handoff documentation |
