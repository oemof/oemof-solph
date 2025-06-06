# -*- coding: utf-8 -*-
import warnings

import pytest
from oemof.tools.debugging import ExperimentalFeatureWarning

from oemof import solph


def test_multi_input_sink():
    num_in = 3
    steps = 10
    costs = -0.1

    es = solph.EnergySystem(
        timeindex=solph.create_time_index(year=2023, number=steps),
        infer_last_interval=False,
    )

    for i in range(num_in):
        bus_label = f"bus input {i}"
        b = solph.Bus(bus_label)
        es.add(b)
        es.add(
            solph.components.Source(f"source {i}", outputs={b: solph.Flow()})
        )
    # Use of experimental API to access nodes by label.
    # Can be removed with future release of network.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ExperimentalFeatureWarning)
        es.add(
            solph.components.Sink(
                inputs={
                    es.node[f"bus input {i}"]: solph.Flow(
                        nominal_capacity=1,
                        variable_costs=costs,
                    )
                    for i in range(num_in)
                }
            )
        )

    model = solph.Model(es)
    model.solve("cbc")

    assert (
        model.solver_results["Solver"][0]["Termination condition"]
        != "infeasible"
    )
    meta_results = solph.processing.meta_results(model)

    assert meta_results["objective"] == pytest.approx(num_in * steps * costs)
