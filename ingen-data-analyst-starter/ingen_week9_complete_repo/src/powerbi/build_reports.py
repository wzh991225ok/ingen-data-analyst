"""Week 9 — Power BI spec PDF + 5-page mid-internship review packet.

Run: python -m src.powerbi.build_reports
"""
from __future__ import annotations
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

ROOT = Path(__file__).resolve().parents[2]
RPT = ROOT / "reports" / "week09"
RPT.mkdir(parents=True, exist_ok=True)
NAVY = colors.HexColor("#1F3864"); BLUE = colors.HexColor("#2E5496"); LT = colors.HexColor("#D9E1F2"); GREEN = colors.HexColor("#2E7D5B")
S = getSampleStyleSheet()
body = ParagraphStyle("b", parent=S["Normal"], fontName="Helvetica", fontSize=9.5, leading=13.5, spaceAfter=5)
bl = ParagraphStyle("bl", parent=body, leftIndent=12, bulletIndent=2, spaceAfter=3)
h1 = ParagraphStyle("h1", parent=S["Normal"], fontName="Helvetica-Bold", fontSize=16, textColor=NAVY, spaceAfter=3)
h2 = ParagraphStyle("h2", parent=S["Normal"], fontName="Helvetica-Bold", fontSize=11.5, textColor=BLUE, spaceBefore=9, spaceAfter=3)
foot = ParagraphStyle("f", parent=S["Normal"], fontName="Helvetica-Oblique", fontSize=7.5, textColor=colors.HexColor("#595959"))
cell = ParagraphStyle("cell", parent=S["Normal"], fontName="Helvetica", fontSize=9, leading=12.5)


def _tbl(data, widths):
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), BLUE), ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), ("FONTSIZE", (0,0), (-1,-1), 8.3),
        ("GRID", (0,0), (-1,-1), 0.3, LT), ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F2F6FC")]),
        ("TOPPADDING", (0,0), (-1,-1), 3), ("BOTTOMPADDING", (0,0), (-1,-1), 3)]))
    return t


def powerbi_spec():
    path = RPT / "spec_powerbi.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=letter, leftMargin=0.8*inch, rightMargin=0.8*inch,
                            topMargin=0.6*inch, bottomMargin=0.6*inch, title="Power BI Dashboard Spec", author="Ziheng Wang")
    st = [Paragraph("Dashboard Spec — Executive Scorecard (Power BI)", h1),
          Paragraph("Third BI tool, different angle from Looker: an executive scorecard with traffic-light KPIs and "
                    "drill-through to product detail. Built on the Week 7 synthetic warehouse.", body)]
    st.append(Paragraph("Question it answers", h2))
    st.append(Paragraph("<b>“At a glance, is the business on target — and where isn't it?”</b> Eight RAG KPI tiles vs "
                        "explicit targets; click any tile to drill through to that product's detail page.", body))
    st.append(Paragraph("KPIs & targets (traffic lights)", h2))
    st.append(_tbl([
        ["KPI", "Target", "DAX measure"],
        ["Fleet active rate", "≥ 95%", "Fleet Active Rate %"],
        ["Avg uptime / day", "≥ 12 h", "Avg Uptime (AVERAGE)"],
        ["Critical resolution", "≤ 8 h", "Avg Resolution Hours (Critical)"],
        ["Ticket resolve rate", "≥ 90%", "Resolve Rate %"],
        ["Avg CSAT", "≥ 4.0", "Avg CSAT + CSAT Status"],
        ["Win rate", "≥ 35%", "Win Rate %"],
        ["Won value (TTM)", "≥ $150M", "Won Value + Rolling 3M"],
        ["Avg sales cycle", "≤ 100 d", "Avg Cycle (AVERAGE)"],
    ], [1.7*inch, 1.0*inch, 3.5*inch]))
    st.append(Paragraph("Pages & interactions", h2))
    st.append(Paragraph("Page 1 — Scorecard (8 RAG tiles + bookings trend). Page 2 — Product detail (drill-through "
        "target): per-product fleet/support/sales with the product passed as filter. Slicers: date range + product + geography. "
        "Tile color is bound to a `… Status` measure (RAG); see docs/dax_measures.md.", body))
    st.append(Paragraph("Build kit", h2))
    st.append(Paragraph("Import the Week 7 warehouse tables (Get Data → DuckDB/ODBC, or the synthetic CSVs). Recreate the "
        "star relationships (facts→dims on the surrogate keys). Mark dim_date as the date table. Paste the 10 measures from "
        "docs/dax_measures.md. Lay out tiles per the prototype below; bind conditional formatting to the Status measures.", body))
    st.append(Paragraph("Prototype (build target)", h2))
    img = RPT / "prototype_powerbi_scorecard.png"
    if img.exists():
        st.append(Image(str(img), width=6.0*inch, height=3.38*inch))
    st.append(Spacer(1, 6))
    st.append(_tbl([[Paragraph("Note", cell), Paragraph("The .pbix is assembled in Power BI Desktop (Windows). This spec + the DAX reference + the "
        "prototype make that ~30-min mechanical work; export to PDF from Power BI for the /reports/week09 PDF artifact. "
        "No .pbix is fabricated here — the prototype is rendered from real warehouse KPIs.", cell)]], [0.9*inch, 5.3*inch]))
    doc.build(st)
    print(f"  spec -> {path.relative_to(ROOT)}")


def review_packet():
    path = RPT / "mid_internship_review.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=letter, leftMargin=0.8*inch, rightMargin=0.8*inch,
                            topMargin=0.6*inch, bottomMargin=0.6*inch, title="Mid-Internship Review", author="Ziheng Wang")
    st = []
    # ---- Page 1: cover + summary ----
    st.append(Paragraph("Mid-Internship Review", h1))
    st.append(Paragraph("Ziheng Wang · Data Analyst Intern · inGen Dynamics (Futurenauts) · Weeks 1–8 · prepared for supervisor review", body))
    st.append(Spacer(1, 6))
    st.append(Paragraph("Summary", h2))
    st.append(Paragraph("Through Week 8 I completed Phase 1 (industry &amp; data foundation) and Phase 2 (market &amp; "
        "competitive analytics), and built out Phase 3 (BI development). The work is a connected arc: understand the five "
        "verticals, engineer a public-data foundation, size the markets, read demand and competitor financials, then stand up "
        "a queryable warehouse and dashboards on top. A consistent discipline runs through all of it — real sourced data, "
        "ranges where there's genuine uncertainty, and clearly-labelled fallbacks where a live source wasn't reachable.", body))
    st.append(Paragraph("Phase status", h2))
    st.append(_tbl([
        ["Phase", "Weeks", "Status"],
        ["1 — Industry & data foundation", "1–3", "Complete"],
        ["2 — Market & competitive analytics", "4–6", "Complete"],
        ["3 — BI development & visualization", "7–9", "Wk7 complete; Wk8 built (publish pending); Wk9 in progress"],
        ["4 — Advanced analytics", "10–13", "Upcoming"],
    ], [3.0*inch, 0.8*inch, 2.4*inch]))
    st.append(PageBreak())

    # ---- Page 2: what shipped ----
    st.append(Paragraph("(a) What shipped — Weeks 1–8", h1))
    st.append(_tbl([
        ["Wk", "Deliverable", "Artifact"],
        ["1", "Product profiles, competitor landscape (40+), data dictionary", "week1 repo"],
        ["2", "15 priority peers: real patents, headcounts, IP-vs-funding analysis", "week2 repo"],
        ["3", "12-dataset ingestion pipeline, DuckDB warehouse, 15 tests, DQ report", "week3 repo"],
        ["4", "TAM/SAM/SOM all 5 verticals, dual-method, tornado sensitivity, workbook", "week4 repo"],
        ["5", "Demand signals (search/news/VoC) + demand-signal index; pain-point taxonomy", "week5 repo"],
        ["6", "Peer financial benchmark (public FY24 + private funding), one-pager, memo", "week6 repo"],
        ["7", "Star-schema warehouse, 100k-row synthetic data, 15 queries, SQL self-assessment 12/12", "week7 repo"],
        ["8", "Two dashboards (Tableau + Looker): specs, real extracts, prototypes, design log", "week8 repo"],
    ], [0.4*inch, 4.3*inch, 1.5*inch]))
    st.append(Paragraph("Every week is a self-contained repo with a README and tests where applicable; all are linked from "
        "the repository INDEX.md.", body))
    st.append(PageBreak())

    # ---- Page 3: what worked / what slowed ----
    st.append(Paragraph("(b) What worked · (c) What slowed progress", h1))
    st.append(Paragraph("What worked", h2))
    for t in [
        "<b>Reusable foundation paid off.</b> The Week 3 ingestion pipeline + DuckDB warehouse were reused directly in Weeks 4, 7, and 8 — building it once accelerated everything after.",
        "<b>Data-integrity discipline.</b> Insisting on sourced values, ranges over false precision, and labelled fallbacks made the work defensible — e.g., the Week 6 benchmark cites a source per row and flags estimated cells.",
        "<b>Cross-week synthesis.</b> Findings compounded: Week 2's “funding ≠ defensible IP” was confirmed by Week 6's financials; Week 4 sizing + Week 5 demand together give a prioritization the company can act on.",
        "<b>Testing.</b> pytest suites (Weeks 3, 5, 6, 7) caught regressions and make every deliverable reproducible.",
    ]:
        st.append(Paragraph(t, bl, bulletText="•"))
    st.append(Paragraph("What slowed progress", h2))
    for t in [
        "<b>Network-restricted environment.</b> Live sources (Google Trends, GDELT, SEC EDGAR) aren't reachable from the build sandbox, so several weeks ship real code against real APIs plus labelled synthetic fallbacks. Fully populating live data needs a networked run.",
        "<b>External BI tools are manual.</b> Tableau Public, Looker Studio, and Power BI publish from my own accounts; I built specs/extracts/prototypes, but the final publish + URLs are a manual step.",
        "<b>No internal InGen data.</b> Market bottom-ups and product analytics rest on public/synthetic data; internal cost/pilot/CRM data would move several outputs from “directional” to “actionable.”",
    ]:
        st.append(Paragraph(t, bl, bulletText="•"))
    st.append(PageBreak())

    # ---- Page 4: Phase 4 goals ----
    st.append(Paragraph("(d) Phase 4 goals (Weeks 10–13)", h1))
    st.append(Paragraph("Phase 4 applies advanced analytics to InGen use cases. Concrete goals:", body))
    for t in [
        "<b>Week 10 — Forecasting.</b> Turn the Week 5 demand signals into supervised targets; fit baselines (seasonal naive, ETS, ARIMA) then Prophet + XGBoost with engineered features; Bass diffusion for humanoid adoption. Compare on MAPE/MASE; sanity-check vs published analyst forecasts.",
        "<b>Weeks 11–13 — applied modeling + capstone.</b> Extend into the remaining Phase 4 use cases and consolidate the internship into a capstone narrative that ties market → demand → financials → forecasts.",
        "<b>Standing objectives.</b> Keep every deliverable reproducible and sourced; convert at least one pipeline to a live networked run; and, where possible, validate against any internal data made available.",
    ]:
        st.append(Paragraph(t, bl, bulletText="•"))
    st.append(Paragraph("Success measure for Phase 4", h2))
    st.append(Paragraph("Forecasts that beat naive baselines on MAPE/MASE, are explainable by named drivers, and are "
        "honestly bounded with confidence intervals — not single-point numbers.", body))
    st.append(PageBreak())

    # ---- Page 5: the ask ----
    st.append(Paragraph("(e) One explicit ask of my supervisor", h1))
    st.append(Spacer(1, 4))
    st.append(_tbl([[Paragraph("The ask", cell),
        Paragraph("Can I get read access to one slice of real InGen data — even a small, anonymized export of fleet telemetry "
        "OR sales-pipeline records — so I can validate the Week 7 warehouse design and the Week 10 forecasts against reality? "
        "The synthetic warehouse mirrors the intended structure, so a real export would slot in with minimal rework and would "
        "move the analytics from directional to decision-grade.", cell)]], [1.1*inch, 5.1*inch]))
    st.append(Spacer(1, 8))
    st.append(Paragraph("Why this is the highest-leverage ask", h2))
    st.append(Paragraph("Most of what currently carries a caveat — bottom-up market assumptions, demand-as-proxy, synthetic "
        "product analytics — resolves the moment any real internal data is available to calibrate against. One representative "
        "export unlocks disproportionate value across Phases 3 and 4.", body))
    st.append(Paragraph("Secondary (smaller) asks", h2))
    for t in ["A networked environment (or approval to run locally) to populate the live Google Trends / GDELT / SEC pulls.",
              "15 minutes to confirm the five product names/positioning and any KPI targets the leadership team actually uses, so the scorecard reflects real targets."]:
        st.append(Paragraph(t, bl, bulletText="•"))
    st.append(Spacer(1, 10))
    st.append(Table([[Paragraph("Prepared by Ziheng Wang · inGen Data Analyst internship · mid-internship self-review · "
        "Weeks 1–8 shipped, Phase 4 next. All artifacts linked from the repository INDEX.md.", foot)]],
        colWidths=[6.9*inch], style=TableStyle([("LINEABOVE", (0,0), (-1,-1), 0.5, LT), ("TOPPADDING", (0,0), (-1,-1), 4)])))
    doc.build(st)
    print(f"  review -> {path.relative_to(ROOT)}")


def main():
    powerbi_spec()
    review_packet()


if __name__ == "__main__":
    main()
