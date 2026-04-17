# -*- coding: utf-8 -*-

import pandas as pd

from oemof.solph import processing


def test_disaggregate_timeindex():
    ti_1 = pd.date_range("2020-01-01", periods=10, freq="h")
    ti_2 = pd.date_range("2030-01-01", periods=20, freq="h")
    ti_3 = pd.date_range("2040-01-01", periods=40, freq="h")
    ti = ti_1.union(ti_2).union(ti_3)

    periods = [ti_1, ti_2, ti_3]
    tsa_parameters = [
        {"timesteps_per_period": 5, "order": [1, 0]},
        {"timesteps_per_period": 5, "order": [1, 0, 0, 1]},
        {"timesteps_per_period": 10, "order": [1, 0, 0, 1]},
    ]

    for p, period_data in enumerate(tsa_parameters):
        if p == 0:
            result_index = processing._disaggregate_tsa_timeindex(
                periods[p], period_data
            )
        else:
            result_index = result_index.union(
                processing._disaggregate_tsa_timeindex(periods[p], period_data)
            )

    assert all(result_index == ti)


# Long-format / "melted" frame (see pandas.DataFrame.melt); matches the
# shape the processing module uses internally for flow results
def _make_melted_var(var_name, values):
    return pd.DataFrame(
        {
            "timestep": range(len(values)),
            "variable_name": [var_name] * len(values),
            "value": list(values),
        }
    )


def test_disaggregate_tsa_result_single_sequence_flow():
    """A plain Flow frame (single sequence variable) disaggregates by order"""
    flow_df = _make_melted_var("flow", [10.0, 11.0, 12.0, 20.0, 21.0, 22.0])
    df_dict = {("source", "target"): flow_df}
    tsa_parameters = [
        {"timesteps": 3, "order": [1, 0, 1], "occurrences": {0: 1, 1: 2}},
    ]

    result = processing._disaggregate_tsa_result(df_dict, tsa_parameters)

    disaggregated = result[("source", "target")]
    flow_values = disaggregated.loc[
        disaggregated["variable_name"] == "flow", "value"
    ].tolist()
    # order [1, 0, 1] picks period 1, then period 0, then period 1
    assert flow_values == [20.0, 21.0, 22.0, 10.0, 11.0, 12.0, 20.0, 21.0, 22.0]


def test_disaggregate_tsa_result_multi_sequence_flow():
    """A flow carrying multiple per-timestep sequences disaggregates each
    independently.

    Regression test for a bug where position-based iloc slicing silently
    assumed each flow's melted frame contained exactly one sequence
    variable. Flows emitted by ``NonConvexFlowBlock`` /
    ``InvestNonConvexFlowBlock`` carry ``flow``, ``status``,
    ``status_nominal``, ``startup`` and friends together, which broke the
    assumption and produced misaligned results.
    """
    flow_df = _make_melted_var("flow", [10.0, 11.0, 12.0, 20.0, 21.0, 22.0])
    status_df = _make_melted_var("status", [1, 1, 1, 0, 1, 1])
    status_nominal_df = _make_melted_var(
        "status_nominal", [100.0, 100.0, 100.0, 0.0, 150.0, 150.0]
    )
    combined = pd.concat([flow_df, status_df, status_nominal_df], ignore_index=True)
    df_dict = {("source", "target"): combined}
    tsa_parameters = [
        {"timesteps": 3, "order": [1, 0, 1], "occurrences": {0: 1, 1: 2}},
    ]

    result = processing._disaggregate_tsa_result(df_dict, tsa_parameters)
    disaggregated = result[("source", "target")]

    def _values(var):
        return disaggregated.loc[
            disaggregated["variable_name"] == var, "value"
        ].tolist()

    assert _values("flow") == [20.0, 21.0, 22.0, 10.0, 11.0, 12.0, 20.0, 21.0, 22.0]
    assert _values("status") == [0, 1, 1, 1, 1, 1, 0, 1, 1]
    assert _values("status_nominal") == [
        0.0, 150.0, 150.0, 100.0, 100.0, 100.0, 0.0, 150.0, 150.0,
    ]


def test_disaggregate_tsa_result_invest_status_is_periodic():
    """``invest_status`` (binary from nonconvex Investment /
    InvestNonConvexFlow) is a scalar per period and must be passed through
    via ``PERIOD_INDEXES`` rather than iloc-sliced as a sequence.
    """
    flow_df = _make_melted_var("flow", [10.0, 11.0, 12.0])
    invest_status_df = pd.DataFrame(
        {
            "timestep": [0],
            "variable_name": ["invest_status"],
            "value": [1.0],
        }
    )
    combined = pd.concat([flow_df, invest_status_df], ignore_index=True)
    df_dict = {("source", "target"): combined}
    tsa_parameters = [
        {"timesteps": 3, "order": [0, 0], "occurrences": {0: 2}},
    ]

    assert "invest_status" in processing.PERIOD_INDEXES

    result = processing._disaggregate_tsa_result(df_dict, tsa_parameters)
    disaggregated = result[("source", "target")]

    # invest_status should appear exactly once, as a period-scalar, not
    # iloc-sliced into the sequence path
    invest_status_rows = disaggregated[
        disaggregated["variable_name"] == "invest_status"
    ]
    assert len(invest_status_rows) == 1
    assert invest_status_rows["value"].iloc[0] == 1.0

    flow_rows = disaggregated[disaggregated["variable_name"] == "flow"]
    assert flow_rows["value"].tolist() == [10.0, 11.0, 12.0, 10.0, 11.0, 12.0]
