# -*- coding: utf-8 -*-

"""Equivalence of the linopy and the Pyomo backend: multi-period
investment and solph's tsam mode.

SPDX-License-Identifier: MIT
"""

import warnings

import numpy as np
import pandas as pd
import pytest
from oemof.tools.debugging import ExperimentalFeatureWarning

from oemof import solph

pytest.importorskip("linopy")

from oemof.solph import processing  # noqa: E402

from .equivalence import assert_backends_agree  # noqa: E402
from .equivalence import solve_both  # noqa: E402


def multi_period_system():
    """Three capacity periods; investments with a lifetime of one period
    have to be renewed."""
    n_steps = 12
    rng = np.random.default_rng(5)  # same data for every build
    idx = pd.date_range("2025-01-01", periods=n_steps + 1, freq="h")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ExperimentalFeatureWarning)
        es = solph.EnergySystem(
            timeindex=idx,
            investment_times=(idx[0], idx[4], idx[8], idx[-1]),
            infer_last_interval=False,
        )
    el = solph.Bus("el")
    es.add(el)
    price = 40 + 40 * rng.random(n_steps)
    es.add(
        solph.components.Source(
            "grid", outputs={el: solph.Flow(variable_costs=price)}
        ),
        solph.components.Source(
            "pv",
            outputs={
                el: solph.Flow(
                    fix=np.clip(np.sin(np.linspace(0, 3, n_steps)), 0, None),
                    nominal_capacity=solph.Investment(
                        # a list for `existing` fails in
                        # Investment._check_invest_attributes (both backends)
                        ep_costs=[10, 8, 6],
                        lifetime=1,
                        existing=1,
                    ),
                )
            },
        ),
        solph.components.Source(
            "engine",
            outputs={
                el: solph.Flow(
                    variable_costs=30,
                    nominal_capacity=solph.Investment(
                        ep_costs=[5, 5, 5], maximum=[4, 6, 8], lifetime=2
                    ),
                )
            },
        ),
        solph.components.Sink(
            "demand",
            inputs={
                el: solph.Flow(
                    fix=0.5 + 0.5 * rng.random(n_steps), nominal_capacity=6
                )
            },
        ),
        solph.components.GenericStorage(
            "battery",
            inputs={el: solph.Flow(nominal_capacity=solph.Investment())},
            outputs={el: solph.Flow(nominal_capacity=solph.Investment())},
            nominal_capacity=solph.Investment(ep_costs=[2, 2, 2]),
            invest_relation_input_capacity=0.5,
            invest_relation_output_capacity=0.5,
            loss_rate=0.01,
        ),
    )
    return es


def test_multi_period_investment():
    assert_backends_agree(
        multi_period_system,
        compare=("flow", "invest", "nominal_capacity", "storage_capacity"),
    )


def tsam_system(invest=False, nonconvex=False, segments=False):
    """Eight original hours aggregated to two typical periods of two
    hours (four model timesteps)."""

    def build():
        idx = pd.date_range("2022-01-01", periods=4, freq="h")
        parameters = {"timesteps_per_period": 2, "order": [0, 1, 1, 0]}
        if segments:
            parameters["segments"] = {
                (0, 0): 1,
                (0, 1): 1,
                (1, 0): 1,
                (1, 1): 1,
            }
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ExperimentalFeatureWarning)
            es = solph.EnergySystem(
                timeindex=idx,
                tsa_parameters=[parameters],
                infer_last_interval=True,
            )
        el = solph.Bus("electricity")
        es.add(el)
        es.add(
            solph.components.Source(
                "wind",
                outputs={
                    el: solph.Flow(fix=[1, 0, 0.8, 0.2], nominal_capacity=10)
                },
            ),
            solph.components.Source(
                "grid",
                outputs={
                    el: solph.Flow(
                        variable_costs=[50, 60, 70, 40],
                        nominal_capacity=10,
                        minimum=0.2 if nonconvex else 0,
                        nonconvex=(
                            solph.NonConvex(activity_costs=5)
                            if nonconvex
                            else None
                        ),
                    )
                },
            ),
            solph.components.Sink(
                "demand",
                inputs={el: solph.Flow(fix=[4, 5, 6, 5], nominal_capacity=1)},
            ),
            solph.components.Sink(
                "excess", inputs={el: solph.Flow(variable_costs=1)}
            ),
        )
        if invest:
            storage = solph.components.GenericStorage(
                "storage",
                inputs={el: solph.Flow(nominal_capacity=solph.Investment())},
                outputs={el: solph.Flow(nominal_capacity=solph.Investment())},
                nominal_capacity=solph.Investment(ep_costs=3),
                invest_relation_input_capacity=1,
                invest_relation_output_capacity=1,
                loss_rate=0.05,
                outflow_conversion_factor=0.9,
            )
        else:
            storage = solph.components.GenericStorage(
                "storage",
                inputs={el: solph.Flow(nominal_capacity=6)},
                outputs={el: solph.Flow(nominal_capacity=6)},
                nominal_capacity=20,
                loss_rate=0.05,
                min_storage_level=0.1,
                outflow_conversion_factor=0.9,
                balanced=True,
            )
        es.add(storage)
        return es

    return build


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(),
        dict(invest=True),
        dict(nonconvex=True),
        dict(segments=True),
    ],
    ids=["storage", "investment storage", "nonconvex", "segments"],
)
def test_tsam_mode(kwargs):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ExperimentalFeatureWarning)
        # the MILP with a nonconvex flow has alternative optima
        compare = (
            ()
            if kwargs.get("nonconvex")
            else ("flow", "inter_storage_content", "intra_storage_delta")
        )
        assert_backends_agree(tsam_system(**kwargs), compare=compare)


def test_tsam_processing_results():
    """processing.results disaggregates the typical periods the same way."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ExperimentalFeatureWarning)
        pyomo_model, _, linopy_model, _ = solve_both(tsam_system())
        pyomo_results = processing.results(pyomo_model)
        linopy_results = processing.results(linopy_model)

    def by_label(results):
        return {
            tuple(str(getattr(k, "label", k)) for k in key): value
            for key, value in results.items()
        }

    pyomo_results = by_label(pyomo_results)
    linopy_results = by_label(linopy_results)
    assert pyomo_results.keys() == linopy_results.keys()
    for key in pyomo_results:
        left = pyomo_results[key]["sequences"]
        right = linopy_results[key]["sequences"]
        assert list(left.columns) == list(right.columns), key
        np.testing.assert_allclose(
            left.to_numpy(dtype=float),
            right.to_numpy(dtype=float),
            atol=1e-6,
            err_msg=str(key),
        )
