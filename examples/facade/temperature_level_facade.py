# -*- coding: utf-8 -*-

"""
This example gives a simplified idea how Facades and SubNetworks
might be used to work with discretised temperatures.

SPDX-FileCopyrightText: Patrik Schönfeldt <patrik.schoenfeldt@dlr.de>
SPDX-FileCopyrightText: Deutsches Zentrum für Luft- und Raumfahrt (DLR)

SPDX-License-Identifier: MIT
"""

import numpy as np

from oemof.network import SubNetwork

from oemof import solph


class HeatPump(solph.Facade):

    def __init__(
        self,
        label: str,
        el_supply: solph.Bus,
        heat_demand: dict[solph.Bus, float],
        source_temperature: float | list[float],
        cpf: float = 0.5,
        el_power_limit: float = None,
    ):
        self.el_supply_bus = el_supply
        self.heat_demand_buses = heat_demand
        self.temperature = np.array(source_temperature)

        self.cpf = cpf
        self.el_power_limit = el_power_limit

        super().__init__(label=label, facade_type=type(self))

    def define_subnetwork(self):
        el_bus = self.subnode(
            solph.Bus,
            label="el",
            inputs={
                self.el_supply_bus: solph.Flow(
                    nominal_capacity=self.el_power_limit,
                ),
            },
        )

        for target, temperature in self.heat_demand_buses.items():
            cop = self.cpf * temperature / (temperature - self.temperature)

            self.subnode(
                solph.components.Converter,
                label=f"hp_{temperature}",
                inputs={el_bus: solph.Flow()},
                outputs={target: solph.Flow()},
                conversion_factors={el_bus: cop},
            )


def main():

    date_time_index = solph.create_time_index(2025, number=2)

    # create the energysystem and assign the time index
    es = solph.EnergySystem(
        timeindex=date_time_index, infer_last_interval=False
    )

    house = SubNetwork("house")

    el_bus = house.subnode(
        solph.Bus,
        label="el",
    )
    el_source = solph.components.Source(
        label="el_grid",
        outputs={el_bus: solph.Flow(variable_costs=0.3)},
    )
    es.add(house, el_bus, el_source)

    heat_demands = house.subnode(
        SubNetwork,
        label="heat demand",
    )
    demand_bus_dhw = heat_demands.subnode(solph.Bus, "b_dhw")
    demand_bus_sh = heat_demands.subnode(solph.Bus, "b_sh")

    heat_demands.subnode(
        solph.components.Sink,
        label="d_dhw",
        inputs={demand_bus_dhw: solph.Flow(nominal_capacity=1, fix=[0, 0.2])},
    )
    heat_demands.subnode(
        solph.components.Sink,
        label="d_sh",
        inputs={demand_bus_sh: solph.Flow(nominal_capacity=1, fix=[0.4, 2.1])},
    )
    es.add(heat_demands)
    hp = house.subnode(
        HeatPump,
        "hp",
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

    print(results.flow)


if __name__ == "__main__":
    main()
