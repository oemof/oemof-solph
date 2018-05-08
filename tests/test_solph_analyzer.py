
from nose.tools import eq_, assert_raises
from energysystems_for_testing import es_with_invest
from oemof.outputlib import processing
from oemof.solph import analyzer


class Analyzer_Tests:
    def setup(self):
        self.results = processing.results(
            es_with_invest.optimization_model)
        self.param_results = processing.param_results(
            es_with_invest.optimization_model)
        self.analysis = analyzer.Analysis(
            self.results,
            self.param_results,
            iterator=analyzer.FlowNodeIterator
        )

    def test_requirements(self):
        self.analysis.clean()

        # depending analyzer missing:
        nb = analyzer.NodeBalanceAnalyzer()
        with assert_raises(analyzer.DependencyError):
            self.analysis.add_analyzer(nb)

        # wrong iterator:
        self.analysis.set_iterator(analyzer.TupleIterator)
        self.analysis.add_analyzer(analyzer.SequenceFlowSumAnalyzer())
        self.analysis.add_analyzer(analyzer.FlowTypeAnalyzer())
        with assert_raises(analyzer.RequirementError):
            self.analysis.add_analyzer(analyzer.NodeBalanceAnalyzer())
        self.analysis.set_iterator(analyzer.FlowNodeIterator)

        # param_results missing:
        self.analysis.param_results = None
        with assert_raises(analyzer.RequirementError):
            self.analysis.add_analyzer(analyzer.InvestAnalyzer())
        self.analysis.param_results = self.param_results

    def test_sequence_flow_sum_analyzer(self):
        self.analysis.clean()
        seq = analyzer.SequenceFlowSumAnalyzer()
        self.analysis.add_analyzer(seq)
        self.analysis.analyze()

        eq_(len(seq.result), 5)
        eq_(seq.result[(es_with_invest.b_diesel, es_with_invest.dg)], 62.5)
        eq_(seq.result[(es_with_invest.dg, es_with_invest.b_el1)], 125)
        eq_(seq.result[(es_with_invest.b_el1, es_with_invest.batt)], 125)
        eq_(seq.result[(es_with_invest.batt, es_with_invest.b_el2)], 100)
        eq_(seq.result[(es_with_invest.b_el2, es_with_invest.demand)], 100)

    def test_variable_cost_analyzer(self):
        self.analysis.clean()
        seq = analyzer.SequenceFlowSumAnalyzer()
        vc = analyzer.VariableCostAnalyzer()
        self.analysis.add_analyzer(seq)
        self.analysis.add_analyzer(vc)
        self.analysis.analyze()

        eq_(len(vc.result), 5)
        eq_(vc.result[(es_with_invest.b_diesel, es_with_invest.dg)], 125)
        eq_(vc.result[(es_with_invest.dg, es_with_invest.b_el1)], 125)
        eq_(vc.result[(es_with_invest.b_el1, es_with_invest.batt)], 375)
        eq_(vc.result[(es_with_invest.batt, es_with_invest.b_el2)], 250)
        eq_(vc.result[(es_with_invest.b_el2, es_with_invest.demand)], 0)

    def test_bus_balance_analyzer(self):
        self.analysis.clean()
        self.analysis.add_analyzer(analyzer.SequenceFlowSumAnalyzer())
        self.analysis.add_analyzer(analyzer.FlowTypeAnalyzer())
        nb = analyzer.BusBalanceAnalyzer()
        self.analysis.add_analyzer(nb)
        self.analysis.analyze()

        eq_(len(nb.result), 3)

        # b_diesel:
        eq_(len(nb.result[es_with_invest.b_diesel]['input']), 0)
        eq_(len(nb.result[es_with_invest.b_diesel]['output']), 1)
        eq_(
            nb.result[es_with_invest.b_diesel]['output'][es_with_invest.dg],
            62.5
        )

        # b_el1:
        eq_(len(nb.result[es_with_invest.b_el1]['input']), 1)
        eq_(len(nb.result[es_with_invest.b_el1]['output']), 1)
        eq_(
            nb.result[es_with_invest.b_el1]['input'][es_with_invest.dg], 125)
        eq_(
            nb.result[es_with_invest.b_el1]['output'][es_with_invest.batt],
            125
        )

        # b_el2:
        eq_(len(nb.result[es_with_invest.b_el2]['input']), 1)
        eq_(len(nb.result[es_with_invest.b_el2]['output']), 1)
        eq_(nb.result[es_with_invest.b_el2]['input'][es_with_invest.batt], 100)
        eq_(
            nb.result[es_with_invest.b_el2]['output'][es_with_invest.demand],
            100
        )

    def test_invest_analyzer(self):
        self.analysis.clean()
        invest = analyzer.InvestAnalyzer()
        self.analysis.add_analyzer(invest)
        self.analysis.analyze()

        eq_(len(invest.result), 4)

        # dg-b_el1-Flow
        eq_(
            invest.result[(es_with_invest.dg, es_with_invest.b_el1)],
            62.5 * 0.5
        )

        # batt
        eq_(invest.result[(es_with_invest.batt, None)], 600 * 0.4)
        eq_(invest.result[(es_with_invest.b_el1, es_with_invest.batt)], 0)
        eq_(invest.result[(es_with_invest.batt, es_with_invest.b_el2)], 0)

    def test_lcoe_analyzer(self):
        self.analysis.clean()
        self.analysis.add_analyzer(analyzer.SequenceFlowSumAnalyzer())
        self.analysis.add_analyzer(analyzer.FlowTypeAnalyzer())
        self.analysis.add_analyzer(analyzer.NodeBalanceAnalyzer())
        self.analysis.add_analyzer(analyzer.VariableCostAnalyzer())
        self.analysis.add_analyzer(analyzer.InvestAnalyzer())
        lcoe = analyzer.LCOEAnalyzer([es_with_invest.demand])
        self.analysis.add_analyzer(lcoe)
        self.analysis.analyze()

        output = 100
        eq_(len(lcoe.result), 6)

        # dg
        eq_(
            lcoe.result[(es_with_invest.dg, es_with_invest.b_el1)],
            (125 + 62.5 * 0.5) / output
        )
        eq_(
            lcoe.result[(es_with_invest.b_diesel, es_with_invest.dg)],
            125 / output
        )

        # batt
        eq_(lcoe.result[(es_with_invest.batt, None)], 600 * 0.4 / output)
        eq_(
            lcoe.result[(es_with_invest.b_el1, es_with_invest.batt)],
            375 / output
        )
        eq_(
            lcoe.result[(es_with_invest.batt, es_with_invest.b_el2)],
            250 / output
        )
        eq_(
            lcoe.result[(es_with_invest.b_el2, es_with_invest.demand)],
            0 / output
        )
