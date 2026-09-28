# -*- coding: utf-8 -*-

"""
General description
-------------------

A basic example to show how to get the dual variables from the system. Try
to understand the plot.

Code
----
Download source code: :download:`dual_variable_example.py </../examples/dual_variable_example/dual_and_milp.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/dual_variable_example/dual_and_milp.py
        :language: python
        :lines: 34-


Installation requirements
-------------------------

This example requires oemof.solph (at least v0.6.6), install by:

.. code:: bash

    pip install oemof.solph>=0.6.6

SPDX-FileCopyrightText: oemof e.V. and contributors

SPDX-License-Identifier: MIT
"""

import pyomo.environ as po
from oemof import solph


def milp_es():
    es = solph.EnergySystem(timeindex=[0, 1, 2], infer_last_interval=False)
    bus = solph.buses.Bus(label="bus")
    es.add(bus)
    es.add(
        solph.components.Source(
            label="source",
            outputs={
                bus: solph.flows.Flow(
                    variable_costs=10,
                    nominal_capacity=100,
                    nonconvex=solph.NonConvex(),
                )
            },
        )
    )
    es.add(
        solph.components.Sink(
            label="sink",
            inputs={
                bus: solph.flows.Flow(
                    minimum=[0.5, 0.8, 0.3], nominal_capacity=100
                )
            },
        )
    )
    return es


def main(solver="cbc"):
    # Solve MILP
    m = solph.Model(milp_es())
    m.solve(solver=solver)

    # Fix all integer and binary variables.
    for var in m.component_objects(po.Var, active=True):
        for index in var:
            v = var[index]
            if v.domain in (po.Binary, po.Integers, po.NonNegativeIntegers):
                v.fix(v.value)

    # Relax problem to get real LP
    m.relax_problem()

    # Solve LP and receive results for dual variables and reduced cost.
    lp_results = m.solve(solver=solver, duals=True)

    duals = lp_results.get("duals")
    reduced_costs = lp_results.get("reduced_costs")

    print(duals)
    print(reduced_costs)


if __name__ == "__main__":
    main()
