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
from matplotlib import pyplot as plt
from oemof.network import graph
from oemof.tools import debugging
from oemof.tools import logger
from oemof.tools.economics import annuity
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
    df = (
        prepare_input_data(proxy_url=url, proxy_port=port)
        .resample(f"{minutes} min")
        .mean()
    )
    df_un = reshape_unevenly(df)
    return data(even=df, uneven=df_un)


def prepare_cost_data():
    pass


def solve_model(data, year=2025, es=None, n=20, r=0.05):
    if es is None:
        es = EnergySystem(timeindex=data.index)

    var_cost = discounted_average_price(energy_prices(), r, n, year)
    invest_cost = investment_costs().loc[year]

    # Create Investment objects from cost data
    investments = {}
    for key in ["gas boiler", "heat pump", "battery", "pv"]:
        try:
            epc = annuity(invest_cost[(key, "specific_costs [Eur/kW]")], n, r)
        except KeyError:
            epc = annuity(invest_cost[(key, "specific_costs [Eur/kWh]")], n, r)
        fix_cost = calculate_fix_cost(invest_cost[(key, "fixed_costs [Eur]")])
        investments[key] = Investment(ep_costs=epc, fixed_costs=fix_cost)

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
            label="Shortage_heat", outputs={bus_heat: Flow(variable_costs=99)}
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
                bus_el: Flow(variable_costs=var_cost["gas_prices [Eur/kWh]"])
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
            min_storage_level=0.0,
            max_storage_level=1.0,
            balanced=True,
            loss_rate=0.001,  # 0.1%/h
            inflow_conversion_factor=0.95,  # Lade-Wirkungsgrad
            outflow_conversion_factor=0.95,  # Entlade-Wirkungsgrad
        )
    )

    # Sinks
    es.add(cmp.Sink(label="Excess_el", inputs={bus_el: Flow()}))
    es.add(cmp.Sink(label="Excess_heat", inputs={bus_heat: Flow()}))
    es.add(
        cmp.Sink(
            label="Heat demand",
            inputs={
                bus_heat: Flow(
                    fix=data["heat demand (kW)"], nominal_capacity=5.0
                )
            },
        )
    )
    es.add(
        cmp.Sink(
            label="Electricity demand",
            inputs={
                bus_el: Flow(
                    fix=data["electricity demand (kW)"], nominal_capacity=1.0
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
                    nominal_capacity=1.0,
                )
            },
        )
    )
    es.add(
        cmp.Sink(
            label="Grid Feed-in",
            inputs={
                bus_el: Flow(
                    variable_costs=-var_cost["pv_feed_in [Eur/kWh]"] / 1000
                )
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
            conversion_factors={bus_heat: data["cop"]},
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
    intervals = pd.Series(
        flow.index.diff().seconds / 3600, index=flow.index
    ).shift(-1)
    intervals.iloc[-1] = (end_time - flow.index[-2]).seconds / 3600 - 1

    # print(flow.mul(intervals, axis=0).sum())

    soc = results["storage_content"]
    soc.name = "Battery SOC [kWh]"
    investments = results["invest"].rename(
        columns={
            c: c[0].label
            for c in results["invest"].columns
            if isinstance(c, tuple)
        },
    )
    print(investments)


def compare_results(even, uneven):
    flow_e = even["flow"]
    flow_u = uneven["flow"]
    # print(flow_e)
    # print(flow_u)


#
# # interval_hours = df.groupby(buckets).size().sort_index()
# # interval_hours.name = 'interval_hours'
#
#
# print("Energy Balance")
# print(flow.sum())
# print("")
# print("Investment")
# print(investments.squeeze())

# investments.squeeze().plot(kind="bar")
#
# day = 186  # day of the year
# n = 2  # number of days to plot
# flow = flow[day * 24 * 6 : day * 24 * 6 + n * 24 * 6]
# soc = soc[day * 24 * 6 : day * 24 * 6 + 48 * 6]
#
# supply = flow[[c for c in flow.columns if c[1].label == "electricity"]]
# supply = supply.droplevel(1, axis=1)
# supply.rename(columns={c: c.label for c in supply.columns}, inplace=True)
# demand = flow[[c for c in flow.columns if c[0].label == "electricity"]]
# demand = demand.droplevel(0, axis=1)
# demand.rename(columns={c: c.label for c in demand.columns}, inplace=True)

if __name__ == "__main__":
    my_year = 2045
    my_data = prepare_technical_data(10, None, None)
    start = datetime.now()
    results_even = solve_model(my_data.even, year=my_year)
    time_even = datetime.now() - start
    start = datetime.now()
    results_uneven = solve_model(my_data.uneven, year=my_year)
    time_uneven = datetime.now() - start
    process_results(results_even)
    process_results(results_uneven)
    compare_results(results_even, results_uneven)
    print("*** Times ****")
    print("even", time_even)
    print("uneven", time_uneven)
