"""Build Week 5 reports: pain-point taxonomy (markdown), charts (PNG), methodology (PDF).

Usage:  python -m src.signals.build_reports   (run after src.signals.run_all)
Outputs to reports/week05/.
"""
from __future__ import annotations
import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from . import base
from .demand_index import WEIGHTS


def _mode_note():
    rows = [json.loads(l) for l in base.MANIFEST.read_text().splitlines() if l.strip()]
    modes = {r.get("mode") for r in rows}
    live = "network" in modes or "file" in modes
    return rows, ("live + derived" if live and len(modes) > 1 else
                  ("live" if live else "offline-fallback (synthetic, schema-correct)"))


def build_taxonomy_md():
    pp = pd.read_csv(base.DATA / "pain_points_long.csv")
    out = ["# Week 5 — Voice-of-Customer Pain-Point Taxonomy", "",
           f"_Generated {base.TODAY}. Themes are TF-IDF + KMeans clusters of review text; "
           "the example shown is the most negative review in each theme. Where no real reviews "
           "file was supplied, a clearly-labelled sample corpus was used (see data dictionary)._", ""]
    for vert, (product, _) in base.VERTICALS.items():
        sub = pp[pp.vertical == vert].sort_values("size", ascending=False).head(5)
        out.append(f"## {product}  ({vert})")
        out.append("")
        for ti, (_, r) in enumerate(sub.iterrows(), 1):
            out.append(f"### Theme {ti} (n={r['size']}) — {r['top_terms']}")
            for col in ("example_1", "example_2", "example_3"):
                ex = str(r.get(col, "") or "").strip()
                if ex and ex.lower() != "nan":
                    out.append(f"- \"{ex}\"")
            out.append("")
    path = base.REPORTS / "pain_point_taxonomy.md"
    path.write_text("\n".join(out))
    print(f"  taxonomy -> {path.relative_to(base.ROOT)}")


def build_charts():
    idx = pd.read_csv(base.DATA / "demand_signal_index.csv").sort_values("demand_index")
    # 1) demand index bar
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.barh(idx["product"], idx["demand_index"], color="#2E5496")
    ax.set_xlabel("Demand-signal index (0-100, relative)")
    ax.set_title("Which vertical is heating up now — composite demand-signal index")
    for y, v in enumerate(idx["demand_index"]):
        ax.text(v + 1, y, f"{v:.0f}", va="center", fontsize=9)
    plt.tight_layout(); plt.savefig(base.REPORTS / "demand_index.png", dpi=120); plt.close()

    # 2) component stacked contribution
    comp = idx.copy()
    fig, ax = plt.subplots(figsize=(8, 4.2))
    left = [0] * len(comp)
    for col, w, color, lab in (("search_score", WEIGHTS["search_momentum"], "#2E5496", "Search momentum"),
                               ("news_vol_score", WEIGHTS["news_momentum"], "#8FAADC", "News momentum"),
                               ("news_tone_score", WEIGHTS["news_sentiment"], "#C6D2E8", "News sentiment")):
        contrib = (comp[col] * w).tolist()
        ax.barh(comp["product"], contrib, left=left, color=color, label=lab)
        left = [l + c for l, c in zip(left, contrib)]
    ax.set_xlabel("Weighted contribution to index"); ax.legend(fontsize=8, loc="lower right")
    ax.set_title("Demand-index composition by signal family")
    plt.tight_layout(); plt.savefig(base.REPORTS / "demand_index_components.png", dpi=120); plt.close()

    # 3) search-interest trends over time
    si = pd.read_csv(base.DATA / "search_interest_long.csv")
    fig, ax = plt.subplots(figsize=(9, 4.5))
    for vert, (product, _) in base.VERTICALS.items():
        s = si[si.vertical == vert].sort_values("date")
        ax.plot(range(len(s)), s["value"], label=product)
    ax.set_xlabel("Months (oldest -> newest)"); ax.set_ylabel("Search interest (0-100)")
    ax.set_title("Google Trends search interest by vertical"); ax.legend(fontsize=8)
    plt.tight_layout(); plt.savefig(base.REPORTS / "search_interest_trends.png", dpi=120); plt.close()
    print(f"  charts -> demand_index.png, demand_index_components.png, search_interest_trends.png")


def build_methodology_pdf():
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    rows, mode = _mode_note()
    idx = pd.read_csv(base.DATA / "demand_signal_index.csv")
    NAVY = colors.HexColor("#1F3864"); BLUE = colors.HexColor("#2E5496"); LIGHT = colors.HexColor("#D9E1F2")
    S = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=S["Normal"], fontName="Helvetica", fontSize=9.5, leading=13.5, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=S["Normal"], fontName="Helvetica-Bold", fontSize=15, textColor=NAVY, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=S["Normal"], fontName="Helvetica-Bold", fontSize=11.5, textColor=BLUE, spaceBefore=8, spaceAfter=3)
    foot = ParagraphStyle("f", parent=S["Normal"], fontName="Helvetica-Oblique", fontSize=7.5, textColor=colors.HexColor("#595959"))
    path = base.REPORTS / "demand_signal_methodology.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=letter, leftMargin=0.8*inch, rightMargin=0.8*inch,
                            topMargin=0.6*inch, bottomMargin=0.6*inch,
                            title="InGen Week 5 — Demand-Signal Methodology", author="Ziheng Wang")
    st = [Paragraph("Week 5 — Demand-Signal & Customer-Behavior Methodology", h1),
          Paragraph("inGen Dynamics service-robotics portfolio · search interest + news cadence/sentiment + "
                    "voice-of-customer, combined into one comparable demand-signal index across five verticals.", body),
          Spacer(1, 4)]
    st.append(Paragraph("1. Signal families & sources", h2))
    st.append(Paragraph(
        "<b>Search interest</b> — Google Trends (US) monthly interest for curated keywords per vertical (pytrends). "
        "<b>News cadence &amp; sentiment</b> — GDELT DOC 2.0 API: monthly article volume (TimelineVolRaw) and average "
        "tone (TimelineTone). <b>Voice-of-customer</b> — review/comment text per vertical, clustered with TF-IDF + KMeans "
        "into themes; the most negative review per theme is surfaced as the pain point.", body))
    st.append(Paragraph("2. Demand-signal index (documented weights)", h2))
    st.append(Paragraph(
        f"Each component is normalised 0-100 <i>across</i> verticals, then combined: "
        f"search momentum {int(WEIGHTS['search_momentum']*100)}% (last-12-mo vs prior-12-mo), "
        f"news momentum {int(WEIGHTS['news_momentum']*100)}% (last-6-mo vs prior-6-mo volume), "
        f"news sentiment {int(WEIGHTS['news_sentiment']*100)}% (mean tone, last 6 mo). "
        "The index is a <b>relative</b> read of which vertical is heating up now — not an absolute forecast.", body))
    # ranking table
    data = [["Rank", "Vertical / product", "Index", "Search", "News vol", "Sentiment"]]
    for _, r in idx.sort_values("rank").iterrows():
        data.append([int(r["rank"]), f"{r['product']} ({r['vertical']})", f"{r['demand_index']:.1f}",
                     f"{r['search_score']:.0f}", f"{r['news_vol_score']:.0f}", f"{r['news_tone_score']:.0f}"])
    t = Table(data, colWidths=[0.5*inch, 2.4*inch, 0.8*inch, 0.8*inch, 0.9*inch, 1.0*inch])
    t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), BLUE), ("TEXTCOLOR", (0,0), (-1,0), colors.white),
                           ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), ("FONTSIZE", (0,0), (-1,-1), 8.5),
                           ("GRID", (0,0), (-1,-1), 0.3, LIGHT), ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F2F6FC")])]))
    st += [t, Spacer(1, 6)]
    if (base.REPORTS / "demand_index.png").exists():
        st.append(Image(str(base.REPORTS / "demand_index.png"), width=5.6*inch, height=2.95*inch))
    st.append(Paragraph("3. Sentiment model choice (justification)", h2))
    st.append(Paragraph(
        "Two sentiment layers are used. For <b>news</b>, GDELT's document-level <b>tone</b> metric is taken directly "
        "(a validated, corpus-wide score on a consistent scale across all 24 months and verticals), which avoids "
        "re-scoring millions of articles and keeps the signal comparable. For <b>voice-of-customer</b>, themes come from "
        "<b>TF-IDF + KMeans</b> and each theme's pain point is the review with the highest count of negation/▫complaint "
        "terms from a fixed lexicon. This lexicon approach was chosen over a heavier spaCy/NLTK or transformer classifier "
        "because it is fully <b>deterministic and reproducible</b> (no model download, no random init beyond fixed-seed "
        "KMeans), transparent (the ranking rule is inspectable), and adequate for short review text; the same code accepts "
        "a spaCy/NLTK or BERTopic backend if richer sentiment is later required. Choice is documented here per the brief.", body))
    st.append(Paragraph("4. Reproducibility &amp; honesty", h2))
    st.append(Paragraph(
        f"Run mode for this build: <b>{mode}</b>. Real public APIs are wired in each collector; when network is "
        "unavailable the pipeline uses clearly-labelled schema-correct samples so it runs end-to-end, and the manifest "
        "(signal_manifest.jsonl) records mode per source. Set INGEST_ALLOW_NETWORK=1 to populate from live Google Trends "
        "and GDELT, and drop real reviews_&lt;vertical&gt;.csv files for live voice-of-customer.", body))
    st.append(Spacer(1, 8))
    st.append(Table([[Paragraph("Prepared by Ziheng Wang · inGen Data Analyst internship · Week 5 · "
                                + base.TODAY + ". Index is a relative demand read from public signals, not a forecast; "
                                "validate against internal pipeline/CRM data before planning decisions.", foot)]],
                    colWidths=[6.9*inch], style=TableStyle([("LINEABOVE", (0,0), (-1,-1), 0.5, LIGHT), ("TOPPADDING", (0,0), (-1,-1), 4)])))
    doc.build(st)
    print(f"  methodology -> {path.relative_to(base.ROOT)}")


def main():
    build_taxonomy_md()
    build_charts()
    build_methodology_pdf()


if __name__ == "__main__":
    main()
