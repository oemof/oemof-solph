# -*- coding: utf-8 -*-

"""
General description
-------------------
The example of `add_constraints.py` with the (experimental) linopy
backend: user-defined constraints added to a solph model.

With linopy, constraints are written for all timesteps at once, from the
flow variables ``model.flow_var(source, target)`` (dimension
"timestep"), and added to the underlying linopy model ``model.linopy``.
``model.add_custom_constraints`` adds them again whenever the model is
rebuilt (e.g. by ``model.update``).

Code
----
Download source code: :download:`add_constraints_linopy.py </../examples/flexible_modelling/add_constraints_linopy.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/flexible_modelling/add_constraints_linopy.py
        :language: python
        :lines: 43-

Installation requirements
-------------------------
This example requires oemof.solph with the linopy extra, install by:

.. code:: bash

    pip install oemof.solph[linopy]

SPDX-FileCopyrightText: oemof e.V. and contributors

SPDX-License-Identifier: MIT
"""

import logging

import xarray as xr
from add_constraints import main as build_energy_system

from oemof import solph


def main(solver="highs", nologg=False):
    if not nologg:
        logging.basicConfig(level=logging.INFO)

    es = build_energy_system(optimize=False, nologg=True)
    boil = es.groups["oil"]
    blig = es.groups["lignite"]
    pp_oil = es.groups["pp_oil"]

    # create the model
    om = solph.LinopyModel(energysystem=es)

    # add specific emission values to flow objects if source is a commodity bus
    for s, t in om.flows.keys():
        if s is boil:
            om.flows[s, t].emission_factor = 0.27  # t/MWh
        if s is blig:
            om.flows[s, t].emission_factor = 0.39  # t/MWh
    emission_limit = 60e3

    # add the outflow share
    om.flows[(boil, pp_oil)].outflow_share = [1, 0.5, 0, 0.3]

    def my_constraints(m):
        # the flow with an outflow share has to deliver at least that share
        # of all inflows into its target, at every timestep
        for (s, e), flow in m.flows.items():
            if not hasattr(flow, "outflow_share"):
                continue
            inflows = sum(m.flow_var(i, o) for (i, o) in m.FLOWS if o == e)
            share = xr.DataArray(flow.outflow_share, dims="timestep")
            m.linopy.add_constraints(
                m.flow_var(s, e) - share * inflows >= 0,
                name=f"inflow_share_{s.label}_{e.label}",
            )

        # the commodity flows are limited in total, over all timesteps
        commodity_flows = [
            k for k, v in m.flows.items() if hasattr(v, "emission_factor")
        ]
        total = sum(m.flow_var(i, o).sum() for (i, o) in commodity_flows)
        m.linopy.add_constraints(total <= emission_limit, name="emission")

    om.add_custom_constraints(my_constraints)

    # solve and write results to dictionary
    om.solve(solver=solver)
    logging.info("Successfully finished.")


if __name__ == "__main__":
    main()
