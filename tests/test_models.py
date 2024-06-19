# -*- coding: utf-8 -

"""Basic tests.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/basic_tests.py

SPDX-License-Identifier: MIT
"""

import warnings

import pandas as pd
import pytest

from oemof import solph


def test_optimal_solution():
    es = solph.EnergySystem(timeincrement=[1])
    bel = solph.buses.Bus(label="bus")
    es.add(bel)
    es.add(
        solph.components.Sink(
            label="sink",
            inputs={bel: solph.flows.Flow(nominal_value=5, fix=[1])},
        )
    )
    es.add(
        solph.components.Source(
            label="source",
            outputs={bel: solph.flows.Flow(variable_costs=5)},
        )
    )
    m = solph.Model(es)
    m.solve("cbc")
    m.results()
    solph.processing.meta_results(m)


def test_infeasible_model():
    # FutureWarning is i.e. emitted by network Entity registry
    warnings.simplefilter(action="ignore", category=FutureWarning)

    with pytest.raises(ValueError, match=""):
        with warnings.catch_warnings(record=True) as w:
            es = solph.EnergySystem(timeincrement=[1])
            bel = solph.buses.Bus(label="bus")
            es.add(bel)
            es.add(
                solph.components.Sink(
                    inputs={bel: solph.flows.Flow(nominal_value=5, fix=[1])}
                )
            )
            es.add(
                solph.components.Source(
                    outputs={
                        bel: solph.flows.Flow(
                            nominal_value=4, variable_costs=5
                        )
                    }
                )
            )
            m = solph.Model(es)
            m.solve(solver="cbc")
            assert "Optimization ended with status" in str(w[0].message)
            solph.processing.meta_results(m)


@pytest.mark.filterwarnings(
    "ignore:Ensure that your timeindex and timeincrement are"
    " consistent.:UserWarning"
)
@pytest.mark.filterwarnings(
    "ignore:CAUTION! You specified the 'periods' attribute:UserWarning"
)
def test_multi_period_default_discount_rate():
    """Test error being thrown for default multi-period discount rate"""
    timeindex = pd.date_range(start="2017-01-01", periods=100, freq="D")
    es = solph.EnergySystem(
        timeindex=timeindex,
        timeincrement=[1] * len(timeindex),
        periods=[timeindex],
        infer_last_interval=False,
    )
    bel = solph.buses.Bus(label="bus")
    es.add(bel)
    es.add(
        solph.components.Sink(
            label="sink",
            inputs={
                bel: solph.flows.Flow(
                    nominal_value=5, fix=[1] * len(timeindex)
                )
            },
        )
    )
    es.add(
        solph.components.Source(
            label="source",
            outputs={bel: solph.flows.Flow(nominal_value=4, variable_costs=5)},
        )
    )
    msg = (
        "By default, a discount_rate of 0.02 is used for a multi-period model."
    )
    with warnings.catch_warnings(record=True) as w:
        solph.Model(es)
        assert msg in str(w[0].message)
