# -*- coding: utf-8 -*-

"""
This example gives a simplified idea how subnodes
might be used to work with discretised temperatures.

SPDX-FileCopyrightText: Patrik Schönfeldt <patrik.schoenfeldt@dlr.de>
SPDX-FileCopyrightText: Deutsches Zentrum für Luft- und Raumfahrt (DLR)

SPDX-License-Identifier: MIT
"""

import numpy as np

import matplotlib.pyplot as plt

from oemof.network import Node
from oemof.network.network.nodes import QualifiedLabel

from oemof import solph


class HeatPump(Node):
    """A simple heat pump model (including its source) with a COP depending
    on source a temperature (parameter) and and one of multiple possible target
    temperatures (optimiser decision).
    """

    def __init__(
        self,
        label: str,
        el_supply: solph.Bus,
        heat_demand: dict[solph.Bus, float],
        source_temperature: float | list[float],
        cpf: float = 0.5,
        el_power_limit: float = None,
        parent_node=None,
    ):
        """
        Parameters
        ----------
        label: str
            Name of the heat pump
        el_supply
            Bus where electricity is taken from
        heat_demand:
            dictionary containing heat demand Buses (keys),
            and temperatures (in °C, values)
        source_temperature:
            temperature (in °C), potentially a time series
        cpf:
            Carnot Performacne Factor
            (efficiency relative to thermodynamic optimum)
        el_power_limit:
            Limit for electric power consumption.
        """
        self.el_supply_bus = el_supply
        self.heat_demand_buses = heat_demand
        self.temperature = np.array(source_temperature)

        self.cpf = cpf
        self.el_power_limit = el_power_limit

        super().__init__(label=label, parent_node=parent_node)

        el_bus = self.subnode(
            solph.Bus,
            local_name="el",
            inputs={
                self.el_supply_bus: solph.Flow(
                    nominal_capacity=self.el_power_limit,
                ),
            },
        )

        for target, temperature in self.heat_demand_buses.items():
            cop = (
                self.cpf
                * (temperature + 273.15)
                / (temperature - self.temperature)
            )

            self.subnode(
                solph.components.Converter,
                local_name=f"hp_{temperature}",
                inputs={el_bus: solph.Flow()},
                outputs={target: solph.Flow()},
                conversion_factors={target: cop},
            )


def main():

    date_time_index = solph.create_time_index(2025, number=2)

    # create the energysystem and assign the time index
    es = solph.EnergySystem(
        timeindex=date_time_index, infer_last_interval=False
    )

    house = Node("house")

    el_bus = house.subnode(
        solph.Bus,
        local_name="el",
    )
    el_source = solph.components.Source(
        label=QualifiedLabel(("el_grid",)),
        outputs={el_bus: solph.Flow(variable_costs=0.3)},
    )
    es.add(house, el_bus, el_source)

    heat_demands = house.subnode(
        Node,
        local_name="heat demand",
    )
    demand_bus_dhw = heat_demands.subnode(solph.Bus, "b_dhw")
    demand_bus_sh = heat_demands.subnode(solph.Bus, "b_sh")

    heat_demands.subnode(
        solph.components.Sink,
        local_name="d_dhw",
        inputs={demand_bus_dhw: solph.Flow(nominal_capacity=1, fix=[0, 0.2])},
    )
    heat_demands.subnode(
        solph.components.Sink,
        local_name="d_sh",
        inputs={demand_bus_sh: solph.Flow(nominal_capacity=1, fix=[0.4, 2.1])},
    )
    es.add(heat_demands)
    hp = house.subnode(
        HeatPump,
        local_name="hp",
        el_supply=el_bus,
        heat_demand={demand_bus_dhw: 60.0, demand_bus_sh: 30},
        source_temperature=[3, 0],
        cpf=0.45,
        el_power_limit=3,
    )
    es.add(hp)

    model = solph.Model(es)
    model.solve()

    results = solph.Results(model)

    print(results.flow.columns)



if __name__ == "__main__":
    main()
