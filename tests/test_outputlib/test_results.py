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

    def test_objective(self):
        assert self.results["objective"] == pytest.approx(8495, abs=1)

    def test_to_set_objective(self):
        with pytest.raises(TypeError):
            self.results["objective"] = 5

    def test_time_index(self):
        assert len(self.results.timeindex) == 25
        assert (
            self.results.timeindex[3].strftime("%m/%d/%Y, %H")
            == "01/01/2012, 03"
        )

    def test_attribute_checking(self):
        assert hasattr(self.results, "timeindex")
        assert not hasattr(self.results, "non_existing")
