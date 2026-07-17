"""Week 11 — charts + the 2-page Sentinel Prime operational framing PDF.

Run: python -m src.anomaly.build_report   (after run_all)
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "week11"
RPT = ROOT / "reports" / "week11"
RPT.mkdir(parents=True, exist_ok=True)

NAVY = "#1F3864"; BLUE = "#2E5496"; ORANGE = "#E69F00"; GREEN = "#2E7D5B"
RED = "#C0392B"; GREY = "#7F7F7F"
# Okabe-Ito (color-blind safe), consistent with the Week 8 design review
MODEL_COLOR = {"Isolation Forest": "#0072B2", "One-Class SVM": "#E69F00", "LOF": "#009E73",
               "AutoEncoder": "#CC79A7", "Control chart (EWMA)": "#7F7F7F"}


def chart_pr_curves():
    pr = pd.read_csv(DATA / "pr_curves.csv")
    res = pd.read_csv(DATA / "results.csv")
    dsets = pr["dataset"].unique()
    fig, axes = plt.subplots(1, len(dsets), figsize=(11, 4.1))
    for ax, ds in zip(np.atleast_1d(axes), dsets):
        sub = pr[pr.dataset == ds]
        base = None
        for m in sub["model"].unique():
            d = sub[sub.model == m].sort_values("recall")
            ap = res[(res.dataset == ds) & (res.model == m)]["avg_precision"].iloc[0]
            ax.plot(d["recall"], d["precision"], color=MODEL_COLOR.get(m, "#333"),
                    lw=1.7, label=f"{m} (AP={ap:.2f})")
        # base rate line = a random detector's precision
        r = res[res.dataset == ds].iloc[0]
        base = (r["tp"] + r["fn"]) / (r["tp"] + r["fn"] + r["fp"] + r["tn"])
        ax.axhline(base, color=RED, ls="--", lw=1, label=f"Base rate ({base:.2f})")
        ax.set_xlabel("Recall", fontsize=9); ax.set_ylabel("Precision", fontsize=9)
        ax.set_title(ds, fontsize=10.5, color=NAVY, fontweight="bold")
        ax.legend(fontsize=7, loc="upper right"); ax.grid(alpha=0.2)
        ax.set_ylim(0, 1.02); ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout(); fig.savefig(RPT / "pr_curves.png", dpi=135); plt.close()


def chart_confusion_matrices():
    res = pd.read_csv(DATA / "results.csv")
    dsets = res["dataset"].unique()
    models = res["model"].unique()
    fig, axes = plt.subplots(len(dsets), len(models), figsize=(13, 5.0))
    for i, ds in enumerate(dsets):
        for j, m in enumerate(models):
            ax = axes[i, j]
            r = res[(res.dataset == ds) & (res.model == m)]
            if len(r) == 0:
                ax.axis("off"); continue
            r = r.iloc[0]
            cm = np.array([[r["tn"], r["fp"]], [r["fn"], r["tp"]]], float)
            cmn = cm / cm.sum(axis=1, keepdims=True)  # row-normalised
            ax.imshow(cmn, cmap="Blues", vmin=0, vmax=1)
            for a in range(2):
                for b in range(2):
                    ax.text(b, a, f"{int(cm[a, b]):,}\n{cmn[a, b]:.0%}", ha="center", va="center",
                            fontsize=7.5, color="white" if cmn[a, b] > 0.5 else "#222")
            ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
            ax.set_xticklabels(["pred\nnormal", "pred\nanom"], fontsize=6.5)
            ax.set_yticklabels(["normal", "anomaly"], fontsize=6.5)
            if i == 0:
                ax.set_title(m, fontsize=8.5, color=NAVY, fontweight="bold")
            if j == 0:
                ax.set_ylabel(ds.split()[0], fontsize=8.5, color=NAVY, fontweight="bold")
    fig.suptitle("Confusion matrix per model (row-normalised; operating point = min false alarms at recall ≥ 80%)",
                 fontsize=10, color=NAVY, y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.95]); fig.savefig(RPT / "confusion_matrices.png", dpi=135); plt.close()


def chart_timeline():
    sf = pd.read_csv(DATA / "scores_nab.csv", parse_dates=["timestamp"])
    res = pd.read_csv(DATA / "results.csv")
    nab = res[res.dataset == "NAB machine_temperature"].sort_values("f1", ascending=False)
    best = nab.iloc[0]["model"]; thr = float(nab.iloc[0]["threshold"])
    fig, ax = plt.subplots(figsize=(11, 3.4))
    ax.plot(sf["timestamp"], sf[best], color=BLUE, lw=0.5, label=f"{best} anomaly score")
    ax.axhline(thr, color=ORANGE, ls="--", lw=1.2, label=f"threshold ({thr:.2f})")
    # shade true anomaly windows
    ano = sf["is_anomaly"].to_numpy()
    runs, st = [], None
    for i, v in enumerate(ano):
        if v == 1 and st is None: st = i
        elif v == 0 and st is not None: runs.append((st, i - 1)); st = None
    if st is not None: runs.append((st, len(ano) - 1))
    for k, (a, b) in enumerate(runs):
        ax.axvspan(sf["timestamp"].iloc[a], sf["timestamp"].iloc[b], color=RED, alpha=0.16,
                   label="true anomaly window" if k == 0 else None)
    ax.set_title(f"NAB machine temperature — {best} scores vs 4 labelled failure windows",
                 fontsize=10.5, color=NAVY, fontweight="bold")
    ax.set_ylabel("anomaly score", fontsize=9); ax.legend(fontsize=7.5, loc="upper left")
    ax.grid(alpha=0.2); ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout(); fig.savefig(RPT / "score_timeline.png", dpi=135); plt.close()


def chart_operational():
    fr = pd.read_csv(DATA / "operational_frontier.csv").sort_values("persistence_readings")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.6))
    x = fr["persistence_readings"] * 5  # minutes @5-min cadence
    a1.plot(x, fr["false_alerts_per_day"], "o-", color=BLUE, lw=2)
    for xi, yi in zip(x, fr["false_alerts_per_day"]):
        a1.annotate(f"{yi:.2f}", (xi, yi), fontsize=7.5, xytext=(4, 5), textcoords="offset points")
    a1.set_yscale("log"); a1.set_xlabel("Persistence filter (minutes sustained)", fontsize=9)
    a1.set_ylabel("False alerts per day (log)", fontsize=9)
    a1.set_title("Alert load collapses with persistence", fontsize=10.5, color=NAVY, fontweight="bold")
    a1.grid(alpha=0.25, which="both"); a1.spines[["top", "right"]].set_visible(False)

    a2.plot(x, fr["point_recall"], "o-", color=GREEN, lw=2, label="point recall")
    a2.axhline(0.80, color=RED, ls="--", lw=1, label="recall floor (80%)")
    a2.set_ylim(0.5, 1.02); a2.set_xlabel("Persistence filter (minutes sustained)", fontsize=9)
    a2.set_ylabel("Recall", fontsize=9)
    a2.set_title("...while recall stays above the floor", fontsize=10.5, color=NAVY, fontweight="bold")
    a2.legend(fontsize=8); a2.grid(alpha=0.25); a2.spines[["top", "right"]].set_visible(False)
    plt.tight_layout(); fig.savefig(RPT / "operational_frontier.png", dpi=135); plt.close()


def build_pdf():
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                    Image, PageBreak)
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    res = pd.read_csv(DATA / "results.csv")
    fr = pd.read_csv(DATA / "operational_frontier.csv")
    adapt = pd.read_csv(DATA / "adaptive_threshold.csv")
    lic = pd.read_csv(DATA / "dataset_licenses.csv")
    best = fr.iloc[0]   # lowest alert load meeting the recall floor

    NV = colors.HexColor(NAVY); BL = colors.HexColor(BLUE); LT = colors.HexColor("#D9E1F2")
    S = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=S["Normal"], fontName="Helvetica", fontSize=9, leading=12.4, spaceAfter=4)
    h1 = ParagraphStyle("h1", parent=S["Normal"], fontName="Helvetica-Bold", fontSize=14.5, textColor=NV, spaceAfter=2)
    h2 = ParagraphStyle("h2", parent=S["Normal"], fontName="Helvetica-Bold", fontSize=10.5, textColor=BL, spaceBefore=7, spaceAfter=2)
    cell = ParagraphStyle("c", parent=S["Normal"], fontName="Helvetica", fontSize=8, leading=10.5)
    foot = ParagraphStyle("f", parent=S["Normal"], fontName="Helvetica-Oblique", fontSize=7, textColor=colors.HexColor("#666"))

    def tbl(data, widths):
        t = Table(data, colWidths=widths)
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), BL), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.3, LT), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F6FC")]),
            ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
        return t

    st = []
    # ---------------- PAGE 1 ----------------
    st.append(Paragraph("Sentinel Prime AI — Anomaly Detection: Operational Framing", h1))
    st.append(Paragraph("Week 11 · public-data prototype (NAB + SKAB) · no InGen data used. "
                        "The question this answers: <b>what threshold should the product ship with, "
                        "to keep recall above a stated bar without drowning operators in false alarms?</b>", body))

    st.append(Paragraph("Recommendation (headline)", h2))
    st.append(tbl([[Paragraph("<b>Ship a sustained-anomaly rule, not a point rule.</b>", cell),
                    Paragraph(f"On the best model (AutoEncoder), alert only after <b>{int(best['persistence_readings'])} consecutive "
                              f"readings</b> ({int(best['persistence_readings'])*5} minutes sustained) above score "
                              f"<b>{best['threshold']:.2f}</b>. That catches <b>{int(best['events_caught'])}/{int(best['events_total'])} "
                              f"true failure events</b> at <b>{best['point_recall']:.0%} point-recall</b> while raising only "
                              f"<b>{best['false_alerts_per_day']:.2f} false alerts per day</b> — versus "
                              f"<b>16.35/day</b> for the same threshold with no persistence filter.", cell)]],
                  [1.5 * inch, 5.0 * inch]))

    st.append(Paragraph("Why the usual metric misleads", h2))
    st.append(Paragraph("At an 80% recall floor the point-level false-alarm rate sits near <b>13%</b> whichever threshold "
                        "or persistence setting we pick — it is fixed by how well the model separates the classes "
                        "(AP=0.51), not by threshold policy. But an operator never experiences '13% of readings'; they "
                        "experience <b>how often the phone buzzes</b>. Counting one alert per contiguous run — the way a "
                        "product pages — a 120-minute persistence filter cuts alert load <b>33×</b> (16.35 → 0.50/day) "
                        "while recall <i>rises</i> to 88%: the real failures are sustained, the false positives are "
                        "isolated spikes.", body))

    st.append(Paragraph("Stated bars, and an honest gap", h2))
    st.append(Paragraph("<b>Recall floor: 80%</b> of anomalous readings. <b>False-alarm budget: 5%</b> of normal readings. "
                        "<b>The point-level budget is not reachable</b> here: at 80% recall the achievable false-alarm "
                        "rate bottoms out near 13%. Closing that needs a better model (richer context/sensor fusion), not "
                        "more tuning. At the <i>alert</i> level the persistence rule already delivers a comfortable "
                        "0.5 false alerts/day.", body))

    st.append(Paragraph("Model comparison — 5 detectors, identical splits", h2))
    rows = [["Dataset", "Model", "P", "R", "F1", "AP", "FAR", "TTD (s)", "Events"]]
    for _, r in res.iterrows():
        rows.append([r["dataset"].split()[0], r["model"], f"{r['precision']:.3f}", f"{r['recall']:.3f}",
                     f"{r['f1']:.3f}", f"{r['avg_precision']:.3f}", f"{r['false_alarm_rate']:.3f}",
                     "—" if pd.isna(r["ttd_seconds"]) else f"{r['ttd_seconds']:.0f}",
                     f"{int(r['events_detected'])}/{int(r['events_total'])}"])
    st.append(tbl(rows, [0.62*inch, 1.28*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.55*inch, 0.7*inch, 0.6*inch]))
    st.append(Paragraph("AutoEncoder leads on NAB (F1 0.555, AP 0.512); LOF leads on SKAB (F1 0.545, AP 0.531). Both beat "
                        "the EWMA control-chart baseline — the bar that justifies the added complexity. On SKAB every "
                        "model shows a high false-alarm rate: that run is 34% anomalous, straining the 'mostly normal' "
                        "assumption behind unsupervised detection, so NAB is the more realistic Sentinel proxy.", body))
    st.append(Image(str(RPT / "pr_curves.png"), width=5.5*inch, height=2.05*inch))

    st.append(PageBreak())
    # ---------------- PAGE 2 ----------------
    st.append(Paragraph("Threshold policy — fixed vs adaptive (and what failed)", h1))
    st.append(Image(str(RPT / "operational_frontier.png"), width=6.5*inch, height=2.13*inch))

    st.append(Paragraph("Adaptive thresholds lost here — and the reason matters", h2))
    arows = [["Scheme", "Precision", "Recall", "F1", "FAR"]]
    for _, r in adapt.iterrows():
        arows.append([r["scheme"], f"{r['precision']:.3f}", f"{r['recall']:.3f}", f"{r['f1']:.3f}",
                      f"{r['false_alarm_rate']:.3f}"])
    st.append(tbl(arows, [3.3*inch, 0.8*inch, 0.7*inch, 0.7*inch, 0.7*inch]))
    st.append(Paragraph("A rolling-quantile threshold cut false alarms hard (13.4% → 3.3%) but <b>collapsed recall "
                        "(80% → 33%)</b>. Diagnosis: NAB's failure windows run ~2 days (~576 readings), so a baseline "
                        "computed over recent history <b>absorbs the anomaly into itself</b> and lifts the threshold "
                        "exactly when it should hold. This was not a tuning artefact — it survived a sweep of windows "
                        "(1k–12k readings) and EWMA rates (α 0.01–0.0002). Freezing the baseline during an alert "
                        "confirmed the diagnosis (recall recovered to 83%) but over-corrected: with the baseline frozen "
                        "it stops tracking legitimate drift and false alarms jump to 40%.", body))
    st.append(Paragraph("<b>Verdict:</b> adaptive thresholding is the right tool when the drift timescale is much longer "
                        "than the anomaly duration. For sustained failures like these, a fixed threshold calibrated on "
                        "clean commissioning data plus a persistence filter is both simpler and better. Sentinel should "
                        "default to fixed + persistence, and re-baseline on a schedule (or on a site change) rather than "
                        "continuously.", body))

    st.append(Paragraph("Suggested product behaviour: two tiers", h2))
    st.append(tbl([["Tier", "Rule", "Purpose"],
                   ["Fast", "score ≥ high cut-off, no persistence",
                    "Immediate page for unambiguous events (intrusion). Accepts more false alarms by design."],
                   ["Sustained", f"score ≥ {best['threshold']:.2f} for {int(best['persistence_readings'])*5} min",
                    "Low-noise channel for degradation/failure. ~0.5 false alerts/day; TTD ≥ persistence window."]],
                  [0.7*inch, 2.1*inch, 3.7*inch]))
    st.append(Paragraph("The persistence filter buys quiet at the cost of latency: a 120-minute rule cannot detect "
                        "anything faster than 120 minutes. That is acceptable for slow degradation, and unacceptable for "
                        "intrusion — hence two tiers rather than one compromise threshold.", body))

    st.append(Paragraph("Data & licences", h2))
    lrows = [["Dataset", "Series used", "Licence"]]
    for _, r in lic.iterrows():
        lrows.append([Paragraph(f"<b>{r['dataset']}</b><br/>{r['url']}", cell),
                      Paragraph(str(r["series_used"]), cell), Paragraph(str(r["license"]), cell)])
    st.append(tbl(lrows, [2.0*inch, 2.5*inch, 2.0*inch]))
    st.append(Paragraph("Both benchmarks are real public sensor data with published labels; no InGen data was used, "
                        "per the Week 11 brief. Splits: NAB trains on all readings before the first labelled window "
                        "(a clean warm-up, mirroring commissioning); SKAB trains on its shipped anomaly-free reference "
                        "run. Detectors are unsupervised — labels are used only to evaluate and to select the operating "
                        "point. Seeded (random_state=42) and reproducible via <font face='Courier'>python -m "
                        "src.anomaly.run_all</font>.", body))
    st.append(Spacer(1, 4))
    st.append(Table([[Paragraph("Prepared by Ziheng Wang · inGen Data Analyst internship · Week 11 · public-data "
                                "prototype. Findings transfer to Sentinel Prime as a method, not as calibrated "
                                "constants: the thresholds above are fitted to NAB's machine-temperature signal and "
                                "must be re-derived on real Sentinel telemetry before any field use.", foot)]],
                    colWidths=[6.6*inch],
                    style=TableStyle([("LINEABOVE", (0, 0), (-1, -1), 0.5, LT), ("TOPPADDING", (0, 0), (-1, -1), 4)])))

    doc = SimpleDocTemplate(str(RPT / "sentinel_operational_framing.pdf"), pagesize=letter,
                            leftMargin=0.75*inch, rightMargin=0.75*inch, topMargin=0.55*inch,
                            bottomMargin=0.5*inch, title="Sentinel Prime — Anomaly Detection Operational Framing",
                            author="Ziheng Wang")
    doc.build(st)
    print(f"  report -> {(RPT / 'sentinel_operational_framing.pdf').relative_to(ROOT)}")


def main():
    chart_pr_curves(); print("  pr_curves.png")
    chart_confusion_matrices(); print("  confusion_matrices.png")
    chart_timeline(); print("  score_timeline.png")
    chart_operational(); print("  operational_frontier.png")
    build_pdf()


if __name__ == "__main__":
    main()
