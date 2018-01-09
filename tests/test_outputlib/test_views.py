
from nose.tools import eq_
from . import optimization_model
from oemof.outputlib import processing
from oemof.outputlib.views import filter_nodes, NodeOption


class Filter_Test():
    def setup(self):
        self.results = processing.results(optimization_model)

    def test_filter_all(self):
        nodes = filter_nodes(self.results)
        eq_(len(nodes), 19)

    def test_filter_all_without_busses(self):
        nodes = filter_nodes(self.results, exclude_busses=True)
        eq_(len(nodes), 19 - 7)

    def test_filter_only_sources(self):
        nodes = filter_nodes(
            self.results,
            option=NodeOption.HasOnlyOutputs,
            exclude_busses=True
        )
        eq_(len(nodes), 3)

    def test_filter_has_outputs(self):
        nodes = filter_nodes(
            self.results,
            option=NodeOption.HasOutputs
        )
        eq_(len(nodes), 16)
