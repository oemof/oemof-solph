.. SPDX-FileCopyrightText: oemof e.V. and contributors
..
.. SPDX-License-Identifier: MIT

.. _optimization_linopy_backend_label:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
linopy backend (experimental)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:class:`oemof.solph.LinopyModel` builds the optimisation problem of an
:class:`~oemof.solph.EnergySystem` with `linopy <https://linopy.readthedocs.io>`_
instead of Pyomo. Both backends read the same energy system and build the
same problem; the linopy backend creates variables and constraints as
arrays, which makes building the model and handing it to the solver much
faster for large models. For small models (a few hundred timesteps or
fewer) Pyomo is faster to build.

Install the optional dependency and use the model class like
:class:`~oemof.solph.Model`:

.. code-block:: bash

    pip install oemof.solph[linopy]

.. code-block:: python

    from oemof import solph

    model = solph.LinopyModel(energysystem)
    results = model.solve(solver="highs")
    results.get("flow")

``solve()`` takes the same arguments as :meth:`oemof.solph.Model.solve`.
HiGHS and other solvers with an in-memory interface are called directly;
CBC, GLPK and others through LP files. :class:`~oemof.solph.Results`,
:func:`~oemof.solph.processing.results` and :mod:`~oemof.solph.views`
work with both backends.

Not supported yet
=================

:func:`~oemof.solph.constraints.storage_level_constraint` in solph's
time series aggregation mode (energy systems with ``tsa_parameters``)
raises :class:`NotImplementedError`. Everything else, including
multi-period investment and the tsam mode itself, is supported.

Custom constraints
==================

The functions in :mod:`oemof.solph.constraints` work with both backends.
Constraints written against the Pyomo model have to be written again for
linopy. Variables are read as in the Pyomo model:

=====================================================  ==========================================================
Pyomo backend                                          linopy backend
=====================================================  ==========================================================
``model.flow[i, o, t]``                                ``model.flow_var(i, o)`` (all timesteps) or
                                                       ``model.flow_var(i, o).isel(timestep=t)``
``model.InvestmentFlowBlock.invest[i, o, p]``          ``model.InvestmentFlowBlock.invest[i, o, p]``
``model.GenericStorageBlock.storage_content[n, t]``    ``model.GenericStorageBlock.storage_content[n, t]``
``po.Constraint(model.TIMESTEPS, rule=...)``           ``model.linopy.add_constraints(<expression over all
                                                       timesteps>, name=...)``
=====================================================  ==========================================================

For example, a flow that has to deliver at least a share of all inflows
of its target, and a limit on the fuel use:

.. code-block:: python

    # Pyomo
    om = solph.Model(es)
    om.inflow_share = po.Constraint(
        om.TIMESTEPS,
        rule=lambda m, t: om.flow[oil, plant, t]
        >= share[t] * sum(om.flow[i, o, t] for (i, o) in om.FLOWS if o == plant),
    )
    om.fuel_limit = po.Constraint(
        expr=sum(om.flow[oil, plant, t] for t in om.TIMESTEPS) <= 60
    )

    # linopy
    lm = solph.LinopyModel(es)
    inflows = sum(lm.flow_var(i, o) for (i, o) in lm.FLOWS if o == plant)
    share = xr.DataArray(share, dims="timestep")
    lm.linopy.add_constraints(
        lm.flow_var(oil, plant) - share * inflows >= 0, name="inflow_share"
    )
    lm.linopy.add_constraints(
        lm.flow_var(oil, plant).sum() <= 60, name="fuel_limit"
    )

Write constraints over all timesteps at once, not one per timestep: this
is what makes linopy fast.

Components with their own constraint block
==========================================

A component whose ``constraint_group()`` returns its own Pyomo block needs
a linopy builder as well, registered for that block class:

.. code-block:: python

    from oemof.solph._linopy import register_builder

    @register_builder(MyComponentBlock)
    def build_my_components(model, group):
        ...  # model.flow, model.add_variables, model.add_constraints

Without one, building a :class:`~oemof.solph.LinopyModel` raises
:class:`NotImplementedError` naming the block.

Changing parameters and solving again
=====================================

With ``persistent=True`` the solver keeps its model. After changing
parameters, the linopy model is rebuilt from the energy system (fast) and
the solver applies the difference in place, keeping its warm start:

.. code-block:: python

    model = solph.LinopyModel(energysystem)
    model.solve(solver="highs", persistent=True)

    model.update(
        flows={(grid, el): {"variable_costs": new_prices}},
        nodes={heat_pump: {"conversion_factors": {heat: new_cop}}},
    )
    results = model.resolve()

Attributes of a flow's ``Investment`` or ``NonConvex`` are addressed with a
dot, e.g. ``"investment.ep_costs"``. Changing the energy system directly
and calling ``model.rebuild()`` does the same as ``update()``. Costs,
bounds, right-hand sides and coefficients are changed in place; a change
of the model's structure (other variables or constraints) makes the solver
rebuild its model, or raises with ``resolve(require_in_place=True)``.
Constraints that should survive a rebuild are added with
``model.add_custom_constraints(callback)``.
