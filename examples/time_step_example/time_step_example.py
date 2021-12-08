# -*- coding: utf-8 -*-

"""
General description
-------------------

A minimal example to show how (non-hourly) time steps work.

*   One purpose is to illustrate that the nominal_value in Flows
    has to be interpreted in means of power:
    We have nominal_value=1, but the storage content of an ideal
    storage just changes in steps of 0.25, when having four time
    steps per hour.
*   Also, the initial_storage_level of a GenericStorage is given
    _before_ the first time step. If the storage is balanced,
    this is the same storage level as in the last time step.

Installation requirements
-------------------------

This example requires oemof.solph, install by:

    pip install oemof.solph
"""
import pandas as pd
from oemof import solph

solver = "cbc"  # 'glpk', 'gurobi',...
solver_verbose = False  # show/hide solver output

date_time_index = pd.date_range(
    "1/1/2000", periods=8, freq="15T"
)

energy_system = solph.EnergySystem(timeindex=date_time_index)

bus = solph.buses.Bus(label="bus")
source = solph.components.Source(
    label="source",
    outputs={bus: solph.flows.Flow(nominal_value=1,
                                   variable_costs=-1,
                                   max=[0, 0, 0, 0, 1, 1, 1, 1])}
)
storage = solph.components.GenericStorage(
    label="storage",
    inputs={bus: solph.flows.Flow()},
    outputs={bus: solph.flows.Flow()},
    nominal_storage_capacity=4,
    initial_storage_level=0.5,
)
sink = solph.components.Sink(
    label="sink",
    inputs={bus: solph.flows.Flow(nominal_value=1,
                                  max=[1, 1, 1, 1, 0, 0, 0, 0])}
)

energy_system.add(bus, source, sink, storage)
model = solph.Model(energy_system)
model.solve(solver=solver, solve_kwargs={"tee": solver_verbose})

results = solph.processing.results(model)

print(results[(storage, None)]["sequences"])
