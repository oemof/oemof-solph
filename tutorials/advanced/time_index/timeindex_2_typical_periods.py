import warnings
from datetime import datetime

import pandas as pd
import tsam.timeseriesaggregation as tsam
from input_data import discounted_average_price
from input_data import energy_prices
from input_data import get_parameter
from input_data import investment_costs
from input_data import prepare_input_data
from matplotlib import pyplot as plt
from oemof.tools import debugging
from oemof.tools import logger
from timeindex_1_segmentation import populate_and_solve_energy_system

from oemof import solph

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
parameter = get_parameter()

variable_costs = discounted_average_price(
    price_series=energy_prices(),
    observation_period=parameter["n"],
    interest_rate=parameter["r"],
    year_of_investment=year,
)


def create_investment_objects_multi_period(year):
    invest_cost = investment_costs().loc[year]

    # Create Investment objects from cost data
    investments = {}
    for key in ["gas boiler", "heat pump", "battery", "pv"]:
        try:
            epc = invest_cost[(key, "specific_costs [Eur/kW]")]

            maximum = invest_cost[(key, "maximum [kW]")]
        except KeyError:
            epc = invest_cost[(key, "specific_costs [Eur/kWh]")]
            maximum = invest_cost[(key, "maximum [kWh]")]

        fix_cost = invest_cost[(key, "fixed_costs [Eur]")]

        investments[key] = solph.Investment(
            ep_costs=epc,
            offset=fix_cost,
            maximum=maximum,
            lifetime=20,
            nonconvex=True,
        )
    return investments


investments = create_investment_objects_multi_period(
    year=year,
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

    time_series = {
        "cop": aggregation.typicalPeriods["cop"],
        "electricity demand (kW)": aggregation.typicalPeriods[
            "electricity demand (kW)"
        ],
        "heat demand (kW)": aggregation.typicalPeriods["heat demand (kW)"],
        "PV (kW/kWp)": aggregation.typicalPeriods["PV (kW/kWp)"],
        "Electricity for Car Charging_HH1": aggregation.typicalPeriods[
            "Electricity for Car Charging_HH1"
        ],
    }

    tindex_agg = pd.date_range(
        "2022-01-01",
        periods=len(aggregation.clusterPeriodIdx) * hours_per_period,
        freq="h",
    )

    es = solph.EnergySystem(
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

    m = populate_and_solve_energy_system(
        es=es,
        time_series=time_series,
        investments=investments,
        variable_costs=variable_costs,
    )

    results = solph.processing.results(m)

    # The keys actually contain the Nodes and not strings,
    # but as a Node is equal to its string, the following works.
    pv_invest_kw = results[("PV", "electricity")]["period_scalars"][
        "invest"
    ].iloc[0]
    storage_invest_kwh = results[("Battery", None)]["period_scalars"][
        "invest"
    ].iloc[0]
    hp_invest_kw = results[("Heat pump", "heat")]["period_scalars"][
        "invest"
    ].iloc[0]
    gas_boiler_invest_kw = results[("Gas Boiler", "heat")]["period_scalars"][
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
