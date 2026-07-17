# Final Review — Feedback Log

**Session:** Week 13 final review · capstone presentation
**Presenter:** Ziheng Wang, Data Analyst Intern (Futurenauts)
**Audience:** Arshad Hisham (supervising supervisor) · HR / admin team · Iqbal (direct supervisor)
**Materials:** `capstone_report.pdf` (23pp) · `Capstone_Executive_Deck.pptx` / `.pdf` (15 slides) · `dashboard_pack.pdf`

---

## Status

**Awaiting the session.** This log is created with the agenda, the questions I expect, and my
prepared answers. **Feedback gets recorded below, verbatim, immediately after the review** — the
template is filled in, not rewritten, so what was actually said stays distinguishable from what I
planned to say.

> Nothing in the "Feedback received" section is filled in yet. It is not a placeholder to be quietly
> deleted — if the session doesn't happen, this file should say so.

---

## Agenda (20 minutes + questions)

| Min | Item | Slides |
|---|---|---|
| 0–2 | Framing: 13 weeks, 5 verticals, public data only | 1 |
| 2–6 | The six findings | 2 |
| 6–8 | How it was built — four phases, reproducible | 3 |
| 8–13 | Market → competition → demand → financials | 4–7 |
| 13–15 | The BI platform | 8 |
| 15–19 | Phase 4: forecasting, anomaly detection, process optimisation | 9–13 |
| 19–21 | Limitations, honestly | 14 |
| 21–25 | Recommendations + the one ask | 15 |

**The one thing I want them to remember:** the analysis is built and validated; a single small slice
of real internal data converts most of it from directional to decision-grade.

---

## Questions I expect, and my answers

**Q. All of this is public data — how much is actually usable?**
The methods and the pipeline are usable today; several findings are usable now (the Sentinel
attention gap, the funding-vs-IP pattern, the peer margin structures — all from real public
sources). What is *not* decision-grade is anything resting on synthetic data: Weeks 7–9 and 12 fix
the shape of the answer, not the answer. That's stated in §11 of the report and on slide 14.

**Q. Why is the support finding based on simulated data?**
Because the Week 7 warehouse has no stage, team or workload fields — and those are exactly what the
question needs. Rather than invent a parallel dataset I replayed Week 7's real ticket stream through
a documented process model, with reconciliation enforced and tested (1:1 ticket join; stage
durations sum exactly to cycle time). Then I validated the regression against the simulation's own
known parameters: it recovered 7 of 9 effect directions, and the two misses are explainable
(small product effects diluted below noise). So the method is sound; the −23% still needs real
tickets before anyone funds anything on it.

**Q. Which recommendation would you act on first?**
Market Sentinel Prime AI harder. It's the widest gap in the portfolio — first on market
attractiveness, last on demand signal — and unlike the operational recommendations it doesn't
depend on any synthetic data. It comes from real public sources on both sides of the gap.

**Q. How confident are you in the humanoid numbers?**
Not very, and deliberately so. Goldman's anchors and Morgan Stanley's projection differ by roughly
3× on 2035. The Bass curve fits Goldman's anchors exactly, but I'd only use it for *shape* — when
the knee arrives — never for level. That's why humanoid is scenario-bounded everywhere in the
report rather than forecast.

**Q. What would you do differently?**
Ask for data access in Week 1 instead of Week 9. I built the synthetic warehouse as a workaround and
it was the right call — it's the most reusable thing in the repo — but I should have made the ask
much earlier, while there was still time to act on the answer.

**Q. What are you proudest of?**
Two things. The Week 11 finding that the alert problem is solved by persistence, not by a better
threshold — that came from refusing to accept a metric that looked fine and asking what an operator
actually experiences. And the fact that every week says plainly what it couldn't do.

---

## Feedback received

*(To be filled in verbatim during the session.)*

| # | From | Feedback | Type | My response | Action |
|---|---|---|---|---|---|
| | | | | | |

---

## Actions arising

*(To be filled in after the session.)*

| # | Action | Owner | Due | Status |
|---|---|---|---|---|
| | | | | |

---

## Prior feedback carried forward

From supervisor reviews across Weeks 1–12 (recorded in each week's `status.md` and the mid-internship review):

| Week | Feedback | How it was addressed |
|---|---|---|
| 1–4 | "Well structured" · "Good stuff" — approach and phase-1 foundation endorsed | Kept the structure: plan → code → data → report → status, per week |
| 9 | Mid-internship review: predictive modelling, forecasting and anomaly detection identified as the most valuable skills to emphasise | Phase 4 leaned into exactly those — Weeks 10, 11 and 12 are the deepest modules in the repo |
| 9 | Recommendation letter, background check and employment verification offered | Noted with thanks; to follow up after closure |
| Ongoing | Use the internal "Trouble" system for questions | Used for the Week 9 data-access request |

---

*Ziheng Wang · Week 13 · to be updated immediately after the review session.*
