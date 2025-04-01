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


def test_infeasible_model():
    es = solph.EnergySystem(
        timeindex=solph.create_time_index(2025, number=1)
    )
    bel = solph.buses.Bus(label="bus")
    es.add(bel)
    es.add(
        solph.components.Sink(
            inputs={bel: solph.flows.Flow(nominal_capacity=5, fix=[1])}
        )
    )
    es.add(
        solph.components.Source(
            outputs={
                bel: solph.flows.Flow(nominal_capacity=4, variable_costs=5)
            }
        )
    )
    m = solph.Model(es)
    with pytest.warns(
        UserWarning, match="The solver did not return an optimal solution"
    ):
        m.solve(solver="cbc", allow_nonoptimal=True)

    with pytest.raises(
        RuntimeError, match="The solver did not return an optimal solution"
    ):
        m.solve(solver="cbc", allow_nonoptimal=False)


def test_unbounded_model():
    es = solph.EnergySystem(timeindex=solph.create_time_index(2025, number=1))
    bel = solph.buses.Bus(label="bus")
    es.add(bel)
    # Add a Sink with a higher demand
    es.add(solph.components.Sink(inputs={bel: solph.flows.Flow()}))

    # Add a Source with a very high supply
    es.add(
        solph.components.Source(
            outputs={bel: solph.flows.Flow(variable_costs=-5)}
        )
    )
    m = solph.Model(es)

    with pytest.raises(
        RuntimeError, match="The solver did not return an optimal solution"
    ):
        m.solve(solver="cbc", allow_nonoptimal=False)
