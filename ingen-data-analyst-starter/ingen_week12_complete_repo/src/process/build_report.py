"""Week 12 — scenario chart + the 3-page optimisation recommendation memo.

Run: python -m src.process.build_report   (after stage_generator, cycle_time, drivers, capacity_sim)
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

NAVY = "#1F3864"; BLUE = "#2E5496"; ORANGE = "#E69F00"; RED = "#C0392B"; GREEN = "#2E7D5B"; GREY = "#7F7F7F"


def chart_scenarios():
    summ = pd.read_csv(DATA / "capacity_sim_summary.csv")
    paired = pd.read_csv(DATA / "capacity_sim_paired_deltas.csv")
    order = ["S0 Baseline", "S2 Reroute low-severity triage", "S1 +1 Field Ops FTE",
             "S3 Regional parts buffer (EU+APAC)", "S4 +1 Field FTE + parts buffer"]
    summ = summ.set_index("scenario").reindex([s for s in order if s in set(summ["scenario"])]).reset_index()

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 4.0), gridspec_kw={"width_ratios": [1.15, 1]})
    colors = [GREY if s.startswith("S0") else (GREEN if "parts" in s else BLUE) for s in summ["scenario"]]
    y = np.arange(len(summ))
    a1.barh(y, summ["mean"], color=colors)
    a1.errorbar(summ["mean"], y, xerr=[summ["mean"] - summ["ci_low"], summ["ci_high"] - summ["mean"]],
                fmt="none", ecolor="#333", capsize=3, lw=1)
    a1.set_yticks(y); a1.set_yticklabels([s[:34] for s in summ["scenario"]], fontsize=8.5)
    for i, (m, d) in enumerate(zip(summ["mean"], summ["delta_pct_vs_base"])):
        lab = f"{m:.1f}h" + (f"  ({d:+.1f}%)" if abs(d) > 0.01 else "  (baseline)")
        a1.text(m + 0.4, i, lab, va="center", fontsize=8.5, color=NAVY)
    a1.set_xlim(0, summ["mean"].max() * 1.28)
    a1.set_xlabel("Mean cycle time (hours), 95% CI across 8 replications", fontsize=9)
    a1.set_title("What each change actually buys", fontsize=11.5, color=NAVY, fontweight="bold")
    a1.spines[["top", "right"]].set_visible(False); a1.invert_yaxis()

    p = paired.set_index("scenario").reindex([s for s in order[1:] if s in set(paired["scenario"])]).reset_index()
    yy = np.arange(len(p))
    cols = [GREEN if r["significant_95"] else RED for _, r in p.iterrows()]
    a2.barh(yy, p["paired_delta_hours"], color=cols)
    a2.errorbar(p["paired_delta_hours"], yy,
                xerr=[p["paired_delta_hours"] - p["ci_low"], p["ci_high"] - p["paired_delta_hours"]],
                fmt="none", ecolor="#333", capsize=3, lw=1)
    a2.axvline(0, color="#333", lw=1)
    a2.set_yticks(yy); a2.set_yticklabels([s[:30] for s in p["scenario"]], fontsize=8.5)
    for i, r in p.iterrows():
        a2.text(r["paired_delta_hours"] - 0.25, i, f"{r['paired_delta_hours']:.2f}h",
                va="center", ha="right", fontsize=8.5, color=NAVY)
    a2.set_xlabel("Paired change in mean cycle time vs baseline (h)", fontsize=9)
    a2.set_title("Green = significant at 95%; red = not", fontsize=11.5, color=NAVY, fontweight="bold")
    a2.spines[["top", "right"]].set_visible(False); a2.invert_yaxis()
    plt.tight_layout(); fig.savefig(RPT / "scenario_comparison.png", dpi=135); plt.close()


def build_memo():
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                    Image, PageBreak)
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    dec = pd.read_csv(DATA / "stage_decomposition.csv")
    eff = pd.read_csv(DATA / "driver_effects.csv")
    summ = pd.read_csv(DATA / "capacity_sim_summary.csv")
    paired = pd.read_csv(DATA / "capacity_sim_paired_deltas.csv")
    rec = pd.read_csv(DATA / "driver_recovery_check.csv")
    cc = pd.read_csv(DATA / "control_chart_weekly.csv")

    NV = colors.HexColor(NAVY); BL = colors.HexColor(BLUE); LT = colors.HexColor("#D9E1F2")
    S = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=S["Normal"], fontName="Helvetica", fontSize=9, leading=12.3, spaceAfter=4)
    h1 = ParagraphStyle("h1", parent=S["Normal"], fontName="Helvetica-Bold", fontSize=14.5, textColor=NV, spaceAfter=2)
    h2 = ParagraphStyle("h2", parent=S["Normal"], fontName="Helvetica-Bold", fontSize=10.5, textColor=BL, spaceBefore=7, spaceAfter=2)
    cell = ParagraphStyle("c", parent=S["Normal"], fontName="Helvetica", fontSize=8, leading=10.4)
    foot = ParagraphStyle("f", parent=S["Normal"], fontName="Helvetica-Oblique", fontSize=7, textColor=colors.HexColor("#666"))

    def tbl(data, widths, align_mid=True):
        t = Table(data, colWidths=widths)
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), BL), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.3, LT), ("VALIGN", (0, 0), (-1, -1), "MIDDLE" if align_mid else "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F6FC")]),
            ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
        return t

    base = summ[summ.scenario == "S0 Baseline"].iloc[0]
    s1 = paired[paired.scenario.str.startswith("S1")].iloc[0]
    s2 = paired[paired.scenario.str.startswith("S2")].iloc[0]
    s3 = paired[paired.scenario.str.startswith("S3")].iloc[0]
    s4 = paired[paired.scenario.str.startswith("S4")].iloc[0]
    top3 = dec.head(3)
    disp = eff[(eff.model == "B: + dispatch path") & (eff.term == "dispatched")].iloc[0]
    wl = eff[(eff.model == "A: brief spec") & (eff.term == "tier1_queue_on_entry")].iloc[0]
    r2a = 0.042; r2b = 0.719

    st = []
    # ============================== PAGE 1 — DIAGNOSTIC ==============================
    st.append(Paragraph("Support-Ticket Lifecycle — Optimisation Recommendation", h1))
    st.append(Paragraph("Week 12 · InGen fleet support (Fari, Sentinel, Aido) · simulated workflow on the "
                        "Week 7 warehouse · prepared by Ziheng Wang", body))

    st.append(Paragraph("Recommendation in one line", h2))
    st.append(tbl([[Paragraph("<b>Stock parts regionally before you hire.</b>", cell),
                    Paragraph(f"A local parts buffer in Europe and APAC cuts mean cycle time "
                              f"<b>{abs(s3['paired_delta_pct']):.0f}%</b> ({base['mean']:.1f}h → "
                              f"{summ[summ.scenario.str.startswith('S3')].iloc[0]['mean']:.1f}h). Adding a Field Ops "
                              f"FTE cuts it <b>{abs(s1['paired_delta_pct']):.0f}%</b>. Doing both cuts it "
                              f"<b>{abs(s4['paired_delta_pct']):.0f}%</b>. Rerouting Tier-1 triage — the obvious "
                              f"lever — changes <b>nothing measurable</b>.", cell)]],
                  [1.55 * inch, 4.95 * inch], align_mid=False))

    st.append(Paragraph("The process", h2))
    st.append(Paragraph("Intake → Triage (Tier 1) → Remote diagnosis (Tier 2) → <i>[ Parts &amp; dispatch → "
                        "On-site repair (Field Ops) ]</i> → Verification &amp; closure. The bracketed path runs only "
                        "when a ticket needs a physical part or site visit — 37% of tickets. Every one of the 5,000 "
                        "Week 7 tickets was replayed through this lifecycle; stage durations reconcile exactly to each "
                        "ticket's total cycle time, and every ticket_key joins 1:1 back to fact_support_tickets.", body))

    st.append(Paragraph("Where the time goes — top 3 stages are 90% of it", h2))
    rows = [["Stage", "% of all process time", "Cumulative", "Of which waiting", "Median", "P90"]]
    for _, r in dec[dec.total_hours > 0].iterrows():
        rows.append([r["stage"], f"{r['pct_of_total']:.1f}%", f"{r['cumulative_pct']:.1f}%",
                     f"{r['wait_share_of_stage']:.0f}%", f"{r['median_hours']:.1f}h", f"{r['p90_hours']:.1f}h"])
    st.append(tbl(rows, [1.5*inch, 1.15*inch, 0.85*inch, 1.0*inch, 0.7*inch, 0.7*inch]))
    st.append(Paragraph(f"<b>Parts &amp; dispatch alone is {top3.iloc[0]['pct_of_total']:.0f}% of all process time and "
                        f"is 100% waiting</b> — nobody is working during it, so no amount of headcount shortens it. "
                        f"On-site repair is {dec[dec.stage=='On-site repair'].iloc[0]['wait_share_of_stage']:.0f}% "
                        f"queueing, which headcount <i>can</i> shorten. That distinction drives the whole "
                        f"recommendation.", body))
    st.append(Image(str(RPT / "pareto_stages.png"), width=6.0*inch, height=2.80*inch))

    st.append(PageBreak())
    # ============================== PAGE 2 — DRIVERS + SIMULATION ==============================
    st.append(Paragraph("What moves cycle time — and what doesn't", h1))
    st.append(Paragraph("Regression of log(cycle time) on the drivers in the brief (product, severity, geography, "
                        "weekday, team workload), n = 5,000, 95% confidence intervals.", body))
    drows = [["Driver", "Effect on cycle time", "95% CI", "Significant?"]]
    for term in ["severity: Critical", "severity: High", "severity: Low", "tier1_queue_on_entry",
                 "region: APAC", "region: Europe", "product: Aido Humanoid", "weekday: Friday"]:
        r = eff[(eff.model == "A: brief spec") & (eff.term == term)]
        if not len(r): continue
        r = r.iloc[0]
        label = {"tier1_queue_on_entry": "Tier-1 queue length (per ticket waiting)"}.get(term, term)
        drows.append([label, f"{r['effect_pct']:+.1f}%",
                      f"[{r['ci_low_pct']:+.1f}%, {r['ci_high_pct']:+.1f}%]",
                      "yes" if r["significant_5pct"] else "no"])
    st.append(tbl(drows, [2.3*inch, 1.35*inch, 1.65*inch, 0.9*inch]))
    st.append(Paragraph(f"<b>These drivers together explain only {r2a:.0%} of the variance in cycle time.</b> Add one "
                        f"structural fact — did the ticket need a part? — and R² jumps to <b>{r2b:.0%}</b>: a "
                        f"dispatched ticket takes <b>{disp['effect_pct']:+.0f}%</b> longer "
                        f"[{disp['ci_low_pct']:+.0f}%, {disp['ci_high_pct']:+.0f}%]. Severity and queue length are real "
                        f"and significant (a Critical ticket clears {abs(eff[(eff.model=='A: brief spec')&(eff.term=='severity: Critical')].iloc[0]['effect_pct']):.0f}% faster; each "
                        f"ticket already queued adds {wl['effect_pct']:+.1f}%), but they are second-order. "
                        f"<b>Support cycle time is not a people-management problem; it is a parts problem.</b> Weekday "
                        f"shows no effect, which is expected — this model runs follow-the-sun cover with no shift "
                        f"calendar (see limitations).", body))

    st.append(Paragraph("Simulated changes — 8 replications each, paired to the same seeds", h2))
    st.append(Image(str(RPT / "scenario_comparison.png"), width=6.5*inch, height=2.26*inch))
    srows = [["Scenario", "Mean cycle", "Δ vs baseline", "95% CI of Δ", "Verdict"]]
    order = ["S0 Baseline", "S2 Reroute low-severity triage", "S1 +1 Field Ops FTE",
             "S3 Regional parts buffer (EU+APAC)", "S4 +1 Field FTE + parts buffer"]
    for name in order:
        m = summ[summ.scenario == name].iloc[0]
        if name == "S0 Baseline":
            srows.append([name, f"{m['mean']:.1f}h", "—", "—", "reference"])
            continue
        p = paired[paired.scenario == name].iloc[0]
        srows.append([name, f"{m['mean']:.1f}h", f"{p['paired_delta_pct']:+.1f}%",
                      f"[{p['ci_low']:.2f}h, {p['ci_high']:.2f}h]",
                      "significant" if p["significant_95"] else "no measurable effect"])
    st.append(tbl(srows, [2.15*inch, 0.8*inch, 0.9*inch, 1.35*inch, 1.2*inch]))

    st.append(PageBreak())
    # ============================== PAGE 3 — RECOMMENDATION + TRADE-OFFS ==============================
    st.append(Paragraph("Recommendation, trade-offs and limits", h1))

    st.append(Paragraph("Recommendation", h2))
    st.append(Paragraph(f"<b>1. Fund a regional parts buffer in Europe and APAC first.</b> It is the single largest "
                        f"lever in the model: <b>{abs(s3['paired_delta_pct']):.0f}%</b> off mean cycle time "
                        f"[{s3['ci_low']:.1f}h, {s3['ci_high']:.1f}h], and it also pulls P90 down from "
                        f"{base['p90_cycle_hours']:.0f}h to "
                        f"{summ[summ.scenario.str.startswith('S3')].iloc[0]['p90_cycle_hours']:.0f}h — the tail is what "
                        f"customers actually complain about.<br/>"
                        f"<b>2. Add the Field Ops FTE second.</b> Worth a real "
                        f"<b>{abs(s1['paired_delta_pct']):.0f}%</b>, and it nearly eliminates field-queue wait "
                        f"({base['mean_field_wait_hours']:.1f}h → "
                        f"{summ[summ.scenario.str.startswith('S1')].iloc[0]['mean_field_wait_hours']:.1f}h). But its "
                        f"ceiling is set by the stage's share of the process — On-site repair is only ~15% of total "
                        f"time, so perfect staffing there cannot buy more than ~15%.<br/>"
                        f"<b>3. Do not spend effort rerouting Tier-1 triage.</b> Triage is "
                        f"{dec[dec.stage=='Triage'].iloc[0]['pct_of_total']:.0f}% of process time; the simulated change "
                        f"is {s2['paired_delta_pct']:+.1f}% with a CI spanning zero — statistically indistinguishable "
                        f"from doing nothing.<br/>"
                        f"<b>Together (1+2): {abs(s4['paired_delta_pct']):.0f}%</b> off mean cycle time.", body))

    st.append(Paragraph("Trade-offs, named", h2))
    st.append(tbl([["Lever", "Cost", "Cycle time", "Service level", "Risk"],
                   [Paragraph("Regional parts buffer", cell),
                    Paragraph("Working capital tied up in inventory at two sites; obsolescence risk as hardware revs.", cell),
                    Paragraph(f"<b>−{abs(s3['paired_delta_pct']):.0f}%</b> mean; P90 "
                              f"{base['p90_cycle_hours']:.0f}h→{summ[summ.scenario.str.startswith('S3')].iloc[0]['p90_cycle_hours']:.0f}h", cell),
                    Paragraph("Biggest tail improvement — best CSAT lever", cell),
                    Paragraph("Stock the wrong SKUs and the gain evaporates", cell)],
                   [Paragraph("+1 Field Ops FTE", cell),
                    Paragraph("Recurring salary; hiring lead time; needs utilisation to stay justified.", cell),
                    Paragraph(f"<b>−{abs(s1['paired_delta_pct']):.0f}%</b> mean", cell),
                    Paragraph("Removes field queue almost entirely", cell),
                    Paragraph("Capped by the stage's 15% share of process time", cell)],
                   [Paragraph("Reroute Tier-1 triage", cell),
                    Paragraph("Engineering time to build auto-routing/self-service.", cell),
                    Paragraph(f"{s2['paired_delta_pct']:+.1f}% — not significant", cell),
                    Paragraph("No measurable gain", cell),
                    Paragraph("Opportunity cost of building it", cell)]],
                  [1.1*inch, 1.75*inch, 1.25*inch, 1.2*inch, 1.3*inch], align_mid=False))

    st.append(Paragraph("Is the process in control?", h2))
    st.append(Paragraph(f"Weekly mean cycle time over {len(cc)} weeks sits on a centre line of "
                        f"{cc['center'].iloc[0]:.1f}h with 3σ limits at {cc['lcl'].iloc[0]:.1f}–{cc['ucl'].iloc[0]:.1f}h; "
                        f"<b>{int(cc['out_of_control'].sum())} weeks breach the upper limit</b>. The process is broadly "
                        f"in statistical control — meaning the long cycle times are not an anomaly to be firefought, "
                        f"they are what this process delivers by design. Fixing them requires changing the process "
                        f"(parts availability), not chasing individual bad weeks.", body))
    st.append(Image(str(RPT / "control_chart.png"), width=5.8*inch, height=2.20*inch))

    st.append(Paragraph("Limitations — read before acting", h2))
    st.append(Paragraph(f"<b>This runs on synthetic data.</b> The Week 7 warehouse carries no stage, team or workload "
                        f"fields, so the lifecycle layer was generated by a documented model "
                        f"(src/process/process_model.py) replaying Week 7's real ticket stream. Every number above is "
                        f"therefore a property of that model, <b>not a measurement of InGen's support org</b>. Team "
                        f"sizes (Tier 1 = 1, Tier 2 = 2, Field Ops = 1) were chosen to load the teams realistically "
                        f"against the observed ~6.8 tickets/day, not observed from data.<br/>"
                        f"<b>What does transfer</b> is the method and the pipeline: point the same code at real ticket "
                        f"data with stage timestamps and it produces the same diagnostic. The driver regression was "
                        f"validated against the model's known generating parameters and recovered "
                        f"<b>{int(rec['direction_recovered'].sum())}/{len(rec)}</b> effect directions — the two misses "
                        f"are small, non-significant product effects that act only on a stage covering 15% of time for "
                        f"37% of tickets, so they are diluted below noise. No shift calendar is modelled, so the null "
                        f"weekday result should not be read as evidence that weekday doesn't matter in reality.<br/>"
                        f"<b>The ask:</b> real support-ticket data with stage-level timestamps would turn this from a "
                        f"validated method into an actual answer.", body))
    st.append(Spacer(1, 3))
    st.append(Table([[Paragraph("Reproduce: python -m src.process.stage_generator → cycle_time → drivers → "
                                "capacity_sim → build_report. Seeded (SEED=20260710); 8 replications per scenario; "
                                "paired deltas against identical seeds. Ziheng Wang · inGen Data Analyst internship · Week 12.", foot)]],
                    colWidths=[6.6*inch],
                    style=TableStyle([("LINEABOVE", (0, 0), (-1, -1), 0.5, LT), ("TOPPADDING", (0, 0), (-1, -1), 4)])))

    doc = SimpleDocTemplate(str(RPT / "process_optimization_memo.pdf"), pagesize=letter,
                            leftMargin=0.75*inch, rightMargin=0.75*inch, topMargin=0.55*inch,
                            bottomMargin=0.5*inch, title="Support Lifecycle Optimisation Memo",
                            author="Ziheng Wang")
    doc.build(st)
    print(f"  memo -> {(RPT / 'process_optimization_memo.pdf').relative_to(ROOT)}")


def main():
    chart_scenarios(); print("  scenario_comparison.png")
    build_memo()


if __name__ == "__main__":
    main()
