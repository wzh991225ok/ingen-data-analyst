"""Week 8 — dashboard SPEC PDFs (Market & Competitive; Product Analytics).

Each spec states the question the dashboard answers, the tabs/panels, data sources, filters,
chart types, and the success criteria from the plan. Run: python -m src.dashboards.build_specs
"""
from __future__ import annotations
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

ROOT = Path(__file__).resolve().parents[2]
RPT = ROOT / "reports" / "week08"
RPT.mkdir(parents=True, exist_ok=True)
NAVY = colors.HexColor("#1F3864"); BLUE = colors.HexColor("#2E5496"); LT = colors.HexColor("#D9E1F2")
S = getSampleStyleSheet()
body = ParagraphStyle("b", parent=S["Normal"], fontName="Helvetica", fontSize=9.5, leading=13.5, spaceAfter=5)
h1 = ParagraphStyle("h1", parent=S["Normal"], fontName="Helvetica-Bold", fontSize=16, textColor=NAVY, spaceAfter=3)
h2 = ParagraphStyle("h2", parent=S["Normal"], fontName="Helvetica-Bold", fontSize=11.5, textColor=BLUE, spaceBefore=9, spaceAfter=3)
foot = ParagraphStyle("f", parent=S["Normal"], fontName="Helvetica-Oblique", fontSize=7.5, textColor=colors.HexColor("#595959"))


def _tbl(data, widths):
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), BLUE), ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), ("FONTSIZE", (0,0), (-1,-1), 8.3),
        ("GRID", (0,0), (-1,-1), 0.3, LT), ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F2F6FC")]),
        ("TOPPADDING", (0,0), (-1,-1), 3), ("BOTTOMPADDING", (0,0), (-1,-1), 3)]))
    return t


def _doc(path, title):
    return SimpleDocTemplate(str(path), pagesize=letter, leftMargin=0.8*inch, rightMargin=0.8*inch,
                             topMargin=0.6*inch, bottomMargin=0.6*inch, title=title, author="Ziheng Wang")


def market_spec():
    path = RPT / "spec_market_competitive.pdf"
    st = [Paragraph("Dashboard Spec — Market &amp; Competitive (Tableau Public)", h1),
          Paragraph("Audience: InGen leadership + external stakeholders. Built from public data only.", body)]
    st.append(Paragraph("Question it answers", h2))
    st.append(Paragraph("<b>“Across our five verticals, which markets are biggest, which are heating up now, "
        "and how do we compare to peers?”</b> The Overview tab answers this on the first screen, no scrolling.", body))
    st.append(Paragraph("Tabs &amp; panels", h2))
    st.append(_tbl([
        ["Tab", "Panels", "Source"],
        ["Overview", "Demand-index ranking · market attractiveness · public-peer margin↔R&D · private capital raised", "Wk4-6"],
        ["Verticals", "Per-vertical: market size range, demand index, top customer pain points", "Wk4-5"],
        ["Peers", "Public financials table (rev, GM, R&D%, margins) + private funding rounds (sourced)", "Wk6"],
        ["Demand", "Search/news/sentiment trends; demand-index composition (stacked weights)", "Wk5"],
        ["Methodology", "Sources, metric definitions, weights, caveats (EV/Rev computed live)", "Wk4-6"],
    ], [0.9*inch, 4.6*inch, 0.7*inch]))
    st.append(Paragraph("Data sources (upload-ready extracts)", h2))
    st.append(Paragraph("data/week08/extracts/: demand_index.csv, demand_signals_long.csv, peer_public_financials.csv, "
        "peer_private_funding.csv, market_sizing_summary.csv. Numeric TAM/SAM/SOM link to Week 4 market_sizing_workbook.xlsx.", body))
    st.append(Paragraph("Filters &amp; interactions", h2))
    st.append(Paragraph("Global filters: <b>Vertical</b> (All/each) and <b>Wave</b> (latest/prior). Filters apply across "
        "all tabs; selecting a vertical cross-highlights its bar in every panel. No broken states (all panels share the vertical key).", body))
    st.append(Paragraph("Chart types (and why)", h2))
    st.append(Paragraph("Ranked horizontal bars for the index and attractiveness (easy comparison of ordered categories); "
        "scatter for margin↔R&D (two continuous measures); horizontal bars for capital raised. No pie charts.", body))
    st.append(Paragraph("Prototype", h2))
    img = RPT / "prototype_market_competitive.png"
    if img.exists():
        st.append(Image(str(img), width=6.0*inch, height=3.38*inch))
    st.append(Paragraph("Success criteria (from plan)", h2))
    st.append(Paragraph("Loads &lt;5s · answers its question on the first screen · color-blind-safe palette (Okabe-Ito) · "
        "filters update all charts coherently. Publishing produces the public Tableau URL (done in the user's account).", body))
    st.append(Spacer(1, 6))
    st.append(_tbl([["Note", "This spec + extracts make the Tableau build mechanical. The live URL is created by publishing "
        "to Tableau Public from the user's own account; it is not auto-generated here. Prototype above is rendered from the real data."]],
        [1.0*inch, 5.2*inch]))
    _doc(path, "Market & Competitive Dashboard Spec").build(st)
    print(f"  spec -> {path.relative_to(ROOT)}")


def product_spec():
    path = RPT / "spec_product_analytics.pdf"
    st = [Paragraph("Dashboard Spec — Simulated Product Analytics (Looker Studio)", h1),
          Paragraph("Audience: InGen product + ops + sales. Built on the Week 7 synthetic warehouse (no real InGen data).", body)]
    st.append(Paragraph("Question it answers", h2))
    st.append(Paragraph("<b>“How healthy is the fleet, how is support performing, and how is the sales pipeline tracking — "
        "by product line and over time?”</b> Answered on the first screen via a KPI band + six panels.", body))
    st.append(Paragraph("Layout &amp; panels", h2))
    st.append(_tbl([
        ["Section", "Panels"],
        ["KPI band", "Active robots · avg uptime/day · tickets · avg CSAT · won value (scorecards)"],
        ["Fleet health", "Uptime trend by product (line) · total errors by product (bar)"],
        ["Support", "Avg resolution hours by severity (bar) · (drill: by category)"],
        ["Sales", "Won value by month (area) · win rate by product (bar) · avg CSAT by product (bar)"],
    ], [1.1*inch, 5.1*inch]))
    st.append(Paragraph("Data sources (upload-ready extracts)", h2))
    st.append(Paragraph("data/week08/extracts/: fleet_health_daily.csv, support_performance.csv, sales_pipeline.csv, "
        "kpi_summary_by_product.csv — all aggregated directly from the Week 7 DuckDB warehouse.", body))
    st.append(Paragraph("Filters &amp; interactions", h2))
    st.append(Paragraph("<b>Date-range</b> control (default last 24 months) and <b>Product-line</b> filter (All / each of the five). "
        "Both apply to every panel; the KPI band recomputes on filter change. Date and product keys exist in every extract, so no broken states.", body))
    st.append(Paragraph("Chart types (and why)", h2))
    st.append(Paragraph("Lines for trends over time; bars for per-product comparison; area for cumulative monthly bookings; "
        "scorecards for headline KPIs. Severity uses an ordered Critical→Low scale with a sequential color ramp.", body))
    st.append(Paragraph("Prototype", h2))
    img = RPT / "prototype_product_analytics.png"
    if img.exists():
        st.append(Image(str(img), width=6.0*inch, height=3.38*inch))
    st.append(Paragraph("Success criteria (from plan)", h2))
    st.append(Paragraph("Loads &lt;5s · answers its question on the first screen · color-blind-safe palette · "
        "date + product filters update all charts coherently. Publishing produces the Looker Studio share link (user's account).", body))
    _doc(path, "Product Analytics Dashboard Spec").build(st)
    print(f"  spec -> {path.relative_to(ROOT)}")


def main():
    market_spec()
    product_spec()


if __name__ == "__main__":
    main()
