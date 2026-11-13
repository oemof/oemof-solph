# -*- coding: utf-8 -*-

"""
General description
-------------------
The example of `emission_constraint.py` with the (experimental) linopy
backend: the functions in `solph.constraints` work for both backends.

Code
----
Download source code: :download:`emission_constraint_linopy.py </../examples/emission_constraint/emission_constraint_linopy.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/emission_constraint/emission_constraint_linopy.py
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

import matplotlib.pyplot as plt
from emission_constraint import main as build_energy_system

from oemof import solph
from oemof.solph import constraints


def main(solver="highs"):
    energysystem = build_energy_system(optimize=False)

    model = solph.LinopyModel(energysystem)

    # add the emission constraint
    constraints.emission_limit(model, limit=100)

    # print out the emission constraint (in the Pyomo version: pprint())
    print(
        model.linopy.constraints["integral_limit_emission_factor_upper_limit"]
    )
    print(model.expression("integral_limit_emission_factor"))

    # solve the model
    results = model.solve(solver=solver)

    # print out the amount of emissions from the emission constraint
    print(model.integral_limit_emission_factor())

    data = results["flow"]
    outflows = data.xs("electricity", axis=1, level=0, drop_level=False)
    inflows = data.xs("electricity", axis=1, level=1, drop_level=False)

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.stackplot(
        inflows.index,
        inflows.T,
        labels=[f"supply: {col[0]}" for col in inflows.columns],
    )
    ax.plot(outflows, "k--", label="demand")
    ax.legend()
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("P (MW)")
    plt.show()


if __name__ == "__main__":
    main()
