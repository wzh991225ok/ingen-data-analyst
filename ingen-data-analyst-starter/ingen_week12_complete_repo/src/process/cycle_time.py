"""Week 12 — cycle-time decomposition, Pareto and control charts.

Answers: where does the time actually go, which stages drive the delay, and is the process
in statistical control or is something drifting?

Run: python -m src.process.cycle_time
"""
from __future__ import annotations
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "week12"
RPT = ROOT / "reports" / "week12"
RPT.mkdir(parents=True, exist_ok=True)

NAVY = "#1F3864"; BLUE = "#2E5496"; ORANGE = "#E69F00"; RED = "#C0392B"; GREEN = "#2E7D5B"
GREY = "#7F7F7F"
STAGE_ORDER = ["Intake", "Triage", "Remote diagnosis", "Parts & dispatch", "On-site repair", "Verification"]


def load():
    ev = pd.read_csv(DATA / "fact_ticket_stage_events.csv")
    cycle = pd.read_csv(DATA / "ticket_cycle_times.csv", parse_dates=["opened_date"])
    return ev, cycle


def decompose(ev: pd.DataFrame) -> pd.DataFrame:
    """Total hours per stage, split into waiting vs staffed service — the split that decides
    whether a fix is headcount (service/queue) or logistics (unstaffed wait)."""
    g = ev.groupby("stage").agg(
        tickets=("ticket_key", "nunique"),
        total_hours=("stage_hours", "sum"),
        wait_hours=("wait_hours", "sum"),
        service_hours=("service_hours", "sum"),
        mean_hours=("stage_hours", "mean"),
        median_hours=("stage_hours", "median"),
        p90_hours=("stage_hours", lambda s: s.quantile(0.90)),
    ).reset_index()
    total = g["total_hours"].sum()
    g["pct_of_total"] = (g["total_hours"] / total * 100).round(2)
    g["wait_share_of_stage"] = (g["wait_hours"] / g["total_hours"].replace(0, np.nan) * 100).round(1)
    g = g.sort_values("total_hours", ascending=False).reset_index(drop=True)
    g["cumulative_pct"] = g["pct_of_total"].cumsum().round(2)
    return g


def chart_pareto(dec: pd.DataFrame):
    d = dec[dec["total_hours"] > 0].copy()
    fig, ax = plt.subplots(figsize=(9, 4.2))
    x = np.arange(len(d))
    ax.bar(x, d["total_hours"] / 1000, color=BLUE, label="Total hours in stage (000s)")
    ax.set_xticks(x); ax.set_xticklabels(d["stage"], rotation=18, ha="right", fontsize=9)
    ax.set_ylabel("Total hours across all tickets (000s)", fontsize=9, color=BLUE)
    ax.tick_params(axis="y", labelcolor=BLUE)
    ax2 = ax.twinx()
    ax2.plot(x, d["cumulative_pct"], "o-", color=ORANGE, lw=2, label="Cumulative %")
    ax2.axhline(80, color=RED, ls="--", lw=1, label="80% line")
    ax2.set_ylabel("Cumulative % of total process time", fontsize=9, color=ORANGE)
    ax2.tick_params(axis="y", labelcolor=ORANGE); ax2.set_ylim(0, 105)
    for xi, (pct, cum) in enumerate(zip(d["pct_of_total"], d["cumulative_pct"])):
        ax2.annotate(f"{cum:.0f}%", (xi, cum), fontsize=8, xytext=(4, -12), textcoords="offset points", color=ORANGE)
        ax.annotate(f"{pct:.0f}%", (xi, d['total_hours'].iloc[xi] / 1000), fontsize=8.5,
                    ha="center", xytext=(0, 3), textcoords="offset points", color=NAVY)
    ax.set_title("Pareto — where support cycle time actually goes", fontsize=11.5, color=NAVY, fontweight="bold")
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=8, loc="center right")
    ax.spines[["top"]].set_visible(False); ax2.spines[["top"]].set_visible(False)
    plt.tight_layout(); fig.savefig(RPT / "pareto_stages.png", dpi=135); plt.close()


def chart_wait_vs_service(dec: pd.DataFrame):
    """The chart that decides the recommendation: queueing (fixable with people) vs unstaffed wait."""
    d = dec[dec["total_hours"] > 0].sort_values("total_hours")
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.barh(d["stage"], d["wait_hours"] / 1000, color=ORANGE, label="Waiting (queue or parts)")
    ax.barh(d["stage"], d["service_hours"] / 1000, left=d["wait_hours"] / 1000, color=BLUE,
            label="Staffed work")
    for i, (_, r) in enumerate(d.iterrows()):
        if r["total_hours"] > 0:
            ax.text(r["total_hours"] / 1000 + 0.8, i, f"{r['wait_share_of_stage']:.0f}% waiting",
                    va="center", fontsize=8, color=GREY)
    ax.set_xlabel("Total hours across all tickets (000s)", fontsize=9)
    ax.set_title("Waiting vs staffed work — headcount only fixes the blue part",
                 fontsize=11.5, color=NAVY, fontweight="bold")
    ax.legend(fontsize=8.5, loc="lower right"); ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout(); fig.savefig(RPT / "wait_vs_service.png", dpi=135); plt.close()


def control_chart(cycle: pd.DataFrame, stage_ev: pd.DataFrame):
    """Weekly X-bar chart of mean cycle time with 3-sigma limits.

    Limits are computed from the observed weekly means (mean +/- 3 * sigma of the weekly means),
    the standard individuals-chart convention when subgroup sizes vary.
    """
    w = (cycle.set_index("opened_date")["cycle_time_hours"].resample("W").agg(["mean", "count"])
         .dropna().rename(columns={"mean": "mean_cycle_hours", "count": "tickets"}))
    mu = w["mean_cycle_hours"].mean(); sd = w["mean_cycle_hours"].std()
    ucl, lcl = mu + 3 * sd, max(0, mu - 3 * sd)
    w["ucl"] = ucl; w["lcl"] = lcl; w["center"] = mu
    w["out_of_control"] = (w["mean_cycle_hours"] > ucl) | (w["mean_cycle_hours"] < lcl)
    w.reset_index().to_csv(DATA / "control_chart_weekly.csv", index=False)

    fig, ax = plt.subplots(figsize=(10, 3.8))
    ax.plot(w.index, w["mean_cycle_hours"], "o-", color=BLUE, ms=3, lw=1.2, label="Weekly mean cycle time")
    ax.axhline(mu, color=GREEN, lw=1.4, label=f"Centre line ({mu:.1f}h)")
    ax.axhline(ucl, color=RED, ls="--", lw=1.2, label=f"UCL/LCL (3σ)")
    ax.axhline(lcl, color=RED, ls="--", lw=1.2)
    oc = w[w["out_of_control"]]
    if len(oc):
        ax.scatter(oc.index, oc["mean_cycle_hours"], color=RED, zorder=5, s=45,
                   label=f"Out of control ({len(oc)} weeks)")
    ax.set_ylabel("Mean cycle time (h)", fontsize=9)
    ax.set_title("Control chart — weekly mean support cycle time", fontsize=11.5, color=NAVY, fontweight="bold")
    ax.legend(fontsize=8, loc="upper right"); ax.grid(alpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout(); fig.savefig(RPT / "control_chart.png", dpi=135); plt.close()
    return w


def main():
    ev, cycle = load()
    dec = decompose(ev)
    dec.to_csv(DATA / "stage_decomposition.csv", index=False)
    chart_pareto(dec); chart_wait_vs_service(dec)
    w = control_chart(cycle, ev)

    print("=== Stage decomposition (Pareto order) ===")
    print(dec[["stage", "total_hours", "pct_of_total", "cumulative_pct",
               "wait_share_of_stage", "median_hours", "p90_hours"]].round(1).to_string(index=False))
    top3 = dec.head(3)["stage"].tolist()
    print(f"\nTop 3 stages by contribution to delay: {', '.join(top3)} "
          f"({dec.head(3)['pct_of_total'].sum():.0f}% of all process time)")
    print(f"\n=== Control chart ===\nweeks={len(w)}  centre={w['center'].iloc[0]:.1f}h  "
          f"UCL={w['ucl'].iloc[0]:.1f}h  out-of-control weeks={int(w['out_of_control'].sum())}")
    print(f"\nCharts -> {RPT.relative_to(ROOT)}/ (pareto_stages.png, wait_vs_service.png, control_chart.png)")
    return dec, w


if __name__ == "__main__":
    main()
