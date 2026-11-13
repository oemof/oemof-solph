# -*- coding: utf-8 -*-

"""Tests of the linopy backend's model skeleton.

SPDX-License-Identifier: MIT
"""

import numpy as np
import pandas as pd
import pytest

from oemof import solph

linopy = pytest.importorskip("linopy")

from oemof.solph._linopy import LinopyModel  # noqa: E402
from oemof.solph._linopy import get_builder  # noqa: E402
from oemof.solph._linopy import register_builder  # noqa: E402
from oemof.solph._linopy import unregister_builder  # noqa: E402
from oemof.solph._linopy._indexing import ragged_sum  # noqa: E402
from oemof.solph.buses._bus import BusBlock  # noqa: E402
from oemof.solph.flows._non_convex_flow_block import (  # noqa: E402
    NonConvexFlowBlock,
)
from oemof.solph.flows._simple_flow_block import SimpleFlowBlock  # noqa: E402


def _energy_system(n_steps=4):
    idx = pd.date_range("2025-01-01", periods=n_steps, freq="h")
    return solph.EnergySystem(timeindex=idx, infer_last_interval=True)


def test_lazy_export():
    assert solph.LinopyModel is LinopyModel


def test_empty_energy_system_builds():
    model = LinopyModel(_energy_system())
    assert model.linopy.nvars == 0
    assert list(model.TIMESTEPS) == [0, 1, 2, 3]
    assert list(model.TIMEPOINTS) == [0, 1, 2, 3, 4]


def test_unsupported_block_raises():
    es = _energy_system()
    bus = solph.Bus("el")
    es.add(bus, solph.components.Sink("d", inputs={bus: solph.Flow()}))
    saved = {b: get_builder(b) for b in (BusBlock, SimpleFlowBlock)}
    for block in saved:
        unregister_builder(block)
    try:
        with pytest.raises(NotImplementedError, match="BusBlock"):
            LinopyModel(es)
    finally:
        for block, builder in saved.items():
            if builder is not None:
                register_builder(block)(builder)


@pytest.fixture
def no_op_flow_builders():
    """Replace the bus and flow builders by no-ops, to test the skeleton."""
    blocks = (BusBlock, SimpleFlowBlock, NonConvexFlowBlock)
    saved = {b: get_builder(b) for b in blocks}
    for block in saved:
        register_builder(block)(lambda model, group: None)
    yield
    for block, builder in saved.items():
        if builder is None:
            unregister_builder(block)
        else:
            register_builder(block)(builder)


def test_flow_bounds_match_pyomo(no_op_flow_builders):
    n_steps = 5
    es = _energy_system(n_steps)
    el = solph.Bus("el")
    es.add(el)
    es.add(
        solph.components.Source(
            "fixed",
            outputs={el: solph.Flow(fix=[1, 2, 3, 4, 5], nominal_capacity=2)},
        ),
        solph.components.Source(
            "bounded",
            outputs={
                el: solph.Flow(
                    minimum=0.2,
                    maximum=[1, 0.5, 1, 0.5, 1],
                    nominal_capacity=10,
                )
            },
        ),
        solph.components.Source(
            "nonconvex",
            outputs={
                el: solph.Flow(
                    minimum=0.3,
                    nominal_capacity=4,
                    nonconvex=solph.NonConvex(),
                )
            },
        ),
        solph.components.Source("free", outputs={el: solph.Flow()}),
        solph.components.Sink(
            "bidirectional",
            inputs={el: solph.Flow(minimum=-1, nominal_capacity=3)},
        ),
    )
    pyomo_model = solph.Model(es)
    model = LinopyModel(es)

    lower = model.flow.lower.values
    upper = model.flow.upper.values
    for k, (i, o) in enumerate(model.FLOWS):
        for t in model.TIMESTEPS:
            var = pyomo_model.flow[i, o, t]
            if var.fixed:
                lb = ub = var.value
            else:
                lb = -np.inf if var.lb is None else var.lb
                ub = np.inf if var.ub is None else var.ub
            assert lower[k, t] == pytest.approx(lb), (i.label, o.label, t)
            assert upper[k, t] == pytest.approx(ub), (i.label, o.label, t)


def test_ragged_sum_builds_signed_sums():
    model = linopy.Model()
    var = model.add_variables(
        lower=0,
        coords=[
            pd.RangeIndex(4, name="flow"),
            pd.RangeIndex(3, name="timestep"),
        ],
        name="flow",
    )
    labels = var.labels.values
    rows = [[(0, 1.0), (1, -1.0)], [(2, 1.0), (3, -1.0), (1, 2.0)]]
    expr = ragged_sum(model, labels, rows, "bus", tail_dims=("timestep",))
    assert expr.dims == ("bus", "timestep", "_term")
    vars_ = expr.vars.values
    coeffs = expr.coeffs.values
    # bus 0, first timestep: +f0 -f1, third term absent
    assert list(vars_[0, 0]) == [labels[0, 0], labels[1, 0], -1]
    assert list(coeffs[0, 0][:2]) == [1.0, -1.0]
    # bus 1: +f2 -f3 +2 f1
    assert list(vars_[1, 2]) == [labels[2, 2], labels[3, 2], labels[1, 2]]
    assert list(coeffs[1, 2]) == [1.0, -1.0, 2.0]
