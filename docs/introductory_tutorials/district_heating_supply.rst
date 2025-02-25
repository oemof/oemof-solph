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

2. Import dependencies + setup EnergySystem (code snippet)

.. literalinclude:: /../tutorial/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_2_start]
    :end-before: [sec_2_end]

3. Description of which buses are required + setup? (code snippet)

.. literalinclude:: /../tutorial/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_3_start]
    :end-before: [sec_3_end]

4. Description which sinks and sources are required, load the necessary data, setup (code snippet)

.. literalinclude:: /../tutorial/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_4_start]
    :end-before: [sec_4_end]

5. Converter setup (gas boiler), how to connect buses, variable costs, capacity (code snippet)

.. literalinclude:: /../tutorial/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [sec_5_start]
    :end-before: [sec_5_end]

6. "Optimization" of dispatch, has to follow load (code snippet)

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
