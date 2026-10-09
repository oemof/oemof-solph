# SPDX-FileCopyrightText: oemof e.V. and contributors

# -*- coding: utf-8 -

"""Basic tests.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/basic_tests.py

SPDX-License-Identifier: MIT
"""

import pandas as pd
import pytest

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


def test_infeasible_cbc_returns_solver_metadata():
    """CBC returns solver metadata when non-optimal results are allowed."""
    m = solph.Model(_make_infeasible_es())
    with pytest.warns(UserWarning):
        result = m.solve(solver="cbc", allow_nonoptimal=True)
    assert isinstance(result, dict)
    assert result["termination_condition"] == "infeasible"


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
# Coverage additions: Model.__init__ branches
# ---------------------------------------------------------------------------


def test_constraint_groups_explicitly_passed_skips_default_init():
    """Passing a non-None `constraint_groups` must skip the
    `constraint_groups = []` fallback assignment (branch 195->198)."""
    es = _make_feasible_es()
    model = solph.Model(es, constraint_groups=[])

    # default CONSTRAINT_GROUPS must still be the prefix of the combined list
    assert (
        model._constraint_groups[: len(solph.Model.CONSTRAINT_GROUPS)]
        == solph.Model.CONSTRAINT_GROUPS
    )


def test_auto_construct_false_skips_construction():
    """auto_construct=False must skip the automatic `_construct()` call
    (branch 214->216)."""
    es = _make_feasible_es()
    model = solph.Model(es, auto_construct=False)

    assert not hasattr(model, "objective")

    # Manual, sequential construction (as documented) still works.
    model._add_parent_block_sets()
    model._add_parent_block_variables()
    model._add_child_blocks()
    model._add_objective()

    assert hasattr(model, "objective")


# ---------------------------------------------------------------------------
# Coverage additions: bidirectional + (non)convex flow variable bounds
# ---------------------------------------------------------------------------


def test_bidirectional_nonconvex_flow_with_capacity_skips_lower_bound():
    """A flow with nominal_capacity, no fix, nonconvex=True and
    bidirectional=True must *not* get an explicit lower bound set
    (branch 412->388)."""
    es = solph.EnergySystem(timeindex=[0, 1], infer_last_interval=False)
    bus = solph.buses.Bus(label="bus")
    es.add(bus)
    es.add(
        solph.components.Sink(
            label="sink",
            inputs={
                bus: solph.flows.Flow(
                    nominal_capacity=10,
                    bidirectional=True,
                    nonconvex=solph.NonConvex(),
                )
            },
        )
    )

    model = solph.Model(es, auto_construct=False)
    model._add_parent_block_sets()
    model._add_parent_block_variables()

    key = next(iter(model.FLOWS))
    assert key in model.BIDIRECTIONAL_FLOWS

    flow_var = model.flow[key[0], key[1], 0]
    assert flow_var.lb is None


def test_bidirectional_flow_without_capacity_skips_lower_bound():
    """A bidirectional flow without nominal_capacity must *not* get an
    explicit lower bound of 0 set (branch 417->388)."""
    es = solph.EnergySystem(timeindex=[0, 1], infer_last_interval=False)
    bus = solph.buses.Bus(label="bus")
    es.add(bus)
    es.add(
        solph.components.Sink(
            label="sink",
            inputs={bus: solph.flows.Flow(bidirectional=True)},
        )
    )

    model = solph.Model(es, auto_construct=False)
    model._add_parent_block_sets()
    model._add_parent_block_variables()

    key = next(iter(model.FLOWS))
    assert key in model.BIDIRECTIONAL_FLOWS

    flow_var = model.flow[key[0], key[1], 0]
    assert flow_var.lb is None


# ---------------------------------------------------------------------------
# Coverage additions: _add_objective(update=True)
# ---------------------------------------------------------------------------


def test_add_objective_update_replaces_existing_objective():
    """Calling `_add_objective(update=True)` must delete the existing
    'objective' component before re-adding it (line 443)."""
    es = _make_feasible_es()
    model = solph.Model(es, auto_construct=False)
    model._add_parent_block_sets()
    model._add_parent_block_variables()
    model._add_objective()

    first_objective_id = id(model.objective)

    model._add_objective(update=True)

    assert hasattr(model, "objective")
    assert id(model.objective) != first_objective_id


# ---------------------------------------------------------------------------
# Coverage additions: receive_duals() deprecated wrapper
# ---------------------------------------------------------------------------


def test_receive_duals_deprecated_method_sets_suffixes():
    """The deprecated `receive_duals()` method must warn and delegate to
    `_receive_duals()` (lines 454-459)."""
    es = _make_feasible_es()
    model = solph.Model(es)

    with pytest.warns(FutureWarning, match="receive_duals"):
        model.receive_duals()

    assert model.dual is not None
    assert model.rc is not None


def test_receive_duals_can_be_called_multiple_times():
    """Calling `_receive_duals()` a second time must not try to `del` an
    unset suffix, i.e. the `is None` checks must evaluate to False on the
    second call (branches 466->468 and 470->472)."""
    es = _make_feasible_es()
    model = solph.Model(es)

    model._receive_duals()
    first_dual = model.dual
    first_rc = model.rc

    # Second call: self.dual / self.rc are already set (not None).
    model._receive_duals()

    assert model.dual is not None
    assert model.rc is not None
    assert model.dual is not first_dual
    assert model.rc is not first_rc


# ---------------------------------------------------------------------------
# Coverage additions: relax_problem()
# ---------------------------------------------------------------------------


def test_relax_problem_returns_self():
    """`relax_problem()` must apply the relaxation transformation and
    return the model instance itself (lines 681-682)."""
    es = _make_mip_es()
    model = solph.Model(es)

    relaxed = model.relax_problem()

    assert relaxed is model
