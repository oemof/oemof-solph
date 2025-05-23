.. _district_heating_portfolio_optimization_label:

District heating portfolio optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this tutorial, we will optimize the portfolio of a district heating supply system.

The tutorial is set up in three main steps:

1. Modeling the existing system delivering heat with a gas boiler
2. Adding a heat pump utilizing waste heat from datacenter and a thermal storage
3. Introducing a minimal load constraint to the heat production units

Each section contains a step by step explanation of how the district heating supply
system is build using oemof.solph. Additionally, the repository contains a fully
functional Python file of all three main steps for you to execute yourself or
modify and play around with.

Step 1: Status-Quo system
-------------------------

As described above, we want to start by building the existing district heating
supply systems, which in our simple example only contains a single gas boiler.

.. figure:: /_files/tutorial_dhs_1.svg
    :align: center
    :alt: Structure of the heating supplier's portfolio
    :figclass: only-light

    Structure of the heating supplier's portfolio

.. figure:: /_files/tutorial_dhs_1_darkmode.svg
    :align: center
    :alt: Structure of the heating supplier's portfolio
    :figclass: only-dark

    Structure of the heating supplier's portfolio

But before we start modeling the energy system, we should give some thought about
what kind of input data we need for the simulation.Maybe the first that comes to 
mind is the heat demand our system should supply.
As the demand varies throughout the seasons, it makes sense to simulate a full
year. Typically, this is done with an hourly time resolution. Furthermore, we have
to know the technical specifications of our gas boiler. This includes the existing
capacity (i.e. the nominal heat output of the unit), its efficiency as well as
variable cost arising with its operation. For simplicity and in good approximation
of the real behavior of gas boilers, we make the assumption that the efficiency is
constant. Finally, we need the price of the natural gas we burn inside the boiler.
This could be a constant value if the price is contractually fixed or a time series
of differing values if the gas is bought at an auction. For this tutorial, we assume
the latter case.

To get started with our model, we first import the pandas package to read in a
CSV file containing our time series input data. In this case, it includes the hourly
heat demand and gas prices. The first column however contains the time index we make
sure to be properly parsed. Generally, it is also recommended to use a parameter
file (e.g. in the JSON format) for the constant input data, but in a small example
like this, we opt to writing those values directly into the code.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_1_start]
    :end-before: [sec_1_end]

Now we can begin the modeling process of our district heating supply system. Every
oemof.solph model starts be creating (also called "initializing") the ``EnergySystem``.
To create an instance of the :py:class:`solph.EnergySystem` class, we have to import the solph
package at first. To enforce our simulation time period and resolution, we set its
:py:attr:`timeindex` keyword argument to the index of the input DataFrame.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_2_start]
    :end-before: [sec_2_end]

After that, we need to set up the two energy carrying buses, i.e. the heat and gas
network. We make sure to set a label for the two to reference them later when we
analyze the results. After initialization, we add them to the ``district_heating_system``
object.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_3_start]
    :end-before: [sec_3_end]

Now we add a gas source for our boiler. We initialize a :py:class:`solph.components.Source`
instance, give it a label and set the output to be the gas network, by setting it
to a dictionary with the ``gnw`` variable as key and the value to be a new :py:class:`solph.flows.Flow`
instance. To define the cost for using the gas source, we set the :py:attr:`variable_cost`
keyword argument to the 'gas price' column of our input data time series.

Defining the heat sink works very similar, but we use a :py:class:`solph.components.Sink`
and set its :py:attr:`inputs` argument instead. Also, we do not impose any costs
(even though we could set the :py:attr:`variable_cost` to a negative value to imply
a revenue). In order to enforce the heat demand to be covered at any point in time,
we use the :py:attr:`fix` argument. It takes a normalized time series that gets
multiplied with the :py:attr:`nominal_value`. Therefore, we set the latter to be
the maximum value of the time series and divide the whole time series by it when
setting the :py:attr:`fix` parameter.

Finally, both components get added to the energy system.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_4_start]
    :end-before: [sec_4_end]

Last, but not least, we will depict the gas boiler itself, using a simple linear
model with the :py:class:`solph.components.Converter` class. In contrast to the
components before, we have to define at least one input *and* one output, which in
case of the gas boiler is the natural gas burnt and the heat produced from it.
The connection from the gas network does not need any parametrization. We set the
:py:attr:`nominal_value` of the heat output to 20 MW (see note on units below) and
add :py:attr:`variable_cost` of 1.10 €/MWh. To depict energy losses due to thermodynamic
inefficiencies, we can set the :py:attr:`conversion_factors` keyword argument of
the :py:class:`solph.components.Converter`. It expects a dictionary, with a key
corresponding to the bus to which the value (scalar or iterable) is applied. So,
to model a constant efficiency of 95 %, we set it to 0.95. Do not forget to add
the gas boiler to the district heating supply system.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_5_start]
    :end-before: [sec_5_end]

.. note::
    Keep in mind that the units used in your energy system model are only implicit
    and that you have to check their consistency yourself.

FLOWCHART ENERGY SYSTEM

As our system is complete for this step, its time to start the unit commitment
optimization. For that, we first have to create a :py:class:`solph.Model` instance
from our ``district_heating_system``. Then we can use its :py:func:`solve` method
to run the optimization. We decide to use the open source solver
`CBC <https://projects.coin-or.org/Cbc>`_ and add the additional :py:attr:`solve_kwargs`
parameter ``'tee'`` to ``True``, in order to get a more verbose solver logging
output in the console.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_6_start]
    :end-before: [sec_6_end]

To receive the results, we pass the ``model`` into the ``results`` method
of the ``solph.processing`` submodule. We then use the ``node`` method of the
``solph.views`` submodule to access the results of the two buses ``'gas network'``
and ``'heat network'``. Specifically, we need the optimized unit commitment time
series, so we access the ``'sequences'`` key.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_7_start]
    :end-before: [sec_7_end]

Now, let's have a look at those results. We will create a simple bar plot of
the gas boilers unit commitment. To achieve this, we have to import a plotting
library like ``matplotlib``. We use its ``subplots`` method to create a figure
``fig`` and an axes ``ax`` and set the plots size to be ten by six inches.
Then, we pass the index of `data_heat_bus` and the column containing the gas
boiler's heat production into the axes ``bar`` method.

.. note::
    In ``oemof.solph``, indexing works by passing a tuple containing two items:
    at first, another tuple containing the string labels of the two nodes of
    interest and second, the the ``oemof.solph`` variable name to be extracted.
    In case of the example below, we are looking for the ``'flow'`` between the
    ``'gas boiler'`` and ``'heat network'`` nodes.

Finally, we set a label to the bars to be plotted that corresponds to the
unit's name. This is mostly anticipatory, as we will want to decern between
different heat production units later in this tutorial. To improve the plots
appearance, we add a legend in the upper right corner, grid lines along the
horizontal axis and a fitting label for the same. Feel free to change the look
of the plot to your heart's content. The final step to see the optimization
results is calling the ``show`` method.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_8_start]
    :end-before: [sec_8_end]

Your plot should look similar to this:

.. figure:: /_files/intro_tut_dhs_1_hourly_heat_production.svg
    :align: center
    :alt: System dispatch of heating system with gas boiler
    :figclass: only-light

    System dispatch of heating system with gas boiler

.. figure:: /_files/intro_tut_dhs_1_hourly_heat_production_darkmode.svg
    :align: center
    :alt: System dispatch of heating system with gas boiler
    :figclass: only-dark

    System dispatch of heating system with gas boiler

Let's continue by assessing the economic merit of our district heating supply
system. A common indicator for that purpose are the Levelized Cost of Heat
(:math:`LCOH`). As shown in equation :eq:`eq:LCOH`, they account for the
upfront invest cost :math:`C_\text{invest}` necessary to build the heat
production units as well as the cost evoked via their operation
:math:`C_\text{operation}` over the unit's assumed lifetime :math:`n`. These
cost get reduced by any additional revenues :math:`R` generated besides its
heat production. The total cash flow balance is then devided by the total heat
produced :math:`Q_\text{total}`. In order to make one-off investments
comparable with the other periodically occuring values, the latter are
multiplied with the Present Value Factor (:math:`PVF`, see equation
:eq:`eq:PVF`). This yields the total cost necessary to produce one unit of heat
by the heat supply system (not accounting for any additional cost for e.g. the
pipe network, etc.).

.. math::
    LCOH = \frac{C_\text{invest} + PVF \cdot \left(C_\text{operation} - R\right)}{PVF \cdot Q_\text{total}}
    :label: eq:LCOH

.. math::
    PVF = \frac{\left(1 + i\right)^n - 1}{\left(1 + i\right)^n \cdot i}
    :label: eq:PVF

As we will evaluate the :math:`LCOH` again later, let's define a function to
calculate it from the input values using sensible default values as depicted
below.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/helpers.py
    :language: python
    :start-after: [func_lcoh_start]
    :end-before: [func_lcoh_end]

Now we'll begin computing the :math:`LCOH`. First of all, we need some cost
data of a typical gas boiler. We assume specific invest cost of 50,000.00 €/MW,
a nominal rated capacity of 20 MW and variable operation cost of 1.10 €/MWh.
The invest cost can be calculate by multiplying the specific cost and capacity.
For all cost related to the gas boiler's operation, we multiply the variable
cost with the total heat produced by the unit and add it to the sum of the
hourly cost evoked by the purchase of natural gas. Finllay, we sum up the heat
supplied to the heat sink and use the calculated values to compute the
:math:`LCOH`, which are printed to the console with a value of 18.84 €/MWh.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_9_start]
    :end-before: [sec_9_end]

This completes the first step of the District Heating Tutorial. Take a look at
the following lessons and think about what you should take away with you for
now.

.. admonition:: Learnings
    :class: important

    After the first step of this tutorial you should be able to do the
    following:

    * Read data from csv-files

    * Initialize an energy system

    * Create simple components

    * Optimize the dispatch of a district heating system

    * Visualize results and compute key parameters


Step 2: Plan capacity of heat pump and heat storage
---------------------------------------------------

In addition to the gas boiler, in the second step of the tutorial, we want to
consider adding a heat pump as well as a thermal energy storage to our district
heating system.

.. figure:: /_files/tutorial_dhs_2.svg
    :align: center
    :alt: Structure of the heating supplier's portfolio
    :figclass: only-light

    Structure of the heating supplier's portfolio

.. figure:: /_files/tutorial_dhs_2_darkmode.svg
    :align: center
    :alt: Structure of the heating supplier's portfolio
    :figclass: only-dark

    Structure of the heating supplier's portfolio

As we don't want to predefine their respective sizes, but rather build them
according to what makes the most sense economically, we will employ a combined
design and dispatch optimization. To make it a fair comparison, the gas
boiler's size will also be optimized, as opposed to our approach in the
previous step.

.. note::
    For clarity, we'll only show code that is new or changing, but each example
    step will contain a fully functional model.

First of all, we have to think about what new information we need for adding a
heat pump and storage. Besides technical specifications of the two units we
also have to know the price of electricity our heat pump will use to produce
heat. As we won't model any constraints for its heat source yet, the
electricity price data is the only new entry in our time series input data.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_2.py
    :language: python
    :start-after: [sec_1_start]
    :end-before: [sec_1_end]

As new energy carriers will be used in our energy system, we need to add
corresponding buses to it. So let's add an electricity and a waste heat bus.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_2.py
    :language: python
    :start-after: [sec_2_start]
    :end-before: [sec_2_end]

Using the buses above, we can now add two sources accordingly by connecting
their respective outputs to them via :py:class:`solph.flows.Flow` instances.
Secondly, we make sure to add the `'el_spot_price'` time series as variable
cost of the flow.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_2.py
    :language: python
    :start-after: [sec_3_start]
    :end-before: [sec_3_end]

Finally, let's add the waste heat heat pump to the energy system. Before
creating the :py:class:`solph.components.Converter` instance, we'll define some
specifications like the heat pump's :math:`COP` as well as specific invest and
variable operation costs, which we can use again later for the economic
evaluation. We then add to flows from the electricity and waste heat buses to
the inputs and the heat bus to the outputs dictionary. As we decided not to
predefine the heat pump's nominal capacity, we can't set it to a numerical
value, but rather pass an instance of the :py:class:`solph.Investment` class.
It can take upper and lower bounds as well as other arguments, but we only set
the so called 'equivalent periodical cost' to the :py:attr:`ep_cost` parameter.
Before diving deeper into those cost, let's finish the initialization of the
heat pump by defining the :py:attr:`conversion_factors` between the output and
the two inputs.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_2.py
    :language: python
    :start-after: [sec_4_start]
    :end-before: [sec_4_end]

To derive the correct relations between the respective inputs and the produced
heat flow, we have to take a look at the definition of the :math:`COP`.
Equation :eq:`eq:COP` describes it according to both the power and the heat
input. These terms can then be rearranged to calculate the ratios between all
flows, which are finally passed into the values of the
:py:attr:`conversion_factors` dictionary to the bus keys.

.. math::
    COP = \frac{\dot Q_{out}}{P_{in}} = \frac{\dot Q_{out}}{\dot Q_{out} - \dot Q_{in}}
    :label: eq:COP

As mentioned above, specific investment cost aren't directly passed to the
:py:attr:`ep_cost` argument, as they are typically allocated over the units
lifetime. Furthermore, capital cost in the form of interest have to be
considered. This is done by multiplying the specific investment cost
:math:`c_\text{invest}` by the annuity factor :math:`AF` (see equation
:eq:`eq:ep_cost`), which itself is the reciprocal of the :math:`PVF` introduced
earlier (see equation :eq:`eq:AF`).

.. math::
    c_\text{ep} = c_\text{invest} \cdot AF
    :label: eq:ep_cost

.. math::
    AF = \frac{\left(1 + i\right)^n \cdot 1}{\left(1 + i\right)^n - i}
    :label: eq:AF

The calculation of the specific equivalent periodical cost :math:`c_\text{ep}`
are again implemented via a python function, which will be organized together
with the :math:`LCOH` function in the ``helpers.py`` utility file.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/helpers.py
    :language: python
    :start-after: [func_epc_start]
    :end-before: [func_epc_end]

.. tip::
    It often makes sense to organize code in different logically coherent
    utility files. Just make sure to import the functions you want to use from
    now on like this: ``from helpers import LCOH, epc``

This concludes the addition of the heat pump and we can continue by adding the
thermal energy storage. Again, we are considering specific invest cost as well
as operational cost while charging and discharging the storage. Besides that,
the :py:class:`solph.components.GenericStorage` class takes some additional
arguments we will supply. Besides defining the in- and output with an empty
flow, we pass the constant relation between their nominal flows and the
storage's capacity to be optimized. The value of 1/24 is chosen so that the TES
can be fully charged from an empty content within one day. Furthermore, we set
the :py:attr:`balanced` parameter ``True`` in order to force the optimizer to
recharge the TES back to its inital storage content at the end of the period.
Last of all, we define a constant relative loss factor of 0.001 per timestep or
1/10 % per hour.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_2.py
    :language: python
    :start-after: [sec_5_start]
    :end-before: [sec_5_end]

Now we can finally run the model and extract the optimization results again. In
addition to the data in the previous step, we also pull out data for the
electricity bus as well as the optimized capacities of our heat production
units. The latter are also displayed in :numref:`tab-caps-1`.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_2.py
    :language: python
    :start-after: [sec_6_start]
    :end-before: [sec_6_end]

.. list-table:: Optimized heat production unit capacities
    :name: tab-caps-1
    :widths: 1 1 1 1
    :header-rows: 1

    * - 
      - gas boiler
      - heat pump
      - heat storage
    * - capacity
      - 10.2 MW
      - 6.0 MW
      - 98.6 MWh

The results show that the gas boilers capacities is halfed, yet it stays the
biggest heat production unit, with the heat pump being about 60% of the
boiler's size. Interestingly, the heat production units are not large enough to
supply the peak load on their own, but rather rely on the storage to support
them in the few hours of the year where it is necessary. The TES itself is
sized to store about 10 hours of full load production of the gas boiler. To
investigate how the units are actually dispatched, let's plot the hourly heat
production again. Furthermore, we can plot the heat storages hourly content to
help our understanding of the district heating system.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_2.py
    :language: python
    :start-after: [sec_8_start]
    :end-before: [sec_8_end]

Below you can see the two plots created from the code snippet above. We can see
that the heat pump is used to deliver the base load most of the time throughout
the year. During the heating period the gas boiler is dispatched together with
the heat pump to cover the middle load. As suspected from the optimized
capacities, the heat storage then joins the other two units to supply the peak
load. It is also employed to cover the summer demand when it falls below the
nominal capacity of the heat pump, which is used in tandem with the storage to
avoid part load operation.

.. figure:: /_files/intro_tut_dhs_2_hourly_heat_production.svg
    :align: center
    :alt: System dispatch of heating system with gas boiler, heat pump and storage
    :figclass: only-light

    System dispatch of heating system with gas boiler, heat pump and storage

.. figure:: /_files/intro_tut_dhs_2_hourly_heat_production_darkmode.svg
    :align: center
    :alt: System dispatch of heating system with gas boiler, heat pump and storage
    :figclass: only-dark

    System dispatch of heating system with gas boiler, heat pump and storage

The hourly storage content plot reinforces our assumptions about its usage
within the district heating system. It is filled for peak load early in the
year, then empty for a while until the summer demand makes it desirable again.
This holds true for almost the rest of the year until it phases out again, with
the exception of a peak load case in december.

.. figure:: /_files/intro_tut_dhs_2_hourly_storage_content.svg
    :align: center
    :alt: Storage content over the operating period
    :figclass: only-light

    Storage content over the operating period

.. figure:: /_files/intro_tut_dhs_2_hourly_storage_content_darkmode.svg
    :align: center
    :alt: Storage content over the operating period
    :figclass: only-dark

    Storage content over the operating period

Let's conclude our result analysis by recalculating the :math:`LCOH` of the
newly designed system. The computation works analogous to the one before, but
with additional investment and operational cost of the new heat production
units. Make sure to correctly import the ``LCOH`` function, if you moved it to
the ``helpers.py`` file like we did.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_2.py
    :language: python
    :start-after: [sec_7_start]
    :end-before: [sec_7_end]

The calculation yields a :math:`LCOH` of 18.61 €/MWh, which is slightly cheaper
then the one we got from only using the gas boiler in the step before. We
ommited any ecological analysis or emission calculation to keep the tutorial
concise, but it is self-evident that reducing gas boiler heat covarage in
favor of Power-to-Heat technologies has environmental benefits as well.

.. admonition:: Learnings
    :class: important

    After the second step of this tutorial you should be able to do the following:

    * Expand the district heating system

    * Create first complex components

    * Use functions for recurring tasks

    * Optimize the design and dispatch of district heating system

Step 3: Introduce constraints to the heat production units
----------------------------------------------------------

To round off this tutorial, let's add some more realistic constraints to our
heat pump. We will begin by enforcing a relative minimum part load and finish
by constraining the waste heat source.

To implement the minimum part load constraint we have to change the definition
of our heat pump converter. The :py:attr:`min` keyword takes a relative
minimum part load that is multiplied with the nominal capacity or invest
variable to form a lower bound of the flow. Passing ``0.5`` results in a
minimum heat production of 50% its nominal value. If we only set this argument,
the heat pump would always have to produce at least this amount of heat. As we
also want to allow it to be switched off, we have to use a mixed integer linear
formulation, instead of the purely linear one we used until now. That is
achieved by setting the :py:attr:`nonconvex` argument to an instance of the
:py:class:`solph.NonConvex` class. This powerful object also allows for setting
minimum and maximum up- or downtimes and startups as well as gradient limits.
A side effect of setting the :py:attr:`nonconvex` parameter is, that we also
have to pass an upper limit to the :py:class:`solph.Investment` instance via
the :py:attr:`maximum` parameter. To not interfere with the free optimization
of the nominal capacity, we can set it to an amount that is arbitrarily larger
than the peak load, so we decide on 999 MW.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_3.py
    :language: python
    :start-after: [sec_1_start]
    :end-before: [sec_1_end]

.. tip::

    What if minimum demand cannot be supplied?

    * Add a slack source for the heat demand

    * Add a thermal energy store or change parameters of the existing storage

    * Add a new heat production unit

As these changes introduce mixed integer linear formulations, the CBC solver is
taking longer to solve the optimization problem and may not reach optimality in
a feasable time frame. We can reach a solution that is good enough for our
standards by introducing the concept of an optimality tolerance or MIP Gap. It
describes a relative tolerance to a known optimal objective value from a
solution, that is small enough to tolerate to us. For example, we can decide
that a solution that is within 1% of the optimum is precise enough for us that
we don't need the solver to potentially run for hours longer to reach it. Each
solver has its own parameter to control this behavior. Using CBC, we can set
the ``'ratio'`` key of the :py:attr:`cmdline_options` parameter to the desired
tolerance. As this will likely lead to an early termination short of optimality
(as is also intended), we have to set the :py:attr:`allow_nonoptimal` flag to
``True`` in order to avoid raising an exception.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_3.py
    :language: python
    :start-after: [sec_2_start]
    :end-before: [sec_2_end]

We extract the optimized unit capacities just as we did before.
:numref:`tab-caps-2` contains those results, which are not too far off from the
previous solution without the minimum part load constraint. This shouldn't be
too confusing, as the heat pump hasn't been operated in part load very often
before.

.. list-table:: Optimized heat production unit capacities
    :name: tab-caps-2
    :widths: 1 1 1 1
    :header-rows: 1

    * - 
      - gas boiler
      - heat pump
      - heat storage
    * - capacity
      - 10.6 MW
      - 5.7 MW
      - 91.1 MWh

.. note::
    Especially when introducing an optimality tolerance, but also in the case
    of flat optima, different solutions to the same optimization problem can
    result in similar objective values. Keep that in mind when comparing your
    results with ours and in future analyses.

To check for any significant changes of the hourly unit dispatch, let's create
the plots from before again. They don't need any adaptation, so we don't show
the code again.

.. figure:: /_files/intro_tut_dhs_3_hourly_heat_production.svg
    :align: center
    :alt: System dispatch of heating system with minimum part load of heat pump
    :figclass: only-light

    System dispatch of heating system with minimum part load of heat pump

.. figure:: /_files/intro_tut_dhs_3_hourly_heat_production_darkmode.svg
    :align: center
    :alt: System dispatch of heating system with minimum part load of heat pump
    :figclass: only-dark

    System dispatch of heating system with minimum part load of heat pump

We can visually confirm the enforcement of minimum part load by observing the
valleys of the heat pump heat production. While those reach deeper in the
previous plot, this time we can see them being half the height of full load
operation, which is exactly what we imposed. As to be expected from the
similar size of capacities, we don't see any major differences in the unit
dispatch.

For the sake of completeness, we'll have a look at the storage content as well.
It shows even fewer obvious dissimilarities to the previous plot.

.. figure:: /_files/intro_tut_dhs_3_hourly_storage_content.svg
    :align: center
    :alt: Storage content over the operating period with minimum part load of heat pump
    :figclass: only-light

    Storage content over the operating period with minimum part load of heat pump

.. figure:: /_files/intro_tut_dhs_3_hourly_storage_content_darkmode.svg
    :align: center
    :alt: Storage content over the operating period with minimum part load of heat pump
    :figclass: only-dark

    Storage content over the operating period with minimum part load of heat pump

As the :math:`LCOH` comes out only a few cents higher than before, we also
don't spend too much time on economical analysis. Rather, let's have a look at
the last constraint we want to add to our district heating system model. Up
until now, we didn't impose any restriction on the amount of wast heat we could
obtain from the source. In reality, often this isn't the case at all. If the
heat comes from an industrial process, it likely runs as much as possible and
oftentimes produces a constant rate of excess heat. Depending on agreements or
contracts between the waste heat supplier and the district heating system
operator, using the waste heat at any time could be obligated.

For our last example, let's say this is the case. We decide that a constant
2.5 MW of excess heat is produced at all times throughout the year.
Furthermore, we agree to use it in our district heating system every time as
well. We can model this behavior by adding the :py:attr:`fix` parameter to the
definition of the waste heat source and passing the amount to it.
:py:attr:`fix` can also take a time series of values and is multiplied with the
:py:attr:`nominal_value` elementwise to compute the amount supplied to the
energy system in all time intervals. In this example, we'll do without
considering any cost for the usage of waste heat, but feel free play around
with that on your own.

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_4.py
    :language: python
    :start-after: [sec_1_start]
    :end-before: [sec_1_end]

As this is the only change we'll perform, we can have a look at the results
again. :numref:`tab-caps-3` shows the capacities, with the gas boiler coming
out slightly larger again. The heat pump is excatly 3.5 MW, which you can
ponder for a moment to why this occured. In contrast to the previous examples,
the heat storage is much larger and can work as more than just a daily buffer.

.. list-table:: Optimized heat production unit capacities
    :name: tab-caps-3
    :widths: 1 1 1 1
    :header-rows: 1

    * - 
      - gas boiler
      - heat pump
      - heat storage
    * - capacity
      - 10.9 MW
      - 3.5 MW
      - 542.8 MWh

To possibly confirm a suspicion of yours about how the size of the heat pump
came about, let's have a look at the unit commitment in the figure below. We
can see that the heat pump is always running at full capacity. This results
from the new constraint we subjected the waste heat source to. The biggest
other difference is the extended usage of the heat storage, which has to pick
up excess heat production of the heat pump during the low summer load. This is
also seen in the storage content plot below the unit commitment figure.
Beyond that, we see peaks of usage during the heating period.

.. figure:: /_files/intro_tut_dhs_4_hourly_heat_production.svg
    :align: center
    :alt: System dispatch of heating system with fixed waste heat source
    :figclass: only-light

    System dispatch of heating system with fixed waste heat source

.. figure:: /_files/intro_tut_dhs_4_hourly_heat_production_darkmode.svg
    :align: center
    :alt: System dispatch of heating system with fixed waste heat source
    :figclass: only-dark

    System dispatch of heating system with fixed waste heat source

.. figure:: /_files/intro_tut_dhs_4_hourly_storage_content.svg
    :align: center
    :alt: Storage content over the operating period with fixed waste heat source
    :figclass: only-light

    Storage content over the operating period with fixed waste heat source

.. figure:: /_files/intro_tut_dhs_4_hourly_storage_content_darkmode.svg
    :align: center
    :alt: Storage content over the operating period with fixed waste heat source
    :figclass: only-dark

    Storage content over the operating period with fixed waste heat source

.. admonition:: Learnings
    :class: important

    After the third step of this tutorial you should be able to do the following:

    * Add or change key word arguments to add constraints to heat production units

    * Understand the functionality of minimum load constraints as well as the impact of fixed and variable sources

    * Understand the implications of adding mixed integer linear constraints compared to purely linear problems

    * Deal with theoretically unsolvable optimization problems
