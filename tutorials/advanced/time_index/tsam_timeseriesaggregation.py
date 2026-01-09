import logging
import warnings
from datetime import datetime

import pandas as pd
import tsam.timeseriesaggregation as tsam
from cost_data import create_investment_objects
from cost_data import discounted_average_price
from cost_data import energy_prices
from matplotlib import pyplot as plt
from oemof.tools import debugging
from oemof.tools import logger
from shared import get_parameter
from shared import prepare_input_data

from oemof import solph
from oemof.solph import Bus
from oemof.solph import EnergySystem
from oemof.solph import Flow
from oemof.solph import Model
from oemof.solph import components as cmp

warnings.filterwarnings(
    "ignore", category=debugging.ExperimentalFeatureWarning
)
logger.define_logging()

# -----------------------------
# Global inputs (once)
# -----------------------------
data = prepare_input_data()
data = data.resample("1 h").mean()

PARAMETER = get_parameter()

year = 2025
n = 20
r = 0.05

var_cost = discounted_average_price(energy_prices(), r, n, year)

INV_OBJECTS = create_investment_objects(
    n=n, r=r, year=year, max_capacity_pv=PARAMETER["max_capacity_pv"]
)


def run_for_typical_periods(
    typical_periods: int, hours_per_period: int = 24
) -> pd.Series:
    """
    Run the full TSAM aggregation + oemof optimization for one typical_periods
    value.
    Returns installed capacities as a Series (PV kW, Battery kWh, HP kW, Gas
    boiler kW).
    """

    # --- TSAM clustering ---
    aggregation = tsam.TimeSeriesAggregation(
        timeSeries=data.iloc[:8760],
        noTypicalPeriods=typical_periods,
        hoursPerPeriod=hours_per_period,
        clusterMethod="k_means",
        sortValues=False,
        rescaleClusterPeriods=False,
    )
    aggregation.createTypicalPeriods()

    tindex_agg = pd.date_range(
        "2022-01-01", periods=typical_periods * hours_per_period, freq="h"
    )

    es = EnergySystem(
        timeindex=tindex_agg,
        timeincrement=[1] * len(tindex_agg),
        periods=[tindex_agg],
        tsa_parameters=[
            {
                "timesteps_per_period": aggregation.hoursPerPeriod,
                "order": aggregation.clusterOrder,
                "timeindex": aggregation.timeIndex,
            }
        ],
        infer_last_interval=False,
    )

    # --- Buses ---
    bus_el = Bus(label="electricity")
    bus_heat = Bus(label="heat")
    bus_gas = Bus(label="gas")
    es.add(bus_el, bus_heat, bus_gas)

    # --- PV ---
    pv = cmp.Source(
        label="PV",
        outputs={
            bus_el: Flow(
                fix=aggregation.typicalPeriods["PV (kW/kWp)"],
                nominal_capacity=INV_OBJECTS["pv"],
            )
        },
    )
    es.add(pv)

    # --- Battery ---
    battery = cmp.GenericStorage(
        label="Battery",
        inputs={bus_el: Flow()},
        outputs={bus_el: Flow()},
        nominal_capacity=INV_OBJECTS["battery"],  # kWh
        loss_rate=PARAMETER["loss_rate_battery"],
        inflow_conversion_factor=PARAMETER["charge_efficiency_battery"],
        outflow_conversion_factor=PARAMETER["discharge_efficiency_battery"],
    )
    es.add(battery)

    # --- Electricity demand ---
    house_sink = cmp.Sink(
        label="Electricity demand",
        inputs={
            bus_el: Flow(
                fix=aggregation.typicalPeriods["electricity demand (kW)"],
                nominal_capacity=1.0,
            )
        },
    )
    es.add(house_sink)

    # --- EV demand ---
    wallbox_sink = cmp.Sink(
        label="Electric Vehicle",
        inputs={
            bus_el: Flow(
                fix=aggregation.typicalPeriods[
                    "Electricity for Car Charging_HH1"
                ],
                nominal_capacity=1.0,
            )
        },
    )
    es.add(wallbox_sink)

    # --- Heat Pump ---
    hp = cmp.Converter(
        label="Heat pump",
        inputs={bus_el: Flow()},
        outputs={bus_heat: Flow(nominal_capacity=INV_OBJECTS["heat pump"])},
        conversion_factors={bus_heat: aggregation.typicalPeriods["cop"]},
    )
    es.add(hp)

    # --- Gas Boiler ---
    gas_boiler = cmp.Converter(
        label="Gas Boiler",
        inputs={bus_gas: Flow()},
        outputs={bus_heat: Flow(nominal_capacity=INV_OBJECTS["gas boiler"])},
        conversion_factors={bus_heat: PARAMETER["efficiency_boiler"]},
    )
    es.add(gas_boiler)

    # --- Heat demand ---
    heat_sink = cmp.Sink(
        label="Heat demand",
        inputs={
            bus_heat: Flow(
                fix=aggregation.typicalPeriods["heat demand (kW)"],
                nominal_capacity=1.0,
            )
        },
    )
    es.add(heat_sink)

    # --- Imports/exports ---
    grid_import = cmp.Source(
        label="Grid import",
        outputs={
            bus_el: Flow(
                variable_costs=var_cost["electricity_prices [Eur/kWh]"]
            )
        },
    )
    es.add(grid_import)

    feed_in = cmp.Sink(
        label="Grid Feed-in",
        inputs={bus_el: Flow(variable_costs=var_cost["pv_feed_in [Eur/kWh]"])},
    )
    es.add(feed_in)

    gas_import = cmp.Source(
        label="Gas import",
        outputs={
            bus_gas: Flow(variable_costs=var_cost["gas_prices [Eur/kWh]"])
        },
    )
    es.add(gas_import)

    # --- Solve ---
    logging.info(f"Creating Model for typical_periods={typical_periods} ...")
    m = Model(es)
    logging.info("Solving Model...")
    m.solve(solver="cbc", solve_kwargs={"tee": False})

    results = solph.processing.results(m)

    pv_invest_kw = results[(pv, bus_el)]["period_scalars"]["invest"].iloc[0]
    storage_invest_kwh = results[(battery, None)]["period_scalars"][
        "invest"
    ].iloc[0]
    hp_invest_kw = results[(hp, bus_heat)]["period_scalars"]["invest"].iloc[0]
    gas_boiler_invest_kw = results[(gas_boiler, bus_heat)]["period_scalars"][
        "invest"
    ].iloc[0]

    return pd.Series(
        {
            "PV": pv_invest_kw,
            "Battery": storage_invest_kwh,
            "HP": hp_invest_kw,
            "Gas boiler": gas_boiler_invest_kw,
        },
        name=f"{typical_periods}",
    )


# -----------------------------
# Config for both aggregations
# -----------------------------
configs = [
    {"hours_per_period": 24, "typical_periods": [40, 100, 160, 220, 280, 365]},
    {"hours_per_period": 24 * 7, "typical_periods": [1, 4, 8, 12, 24, 52]},
]

caps_by_hpp = {}  # store results per hours_per_period


# -----------------------------
# Run for multiple typical periods AND multiple hours_per_period
# -----------------------------
computation_time = {}
for cfg in configs:
    hpp = cfg["hours_per_period"]
    tp_list = cfg["typical_periods"]

    all_caps = []
    for tp in tp_list:
        start = datetime.now()
        all_caps.append(run_for_typical_periods(tp, hours_per_period=hpp))
        computation_time[hpp, tp] = datetime.now() - start

    capas_df = pd.concat(all_caps, axis=1)
    capas_df.columns = [int(c) for c in capas_df.columns]
    caps_by_hpp[hpp] = capas_df

print(pd.Series(computation_time))


# -----------------------------
# Plotting helper
# -----------------------------
def plot_caps(
    caps_df: pd.DataFrame, hours_per_period: int, filename_prefix: str
):
    fig, ax = plt.subplots(figsize=(4, 2.5), tight_layout=True)

    caps_df.plot(kind="bar", ax=ax)

    ax.set_ylabel("Installed capacity")  # explain mixed units in caption
    ax.set_xlabel(None)
    ax.grid(True, linewidth=0.3, alpha=0.6)

    # Put the period duration "cleverly" into the legend title
    ax.legend(
        title=f"Typical periods (period length = {hours_per_period} h)",
        ncol=3,
        frameon=False,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.02),
    )

    ax.tick_params(axis="x", rotation=0)

    fig.savefig(f"{filename_prefix}.eps")
    fig.savefig(f"{filename_prefix}.pdf")

    return fig, ax


# -----------------------------
# Create TWO plots
# -----------------------------
fig_day, ax_day = plot_caps(
    caps_by_hpp[24],
    hours_per_period=24,
    filename_prefix="investments_bar_tp_daily",
)

fig_week, ax_week = plot_caps(
    caps_by_hpp[24 * 7],
    hours_per_period=24 * 7,
    filename_prefix="investments_bar_tp_weekly",
)

plt.show()
