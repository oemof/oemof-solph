
from nose.tools import ok_, eq_
import pandas
from oemof.solph import (
    EnergySystem, Bus, Transformer, Flow, Investment, Sink, Model)
from oemof.solph.components import GenericStorage
from oemof.outputlib import processing, views


class Flow_Tests:
    @classmethod
    def setUpClass(cls):
        cls.period = 24
        cls.es = EnergySystem(
            timeindex=pandas.date_range(
                '2016-01-01',
                periods=cls.period,
                freq='H'
            )
        )

        # BUSSES
        b_el1 = Bus(label="b_el1")
        b_el2 = Bus(label="b_el2")
        b_diesel = Bus(label='b_diesel', balanced=False)
        cls.es.add(b_el1, b_el2, b_diesel)

        # TEST DIESEL:
        dg = Transformer(
            label='diesel',
            inputs={b_diesel: Flow(variable_costs=2)},
            outputs={
                b_el1: Flow(
                    variable_costs=1,
                    fixed_costs=20,
                    investment=Investment(ep_costs=0.5)
                )
            },
            conversion_factors={b_el1: 2},
        )

        batt = GenericStorage(
            label='storage',
            inputs={b_el1: Flow(variable_costs=3)},
            outputs={b_el2: Flow(variable_costs=2.5)},
            capacity_loss=0.00,
            initial_capacity=0,
            nominal_input_capacity_ratio=1 / 6,
            nominal_output_capacity_ratio=1 / 6,
            inflow_conversion_factor=1,
            outflow_conversion_factor=0.8,
            fixed_costs=35,
            investment=Investment(ep_costs=0.4),
        )

        demand = [100] * 8760
        demand[0] = 0.0
        demand = Sink(
            label="demand_el",
            inputs={
                b_el2: Flow(
                    nominal_value=1,
                    actual_value=demand,
                    fixed=True
                )
            }
        )
        cls.es.add(dg, batt, demand)
        om = Model(cls.es)
        om.solve(solver='cbc')
        cls.results = processing.results(om)

    def test_filter_nodes(self):
        nodes = views.filter_nodes(self.results)
        eq_(len(nodes), 6)
        nodes = views.filter_nodes(self.results, exclude_busses=True)
        eq_(len(nodes), 3)
        nodes = views.filter_nodes(
            self.results,
            option=views.NodeOption.HasInputs
        )
        eq_(len(nodes), 5)
        nodes = views.filter_nodes(
            self.results,
            option=views.NodeOption.HasInputs,
            exclude_busses=True
        )
        eq_(len(nodes), 3)
        nodes = views.filter_nodes(
            self.results,
            option=views.NodeOption.HasOutputs
        )
        eq_(len(nodes), 5)
        nodes = views.filter_nodes(
            self.results,
            option=views.NodeOption.HasOnlyInputs
        )
        eq_(len(nodes), 1)
        nodes = views.filter_nodes(
            self.results,
            option=views.NodeOption.HasOnlyOutputs
        )
        eq_(len(nodes), 1)
        nodes = views.filter_nodes(
            self.results,
            option=views.NodeOption.HasOnlyOutputs,
            exclude_busses=True
        )
        eq_(len(nodes), 0)

    def test_get_node_by_name(self):
        b_diesel = views.get_node_by_name(self.results, 'b_diesel')
        eq_(b_diesel, self.es.groups['b_diesel'])
        dg, storage = views.get_node_by_name(
            self.results,
            'diesel',
            'storage'
        )
        eq_(dg, self.es.groups['diesel'])
        eq_(storage, self.es.groups['storage'])

    def test_input_flows(self):
        dg = self.es.groups['diesel']
        input_flows = views.flows(
            self.results,
            dg,
            flow_type=views.FlowType.Input
        )
        eq_(len(input_flows), 1)

        b_diesel = self.es.groups['b_diesel']
        ok_(isinstance(input_flows[(b_diesel, dg)], Flow))

    def test_node_with_flows(self):
        storage = self.es.groups['storage']
        node_results = views.node(self.results, storage, get_flows=True)
        ok_('flows' in node_results)
        eq_(len(node_results['flows']), 3)

        b_el1 = self.es.groups['b_el1']
        b_el2 = self.es.groups['b_el2']
        flow = node_results['flows'][(b_el1, storage)]
        eq_(flow.type, views.FlowType.Input)
        eq_(flow.component.variable_costs, [3] * self.period)
        # Test other flow type comparison:
        eq_(
            node_results['flows'][(b_el1, storage)].type,
            'input'
        )
        eq_(
            node_results['flows'][(storage, b_el2)].type,
            views.FlowType.Output
        )
        eq_(
            node_results['flows'][(storage, None)].type,
            views.FlowType.Single
        )
