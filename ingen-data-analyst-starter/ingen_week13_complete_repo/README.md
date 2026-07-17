# ingen-data-analyst — Week 13 (Capstone)

Data Analyst Internship · Ziheng Wang · inGen Dynamics Inc. (Futurenauts Program)
**Week 13 — Capstone Synthesis, Final Presentation & Handoff** (17–23 Jul 2026)
**Status: all 13 weeks complete.**

Thirteen weeks of public-data analytics on InGen's five-vertical robotics portfolio, synthesised
into one report a stakeholder can read in twenty minutes.

## Start here
| If you want... | Read |
|---|---|
| Everything, in one place | `reports/week13/capstone_report.pdf` (23 pages) |
| The three-minute version | Page 2 of the capstone — the executive summary stands alone |
| The presentation | `reports/week13/Capstone_Executive_Deck.pdf` (15 slides) |
| To pick up the work | `HANDOFF.md` |
| The file map | `INDEX.md` |
| The dashboards | `reports/week13/dashboard_pack.pdf` |

## Deliverables
| Deliverable | File |
|---|---|
| Capstone report (20–25pp target → 23pp) | `reports/week13/capstone_report.pdf` |
| Executive deck (.pptx + PDF export) | `reports/week13/Capstone_Executive_Deck.pptx` · `.pdf` |
| Dashboard pack + reading guide | `reports/week13/dashboard_pack.pdf` |
| HANDOFF.md + final INDEX.md | repo root |
| Final review feedback log | `reports/week13/feedback_log.md` |

## The six findings
1. **Funding is not a moat.** Capital raised and defensible IP diverge sharply. Margin structure predicts durability — Teradyne 58.5% and Cognex 68% gross margins are precision-instrument businesses; the consumer-robotics pure-play (iRobot) ran −15.1% operating in FY2024.
2. **The biggest near-term market is not the loudest one.** Sentinel Prime AI (indoor security) has the clearest economics. Humanoid gets the capital and the headlines — and published estimates span an order of magnitude.
3. **Attention ≠ opportunity.** The demand ranking is the near-inverse of market attractiveness. Sentinel is a strong asset with weak share of voice — a marketing problem, which is solvable.
4. **Momentum is up in all five verticals**, and models beat seasonal-naive in four of five (MASE < 1.0). No single model wins everywhere — ETS, Prophet and XGBoost each take a vertical.
5. **Sentinel's alert problem is solved by persistence, not by a better threshold.** The 5% false-alarm budget is unreachable at 80% recall (~13% floor — a model-quality ceiling). A 120-minute persistence filter cuts alert load 33× (16.35 → 0.50/day) while recall *rises* to 88%, catching 4/4 real failures.
6. **Support cycle time is a parts problem, not a people problem.** Parts & dispatch is 53% of process time and 100% unstaffed waiting. A regional parts buffer buys −23%; a field engineer −8%; rerouting triage does nothing measurable.

## Build
```bash
pip install -r requirements.txt
python -m src.capstone.build_capstone         # 23-page capstone report
python -m src.capstone.build_dashboard_pack   # dashboard pack + reading guide
node src/capstone/make_capstone_deck.js       # 15-slide executive deck (needs: npm install pptxgenjs)
```
Every number in the report is loaded at build time from the committed outputs of Weeks 4–12 — nothing
is retyped, so the report cannot drift from the data.

## Data integrity
**Everything rests on public data or clearly-labelled synthetic data. No InGen internal data was used
anywhere.** §11 of the capstone is an eight-item honest inventory of what that cost — synthetic
warehouse (Weeks 7–9, 12), offline fallbacks where live APIs were unreachable (Weeks 3, 5, 6),
dashboards built but not published, forecasts that are momentum reads rather than unit forecasts,
and the things I could not verify and therefore left out. Week 11 is the exception that proves the
point: real licensed public benchmarks (NAB — MIT; SKAB — GPL-3.0), and its results are measurements
on real sensor data.

**The one ask:** read access to one small anonymised slice of real InGen data. The synthetic
warehouse already matches the intended schema, so real data slots in with minimal rework — and it
dissolves most of §11 at once.
