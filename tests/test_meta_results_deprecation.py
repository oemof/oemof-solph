# SPDX-FileCopyrightText: oemof e.V. and contributors
#
# SPDX-License-Identifier: MIT

"""Tests for the deprecated processing.meta_results (see #1343)."""

import pandas as pd
import pytest

from oemof import solph
from oemof.solph import processing


def _solved_model(solver):
    es = solph.EnergySystem(
        timeindex=pd.date_range("2020-01-01", periods=3, freq="h"),
        infer_last_interval=True,
    )
    bus = solph.buses.Bus(label="bus")
    source = solph.components.Source(
        label="source", outputs={bus: solph.flows.Flow(variable_costs=2)}
    )
    sink = solph.components.Sink(
        label="sink",
        inputs={bus: solph.flows.Flow(fix=[1, 2, 3], nominal_capacity=1)},
    )
    es.add(bus, source, sink)
    model = solph.Model(es)
    results = model.solve(solver=solver)
    return model, results


def test_meta_results_warns_and_works_with_highs():
    model, results = _solved_model("highs")
    with pytest.warns(FutureWarning, match="meta_results"):
        meta = processing.meta_results(model)
    assert meta["objective"] == pytest.approx(12)
    assert meta["objective"] == pytest.approx(results.solver["objective"])
    assert set(meta) == {"objective", "problem", "solver"}
    assert meta["problem"]["MIPGap"] == pytest.approx(0)
    assert meta["solver"]["Termination condition"] == "optimal"
