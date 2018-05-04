
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
        analyzer.init(
            self.results,
            self.param_results,
            iterator=analyzer.FlowNodeIterator
        )

    def test_requirements(self):
        analyzer.clean()

        # depending analyzer missing:
        with assert_raises(analyzer.DependencyError):
            _ = analyzer.BusBalanceAnalyzer()

        # wrong iterator:
        analyzer.Analysis().iterator = analyzer.TupleIterator
        _ = analyzer.SequenceFlowSumAnalyzer()
        _ = analyzer.FlowTypeAnalyzer()
        with assert_raises(analyzer.RequirementError):
            _ = analyzer.BusBalanceAnalyzer()
        analyzer.Analysis().iterator = analyzer.FlowNodeIterator

        # param_results missing:
        analyzer.Analysis().param_results = None
        with assert_raises(analyzer.RequirementError):
            _ = analyzer.InvestAnalyzer()
        analyzer.Analysis().param_results = self.param_results

    @staticmethod
    def test_sequence_flow_sum_analyzer():
        analyzer.clean()
        seq = analyzer.SequenceFlowSumAnalyzer()
        analyzer.analyze()

        eq_(len(seq.result), 5)
        eq_(seq.result[(es_with_invest.b_diesel, es_with_invest.dg)], 62.5)
        eq_(seq.result[(es_with_invest.dg, es_with_invest.b_el1)], 125)
        eq_(seq.result[(es_with_invest.b_el1, es_with_invest.batt)], 125)
        eq_(seq.result[(es_with_invest.batt, es_with_invest.b_el2)], 100)
        eq_(seq.result[(es_with_invest.b_el2, es_with_invest.demand)], 100)

    @staticmethod
    def test_variable_cost_analyzer():
        analyzer.clean()
        _ = analyzer.SequenceFlowSumAnalyzer()
        vc = analyzer.VariableCostAnalyzer()
        analyzer.analyze()

        eq_(len(vc.result), 5)
        eq_(vc.result[(es_with_invest.b_diesel, es_with_invest.dg)], 125)
        eq_(vc.result[(es_with_invest.dg, es_with_invest.b_el1)], 125)
        eq_(vc.result[(es_with_invest.b_el1, es_with_invest.batt)], 375)
        eq_(vc.result[(es_with_invest.batt, es_with_invest.b_el2)], 250)
        eq_(vc.result[(es_with_invest.b_el2, es_with_invest.demand)], 0)

    @staticmethod
    def test_bus_balance_analyzer():
        analyzer.clean()
        _ = analyzer.SequenceFlowSumAnalyzer()
        _ = analyzer.FlowTypeAnalyzer()
        bb = analyzer.BusBalanceAnalyzer()
        analyzer.analyze()

        eq_(len(bb.result), 3)

        # b_diesel:
        eq_(len(bb.result[es_with_invest.b_diesel]['input']), 0)
        eq_(len(bb.result[es_with_invest.b_diesel]['output']), 1)
        eq_(
            bb.result[es_with_invest.b_diesel]['output'][es_with_invest.dg],
            62.5
        )

        # b_el1:
        eq_(len(bb.result[es_with_invest.b_el1]['input']), 1)
        eq_(len(bb.result[es_with_invest.b_el1]['output']), 1)
        eq_(
            bb.result[es_with_invest.b_el1]['input'][es_with_invest.dg],
            125
        )
        eq_(
            bb.result[es_with_invest.b_el1]['output'][es_with_invest.batt],
            125
        )

        # b_el2:
        eq_(len(bb.result[es_with_invest.b_el2]['input']), 1)
        eq_(len(bb.result[es_with_invest.b_el2]['output']), 1)
        eq_(
            bb.result[es_with_invest.b_el2]['input'][es_with_invest.batt],
            100
        )
        eq_(
            bb.result[es_with_invest.b_el2]['output'][es_with_invest.demand],
            100
        )

    @staticmethod
    def test_invest_analyzer():
        analyzer.clean()
        invest = analyzer.InvestAnalyzer()
        analyzer.analyze()

        eq_(len(invest.result), 4)

        # dg-b_el1-Flow
        eq_(
            invest.result[(es_with_invest.dg, es_with_invest.b_el1)],
            62.5 * 0.5
        )

        # batt
        eq_(
            invest.result[(es_with_invest.batt, None)],
            600 * 0.4
        )
        eq_(
            invest.result[(es_with_invest.b_el1, es_with_invest.batt)],
            0
        )
        eq_(
            invest.result[(es_with_invest.batt, es_with_invest.b_el2)],
            0
        )

    # @staticmethod
    # def test_lcoe_analyzer():
    #     analyzer.clean()
    #     _ = analyzer.SequenceFlowSumAnalyzer()
    #     _ = analyzer.FlowTypeAnalyzer()
    #     _ = analyzer.NodeBalanceAnalyzer()
    #     analyzer.analyze()
    #     analyzer.store_results()
    #     lcoe = analyzer.LCOEAnalyzer([es_with_invest.demand])
    #     analyzer.analyze()
