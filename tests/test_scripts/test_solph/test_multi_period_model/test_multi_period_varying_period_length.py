import pandas as pd
from pandas.testing import assert_frame_equal

from oemof import solph


def test_multi_period_varying_period_length(lp=False):
    t_idx_1 = pd.date_range("1/1/2000", periods=12, freq="H")
    # Create a timeindex for each period
    t_idx_2 = pd.date_range("1/1/2020", periods=12, freq="H")
    t_idx_3 = pd.date_range("1/1/2035", periods=12, freq="H")
    t_idx_4 = pd.date_range("1/1/2045", periods=12, freq="H")
    t_idx_5 = pd.date_range("1/1/2050", periods=12, freq="H")
    t_idx_6 = pd.date_range("1/1/2060", periods=12, freq="H")
    t_idx_7 = pd.date_range("1/1/2075", periods=12, freq="H")
    t_idx_8 = pd.date_range("1/1/2095", periods=12, freq="H")

    # Create an overall timeindex
    t_idx_1_series = pd.Series(index=t_idx_1, dtype="float64")
    t_idx_2_series = pd.Series(index=t_idx_2, dtype="float64")
    t_idx_3_series = pd.Series(index=t_idx_3, dtype="float64")
    t_idx_4_series = pd.Series(index=t_idx_4, dtype="float64")
    t_idx_5_series = pd.Series(index=t_idx_5, dtype="float64")
    t_idx_6_series = pd.Series(index=t_idx_6, dtype="float64")
    t_idx_7_series = pd.Series(index=t_idx_7, dtype="float64")
    t_idx_8_series = pd.Series(index=t_idx_8, dtype="float64")

    timeindex = pd.concat(
        [
            t_idx_1_series,
            t_idx_2_series,
            t_idx_3_series,
            t_idx_4_series,
            t_idx_5_series,
            t_idx_6_series,
            t_idx_7_series,
            t_idx_8_series,
        ]
    ).index

    # Create a list of timeindex for each period
    periods = [
        t_idx_1,
        t_idx_2,
        t_idx_3,
        t_idx_4,
        t_idx_5,
        t_idx_6,
        t_idx_7,
        t_idx_8,
    ]

    # Create an energy system
    es = solph.EnergySystem(
        timeindex=timeindex,
        timeincrement=[1] * len(timeindex),
        periods=periods,
        infer_last_interval=False,
    )

    df_profiles = pd.DataFrame(
        {
            "demand": [7e-05] * len(timeindex),
            "pv-profile": ([0.0] * 8 + [0.1] * 4) * len(periods),
            "wind-profile": ([0.1] * 5 + [0.2] * 4 + [0.1] * 3) * len(periods),
        },
        index=timeindex,
    )

    # df_profiles = pd.read_csv("profiles.csv", index_col=0, parse_dates=True)

    bel = solph.Bus(label="electricity", balanced=True)

    storage = solph.components.GenericStorage(
        label="storage",
        inputs={
            bel: solph.Flow(
                variable_costs=0,
                investment=solph.Investment(
                    ep_costs=10,
                    existing=0,
                    lifetime=20,
                    age=0,
                    interest_rate=0.02,
                ),
            )
        },
        outputs={
            bel: solph.Flow(
                variable_costs=0,
                investment=solph.Investment(
                    ep_costs=10,
                    existing=0,
                    lifetime=20,
                    age=0,
                    interest_rate=0.02,
                ),
            )
        },
        loss_rate=0.00,
        invest_relation_output_capacity=0.2,
        invest_relation_input_output=1,
        # inflow_conversion_factor=1,
        # outflow_conversion_factor=0.8,
        # nominal_storage_capacity=100,
        investment=solph.Investment(
            ep_costs=10,
            maximum=float("+inf"),
            existing=0,
            lifetime=20,
            age=0,
            fixed_costs=None,
            interest_rate=0.02,
        ),
    )

    demand = solph.components.Sink(
        label="demand",
        inputs={bel: solph.Flow(fix=df_profiles["demand"], nominal_value=1e5)},
    )

    pv = solph.components.Source(
        label="pv",
        outputs={
            bel: solph.Flow(
                fix=df_profiles["pv-profile"],
                investment=solph.Investment(
                    ep_costs=20,
                    maximum=float("+inf"),
                    minimum=0,
                    lifetime=20,
                    age=0,
                    interest_rate=0.02,
                ),
            )
        },
    )

    wind = solph.components.Source(
        label="wind",
        outputs={
            bel: solph.Flow(
                fix=df_profiles["wind-profile"],
                investment=solph.Investment(
                    ep_costs=50,
                    maximum=float("+inf"),
                    minimum=0,
                    lifetime=20,
                    age=0,
                    interest_rate=0.02,
                ),
            )
        },
    )
    es.add(bel, storage, demand, pv, wind)

    # Create an optimization problem and solve it
    om = solph.Model(es)
    # om.write("file.lp", io_options={"symbolic_solver_labels": True})
    if lp:
        return om
    else:
        # Solve the optimization problem
        om.solve(solver="cbc")

        # Get the results
        results = om.results()

        # Convert the results into a more readable format
        result_views = solph.views.convert_keys_to_strings(results)

        # Investment results for
        # storage capacity investment
        df_storage_invest_mwh = result_views[("storage", "None")][
            "period_scalars"
        ]
        # capacity investment
        df_storage_invest_mw = result_views[("storage", "electricity")][
            "period_scalars"
        ]

        # Expected results
        df_storage_invest_mwh_expected = pd.DataFrame(
            {
                "invest": [
                    91.347378,
                    12.014044,
                    12.957867,
                    4.173220,
                    0.0,
                    33.555515,
                    0.0,
                    12.727273,
                ],
                "old": [
                    0.0,
                    91.347378,
                    0.0,
                    12.014044,
                    0.0,
                    12.957867,
                    4.173220,
                    33.555515,
                ],
                "old_end": [
                    0.0,
                    91.347378,
                    0.0,
                    12.014044,
                    0.0,
                    12.957867,
                    4.173220,
                    33.555515,
                ],
                "old_exo": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                "total": [
                    91.347378,
                    12.014044,
                    24.971912,
                    17.131087,
                    17.131087,
                    37.728735,
                    33.555515,
                    12.727273,
                ],
            },
            index=[2000, 2020, 2035, 2045, 2050, 2060, 2075, 2095],
        )

        df_storage_invest_mw_expected = pd.DataFrame(
            {
                "invest": [
                    18.269476,
                    2.402809,
                    2.591573,
                    0.834644,
                    0.0,
                    6.711103,
                    0.0,
                    2.545454,
                ],
                "old": [
                    0.0,
                    18.269476,
                    0.0,
                    2.402809,
                    0.0,
                    2.591573,
                    0.834644,
                    6.711103,
                ],
                "old_end": [
                    0.0,
                    18.269476,
                    0.0,
                    2.402809,
                    0.0,
                    2.591573,
                    0.834644,
                    6.711103,
                ],
                "old_exo": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                "total": [
                    18.269476,
                    2.402809,
                    4.994382,
                    3.426217,
                    3.426217,
                    7.545747,
                    6.711103,
                    2.545454,
                ],
            },
            index=[2000, 2020, 2035, 2045, 2050, 2060, 2075, 2095],
        )

        # Compare results

        assert_frame_equal(
            df_storage_invest_mwh,
            df_storage_invest_mwh_expected,
            check_names=False,
            check_dtype=False,
        )

        assert_frame_equal(
            df_storage_invest_mw,
            df_storage_invest_mw_expected,
            check_names=False,
            check_dtype=False,
        )
