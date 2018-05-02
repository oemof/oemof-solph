
from nose.tools import eq_
from energysystems_for_testing import multiple_sources_and_transformers
from oemof.outputlib import processing
from oemof.solph import analyzer


class Analyzer_Tests:
    def setup(self):
        self.results = processing.results(
            multiple_sources_and_transformers.optimization_model)
        self.param_results = processing.param_results(
            multiple_sources_and_transformers.optimization_model)
        analyzer.init(self.results, self.param_results)

    def test_simple_analyzer(self):
        analyzer.clean()
        a = analyzer.SequenceFlowSumAnalyzer()
        for flow in self.results:
            analyzer.analyze(*flow)

        eq_(len(a.result), 20)

    def test_multiple_analyzer(self):
        analyzer.clean()
        a = analyzer.SequenceFlowSumAnalyzer()
        b = analyzer.NodeAnalyzer()
        for flow in self.param_results:
            analyzer.analyze(*flow)

        eq_(len(a.result), 20)
        eq_(len(b.result), 6)

    def test_dependent_analyzer(self):
        analyzer.clean()
        a = analyzer.SequenceFlowSumAnalyzer()
        b = analyzer.OpexAnalyzer()
        for flow in self.param_results:
            analyzer.analyze(*flow)

        eq_(len(a.result), 20)
        eq_(len(b.result), 6)
