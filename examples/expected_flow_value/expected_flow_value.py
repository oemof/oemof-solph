# -*- coding: utf-8 -*-

"""
General description
-------------------

A minimal example to show speedup of giving expected value to solver.

Installation requirements
-------------------------

This example requires oemof.solph, install by:

    pip install oemof.solph
"""
import numpy as np
import pandas as pd

from oemof import solph

solver = "cbc"  # 'glpk', 'gurobi',...
solver_verbose = False  # show/hide solver output
time_steps = 24*31  # 8760

date_time_index = pd.date_range("1/1/2000", periods=time_steps, freq="H")

rng = np.random.default_rng(seed=1337)
random_costs = rng.exponential(size=time_steps)
random_demands = rng.uniform(size=time_steps)
random_losses = np.minimum(
    np.ones(time_steps),
    rng.exponential(scale=1e-1, size=time_steps)
)


def run_energy_system(index, costs, demands, losses, expected=None):
    energy_system = solph.EnergySystem(timeindex=index)

    if expected is None:
        expected = {
            (("bus", "storage"), "flow"): None,
            (("source", "bus"), "flow"): None,
            (("storage", "bus"), "flow"): None,
        }

    bus = solph.buses.Bus(label="bus")
    source = solph.components.Source(
        label="source",
        outputs={bus: solph.flows.NonConvexFlow(
            variable_costs=costs,
            min=0.2,
            nominal_value=100,
            activity_costs=0.01,
        )},
    )
    storage = solph.components.GenericStorage(
        label="storage",
        inputs={bus: solph.flows.Flow(
            expected=expected[(("bus", "storage"), "flow")])},
        outputs={bus: solph.flows.Flow(
            expected=expected[(("storage", "bus"), "flow")])},
        nominal_storage_capacity=1e4,
        loss_rate=losses,
    )
    sink = solph.components.Sink(
        label="sink",
        inputs={
            bus: solph.flows.Flow(nominal_value=1,
                                  fix=demands)
        },
    )

    energy_system.add(bus, source, sink, storage)
    model = solph.Model(energy_system)
    model.solve(solver=solver, solve_kwargs={"tee": solver_verbose})

    _results = solph.processing.results(model)
    _meta_results = solph.processing.meta_results(model)
    return _results, _meta_results


results, meta_results = run_energy_system(
    date_time_index, random_costs, random_demands, random_losses)
print("Time to solve run (no hints): {time:.2f} s".format(
    time=meta_results['solver']['Wallclock time']))
bus_data = solph.views.node(results, "bus")["sequences"]

_, meta_results = run_energy_system(
    date_time_index, random_costs, random_demands, random_losses)
print("Time to solve run (no hints): {time:.2f} s".format(
    time=meta_results['solver']['Wallclock time']))

_, meta_results = run_energy_system(
    date_time_index, random_costs, random_demands, random_losses,
    expected=bus_data
)
print("Time to solve run (with hints): {time:.2f} s".format(
    time=meta_results['solver']['Wallclock time']))

_, meta_results = run_energy_system(
    date_time_index, random_costs, random_demands, random_losses)
print("Time to solve run (no hints): {time:.2f} s".format(
    time=meta_results['solver']['Wallclock time']))
