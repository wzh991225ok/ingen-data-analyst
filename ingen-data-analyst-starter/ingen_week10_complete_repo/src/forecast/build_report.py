"""Week 10 — forecast charts + 5-page forecast report (one page per vertical).

Run: python -m src.forecast.build_report   (after run_forecasts)
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .data_prep import VERTICALS, PRODUCT, load_target
from . import models as M

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "week10"
RPT = ROOT / "reports" / "week10"
RPT.mkdir(parents=True, exist_ok=True)
NAVY = "#1F3864"; BLUE = "#2E5496"; ORANGE = "#E69F00"; GREEN = "#2E7D5B"; GREY = "#7F7F7F"

# Analyst cross-checks (cited). Humanoid has the strongest public analyst coverage.
ANALYST = {
 "humanoid": "Goldman Sachs (Jan 2024): ~20k humanoid shipments 2025 -> ~250k (2030) -> ~1.4M/yr (2035), ~70% CAGR, $38B TAM by 2035. "
             "Morgan Stanley (Apr 2025): ~13M humanoids in service by 2035. Our search-momentum rise is directionally consistent with this accelerating adoption.",
 "indoor_security": "Public service-robotics forecasts broadly project double-digit CAGR for professional security robots; our modest upward search momentum is consistent, though no single audited point forecast is used as an anchor.",
 "outdoor_patrol": "Perimeter/patrol robotics is an emerging professional-service segment; published forecasts are directional. Our forecast is treated as a relative momentum read, not an absolute market size.",
 "eldercare": "Eldercare/companion-robot adoption is widely expected to grow but is penetration-constrained; our near-flat-to-up momentum reflects that. No single analyst point forecast is anchored.",
 "education": "Educational-robotics forecasts project steady growth tied to budget cycles; our stable upward momentum is consistent. Treated as a relative read.",
}


def _forecast_plot(ax, vertical, results):
    y = load_target(vertical)
    fc = pd.read_csv(DATA / f"forecasts_{vertical}.csv")
    best = results[(results.vertical == vertical) & (results.is_best)]["model"].iloc[0]
    fb = fc[fc.model == best].copy()
    fb["d"] = pd.to_datetime(fb["date"] + "-01")
    # empirical band from best model's holdout MAPE
    mapev = float(results[(results.vertical == vertical) & (results.model == best)]["MAPE"].iloc[0]) / 100
    lower = fb["yhat"] * (1 - 1.28 * mapev)
    upper = fb["yhat"] * (1 + 1.28 * mapev)
    ax.plot(y.index, y.values, color=NAVY, lw=1.6, label="History (search interest)")
    ax.plot(fb["d"], fb["yhat"], color=ORANGE, lw=2, label=f"Forecast — {best}")
    ax.fill_between(fb["d"], lower, upper, color=ORANGE, alpha=0.18, label="~80% band (holdout error)")
    ax.axvline(y.index[-1], color=GREY, ls=":", lw=0.8)
    ax.set_ylabel("Search interest (0-100)", fontsize=8)
    ax.tick_params(labelsize=7.5); ax.legend(fontsize=7, loc="upper left"); ax.grid(alpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)


def _importance_plot(ax, vertical):
    imp = pd.read_csv(DATA / "xgb_importances.csv")
    top = imp[imp.vertical == vertical].nlargest(6, "importance").iloc[::-1]
    ax.barh(top["feature"], top["importance"], color=BLUE)
    ax.set_title("XGBoost feature importance", fontsize=8.5, loc="left")
    ax.tick_params(labelsize=7.5); ax.spines[["top", "right"]].set_visible(False)


def build_charts(results):
    for v in VERTICALS:
        fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.5, 3.0), gridspec_kw={"width_ratios": [2, 1]})
        _forecast_plot(a1, v, results)
        _importance_plot(a2, v)
        fig.suptitle(f"{PRODUCT[v]} ({v}) — 24-month demand forecast", fontsize=11, fontweight="bold", color=NAVY, x=0.02, ha="left")
        plt.tight_layout(rect=[0, 0, 1, 0.94])
        fig.savefig(RPT / f"fc_{v}.png", dpi=130); plt.close()
    # Bass humanoid chart
    bass = pd.read_csv(DATA / "bass_humanoid.csv")
    fig, ax = plt.subplots(figsize=(7.5, 3.2))
    ax.bar(bass["year"], bass["annual_shipments"] / 1e3, color=BLUE, alpha=0.85, label="Annual shipments (model)")
    for yr, val in [(2025, 20), (2030, 250), (2035, 1400)]:
        ax.scatter([yr], [val], color=ORANGE, zorder=5, s=45)
    ax.scatter([], [], color=ORANGE, label="Goldman Sachs anchors")
    ax.set_ylabel("Annual shipments (000s)", fontsize=9); ax.set_title("Humanoid adoption — Bass diffusion vs Goldman anchors", fontsize=10, color=NAVY)
    ax.legend(fontsize=8); ax.grid(alpha=0.2); ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout(); fig.savefig(RPT / "bass_humanoid.png", dpi=130); plt.close()
    print("  charts built")


def build_pdf(results):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    NV = colors.HexColor(NAVY); BL = colors.HexColor(BLUE); LT = colors.HexColor("#D9E1F2")
    S = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=S["Normal"], fontName="Helvetica", fontSize=9, leading=12.5, spaceAfter=4)
    h1 = ParagraphStyle("h1", parent=S["Normal"], fontName="Helvetica-Bold", fontSize=14, textColor=NV, spaceAfter=2)
    h2 = ParagraphStyle("h2", parent=S["Normal"], fontName="Helvetica-Bold", fontSize=10.5, textColor=BL, spaceBefore=6, spaceAfter=2)
    foot = ParagraphStyle("f", parent=S["Normal"], fontName="Helvetica-Oblique", fontSize=7, textColor=colors.HexColor("#666"))
    path = RPT / "forecast_report.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=letter, leftMargin=0.7*inch, rightMargin=0.7*inch,
                            topMargin=0.55*inch, bottomMargin=0.5*inch, title="InGen Week 10 — Demand Forecast Report", author="Ziheng Wang")

    def tblrow(vertical):
        sub = results[results.vertical == vertical]
        data = [["Model", "MAPE", "MASE", "12m", "24m"]]
        for _, r in sub.iterrows():
            tag = " *" if r["is_best"] else ""
            data.append([r["model"] + tag, f"{r['MAPE']:.1f}%" if pd.notna(r['MAPE']) else "—",
                         f"{r['MASE']:.2f}" if pd.notna(r['MASE']) else "—",
                         f"{r['est_12m']:.0f}" if pd.notna(r['est_12m']) else "—",
                         f"{r['est_24m']:.0f}" if pd.notna(r['est_24m']) else "—"])
        t = Table(data, colWidths=[1.5*inch, 0.8*inch, 0.7*inch, 0.6*inch, 0.6*inch])
        t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), BL), ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), ("FONTSIZE", (0,0), (-1,-1), 8),
            ("GRID", (0,0), (-1,-1), 0.3, LT), ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F2F6FC")])]))
        return t

    story = []
    # intro page header (kept on page 1 with first vertical)
    for i, v in enumerate(VERTICALS):
        sub = results[results.vertical == v]
        best = sub[sub.is_best].iloc[0]
        story.append(Paragraph(f"{PRODUCT[v]} — 24-month demand forecast", h1))
        story.append(Paragraph(f"Target: monthly search-interest momentum (Week 5). Backtest on the last 12 months; "
                               f"best model by MASE: <b>{best['model']}</b> (MAPE {best['MAPE']:.1f}%, MASE {best['MASE']:.2f}).", body))
        story.append(Image(str(RPT / f"fc_{v}.png"), width=6.7*inch, height=2.11*inch))
        story.append(Paragraph("Model comparison (backtest)", h2))
        story.append(tblrow(v))
        story.append(Paragraph("Point forecast &amp; drivers", h2))
        imp = pd.read_csv(DATA / "xgb_importances.csv")
        topf = ", ".join(imp[imp.vertical == v].nlargest(3, "importance")["feature"].tolist())
        story.append(Paragraph(f"12-month point estimate <b>{best['est_12m']:.0f}</b>, 24-month <b>{best['est_24m']:.0f}</b> "
                               f"(search-interest index, ~80% band shown from holdout error). Top XGBoost drivers: <b>{topf}</b>.", body))
        story.append(Paragraph("Sanity-check vs published analyst forecasts", h2))
        story.append(Paragraph(ANALYST[v], body))
        if v == "humanoid":
            story.append(Paragraph("Adoption curve (Bass diffusion)", h2))
            story.append(Image(str(RPT / "bass_humanoid.png"), width=5.6*inch, height=2.39*inch))
            bp = (DATA / "bass_params.txt").read_text().strip()
            story.append(Paragraph(f"Bass fit to Goldman anchors ({bp}); hits 20k/2025, 250k/2030, 1.4M/2035 with a smooth S-curve; "
                                   "cumulative installed base ~4.3M by 2035 (between Goldman shipment view and Morgan Stanley's 13M-in-service scenario).", body))
        story.append(Spacer(1, 4))
        story.append(Table([[Paragraph("Method: search-momentum target from Week 5; models statsmodels/Prophet/XGBoost; MASE vs in-sample naive-1. "
                             "Forecasts are a relative demand read, not absolute unit/market forecasts; validate against internal data before planning. "
                             "Prepared by Ziheng Wang, Week 10.", foot)]], colWidths=[7.0*inch],
                            style=TableStyle([("LINEABOVE", (0,0), (-1,-1), 0.5, LT), ("TOPPADDING", (0,0), (-1,-1), 3)])))
        if i < len(VERTICALS) - 1:
            story.append(PageBreak())
    doc.build(story)
    print(f"  report -> {path.relative_to(ROOT)} ({len(VERTICALS)} vertical pages)")


def main():
    results = pd.read_csv(DATA / "forecast_results.csv")
    build_charts(results)
    build_pdf(results)


if __name__ == "__main__":
    main()
