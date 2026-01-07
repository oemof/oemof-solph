# -*- coding: utf-8 -*-

"""
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: DLR e.V.

SPDX-License-Identifier: MIT
"""

import logging
import warnings
from collections import namedtuple
from datetime import datetime
from pathlib import Path

import pandas as pd
import pytz
from cost_data import discounted_average_price
from cost_data import energy_prices
from cost_data import investment_costs
from create_timeseries import reshape_unevenly
from oemof.network import graph
from oemof.tools import debugging
from oemof.tools import logger
from oemof.tools.economics import annuity
from shared import get_parameter
from shared import prepare_input_data

from oemof.solph import Bus
from oemof.solph import EnergySystem
from oemof.solph import Flow
from oemof.solph import Investment
from oemof.solph import Model
from oemof.solph import Results
from oemof.solph import components as cmp

warnings.filterwarnings(
    "ignore", category=debugging.ExperimentalFeatureWarning
)
logger.define_logging()


def calculate_annuity(value):
    return value / 20


def calculate_fix_cost(value):
    return value / 20


def prepare_technical_data(minutes, url, port):
    data = namedtuple("data", "even uneven")
    data_table = (
        prepare_input_data(proxy_url=url, proxy_port=port)
        .resample(f"{minutes} min")
        .mean()
    )
    df_un = reshape_unevenly(data_table)
    return data(even=data_table, uneven=df_un)


def prepare_cost_data():
    pass


def solve_model(data, parameter, year=2025, es=None):
    if es is None:
        es = EnergySystem(timeindex=data.index)

    var_cost = discounted_average_price(
        price_series=energy_prices(),
        observation_period=parameter["n"],
        interest_rate=parameter["r"],
        year_of_investment=year,
    )
    invest_cost = investment_costs().loc[year]

    # Create Investment objects from cost data
    investments = {}
    for key in ["gas boiler", "heat pump", "battery", "pv"]:
        try:
            epc = annuity(
                invest_cost[(key, "specific_costs [Eur/kW]")],
                parameter["n"],
                parameter["r"],
            )
        except KeyError:
            epc = annuity(
                invest_cost[(key, "specific_costs [Eur/kWh]")],
                parameter["n"],
                parameter["r"],
            )
        fix_cost = calculate_fix_cost(invest_cost[(key, "fixed_costs [Eur]")])
        if key == "pv":
            maxi = parameter["max_capacity_pv"]
        else:
            maxi = float("+inf")
        investments[key] = Investment(
            ep_costs=epc, fixed_costs=fix_cost, maximum=maxi
        )

    # Buses
    bus_el = Bus(label="electricity")
    bus_heat = Bus(label="heat")
    bus_gas = Bus(label="gas")
    es.add(bus_el, bus_heat, bus_gas)

    # Sources
    es.add(
        cmp.Source(
            label="PV",
            outputs={
                bus_el: Flow(
                    fix=data["PV (kW/kWp)"],
                    nominal_capacity=investments["pv"],
                )
            },
        )
    )
    es.add(
        cmp.Source(
            label="Grid import",
            outputs={
                bus_el: Flow(
                    variable_costs=var_cost["electricity_prices [Eur/kWh]"]
                )
            },
        )
    )
    es.add(
        cmp.Source(
            label="Gas import",
            outputs={
                bus_gas: Flow(variable_costs=var_cost["gas_prices [Eur/kWh]"])
            },
        )
    )

    # Battery
    es.add(
        cmp.GenericStorage(
            label="Battery",
            inputs={bus_el: Flow()},
            outputs={bus_el: Flow()},
            nominal_capacity=investments["battery"],  # kWh
            loss_rate=parameter["loss_rate_battery"],  # 0.1%/h
            inflow_conversion_factor=parameter["charge_efficiency_battery"],
            outflow_conversion_factor=parameter[
                "discharge_efficiency_battery"
            ],
        )
    )

    # Sinks
    es.add(
        cmp.Sink(
            label="Heat demand",
            inputs={
                bus_heat: Flow(
                    fix=data["heat demand (kW)"],
                    nominal_capacity=1,
                )
            },
        )
    )
    es.add(
        cmp.Sink(
            label="Electricity demand",
            inputs={
                bus_el: Flow(
                    fix=data["electricity demand (kW)"],
                    nominal_capacity=1,
                )
            },
        )
    )
    es.add(
        cmp.Sink(
            label="Electric Vehicle",
            inputs={
                bus_el: Flow(
                    fix=data["Electricity for Car Charging_HH1"],
                    nominal_capacity=1,
                )
            },
        )
    )
    es.add(
        cmp.Sink(
            label="Grid Feed-in",
            inputs={
                bus_el: Flow(variable_costs=var_cost["pv_feed_in [Eur/kWh]"])
            },
        )
    )

    # Heat Pump
    es.add(
        cmp.Converter(
            label="Heat pump",
            inputs={bus_el: Flow()},
            outputs={
                bus_heat: Flow(nominal_capacity=investments["heat pump"])
            },
            conversion_factors={bus_heat: data["cop"]},
        )
    )
    # Gas Boiler
    es.add(
        cmp.Converter(
            label="Gas Boiler",
            inputs={bus_gas: Flow()},
            outputs={
                bus_heat: Flow(nominal_capacity=investments["gas boiler"])
            },
            conversion_factors={bus_heat: parameter["efficiency_boiler"]},
        )
    )

    graph.create_nx_graph(es, filename=Path(Path.home(), "test_graph.graphml"))

    # Create Model and solve it
    logging.info("Creating Model...")
    m = Model(es)
    logging.info("Solving Model...")
    m.solve(solver="cbc", solve_kwargs={"tee": False})

    # Create Results
    return Results(m)


def process_results(results):
    flow = results["flow"]
    year = flow.index[0].year

    end_time = pytz.utc.localize(
        datetime.strptime(f"{year + 1}-01-01 00:00", "%Y-%m-%d %H:%M")
    )
    time_intervals = pd.Series(
        flow.index.diff().seconds / 3600, index=flow.index
    ).shift(-1)
    time_intervals.iloc[-1] = (end_time - flow.index[-2]).seconds / 3600 - 1
    print(time_intervals)
    print(flow.mul(time_intervals, axis=0).sum())

    soc = results["storage_content"]
    soc.name = "Battery SOC [kWh]"
    investments = results["invest"].rename(
        columns={
            c: c[0].label
            for c in results["invest"].columns
            if isinstance(c, tuple)
        },
    )
    return investments


def optimise_investment(year, interval, result_path):
    result_file = f"time_series_even_uneven_{year}_{interval}min.csv"
    result_fn = Path(result_path, result_file)

    if not result_fn.is_file():
        # Create empty file
        file = open(result_fn, "w")
        file.write(f"Start with {year} - {interval}")
        file.close()

        my_data = prepare_technical_data(interval, None, None)
        start = datetime.now()
        results_even = solve_model(my_data.even, get_parameter(), year=year)
        time_even = datetime.now() - start
        start = datetime.now()
        results_uneven = solve_model(my_data.uneven, get_parameter(), year=year)
        time_uneven = datetime.now() - start
        key_results_even = process_results(results_even)
        key_results_even["time"] = time_even.seconds
        key_results_even["objective"] = results_even["objective"]
        key_results_even["short_interval"] = interval
        key_results_even["year_of_investment"] = year
        key_results_uneven = process_results(results_uneven)
        key_results_uneven["time"] = time_uneven.seconds
        key_results_uneven["objective"] = results_uneven["objective"]
        key_results_uneven["short_interval"] = interval
        key_results_uneven["year_of_investment"] = year
        results = (
            pd.concat(
                [key_results_uneven, key_results_even],
                keys=["uneven", "even"],
            )
            .droplevel(1)
            .T
        )
        results.to_csv(result_fn)

        # compare_results(results_even, results_uneven)
        print()
        print("*** Investment ***")
        print("even\n", key_results_even.iloc[0])
        print("uneven\n", key_results_uneven.iloc[0])
        print()
        print("*** Times ****")
        print("even", time_even)
        print("uneven", time_uneven)


def read_result_files(year, interval, result_path):
    result_file = f"time_series_even_uneven_{year}_{interval}min.csv"
    temp = pd.read_csv(Path(result_path, result_file), index_col=[0])
    temp = pd.concat([temp], keys=[interval], axis=1)
    return pd.concat([temp], keys=[year], axis=1)


if __name__ == "__main__":
    my_result_path = Path(Path.home(), ".oemof", "tutorial", "time_series")
    my_result_path.mkdir(exist_ok=True)
    intervals = [60]
    years = [2025]

    for my_year in years:
        for my_interval in intervals:
            optimise_investment(my_year, my_interval, my_result_path)

    df = pd.DataFrame()
    for my_year in years:
        for my_interval in intervals:
            df = pd.concat(
                [df, read_result_files(my_year, my_interval, my_result_path)],
                axis=1,
            )

    df.sort_index(axis=1).to_csv(Path(my_result_path, "results_all.csv"))
