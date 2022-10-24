# -*- coding: utf-8 -*-

"""
General description
-------------------

A minimal example to show how time steps work.

*   Flows are defined in time intervals, storage content at points in time.
    Thus, there is one more value for storage contents then for the
    flow values.
*   Time intervals are named by the time at the beginning of that interval.
    The quantity changes to the given value at the given point in time.
*   The initial_storage_level of a GenericStorage is given
    at the first time step. If the storage is balanced,
    this is the same storage level as in the last time step.
*   The nominal_value in Flows has to be interpreted in means of power:
    We have nominal_value=0.5, but the maximum change of the storage content
    of an ideal storage is 0.125.

Installation requirements
-------------------------

This example requires oemof.solph, install by:

    pip install oemof.solph
"""
import pandas as pd
from oemof import solph

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None

solver = "cbc"  # 'glpk', 'gurobi',...
solver_verbose = False  # show/hide solver output

date_time_index = pd.date_range("1/1/2000", periods=9, freq="15T")

energy_system = solph.EnergySystem(
    timeindex=date_time_index, infer_last_interval=False
)

bus = solph.buses.Bus(label="bus")
source = solph.components.Source(
    label="source",
    outputs={
        bus: solph.flows.Flow(
            nominal_value=2,
            variable_costs=0.2,
            max=[0, 0, 0, 0, 1, 0.25, 0.75, 1],
        )
    },
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
    inputs={
        bus: solph.flows.Flow(
            nominal_value=2,
            variable_costs=0.1,
            fix=[1, 1, 0.5, 0.5, 0, 0, 0, 0],
        )
    },
)

energy_system.add(bus, source, sink, storage)
model = solph.Model(energy_system)
model.solve(solver=solver, solve_kwargs={"tee": solver_verbose})

results = solph.processing.results(model)

results_df = results[(storage, None)]["sequences"].copy()
results_df["storage_inflow"] = results[(bus, storage)]["sequences"]["flow"]
results_df["storage_outflow"] = results[(storage, bus)]["sequences"]["flow"]

print(results_df)

if plt is not None:
    plt.plot(
        results[(bus, storage)]["sequences"],
        drawstyle="steps-post",
        label="Storage inflow",
    )
    plt.plot(results[(storage, None)]["sequences"], label="Storage content")
    plt.plot(
        results[(storage, bus)]["sequences"],
        drawstyle="steps-post",
        label="Storage outflow",
    )

    plt.legend(loc="lower left")
    plt.show()
