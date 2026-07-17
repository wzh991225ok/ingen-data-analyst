"""Week 12 — capacity simulation: quantify what each operational change would actually buy.

Re-runs the same discrete-event process model with one lever changed at a time, across several
seeded replications, and reports the change in cycle time with a confidence interval — deltas, not
directional statements.

Scenarios
---------
  S0  Baseline                    Tier 1 = 1, Tier 2 = 2, Field Ops = 1
  S1  +1 Field Ops FTE            the queueing bottleneck named in the brief
  S2  Reroute low-severity        Low-severity tickets skip human triage (self-service/auto-route)
  S3  Regional parts buffer       local parts stock in Europe + APAC (cuts parts lead time)
  S4  S1 + S3 combined            do both

S3 is not in the brief's examples — the diagnostic put it there. Parts & dispatch is 53% of all
process time and is 100% unstaffed waiting, so no amount of headcount can touch it. Testing a lever
that the data points at is the whole reason for building the model.

Run: python -m src.process.capacity_sim
"""
from __future__ import annotations
from pathlib import Path

import numpy as np
import pandas as pd

from .process_model import SupportProcess, TEAMS_BASELINE, SEED
from .stage_generator import load_week7_tickets, EPOCH
from .process_model import Ticket

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "week12"
DATA.mkdir(parents=True, exist_ok=True)

N_REPLICATIONS = 8

SCENARIOS = {
    "S0 Baseline": dict(),
    "S1 +1 Field Ops FTE": dict(teams={**TEAMS_BASELINE, "Field Ops": TEAMS_BASELINE["Field Ops"] + 1}),
    "S2 Reroute low-severity triage": dict(reroute_low_severity=True),
    "S3 Regional parts buffer (EU+APAC)": dict(parts_buffer_regions=("Europe", "APAC")),
    "S4 +1 Field FTE + parts buffer": dict(teams={**TEAMS_BASELINE, "Field Ops": TEAMS_BASELINE["Field Ops"] + 1},
                                           parts_buffer_regions=("Europe", "APAC")),
}


def _make_tickets(tickets_df, seed):
    rng = np.random.default_rng(seed)
    offsets = rng.uniform(0, 24, len(tickets_df))
    arrival_h = ((pd.to_datetime(tickets_df["opened_date"]) - EPOCH).dt.total_seconds() / 3600.0
                 + offsets).to_numpy()
    return [Ticket(ticket_key=int(r.ticket_key), ticket_id=r.ticket_id, arrival_h=float(a),
                   severity=r.severity, category=r.category, product=r.product, region=r.region)
            for r, a in zip(tickets_df.itertuples(index=False), arrival_h)]


def run_scenario(tickets_df, name, cfg, seed):
    tickets = _make_tickets(tickets_df, seed)
    rows = SupportProcess(tickets, seed=seed, **cfg).run()
    ev = pd.DataFrame(rows)
    ev["stage_hours"] = ev["wait_hours"] + ev["service_hours"]
    cyc = ev.groupby("ticket_key")["stage_hours"].sum()
    field_wait = ev.loc[ev["stage"] == "On-site repair", "wait_hours"]
    return {"scenario": name, "seed": seed,
            "mean_cycle_hours": float(cyc.mean()),
            "median_cycle_hours": float(cyc.median()),
            "p90_cycle_hours": float(cyc.quantile(0.90)),
            "mean_field_wait_hours": float(field_wait.mean()) if len(field_wait) else 0.0,
            "tickets": int(cyc.shape[0])}


def main(n_reps: int = N_REPLICATIONS):
    tickets_df = load_week7_tickets()
    raw = []
    for name, cfg in SCENARIOS.items():
        for i in range(n_reps):
            raw.append(run_scenario(tickets_df, name, cfg, seed=SEED + i))
        print(f"  ran {name} x{n_reps}")
    df = pd.DataFrame(raw)
    df.to_csv(DATA / "capacity_sim_runs.csv", index=False)

    # summarise with 95% CI on the mean across replications
    def ci(s):
        m, sd, n = s.mean(), s.std(ddof=1), len(s)
        half = 1.96 * sd / np.sqrt(n) if n > 1 else 0.0
        return pd.Series({"mean": m, "ci_low": m - half, "ci_high": m + half})

    summ = df.groupby("scenario")["mean_cycle_hours"].apply(ci).unstack().reset_index()
    p90 = df.groupby("scenario")["p90_cycle_hours"].mean().rename("p90_cycle_hours").reset_index()
    fw = df.groupby("scenario")["mean_field_wait_hours"].mean().rename("mean_field_wait_hours").reset_index()
    summ = summ.merge(p90, on="scenario").merge(fw, on="scenario")

    base = summ[summ["scenario"] == "S0 Baseline"].iloc[0]
    summ["delta_hours_vs_base"] = (summ["mean"] - base["mean"]).round(3)
    summ["delta_pct_vs_base"] = ((summ["mean"] / base["mean"] - 1) * 100).round(2)

    # paired delta CI (same seeds across scenarios -> paired comparison is tighter and correct)
    pivot = df.pivot_table(index="seed", columns="scenario", values="mean_cycle_hours")
    prows = []
    for name in SCENARIOS:
        if name == "S0 Baseline":
            continue
        d = pivot[name] - pivot["S0 Baseline"]
        m, sd, n = d.mean(), d.std(ddof=1), len(d)
        half = 1.96 * sd / np.sqrt(n) if n > 1 else 0.0
        prows.append({"scenario": name, "paired_delta_hours": round(m, 3),
                      "ci_low": round(m - half, 3), "ci_high": round(m + half, 3),
                      "paired_delta_pct": round(m / pivot["S0 Baseline"].mean() * 100, 2),
                      "significant_95": bool((m - half) * (m + half) > 0)})
    paired = pd.DataFrame(prows)
    summ.round(3).to_csv(DATA / "capacity_sim_summary.csv", index=False)
    paired.to_csv(DATA / "capacity_sim_paired_deltas.csv", index=False)

    print("\n=== Scenario results (mean cycle time across replications) ===")
    print(summ[["scenario", "mean", "ci_low", "ci_high", "p90_cycle_hours",
                "mean_field_wait_hours", "delta_pct_vs_base"]].round(2).to_string(index=False))
    print("\n=== Paired deltas vs baseline (same seeds; 95% CI) ===")
    print(paired.to_string(index=False))
    return summ, paired


if __name__ == "__main__":
    main()
