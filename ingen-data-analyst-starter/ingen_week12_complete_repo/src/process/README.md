# src/process — Support-Ticket Lifecycle Optimisation (Week 12)

Diagnoses where fleet-support cycle time goes and quantifies what operational changes would buy,
on the Week 7 synthetic warehouse.

## Run
```bash
pip install -r requirements.txt
export WEEK7_DB=/path/to/week07/ingen_warehouse.duckdb   # optional; defaults to the sibling repo
python -m src.process.stage_generator   # replay Week 7 tickets through the lifecycle (+ reconcile)
python -m src.process.cycle_time        # decomposition, Pareto, control chart
python -m src.process.drivers           # regression with CIs + generating-parameter recovery check
python -m src.process.capacity_sim      # 5 scenarios x 8 replications, paired deltas
python -m src.process.build_report      # scenario chart + 3-page memo
python -m pytest src/process/tests -q   # 12 tests
```

## Modules
| File | Role |
|---|---|
| `process_model.py` | the simpy DES: stages, teams, routing, service/parts distributions, levers |
| `stage_generator.py` | replays Week 7's ticket stream -> stage events; reconciliation checks |
| `cycle_time.py` | stage decomposition, Pareto, wait-vs-service, control chart |
| `drivers.py` | log-cycle regression with 95% CIs; validates against known generating params |
| `capacity_sim.py` | scenario runner with replications + paired delta CIs |
| `build_report.py` | scenario chart + 3-page recommendation memo |

## Findings in one line
Parts & dispatch is 53% of process time and 100% unstaffed waiting — so a regional parts buffer
(−23%) beats hiring a Field engineer (−8%), and rerouting Tier-1 triage (4% of process time) does
nothing measurable.
