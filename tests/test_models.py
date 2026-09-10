# -*- coding: utf-8 -

"""Basic tests.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/basic_tests.py

SPDX-License-Identifier: MIT
"""

import warnings

import pandas as pd
import pytest
from pyomo.opt.results import SolverResults

from oemof import solph
from oemof.solph._results import Results

# ---------------------------------------------------------------------------
# Shared energy-system factories
# ---------------------------------------------------------------------------


def _make_infeasible_es():
    """Source capacity (4) < sink demand (5) → infeasible."""
    es = solph.EnergySystem(timeindex=[0, 1], infer_last_interval=False)
    bus = solph.buses.Bus(label="bus")
    es.add(bus)
    es.add(
        solph.components.Sink(
            inputs={bus: solph.flows.Flow(nominal_capacity=5, fix=[1])}
        )
    )
    es.add(
        solph.components.Source(
            outputs={
                bus: solph.flows.Flow(nominal_capacity=4, variable_costs=5)
            }
        )
    )
    return es


def _make_unbounded_es():
    """Negative variable cost with no upper bound → unbounded."""
    es = solph.EnergySystem(timeindex=[0, 1], infer_last_interval=False)
    bus = solph.buses.Bus(label="bus")
    es.add(bus)
    es.add(solph.components.Sink(inputs={bus: solph.flows.Flow()}))
    es.add(
        solph.components.Source(
            outputs={bus: solph.flows.Flow(variable_costs=-5)}
        )
    )
    return es


def _make_feasible_es():
    """Simple LP: one source, one fixed-demand sink."""
    es = solph.EnergySystem(timeindex=[0, 1, 2], infer_last_interval=False)
    bus = solph.buses.Bus(label="bus")
    es.add(bus)
    es.add(
        solph.components.Source(
            label="source",
            outputs={
                bus: solph.flows.Flow(variable_costs=10, nominal_capacity=100)
            },
        )
    )
    es.add(
        solph.components.Sink(
            label="sink",
            inputs={
                bus: solph.flows.Flow(
                    fix=[0.5, 0.8, 0.3], nominal_capacity=100
                )
            },
        )
    )
    return es


def _make_mip_es():
    """Same as feasible LP but with a NonConvex flow → MIP."""
    es = solph.EnergySystem(timeindex=[0, 1, 2], infer_last_interval=False)
    bus = solph.buses.Bus(label="bus")
    es.add(bus)
    es.add(
        solph.components.Source(
            label="source",
            outputs={
                bus: solph.flows.Flow(
                    variable_costs=10,
                    nominal_capacity=100,
                    nonconvex=solph.NonConvex(),
                )
            },
        )
    )
    es.add(
        solph.components.Sink(
            label="sink",
            inputs={
                bus: solph.flows.Flow(
                    fix=[0.5, 0.8, 0.3], nominal_capacity=100
                )
            },
        )
    )
    return es


# ---------------------------------------------------------------------------
# Parametrized: CBC and HiGHS must behave identically
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("solver", ["cbc", "highs"])
def test_feasible_returns_results(solver):
    """A feasible model must return a solph.Results object for any solver."""
    result = solph.Model(_make_feasible_es()).solve(solver=solver)
    assert isinstance(result, Results)


@pytest.mark.parametrize("solver", ["cbc", "highs"])
def test_infeasible_warns_when_nonoptimal_allowed(solver):
    """allow_nonoptimal=True must issue a UserWarning for any solver."""
    m = solph.Model(_make_infeasible_es())
    with pytest.warns(
        UserWarning, match="The solver did not return an optimal solution"
    ):
        m.solve(solver=solver, allow_nonoptimal=True)


def test_infeasible_cbc_returns_solver_results():
    """CBC specifically returns a SolverResults object when non-optimal."""
    m = solph.Model(_make_infeasible_es())
    with pytest.warns(UserWarning):
        result = m.solve(solver="cbc", allow_nonoptimal=True)
    assert isinstance(result, SolverResults)


@pytest.mark.parametrize("solver", ["cbc", "highs"])
def test_infeasible_raises_by_default(solver):
    """
    allow_nonoptimal=False (default) must raise RuntimeError for any solver.
    """
    m = solph.Model(_make_infeasible_es())
    with pytest.raises(
        RuntimeError, match="The solver did not return an optimal solution"
    ):
        m.solve(solver=solver, allow_nonoptimal=False)


@pytest.mark.parametrize("solver", ["cbc", "highs"])
def test_unbounded_raises(solver):
    """An unbounded model must raise RuntimeError for any solver."""
    m = solph.Model(_make_unbounded_es())
    with pytest.raises(
        RuntimeError, match="The solver did not return an optimal solution"
    ):
        m.solve(solver=solver)


# ---------------------------------------------------------------------------
# Cross-validation: HiGHS and CBC must agree on numerics
# ---------------------------------------------------------------------------


def test_highs_objective_matches_cbc():
    es = _make_feasible_es()
    r_highs = solph.Model(es).solve(solver="highs")
    r_cbc = solph.Model(es).solve(solver="cbc")
    assert r_highs["objective"] == pytest.approx(r_cbc["objective"])


def test_highs_flow_values_match_cbc():
    es = _make_feasible_es()
    r_highs = solph.Model(es).solve(solver="highs")
    r_cbc = solph.Model(es).solve(solver="cbc")
    pd.testing.assert_frame_equal(
        r_highs.get("flow").sort_index(axis=1),
        r_cbc.get("flow").sort_index(axis=1),
    )


@pytest.mark.skip(
    reason="Handling of duals in new Results object is not yet implemented"
)
def test_highs_duals_match_cbc():
    es = _make_feasible_es()

    m_highs = solph.Model(es)
    m_highs.receive_duals()
    m_highs.solve(solver="highs")

    m_cbc = solph.Model(es)
    m_cbc.receive_duals()
    m_cbc.solve(solver="cbc")

    highs_duals = {str(c): v for c, v in m_highs.dual.items()}
    cbc_duals = {str(c): v for c, v in m_cbc.dual.items()}

    assert highs_duals.keys() == cbc_duals.keys()
    for key in highs_duals:
        assert highs_duals[key] == pytest.approx(cbc_duals[key], abs=1e-6)


@pytest.mark.skip(
    reason="Handling of reduced cost in new Results object is not yet "
           "implemented"
)
def test_highs_reduced_costs_match_cbc():
    """Reduced costs match CBC for variables both solvers report.

    HiGHS omits RC for fixed-bound variables while CBC includes them,
    so we only assert equality on the intersection.
    """
    es = _make_feasible_es()

    m_highs = solph.Model(es)
    m_highs.receive_duals()
    m_highs.solve(solver="highs")

    m_cbc = solph.Model(es)
    m_cbc.receive_duals()
    m_cbc.solve(solver="cbc")

    highs_rc = {str(v): val for v, val in m_highs.rc.items()}
    cbc_rc = {str(v): val for v, val in m_cbc.rc.items()}

    common_keys = highs_rc.keys() & cbc_rc.keys()
    assert len(common_keys) > 0, "No common RC variables to compare"
    for key in common_keys:
        assert highs_rc[key] == pytest.approx(cbc_rc[key], abs=1e-6)


@pytest.mark.parametrize("solver", ["cbc", "highs"])
def test_receive_duals_on_mip_does_not_crash(solver):
    """receive_duals() followed by solve must not crash for MIP models."""
    m = solph.Model(_make_mip_es())
    m.receive_duals()
    m.solve(solver=solver)


# ---------------------------------------------------------------------------
# Solver-specific: command-line options are forwarded correctly
# ---------------------------------------------------------------------------


def test_cbc_cmdline_options(capsys):
    """CBC echoes command-line options in its solver output."""
    es = solph.EnergySystem(timeindex=[0, 1], infer_last_interval=False)
    bel = solph.buses.Bus(label="bus")
    es.add(bel)
    # bound Sink
    es.add(
        solph.components.Sink(
            inputs={bel: solph.flows.Flow(nominal_capacity=4)}
        )
    )

    # Source with a revenue
    es.add(
        solph.components.Source(
            outputs={bel: solph.flows.Flow(variable_costs=-5)}
        )
    )
    m = solph.Model(es)

    m.solve(
        solver="cbc",
        cmdline_options={"ratio": 0.01},
        solve_kwargs={"tee": True},
    )

    captured = capsys.readouterr()
    assert "-ratio 0.01" in captured.out


def test_highs_cmdline_options(capsys):
    """HiGHS options passed via cmdline_options are applied to the solver."""
    m = solph.Model(_make_feasible_es())

    m.solve(
        solver="highs",
        cmdline_options={"presolve": "off"},
        solve_kwargs={"tee": True},
    )

    captured = capsys.readouterr()
    assert "without presolve" in captured.out


# ---------------------------------------------------------------------------
# Multi-period
# ---------------------------------------------------------------------------


@pytest.mark.filterwarnings(
    "ignore:Ensure that your timeindex and timeincrement are"
    " consistent.:UserWarning"
)
@pytest.mark.filterwarnings(
    "ignore:CAUTION! You specified the 'periods' attribute:UserWarning"
)
def test_multi_period_default_discount_rate():
    """Test error being thrown for default multi-period discount rate"""
    timeindex = pd.date_range(start="2017-01-01", periods=100, freq="D")
    es = solph.EnergySystem(
        timeindex=timeindex,
        timeincrement=[1] * len(timeindex),
        periods=[timeindex],
        infer_last_interval=False,
    )
    bel = solph.buses.Bus(label="bus")
    es.add(bel)
    es.add(
        solph.components.Sink(
            label="sink",
            inputs={
                bel: solph.flows.Flow(
                    nominal_capacity=5, fix=[1] * len(timeindex)
                )
            },
        )
    )
    es.add(
        solph.components.Source(
            label="source",
            outputs={
                bel: solph.flows.Flow(nominal_capacity=4, variable_costs=5)
            },
        )
    )
    msg = (
        "By default, a discount_rate of 0.02 is used for a multi-period model."
    )
    with warnings.catch_warnings(record=True) as w:
        solph.Model(es)
        assert msg in str(w[0].message)
