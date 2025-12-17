"""
This integration test validates that the Results object properly merges
status variables from NonConvexFlowBlock and InvestNonConvexFlowBlock
into one DataFrame.

The test scenario is using the following components:
* Gas boiler with insufficient minimal part load to supply heat in time step 2.
* Electrical heater without constraint but high operational costs.
* Heat pump (with extremely low investment costs) but a rather low power limit.
  It can only supply part of the heat. As the electrical heater is always
  needed as a complement, it is only run if the boiler cannot.

SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT
"""

import pandas as pd

from oemof import solph


def test_non_convex_status_variables():
    # Energy System
    energy_system = solph.EnergySystem(
        timeindex=pd.date_range(start="2025-01-01 12:00", freq="h", periods=3),
        infer_last_interval=False,
    )

    # Buses
    bus_heat = solph.Bus("heat")

    energy_system.add(bus_heat)

    demand_heat = solph.components.Sink(
        label="demand",
        inputs={bus_heat: solph.Flow(nominal_capacity=5, fix=[0.5, 0.3])},
    )
    energy_system.add(demand_heat)

    # gas boiler with minimal load
    boiler = solph.components.Source(
        label="gb",
        outputs={
            bus_heat: solph.Flow(
                nonconvex=solph.NonConvex(),
                nominal_capacity=5,
                min=0.5,
                variable_costs=0.15,
            ),
        },
    )
    energy_system.add(boiler)

    # heat pump with limited size
    heat_pump = solph.components.Source(
        label="hp",
        outputs={
            bus_heat: solph.Flow(
                nominal_capacity=solph.Investment(maximum=1, ep_costs=0.1),
                min=0.5,
                nonconvex=solph.NonConvex(),
                variable_costs=0.1,
            )
        },
    )
    energy_system.add(heat_pump)

    el_heater = solph.components.Source(
        label="rh",
        outputs={bus_heat: solph.Flow(variable_costs=0.3)},
    )
    energy_system.add(el_heater)

    # Model
    model = solph.Model(energy_system)

    # Optimization
    model.solve(solver="cbc", solve_kwargs={"tee": False})

    results = solph.Results(model)

    assert (results["status"][(boiler, bus_heat)] == [1, 0]).all()
    assert (results["status"][(heat_pump, bus_heat)] == [0, 1]).all()

    print(results["flow"])


if __name__ == "__main__":
    test_non_convex_status_variables()
