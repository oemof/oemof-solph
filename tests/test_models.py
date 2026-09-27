# SPDX-FileCopyrightText: oemof e.V. and contributors

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
    """Source capacity (4) < sink demand (5) -> infeasible."""
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
    """Negative variable cost with no upper bound -> unbounded."""
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
                    minimum=[0.5, 0.8, 0.3], nominal_capacity=100
                )
            },
        )
    )
    return es


def _make_mip_es():
    """Same as feasible LP but with a NonConvex flow -> MIP."""
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
                    minimum=[0.5, 0.8, 0.3], nominal_capacity=100
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
    assert r_highs.solver.objective == pytest.approx(r_cbc.solver.objective)


def test_highs_flow_values_match_cbc():
    es = _make_feasible_es()
    r_highs = solph.Model(es).solve(solver="highs")
    r_cbc = solph.Model(es).solve(solver="cbc")
    pd.testing.assert_frame_equal(
        r_highs.get("flow").sort_index(axis=1),
        r_cbc.get("flow").sort_index(axis=1),
    )


def test_highs_duals_match_cbc():
    """Dual values (shadow prices) must match between CBC and HiGHS."""
    es = _make_feasible_es()

    r_highs = solph.Model(es).solve(solver="highs", duals=True)
    r_cbc = solph.Model(es).solve(solver="cbc", duals=True)

    highs_duals = r_highs.get("duals")
    cbc_duals = r_cbc.get("duals")

    assert highs_duals is not None
    assert cbc_duals is not None
    pd.testing.assert_frame_equal(
        highs_duals.sort_index(axis=1),
        cbc_duals.sort_index(axis=1),
    )


def test_highs_reduced_costs_match_cbc():
    """Reduced costs match CBC for variables both solvers report.

    HiGHS omits RC for fixed-bound variables while CBC includes them,
    so we only assert equality on the intersection.
    """
    es = _make_feasible_es()

    r_highs = solph.Model(es).solve(solver="highs", duals=True)
    r_cbc = solph.Model(es).solve(solver="cbc", duals=True)

    highs_rc = r_highs.get("reduced_costs")
    cbc_rc = r_cbc.get("reduced_costs")

    assert highs_rc is not None
    assert cbc_rc is not None

    common_cols = highs_rc.columns.intersection(cbc_rc.columns)
    assert len(common_cols) > 0, "No common RC variables to compare"

    pd.testing.assert_frame_equal(
        highs_rc[common_cols].sort_index(axis=1),
        cbc_rc[common_cols].sort_index(axis=1),
        check_exact=False,
        atol=1e-6,
    )


@pytest.mark.filterwarnings("ignore:Could not extract")
@pytest.mark.parametrize("solver", ["cbc", "highs"])
def test_receive_duals_on_mip_does_not_crash(solver):
    """duals=True on a MIP model must not crash (no duals for MIP,
    but reduced_costs may still be requested without error)."""
    m = solph.Model(_make_mip_es())
    m.solve(solver=solver, duals=True)


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


# ---------------------------------------------------------------------------
# Duals / reduced costs are optional (only populated if requested)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("solver", ["cbc", "highs"])
def test_duals_none_when_not_requested(solver):
    """Without duals=True, both 'duals' and 'reduced_costs' must be None."""
    result = solph.Model(_make_feasible_es()).solve(solver=solver)
    assert result.get("duals") is None
    assert result.get("reduced_costs") is None


@pytest.mark.parametrize("solver", ["cbc", "highs"])
def test_duals_keys_absent_when_not_requested(solver):
    """'duals'/'reduced_costs' must not appear in keys() if not requested."""
    result = solph.Model(_make_feasible_es()).solve(solver=solver)
    assert "duals" not in result.keys()
    assert "reduced_costs" not in result.keys()


@pytest.mark.parametrize("solver", ["cbc", "highs"])
def test_duals_keys_present_when_requested(solver):
    """'duals'/'reduced_costs' must appear in keys() once requested."""
    result = solph.Model(_make_feasible_es()).solve(solver=solver, duals=True)
    assert "duals" in result.keys()
    assert "reduced_costs" in result.keys()


def test_results_get_custom_default_for_missing_duals():
    """Results.get() must honor a custom default, not just None."""
    result = solph.Model(_make_feasible_es()).solve(solver="cbc")
    sentinel = object()
    assert result.get("duals", sentinel) is sentinel
    assert result.get("reduced_costs", sentinel) is sentinel


def test_extract_suffix_dataframe_nan_for_missing_entry():
    """_extract_suffix_dataframe must return NaN (not raise KeyError)
    for components missing from the suffix dict -- this happens when
    a solver's presolve eliminates a variable/constraint before
    reporting duals/reduced costs."""
    result = solph.Model(_make_feasible_es()).solve(solver="cbc", duals=True)

    class _EmptySuffix(dict):
        def get(self, key, default=None):
            return default  # simulate: nothing reported by the solver

    df = result._extract_suffix_dataframe(
        _EmptySuffix(),
        grouped_components={"some_key": [object(), object()]},
    )
    assert df["some_key"].isna().all()


# ---------------------------------------------------------------------------
# Deprecated receive_duals() must still work (no infinite recursion)
# ---------------------------------------------------------------------------

def test_receive_duals_deprecated_still_populates_duals():
    """receive_duals() is deprecated but must still enable dual extraction."""
    m = solph.Model(_make_feasible_es())
    with pytest.warns(FutureWarning, match="deprecated"):
        m.receive_duals()

    result = m.solve(solver="cbc")
    assert result.get("duals") is not None
    assert result.get("reduced_costs") is not None


def test_receive_duals_on_mip_highs_warns():
    """duals=True on a MIP model must not crash, but should warn."""
    m = solph.Model(_make_mip_es())
    with pytest.warns(UserWarning, match="MIP"):
        m.solve(solver="highs", duals=True)
