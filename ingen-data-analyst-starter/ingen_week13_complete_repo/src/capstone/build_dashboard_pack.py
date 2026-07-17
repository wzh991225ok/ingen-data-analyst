"""Week 13 — dashboard pack: the one-page 'how to read each one' index.

Bundles the three dashboards built in Weeks 8-9 with an honest status line for each.

Run: python -m src.capstone.build_dashboard_pack
"""
from __future__ import annotations
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                Image, PageBreak)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY

ROOT = Path(__file__).resolve().parents[2]
RPT = ROOT / "reports" / "week13"
RPT.mkdir(parents=True, exist_ok=True)
FIG = Path("/home/claude/cap_fig")

NAVY = colors.HexColor("#1F3864"); BLUE = colors.HexColor("#2E5496")
LT = colors.HexColor("#D9E1F2"); GREY = colors.HexColor("#595959")
AMBER = colors.HexColor("#B8860B")

S = getSampleStyleSheet()
body = ParagraphStyle("b", parent=S["Normal"], fontName="Helvetica", fontSize=9, leading=12.3,
                      spaceAfter=4, alignment=TA_JUSTIFY)
h1 = ParagraphStyle("h1", parent=S["Normal"], fontName="Helvetica-Bold", fontSize=16,
                    textColor=NAVY, spaceAfter=4)
h2 = ParagraphStyle("h2", parent=S["Normal"], fontName="Helvetica-Bold", fontSize=11,
                    textColor=BLUE, spaceBefore=8, spaceAfter=2)
cell = ParagraphStyle("c", parent=S["Normal"], fontName="Helvetica", fontSize=7.8, leading=10)
cap = ParagraphStyle("cap", parent=S["Normal"], fontName="Helvetica-Oblique", fontSize=7.4,
                     textColor=GREY, spaceBefore=2, spaceAfter=5)
foot = ParagraphStyle("f", parent=S["Normal"], fontName="Helvetica-Oblique", fontSize=7,
                      textColor=GREY)


def tbl(data, widths, fs=7.8):
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), fs),
        ("GRID", (0, 0), (-1, -1), 0.3, LT), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F6FC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return t


def build():
    st = []
    st.append(Paragraph("Dashboard Pack — How to Read Each One", h1))
    st.append(Paragraph("Three dashboards, built across Weeks 8–9, each answering a different question for a "
                        "different audience. This page is the index; the sections below say what each one shows, who "
                        "it is for, and what to be careful about.", body))

    st.append(tbl([
        ["Dashboard", "Tool", "Audience", "Question it answers", "Status"],
        [Paragraph("<b>Market &amp; Competitive</b>", cell), "Tableau Public",
         Paragraph("Exec, BD, marketing", cell),
         Paragraph("How big are our markets, who competes, and where is demand moving?", cell),
         Paragraph("Spec + extracts + prototype complete. <b>Not published</b> — needs a Tableau Public account.", cell)],
        [Paragraph("<b>Product Analytics</b>", cell), "Looker Studio",
         Paragraph("Product, support, ops", cell),
         Paragraph("How is the fleet performing, how is support doing, what's in the pipeline?", cell),
         Paragraph("Spec + extracts + prototype complete. <b>Not published</b> — needs a Google account + Sheets connector.", cell)],
        [Paragraph("<b>Executive Scorecard</b>", cell), "Power BI",
         Paragraph("Leadership", cell),
         Paragraph("Are we on target, and where are we off?", cell),
         Paragraph("Spec + 10 DAX measures + prototype complete. <b>Not published</b> — needs Power BI Desktop + a workspace.", cell)],
    ], [1.05 * inch, 0.85 * inch, 0.95 * inch, 1.85 * inch, 1.9 * inch]))

    st.append(Paragraph("Read this first — the honest status", h2))
    st.append(Paragraph("<b>None of the three is live.</b> Each has a complete specification, an upload-ready "
                        "pre-aggregated extract, and a rendered prototype showing exactly what it looks like. What is "
                        "missing is publication, which runs through the analyst's personal Tableau/Google/Microsoft "
                        "accounts — so there are no live URLs and none are claimed. Anyone with the relevant account "
                        "can publish from the extracts in an afternoon; see HANDOFF.md.", body))
    st.append(Paragraph("<b>All three sit on synthetic data</b> (the Week 7 warehouse) except the Market &amp; "
                        "Competitive dashboard, which uses real public data from Weeks 4–6. The KPI targets on the "
                        "Executive Scorecard are my reasonable assumptions, not InGen's actual targets — the traffic "
                        "lights show the mechanism working, not a verdict on the business.", body))

    st.append(Paragraph("1 · Market & Competitive (Tableau Public)", h2))
    st.append(Paragraph("<b>What it shows:</b> five tabs — market sizing by vertical (TAM/SAM/SOM with the "
                        "sensitivity range), the demand-signal index and its components, peer financial benchmarks, "
                        "the competitor landscape, and a summary. <b>Built from real public data</b> (Weeks 4–6).<br/>"
                        "<b>How to read it:</b> start on the summary tab. Market bars are <i>ranges</i>, not points — "
                        "the width is the finding. The demand index is <i>relative</i> (0–100 across our five "
                        "verticals), not an absolute measure of market size; a high demand score with a low market "
                        "score means attention without money, and vice versa.<br/>"
                        "<b>Watch out for:</b> the demand index and the market size deliberately disagree "
                        "(§5 of the capstone). That is not a data error.", body))
    if (FIG / "prototype_market_competitive.png").exists():
        st.append(Image(str(FIG / "prototype_market_competitive.png"), width=5.6 * inch, height=3.15 * inch))
        st.append(Paragraph("Market &amp; Competitive prototype (Week 8) — rendered from the real Weeks 4–6 data.", cap))

    st.append(PageBreak())
    st.append(Paragraph("2 · Product Analytics (Looker Studio)", h2))
    st.append(Paragraph("<b>What it shows:</b> fleet health (active rate, uptime, battery, errors), support "
                        "performance (volume, resolution time, CSAT by severity), and sales pipeline (stage funnel, "
                        "win rate, cycle time) — with date-range and product filters.<br/>"
                        "<b>How to read it:</b> the date filter drives everything; the product filter cross-filters "
                        "all three panels. Fleet health is a daily grain; support and pipeline are per-record grains "
                        "rolled up — so a spike in ticket volume does not mean a spike in fleet issues unless the "
                        "error-rate panel moves too.<br/>"
                        "<b>Watch out for:</b> <b>this is synthetic data.</b> Nothing here measures a real robot. It "
                        "shows what the dashboard does, not what the fleet is doing.", body))
    if (FIG / "prototype_product_analytics.png").exists():
        st.append(Image(str(FIG / "prototype_product_analytics.png"), width=5.9 * inch, height=3.3 * inch))
        st.append(Paragraph("Product Analytics prototype (Week 8) — from the synthetic Week 7 warehouse.", cap))

    st.append(Paragraph("3 · Executive Scorecard (Power BI)", h2))
    st.append(Paragraph("<b>What it shows:</b> eight KPIs against targets with red/amber/green status and "
                        "drill-through to detail — fleet active rate, uptime, critical resolution time, ticket "
                        "resolve rate, CSAT, win rate, won value, and sales-cycle length. Backed by ten documented, "
                        "reusable DAX measures (docs/dax_measures.md).<br/>"
                        "<b>How to read it:</b> the RAG status is <i>relative to a target</i>, so read the target, not "
                        "just the colour. Two KPIs sit amber on the synthetic data (ticket resolve rate 88% against a "
                        "90% target; CSAT 3.84 against 4.0) — that is the mechanism working, not a business finding.<br/>"
                        "<b>Watch out for:</b> the targets are <b>my assumptions</b>. Confirm the real ones before "
                        "anyone reads a colour as a verdict. That is TODO #3 in HANDOFF.md.", body))
    if (FIG / "prototype_powerbi_scorecard.png").exists():
        st.append(Image(str(FIG / "prototype_powerbi_scorecard.png"), width=5.9 * inch, height=1.5 * inch))
        st.append(Paragraph("Executive Scorecard prototype (Week 9).", cap))

    st.append(Paragraph("Files in the pack", h2))
    st.append(tbl([
        ["Artifact", "Where"],
        ["Tableau spec (5 tabs, field-by-field)", "reports/week08/spec_market_competitive.pdf"],
        ["Looker spec (3 panels, filters, grain)", "reports/week08/spec_product_analytics.pdf"],
        ["Power BI spec + RAG rules", "reports/week09/spec_powerbi.pdf"],
        ["DAX measures (10, documented)", "docs/dax_measures.md"],
        ["Upload-ready extracts (largest ~3.6k rows)", "data/week08/extracts/*.csv"],
        ["Prototypes (rendered)", "reports/week08/prototype_*.png · reports/week09/prototype_powerbi_scorecard.png"],
        ["Design review log (incl. the rejected red/green palette)", "reports/week08/design_review_log.md"],
    ], [2.6 * inch, 3.9 * inch]))

    st.append(Paragraph("Design notes worth keeping", h2))
    st.append(Paragraph("The palette is <b>Okabe-Ito</b> (colour-blind safe) — an earlier red/green draft was "
                        "rejected in review for exactly that reason, and the log records why. Chart types were "
                        "checked against what they actually encode (a donut was replaced with ranked bars). "
                        "Dashboards are fed <b>pre-aggregated extracts</b>, not raw 100k-row tables, so they load in "
                        "well under five seconds. Keep all three properties if you rebuild.", body))

    st.append(Spacer(1, 5))
    st.append(Table([[Paragraph("Ziheng Wang · inGen Data Analyst internship · Week 13 dashboard pack. "
                                "Status is stated honestly: all three dashboards are specified, extracted and "
                                "prototyped; none is published, and no live URLs exist.", foot)]],
                    colWidths=[6.5 * inch],
                    style=TableStyle([("LINEABOVE", (0, 0), (-1, -1), 0.5, LT),
                                      ("TOPPADDING", (0, 0), (-1, -1), 4)])))

    doc = SimpleDocTemplate(str(RPT / "dashboard_pack.pdf"), pagesize=letter,
                            leftMargin=0.8 * inch, rightMargin=0.8 * inch,
                            topMargin=0.6 * inch, bottomMargin=0.55 * inch,
                            title="Dashboard Pack — How to Read Each One", author="Ziheng Wang")
    doc.build(st)
    print(f"  dashboard pack -> {(RPT / 'dashboard_pack.pdf').relative_to(ROOT)}")


if __name__ == "__main__":
    build()
