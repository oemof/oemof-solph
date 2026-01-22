import numpy as np
import pandas as pd
from oemof.tools.economics import annuity

from oemof.solph import Investment


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

        investments[key] = Investment(
            ep_costs=epc,
            offset=fix_cost,
            maximum=maximum,
            lifetime=20,
            nonconvex=True,
        )
    return investments


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

        investments[key] = Investment(
            ep_costs=epc,
            offset=fix_cost,
            maximum=maximum,
            lifetime=20,
            nonconvex=bool(fix_cost > 0),  # need to cast to avoid np.bool
        )
    return investments
