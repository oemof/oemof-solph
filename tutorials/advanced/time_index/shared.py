"""
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: DLR e.V.

SPDX-License-Identifier: MIT
"""

import datetime
from pathlib import Path

import demandlib
import pandas as pd
import numpy as np
from urllib.request import urlretrieve
from workalendar.europe import Germany


def prepare_input_data():
    # ToDo: Mobilitätszeitreihe, die zu den Daten passt.

    url_temperature = (
        "https://oemof.org/wp-content/uploads/2025/12/temperature.csv"
    )
    url_energy = "https://oemof.org/wp-content/uploads/2026/01/energy.csv"

    print(
        "Data is licensed from M. Schlemminger, T. Ohrdes, E. Schneider,"
        " and M. Knoop. Under Creative Commons Attribution 4.0 International"
        " License. It is also available at doi: 10.5281/zenodo.5642902."
        " (We use building 27 plus the south-facing PV"
        " from that dataset.)"
    )

    file_path = Path(__file__).parent

    def _temperature_dataframe():
        temperature_file = Path(file_path, "temperature.csv")
        if not temperature_file.exists():
            urlretrieve(url_temperature, temperature_file)
        temperature = pd.read_csv(
            temperature_file,
            index_col="Unix Epoch",
        )

        temperature.index = pd.to_datetime(
            temperature.index,
            unit="s",
            utc=True,
        )

        temperature[temperature == np.inf] = np.nan
        temperature = temperature[10:].resample("1 min").mean()
        return temperature

    def _energy_dataframe():
        energy_file = Path(file_path, "energy.csv")
        if not energy_file.exists():
            urlretrieve(url_energy, energy_file)

        energy = pd.read_csv(
            energy_file,
            index_col=0,
        )
        energy.index = pd.to_datetime(
            energy.index,
            unit="s",
            utc=True,
        )

        energy[energy == np.inf] = np.nan

        energy = (
            energy.resample("1 min")
            .mean()
        )
        return energy

    df = pd.concat([_energy_dataframe(), _temperature_dataframe()], axis=1)

    df = df.interpolate()

    building_area = 110  # m² (from publication)
    specific_heat_demand = 60  #  kWh/m²/a  (educated guess)
    holidays = dict(Germany().holidays(2019))

    # We estimate the heat demand from the ambient temperature using demandlib.
    # This returns energy per time step in units of kWh, but we want kW.
    df["heat demand (kW)"] = demandlib.bdew.HeatBuilding(
        df.index,
        holidays=holidays,
        temperature=df["Air Temperature (°C)"],
        shlp_type="EFH",
        building_class=1,
        wind_class=1,
        annual_heat_demand=building_area * specific_heat_demand,
        name="EFH",
    ).get_bdew_profile() * 60

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

    return df


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    df =prepare_input_data()

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
        time_series = 15.4 * df["PV (kW/kWp)"].resample(resolution).mean()
        # plt.plot(
        #    np.linspace(0, 8760, len(p_pv[resolution])),
        #    sorted(p_pv[resolution])[::-1],
        #    label=resolution,
        # )

        time_series = time_series[
            datetime.datetime(2019, 11, 3, 0, tzinfo=datetime.timezone.utc)
            : datetime.datetime(2019, 11, 4, 0, tzinfo=datetime.timezone.utc)
        ]
        hour_axis = np.linspace(0, 24, num=len(time_series))
        ax0.step(
            x=hour_axis,
            y=time_series,
            label=resolution,# + f" ({len(time_series)} steps)",
            where="post",
        )
        ax1.step(
            x=hour_axis,
            y=sorted(time_series)[::-1],
            label=resolution,# + f" ({len(time_series)} steps)",
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
    #ax1.legend()
    fig1.savefig("2019-11-3_PV-duration.eps")
    fig1.savefig("2019-11-3_PV-duration.pdf")

    plt.show()
