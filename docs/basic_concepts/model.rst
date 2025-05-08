.. _basic_concepts_model_label:

~~~~~~~~~~~~~~~~~~
Optimization Model
~~~~~~~~~~~~~~~~~~

The typical optimisation of an energy system in solph is the dispatch optimisation (:ref:`optimization_dispatch_vs_invest_label`), which means that the use of the sources is optimised to satisfy the demand at least costs. The capacities of component must be fixed, i.e. the attribute `nominal_capacity` of a flow assigned to the component should be used

.. code-block:: python

    components.Source(
        label="gas_source",
        outputs={
            bus_1: flows.Flow(
                nominal_capacity=1000
            )
        },
    )

Variable costs can be defined for each components. For example, the cost for gas could be defined in the gas source The operating costs of the gas power plan could be defined in gas power plant converter.

.. code-block:: python

        components.Converter(
            label="gas_power_plan",
            outputs={
                bus_1: flows.Flow(
                    variable_costs=50
                )
            },
            conversion_factors={bus_electricity: 0.58},
        )


Costs do not have to be monetary costs but could be emissions or other variable units.

Furthermore, it is possible to optimise the capacity of different components using the investment mode (see :ref:`optimization_invest_label`).

Since v0.5.1, there also is the possibility to have multi-period (i.e. dynamic) investments over longer-time horizon which is in experimental state (see :ref:`optimization_multi_period_label`).

.. code-block:: python

    # set up a simple least cost optimisation
    om = solph.Model(my_energysystem)

    # solve the energy model using the CBC solver
    om.solve(solver='cbc', solve_kwargs={'tee': True})

If you want to analyse the lp-file to see all equations and bounds you can write it into a file. In that case, it is recommended to reduce the number of timesteps to 3, to increase the readability of the file.

Solver
------

For a list on possible solver please have a look at SOLVER_SECTION_LINK

..
   TODO Move/link the lp-file to the debugging section
