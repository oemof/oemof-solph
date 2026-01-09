import logging
import warnings

import tsam.timeseriesaggregation as tsam
import pandas as pd
from matplotlib import pyplot as plt

from oemof.tools.economics import annuity
from oemof.tools import debugging, logger
from oemof.solph import Bus, EnergySystem, Flow, Investment, Model
from oemof.solph import components as cmp
from oemof import solph

from shared import prepare_input_data
from cost_data import discounted_average_price, energy_prices, investment_costs
from time_series_un_even import calculate_fix_cost

warnings.filterwarnings(
    "ignore", category=debugging.ExperimentalFeatureWarning
)
logger.define_logging()

# -----------------------------
# Global inputs (once)
# -----------------------------
data = prepare_input_data()
data = data.resample("1 h").mean()

year = 2025
n = 20
r = 0.05

var_cost = discounted_average_price(energy_prices(), r, n, year)
invest_cost = investment_costs().loc[year]


def build_investment_objects(invest_cost_row, n, r):
    """Create oemof.solph.Investment objects for each technology."""
    inv = {}
    for key in ["gas boiler", "heat pump", "battery", "pv"]:
        # ep_costs may be given per kW or per kWh depending on tech
        try:
            epc = annuity(
                invest_cost_row[(key, "specific_costs [Eur/kW]")], n, r
            )
        except KeyError:
            epc = annuity(
                invest_cost_row[(key, "specific_costs [Eur/kWh]")], n, r
            )

        fix_cost = calculate_fix_cost(
            invest_cost_row[(key, "fixed_costs [Eur]")]
        )
        inv[key] = Investment(ep_costs=epc, fixed_costs=fix_cost, lifetime=20)

    return inv


INV_OBJECTS = build_investment_objects(invest_cost, n, r)


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
        min_storage_level=0.0,
        max_storage_level=1.0,
        loss_rate=0.001,
        inflow_conversion_factor=0.95,
        outflow_conversion_factor=0.95,
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

    pv_invest_kW = results[(pv, bus_el)]["period_scalars"]["invest"].iloc[0]
    storage_invest_kWh = results[(battery, None)]["period_scalars"][
        "invest"
    ].iloc[0]
    hp_invest_kW = results[(hp, bus_heat)]["period_scalars"]["invest"].iloc[0]
    gas_boiler_invest_kW = results[(gas_boiler, bus_heat)]["period_scalars"][
        "invest"
    ].iloc[0]

    return pd.Series(
        {
            "PV": pv_invest_kW,
            "Battery": storage_invest_kWh,
            "HP": hp_invest_kW,
            "Gas boiler": gas_boiler_invest_kW,
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
for cfg in configs:
    hpp = cfg["hours_per_period"]
    tp_list = cfg["typical_periods"]

    all_caps = []
    for tp in tp_list:
        all_caps.append(run_for_typical_periods(tp, hours_per_period=hpp))

    caps_df = pd.concat(all_caps, axis=1)
    caps_df.columns = [int(c) for c in caps_df.columns]
    caps_by_hpp[hpp] = caps_df


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
