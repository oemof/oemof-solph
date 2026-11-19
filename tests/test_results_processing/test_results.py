# SPDX-FileCopyrightText: oemof e.V. and contributors
#
# SPDX-License-Identifier: MIT

import pandas as pd
import pytest
from oemof.tools.debugging import ExperimentalFeatureWarning
from pyomo.opt.results.container import ListContainer

from oemof import solph
from oemof.solph._results import Results

from . import optimisation_results


class TestResultsClass:
    @classmethod
    def setup_class(cls):
        cls.results = optimisation_results

    def test_hasattr(self):
        assert hasattr(self.results, "_variables"), (
            '\nFailed testing `hasattr(results, "_variables")`, where'
            " `results` is a `Results` instance."
            '\nExpected: `hasattr(results, "_variables")`'
            '\nGot     : `not hasattr(results, "_variables")`'
        )
        assert not hasattr(self.results, "flow"), (
            '\nFailed testing `not hasattr(results, "flow")`, where'
            " `results` is a `Results` instance."
            '\nExpected: `not hasattr(results, "flow")`'
            '\nGot     : `hasattr(results, "flow")`'
        )

    def test_membership_checking(self):
        assert "flow" in self.results, (
            '\nFailed testing `"flow" in results`, where `results` is a'
            " `Results` instance."
            '\nExpected: `"flow" in results`'
            '\nGot     : `"flow" not in results`'
        )
        assert "" not in self.results, (
            '\nFailed testing `"" in results`, where `results` is a'
            " `Results` instance."
            '\nExpected: `"" not in results`'
            '\nGot     : `"" in results`'
        )

    def test_objective(self):
        assert self.results.solver.objective == pytest.approx(8495, abs=1)

    def test_get(self):
        flows = self.results.get("flow")
        assert isinstance(flows, pd.DataFrame)

    def test_get_default(self):
        rv = self.results.get("non_existing_key")
        assert rv is None

    def test_get_custom(self):
        rv = self.results.get("non_existing_key", 42)
        assert rv == 42

    def test_getitem(self):
        flows = self.results["flow"]
        assert isinstance(flows, pd.DataFrame)

    def test_to_getitem_fails(self):
        with pytest.raises(KeyError, match="not in Results"):
            self.results["non_existing_key"]

    def test_to_df_fails(self):
        with pytest.warns(FutureWarning):
            with pytest.raises(KeyError, match="not in Results"):
                self.results.to_df("non_existing_key")

    def test_to_df(self):
        with pytest.warns(FutureWarning, match="Results.get\\(str\\)"):
            flows = self.results.to_df("flow")
        assert isinstance(flows, pd.DataFrame)

    def test_to_set_objective(self):
        with pytest.raises(TypeError):
            self.results["objective"] = 5

    def test_solver_result_access(self):
        with pytest.warns(
            FutureWarning,
            match="The key 'Problem' is deprecated,",
        ):
            assert isinstance(self.results["Problem"], ListContainer)

    def test_economic_calculations(self):
        with pytest.warns(
            ExperimentalFeatureWarning,
            match="Economic calculations in results are experimental.",
        ):
            assert sum(self.results["investment_costs"].sum()) == 0
            total_variable_costs = sum(self.results["variable_costs"].sum())
            assert total_variable_costs == pytest.approx(8495, abs=1)

    def test_time_index(self):
        with pytest.warns(
            FutureWarning,
            match="Results.timeindex will be removed in a future version.",
        ):
            timeindex = self.results.timeindex
        assert len(timeindex) == 25
        assert timeindex[3].strftime("%m/%d/%Y, %H") == "01/01/2012, 03"


def test_direct_pyomo_result_warning_static_method():
    """_direct_pyomo_result_waring() is not called anywhere internally
    but must still raise its FutureWarning when invoked directly
    (covers _results.py line 213)."""
    with pytest.warns(FutureWarning, match="Direct access to Pyomo results"):
        Results._direct_pyomo_result_waring()


def test_results_init_ignores_duplicate_variable_occurrence():
    """If the same (key, occurrence) pair is encountered twice while
    scanning the model's Var components, Results must simply ignore
    the duplicate (covers _results.py line 75)."""

    class _FakeVar:
        def __init__(self, name, block):
            self._name = name
            self._block = block

        def getname(self):
            return self._name

        def parent_block(self):
            return self._block

    class _FakeModel:
        def __init__(self, variables):
            self._solver_results = {}
            self.dual = None
            self.rc = None
            self._variables = variables

        def component_objects(self, _cls):
            return self._variables

    block = object()
    var = _FakeVar("flow", block)
    model = _FakeModel([var, var])  # same variable object seen twice

    result = Results(model, solver_info=pd.Series(dtype=object))
    assert result._variables["flow"][block] is var


def test_investment_costs_dataframe(recwarn):
    """_calc_capex must compute investment costs for InvestmentFlows and
    GenericStorage investments (covers _results.py 228-283).

    NOTE: Adjust the ``Investment``/``GenericStorage`` keyword names below
    if they differ from your installed oemof.solph version.
    """
    es = solph.EnergySystem(timeindex=[0, 1, 2], infer_last_interval=False)
    bus = solph.buses.Bus(label="bus")
    es.add(bus)
    es.add(
        solph.components.Source(
            label="source",
            outputs={
                bus: solph.flows.Flow(
                    nominal_capacity=solph.Investment(
                        ep_costs=10,
                        offset=5,
                        nonconvex=True,
                        maximum=50,
                    )
                )
            },
        )
    )
    es.add(
        solph.components.GenericStorage(
            label="storage",
            inputs={bus: solph.flows.Flow()},
            outputs={bus: solph.flows.Flow()},
            nominal_storage_capacity=solph.Investment(
                ep_costs=20,
                offset=3,
                nonconvex=True,
                maximum=50,
            ),
        )
    )
    es.add(
        solph.components.Sink(
            label="sink",
            inputs={
                bus: solph.flows.Flow(nominal_capacity=10, fix=[0.5, 0.8, 0.3])
            },
        )
    )

    result = solph.Model(es).solve(solver="cbc")

    with pytest.warns(ExperimentalFeatureWarning):
        capex = result.get("investment_costs")

    assert isinstance(capex, pd.DataFrame)
    assert not capex.empty
