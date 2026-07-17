# Data Dictionary — Week 12

## Inputs
Week 7 synthetic warehouse (`fact_support_tickets` + `dim_date` / `dim_product` / `dim_geography`).
Path via `WEEK7_DB` env var. **The Week 7 ticket stream is used unchanged** — ticket_id, opened date,
severity, category, product and geography all come from Week 7.

## Generated (Week 12 extension — documented model, not observed data)
| File | Schema |
|---|---|
| fact_ticket_stage_events.csv | ticket_key, ticket_id, stage, team, enter_h, start_h, exit_h, wait_hours, service_hours, queue_len_on_entry, stage_hours |
| ticket_cycle_times.csv | ticket_key, cycle_time_hours, ticket_id, severity, category, opened_date, product, region, country, week7_resolution_hours, is_resolved, weekday, dispatched, tier1_queue_on_entry |
| stage_decomposition.csv | stage, tickets, total_hours, wait_hours, service_hours, mean/median/p90_hours, pct_of_total, wait_share_of_stage, cumulative_pct |
| control_chart_weekly.csv | opened_date (week), mean_cycle_hours, tickets, ucl, lcl, center, out_of_control |
| driver_effects.csv | model, term, coef_log, ci_low_log, ci_high_log, p_value, effect_pct, ci_low_pct, ci_high_pct, significant_5pct |
| driver_recovery_check.csv | driver, generating_param, expected_direction, estimated_effect_pct, estimated_direction, significant, direction_recovered |
| capacity_sim_runs.csv | scenario, seed, mean/median/p90_cycle_hours, mean_field_wait_hours, tickets |
| capacity_sim_summary.csv | scenario, mean, ci_low, ci_high, p90_cycle_hours, mean_field_wait_hours, delta_hours_vs_base, delta_pct_vs_base |
| capacity_sim_paired_deltas.csv | scenario, paired_delta_hours, ci_low, ci_high, paired_delta_pct, significant_95 |

## Process stages
Intake → Triage (Tier 1) → Remote diagnosis (Tier 2) → [Parts & dispatch (unstaffed wait) → On-site repair (Field Ops)] → Verification (Tier 1).
The bracketed path runs only when a part/site visit is needed (37% of tickets).

## Documented model parameters (src/process/process_model.py)
- Teams (baseline): Tier 1 = 1, Tier 2 = 2, Field Ops = 1 FTE — chosen to load teams realistically vs ~6.8 tickets/day.
- Service medians (h): Triage 0.5, Remote diagnosis 3.0, On-site repair 4.0, Verification 1.0 (lognormal).
- Parts lead time: lognormal median 20h; region multiplier NA 1.0 / EU 1.25 / APAC 1.5; parts buffer x0.35.
- Dispatch probability by category: mechanical .75, battery .60, navigation .35, connectivity .15, software .05.
- Severity: queue priority (Critical first) + service multiplier (Critical .55, High .8, Medium 1.0, Low 1.15).
- Product repair multiplier: Aido Humanoid 1.5, Aido Rover 1.35, Sentinel 1.1, Fari 1.0, Senpai 0.85.
- SEED = 20260710.

## Reconciliation guarantees (tested)
- Every generated ticket_key exists in Week 7's fact_support_tickets (1:1, no orphans).
- Per ticket, sum(wait_hours + service_hours) across stages == cycle_time_hours exactly.
- severity/category on generated rows match Week 7 exactly.

## Honesty
The stage layer is **generated**, not observed — Week 7 carries no stage/team/workload fields. All findings
are properties of the documented model. `week7_resolution_hours` is retained for reference but is NOT the
Week 12 cycle time: Week 7 modelled no queueing, Week 12 adds it.
