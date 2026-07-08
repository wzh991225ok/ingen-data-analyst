"""Week 10 — Bass diffusion model for humanoid robot adoption.

Anchored to publicly stated shipment guidance (cited):
  - Goldman Sachs Research (Jan 2024): ~20,000 humanoid shipments in 2025; base case > 250,000 in
    2030; ~1.4 million units annually by 2035 (~70% CAGR). TAM $38B by 2035.
    Source: goldmansachs.com/insights/articles/the-global-market-for-robots-could-reach-38-billion-by-2035
  - Morgan Stanley (Apr 2025): ~13 million humanoids in service by 2035 (installed base).
    Used as an upper-scenario cross-check only.

Approach: fit the Bass cumulative-adoption curve N(t) to the Goldman ANNUAL-shipment anchors, then
report annual shipments (the derivative) and cumulative installed base through 2035. Bass params:
  p = coefficient of innovation, q = coefficient of imitation, M = ultimate market potential (units).

Bass cumulative fraction F(t) = (1 - e^-(p+q)t) / (1 + (q/p) e^-(p+q)t).
Annual shipments ~ M * f(t) where f = dF/dt.
"""
from __future__ import annotations
import numpy as np
from scipy.optimize import curve_fit

# Cited anchors: (calendar_year, annual_shipments_units)
GOLDMAN_ANCHORS = {2025: 20_000, 2030: 250_000, 2035: 1_400_000}
T0 = 2025  # t=0 at 2025


def bass_F(t, p, q):
    e = np.exp(-(p + q) * t)
    return (1 - e) / (1 + (q / p) * e)


def bass_f(t, p, q):
    """pdf (adoption rate) = dF/dt."""
    e = np.exp(-(p + q) * t)
    num = (p + q) ** 2 * e
    den = p * (1 + (q / p) * e) ** 2
    return num / den


def fit_bass():
    """Fit p, q, M to the Goldman annual-shipment anchors in LOG space, so all three anchors
    (which span 20k -> 1.4M) get proportional weight rather than the largest dominating."""
    years = np.array(sorted(GOLDMAN_ANCHORS))
    t = (years - T0).astype(float)
    log_ship = np.log(np.array([GOLDMAN_ANCHORS[y] for y in years], float))

    def log_model(t, p, q, M):
        return np.log(np.clip(M * bass_f(t, p, q), 1e-6, None))

    p0 = [0.01, 0.6, 8_000_000]
    bounds = ([1e-4, 1e-3, 1_000_000], [0.5, 1.5, 60_000_000])
    popt, _ = curve_fit(log_model, t, log_ship, p0=p0, bounds=bounds, maxfev=40000)
    return popt  # p, q, M


def project(years_out=list(range(2025, 2036))):
    p, q, M = fit_bass()
    out = []
    for y in years_out:
        t = y - T0
        annual = M * bass_f(t, p, q)
        cum = M * bass_F(t, p, q)
        out.append({"year": y, "annual_shipments": round(annual),
                    "cumulative_installed": round(cum)})
    return {"p": float(p), "q": float(q), "M": float(M)}, out


if __name__ == "__main__":
    params, rows = project()
    print(f"Bass fit: p={params['p']:.4f}  q={params['q']:.3f}  M={params['M']:,.0f}")
    print(f"{'year':>6} {'annual':>12} {'cumulative':>14}   anchor")
    for r in rows:
        a = GOLDMAN_ANCHORS.get(r["year"], "")
        anchor = f"GS {a:,}" if a else ""
        print(f"{r['year']:>6} {r['annual_shipments']:>12,} {r['cumulative_installed']:>14,}   {anchor}")
