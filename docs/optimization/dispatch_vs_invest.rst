.. _optimization_dispatch_vs_invest_label:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Dispatch vs. Investment Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _optimization_dispatch_label:


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


.. _optimization_invest_label:

Investment optimization
^^^^^^^^^^^^^^^^^^^^^^^

As described in :ref:`optimization_multi_period_label` the typical way to optimise an energy system is the dispatch optimisation based on marginal costs. Solph also provides a combined dispatch and investment optimisation.
This standard investment mode is limited to one period where all investments happen at the start of the optimization time frame. If you want to optimize longer-term horizons and allow investments at the beginning
of each of multiple periods, also taking into account units lifetimes, you can try the :ref:`optimization_multi_period_label`. Please be aware that the multi-period feature is experimental. If you experience any bugs or unexpected
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
:ref:`basic_concepts_components_label` section for detailed information of each
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

In case of a convex investment (which is the default setting
`nonconvex=False`), the *minimum* attribute leads to a forced investment,
whereas in the nonconvex case, the investment can become zero as well.

The calculation of the specific costs per kilowatt installed capacity results
in the following relation for convex and nonconvex investments:

.. 	figure:: /_files/nonconvex_invest_specific_costs.svg
   :width: 70 %
   :alt: nonconvex_invest_specific_costs.svg
   :align: center

See :py:class:`~oemof.solph.blocks.investment_flow.InvestmentFlow` and
:py:class:`~oemof.solph.components._generic_storage.GenericInvestmentStorageBlock` for all the
mathematical background, like variables and constraints, which are used.

.. note:: At the moment the investment class is not compatible with the MIP classes :py:class:`~oemof.solph.options.NonConvex`.


Combination of Dispatch and Investment Optimization
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


Solving such an optimisation problem considering `min`/`max` loads without the :py:class:`~oemof.solph.flows._invest_non_convex_flow_block.InvestNonConvexFlowBlock` class, the only possibility is first to obtain the optimal capacity using the
:py:class:`~oemof.solph.flows._investment_flow_block.InvestmentFlowBlock` and then implement the `min`/`max` loads using the
:py:class:`~oemof.solph.flows._non_convex_flow_block.NonConvexFlowBlock` class. The following duration curve would be obtained by applying
this method to the same diesel genset.

.. 	figure:: /_files/diesel_genset_nonconvex_flow.svg
   :width: 100 %
   :alt: diesel_genset_nonconvex_flow.svg
   :align: center

Because of the oversized diesel genset obtained from this approach, the capacity of the PV and battery in the given case study
would be 13% and 43% smaller than the capacities obtained using the :py:class:`~oemof.solph.flows.NonConvexInvestmentFlow` class.
This results in a 15% reduction in the share of renewable energy sources to cover the given demand and a higher levelized
cost of electricity. Last but not least, apart from the nonreliable results, using :py:class:`~oemof.solph._options.Investment`
and :py:class:`~oemof.solph._options.NonConvex` classes for the dispatch and investment optimization of the given case study
increases the computation time by more than 9 times compared to the
:py:class:`~oemof.solph.flows.NonConvexInvestmentFlow` class.
