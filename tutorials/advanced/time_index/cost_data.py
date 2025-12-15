import pandas as pd


def energy_prices() -> pd.DataFrame:

    print("Data is taken from at doi: https://doi.org/10.52202/077185-0033")

    years = [2025, 2030, 2035, 2040, 2045]
    return pd.DataFrame(
        {
            "gas_prices [Eur/Wh]": [
                0.116 / 1000,
                0.106 / 1000,
                0.133 / 1000,
                0.116 / 1000,
                0.118 / 1000,
            ],
            "electricity_prices [Eur/Wh]": [
                0.386 / 1000,
                0.303 / 1000,
                0.290 / 1000,
                0.294 / 1000,
                0.286 / 1000,
            ],
            "pv_feed_in [Eur/Wh]": [-0.081 / 1000] * 5,
        },
        index=pd.Index(years, name="year"),
    )


def investment_costs() -> pd.DataFrame:
    print("Data is taken from doi: https://doi.org/10.52202/077185-0033")

    years = [2025, 2030, 2035, 2040, 2045]
    idx = pd.Index(years, name="year")

    df = pd.DataFrame(
        {
            ("gas boiler", "specific_costs [Eur/W]"): [61 / 1000] * 5,
            ("gas boiler", "fixed_costs [Eur]"): [4794] * 5,
            ("heat pump", "specific_costs [Eur/W]"): [
                1680 / 1000,
                1318 / 1000,
                1182 / 1000,
                1101 / 1000,
                1048 / 1000,
            ],
            ("heat pump", "fixed_costs [Eur]"): [3860, 3030, 2716, 2530, 2410],
            ("heat storage", "specific_costs [Eur/m3]"): [1120] * 5,
            ("heat storage", "fixed_costs [Eur]"): [806] * 5,
            ("pv", "specific_costs [Eur/W]"): [
                1200 / 1000,
                1017 / 1000,
                927 / 1000,
                864 / 1000,
                828 / 1000,
            ],
            ("pv", "fixed_costs [Eur]"): [3038, 2575, 2347, 2188, 2096],
            ("battery", "specific_costs [Eur/Wh]"): [
                850 / 1000,
                544 / 1000,
                453 / 1000,
                420 / 1000,
                409 / 1000,
            ],
            ("battery", "fixed_costs [Eur]"): [0] * 5,
        },
        index=idx,
    )

    return df
