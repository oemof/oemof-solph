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
thermal energy storage. This time only specific invest cost are considered, as
operational cost of heat storage are often negligible. Then again, the
:py:class:`solph.components.GenericStorage` class takes some additional
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
units. The latter are also displayed in :numref:`tab-caps`.

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
them in the few hours of the year when necessary.

.. figure:: /_files/intro_tut_dhs_2_hourly_heat_production.svg
    :align: center
    :alt: System dispatch of heating system with gas boiler
    :figclass: only-light

    System dispatch of heating system with gas boiler

.. figure:: /_files/intro_tut_dhs_2_hourly_heat_production_darkmode.svg
    :align: center
    :alt: System dispatch of heating system with gas boiler
    :figclass: only-dark

    System dispatch of heating system with gas boiler

.. figure:: /_files/intro_tut_dhs_2_hourly_storage_content.svg
    :align: center
    :alt: System dispatch of heating system with gas boiler
    :figclass: only-light

    Storage content over an operating period

.. figure:: /_files/intro_tut_dhs_2_hourly_storage_content_darkmode.svg
    :align: center
    :alt: System dispatch of heating system with gas boiler
    :figclass: only-dark

    Storage content over an operating period

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_2.py
    :language: python
    :start-after: [sec_7_start]
    :end-before: [sec_7_end]

:math:`LCOH`: 18.61 €/MWh

.. admonition:: Learnings
    :class: important

    After the second step of this tutorial you should be able to do the following:

    * Expand the district heating system

    * Create first complex components

    * Use functions for recurring tasks

    * Optimize the design and dispatch of district heating system

Step 3: Introduce constraints to the heat production units
----------------------------------------------------------

1. Introduce a minimal load constraint for the heat pump

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_3.py
    :language: python
    :start-after: [sec_1_start]
    :end-before: [sec_1_end]

.. tip::

    What if minimum demand cannot be supplied?

    * Add a slack source for the heat demand

    * Add a thermal energy store or change parameters of the existing storage

    * Add a new heat production unit

2. Run optimization, get results, what is the difference to before?

.. list-table:: Optimized heat production unit capacities
    :name: tab-caps-2
    :widths: 1 1 1 1
    :header-rows: 1

    * - 
      - gas boiler
      - heat pump
      - heat storage
    * - capacity
      - 12.5 MW
      - 3.9 MW
      - 86.3 MWh

.. figure:: /_files/intro_tut_dhs_3_hourly_heat_production.svg
    :align: center
    :alt: System dispatch of heating system with gas boiler
    :figclass: only-light

    System dispatch of heating system with gas boiler

.. figure:: /_files/intro_tut_dhs_3_hourly_heat_production_darkmode.svg
    :align: center
    :alt: System dispatch of heating system with gas boiler
    :figclass: only-dark

    System dispatch of heating system with gas boiler

.. figure:: /_files/intro_tut_dhs_3_hourly_storage_content.svg
    :align: center
    :alt: System dispatch of heating system with gas boiler
    :figclass: only-light

    Storage content over an operating period

.. figure:: /_files/intro_tut_dhs_3_hourly_storage_content_darkmode.svg
    :align: center
    :alt: System dispatch of heating system with gas boiler
    :figclass: only-dark

    Storage content over an operating period

3. Expand the waste heat source with a constraint on fixed consumption

.. literalinclude:: /../tutorials/introductory/district_heating_supply/district_heating_supply_4.py
    :language: python
    :start-after: [sec_1_start]
    :end-before: [sec_1_end]

4. Again: Run optimization, get results, what is the difference to before?

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

.. figure:: /_files/intro_tut_dhs_4_hourly_heat_production.svg
    :align: center
    :alt: System dispatch of heating system with gas boiler
    :figclass: only-light

    System dispatch of heating system with gas boiler

.. figure:: /_files/intro_tut_dhs_4_hourly_heat_production_darkmode.svg
    :align: center
    :alt: System dispatch of heating system with gas boiler
    :figclass: only-dark

    System dispatch of heating system with gas boiler

.. figure:: /_files/intro_tut_dhs_4_hourly_storage_content.svg
    :align: center
    :alt: System dispatch of heating system with gas boiler
    :figclass: only-light

    Storage content over an operating period

.. figure:: /_files/intro_tut_dhs_4_hourly_storage_content_darkmode.svg
    :align: center
    :alt: System dispatch of heating system with gas boiler
    :figclass: only-dark

    Storage content over an operating period

.. admonition:: Learnings
    :class: important

    After the third step of this tutorial you should be able to do the following:

    * Add or change key word arguments to customize heat production units

    * Deal with theoretically unsolvable optimization problems

    * Understand the functionality of minimum load constraints as well as the impact of fixed and variable sources

    * Analyse results of design and dispatch
