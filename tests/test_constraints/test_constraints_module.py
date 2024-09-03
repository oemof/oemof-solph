import numpy as np
import pandas as pd
import pytest

from oemof import solph


def test_integral_limit():
    periods = 5
    integral_limit1 = 250
    low_emission_flow_limit = 500
    integral_weight1 = 0.8
    integral_weight3 = 1.0
    emission_factor_low = 0.5
    emission_factor_high = 1
    high_emission_flow_limit = 200
    emission_limit = (
        emission_factor_low * low_emission_flow_limit
        + emission_factor_high * high_emission_flow_limit
    )

    date_time_index = pd.date_range("1/1/2012", periods=periods, freq="h")
    energysystem = solph.EnergySystem(
        timeindex=date_time_index,
        infer_last_interval=True,
    )
    bel = solph.buses.Bus(label="electricityBus", balanced=False)
    flow1 = solph.flows.Flow(
        nominal_capacity=100,
        custom_attributes={
            "my_factor": integral_weight1,
            "emission_factor": emission_factor_low,
        },
        variable_costs=-1,
    )
    flow2 = solph.flows.Flow(
        nominal_capacity=50,
        variable_costs=-0.5,
    )
    flow3 = solph.flows.Flow(
        nominal_capacity=100,
        custom_attributes={
            "my_factor": integral_weight3,
            "emission_factor": emission_factor_low,
        },
        variable_costs=-0.5,
    )
    flow4 = solph.flows.Flow(
        nominal_capacity=500,
        custom_attributes={
            "emission_factor": emission_factor_high,
        },
        variable_costs=-0.1,
    )

    src1 = solph.components.Source(label="source1", outputs={bel: flow1})
    src2 = solph.components.Source(label="source2", outputs={bel: flow2})
    src3 = solph.components.Source(label="source3", outputs={bel: flow3})
    src4 = solph.components.Source(label="source4", outputs={bel: flow4})
    energysystem.add(bel, src1, src2, src3, src4)
    model = solph.Model(energysystem)

    # Note we do not consider flow3 for this constraint.
    flows_with_keyword = {
        (src1, bel): flow1,
    }

    solph.constraints.generic_integral_limit(
        model, "my_factor", flows_with_keyword, upper_limit=integral_limit1
    )
    solph.constraints.emission_limit(
        model,
        limit=emission_limit,
    )

    solph.constraints.generic_integral_limit(
        model,
        "my_factor",
        limit_name="limit_my_factor",
        upper_limit=low_emission_flow_limit,
    )

    model.solve()

    results = solph.processing.results(model)

    # total limeted to integral_limit1
    assert integral_weight1 * sum(
        results[(src1, bel)]["sequences"]["flow"][:-1]
    ) == pytest.approx(integral_limit1)

    # unconstrained, full load all the time
    assert (
        np.array(results[(src2, bel)]["sequences"]["flow"][:-1])
        == np.full(periods, 50)
    ).all()

    # have my_factor, limited to low_emission_flow_limit
    assert integral_weight1 * sum(
        results[(src1, bel)]["sequences"]["flow"][:-1]
    ) + integral_weight3 * sum(
        results[(src3, bel)]["sequences"]["flow"][:-1]
    ) == pytest.approx(
        low_emission_flow_limit
    )

    assert emission_factor_low * sum(
        results[(src1, bel)]["sequences"]["flow"][:-1]
    ) + emission_factor_low * sum(
        results[(src3, bel)]["sequences"]["flow"][:-1]
    ) + emission_factor_high * sum(
        results[(src4, bel)]["sequences"]["flow"][:-1]
    ) == pytest.approx(
        emission_limit
    )
