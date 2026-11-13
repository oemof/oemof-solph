# -*- coding: utf-8 -*-

"""
General description
-------------------
The example of `dual_and_milp.py` with the (experimental) linopy backend:
solve a MILP, fix its integer and binary variables to the solution, relax
the problem and solve the resulting LP to get dual variables and reduced
costs.

Code
----
Download source code: :download:`dual_and_milp_linopy.py </../examples/dual_variable_example/dual_and_milp_linopy.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/dual_variable_example/dual_and_milp_linopy.py
        :language: python
        :lines: 37-

Installation requirements
-------------------------
This example requires oemof.solph with the linopy extra, install by:

.. code:: bash

    pip install oemof.solph[linopy]

SPDX-FileCopyrightText: oemof e.V. and contributors

SPDX-License-Identifier: MIT
"""

from dual_and_milp import milp_es

from oemof import solph


def main(solver="highs"):
    # Solve MILP
    m = solph.LinopyModel(milp_es())
    m.solve(solver=solver)

    # Fix all integer and binary variables to their solution. linopy keeps
    # them by name, e.g. "NonConvexFlowBlock.status".
    for name in list(m.linopy.binaries) + list(m.linopy.integers):
        m.linopy.variables[name].fix()

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
