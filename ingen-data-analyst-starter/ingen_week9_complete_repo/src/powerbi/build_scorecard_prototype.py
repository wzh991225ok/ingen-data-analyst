"""Week 9 — Power BI executive scorecard PROTOTYPE (traffic-light KPIs) from real warehouse KPIs.

A high-fidelity mockup of the Power BI executive scorecard: RAG (red/amber/green) KPI tiles vs
targets, plus a small trend strip. Rendered from real Week 7 warehouse aggregates. This is the
build target for the .pbix (which is assembled in Power BI Desktop — see spec_powerbi.pdf).

Run: python -m src.powerbi.build_scorecard_prototype
"""
from __future__ import annotations
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
RPT = ROOT / "reports" / "week09"
K = json.load(open(RPT / "_exec_kpis.json"))

NAVY = "#1F3864"; INK = "#222A4A"; CANVAS = "#EEF1F7"
GREEN = "#2E7D5B"; AMBER = "#E69F00"; RED = "#C0392B"; GREY = "#7F7F7F"

# KPI tiles: (label, value, fmt, target_text, status, direction)
# status pre-computed from value vs target; direction notes higher/lower is better.
def rag(value, green, amber, higher=True):
    if higher:
        return GREEN if value >= green else (AMBER if value >= amber else RED)
    else:
        return GREEN if value <= green else (AMBER if value <= amber else RED)

TILES = [
    ("Fleet active rate", f"{K['active_rate']:.1f}%", "Target ≥ 95%", rag(K['active_rate'], 95, 90, True)),
    ("Avg uptime / day", f"{K['avg_uptime']:.1f} h", "Target ≥ 12 h", rag(K['avg_uptime'], 12, 9, True)),
    ("Critical resolution", f"{K['crit_res']:.1f} h", "Target ≤ 8 h", rag(K['crit_res'], 8, 12, False)),
    ("Ticket resolve rate", f"{K['resolve_rate']:.0f}%", "Target ≥ 90%", rag(K['resolve_rate'], 90, 80, True)),
    ("Avg CSAT", f"{K['csat']:.2f}/5", "Target ≥ 4.0", rag(K['csat'], 4.0, 3.5, True)),
    ("Win rate", f"{K['win_rate']:.0f}%", "Target ≥ 35%", rag(K['win_rate'], 35, 28, True)),
    ("Won value (TTM)", f"${K['won_value']/1e6:.0f}M", "Target ≥ $150M", rag(K['won_value']/1e6, 150, 100, True)),
    ("Avg sales cycle", f"{K['avg_cycle']:.0f} d", "Target ≤ 100 d", rag(K['avg_cycle'], 100, 130, False)),
]


def build():
    fig = plt.figure(figsize=(13.4, 7.55), dpi=150)
    fig.patch.set_facecolor(CANVAS)
    fig.text(0.012, 0.965, "InGen — Executive Scorecard", fontsize=19, fontweight="bold", color=NAVY, va="top")
    fig.text(0.012, 0.927, "Traffic-light KPIs vs target  ·  Power BI (drill-through to product detail)  ·  synthetic warehouse",
             fontsize=10.5, color="#5A6175", va="top", style="italic")
    # legend chips
    for i, (lab, col) in enumerate([("On target", GREEN), ("Watch", AMBER), ("Off target", RED)]):
        x = 0.74 + i * 0.087
        fig.patches.append(plt.Circle((x, 0.945), 0.009, transform=fig.transFigure, color=col, zorder=3))
        fig.text(x + 0.014, 0.945, lab, fontsize=8.5, color=INK, va="center")

    # 2 rows x 4 cols of KPI tiles
    cols, rows = 4, 2
    x0, y0, w, h, gx, gy = 0.02, 0.50, 0.225, 0.30, 0.015, 0.04
    for i, (label, value, target, status) in enumerate(TILES):
        r, c = divmod(i, cols)
        x = x0 + c * (w + gx)
        y = y0 - r * (h + gy)
        ax = fig.add_axes([x, y, w, h]); ax.axis("off")
        ax.add_patch(FancyBboxPatch((0.02, 0.04), 0.96, 0.92, boxstyle="round,pad=0.01,rounding_size=0.04",
                                    transform=ax.transAxes, facecolor="white", edgecolor="#E2E7F2", lw=1))
        # status dot
        ax.add_patch(plt.Circle((0.12, 0.80), 0.055, transform=ax.transAxes, color=status, zorder=4))
        ax.text(0.24, 0.78, label, fontsize=11, color=INK, fontweight="bold", transform=ax.transAxes, va="center")
        ax.text(0.5, 0.46, value, fontsize=30, color=status, fontweight="bold", ha="center", transform=ax.transAxes)
        ax.text(0.5, 0.16, target, fontsize=9, color="#6A6A7A", ha="center", transform=ax.transAxes)

    fig.text(0.012, 0.012, "PROTOTYPE — rendered from real Week 7 warehouse KPIs; build the .pbix in Power BI Desktop (see spec_powerbi.pdf).",
             fontsize=8, color="#8A93AB", style="italic")
    out = RPT / "prototype_powerbi_scorecard.png"
    fig.savefig(out, facecolor=CANVAS); plt.close()
    print(f"  prototype -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
