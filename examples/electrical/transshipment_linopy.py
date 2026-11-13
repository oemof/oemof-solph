# -*- coding: utf-8 -*-

"""
General description
-------------------
The example of `transshipment.py` with the (experimental) linopy backend:
two buses connected by a lossy `Link` whose capacity is invested in.

Code
----
Download source code: :download:`transshipment_linopy.py </../examples/electrical/transshipment_linopy.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/electrical/transshipment_linopy.py
        :language: python
        :lines: 36-

Installation requirements
-------------------------
This example requires oemof.solph with the linopy extra, install by:

.. code:: bash

    pip install oemof.solph[linopy]

SPDX-FileCopyrightText: oemof e.V. and contributors

SPDX-License-Identifier: MIT
"""

from matplotlib import pyplot as plt
from transshipment import main as build_energy_system

from oemof import solph


def main(solver="highs"):
    es = build_energy_system(optimize=False)

    m = solph.LinopyModel(energysystem=es)
    results = m.solve(solver=solver, solve_kwargs={"tee": True})

    print(results["flow"][("gen_0", "b_0")])
    print(results["flow"][("gen_1", "b_1")])

    results["flow"].plot(kind="bar")

    # look at the constraints of the Links in the linopy model (the Pyomo
    # version prints m.LinkBlock.pprint())
    print(m.linopy.constraints["LinkBlock.relation"])

    plt.show()


if __name__ == "__main__":
    main()
