# SPDX-FileCopyrightText: Geert Petrin
# SPDX-FileCopyrightText: Patrik Schönfeldt
# SPDX-FileCopyrightText: DLR e.V.
#
# SPDX-License-Identifier: MIT

"""
General description
-------------------

This is a rather advanced example that shows how temepratures can be considered
as optimisation variables in optimisation models fo the heat sector.
It complements a publication that can be found at https://elib.dlr.de/216784/.
Directly using temperature is more difficult than using discrete temperatures
(see other example).

The convention in this script is to use Flows in terms of energy/power (in kW),
but storage units have temeprature (in °C) as their unit.
"""

import os

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from pyomo import environ as po
from pyomo.core import Var
from pytz import timezone

from oemof.solph import Bus
from oemof.solph import EnergySystem
from oemof.solph import Flow
from oemof.solph import Model
from oemof.solph import NonConvex
from oemof.solph import Results
from oemof.solph.components import Converter
from oemof.solph.components import GenericStorage
from oemof.solph.components import Sink
from oemof.solph.components import Source
from oemof.solph.constraints import limit_active_flow_count_by_keyword

from _shared import celsius2kelvin
from _shared import kcal2kilowatthours
from _shared import prepare_input_data
from _shared import plot_heat_flow_stack


def main():
    START_TIME = "2017-07-01T00:00:00"
    END_TIME = "2017-07-10T23:00:00"

    SOLVER = "highs"  # could also be e.g. "cbc"
    SOLVER_TIME_LIMIT = 300  # seconds

    COLD_STORAGE_VOLUME = 50  # m³
    WARM_STORAGE_VOLUME = 50  # m³

    DOWNHOLE_POWER = 200  # kW
    DOWNHOLE_DESIGN_DELTA = 5  #  °C

    HEAT_PUMP_NOMINAL_POWER = 200  # kW
    HEAT_PUMP_EFFICIENCY = 0.45
    HEAT_PUMP_OUTLET_TEMPERATURE = 35  # °C

    FRESH_WATER_TEMPERATURE = 10  # °C
    SPACE_HEATING_TEMPERATURE = 30  # °C
    TAP_WATER_TEMPERATURE = 40  # °C

    SOLAR_COLLECTOR_BIG_M = 1500  # kW
    SOLAR_COLLECTOR_EFFICIENCY = 0.988
    HEAT_LOSS_COEFFIANT = 0.0035  # kW/m2/K
    COLLECTOR_AREA = 500  #  m2
    FLOW_PER_HOUR = 2 * 3600  # 2 l/s * 3600 s/h

    # derrived parameters
    POWER_LIMIT_PER_KELVIN = kcal2kilowatthours(
        FLOW_PER_HOUR
    )  # (rho c_p dot{V}) in kW/K
    VIRUTAL_THERMAL_TRANSMITTANCE = (
        POWER_LIMIT_PER_KELVIN
        * (  # U_C x A_C in kW/k
            1
            - np.exp(
                (
                    -HEAT_LOSS_COEFFIANT
                    * COLLECTOR_AREA
                    * SOLAR_COLLECTOR_EFFICIENCY
                )
                / POWER_LIMIT_PER_KELVIN
            )
        )
    )

    input_data = prepare_input_data(start_time=START_TIME, end_time=END_TIME)

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
    es.add(bus_el, input_grid_el)

    # Cold heat (<= 15 °C, before heat pump)
    ########################################
    bus_heat_cold = Bus(label="heat_cold")

    input_sol_cold = Source(
        label="Cold Solar",
        outputs={
            bus_heat_cold: Flow(
                nominal_capacity=SOLAR_COLLECTOR_BIG_M,
                nonconvex=NonConvex(),
                custom_properties={"solar_thermal": True},
            )
        },
    )

    input_geothermal = Source(
        label="input_geothermal",
        outputs={
            bus_heat_cold: Flow(
                nominal_capacity=DOWNHOLE_POWER,
                nonconvex=NonConvex(),
            )
        },
    )

    COLD_STORAGE_CONVERSION = 1 / kcal2kilowatthours(
        1000 * COLD_STORAGE_VOLUME
    )  # °C / kWh
    storage_cold = GenericStorage(
        label="storage_cold",
        nominal_capacity=15,  # up to 20 °C
        balanced=True,
        loss_rate=0,
        inputs={bus_heat_cold: Flow()},
        outputs={bus_heat_cold: Flow(nominal_capacity=100)},
        inflow_conversion_factor=COLD_STORAGE_CONVERSION,
        outflow_conversion_factor=1 / COLD_STORAGE_CONVERSION,
    )

    es.add(bus_heat_cold, input_sol_cold, input_geothermal, storage_cold)

    # Warm heat (>= 25°C, after heat pump)
    ######################################
    bus_heat_warm = Bus(label="heat_warm")

    heating_rod = Converter(
        label="Heating Rod",
        inputs={bus_el: Flow()},
        outputs={bus_heat_warm: Flow()},
        conversion_factors={bus_heat_warm: 0.99},  #  99% efficiency
    )

    input_sol_warm = Source(
        label="Collector Warm",
        outputs={
            bus_heat_warm: Flow(
                nominal_capacity=SOLAR_COLLECTOR_BIG_M,
                nonconvex=NonConvex(),
                custom_properties={"solar_thermal": True},
            )
        },
    )

    # space heating can use 25 °C, so no constraints
    demand_sh = Sink(
        label="output_SH",
        inputs={
            bus_heat_warm: Flow(
                nominal_capacity=1,
                fix=input_data["Space Heating (kW)"],
            )
        },
    )

    WARM_STORAGE_CONVERSION = 1 / kcal2kilowatthours(
        1000 * WARM_STORAGE_VOLUME
    )  # °C / kWh
    WARM_STORAGE_CAPACITY = 100  # 0 - 100 °C, scale is easy to work with
    storage_warm = GenericStorage(
        label="storage_warm",
        nominal_capacity=WARM_STORAGE_CAPACITY,
        min_storage_level=SPACE_HEATING_TEMPERATURE / WARM_STORAGE_CAPACITY,
        max_storage_level=0.60,  # maximum 60 °C
        balanced=True,
        loss_rate=0.01,
        inputs={bus_heat_warm: Flow()},
        outputs={bus_heat_warm: Flow()},
        inflow_conversion_factor=WARM_STORAGE_CONVERSION,
        outflow_conversion_factor=1 / WARM_STORAGE_CONVERSION,
    )

    es.add(bus_heat_warm, heating_rod, input_sol_warm, demand_sh, storage_warm)

    # Tap water (== 40°C, after flow heater)
    ########################################
    bus_heat_dhw = Bus(label="heat_dhw")

    demand_dhw = Sink(
        label="output_DHW",
        inputs={
            bus_heat_dhw: Flow(
                nominal_capacity=1,
                fix=input_data["Warm Water (kW)"],
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
            bus_heat_warm: Flow(
                nominal_capacity=HEAT_PUMP_NOMINAL_POWER,
                nonconvex=NonConvex(),
            ),
        },
    )

    flow_heater = Bus(
        label="flow_heater",
        inputs={bus_heat_warm: Flow()},
        outputs={bus_heat_dhw: Flow()},
    )

    p2h = Converter(
        label="P2H",
        inputs={bus_el: Flow()},
        outputs={flow_heater: Flow()},
        conversion_factors={flow_heater: 0.95},  # 95 % efficiency
    )

    es.add(heat_pump, flow_heater, p2h)

    # Pyomo constraints
    ###################
    model = Model(es)

    limit_active_flow_count_by_keyword(
        model,
        "solar_thermal",
        lower_limit=0,
        upper_limit=1,
    )

    def dhw_temperature_rule(m, ts):
        stor_temp = m.GenericStorageBlock.storage_content[storage_warm, ts + 1]
        return (m.flow[bus_heat_warm, flow_heater, ts]) <= (
            input_data["Warm Water (kW)"].iloc[ts]
            * (
                (stor_temp - FRESH_WATER_TEMPERATURE)
                / (TAP_WATER_TEMPERATURE - FRESH_WATER_TEMPERATURE)
            )
        )

    setattr(
        model,
        "dhw_temp_constrait",
        po.Constraint(
            model.TIMESTEPS,
            rule=dhw_temperature_rule,
        ),
    )

    def geothermal_power_rule(m, ts):
        geothermal_power = (
            DOWNHOLE_POWER
            / DOWNHOLE_DESIGN_DELTA
            * (
                input_data["temp_soil (°C)"].iloc[ts]
                - m.GenericStorageBlock.storage_content[storage_cold, ts + 1]
            )
        )
        return m.flow[input_geothermal, bus_heat_cold, ts] <= (
            geothermal_power
            + 10
            * DOWNHOLE_POWER
            * (  # some Big M
                1
                - m.NonConvexFlowBlock.status[
                    input_geothermal, bus_heat_cold, ts
                ]
            )
        )

    setattr(
        model,
        "geothermal_power_constrait",
        po.Constraint(
            model.TIMESTEPS,
            rule=geothermal_power_rule,
        ),
    )

    def solar_power_cold_rule(m, ts):
        Q_st_raw = VIRUTAL_THERMAL_TRANSMITTANCE * (
            input_data["temp_air (°C)"].iloc[ts]
            + input_data["radiation (kW/m2)"].iloc[ts] / HEAT_LOSS_COEFFIANT
            - m.GenericStorageBlock.storage_content[storage_cold, ts + 1]
        )
        return m.flow[input_sol_cold, bus_heat_cold, ts] <= (
            Q_st_raw
            + (
                1
                - m.NonConvexFlowBlock.status[
                    input_sol_cold, bus_heat_cold, ts
                ]
            )
            * SOLAR_COLLECTOR_BIG_M
        )

    setattr(
        model,
        "solar_power_cold_constraint",
        po.Constraint(
            model.TIMESTEPS,
            rule=solar_power_cold_rule,
        ),
    )

    def solar_power_warm_rule(m, ts):
        Q_st_raw = VIRUTAL_THERMAL_TRANSMITTANCE * (
            input_data["temp_air (°C)"].iloc[ts]
            + input_data["radiation (kW/m2)"].iloc[ts] / HEAT_LOSS_COEFFIANT
            - m.GenericStorageBlock.storage_content[storage_warm, ts + 1]
        )
        return m.flow[input_sol_warm, bus_heat_warm, ts] <= (
            Q_st_raw
            + (
                1
                - m.NonConvexFlowBlock.status[
                    input_sol_warm, bus_heat_warm, ts
                ]
            )
            * SOLAR_COLLECTOR_BIG_M
        )

    setattr(
        model,
        "solar_power_warm_constraint",
        po.Constraint(
            model.TIMESTEPS,
            rule=solar_power_warm_rule,
        ),
    )

    def limit_cop_rule(m, ts):
        return m.flow[bus_el, heat_pump, ts] >= (
            HEAT_PUMP_NOMINAL_POWER
            / HEAT_PUMP_EFFICIENCY
            * (
                m.NonConvexFlowBlock.status[heat_pump, bus_heat_warm, ts]
                - celsius2kelvin(
                    m.GenericStorageBlock.storage_content[storage_cold, ts + 1]
                )
                / celsius2kelvin(HEAT_PUMP_OUTLET_TEMPERATURE)
            )
        )

    setattr(
        model,
        "heat_pump_cop_constraint",
        po.Constraint(
            model.TIMESTEPS,
            rule=limit_cop_rule,
        ),
    )

    setattr(
        model,
        "storage_disallows_heat_pump_outlet",
        Var(model.TIMESTEPS, domain=po.Binary, bounds=(0, 1)),
    )

    # analogue to storage_level_constraint
    def storage_hot_rule(m, ts):
        return (
            m.GenericStorageBlock.storage_content[storage_warm, ts + 1]
            - HEAT_PUMP_OUTLET_TEMPERATURE
        ) <= m.storage_disallows_heat_pump_outlet[ts] * WARM_STORAGE_CAPACITY

    setattr(
        model,
        "hot_storage_constraint",
        po.Constraint(
            model.TIMESTEPS,
            rule=storage_hot_rule,
        ),
    )

    def limit_hp_usage_rule(m, ts):
        return (
            m.NonConvexFlowBlock.status[heat_pump, bus_heat_warm, ts]
            <= 1 - m.storage_disallows_heat_pump_outlet[ts]
        )

    setattr(
        model,
        "hot_pump_constraint",
        po.Constraint(
            model.TIMESTEPS,
            rule=limit_hp_usage_rule,
        ),
    )

    # Optimisation and plotting
    ###########################

    cmdlineoptions = {
        "cbc": {
            "seconds": SOLVER_TIME_LIMIT,
        },
        "highs": {
            "time_limit": SOLVER_TIME_LIMIT,
        },
    }

    model.solve(
        solver=SOLVER,
        solve_kwargs={"tee": True},
        cmdline_options=cmdlineoptions.get(SOLVER, {}),
        allow_nonoptimal=True,
    )

    # Workaround: manual creation because of non-optimal result
    results = Results(model, solver_info=None)

    flows = results["flow"]
    temperature = results["storage_content"]

    fig, (ax0, ax1) = plt.subplots(
        2,
        1,
        height_ratios=[2, 1],
        figsize=(10, 3),
        layout="tight",
        sharex=True,
    )

    heatsource_plot_data = [
        ("Geotehrmal", flows[(input_geothermal, bus_heat_cold)], "tab:brown"),
        ("Cold Solar", flows[(input_sol_cold, bus_heat_cold)], "tab:blue"),
        ("Warm Solar", flows[(input_sol_warm, bus_heat_warm)], "tab:orange"),
        ("Heat Pump (el.)", flows[(bus_el, heat_pump)], "tab:green"),
        ("Heating Rod", flows[(heating_rod, bus_heat_warm)], "tab:cyan"),
        ("Flow Heater", flows[(p2h, flow_heater)], "tab:pink"),
    ]

    plot_heat_flow_stack(ax0, flows, heatsource_plot_data)

    ax0.step(
        input_data.index,
        input_data["Space Heating (kW)"] + input_data["Warm Water (kW)"],
        color="k",
        ls="-",
    )
    ax0.step(
        input_data.index,
        input_data["Space Heating (kW)"],
        color="k",
        ls="--",
    )
    ax0.set_ylabel("Heat Flow (kW)")

    ax1.plot(temperature[storage_cold], "b-")
    ax1.set_ylim(-5, 10)
    ax1.tick_params(axis="y", colors="blue")
    ax1.spines["left"].set_color("blue")
    ax1.set_ylabel("Storage (°C)")

    ax2 = ax1.twinx()
    ax2.plot(temperature[storage_warm], "-", color="orange")
    ax2.set_ylim(30, 45)
    ax2.tick_params(axis="y", colors="orange")
    ax2.spines["right"].set_color("orange")
    ax2.spines["left"].set_color("blue")
    ax2.grid()
    ax2.set_xlim(temperature.index[0], temperature.index[-1])

    ax2.xaxis.set_major_formatter(
        mdates.DateFormatter(
            "%b %d",
            tz=timezone("Europe/Berlin"),
        )
    )
    # remove last day tick
    ax2.xaxis.get_major_ticks()[-1].label1.set_visible(False)
    fig.autofmt_xdate(rotation=0, ha="left")

    fig.savefig(
        os.path.join(
            os.path.dirname(__file__),
            f"discrete_volume_{START_TIME.replace(':','-')}"
            + f"_{END_TIME.replace(':','-')}.eps",
        )
    )

    plt.show()


if __name__ == "__main__":
    main()
