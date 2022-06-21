# -*- coding: utf-8 -

"""Basic tests.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/basic_tests.py

SPDX-License-Identifier: MIT
"""

import warnings

import pytest

from oemof import solph


def test_optimal_solution():
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
            outputs={bel: solph.flows.Flow(variable_costs=5)}
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
