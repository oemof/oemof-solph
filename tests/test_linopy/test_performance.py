# -*- coding: utf-8 -*-

"""Build-time tests of the linopy backend.

Run with ``pytest --run-performance tests/test_linopy``. They print the
build times of both backends for a fixed set of systems and fail if the
linopy backend is not faster for a full year, which would mean a builder
fell back to Python loops over elements.

SPDX-License-Identifier: MIT
"""

import time

import numpy as np
import pandas as pd
import pytest

from oemof import solph

pytest.importorskip("linopy")

from oemof.solph._linopy import LinopyModel  # noqa: E402
from oemof.solph._models import Model as PyomoModel  # noqa: E402


def chain_energy_system(n_steps, n_buses=14, seed=1):
    """A district-heating sized system: a chain of buses with one or two
    converters between neighbours, a source at the start, a sink at the
    end (about 45 flows)."""
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2025-01-01", periods=n_steps, freq="h")
    es = solph.EnergySystem(timeindex=idx, infer_last_interval=True)
    buses = [solph.Bus(f"b{i}") for i in range(n_buses)]
    es.add(*buses)
    es.add(
        solph.components.Source(
            "source",
            outputs={
                buses[0]: solph.Flow(
                    variable_costs=50 + 30 * rng.random(n_steps)
                )
            },
        )
    )
    for i in range(n_buses - 1):
        for j in range(2 if i < 6 else 1):
            es.add(
                solph.components.Converter(
                    f"c{i}_{j}",
                    inputs={buses[i]: solph.Flow()},
                    outputs={buses[i + 1]: solph.Flow(variable_costs=0.1 * j)},
                    conversion_factors={buses[i + 1]: 0.9 + 0.05 * j},
                )
            )
    es.add(
        solph.components.Sink(
            "sink",
            inputs={
                buses[-1]: solph.Flow(
                    fix=0.5 + 0.5 * rng.random(n_steps), nominal_capacity=10
                )
            },
        )
    )
    return es


def _build_time(model_class, es, repeat):
    model_class(es)  # warm up imports and caches
    start = time.perf_counter()
    for _ in range(repeat):
        model_class(es)
    return (time.perf_counter() - start) / repeat


@pytest.mark.performance
@pytest.mark.parametrize("n_steps,repeat", [(24, 10), (8760, 2)])
def test_build_time(n_steps, repeat):
    es = chain_energy_system(n_steps)
    pyomo = _build_time(PyomoModel, es, repeat)
    linopy_ = _build_time(LinopyModel, es, repeat)
    print(
        f"\n{n_steps} steps: pyomo {1000 * pyomo:.1f} ms, "
        f"linopy {1000 * linopy_:.1f} ms"
    )
    if n_steps >= 8760:
        assert linopy_ < pyomo
