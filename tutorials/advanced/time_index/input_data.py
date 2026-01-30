"""
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: DLR e.V.

SPDX-License-Identifier: MIT
"""

import datetime
from os import environ
from pathlib import Path
import requests

import demandlib
import numpy as np
import pandas as pd
from oemof.tools.economics import annuity
from workalendar.europe import Germany

PROXY_SET = False


def set_proxy(url, port):
    proxy = f"{url}:{port}"
    environ["http_proxy"] = proxy
    environ["https_proxy"] = proxy


def get_parameter():
    return {
        "n": 20,
        "r": 0.05,
        "efficiency_boiler": 0.90,
        "loss_rate_battery": 0.001,
        "charge_efficiency_battery": 0.95,
        "discharge_efficiency_battery": 0.95,
    }


def prepare_input_data(proxy_url=None, proxy_port=None):
    # ToDo: Mobilitätszeitreihe, die zu den Daten passt.

    print(
        "Data is licensed from M. Schlemminger, T. Ohrdes, E. Schneider,"
        " and M. Knoop. Under Creative Commons Attribution 4.0 International"
        " License. It is also available at doi: 10.5281/zenodo.5642902."
        " (We use building 27 plus the south-facing PV"
        " from that dataset.)"
    )

    url = {
        "temperature.csv": "https://oemof.org/wp-content/uploads/2025/12/temperature.csv",
        "energy.csv": "https://oemof.org/wp-content/uploads/2026/01/energy.csv",
        "car_charging.csv": "https://oemof.org/wp-content/uploads/2026/01/"
        + "car_charging_with_7kW_minute.csv",
    }

    global PROXY_SET
    if PROXY_SET is False and proxy_url is not None:
        set_proxy(url=proxy_url, port=proxy_port)
        PROXY_SET = True

    def _get_data(filename):
        file_path = Path(__file__).parent
        file_path = Path(file_path, filename)
        if not file_path.exists():
            data_file = open(file_path, "w")
            data_file.write(requests.get(url[filename], timeout=10).text)
            data_file.close()
        df = pd.read_csv(
            file_path,
            index_col=0,
        )
        return df

    def _temperature_dataframe():
        temperature = _get_data("temperature.csv")

        temperature.index = pd.to_datetime(
            temperature.index,
            unit="s",
            utc=True,
        )

        temperature[temperature == np.inf] = np.nan
        temperature = temperature[10:].resample("1 min").mean()
        return temperature

    def _energy_dataframe():
        energy = _get_data("energy.csv")

        energy.index = pd.to_datetime(
            energy.index,
            unit="s",
            utc=True,
        )

        energy[energy == np.inf] = np.nan

        energy = energy.resample("1 min").mean()
        return energy

    df = pd.concat([_energy_dataframe(), _temperature_dataframe()], axis=1)

    df = df.interpolate()

    building_area = 110  # m² (from publication)
    specific_heat_demand = 60  # kWh/m²/a  (educated guess)
    holidays = dict(Germany().holidays(2019))

    # We estimate the heat demand from the ambient temperature using demandlib.
    # This returns energy per time step in units of kWh, but we want kW.
    df["heat demand (kW)"] = (
        demandlib.bdew.HeatBuilding(
            df.index,
            holidays=holidays,
            temperature=df["Air Temperature (°C)"],
            shlp_type="EFH",
            building_class=1,
            wind_class=1,
            annual_heat_demand=building_area * specific_heat_demand,
            name="EFH",
        ).get_bdew_profile()
        * 60
    )

    # **************** COP calculation **********************************
    t_supply = 60
    efficiency = 0.5  # source?
    cop_max = 7  # source???

    cop_hp = (t_supply + 273.15 * efficiency) / (
        t_supply - df["Air Temperature (°C)"]
    )
    cop_hp.loc[cop_hp > cop_max] = cop_max

    df["cop"] = cop_hp

    df["PV (kW/kWp)"] = df["P_PV (W)"] / 14.5e3  # Wp from publication

    df["P_tot27 (W)"] /= 1000
    df.rename(
        columns={"P_tot27 (W)": "electricity demand (kW)"},
        inplace=True,
    )

    # drop colums that are no longer useful
    df.drop(columns=["P_PV (W)"], inplace=True)

    # add car charging profile
    def _car_dataframe():
        car = _get_data("car_charging.csv")
        car.index = df.index
        return car

    df = pd.concat([df, _car_dataframe()], axis=1)

    return df


def discounted_average_price(
    price_series, interest_rate, observation_period, year_of_investment
):
    discount_factors = 1 / (1 + interest_rate) ** np.arange(observation_period)

    # Formel:
    # p* = Sum( p_t / (1+r)^(t-1) ) / Sum( 1/(1+r)^(t-1) )

    numerator = (
        price_series.loc[
            year_of_investment : year_of_investment + observation_period - 1
        ]
        .mul(discount_factors, axis=0)
        .sum()
    )

    denominator = discount_factors.sum()

    print(annuity(numerator, observation_period, interest_rate))
    print(numerator / denominator)

    return numerator / denominator


def energy_prices() -> pd.DataFrame:
    print("Data is taken from at doi: https://doi.org/10.52202/077185-0033")

    years = [2025, 2030, 2035, 2040, 2045]
    # years = [2025, 2026, 2027, 2028, 2029]
    var_cost = pd.DataFrame(
        {
            "gas_prices [Eur/kWh]": [
                0.116,
                0.106,
                0.133,
                0.116,
                0.118,
            ],
            "electricity_prices [Eur/kWh]": [
                0.386,
                0.303,
                0.290,
                0.294,
                0.286,
            ],
            "pv_feed_in [Eur/kWh]": [-0.081] * 5,
        },
        index=pd.Index(years, name="year"),
    )
    return pd.concat(
        [pd.DataFrame(index=range(2025, 2065)), var_cost], axis=1
    ).interpolate()


def investment_costs() -> pd.DataFrame:
    print("Data is taken from doi: https://doi.org/10.52202/077185-0033")

    years = [2025, 2030, 2035, 2040, 2045]
    # years = [2025, 2026, 2027, 2028, 2029]
    idx = pd.Index(years, name="year")

    df = pd.DataFrame(
        {
            ("gas boiler", "specific_costs [Eur/kW]"): [61] * 5,
            ("gas boiler", "fixed_costs [Eur]"): [4794] * 5,
            ("gas boiler", "maximum [kW]"): 100,
            ("heat pump", "specific_costs [Eur/kW]"): [
                1680,
                1318,
                1182,
                1101,
                1048,
            ],
            ("heat pump", "fixed_costs [Eur]"): [3860, 3030, 2716, 2530, 2410],
            ("heat pump", "maximum [kW]"): 100,
            ("heat storage", "specific_costs [Eur/m3]"): [1120] * 5,
            ("heat storage", "fixed_costs [Eur]"): [806] * 5,
            ("heat storage", "maximum [kWh]"): 100,
            ("pv", "specific_costs [Eur/kW]"): [
                1200,
                1017,
                927,
                864,
                828,
            ],
            ("pv", "fixed_costs [Eur]"): [3038, 2575, 2347, 2188, 2096],
            ("pv", "maximum [kW]"): 10,
            ("battery", "specific_costs [Eur/kWh]"): [
                850,
                544,
                453,
                420,
                409,
            ],
            ("battery", "fixed_costs [Eur]"): [0] * 5,
            ("battery", "maximum [kWh]"): 100,
        },
        index=idx,
    )

    return pd.concat(
        [pd.DataFrame(index=range(2025, 2065)), df], axis=1
    ).interpolate()


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    my_df = prepare_input_data()

    # plt.plot(df["electricity demand (kW)"], "k")

    p_pv = {}
    resolutions = [
        "1 min",
        #    "5 min",
        #    "10 min",
        "15 min",
        #    "30 min",
        "1 h",
        #    "2 h",
        "3 h",
        #    "6 h",
    ]

    fig0, ax0 = plt.subplots(figsize=(4, 2), tight_layout=True)
    fig1, ax1 = plt.subplots(figsize=(4, 2), tight_layout=True)

    for resolution in resolutions[::-1]:
        time_series = 15.4 * my_df["PV (kW/kWp)"].resample(resolution).mean()
        # plt.plot(
        #    np.linspace(0, 8760, len(p_pv[resolution])),
        #    sorted(p_pv[resolution])[::-1],
        #    label=resolution,
        # )

        time_series = time_series[
            datetime.datetime(
                2019, 11, 3, 0, tzinfo=datetime.timezone.utc
            ) : datetime.datetime(2019, 11, 4, 0, tzinfo=datetime.timezone.utc)
        ]
        hour_axis = np.linspace(0, 24, num=len(time_series))
        ax0.step(
            x=hour_axis,
            y=time_series,
            label=resolution,  # + f" ({len(time_series)} steps)",
            where="post",
        )
        ax1.step(
            x=hour_axis,
            y=sorted(time_series)[::-1],
            label=resolution,  # + f" ({len(time_series)} steps)",
            where="post",
        )

        p_pv[resolution] = time_series

    ax0.set_xlim(5.9, 18.1)
    ax0.set_xlabel("Time (UTC)")
    ax0.set_ylabel("Power (kW)")
    ax0.legend()
    ax0.grid()
    fig0.savefig("2019-11-3_PV-timeseries.eps")
    fig0.savefig("2019-11-3_PV-timeseries.pdf")

    ax1.grid()
    ax1.set_xlim(-0.1, 12.1)
    ax1.set_xlabel("Duration (h)")
    ax1.set_ylabel("Power (kW)")
    ax1.set_yscale("log")
    # ax1.legend()
    fig1.savefig("2019-11-3_PV-duration.eps")
    fig1.savefig("2019-11-3_PV-duration.pdf")

    plt.show()
