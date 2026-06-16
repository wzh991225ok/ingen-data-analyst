"""Build the Week 6 benchmark one-pager (5-panel PDF) and methodology+caveats memo (2-page PDF).

Run:  python -m src.financials.build_reports
Outputs to reports/week06/.
"""
from __future__ import annotations
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from .peer_data import PUBLIC, PRIVATE, RETRIEVED

ROOT = Path(__file__).resolve().parents[2]
RPT = ROOT / "reports" / "week06"
RPT.mkdir(parents=True, exist_ok=True)
NAVY = "#1F3864"; BLUE = "#2E5496"; LIGHT = "#8FAADC"


def build_one_pager():
    fig = plt.figure(figsize=(11, 8.5))
    fig.suptitle("Robotics Peer Benchmark — one-page read (FY2024, public; latest rounds, private)",
                 fontsize=14, fontweight="bold", color=NAVY, y=0.97)
    names = [p["name"] for p in PUBLIC]
    rev = [p["revenue"] for p in PUBLIC]
    yoy = [(p["revenue"] / p["revenue_prior"] - 1) * 100 for p in PUBLIC]
    gm = [p["gross_margin"] * 100 for p in PUBLIC]
    rnd = [p["rnd"] / p["revenue"] * 100 for p in PUBLIC]

    ax1 = fig.add_subplot(2, 3, 1)
    ax1.bar(names, rev, color=BLUE); ax1.set_title("Revenue scale ($M, FY24)", fontsize=10)
    ax1.tick_params(axis="x", rotation=30, labelsize=8)

    ax2 = fig.add_subplot(2, 3, 2)
    ax2.bar(names, yoy, color=[("#C00000" if v < 0 else "#2E7D32") for v in yoy])
    ax2.axhline(0, color="#888", lw=0.8); ax2.set_title("Revenue growth (YoY %)", fontsize=10)
    ax2.tick_params(axis="x", rotation=30, labelsize=8)

    ax3 = fig.add_subplot(2, 3, 3)
    ax3.bar(names, gm, color=BLUE); ax3.set_title("Gross margin (%)", fontsize=10)
    ax3.tick_params(axis="x", rotation=30, labelsize=8)

    ax4 = fig.add_subplot(2, 3, 4)
    ax4.bar(names, rnd, color=LIGHT); ax4.set_title("R&D intensity (% of revenue)", fontsize=10)
    ax4.tick_params(axis="x", rotation=30, labelsize=8)

    # capital raised (private) — total disclosed
    from collections import defaultdict
    raised = defaultdict(float)
    for p in PRIVATE:
        if p["amount_musd"]:
            raised[p["name"]] += p["amount_musd"]
    pv = sorted(raised.items(), key=lambda kv: kv[1], reverse=True)
    ax5 = fig.add_subplot(2, 3, 5)
    ax5.barh([k for k, _ in pv][::-1], [v for _, v in pv][::-1], color=NAVY)
    ax5.set_title("Private capital raised ($M, disclosed)", fontsize=10)
    ax5.tick_params(axis="y", labelsize=8)

    ax6 = fig.add_subplot(2, 3, 6); ax6.axis("off")
    txt = ("Read in 30 seconds:\n\n"
           "• Vision/test peers (Cognex, Teradyne) carry\n  much higher gross margin than robotics\n  hardware (iRobot, Symbotic).\n\n"
           "• R&D intensity is high across the board\n  (~14-16% of revenue).\n\n"
           "• Humanoid privates are funded far ahead of\n  revenue — bets on future deployment.\n\n"
           "Public = SEC FY2024 filings/earnings.\nPrivate = press-sourced rounds.\n"
           f"Retrieved {RETRIEVED}.")
    ax6.text(0, 0.95, txt, va="top", fontsize=8.5, color="#222222")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    out = RPT / "benchmark_one_pager.pdf"
    plt.savefig(out, dpi=150); plt.close()
    print(f"one-pager -> {out.relative_to(ROOT)}")


def build_methodology():
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    NV = colors.HexColor("#1F3864"); BL = colors.HexColor("#2E5496"); LT = colors.HexColor("#D9E1F2")
    S = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=S["Normal"], fontName="Helvetica", fontSize=9.5, leading=13.5, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=S["Normal"], fontName="Helvetica-Bold", fontSize=15, textColor=NV, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=S["Normal"], fontName="Helvetica-Bold", fontSize=11.5, textColor=BL, spaceBefore=8, spaceAfter=3)
    foot = ParagraphStyle("f", parent=S["Normal"], fontName="Helvetica-Oblique", fontSize=7.5, textColor=colors.HexColor("#595959"))
    out = RPT / "methodology_and_caveats.pdf"
    doc = SimpleDocTemplate(str(out), pagesize=letter, leftMargin=0.8*inch, rightMargin=0.8*inch,
                            topMargin=0.6*inch, bottomMargin=0.6*inch,
                            title="InGen Week 6 — Peer Benchmark Methodology & Caveats", author="Ziheng Wang")
    st = [Paragraph("Week 6 — Financial Peer Benchmark: Methodology &amp; Caveats", h1),
          Paragraph("inGen Dynamics · robotics &amp; humanoid peer-comp model for benchmarking and fundraising narratives. "
                    "All figures from public disclosures.", body), Spacer(1, 4)]
    st.append(Paragraph("1. Peer universe", h2))
    st.append(Paragraph(
        "<b>Public:</b> iRobot (IRBT), Teradyne (TER), Cognex (CGNX), Symbotic (SYM) — robotics/automation/vision/test "
        "peers with SEC reporting. <b>Private:</b> humanoid/robotics peers from the Week 2 dossier — Figure AI, Apptronik, "
        "Agility Robotics, 1X Technologies, Neura Robotics, Gecko Robotics — selected for disclosed, press-verifiable rounds.", body))
    st.append(Paragraph("2. Metrics &amp; definitions", h2))
    st.append(Paragraph(
        "<b>Public:</b> revenue, revenue YoY growth, gross margin, R&amp;D as % of revenue, operating margin, net margin "
        "(FY2024 from 10-K/10-Q and earnings releases). <b>Private:</b> round, date, amount, lead investors, post-money "
        "valuation. <b>Comparables:</b> revenue growth and margin/R&amp;D intensity for public peers; "
        "<b>funding-per-employee</b> (total disclosed raised ÷ headcount) as a capital-efficiency proxy for private peers.", body))
    st.append(Paragraph("3. Caveats on comparability (important)", h2))
    for c in [
        "EV/Revenue is intentionally NOT hard-coded: enterprise value needs a live market cap (and net debt) on a chosen "
        "date. The workbook flags this; compute it at use-time from a current quote so it is never stale.",
        "Public vs private are not directly comparable: private valuations are negotiated post-money figures from primary "
        "rounds, not market-clearing prices, and reflect future-deployment optionality rather than current earnings.",
        "Robotics-hardware gross margins (iRobot ~21%, Symbotic ~18%) are structurally far below vision/test peers "
        "(Cognex ~68%, Teradyne ~58%); never benchmark across those groups without noting the business-model difference.",
        "Funding-per-employee is a rough proxy: headcounts are approximate and disclosed rounds may be partial, so treat "
        "it as directional, not precise.",
        "FY2024 cells marked 'approx/annualised' (yellow in the workbook) — notably Cognex full-year and Symbotic "
        "GM/R&D — should be confirmed against the exact filing before external use.",
    ]:
        st.append(Paragraph("• " + c, body))
    st.append(Paragraph("4. Reproducibility", h2))
    st.append(Paragraph(
        "Public anchors live in src/financials/peer_data.py with a source per row. For filing-exact 12-quarter histories, "
        "src/financials/edgar_fetch.py pulls Revenues / GrossProfit / R&amp;D / OperatingIncome from the SEC EDGAR "
        "companyfacts API (no key; run with INGEST_ALLOW_NETWORK=1 and a descriptive User-Agent). Private rounds each cite "
        "a public press source; extend the table via Crunchbase free tier as new rounds are announced.", body))
    st.append(Spacer(1, 8))
    st.append(Table([[Paragraph("Prepared by Ziheng Wang · inGen Data Analyst internship · Week 6 · " + RETRIEVED +
                                ". Public figures from SEC filings/earnings; private rounds press-sourced. Benchmark is for "
                                "context, not investment advice; verify EV/Revenue against a live quote before external use.", foot)]],
                    colWidths=[6.9*inch], style=TableStyle([("LINEABOVE", (0,0), (-1,-1), 0.5, LT), ("TOPPADDING", (0,0), (-1,-1), 4)])))
    doc.build(st)
    print(f"methodology -> {out.relative_to(ROOT)}")


def main():
    build_one_pager()
    build_methodology()


if __name__ == "__main__":
    main()
