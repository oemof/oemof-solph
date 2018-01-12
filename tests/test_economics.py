
from nose.tools import eq_
import pandas
from oemof.solph import (
    EnergySystem, Bus, Transformer, Flow, Investment, Sink, Model)
from oemof.solph.components import GenericStorage
from oemof.outputlib import processing
from oemof.tools import economics


# initialize energy system
es = EnergySystem(
    timeindex=pandas.date_range('2016-01-01', periods=2, freq='H')
)

# BUSSES
b_el1 = Bus(label="b_el1")
b_el2 = Bus(label="b_el2")
b_diesel = Bus(label='b_diesel', balanced=False)
es.add(b_el1, b_el2, b_diesel)

# TEST DIESEL:
dg_output = Flow(
    variable_costs=1,
    investment=Investment(ep_costs=0.5)
)
dg_output.real_invest_costs = 10
dg = Transformer(
    label='diesel',
    inputs={
        b_diesel: Flow(
            variable_costs=2,
        )
    },
    outputs={
        b_el1: dg_output
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
    investment=Investment(ep_costs=0.4),
)
# Add custom attribute:
batt.real_invest_costs = 30

demand = Sink(
    label="demand_el",
    inputs={
        b_el2: Flow(
            nominal_value=1,
            actual_value=[0, 100],
            fixed=True
        )
    }
)
es.add(dg, batt, demand)

om = Model(energysystem=es)
om.solve(solve_kwargs={'tee': True, 'keepfiles': True})

results = processing.results(om)
param_results = processing.param_results(om, exclude_none=True)
cost_results = economics.cost_results(results, param_results)


class Economic_Tests():
    def test_diesel_cost_results(self):
        eq_(
            cost_results[(dg, None)].get('invest'),
            None
        )
        eq_(
            cost_results[(dg, b_el1)]['variable_costs'],
            62.5 * 2 * 1
        )
        eq_(
            cost_results[(dg, b_el1)]['invest'],
            62.5 * 0.5
        )
        eq_(
            cost_results[(b_diesel, dg)]['variable_costs'],
            31.25 * 2 * 2
        )

    def test_storage_cost_results(self):
        eq_(
            cost_results[(batt, None)]['invest'],
            600 * 0.4
        )
        eq_(
            cost_results[(b_el1, batt)]['variable_costs'],
            62.5 * 2 * 3
        )
        eq_(
            cost_results[(batt, b_el2)]['variable_costs'],
            100 * 2.5
        )

    def test_custom_costs(self):
        custom_costs = [
            economics.Costs(
                name='real_invest_costs',
                flow_key=economics.AttributeKey(
                    dimension='scalars',
                    name='invest'
                ),
                param_key=economics.AttributeKey(
                    dimension='scalars',
                    name='real_invest_costs'
                )
            )
        ]
        custom_cost_results = economics.cost_results(
            results, param_results, custom_costs)
        eq_(
            custom_cost_results[(batt, None)]['real_invest_costs'],
            600 * 30
        )
