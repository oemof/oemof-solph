.. _basic_concepts_model_label:

~~~~~~~~~~~~~~~~~~
Optimization Model
~~~~~~~~~~~~~~~~~~

The typical optimisation of an energy system in solph is the dispatch optimisation, which means that the use of the sources is optimised to satisfy the demand at least costs.
Therefore, variable cost can be defined for all components. The cost for gas should be defined in the gas source while the variable costs of the gas power plant are caused by operating material.
The actual fuel cost in turn is calculated in the framework itself considering the efficiency of the power plant.
You can deviate from this scheme but you should keep it consistent to make it understandable for others.

Costs do not have to be monetary costs but could be emissions or other variable units.

Furthermore, it is possible to optimise the capacity of different components using the investment mode (see :ref:`investment_mode_label`).

Since v0.5.1, there also is the possibility to have multi-period (i.e. dynamic) investments over longer-time horizon which is in experimental state (see :ref:`multi_period_mode_label`).

.. code-block:: python

    # set up a simple least cost optimisation
    om = solph.Model(my_energysystem)

    # solve the energy model using the CBC solver
    om.solve(solver='cbc', solve_kwargs={'tee': True})

If you want to analyse the lp-file to see all equations and bounds you can write the file to you disc. In that case you should reduce the timesteps to 3. This will increase the readability of the file.

