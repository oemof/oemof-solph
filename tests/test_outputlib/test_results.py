import warnings

import pytest
from oemof.tools.debugging import ExperimentalFeatureWarning

from oemof.solph import Results

from . import optimization_model


class TestResultsClass:
    @classmethod
    def setup_class(cls):
        with warnings.catch_warnings():
            warnings.simplefilter(
                "ignore",
                category=ExperimentalFeatureWarning,
            )
            cls.results = Results(optimization_model)

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
        assert self.results.objective == pytest.approx(8495, abs=1)

    def test_to_set_objective(self):
        with pytest.raises(AttributeError):
            self.results.objective = 5

    def test_time_index(self):
        assert len(self.results.timeindex) == 25
        assert (
            self.results.timeindex[3].strftime("%m/%d/%Y, %H")
            == "01/01/2012, 03"
        )
