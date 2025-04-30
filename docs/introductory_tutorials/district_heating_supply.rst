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
functional python file of all three main steps for you to execute yourself or
modify and play around with.

.. figure:: /_files/example_network.svg
    :align: center
    :alt: Structure of the heating supplier's portfolio
    :figclass: only-light

    Structure of the heating supplier's portfolio

.. figure:: /_files/example_network_darkmode.svg
    :align: center
    :alt: Structure of the heating supplier's portfolio
    :figclass: only-dark

    Structure of the heating supplier's portfolio

Step 1: Status-Quo system
-------------------------

As described above, we want to start by building the existing district heating
supply systems, which in our simple example only contains a single gas boiler.
But before we start modeling the energy system, we should give some thought about
what kind of input data we need for the simulation.

Maybe the first that comes to mind is the heat demand our system should supply.
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

.. literalinclude:: /../tutorial/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_1_start]
    :end-before: [sec_1_end]

Now we can begin the modeling process of our district heating supply system. Every
oemof.solph model starts be creating (also called "initializing") the ``EnergySystem``.
To create an instance of the :py:class:`solph.EnergySystem` class, we have to import the solph
package at first. To enforce our simulation time period and resolution, we set its
:py:attr:`timeindex` keyword argument to the index of the input DataFrame.

.. literalinclude:: /../tutorial/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_2_start]
    :end-before: [sec_2_end]

After that, we need to set up the two energy carrying buses, i.e. the heat and gas
network. We make sure to set a label for the two to reference them later when we
analyze the results. After initialization, we add them to the ``district_heating_system``
object.

.. literalinclude:: /../tutorial/introductory/district_heating_supply/district_heating_supply_1.py
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

.. literalinclude:: /../tutorial/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_4_start]
    :end-before: [sec_4_end]

Last, but not least, we will depict the gas boiler itself, using a simple linear
model with the :py:class:`solph.components.Converter` class. In contrast to the
components before, we have to define at least one input *and* one output, which in
case of the gas boiler is the natural gas burnt and the heat produced from it.
The connection from the gas network does not need any parametrization. We set the
:py:attr:`nominal_value` of the heat output to 20 MW (see note on units below) and
add :py:attr:`variable_cost` of 0.50 €/MWh. To depict energy losses due to thermodynamic
inefficiencies, we can set the :py:attr:`conversion_factors` keyword argument of
the :py:class:`solph.components.Converter`. It expects a dictionary, with a key
corresponding to the bus to which the value (scalar or iterable) is applied. So,
to model a constant efficiency of 95 %, we set it to 0.95. Do not forget to add
the gas boiler to the district heating supply system.

.. literalinclude:: /../tutorial/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_5_start]
    :end-before: [sec_5_end]

.. note::
    Keep in mind that the units used in your energy system model are only implicit
    and that you have to check their consistency yourself.

As our system is complete for this step, its time to start the unit commitment
optimization. For that, we first have to create a :py:class:`solph.Model` instance
from our ``district_heating_system``. Then we can use its :py:func:`solve` method
to run the optimization. We decide to use the open source solver CBC and add the
additional :py:attr:`solve_kwargs` parameter ``'tee'`` to ``True``, in order to
get a more verbose solver logging output in the console.

.. literalinclude:: /../tutorial/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_6_start]
    :end-before: [sec_6_end]

7. Some results, LCOH, CO2 emissions (how to calculate and resulting numbers),
   dispatch plot(s). Include the plots in the page here!!

.. literalinclude:: /../tutorial/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_7_start]
    :end-before: [sec_7_end]

.. literalinclude:: /../tutorial/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_8_start]
    :end-before: [sec_8_end]

.. literalinclude:: /../tutorial/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_9_start]
    :end-before: [sec_9_end]

.. literalinclude:: /../tutorial/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_10_start]
    :end-before: [sec_10_end]

.. figure:: /_files/example_network.svg
    :align: center
    :alt: System dispatch of heating system with gas boiler
    :figclass: only-light

    System dispatch

.. figure:: /_files/example_network_darkmode.svg
    :align: center
    :alt: System dispatch of heating system with gas boiler
    :figclass: only-dark

    System dispatch

Step 2: Plan capacity of heat pump and heat storage
---------------------------------------------------

.. dropdown:: See the complete code

    .. literalinclude:: /../tutorial/introductory/district_heating_supply/district_heating_supply_2.py
        :language: python
        :start-after: [sec_6_start]
        :end-before: [sec_6_end]

1. What information is required on the new components? (data, no code, include waste heat time series)

2. Add new buses (electricity, waste heat)

3. Add waste heat source and electricity source

4. Add heat storage

5. Add heat pump

6. Run model and analyze results

Step 3: Introduce a minimal load for the converters
---------------------------------------------------

1. Modify the converters, remaining parts are identical.

.. tip::

    What if minimum demand cannot be supplied? Add a slack source for the heat
    demand.

2. Run optimization, get results, what is the difference to before?
