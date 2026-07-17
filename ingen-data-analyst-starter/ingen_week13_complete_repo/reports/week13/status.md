# Week 13 — Status
**Phase 5 · 17–23 Jul 2026 · FINAL WEEK**

## Done
- [x] Capstone report, 23 pages — every number loaded live from the committed outputs of Weeks 4–12, every section citing its source notebook/workbook
- [x] 15-slide executive deck (.pptx + PDF), readable standalone, 9 real figures embedded
- [x] Dashboard pack + one-page reading guide, with honest status per dashboard (all built, none published)
- [x] HANDOFF.md — day-one quickstart, ranked known issues, per-workstream pickup notes
- [x] Final INDEX.md across all 13 weeks
- [x] feedback_log.md — agenda + expected Q&A prepared; verbatim feedback section left empty until the session actually happens
- [x] Data dictionary index for all 13 weeks

## The six findings
1. Funding is not a moat — margin structure predicts durability
2. The biggest near-term market (Sentinel) is not the loudest one (humanoid)
3. Attention ≠ opportunity — demand ranking is the near-inverse of market attractiveness
4. Momentum up in all five verticals; MASE < 1.0 in four of five; no single model wins
5. Sentinel's alert problem is solved by persistence (33× fewer alerts), not by a better threshold
6. Support cycle time is a parts problem (53% of time, 100% waiting), not a people problem

## Internship status
**Weeks 1–13 complete.** The capstone report doubles as the consolidated internship report inGen
requested for closure.

## Run
```bash
python -m src.capstone.build_capstone         # 23-page report
python -m src.capstone.build_dashboard_pack   # dashboard reading guide
node src/capstone/make_capstone_deck.js       # 15-slide deck
```

## Outstanding (documented in HANDOFF.md §3)
- Three dashboards built but not published (needs personal Tableau/Google/Power BI accounts)
- Weeks 3/5/6 collectors never run against live APIs (sandbox egress)
- Executive scorecard KPI targets are assumptions, not InGen's actual targets
- Week 11 thresholds need re-deriving on real Sentinel telemetry before field use
