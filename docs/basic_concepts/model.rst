.. _basic_concepts_model_label:

~~~~~~~~~~~~~~~~~~
Optimization Model
~~~~~~~~~~~~~~~~~~

The typical optimisation of an energy system in solph is the dispatch
optimisation (:ref:`optimization_dispatch_vs_invest_label`), which means that
the use of the sources is optimised to satisfy the demand at least costs. The
capacities of component must be fixed, i.e. the attribute `nominal_capacity` of
a flow assigned to the component should be used

.. code-block:: python

    >>> from oemof import solph
    >>> my_energysystem = solph.EnergySystem(
    ...     timeindex=solph.create_time_index(2025, number=24)
    ... )

    >>> bus_electricity = solph.Bus("electricity")
    >>> bus_gas = solph.Bus("gas")
    >>> gas_grid = solph.components.Source(
    ...     label="gas grid",
    ...     outputs={
    ...         bus_gas: solph.Flow(
    ...             nominal_capacity=1000,
    ...             variable_costs=50
    ...         )
    ...     },
    ... )

    >>> electricity_grid = solph.components.Sink(
    ...     label="electricity grid",
    ...     inputs={
    ...         bus_electricity: solph.Flow(
    ...             fix=100,
    ...             nominal_capacity=1
    ...         )
    ...     },
    ... )

Variable costs can be defined for each components. For example, the cost for
gas could be defined in the gas source The operating costs of the gas power
plant could be defined in gas power plant converter.

.. code-block:: python

    >>> power_plant = solph.components.Converter(
    ...     label="gas_power_plant",
    ...     inputs={
    ...         bus_gas: solph.Flow()
    ...     },
    ...     outputs={
    ...         bus_electricity: solph.Flow()
    ...     },
    ...     conversion_factors={bus_electricity: 0.58},
    ... )

    >>> my_energysystem.add(
    ...    bus_electricity, bus_gas, gas_grid, electricity_grid, power_plant
    ... )

Costs do not have to be monetary costs but could be emissions or other variable
units.

Furthermore, it is possible to optimise the capacity of different components
using the investment mode (see :ref:`optimization_invest_label`).

.. note::

    Since v0.5.1, there also is the possibility to have multi-period (i.e. dynamic)
    investments over longer-time horizon which is in experimental state (see
    :ref:`optimization_multi_period_label`).

.. code-block:: python

    # set up a simple least cost optimisation
    >>> om = solph.Model(my_energysystem)

    # solve the energy model using the CBC solver
    >>> result = om.solve(solver='cbc')

If you want to analyse the lp-file to see all equations and bounds you can
write it into a file. In that case, it is recommended to reduce the number of
timesteps to 3, to increase the readability of the file.

Solver
------

For a list on possible solver please have a look at SOLVER_SECTION_LINK

..
   TODO Move/link the lp-file to the debugging section
