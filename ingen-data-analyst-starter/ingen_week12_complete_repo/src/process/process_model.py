"""Week 12 — discrete-event model of the InGen support-ticket lifecycle.

ONE process model, used twice:
  1. as the BASELINE generator — replaying Week 7's real ticket arrival stream through it to
     produce stage-level events the Week 7 warehouse doesn't carry;
  2. as the COUNTERFACTUAL engine — re-running with an operational change to quantify its effect.

That is how discrete-event simulation is meant to be used: calibrate a model of the observed
process, then ask "what if". The deltas it produces are properties of THIS model, not measured
facts about InGen's support org — see the memo's limitations section.

Why the Week 7 warehouse had to be extended
-------------------------------------------
fact_support_tickets carries opened/closed dates, severity, category, product, geography and a
single resolution_hours total. It has no stages, no team, and no workload — all three of which the
Week 12 brief requires. Rather than inventing a parallel dataset, this model REPLAYS the real Week 7
tickets (same ticket_id, opened date, severity, category, product, geography) and adds only the
lifecycle layer. Every generated row therefore joins 1:1 back to a real Week 7 ticket_key.

Process (support-ticket lifecycle for a fleet robot, e.g. a Fari unit)
----------------------------------------------------------------------
    Intake -> Triage (Tier 1) -> Remote diagnosis (Tier 2)
           -> [ Parts & dispatch (wait, not staffed) -> On-site repair (Field Ops) ]   (if needed)
           -> Verification & closure (Tier 1)

Two structurally different delays are modelled on purpose, because they need different fixes:
  * QUEUEING delay  — waiting for a person on a finite team. Fixed with headcount/routing.
  * PARTS LEAD TIME — waiting for a physical part. Consumes no FTE, so headcount cannot fix it.

Severity drives queue priority (Critical first). All randomness flows through a seeded generator.
"""
from __future__ import annotations
from dataclasses import dataclass, field

import numpy as np
import simpy

SEED = 20260710

# ---------------------------------------------------------------- documented parameters
# Team capacity (FTE, follow-the-sun continuous cover). Sized to the observed Week 7 arrival rate
# (~6.8 tickets/day) at a realistic ~50-60% utilisation — Week 7 carries no team data, so these are
# a documented modelling choice, not an observed fact. Sensitivity to this choice is in the memo.
TEAMS_BASELINE = {"Tier 1": 1, "Tier 2": 2, "Field Ops": 1}

# Median service hours per stage (lognormal). sigma is the log-scale spread.
SERVICE = {
    "Triage":            {"median": 0.5,  "sigma": 0.5},
    "Remote diagnosis":  {"median": 3.0,  "sigma": 0.8},
    "On-site repair":    {"median": 4.0,  "sigma": 0.6},
    "Verification":      {"median": 1.0,  "sigma": 0.5},
}
STAGE_TEAM = {"Triage": "Tier 1", "Remote diagnosis": "Tier 2",
              "On-site repair": "Field Ops", "Verification": "Tier 1"}

# Parts lead time (hours) — a pure wait, consumes no FTE. Long right tail on purpose.
PARTS_LEAD = {"median": 20.0, "sigma": 0.9}

# P(a physical part / site visit is required) by ticket category.
DISPATCH_P = {"mechanical": 0.75, "battery": 0.60, "navigation": 0.35,
              "connectivity": 0.15, "software": 0.05}

# Severity: queue priority (lower = served first) and a service-speed multiplier
# (Critical work is done faster because it gets the senior engineer and full attention).
SEVERITY_PRIORITY = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
SEVERITY_SERVICE_MULT = {"Critical": 0.55, "High": 0.8, "Medium": 1.0, "Low": 1.15}

# Regional parts-logistics multiplier on parts lead time.
REGION_PARTS_MULT = {"North America": 1.0, "Europe": 1.25, "APAC": 1.5}

# Products needing more field time (bigger, more mechanical machines).
PRODUCT_REPAIR_MULT = {"Aido Humanoid": 1.5, "Aido Rover": 1.35, "Sentinel Prime AI": 1.1,
                       "Fari": 1.0, "Senpai": 0.85}


def _lognormal(rng, median, sigma, mult=1.0):
    """Lognormal draw with the given median (hours), scaled by mult."""
    return float(rng.lognormal(mean=np.log(median * mult), sigma=sigma))


@dataclass
class Ticket:
    ticket_key: int
    ticket_id: str
    arrival_h: float          # hours since sim epoch
    severity: str
    category: str
    product: str
    region: str
    events: list = field(default_factory=list)


class SupportProcess:
    """The simpy model. `teams` maps team name -> FTE count."""

    def __init__(self, tickets, teams=None, reroute_low_severity=False,
                 parts_buffer_regions=(), seed=SEED):
        self.tickets = tickets
        self.teams_cfg = dict(teams or TEAMS_BASELINE)
        self.reroute_low_severity = reroute_low_severity      # scenario B lever
        self.parts_buffer_regions = set(parts_buffer_regions)  # scenario C lever
        self.rng = np.random.default_rng(seed)
        self.rows = []

    # -------------------------------------------------- stages
    def _serve(self, env, resources, stage, tk):
        """Queue for the stage's team, then serve. Records wait and service separately."""
        team = STAGE_TEAM[stage]
        enter = env.now
        prio = SEVERITY_PRIORITY[tk.severity]
        with resources[team].request(priority=prio) as req:
            yield req
            start = env.now
            spec = SERVICE[stage]
            mult = SEVERITY_SERVICE_MULT[tk.severity]
            if stage == "On-site repair":
                mult *= PRODUCT_REPAIR_MULT.get(tk.product, 1.0)
            dur = _lognormal(self.rng, spec["median"], spec["sigma"], mult)
            yield env.timeout(dur)
            self.rows.append({
                "ticket_key": tk.ticket_key, "ticket_id": tk.ticket_id, "stage": stage,
                "team": team, "enter_h": enter, "start_h": start, "exit_h": env.now,
                "wait_hours": round(start - enter, 4), "service_hours": round(dur, 4),
                "queue_len_on_entry": len(resources[team].queue),
            })

    def _parts_wait(self, env, tk):
        """Parts lead time: a wait, not staffed work. Headcount cannot shorten it."""
        enter = env.now
        mult = REGION_PARTS_MULT.get(tk.region, 1.0)
        if tk.region in self.parts_buffer_regions:
            mult *= 0.35        # a local parts buffer cuts the lead time
        dur = _lognormal(self.rng, PARTS_LEAD["median"], PARTS_LEAD["sigma"], mult)
        yield env.timeout(dur)
        self.rows.append({
            "ticket_key": tk.ticket_key, "ticket_id": tk.ticket_id, "stage": "Parts & dispatch",
            "team": "(unstaffed wait)", "enter_h": enter, "start_h": enter, "exit_h": env.now,
            "wait_hours": round(dur, 4), "service_hours": 0.0, "queue_len_on_entry": 0,
        })

    def _lifecycle(self, env, resources, tk):
        yield env.timeout(max(0.0, tk.arrival_h - env.now))
        # Intake is instantaneous (auto-acknowledged) — recorded for the process map completeness.
        self.rows.append({"ticket_key": tk.ticket_key, "ticket_id": tk.ticket_id, "stage": "Intake",
                          "team": "(automated)", "enter_h": env.now, "start_h": env.now,
                          "exit_h": env.now, "wait_hours": 0.0, "service_hours": 0.0,
                          "queue_len_on_entry": 0})
        # Scenario B: low-severity tickets skip human triage (self-service / auto-routing).
        skip_triage = self.reroute_low_severity and tk.severity == "Low"
        if not skip_triage:
            yield env.process(self._serve(env, resources, "Triage", tk))
        yield env.process(self._serve(env, resources, "Remote diagnosis", tk))
        needs_field = self.rng.random() < DISPATCH_P.get(tk.category, 0.2)
        if needs_field:
            yield env.process(self._parts_wait(env, tk))
            yield env.process(self._serve(env, resources, "On-site repair", tk))
        yield env.process(self._serve(env, resources, "Verification", tk))

    def run(self):
        env = simpy.Environment()
        resources = {name: simpy.PriorityResource(env, capacity=n)
                     for name, n in self.teams_cfg.items()}
        for tk in self.tickets:
            env.process(self._lifecycle(env, resources, tk))
        env.run()
        return self.rows
