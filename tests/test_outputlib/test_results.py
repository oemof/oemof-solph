import pytest

from oemof.solph import _results

from . import optimization_model


class TestFilterView:
    @classmethod
    def setup_class(cls):
        cls.results = _results.Results(optimization_model)

    def test_objective(self):
        assert int(self.results.objective) == 8495

    def test_to_set_objective(self):
        msg = "property 'objective' of 'Results' object has no setter"
        with pytest.raises(AttributeError, match=msg):
            self.results.objective = 5

    def test_time_index(self):
        assert len(self.results.timeindex) == 25
        assert (
            self.results.timeindex[3].strftime("%m/%d/%Y, %H")
            == "01/01/2012, 03"
        )
