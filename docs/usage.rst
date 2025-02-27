.. _oemof_solph_label:

.. _using_oemof_label:

~~~~~~~~~~~~
User's guide
~~~~~~~~~~~~

Solph is an oemof-package, designed to create and solve linear or mixed-integer linear optimization problems. The package is based on pyomo. To create an energy system model generic and specific components are available. To get started with solph, checkout the examples in the :ref:`examples_label` section.

This User's guide provides a user-friendly introduction into oemof.solph,
which includes small examples and nice illustrations.
However, the functionalities of oemof.solph go beyond the content of this User's guide section.
So, if you want to know all details of a certain component or a function,
please go the :ref:`api_reference_label`. There, you will find
a detailed and complete description of all oemof.solph modules.

How can I use solph?
--------------------

To use solph you have to install oemof.solph and at least one solver (see :ref:`installation_label`),
which can be used together with `pyomo <https://pyomo.readthedocs.io/en/stable/getting_started/installation.html>`_
(e.g. CBC, GLPK, Gurobi, Cplex).
You can test it by executing one of the existing examples (see :ref:`examples_label`).
Be aware that the examples require the CBC solver but you can change the solver name in the example files to your
solver.

Once the examples work you are close to your first energy model.


Handling of Warnings
^^^^^^^^^^^^^^^^^^^^

The solph library is designed to be as generic as possible to make it possible
to use it in different use cases. This concept makes it difficult to raise
Errors or Warnings because sometimes untypical combinations of parameters are
allowed even though they might be wrong in over 99% of the use cases.

Therefore, a SuspiciousUsageWarning was introduced. This warning will warn you
if you do something untypical. If you are sure that you know what you are doing
you can switch the warning off.

See `the debugging module of oemof-tools <https://oemof-tools.readthedocs.io/en/latest/usage.html#debugging>`_ for more
information.







Analysing your results
^^^^^^^^^^^^^^^^^^^^^^

If you want to analyse your results, you should first dump your EnergySystem instance to permanently store results. Otherwise you would have to run the simulation again.

.. code-block:: python

    my_energysystem.results = processing.results(om)
    my_energysystem.dump('my_path', 'my_dump.oemof')

If you need the meta results of the solver you can do the following:

.. code-block:: python

    my_energysystem.results['main'] = processing.results(om)
    my_energysystem.results['meta'] = processing.meta_results(om)
    my_energysystem.dump('my_path', 'my_dump.oemof')

To restore the dump you can simply create an EnergySystem instance and restore your dump into it.

.. code-block:: python

    import oemof.solph as solph
    my_energysystem = solph.EnergySystem()
    my_energysystem.restore('my_path', 'my_dump.oemof')
    results = my_energysystem.results

    # If you use meta results do the following instead of the previous line.
    results = my_energysystem.results['main']
    meta = my_energysystem.results['meta']


If you call dump/restore without any parameters, the dump will be stored as *'es_dump.oemof'* into the *'.oemof/dumps/'* folder created in your HOME directory.

See :ref:`oemof_outputlib_label` to learn how to process, plot and analyse the results.






.. _investment_mode_label:

Investment optimisation
-------------------------

As described in :ref:`oemof_solph_optimise_es_label` the typical way to optimise an energy system is the dispatch optimisation based on marginal costs. Solph also provides a combined dispatch and investment optimisation.
This standard investment mode is limited to one period where all investments happen at the start of the optimization time frame. If you want to optimize longer-term horizons and allow investments at the beginning
of each of multiple periods, also taking into account units lifetimes, you can try the :ref:`multi_period_mode_label`. Please be aware that the multi-period feature is experimental. If you experience any bugs or unexpected
behaviour, please report them.

In the standard investment mode, based on investment costs you can compare the usage of existing components against building up new capacity.
The annual savings by building up new capacity must therefore compensate the annuity of the investment costs (the time period does not have to be one year, but depends on your Datetime index).

See the API of the :py:class:`~oemof.solph.options.Investment` class to see all possible parameters.

Basically, an instance of the Investment class can be added to a Flow, a
Storage or a DSM Sink. All parameters that usually refer to the *nominal_capacity* will
now refer to the investment variables and existing capacity. It is also
possible to set a maximum limit for the capacity that can be build.
If existing capacity is considered for a component with investment mode enabled,
the *ep_costs* still apply only to the newly built capacity, i.e. the existing capacity
comes at no costs.

The investment object can be used in Flows and some components. See the
:ref:`oemof_solph_components_label` section for detailed information of each
component. Besides the flows, it can be invested into

* :ref:`oemof_solph_components_generic_storage_label` and
* :ref:`oemof_solph_custom_sinkdsm_label`

For example if you want to find out what would be the optimal capacity of a wind
power plant to decrease the costs of an existing energy system, you can define
this model and add an investment source.
The *wind_power_time_series* has to be a normalised feed-in time series of you
wind power plant. The maximum value might be caused by limited space for wind
turbines.

.. code-block:: python

    solph.components.Source(label='new_wind_pp', outputs={electricity: solph.flows.Flow(
        fix=wind_power_time_series,
	nominal_capacity=solph.Investment(ep_costs=epc, maximum=50000))})

Let's slightly alter the case and consider for already existing wind power
capacity of 20,000 kW. We're still expecting the total wind power capacity, thus we
allow for 30,000 kW of new installations and formulate as follows.

.. code-block:: python

    solph.components.Source(label='new_wind_pp', outputs={electricity: solph.flows.Flow(
        fix=wind_power_time_series,
	    nominal_capacity=solph.Investment(ep_costs=epc,
	                                maximum=30000,
	                                existing=20000))})

The periodical costs (*ep_costs*) are typically calculated as annuities, i.e. as follows:

.. code-block:: python

    capex = 1000  # investment cost
    lifetime = 20  # life expectancy
    wacc = 0.05  # weighted average of capital cost
    epc = capex * (wacc * (1 + wacc) ** lifetime) / ((1 + wacc) ** lifetime - 1)

This also implemented in the annuity function of the economics module in the oemof.tools package. The code above would look like this:

.. code-block:: python

    from oemof.tools import economics
    epc = economics.annuity(1000, 20, 0.05)

So far, the investment costs and the installed capacity are mathematically a
line through origin. But what if there is a minimum threshold for doing an
investment, e.g. you cannot buy gas turbines lower than a certain
nominal power, or, the marginal costs of bigger plants
decrease.
Therefore, you can use the parameter *nonconvex* and *offset* of the
investment class. Both, work with investment in flows and storages. Here is an
example of a converter:

.. code-block:: python

    trafo = solph.components.Converter(
        label='converter_nonconvex',
        inputs={bus_0: solph.flows.Flow()},
        outputs={bus_1: solph.flows.Flow(
            nominal_capacity=solph.Investment(
                ep_costs=4,
                maximum=100,
                minimum=20,
                nonconvex=True,
                offset=400))},
        conversion_factors={bus_1: 0.9})

In this examples, it is assumed, that independent of the size of the
converter, there are always fix investment costs of 400 (€).
The minimum investment size is 20 (kW)
and the costs per installed unit are 4 (€/kW). With this
option, you could theoretically approximate every cost function you want. But
be aware that for every nonconvex investment flow or storage you are using,
an additional binary variable is created. This might boost your computing time
into the limitless.

The following figures illustrates the use of the nonconvex investment flow.
Here, :math:`c_{invest,fix}` is the *offset* value and :math:`c_{invest,var}` is
the *ep_costs* value:

.. 	figure:: /_files/nonconvex_invest_investcosts_power.svg
   :width: 70 %
   :alt: nonconvex_invest_investcosts_power.svg
   :align: center
   :figclass: only-light

.. 	figure:: /_files/nonconvex_invest_investcosts_power_darkmode.svg
   :width: 70 %
   :alt: nonconvex_invest_investcosts_power_darkmode.svg
   :align: center
   :figclass: only-dark

In case of a convex investment (which is the default setting
`nonconvex=False`), the *minimum* attribute leads to a forced investment,
whereas in the nonconvex case, the investment can become zero as well.

The calculation of the specific costs per kilowatt installed capacity results
in the following relation for convex and nonconvex investments:

.. 	figure:: /_files/nonconvex_invest_specific_costs.svg
   :width: 70 %
   :alt: nonconvex_invest_specific_costs.svg
   :align: center
   :figclass: only-light

.. 	figure:: /_files/nonconvex_invest_specific_costs_darkmode.svg
   :width: 70 %
   :alt: nonconvex_invest_specific_costs_darkmode.svg
   :align: center
   :figclass: only-dark

See :py:class:`~oemof.solph.blocks.investment_flow.InvestmentFlow` and
:py:class:`~oemof.solph.components._generic_storage.GenericInvestmentStorageBlock` for all the
mathematical background, like variables and constraints, which are used.

.. note:: At the moment the investment class is not compatible with the MIP classes :py:class:`~oemof.solph.options.NonConvex`.


.. _multi_period_mode_label:

Multi-period (investment) mode (experimental)
---------------------------------------------
Sometimes you might be interested in how energy systems could evolve in the longer-term, e.g. until 2045 or 2050 to meet some
carbon neutrality and climate protection or RES and energy efficiency targets.

While in principle, you could try to model this in oemof.solph using the standard investment mode described above (see :ref:`investment_mode_label`),
you would make the implicit assumption that your entire system is built at the start of your optimization and doesn't change over time.
To address this shortcoming, the multi-period (investment) feature has been introduced. Be aware that it is still experimental.
So feel free to report any bugs or unexpected behaviour if you come across them.

While in principle, you can define a dispatch-only multi-period system, this doesn't make much sense. The power of the multi-period feature
only unfolds if you look at long-term investments. Let's see how.

First, you start by defining your energy system as you might have done before, but you

* choose a longer-term time horizon (spanning multiple years, i.e. multiple periods) and
* explicitly define the `periods` attribute of your energy system which lists the time steps for each period.

.. code-block:: python

    import pandas as pd
    import oemof.solph as solph

    my_index = pd.date_range('1/1/2013', periods=17520, freq='h')
    periods = [
        pd.date_range('1/1/2013', periods=8760, freq='h'),
        pd.date_range('1/1/2014', periods=8760, freq='h'),
    ]
    my_energysystem = solph.EnergySystem(timeindex=my_index, periods=periods)

If you want to use a multi-period model you have define periods of your energy system explicitly. This way,
you are forced to critically think, e.g. about handling leap years, and take some design decisions. It is possible to
define periods with different lengths, but remember that decommissioning of components is possible only at the
beginning of each period. This means that if the life of a component is just a little longer, it will remain for the
entire next period. This can have a particularly large impact the longer your periods are.

To assist you, here is a plain python snippet that includes leap years which you can just copy
and adjust to your needs:

.. code-block:: python

    def determine_periods(datetimeindex):
        """Explicitly define and return periods of the energy system

        Leap years have 8784 hourly time steps, regular years 8760.

        Parameters
        ----------
        datetimeindex : pd.date_range
            DatetimeIndex of the model comprising all time steps

        Returns
        -------
        periods : list
            periods for the optimization run
        """
        years = sorted(list(set(getattr(datetimeindex, "year"))))
        periods = []
        filter_series = datetimeindex.to_series()
        for number, year in enumerate(years):
            start = filter_series.loc[filter_series.index.year == year].min()
            end = filter_series.loc[filter_series.index.year == year].max()
            periods.append(pd.date_range(start, end, freq=datetimeindex.freq))

        return periods

So if you want to use this, the above would simplify to:

.. code-block:: python

    import pandas as pd
    import oemof.solph as solph

    # Define your method (or import it from somewhere else)
    def determine_periods(datetimeindex):
        ...

    my_index = pd.date_range('1/1/2013', periods=17520, freq='h')
    periods = determine_periods(my_index)  # Make use of method
    my_energysystem = solph.EnergySystem(timeindex=my_index, periods=periods)


Then you add all the *components* and *buses* to your energy system, just as you are used to with, but with few additions.

.. code-block:: python

    hydrogen_bus = solph.buses.Bus(label="hydrogen")
    coal_bus = solph.buses.Bus(label="coal")
    electricity_bus = solph.buses.Bus(label="electricity")

    hydrogen_source = solph.components.Source(
        label="green_hydrogen",
        outputs={
            hydrogen_bus: solph.flows.Flow(
                variable_costs=[25] * 8760 + [30] * 8760
            )
        },
    )

    coal_source = solph.components.Source(
        label="hardcoal",
        outputs={
            coal_bus: solph.flows.Flow(variable_costs=[20] * 8760 + [24] * 8760)
        },
    )

    electrical_sink = solph.components.Sink(
        label="electricity_demand",
        inputs={
            electricity_bus: solph.flows.Flow(
                nominal_capacity=1000, fix=[0.8] * len(my_index)
            )
        },
    )

So defining buses is the same as for standard models. Also defining components that do not have any investments associated with
them or any lifetime limitations is the same.

Now if you want to have components that can be invested into, you use the investment option, just as in :ref:`investment_mode_label`,
but with a few minor additions and modifications in the investment object itself which you specify by additional attributes:

* You have to specify a `lifetime` attribute. This is the components assumed technical lifetime in years. If it is 20 years,
  the model invests into it and your simulation has a 30 years horizon, the plant will be decommissioned. Now the model is
  free to reinvest or choose another option to fill up the missing capacity.
* You can define an initial `age` if you have `existing` capacity. If you do not specify anything, the default value 0 will be used,
  meaning your `existing` capacity has just been newly invested.
* You also can define `fixed_costs`, i.e. costs that occur every period independent of the plants usage.

Here is an example

.. code-block:: python

    hydrogen_power_plant = solph.components.Converter(
        label="hydrogen_pp",
        inputs={hydrogen_bus: solph.flows.Flow()},
        outputs={
            electricity_bus: solph.flows.Flow(
                nominal_capacity=solph.Investment(
                    maximum=1000,
                    ep_costs=1e6,
                    lifetime=30,
                    fixed_costs=100,
                ),
                variable_costs=3,
            )
        },
        conversion_factors={electricity_bus: 0.6},
    )

.. warning::

    The `ep_costs` attribute for investments is used in a different way in a multi-period model. Instead
    of periodical costs, it depicts (nominal or real) investment expenses, so actual Euros you have to pay per kW or MW
    (or whatever power or energy unit) installed. Also, you can depict a change in investment expenses over time,
    so instead of providing a scalar value, you could define a list with investment expenses with one value for each period modelled.

    Annuities are calculated within the model. You do not have to do that.
    Also the model takes care of discounting future expenses / cashflows.

Below is what it would look like if you altered `ep_costs` and `fixed_costs` per period. This can be done by simply
providing a list. Note that the length of the list must equal the number of periods of your model.
This would mean that for investments in the particular period, these values would be the one that are applied over their lifetime.

.. code-block:: python

    hydrogen_power_plant = solph.components.Converter(
        label="hydrogen_pp",
        inputs={hydrogen_bus: solph.flows.Flow()},
        outputs={
            electricity_bus: solph.flows.Flow(
                nominal_capacity=solph.Investment(
                    maximum=1000,
                    ep_costs=[1e6, 1.1e6],
                    lifetime=30,
                    fixed_costs=[100, 110],
                ),
                variable_costs=3,
            )
        },
        conversion_factors={electricity_bus: 0.6},
    )

For components that is not invested into, you also can specify some additional attributes for their inflows and outflows:

* You can specify a `lifetime` attribute. This can be used to depict existing plants going offline when reaching their lifetime.
* You can define an initial `age`. Also, this can be used for existing plants.
* You also can define `fixed_costs`, i.e. costs that occur every period independent of the plants usage. How they are handled
  depends on whether the flow has a limited or an unlimited lifetime.

.. code-block:: python

    coal_power_plant = solph.components.Converter(
        label="existing_coal_pp",
        inputs={coal_bus: solph.flows.Flow()},
        outputs={
            electricity_bus: solph.flows.Flow(
                nominal_capacity=600,
                max=1,
                min=0.4,
                lifetime=50,
                age=46,
                fixed_costs=100,
                variable_costs=3,
            )
        },
        conversion_factors={electricity_bus: 0.36},
    )

To solve our model and retrieve results, you basically perform the same operations as for standard models.
So it works like this:

.. code-block:: python

    my_energysystem.add(
        hydrogen_bus,
        coal_bus,
        electricity_bus,
        hydrogen_source,
        coal_source,
        electrical_sink,
        hydrogen_power_plant,
        coal_power_plant,
    )

    om = solph.Model(my_energysystem)
    om.solve(solver="cbc", solve_kwargs={"tee": True})

    # Obtain results
    results = solph.processing.results(om)
    hydrogen_results = solph.views.node(results, "hydrogen_pp")

    # Show investment plan for hydrogen power plants
    print(hydrogen_results["period_scalars"])

The keys in the results dict in a multi-period model are "sequences" and "period_scalars".
So for sequences, it is all the same, while for scalar values, we now have values for each period.

Besides the `invest` variable, new variables are introduced as well. These are:

* `total`: The total capacity installed, i.e. how much is actually there in a given period.
* `old`: (Overall) capacity to be decommissioned in a given period.
* `old_end`: Endogenous capacity to be decommissioned in a given period. This is capacity that has been invested into
  in the model itself.
* `old_exo`: Exogenous capacity to be decommissioned in a given period. This is capacity that was already existing and
  given by the `existing` attribute.

.. note::

    * For storage units, the `initial_content` is not allowed combined with multi-period investments.
      The storage inflow and outflow are forced to zero until the storage unit is invested into.
    * You can specify periods of different lengths, but the frequency of your timeindex needs to be consistent. Also,
      you could use the `timeincrement` attribute of the energy system to model different weightings. Be aware that this
      has not yet been tested.
    * For now, both, the `timeindex` as well as the `timeincrement` of an energy system have to be defined since they
      have to be of the same length for a multi-period model.
    * You can choose whether to re-evaluate assets at the end of the optimization horizon. If you set attribute
      `use_remaining_value` of the energy system to True (defaults to False), this leads to the model evaluating the
      difference in the asset value at the end of the optimization horizon vs. at the time the investment was made.
      The difference in value is added to or subtracted from the respective investment costs increment,
      assuming assets are to be liquidated / re-evaluated at the end of the optimization horizon.
    * Also please be aware, that periods correspond to years by default. You could also choose
      monthly periods, but you would need to be very careful in parameterizing your energy system and your model and also,
      this would mean monthly discounting (if applicable) as well as specifying your plants lifetimes in months.


Mixed Integer (Linear) Problems
-------------------------------

Solph also allows you to model components with respect to more technical details,
such as minimum power production. This can be done in both possible combinations,
as dispatch optimization with fixed capacities or combined dispatch and investment optimization.

Dispatch Optimization
^^^^^^^^^^^^^^^^^^^^^
In dispatch optimization, it is assumed that the capacities of the assets are already known,
but the optimal dispatch strategy must be obtained.
For this purpose, the class :py:class:`~oemof.solph._options.NonConvex` should be used, as seen in the following example.

Note that this flow class's usage is incompatible with the :py:mod:`~oemof.solph.options.Investment` option. This means that,
as stated before, the optimal capacity of the converter cannot be obtained using the :py:class:`~oemof.solph.flows.NonConvexFlow`
class, and only the optimal dispatch strategy of an existing asset with a given capacity can be optimized here.

.. code-block:: python

    b_gas = solph.buses.Bus(label='natural_gas')
    b_el = solph.buses.Bus(label='electricity')
    b_th = solph.buses.Bus(label='heat')

    solph.components.Converter(
        label='pp_chp',
        inputs={b_gas: solph.flows.Flow()},
        outputs={b_el: solph.flows.Flow(
            nonconvex=solph.NonConvex(),
            nominal_capacity=30,
            min=0.5),
        b_th: solph.flows.Flow(nominal_capacity=40)},
        conversion_factors={b_el: 0.3, b_th: 0.4})

The class :py:class:`~oemof.solph.options.NonConvex` for the electrical output of the created Converter (i.e., CHP)
will create a 'status' variable for the flow.
This will be used to model, for example, minimal/maximal power production constraints if the
attributes `min`/`max` of the flow are set. It will also be used to include start-up constraints and costs
if corresponding attributes of the class are provided. For more information, see the API of the
:py:class:`~oemof.solph.flows.NonConvexFlow` class.

.. note:: The usage of this class can sometimes be tricky as there are many interdenpendencies. So
          check out the examples and do not hesitate to ask the developers if your model does
          not work as expected.

Combination of Dispatch and Investment Optimisation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Since version 'v0.5', it is also possilbe to combine the investment and nonconvex option.
Therefore, a new constraint block for flows, called :py:class:`~oemof.solph.flows._invest_non_convex_flow_block.InvestNonConvexFlowBlock` has been developed,
which combines both :py:class:`~oemof.solph._options.Investment` and :py:class:`~oemof.solph._options.NonConvex` classes.
The new class offers the possibility to perform the investment optimization of an asset considering `min`/`max` values of the flow
as fractions of the optimal capacity. Moreover, it obtains the optimal 'status' of the flow during the simulation period.

It must be noted that in a straighforward implementation, a binary variable
representing the 'status' of the flow at each time is multiplied by the 'invest' parameter,
which is a continuous variable representing the capacity of the asset being optimized (i.e., :math:`status \times invest`).
This nonlinearity is linearised in the
:py:class:`~oemof.solph.flows._invest_non_convex_flow_block.InvestNonConvexFlowBlock`

.. code-block:: python

    b_diesel = solph.buses.Bus(label='diesel')
    b_el = solph.buses.Bus(label='electricity')

    solph.components.Converter(
        label='diesel_genset',
        inputs={b_diesel: solph.flows.Flow()},
        outputs={
            b_el: solph.flows.Flow(
                variable_costs=0.04,
                min=0.2,
                max=1,
                nonconvex=solph.NonConvex(),
                nominal_capacity=solph.Investment(
                    ep_costs=90,
                    maximum=150, # required for the linearization
                ),
            )
        },
        conversion_factors={b_el: 0.3})

The following diagram shows the duration curve of a typical diesel genset in a hybrid mini-grid system consisting of a diesel genset,
PV cells, battery, inverter, and rectifier. By using the :py:class:`~oemof.solph.flows._invest_non_convex_flow_block.InvestNonConvexFlowBlock` class,
it is possible to obtain the optimal capacity of this component and simultaneously limit its operation between `min` and `max` loads.

.. 	figure:: /_files/diesel_genset_nonconvex_invest_flow.svg
   :width: 100 %
   :alt: diesel_genset_nonconvex_invest_flow.svg
   :align: center
   :figclass: only-light

.. 	figure:: /_files/diesel_genset_nonconvex_invest_flow_darkmode.svg
   :width: 100 %
   :alt: diesel_genset_nonconvex_invest_flow_darkmode.svg
   :align: center
   :figclass: only-dark

Without using the new :py:class:`~oemof.solph.flows._invest_non_convex_flow_block.InvestNonConvexFlowBlock` class, if the same system is optimized again, but this
time using the :py:class:`~oemof.solph.flows._investment_flow_block.InvestmentFlowBlock`, the corresponding duration curve would be similar to the following
figure. However, assuming that the diesel genset has a minimum operation load of 20% (as seen in the figure), the
:py:class:`~oemof.solph.flows._investment_flow_block.InvestmentFlowBlock` cannot prevent operations at lower loads than 20%, and it would result in
an infeasible operation of this device for around 50% of its annual operation.

Moreover, using the :py:class:`~oemof.solph.flows._investment_flow_block.InvestmentFlowBlock` class in the given case study would result in a significantly
oversized diesel genset, which has a 30% larger capacity compared with the optimal capacity obtained from the
:py:class:`~oemof.solph.flows._invest_non_convex_flow_block.InvestNonConvexFlowBlock` class.

.. 	figure:: /_files/diesel_genset_investment_flow.svg
   :width: 100 %
   :alt: diesel_genset_investment_flow.svg
   :align: center
   :figclass: only-light

.. 	figure:: /_files/diesel_genset_investment_flow_darkmode.svg
   :width: 100 %
   :alt: diesel_genset_investment_flow_darkmode.svg
   :align: center
   :figclass: only-dark


Solving such an optimisation problem considering `min`/`max` loads without the :py:class:`~oemof.solph.flows._invest_non_convex_flow_block.InvestNonConvexFlowBlock` class, the only possibility is first to obtain the optimal capacity using the
:py:class:`~oemof.solph.flows._investment_flow_block.InvestmentFlowBlock` and then implement the `min`/`max` loads using the
:py:class:`~oemof.solph.flows._non_convex_flow_block.NonConvexFlowBlock` class. The following duration curve would be obtained by applying
this method to the same diesel genset.

.. 	figure:: /_files/diesel_genset_nonconvex_flow.svg
   :width: 100 %
   :alt: diesel_genset_nonconvex_flow.svg
   :align: center
   :figclass: only-light

.. 	figure:: /_files/diesel_genset_nonconvex_flow_darkmode.svg
   :width: 100 %
   :alt: diesel_genset_nonconvex_flow_darkmode.svg
   :align: center
   :figclass: only-dark

Because of the oversized diesel genset obtained from this approach, the capacity of the PV and battery in the given case study
would be 13% and 43% smaller than the capacities obtained using the :py:class:`~oemof.solph.flows.NonConvexInvestmentFlow` class.
This results in a 15% reduction in the share of renewable energy sources to cover the given demand and a higher levelized
cost of electricity. Last but not least, apart from the nonreliable results, using :py:class:`~oemof.solph._options.Investment`
and :py:class:`~oemof.solph._options.NonConvex` classes for the dispatch and investment optimization of the given case study
increases the computation time by more than 9 times compared to the
:py:class:`~oemof.solph.flows.NonConvexInvestmentFlow` class.


Adding additional constraints
-----------------------------

You can add additional constraints to your :py:class:`~oemof.solph.models.Model`.
See :ref:`custom_constraints_label` to learn how to do it.

Some predefined additional constraints can be found in the
:py:mod:`~oemof.solph.constraints` module.

 * Emission limit for the model -> :func:`~.oemof.solph.constraints.emission_limit`
 * Generic integral limit (general form of emission limit) -> :func:`~.oemof.solph.constraints.generic_integral_limit`
 * Coupling of two variables e.g. investment variables) with a factor -> :func:`~.oemof.solph.constraints.equate_variables`
 * Overall investment limit -> :func:`~.oemof.solph.constraints.investment_limit`
 * Generic investment limit -> :func:`~.oemof.solph.constraints.additional_investment_flow_limit`
 * Limit active flow count -> :func:`~.oemof.solph.constraints.limit_active_flow_count`
 * Limit active flow count by keyword -> :func:`~.oemof.solph.constraints.limit_active_flow_count_by_keyword`


The Grouping module (Sets)
--------------------------
To construct constraints,
variables and objective expressions inside all Block classes
and the :py:mod:`~oemof.solph.models` modules, so called groups are used. Consequently,
certain constraints are created for all elements of a specific group. Thus,
mathematically the groups depict sets of elements inside the model.

The grouping is handled by the solph grouping module :py:mod:`~oemof.solph.groupings`
which is based on the groupings module functionality of oemof network. You
do not need to understand how the underlying functionality works. Instead, checkout
how the solph grouping module is used to create groups.

The simplest form is a function that looks at every node of the energy system and
returns a key for the group depending e.g. on node attributes:

.. code-block:: python

    def constraint_grouping(node):
        if isinstance(node, Bus) and node.balanced:
            return blocks.Bus
        if isinstance(node, Converter):
            return blocks.Converter
   GROUPINGS = [constraint_grouping]

This function can be passed in a list to `groupings` of
:class:`oemof.solph.network.energy_system.EnergySystem`. So that we end up with two groups,
one with all Converters and one with all Buses that are balanced. These
groups are simply stored in a dictionary. There are some advanced functionalities
to group two connected nodes with their connecting flow and others
(see for example: FlowsWithNodes class in the oemof.network package).


Using the Excel (csv) reader
----------------------------

Alternatively to a manual creation of energy system component objects as describe above, can also be created from a excel sheet (libreoffice, gnumeric...).

The idea is to create different sheets within one spreadsheet file for different components. Afterwards you can loop over the rows with the attributes in the columns. The name of the columns may differ from the name of the attribute. You may even create two sheets for the GenericStorage class with attributes such as C-rate for batteries or capacity of turbine for a PHES.

Once you have create your specific excel reader you can lower the entry barrier for other users. It is some sort of a GUI in form of platform independent spreadsheet software and to make data and models exchangeable in one archive.

See :ref:`excel_reader_example_label` for an excel reader example.


