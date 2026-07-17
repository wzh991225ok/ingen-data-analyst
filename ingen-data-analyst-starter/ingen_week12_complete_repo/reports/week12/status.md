# Week 12 — Status
**Phase 4 · 10–16 Jul 2026**

## Done
- [x] Discrete-event process model of the support-ticket lifecycle (simpy), replaying Week 7's real ticket stream
- [x] Stage-level event table (23.8k rows, 6 stages) reconciling exactly to Week 7 — 5/5 checks PASS
- [x] Cycle-time decomposition + Pareto + wait-vs-service split + weekly control chart
- [x] Driver regression with 95% CIs + validation against known generating parameters (7/9 directions recovered)
- [x] Capacity simulation: 5 scenarios x 8 replications, paired deltas with CIs
- [x] 3-page recommendation memo with an explicit cost / cycle-time / service-level trade-off table
- [x] 12 passing tests (schema reconciliation, model behaviour, reproducibility, lever sanity checks)

## Key numbers
- Parts & dispatch: **53%** of process time, **100% waiting** · top 3 stages = **90%**
- Brief's drivers R²=**0.04** vs +dispatch-path R²=**0.72** (dispatched +578%)
- Parts buffer **−23%** · +1 Field FTE **−8%** · both **−29%** · reroute Tier-1 **no measurable effect**

## Run
```bash
python -m src.process.stage_generator   # replay Week 7 tickets -> stage events (+ reconciliation)
python -m src.process.cycle_time        # decomposition, Pareto, control chart
python -m src.process.drivers           # regression + CIs + recovery validation
python -m src.process.capacity_sim      # 5 scenarios x 8 replications
python -m src.process.build_report      # scenario chart + 3-page memo
python -m pytest src/process/tests -q
```
Set `WEEK7_DB=/path/to/ingen_warehouse.duckdb` if the Week 7 warehouse lives elsewhere.

## Next (Week 13)
- Capstone synthesis: 20–25 page report, 15-slide exec deck, dashboard pack, HANDOFF.md.
