"""Tests for Week 12 process analytics.

Run: python -m pytest src/process/tests -q
Requires the Week 7 warehouse (path via WEEK7_DB env var, or the default location).
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import pytest

from src.process.process_model import (SupportProcess, Ticket, TEAMS_BASELINE, STAGE_TEAM,
                                       DISPATCH_P, SEVERITY_PRIORITY)
from src.process import stage_generator as sg
from src.process.cycle_time import decompose


@pytest.fixture(scope="module")
def generated():
    ev, cycle = sg.build()
    return ev, cycle


# ---------------------------------------------------------------- schema reconciliation
def test_process_map_reconciles_to_week7_schema(generated):
    """Success criterion: the process map is verifiable against the synthetic data schema."""
    ev, cycle = generated
    checks = sg.verify(ev, cycle)
    for name, passed in checks.items():
        assert passed, f"reconciliation failed: {name}"


def test_stage_durations_sum_exactly_to_cycle_time(generated):
    ev, cycle = generated
    ev = ev.copy()
    ev["stage_hours"] = ev["wait_hours"] + ev["service_hours"]
    recomputed = ev.groupby("ticket_key")["stage_hours"].sum().round(4)
    stated = cycle.set_index("ticket_key")["cycle_time_hours"].round(4)
    assert np.allclose(recomputed.reindex(stated.index).to_numpy(), stated.to_numpy(), atol=1e-3)


def test_every_stage_maps_to_a_known_team(generated):
    ev, _ = generated
    staffed = ev[~ev["team"].isin(["(automated)", "(unstaffed wait)"])]
    assert set(staffed["team"]).issubset(set(TEAMS_BASELINE))
    for stage, team in STAGE_TEAM.items():
        rows = ev[ev["stage"] == stage]
        if len(rows):
            assert set(rows["team"]) == {team}, f"{stage} should be served by {team}"


# ---------------------------------------------------------------- model behaviour
def test_parts_wait_consumes_no_staff_time(generated):
    """Parts & dispatch is an unstaffed wait — that's why headcount can't fix it."""
    ev, _ = generated
    parts = ev[ev["stage"] == "Parts & dispatch"]
    assert len(parts) > 0
    assert (parts["service_hours"] == 0).all()
    assert (parts["wait_hours"] > 0).all()


def test_only_dispatched_tickets_get_field_stages(generated):
    ev, cycle = generated
    dispatched = set(ev.loc[ev["stage"] == "Parts & dispatch", "ticket_key"])
    repaired = set(ev.loc[ev["stage"] == "On-site repair", "ticket_key"])
    assert repaired == dispatched      # on-site repair happens iff a part was needed


def test_dispatch_rate_follows_category_probabilities(generated):
    """Observed dispatch rate per category should track the documented DISPATCH_P."""
    ev, cycle = generated
    disp = cycle.groupby("category")["dispatched"].mean()
    for cat, p in DISPATCH_P.items():
        if cat in disp.index:
            assert abs(disp[cat] - p) < 0.08, f"{cat}: observed {disp[cat]:.2f} vs documented {p}"


def test_critical_tickets_clear_faster_than_low(generated):
    _, cycle = generated
    med = cycle.groupby("severity")["cycle_time_hours"].median()
    assert med["Critical"] < med["Low"], "priority + service multipliers should favour Critical"


def test_severity_priority_ordering_is_sane():
    assert SEVERITY_PRIORITY["Critical"] < SEVERITY_PRIORITY["High"] < SEVERITY_PRIORITY["Medium"] < SEVERITY_PRIORITY["Low"]


# ---------------------------------------------------------------- analysis layer
def test_decomposition_percentages_sum_to_100(generated):
    ev, _ = generated
    ev = ev.copy(); ev["stage_hours"] = ev["wait_hours"] + ev["service_hours"]
    dec = decompose(ev)
    assert abs(dec["pct_of_total"].sum() - 100) < 0.5
    assert abs(dec["cumulative_pct"].iloc[-1] - 100) < 0.5
    assert dec["total_hours"].is_monotonic_decreasing   # Pareto order


def test_simulation_is_reproducible():
    """Same seed -> identical results (success criterion: simulation runs reproducibly)."""
    tickets = [Ticket(i, f"TKT-{i:04d}", float(i * 3), "Medium", "mechanical", "Fari", "Europe")
               for i in range(60)]
    a = pd.DataFrame(SupportProcess(tickets, seed=7).run())
    b = pd.DataFrame(SupportProcess([Ticket(i, f"TKT-{i:04d}", float(i * 3), "Medium", "mechanical",
                                            "Fari", "Europe") for i in range(60)], seed=7).run())
    pd.testing.assert_frame_equal(a, b)


def test_more_field_capacity_reduces_field_wait():
    """Adding capacity to a queueing stage must not increase its wait — a sanity check on the model."""
    tickets = [Ticket(i, f"TKT-{i:04d}", float(i * 0.4), "Medium", "mechanical", "Aido Rover", "Europe")
               for i in range(220)]
    base = pd.DataFrame(SupportProcess(tickets, seed=3).run())
    more = pd.DataFrame(SupportProcess(
        [Ticket(i, f"TKT-{i:04d}", float(i * 0.4), "Medium", "mechanical", "Aido Rover", "Europe")
         for i in range(220)],
        teams={**TEAMS_BASELINE, "Field Ops": TEAMS_BASELINE["Field Ops"] + 2}, seed=3).run())
    w_base = base.loc[base["stage"] == "On-site repair", "wait_hours"].mean()
    w_more = more.loc[more["stage"] == "On-site repair", "wait_hours"].mean()
    assert w_more <= w_base + 1e-6


def test_parts_buffer_reduces_parts_wait():
    """The parts-buffer lever must actually shorten parts lead time in the buffered regions."""
    mk = lambda: [Ticket(i, f"TKT-{i:04d}", float(i * 2), "Medium", "mechanical", "Fari", "APAC")
                  for i in range(120)]
    base = pd.DataFrame(SupportProcess(mk(), seed=11).run())
    buf = pd.DataFrame(SupportProcess(mk(), parts_buffer_regions=("APAC",), seed=11).run())
    assert (buf.loc[buf["stage"] == "Parts & dispatch", "wait_hours"].mean()
            < base.loc[base["stage"] == "Parts & dispatch", "wait_hours"].mean())
