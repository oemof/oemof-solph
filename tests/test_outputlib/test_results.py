import pytest
from oemof.tools.debugging import ExperimentalFeatureWarning
from pyomo.opt.results.container import ListContainer

from oemof.solph import Results

from . import optimization_model


class TestResultsClass:
    @classmethod
    def setup_class(cls):
        cls.results = Results(optimization_model)

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
        assert self.results["objective"] == pytest.approx(8495, abs=1)

    def test_to_set_objective(self):
        with pytest.raises(TypeError):
            self.results["objective"] = 5

    def test_solver_result_access(self):
        with pytest.warns(
            FutureWarning,
            match="Direct access to Pyomo results",
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
        assert len(self.results.timeindex) == 25
        assert (
            self.results.timeindex[3].strftime("%m/%d/%Y, %H")
            == "01/01/2012, 03"
        )
