"""Week 8 — dashboard PROTOTYPES (high-fidelity mockups from REAL data).

These are static prototypes that show exactly what each dashboard should look like when
rebuilt in Tableau Public / Looker Studio. They are rendered from the actual Week 4-7 data
extracts (data/week08/extracts/). They are NOT screenshots of a live Tableau/Looker dashboard
— publishing to those platforms is a manual step done in the user's own accounts.

Palette: Okabe-Ito (color-blind safe). Run: python -m src.dashboards.build_prototypes
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

ROOT = Path(__file__).resolve().parents[2]
EX = ROOT / "data" / "week08" / "extracts"
RPT = ROOT / "reports" / "week08"
RPT.mkdir(parents=True, exist_ok=True)

# Okabe-Ito color-blind-safe palette
OI = {"orange": "#E69F00", "sky": "#56B4E9", "green": "#009E73", "yellow": "#F0E442",
      "blue": "#0072B2", "vermillion": "#D55E00", "purple": "#CC79A7", "grey": "#7F7F7F"}
NAVY = "#1F3864"; INK = "#222A4A"; PANEL = "#FFFFFF"; CANVAS = "#EEF1F7"
PROD_ORDER = ["Sentinel Prime AI", "Fari", "Senpai", "Aido Rover", "Aido Humanoid"]
PROD_COLOR = {"Sentinel Prime AI": OI["blue"], "Fari": OI["green"], "Senpai": OI["orange"],
              "Aido Rover": OI["vermillion"], "Aido Humanoid": OI["purple"]}
SHORT = {"Sentinel Prime AI": "Sentinel", "Fari": "Fari", "Senpai": "Senpai",
         "Aido Rover": "Aido Rover", "Aido Humanoid": "Aido Hum."}


def _chrome(fig, title, subtitle, filters):
    """Draw dashboard title bar + filter chips to make the mockup read like a real dashboard."""
    fig.patch.set_facecolor(CANVAS)
    fig.text(0.012, 0.965, title, fontsize=19, fontweight="bold", color=NAVY, va="top")
    fig.text(0.012, 0.927, subtitle, fontsize=10.5, color="#5A6175", va="top", style="italic")
    # filter chips top-right
    x = 0.99
    for f in reversed(filters):
        w = 0.018 + len(f) * 0.0072
        fig.patches.append(plt.Rectangle((x - w, 0.928), w, 0.038, transform=fig.transFigure,
                                         facecolor="#DCE6F4", edgecolor="#9DB2DC", lw=0.8, zorder=2))
        fig.text(x - w / 2, 0.947, f, fontsize=8.5, color=NAVY, ha="center", va="center", zorder=3)
        x -= (w + 0.012)
    fig.text(0.012, 0.012, "PROTOTYPE — rendered from real Week 4-7 data; rebuild in the BI tool to publish.",
             fontsize=8, color="#8A93AB", style="italic")


def _panel_title(ax, t):
    ax.set_title(t, fontsize=11, fontweight="bold", color=INK, loc="left", pad=6)


def market_competitive():
    demand = pd.read_csv(EX / "demand_index.csv")
    pub = pd.read_csv(EX / "peer_public_financials.csv")
    priv = pd.read_csv(EX / "peer_private_funding.csv")
    market = pd.read_csv(EX / "market_sizing_summary.csv")

    fig = plt.figure(figsize=(13.4, 7.55), dpi=150)
    gs = GridSpec(2, 2, figure=fig, left=0.085, right=0.975, top=0.88, bottom=0.07,
                  hspace=0.42, wspace=0.2)

    # Panel 1: demand-signal index (ranked bar)
    ax = fig.add_subplot(gs[0, 0]); ax.set_facecolor(PANEL)
    d = demand.sort_values("demand_index")
    ax.barh([SHORT.get(p,p) for p in d["product"]], d["demand_index"], color=[PROD_COLOR.get(p, OI["grey"]) for p in d["product"]])
    for y, v in enumerate(d["demand_index"]):
        ax.text(v + 1, y, f"{v:.0f}", va="center", fontsize=8.5, color=INK)
    ax.set_xlim(0, 100); _panel_title(ax, "Demand-signal index (relative, Week 5)")
    ax.tick_params(labelsize=8.5); ax.spines[["top", "right"]].set_visible(False)

    # Panel 2: market attractiveness (Week 4 ranking) as a labeled table-ish bar
    ax = fig.add_subplot(gs[0, 1]); ax.set_facecolor(PANEL); ax.axis("off")
    _panel_title(ax, "Near-term market attractiveness (Week 4)")
    rank_map = {"Highest": 5, "Medium-High": 4, "Medium": 3, "Scenario range": 2}
    m = market.copy(); m["score"] = m["near_term_attractiveness"].map(rank_map).fillna(2)
    m = m.sort_values("score")
    yv = range(len(m))
    axb = ax.inset_axes([0.0, 0.0, 1.0, 0.86])
    axb.barh(list(yv), m["score"], color=[PROD_COLOR.get(p, OI["grey"]) for p in m["product"]])
    axb.set_yticks(list(yv)); axb.set_yticklabels([SHORT.get(p,p) for p in m["product"]], fontsize=8.5)
    axb.set_xticks([])
    for y, (lab) in zip(yv, m["near_term_attractiveness"]):
        axb.text(0.08, y, lab, va="center", fontsize=8, color="white", fontweight="bold")
    axb.spines[["top", "right", "bottom"]].set_visible(False)

    # Panel 3: public peer gross margin vs R&D intensity (scatter)
    ax = fig.add_subplot(gs[1, 0]); ax.set_facecolor(PANEL)
    ax.scatter(pub["gross_margin"] * 100, pub["rnd_pct"] * 100, s=120,
               color=[OI["blue"], OI["green"], OI["orange"], OI["vermillion"]][:len(pub)], zorder=3)
    for _, r in pub.iterrows():
        ax.annotate(r["name"], (r["gross_margin"] * 100, r["rnd_pct"] * 100),
                    fontsize=8, xytext=(5, 4), textcoords="offset points")
    ax.set_xlabel("Gross margin (%)", fontsize=8.5); ax.set_ylabel("R&D intensity (%)", fontsize=8.5)
    _panel_title(ax, "Public peers — margin vs R&D (Week 6)")
    ax.tick_params(labelsize=8); ax.grid(alpha=0.25); ax.spines[["top", "right"]].set_visible(False)

    # Panel 4: private capital raised (bar)
    ax = fig.add_subplot(gs[1, 1]); ax.set_facecolor(PANEL)
    pr = priv.dropna(subset=["amount_musd"]).groupby("name")["amount_musd"].sum().sort_values()
    ax.barh(pr.index, pr.values, color=OI["purple"])
    for y, v in enumerate(pr.values):
        ax.text(v + 15, y, f"${v:,.0f}M", va="center", fontsize=8, color=INK)
    ax.set_xlim(0, pr.values.max() * 1.25)
    _panel_title(ax, "Private peers — capital raised (Week 6)")
    ax.tick_params(labelsize=8.5); ax.spines[["top", "right"]].set_visible(False)

    _chrome(fig, "InGen — Market & Competitive", "Market sizing + demand signals + peer benchmarks  ·  Tableau Public (5 tabs: Overview shown)",
            ["Vertical: All", "Wave: latest"])
    out = RPT / "prototype_market_competitive.png"
    fig.savefig(out, facecolor=CANVAS); plt.close()
    print(f"  prototype -> {out.relative_to(ROOT)}")


def product_analytics():
    fleet = pd.read_csv(EX / "fleet_health_daily.csv", parse_dates=["date"])
    support = pd.read_csv(EX / "support_performance.csv")
    pipe = pd.read_csv(EX / "sales_pipeline.csv")
    kpi = pd.read_csv(EX / "kpi_summary_by_product.csv")

    fig = plt.figure(figsize=(13.4, 7.55), dpi=150)
    gs = GridSpec(2, 3, figure=fig, left=0.05, right=0.975, top=0.81, bottom=0.07,
                  hspace=0.45, wspace=0.28, height_ratios=[1, 1])

    # KPI scorecard row (as text callouts in a band)
    band = fig.add_axes([0.05, 0.835, 0.925, 0.06]); band.axis("off")
    tot_robots = int(kpi["robots"].sum()); avg_up = kpi["avg_uptime_hours"].mean()
    tickets = int(kpi["tickets"].sum()); csat = kpi["avg_csat"].mean()
    won = kpi["won_value"].sum()
    cards = [("Active robots", f"{tot_robots}"), ("Avg uptime/day", f"{avg_up:.1f} h"),
             ("Tickets", f"{tickets:,}"), ("Avg CSAT", f"{csat:.2f}/5"), ("Won value", f"${won/1e6:.0f}M")]
    for i, (lab, val) in enumerate(cards):
        x = 0.0 + i * 0.205
        band.text(x, 0.75, val, fontsize=17, fontweight="bold", color=NAVY, transform=band.transAxes)
        band.text(x, 0.15, lab, fontsize=8.5, color="#5A6175", transform=band.transAxes)

    # Panel 1: fleet uptime trend (monthly avg by product)
    ax = fig.add_subplot(gs[0, 0]); ax.set_facecolor(PANEL)
    fleet["ym"] = fleet["date"].dt.to_period("M").dt.to_timestamp()
    for prod in PROD_ORDER:
        s = fleet[fleet["product"] == prod].groupby("ym")["avg_uptime_hours"].mean()
        if len(s):
            ax.plot(s.index, s.values, color=PROD_COLOR[prod], lw=1.6, label=prod)
    _panel_title(ax, "Fleet uptime trend (avg h/day)")
    ax.tick_params(labelsize=7.5); ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=6.2, ncol=1, loc="lower left", framealpha=0.8)

    # Panel 2: errors by product (bar)
    ax = fig.add_subplot(gs[0, 1]); ax.set_facecolor(PANEL)
    e = fleet.groupby("product")["errors"].sum().reindex(PROD_ORDER)
    ax.bar(range(len(e)), e.values, color=[PROD_COLOR[p] for p in e.index])
    ax.set_xticks(range(len(e))); ax.set_xticklabels([SHORT[p] for p in e.index], fontsize=7, rotation=15)
    _panel_title(ax, "Total fleet errors by product")
    ax.tick_params(labelsize=7.5); ax.spines[["top", "right"]].set_visible(False)

    # Panel 3: ticket resolution hours by severity
    ax = fig.add_subplot(gs[0, 2]); ax.set_facecolor(PANEL)
    sev_order = ["Critical", "High", "Medium", "Low"]
    sv = support.groupby("severity").apply(
        lambda g: (g["avg_resolution_hours"] * g["tickets"]).sum() / g["tickets"].sum()).reindex(sev_order)
    ax.bar(range(len(sv)), sv.values, color=[OI["vermillion"], OI["orange"], OI["sky"], OI["green"]])
    ax.set_xticks(range(len(sv))); ax.set_xticklabels(sev_order, fontsize=8)
    _panel_title(ax, "Avg resolution hours by severity")
    ax.tick_params(labelsize=7.5); ax.spines[["top", "right"]].set_visible(False)

    # Panel 4: monthly won value (area)
    ax = fig.add_subplot(gs[1, 0]); ax.set_facecolor(PANEL)
    pm = pipe.groupby(["year", "month"])["won_value"].sum().reset_index()
    pm["t"] = pd.to_datetime(dict(year=pm.year, month=pm.month, day=1))
    pm = pm.sort_values("t")
    ax.fill_between(pm["t"], pm["won_value"] / 1e6, color=OI["blue"], alpha=0.35)
    ax.plot(pm["t"], pm["won_value"] / 1e6, color=OI["blue"], lw=1.6)
    _panel_title(ax, "Won value by month ($M)")
    ax.tick_params(labelsize=7.5); ax.spines[["top", "right"]].set_visible(False)

    # Panel 5: win rate by product
    ax = fig.add_subplot(gs[1, 1]); ax.set_facecolor(PANEL)
    w = kpi.set_index("product")["win_rate_pct"].reindex(PROD_ORDER)
    ax.barh(range(len(w)), w.values, color=[PROD_COLOR[p] for p in w.index])
    ax.set_yticks(range(len(w))); ax.set_yticklabels([SHORT[p] for p in w.index], fontsize=7.5)
    for y, v in enumerate(w.values):
        ax.text(v + 0.5, y, f"{v:.0f}%", va="center", fontsize=7.5, color=INK)
    ax.set_xlim(0, max(w.values) * 1.2)
    _panel_title(ax, "Win rate by product (%)")
    ax.tick_params(labelsize=7.5); ax.spines[["top", "right"]].set_visible(False)

    # Panel 6: avg CSAT by product
    ax = fig.add_subplot(gs[1, 2]); ax.set_facecolor(PANEL)
    c = kpi.set_index("product")["avg_csat"].reindex(PROD_ORDER)
    ax.bar(range(len(c)), c.values, color=[PROD_COLOR[p] for p in c.index])
    ax.set_xticks(range(len(c))); ax.set_xticklabels([SHORT[p] for p in c.index], fontsize=7, rotation=15)
    ax.set_ylim(3.5, 4.0)
    _panel_title(ax, "Avg CSAT by product (1-5)")
    ax.tick_params(labelsize=7.5); ax.spines[["top", "right"]].set_visible(False)

    _chrome(fig, "InGen — Simulated Product Analytics", "Fleet health · support performance · sales pipeline  ·  Looker Studio (date-range + product filters)",
            ["Date: last 24 mo", "Product: All"])
    out = RPT / "prototype_product_analytics.png"
    fig.savefig(out, facecolor=CANVAS); plt.close()
    print(f"  prototype -> {out.relative_to(ROOT)}")


def main():
    market_competitive()
    product_analytics()


if __name__ == "__main__":
    main()
