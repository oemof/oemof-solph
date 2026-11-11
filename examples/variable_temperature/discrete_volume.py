# SPDX-FileCopyrightText: Geert Petrin
# SPDX-FileCopyrightText: Patrik Schönfeldt
#
# SPDX-License-Identifier: MIT

import os

import pandas as pd
from pyomo import environ as po

from oemof.solph import Bus
from oemof.solph import EnergySystem
from oemof.solph import Flow
from oemof.solph import Model
from oemof.solph import NonConvex
from oemof.solph.components import GenericStorage
from oemof.solph.components import Sink
from oemof.solph.components import Source
from oemof.solph.constraints import limit_active_flow_count_by_keyword

def prepare_input_data(
        start_time=None,
        end_time=None,
) -> pd.DataFrame:
    input_data = pd.read_csv(
        os.path.join(
            os.path.dirname(__file__), "input_data.csv"
        ),
        index_col=0,
        parse_dates=[0],
    )

    if start_time is None:
        start_time = input_data.index[0]
    if end_time is None:
        end_time = input_data.index[-1]

    input_data["temp_soil (°C)"] = 5
    input_data["temp_air (°C)"] = input_data["t2m (K)"] - 273.15
    input_data["radiation (kW/m2)"] = (
        input_data["ssrd (J/m2)"]
        / 3600  # J/h -> W
    )
    # We assume 10 °C for fresh water and 35 °C for warm water (Wh/kcal)
    input_data["Warm Water (W)"] = input_data["Warm Water (l/h)"] * 29.06

    del input_data["t2m (K)"]
    del input_data["ssrd (J/m2)"]

    return input_data[start_time: end_time]


def main():
    input_data = prepare_input_data(
        start_time="2025-02-01 00:00:00",
        end_time="2025-02-14 23:00:00",
    )

    es = EnergySystem(
        timeindex=input_data.index,
        infer_last_interval=True,
    )

    # Electricity
    #############
    bus_el = Bus(label="bus_el")
    input_grid_el = Source(
        label="grid_el",
        outputs={bus_el: Flow(variable_costs=0.30)},
    )
    input_pv_el = Source(
        label="PV",
        outputs={
            bus_el: Flow(
                nominal_capacity=15e3,
                variable_costs=0.1e-3,  # feed-in would give 10 ct/kWh
                maximum=input_data["radiation (kW/m2)"] / 1000,
            )
        },
    )
    es.add(bus_el, input_grid_el, input_pv_el)

    # Cold heat (<= 15 °C, before heat pump)
    ########################################
    bus_heat_cold = Bus(label="heat_cold")

    input_sol_cold = Source(
        label="Cold Solar",
        outputs={
            bus_heat_cold: Flow(
                nominal_capacity=50000,
                nonconvex=NonConvex(),
                custom_properties={"Limit": True},
            )
        },
    )

    input_geothermal = Source(
        label="input_geothermal",
        outputs={bus_heat_cold: Flow(nominal_capacity=150000)},
    )

    storage_cold = GenericStorage(
        label="storage_cold",
        nominal_capacity=150000,  # FIXME: Arbitrary
        balanced=True,
        loss_rate=0,
        inputs={bus_heat_cold: Flow()},
        outputs={bus_heat_cold: Flow(nominal_capacity=100000)},
    )

    es.add(bus_heat_cold, input_sol_cold, input_geothermal, storage_cold)

    # Warm heat (>= 25°C, after heat pump)
    ######################################
    bus_heat_warm = Bus(label="heat_warm")

    input_sol_warm = Source(
        label="Collector Warm",
        outputs={
            bus_heat_warm: Flow(
                nominal_capacity=50000,
                nonconvex=NonConvex(),
                custom_properties={"Limit": True},
            )
        },
    )

    demand_sh = Sink(
        label="output_SH",
        inputs={
            bus_heat_warm: Flow(
                nominal_capacity=1,
                fix=input_data["Space Heating (W)"],
            )
        },
    )

    storage_warm = GenericStorage(
        label="storage_warm",
        nominal_capacity=150000,  # FIXME: Arbitrary
        initial_storage_level=0.5,
        balanced=True,
        loss_rate=0,
        inputs={bus_heat_warm: Flow()},
        outputs={bus_heat_warm: Flow()},
    )

    es.add(bus_heat_warm, input_sol_warm, demand_sh, storage_warm)

    # Tap water (== 35°C, after flow heater)
    ########################################
    bus_heat_dhw = Bus(label="heat_dhw")

    demand_dhw = Sink(
        label="output_DHW",
        inputs={
            bus_heat_dhw: Flow(
                nominal_capacity=1,
                fix=input_data["Warm Water (W)"],
            ),
        },
    )
    es.add(bus_heat_dhw, demand_dhw)

    # heat pump and flow heater
    ###########################
    # These are buses, as we have energy conservation
    # but no conversion factors that can be pre-calculated.
    heat_pump = Bus(
        label="heat_pump",
        inputs={
            bus_heat_cold: Flow(),
            bus_el: Flow(),
        },
        outputs={
            bus_heat_warm: Flow(),
        },
    )

    flow_heater = Bus(
        label="flow_heater",
        inputs={
            bus_heat_warm: Flow(),
            bus_el: Flow(),
        },
        outputs={
            bus_heat_dhw: Flow(),
        }
    )

    es.add(heat_pump, flow_heater)

    model = Model(es)

    limit_active_flow_count_by_keyword(model, "solar_thermal", lower_limit=0, upper_limit=1)

    results = model.solve(
        solver="cbc",
        solve_kwargs={"tee": False},
    )

    print(results["storage_content"])


if __name__ == "__main__":
    main()
