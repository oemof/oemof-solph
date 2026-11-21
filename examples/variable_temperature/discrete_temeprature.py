# SPDX-FileCopyrightText: Geert Petrin
# SPDX-FileCopyrightText: Patrik Schönfeldt
# SPDX-FileCopyrightText: DLR e.V.
#
# SPDX-License-Identifier: MIT

"""
General description
-------------------

This is a rather advanced example that shows how temepratures can be considered
as discretised variable in optimisation models fo the heat sector.
It complements a publication that can be found at https://elib.dlr.de/216784/.
Using multiple discrete temperatures is easier and faster than explicitly using
temperatures as variables (see other example).

The convention in this script is to annotate Flow units (kW or m³/h),
storage units have volume (m³) as their unit, which is assumed to be
equivalent to mass.
"""

import os

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

from oemof.solph import Bus
from oemof.solph import EnergySystem
from oemof.solph import Flow
from oemof.solph import Flow
from oemof.solph import Model
from oemof.solph import NonConvex
from oemof.solph import Results
from oemof.solph.components import Converter
from oemof.solph.components import GenericStorage
from oemof.solph.components import Sink
from oemof.solph.components import Source
from oemof.solph.constraints import limit_active_flow_count_by_keyword
from oemof.solph.constraints import shared_limit

from _shared import celsius2kelvin
from _shared import kcal2kilowatthours
from _shared import prepare_input_data
from _shared import plot_heat_flow_stack


def main():
    START_TIME = "2017-02-01T00:00:00"
    END_TIME = "2017-02-10T23:00:00"

    SOLVER = "highs"  # could also be e.g. "cbc"
    SOLVER_TIME_LIMIT = 300  # seconds

    COLD_STORAGE_VOLUME = 50  # m³
    WARM_STORAGE_VOLUME = 50  # m³

    FRESH_WATER_TEMPERATURE = 10  # °C
    COLD_STORAGE_TEMPERATURE = 15  # °C
    SPACE_HEATING_TEMPERATURE = 30  # °C
    TAP_WATER_TEMPERATURE = 40  # °C

    HEAT_PUMP_NOMINAL_POWER = 200  # kW
    HEAT_PUMP_EFFICIENCY = 0.45

    DOWNHOLE_POWER = 200  # kW

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

    def Q_st_raw(target_temperature: float) -> pd.Series:
        return VIRUTAL_THERMAL_TRANSMITTANCE * (
            input_data["temp_air (°C)"]
            + input_data["radiation (kW/m2)"] / HEAT_LOSS_COEFFIANT
            - target_temperature
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
    es.add(bus_el, input_grid_el)

    # Cold solar collector heat (15 °C, before heat pump)
    # We use freezing point (0 °C) as reference point.
    ####################################################################

    bus_heat_cold = Bus(label=f"heat_{COLD_STORAGE_TEMPERATURE}")

    input_sol_cold = Source(
        label="Collector cold",
        outputs={
            bus_heat_cold: Flow(
                nominal_capacity=1,
                maximum=Q_st_raw(COLD_STORAGE_TEMPERATURE).clip(lower=0),
                nonconvex=NonConvex(),
                custom_properties={"solar_thermal": True},
            )
        },
    )

    COLD_STORAGE_CONVERSION = 1 / kcal2kilowatthours(
        1000 * (COLD_STORAGE_TEMPERATURE)
    )
    storage_cold = GenericStorage(
        label=f"storage_{COLD_STORAGE_TEMPERATURE}",
        nominal_capacity=COLD_STORAGE_VOLUME,
        balanced=True,
        loss_rate=0,
        inputs={bus_heat_cold: Flow()},
        outputs={bus_heat_cold: Flow()},
        inflow_conversion_factor=COLD_STORAGE_CONVERSION,
        outflow_conversion_factor=1 / COLD_STORAGE_CONVERSION,
    )

    es.add(bus_heat_cold, input_sol_cold, storage_cold)

    # As this one cannot feed into the storage, we keep it separate
    bus_gt = Bus(label="GT")
    input_geothermal = Source(
        label="downhole",
        outputs={bus_gt: Flow(nominal_capacity=DOWNHOLE_POWER)},
    )
    es.add(bus_gt, input_geothermal)

    # Warm heat (25°C, e.g. for space heating)
    # We use fresh water temperature (10 °C) as reference point.
    ############################################################
    bus_heat_sh = Bus(label=f"heat_{SPACE_HEATING_TEMPERATURE}")

    heating_rod = Converter(
        label="Heating Rod",
        inputs={bus_el: Flow()},
        outputs={bus_heat_sh: Flow()},
        conversion_factors={bus_heat_sh: 0.99},  #  99% efficiency
    )

    demand_sh = Sink(
        label="output_SH",
        inputs={
            bus_heat_sh: Flow(
                nominal_capacity=1,
                fix=input_data["Space Heating (kW)"],
            )
        },
    )

    input_sol_warm = Source(
        label="Collector Warm",
        outputs={
            bus_heat_sh: Flow(
                nominal_capacity=1,
                maximum=Q_st_raw(SPACE_HEATING_TEMPERATURE).clip(lower=0),
                nonconvex=NonConvex(),
                custom_properties={"solar_thermal": True},
            )
        },
    )

    WARM_STORAGE_CONVERSION = 1 / kcal2kilowatthours(
        1000 * (SPACE_HEATING_TEMPERATURE - FRESH_WATER_TEMPERATURE)
    )
    storage_warm = GenericStorage(
        label=f"storage_{SPACE_HEATING_TEMPERATURE}",
        nominal_capacity=WARM_STORAGE_VOLUME,
        balanced=True,
        loss_rate=0,
        inputs={bus_heat_sh: Flow()},
        outputs={bus_heat_sh: Flow()},
        inflow_conversion_factor=WARM_STORAGE_CONVERSION,
        outflow_conversion_factor=1 / WARM_STORAGE_CONVERSION,
    )

    es.add(bus_heat_sh, heating_rod, demand_sh, storage_warm, input_sol_warm)

    # Hot heat (40°C, e.g. for tap water)
    # We use fresh water temperature (10 °C) as reference point.
    ############################################################

    bus_heat_dhw = Bus(label=f"heat_{TAP_WATER_TEMPERATURE}")

    ALREADY_HEATED_FRACTION = (
        SPACE_HEATING_TEMPERATURE - FRESH_WATER_TEMPERATURE
    ) / (TAP_WATER_TEMPERATURE - FRESH_WATER_TEMPERATURE)
    flow_heater = Converter(
        label="flow_heater",
        inputs={bus_el: Flow(), bus_heat_sh: Flow()},
        outputs={bus_heat_dhw: Flow()},
        conversion_factors={
            bus_heat_sh: ALREADY_HEATED_FRACTION,
            bus_el: (1 - ALREADY_HEATED_FRACTION) / 0.95,  #  95% efficiency
        },
    )

    DHW_STORAGE_CONVERSION = 1 / kcal2kilowatthours(
        1000 * (TAP_WATER_TEMPERATURE - FRESH_WATER_TEMPERATURE)
    )
    # other subvolume of storage_warm
    storage_dhw = GenericStorage(
        label=f"storage_{TAP_WATER_TEMPERATURE}",
        nominal_capacity=WARM_STORAGE_VOLUME,
        balanced=True,
        loss_rate=0,
        inputs={bus_heat_sh: Flow()},
        outputs={bus_heat_sh: Flow()},
        inflow_conversion_factor=DHW_STORAGE_CONVERSION,
        outflow_conversion_factor=1 / DHW_STORAGE_CONVERSION,
    )

    input_sol_dhw = Source(
        label="Collector Hot",
        outputs={
            bus_heat_dhw: Flow(
                nominal_capacity=1,
                maximum=Q_st_raw(TAP_WATER_TEMPERATURE).clip(lower=0),
                nonconvex=NonConvex(),
                custom_properties={"solar_thermal": True},
            )
        },
    )

    demand_dhw = Sink(
        label="output_DHW",
        inputs={
            bus_heat_dhw: Flow(
                nominal_capacity=1,
                fix=input_data["Warm Water (kW)"],
            ),
        },
    )
    es.add(bus_heat_dhw, flow_heater, demand_dhw, storage_dhw, input_sol_dhw)

    # heat pump
    #
    # the heat pump consists of multiple converters,
    # one for each operational mode
    ###########

    # We limit the total power by copying all heat output here.
    bus_hp_output = Bus(label="HP heat")
    sink_hp_output = Sink(
        label="HP produced",
        inputs={bus_hp_output: Flow(nominal_capacity=HEAT_PUMP_NOMINAL_POWER)},
    )

    heat_pump_el = Bus(
        label="HP electricity in",
        inputs={bus_el: Flow()},
    )

    cop_gt_sh = HEAT_PUMP_EFFICIENCY / (
        1
        - celsius2kelvin(input_data["temp_soil (°C)"])
        / celsius2kelvin(SPACE_HEATING_TEMPERATURE)
    )
    hp_gt_sh = Converter(
        label=f"HP_GT_{SPACE_HEATING_TEMPERATURE}",
        inputs={
            heat_pump_el: Flow(),
            bus_gt: Flow(),
        },
        outputs={
            bus_heat_sh: Flow(),
            bus_hp_output: Flow(),
        },
        conversion_factors={
            heat_pump_el: 1 / cop_gt_sh,
            bus_gt: 1 - 1 / cop_gt_sh,
        },
    )

    es.add(bus_hp_output, sink_hp_output, heat_pump_el)

    cop_gt_dhw = HEAT_PUMP_EFFICIENCY / (
        1
        - celsius2kelvin(input_data["temp_soil (°C)"])
        / celsius2kelvin(TAP_WATER_TEMPERATURE)
    )
    hp_gt_dhw = Converter(
        label=f"HP_GT_{TAP_WATER_TEMPERATURE}",
        inputs={
            heat_pump_el: Flow(),
            bus_gt: Flow(),
        },
        outputs={
            bus_heat_dhw: Flow(),
            bus_hp_output: Flow(),
        },
        conversion_factors={
            heat_pump_el: 1 / cop_gt_dhw,
            bus_gt: 1 - 1 / cop_gt_dhw,
        },
    )

    cop_cold_sh = HEAT_PUMP_EFFICIENCY / (
        1
        - celsius2kelvin(COLD_STORAGE_TEMPERATURE)
        / celsius2kelvin(SPACE_HEATING_TEMPERATURE)
    )
    hp_cold_sh = Converter(
        label=f"HP_{COLD_STORAGE_TEMPERATURE}_{SPACE_HEATING_TEMPERATURE}",
        inputs={
            heat_pump_el: Flow(),
            bus_heat_cold: Flow(),
        },
        outputs={
            bus_heat_sh: Flow(),
            bus_hp_output: Flow(),
        },
        conversion_factors={
            heat_pump_el: 1 / cop_cold_sh,
            bus_heat_cold: 1 - 1 / cop_cold_sh,
        },
    )

    cop_cold_dhw = HEAT_PUMP_EFFICIENCY / (
        1
        - celsius2kelvin(COLD_STORAGE_TEMPERATURE)
        / celsius2kelvin(TAP_WATER_TEMPERATURE)
    )
    hp_cold_dhw = Converter(
        label=f"HP_{COLD_STORAGE_TEMPERATURE}_{TAP_WATER_TEMPERATURE}",
        inputs={
            heat_pump_el: Flow(),
            bus_heat_cold: Flow(),
        },
        outputs={
            bus_heat_dhw: Flow(),
            bus_hp_output: Flow(),
        },
        conversion_factors={
            heat_pump_el: 1 / cop_cold_dhw,
            bus_heat_cold: 1 - 1 / cop_cold_dhw,
        },
    )

    es.add(hp_gt_sh, hp_gt_dhw, hp_cold_sh, hp_cold_dhw)

    # Pyomo constraints
    ###################
    model = Model(es)

    limit_active_flow_count_by_keyword(
        model,
        "solar_thermal",
        lower_limit=0,
        upper_limit=1,
    )

    shared_limit(
        model=model,
        quantity=model.GenericStorageBlock.storage_content,
        limit_name=f"combined_warm_storage_limit",
        components=[storage_dhw, storage_warm],
        weights=[1, 1],
        lower_limit=0,
        upper_limit=WARM_STORAGE_VOLUME,
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
    storage_content = results["storage_content"]

    fig, (ax0, ax1, ax2) = plt.subplots(
        3,
        1,
        height_ratios=[2, 1, 1],
        figsize=(10, 4),
        layout="tight",
        sharex=True,
    )

    heatsource_plot_data = [
        ("Geotehrmal", flows[(input_geothermal, bus_gt)], "tab:brown"),
        ("Cold Solar", flows[(input_sol_cold, bus_heat_cold)], "tab:purple"),
        (
            f"Solar ({SPACE_HEATING_TEMPERATURE}°C)",
            flows[(input_sol_warm, bus_heat_sh)],
            "tab:red",
        ),
        (
            f"Solar ({TAP_WATER_TEMPERATURE}°C)",
            flows[(input_sol_dhw, bus_heat_dhw)],
            "tab:orange",
        ),
        ("Heat Pump (el.)", flows[(bus_el, heat_pump_el)], "tab:green"),
        ("Heating Rod", flows[(heating_rod, bus_heat_sh)], "tab:cyan"),
        ("Flow Heater", flows[(bus_el, flow_heater)], "tab:pink"),
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

    ax1.fill_between(
        storage_content.index,
        0,
        WARM_STORAGE_VOLUME
        - storage_content[f"storage_{SPACE_HEATING_TEMPERATURE}"]
        - storage_content[f"storage_{TAP_WATER_TEMPERATURE}"],
        color="tab:purple",
    )
    ax1.fill_between(
        storage_content.index,
        WARM_STORAGE_VOLUME
        - storage_content[f"storage_{SPACE_HEATING_TEMPERATURE}"]
        - storage_content[f"storage_{TAP_WATER_TEMPERATURE}"],
        WARM_STORAGE_VOLUME
        - storage_content[f"storage_{TAP_WATER_TEMPERATURE}"],
        color="tab:red",
    )
    ax1.fill_between(
        storage_content.index,
        WARM_STORAGE_VOLUME
        - storage_content[f"storage_{TAP_WATER_TEMPERATURE}"],
        WARM_STORAGE_VOLUME,
        color="tab:orange",
    )

    ax2.fill_between(
        storage_content.index,
        0,
        COLD_STORAGE_VOLUME
        - storage_content[f"storage_{COLD_STORAGE_TEMPERATURE}"],
        color="tab:blue",
    )
    ax2.fill_between(
        storage_content.index,
        COLD_STORAGE_VOLUME
        - storage_content[f"storage_{COLD_STORAGE_TEMPERATURE}"],
        COLD_STORAGE_VOLUME,
        color="tab:purple",
    )
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%d"))
    ax2.set_xlim(storage_content.index[0], storage_content.index[-1])

    fig.savefig(
        os.path.join(
            os.path.dirname(__file__),
            f"discrete_temperature_{START_TIME.replace(':','-')}"
            + f"_{END_TIME.replace(':','-')}.eps",
        )
    )

    plt.show()


if __name__ == "__main__":
    main()
