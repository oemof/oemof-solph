# SPDX-FileCopyrightText: Geert Petrin
# SPDX-FileCopyrightText: Patrik Schönfeldt
# SPDX-FileCopyrightText: DLR e.V.
#
# SPDX-License-Identifier: MIT

"""
shared helper functions for the scripts in this directory
"""

import os

import pandas as pd


def celsius2kelvin(temperature):
    return temperature + 273.15


def kcal2kilowatthours(energy_in_kcal: float) -> float:
    return 0.001162 * energy_in_kcal


def prepare_input_data(
    start_time=None,
    end_time=None,
) -> pd.DataFrame:
    demand_data = pd.read_csv(
        os.path.join(os.path.dirname(__file__), "demands.csv"),
        index_col=0,
        parse_dates=[0],
    )
    weather_data = pd.read_csv(
        os.path.join(os.path.dirname(__file__), "weather_dwd.csv"),
        index_col=0,
        parse_dates=[0],
    )

    demand_data = demand_data.resample("1h").sum()

    if start_time is None:
        start_time = demand_data.index[0]
    if end_time is None:
        end_time = demand_data.index[-1]

    prepared_data = pd.DataFrame(index=weather_data.index)
    prepared_data = prepared_data[start_time:end_time]

    prepared_data["temp_soil (°C)"] = 5  # easier for this example
    prepared_data["temp_air (°C)"] = weather_data["temp_air (°C)"]
    prepared_data["radiation (kW/m2)"] = weather_data["dni"] / 1000
    prepared_data["Warm Water (kW)"] = kcal2kilowatthours(
        30 * demand_data["Warm Water (l)"]
    )  # We assume 10 °C for fresh water and 40 °C for warm water.
    prepared_data["Space Heating (kW)"] = (
        demand_data["Space Heating (Wh)"] / 1e3
    )

    return prepared_data


def plot_heat_flow_stack(ax, flows, heatsource_plot_data):
    baseline = 0
    for _, data, _ in heatsource_plot_data:
        baseline += data

    # draw top to bottom to let zero width fils disappear
    for label, data, color in heatsource_plot_data[::-1]:
        ax.fill_between(
            flows.index,
            baseline - data,
            baseline,
            color=color,
            step="pre",
            label=label,
        )
        baseline -= data
