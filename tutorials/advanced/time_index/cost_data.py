import pandas as pd
import numpy as np

def discounted_average_price(price_series, interest_rate, observation_period):

    discount_factors = 1 / (1 + interest_rate) ** np.arange(observation_period)

    # Formel:
    # p* = Sum( p_t / (1+r)^(t-1) ) / Sum( 1/(1+r)^(t-1) )

    numerator = np.sum(price_series[:observation_period] * discount_factors)
    denominator = np.sum(discount_factors)

    return numerator/denominator

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
            ("heat pump", "specific_costs [Eur/kW]"): [
                1680,
                1318,
                1182,
                1101,
                1048,
            ],
            ("heat pump", "fixed_costs [Eur]"): [3860, 3030, 2716, 2530, 2410],
            ("heat storage", "specific_costs [Eur/m3]"): [1120] * 5,
            ("heat storage", "fixed_costs [Eur]"): [806] * 5,
            ("pv", "specific_costs [Eur/kW]"): [
                1200,
                1017,
                927,
                864,
                828,
            ],
            ("pv", "fixed_costs [Eur]"): [3038, 2575, 2347, 2188, 2096],
            ("battery", "specific_costs [Eur/kWh]"): [
                850,
                544,
                453,
                420,
                409,
            ],
            ("battery", "fixed_costs [Eur]"): [0] * 5,
        },
        index=idx,
    )

    return pd.concat(
        [pd.DataFrame(index=range(2025, 2065)), df], axis=1
    ).interpolate()
