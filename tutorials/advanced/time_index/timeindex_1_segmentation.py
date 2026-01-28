# -*- coding: utf-8 -*-

"""
SPDX-FileCopyrightText: Uwe Krien
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
from input_data import discounted_average_price
from input_data import energy_prices
from input_data import get_parameter
from input_data import investment_costs
from input_data import prepare_input_data
from oemof.tools import debugging
from oemof.tools import logger
from oemof.tools.economics import annuity

from oemof import solph

warnings.filterwarnings(
    "ignore", category=debugging.ExperimentalFeatureWarning
)
logger.define_logging()


def calculate_fix_cost(value):
    return value / 20


def reshape_unevenly(data):
    def to_bucket(ts: pd.Timestamp) -> pd.Timestamp:
        h = ts.hour
        d = ts.normalize()
        if 5 <= h <= 20:
            return ts
        if h in (21, 22, 23):
            return d + pd.Timedelta(hours=21)
        if h in (0,):
            return (d - pd.Timedelta(days=1)) + pd.Timedelta(hours=21)
        # h in (1, 2, 3, 4, 5)
        return d + pd.Timedelta(hours=1)

    buckets = data.index.map(to_bucket)
    buckets = buckets.where(buckets >= data.index[0], data.index[0])

    data_mean = data.groupby(buckets).mean().sort_index()
    data_mean.index.name = "timestamp"

    return data_mean


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


def populate_and_solve_energy_system(
    es: solph.EnergySystem,
    time_series: dict[str, list] | dict[str, pd.DataFrame],
    investments: dict[str, solph.Investment],
    variable_costs: dict | pd.DataFrame,
    discount_rate=0.02,
):

    parameter = get_parameter()

    bus_el = solph.Bus(label="electricity")
    bus_heat = solph.Bus(label="heat")
    bus_gas = solph.Bus(label="gas")
    es.add(bus_el, bus_heat, bus_gas)

    es.add(
        solph.components.Source(
            label="PV",
            outputs={
                bus_el: solph.Flow(
                    fix=time_series["PV (kW/kWp)"],
                    nominal_capacity=investments["pv"],
                )
            },
        )
    )

    es.add(
        solph.components.GenericStorage(
            label="Battery",
            inputs={bus_el: solph.Flow()},
            outputs={bus_el: solph.Flow()},
            nominal_capacity=investments["battery"],  # kWh
            loss_rate=parameter["loss_rate_battery"],
            inflow_conversion_factor=parameter["charge_efficiency_battery"],
            outflow_conversion_factor=parameter[
                "discharge_efficiency_battery"
            ],
        )
    )

    es.add(
        solph.components.Sink(
            label="Electricity demand",
            inputs={
                bus_el: solph.Flow(
                    fix=time_series["electricity demand (kW)"],
                    nominal_capacity=1.0,
                )
            },
        )
    )

    wallbox_sink = solph.components.Sink(
        label="Electric Vehicle",
        inputs={
            bus_el: solph.Flow(
                fix=time_series["Electricity for Car Charging_HH1"],
                nominal_capacity=1.0,
            )
        },
    )
    es.add(wallbox_sink)

    hp = solph.components.Converter(
        label="Heat pump",
        inputs={bus_el: solph.Flow()},
        outputs={
            bus_heat: solph.Flow(nominal_capacity=investments["heat pump"])
        },
        conversion_factors={bus_heat: time_series["cop"]},
    )
    es.add(hp)

    gas_boiler = solph.components.Converter(
        label="Gas Boiler",
        inputs={bus_gas: solph.Flow()},
        outputs={
            bus_heat: solph.Flow(nominal_capacity=investments["gas boiler"])
        },
        conversion_factors={bus_heat: parameter["efficiency_boiler"]},
    )
    es.add(gas_boiler)

    heat_sink = solph.components.Sink(
        label="Heat demand",
        inputs={
            bus_heat: solph.Flow(
                fix=time_series["heat demand (kW)"],
                nominal_capacity=1.0,
            )
        },
    )
    es.add(heat_sink)

    grid_import = solph.components.Source(
        label="Grid import",
        outputs={
            bus_el: solph.Flow(
                variable_costs=variable_costs["electricity_prices [Eur/kWh]"]
            )
        },
    )
    es.add(grid_import)

    feed_in = solph.components.Sink(
        label="Grid Feed-in",
        inputs={
            bus_el: solph.Flow(
                variable_costs=variable_costs["pv_feed_in [Eur/kWh]"]
            )
        },
    )
    es.add(feed_in)

    gas_import = solph.components.Source(
        label="Gas import",
        outputs={
            bus_gas: solph.Flow(
                variable_costs=variable_costs["gas_prices [Eur/kWh]"]
            )
        },
    )
    es.add(gas_import)

    logging.info("Creating Model...")
    m = solph.Model(es, discount_rate=discount_rate)
    logging.info("Solving Model...")

    m.solve(solver="cbc", solve_kwargs={"tee": False})

    return m


def solve_model(data, parameter, year=2025, es=None):
    if es is None:
        es = solph.EnergySystem(timeindex=data.index)

    var_cost = discounted_average_price(
        price_series=energy_prices(),
        observation_period=parameter["n"],
        interest_rate=parameter["r"],
        year_of_investment=year,
    )
    investments = create_investment_objects(
        n=parameter["n"],
        r=parameter["r"],
        year=year,
    )
    m = populate_and_solve_energy_system(
        es=es,
        time_series=data,
        investments=investments,
        variable_costs=var_cost,
    )

    return solph.Results(m)


def create_investment_objects(n, r, year):
    invest_cost = investment_costs().loc[year]

    # Create Investment objects from cost data
    investments = {}
    for key in ["gas boiler", "heat pump", "battery", "pv"]:
        try:
            epc = annuity(
                invest_cost[(key, "specific_costs [Eur/kW]")],
                n=n,
                wacc=r,
            )
            maximum = invest_cost[(key, "maximum [kW]")]
        except KeyError:
            epc = annuity(
                invest_cost[(key, "specific_costs [Eur/kWh]")],
                n=n,
                wacc=r,
            )
            maximum = invest_cost[(key, "maximum [kWh]")]
        fix_cost = annuity(
            invest_cost[(key, "fixed_costs [Eur]")],
            n=n,
            wacc=r,
        )

        investments[key] = solph.Investment(
            ep_costs=epc,
            offset=fix_cost,
            maximum=maximum,
            lifetime=20,
            nonconvex=bool(fix_cost > 0),  # need to cast to avoid np.bool
        )
    return investments


def process_results(results):
    key_results = results["invest"].rename(
        columns={
            c: c[0].label
            for c in results["invest"].columns
            if isinstance(c, tuple)
        },
    )
    key_results["objective"] = results["objective"]
    return key_results


def optimise_investment(year, interval, result_path):
    result_file = f"time_series_even_uneven_{year}_{interval}min.csv"
    result_fn = Path(result_path, result_file)

    if not result_fn.is_file():
        logging.info(f"Start with {year} - {interval}")
        # Create empty file
        file = open(result_fn, "w")
        file.write(f"Start with {year} - {interval}")
        file.close()
        my_data = prepare_technical_data(interval, None, None)

        logging.info("Start with even....")
        start = datetime.now()
        results_even = solve_model(my_data.even, get_parameter(), year=year)
        key_results_even = process_results(results_even)
        key_results_even["short_interval"] = interval
        key_results_even["year_of_investment"] = year
        time_even = datetime.now() - start
        key_results_even["time"] = time_even.seconds

        logging.info("Start with uneven....")
        start = datetime.now()
        results_uneven = solve_model(
            my_data.uneven, get_parameter(), year=year
        )
        key_results_uneven = process_results(results_uneven)
        time_uneven = datetime.now() - start
        key_results_uneven["time"] = time_uneven.seconds

        logging.info("Create joined results.")
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
    my_result_path.mkdir(parents=True, exist_ok=True)
    intervals = [60, 30, 15, 10, 5, 1]
    years = [2025, 2035, 2045]

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
