import pandas
from oemof.solph import (
    EnergySystem, Bus, Transformer, Flow, Investment, Sink, Model)
from oemof.solph.components import GenericStorage


# initialize energy system
energysystem = EnergySystem(
    timeindex=pandas.date_range('2016-01-01', periods=2, freq='H')
)

# BUSSES
b_el1 = Bus(label="b_el1")
b_el2 = Bus(label="b_el2")
b_diesel = Bus(label='b_diesel', balanced=False)
energysystem.add(b_el1, b_el2, b_diesel)

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
energysystem.add(dg, batt, demand)

optimization_model = Model(energysystem=energysystem)
optimization_model.solve(solve_kwargs={'tee': True, 'keepfiles': True})
