# -*- coding: utf-8 -

"""Basic tests.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/basic_tests.py

SPDX-License-Identifier: MIT
"""

import pytest
from pyomo.opt.results import SolverResults

from oemof import solph


def test_infeasible_model():
    es = solph.EnergySystem(timeindex=[0, 1], infer_last_interval=False)
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
        result = m.solve(solver="cbc", allow_nonoptimal=True)
        assert isinstance(result, SolverResults)

    with pytest.raises(
        RuntimeError, match="The solver did not return an optimal solution"
    ):
        m.solve(solver="cbc", allow_nonoptimal=False)


def test_unbounded_model():
    es = solph.EnergySystem(timeindex=[0, 1], infer_last_interval=False)
    bel = solph.buses.Bus(label="bus")
    es.add(bel)
    # unbound Sink
    es.add(solph.components.Sink(inputs={bel: solph.flows.Flow()}))

    # unbound Source with a revenue
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


def test_cmdline_options(capsys):
    es = solph.EnergySystem(timeindex=[0, 1], infer_last_interval=False)
    bel = solph.buses.Bus(label="bus")
    es.add(bel)
    # bound Sink
    es.add(
        solph.components.Sink(
            inputs={bel: solph.flows.Flow(nominal_capacity=4)}
        )
    )

    # Source with a revenue
    es.add(
        solph.components.Source(
            outputs={bel: solph.flows.Flow(variable_costs=-5)}
        )
    )
    m = solph.Model(es)

    m.solve(
        solver="cbc",
        cmdline_options={"ratio": 0.01},
        solve_kwargs={"tee": True},  # need to set to see command line
    )

    captured = capsys.readouterr()

    assert "-ratio 0.01" in captured.out
