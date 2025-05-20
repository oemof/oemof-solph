.. _ev_charging_label:

Load management of a single EV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this tutorial we will optimize the loading of an EV.

The tutorial is set up in 5 different steps

- Step 1: Plugged EV as load
- Step 2: Unidircetional charging
- Step 3: Free charging with PV system at work
- Step 4: Fix free charging artefact and allow bidirectional use of the battery
- Step 5: Variable electricity prices

Each section contains a step by step explanation of how the a management of an ev loading can be done is using oemof.solph. Additionally, the repository contains a fully
functional python file of all five main steps for you to execute yourself or
modify and play around with.

Step 1: Plugged EV as load
---------------------------

Within the first step we want to simulate a plugged EV as load with pre-calculated charging time series Charged EV with predefined trips for load.
First of all, we create some input data. We use Pandas to do so and will also
import matplotlib to plot the data.
Further for plotting we use a helper function from
:download:`helpers.py </../tutorials/introductory/ev_charging/helpers.py>`.

.. literalinclude:: /../tutorials/introductory/ev_charging/ev_charging_1.py
    :language: python
    :start-after: [imports_start]
    :end-before: [imports_end]


Now we can begin the modeling process of ev loading management. Every oemof.solph model starts be creating (also called "initializing") the energy system.
To create an instance of the :py:class:`solph.EnergySystem` class, we have to import the solph
package at first. Further we need a timeindex for the simulation.Within this example we will regard the first day of the year of 2025.
We will use the :py:func:`date_range` function from the :py:mod:`pandas` package to create a timeindex with 5 minute resolution for one day.


.. literalinclude:: /../tutorials/introductory/ev_charging/ev_charging_1.py
    :language: python
    :start-after: [create_time_index_set_up_energysystem_start]
    :end-before: [create_time_index_set_up_energysystem_end]


After that, we need to define the trip demand series for the real trip scenario. As the demand is a power time series, it has N-1 entries
when compared to the N entires of time axis for the energy.
There is a morning drive from 07:10  a.m. to 08:10 a.m.. The power of 10 kW is required.
Further there is an evening drive from 4:13 p.m. to 5:45 p.m.. The power of 9 kW is required.

.. literalinclude:: /../tutorials/introductory/ev_charging/ev_charging_1.py
    :language: python
    :start-after: [trip_data_start]
    :end-before: [trip_data_end]

.. note::
    Keep in mind that the units used in your energy system model are only implicit
    and that you have to check their consistency yourself.


Lets look at the driving pattern

.. literalinclude:: /../tutorials/introductory/ev_charging/ev_charging_1.py
    :language: python
    :start-after: [plot_trip_data_start]
    :end-before: [plot_trip_data_end]

.. figure:: /./_files/tutorial_ev-charging/driving_pattern.svg
    :align: center
    :alt: Driving pattern
    :figclass: only-light

.. figure:: /./_files/tutorial_ev-charging/driving_pattern_dark_mode.svg
    :align: center
    :alt: Driving pattern
    :figclass: only-dark

    Driving pattern


Now we need to set up the electric energy carrying bus. We make sure to set a label to reference them later when we
analyze the results. After initialization, we add them to the ``ev_energy_system`` object.

.. literalinclude:: /../tutorials/introductory/ev_charging/ev_charging_1.py
    :language: python
    :start-after: [energysystem_and_bus_start]
    :end-before: [energysystem_and_bus_end]

After setting up the energy system and the buses, we can now add the components to the energy system.
We adding the driving demand as :py:class:`solph.components.Sink`, where the loading profile is added as
:py:attr:`fix` and :py:attr:`nominal_capacity` is set to one, because the loading profile is absolute.
As we have a demand time series which is actually in kW, we use a common
"hack" here: We set the nominal capacity to 1 (kW), so that
multiplication by the time series will just yield the correct result.

The driving demand input is connected with the the electric energy carrying bus.


The car battery is added as :py:class:`solph.components.GenericStorage`.
The following parameters are set:

- :py:attr:`nominal_capacity` is set to 50 (kWh), which is the capacity of the battery.
- :py:attr:`capacity_loss` is set to 0.001. This means the battery loss per hour is 0.1% percent.
- :py:attr:`initial_capacity` is set to 1. This indicates that the battery is full at the beginning of the simulation.
- :py:attr:`inflow_conversion_factor` is set to 0.9, so the charging efficency is 90%.
- :py:attr:`balanced` is set to False. This means the battery storage level at the end has not to be the same as at the beginning.
- :py:attr:`storage_costs` is set to the defined storage revenue. Where "storage revenue" is defined as list with negative costs (of 60 ct/kWh) for the last time step, so that energy inside the storage in the last time step is worth something.

This leads to the fact that the battery is not necessary emptied at the end of the simulation.

The car battery inputs and outputs are connected with the the electric energy carrying bus.

.. literalinclude:: /../tutorials/introductory/ev_charging/ev_charging_1.py
    :language: python
    :start-after: [car_start]
    :end-before: [car_end]


As our system is complete for this step. Before we start the unit commitment
optimization, let us have a look at the energy system graph

.. literalinclude:: /../tutorials/introductory/ev_charging/ev_charging_1.py
    :language: python
    :start-after: [graph_start]
    :end-before: [graph_end]

While `nx.draw` is handy to just have a quick look without too many extra
tools, writing the graph `dot` allows for handling in specialised programs.
The folloing has been created using

.. figure:: /./_files/tutorial_ev-charging/ev_charging_graph_1.svg
    :align: center
    :alt: Energy system graph in step 1

For the actual optimisation, we first have to create a :py:class:`solph.Model`
instance from our ``ev_energy_system``. Then we can use its :py:func:`solve`
method to run the optimization.
We decide to use the open source solver CBC and add the additional
:py:attr:`solve_kwargs` parameter ``'tee'`` to ``True``, in order to
get a more verbose solver logging output in the console.


.. literalinclude:: /../tutorials/introductory/ev_charging/ev_charging_1.py
    :language: python
    :start-after: [solve_start]
    :end-before: [solve_end]


.. note::
    Optimisation will fail if supply and demand cannot be balanced.
    You can try this by setting `initial_storage_level=0`.

Now plot the results using the helper function from helpers.py.

The results are showing that the EV is using the battery while driving.

.. literalinclude:: /../tutorials/introductory/ev_charging/ev_charging_1.py
    :language: python
    :start-after: [plot_results_start]
    :end-before: [plot_results_end]

.. figure:: /./_files/tutorial_ev-charging/driving_demand_only.svg
    :align: center
    :alt: Driving pattern
    :figclass: only-light

.. figure:: /./_files/tutorial_ev-charging/driving_demand_only_dark_mode.svg
    :align: center
    :alt: Driving pattern
    :figclass: only-dark

    Driving pattern


.. admonition:: Learning
    :class: important

    The model balances supply and demand along flows in a graph based model.
    The operation is optimised so that the total costs are minimised.

You can get the complete (uncommented) code for this step:
:download:`ev_charging_1.py </../tutorials/introductory/ev_charging/ev_charging_1.py>`

.. dropdown:: Click to display the code

    .. literalinclude:: /../tutorials/introductory/ev_charging/ev_charging_1.py
        :language: python

Step 2: Plugged EV as load
----------------------------


Now, let's assume the car battery can be charged at home.
To be able to load the battery a charger is necessary.  Unfortunately, there
is only a power socket available, limiting the charging process to 16 A at
230 V. The costs for charging are 30 ct/kWh.

.. note::
    Costs in the model are understood as a mathematical term,
    i.e. you could minimise emissions by choosing 363 g/kWh
    (German average for 2024) instead of the monetary costs.

So the charging is added as :py:class:`solph.components.Sink`,
where the :py:attr:`nominal_capacity` is set to 3.68 kW (= 230 V * 16 A) and :py:attr:`variable_costs` are set to 0.3 (30 ct/kWh).
This, of course, can only happen while the car is present at home.
To connect the car while it is at home, we create avalibility data series.
The value 1 means that the car is at home, chargable.
When it is set to 0, car is not present
(between morning departure and the arrival back home in the evening).
The timeseries is set as :py:attr:`max`.

.. literalinclude:: /../tutorials/introductory/ev_charging/ev_charging_2.py
    :language: python
    :start-after: [AC_30ct_charging_start]
    :end-before: [AC_30ct_charging_end]


Now we are looking at the results:
The EV will be charged as much as possible.
As it's not possible to load it completely in the afternoon,
it is charged to 100 % just before the first leaving.


.. figure:: /./_files/tutorial_ev-charging/driving_domestic_power_socket.svg
    :align: center
    :alt: Driving pattern
    :figclass: only-light

.. figure:: /./_files/tutorial_ev-charging/driving_domestic_power_socket_dark_mode.svg
    :align: center
    :alt: Driving pattern
    :figclass: only-dark

.. admonition:: Learning
    :class: important

    Optimisation is carried out under perfect foresight,
    meaning that things that happen later can imply things
    earlier in the time horison.


You can get the complete (uncommented) code for this step:
:download:`ev_charging_2.py </../tutorials/introductory/ev_charging/ev_charging_2.py>`

.. dropdown:: Click to display the code

    .. literalinclude:: /../tutorials/introductory/ev_charging/ev_charging_2.py
        :language: python

Step 3: Free charging with PV system at work
---------------------------------------------

Within this step we are regarding a free charging option at work.
So we add an 11 kW charger (free of charge) which is available at work.
This, of course, can only happen while the car is present at work.
Same with avalibility data at home charging, we will create a data set for
avalibility at work. When it is set to 0, car is not present at the work.
When it is set to 1, car is able to connect to work charge station
(between morning arrival and the evening departure from work).

.. literalinclude:: /../tutorials/introductory/ev_charging/ev_charging_3.py
    :language: python
    :start-after: [DC_charging_start]
    :end-before: [DC_charging_end]



Looking at the results we see the battery is charging and discharing at the same time within the beginning.
Charging and discharging at the same time is almost always a sign that
something is not moddeled accurately in the energy system.
A possible solution will be introducted within the next step.

Further we can see, the battery is charged when the car is at work, because the charging is free.

.. figure:: /./_files/tutorial_ev-charging/driving_home_and_work_charging.svg
    :align: center
    :alt: Driving pattern
    :figclass: only-light

.. figure:: /./_files/tutorial_ev-charging/driving_home_and_work_charging_dark_mode.svg
    :align: center
    :alt: Driving pattern
    :figclass: only-dark


.. admonition:: Learning
    :class: important

    Among multiple optimal solutions, any one can be your results.
    If something is free in the model, this can include unintuitive things.

You can get the complete (uncommented) code for this step:
:download:`ev_charging_3.py </../tutorials/introductory/ev_charging/ev_charging_3.py>`

.. dropdown:: Click to display the code

    .. literalinclude:: /../tutorials/introductory/ev_charging/ev_charging_3.py
        :language: python


Step 4:  Fix free charging artefact and allow bidirectional use of the battery
-------------------------------------------------------------------------------

To avoid the energy from looping in the battery, we introduce costs
to battery charging. This is a way to model cyclic aging of the battery.
This is done by adding some :py:attr:`variable_costs` on flow of to the input.

Further in this step we want to allow the bidirectional use of the battery.
So we are setting the :py:attr:`balanced` to  the default True.
This means the battery storage level at the end has to be the same as at the beginning.
We also have to remove the :py:attr:`initial_capacity`, so SOC(T=0) = SOC(T=T_max) is valid.
To ensure to have a reserve of 10 % within the battery, the :py:attr:`min_storage_level` is set to 0.1.

.. literalinclude:: /../tutorials/introductory/ev_charging/ev_charging_4.py
    :language: python
    :start-after: [car_battery_start]
    :end-before: [car_battery_end]


To be able to discharge the battery we need a discharger, which will be added as :py:class:`solph.components.Sink`.
The :py:attr:`nominal_capacity` is set to 3.68 kW (= 230 V * 16 A) and
:py:attr:`variable_costs` are set to -0.3 to save 30 ct/kWh.
The battery can only be discharged is the car is at home,
so the created timeseries from above is used and set to :py:attr:`max`.


.. literalinclude:: /../tutorials/introductory/ev_charging/ev_charging_4.py
    :language: python
    :start-after: [AC_discharging_start]
    :end-before: [AC_discharging_end]

The final energy system graph now looks like this:

.. figure:: /./_files/tutorial_ev-charging/ev_charging_graph_4.svg
    :align: center
    :alt: Energy system graph in step 4

Looking at the results:

- The charging and discharing within the beginning does not accure anymore
- The battery will be loaded for free within the working period
- There is a discharging at home at the evening to save money

.. figure:: /./_files/tutorial_ev-charging/driving_bidirectional_constant_costs.svg
    :align: center
    :alt: Driving pattern
    :figclass: only-light

.. figure:: /./_files/tutorial_ev-charging/driving_bidirectional_constant_costs_dark_mode.svg
    :align: center
    :alt: Driving pattern
    :figclass: only-dark


.. admonition:: Learning
    :class: important

    Looped energy flows can be used as an indicator for a flawed model.
    If possible, it should be fixed (instead of suppressed).

You can get the complete (uncommented) code for this step:
:download:`ev_charging_4.py </../tutorials/introductory/ev_charging/ev_charging_4.py>`

.. dropdown:: Click to display the code

    .. literalinclude:: /../tutorials/introductory/ev_charging/ev_charging_4.py
        :language: python


Step 5: Variable electricity prices
------------------------------------

Within the last step we want to regard dynamic prices for the the charging and discharging at home.
So the optimization is going to load when the prices are are load and discharge if the prices are high.
Assuming the following prices:

- Before 6 a.m.: 5 ct/kWh
- After 4 p.m. 70 ct/kWh
- Otherwise: 50 ct/kWh

.. literalinclude:: /../tutorials/introductory/ev_charging/ev_charging_5.py
    :language: python
    :start-after: [AC_dynamic_price_start]
    :end-before: [AC_dynamic_price_end]


Lets have a look on the dynamic prices

.. figure:: /./_files/tutorial_ev-charging/dynamic_price.svg
    :align: center
    :alt: Driving pattern
    :figclass: only-light

.. figure:: /./_files/tutorial_ev-charging/dynamic_price_dark_mode.svg
    :align: center
    :alt: Driving pattern
    :figclass: only-dark



The prices have to be set within the charger and discharger instead of the 30 ct/kWh before,
we set the :py:attr:`variable_costs` to the dynamic price or rather to the negative dynamic price.

.. literalinclude:: /../tutorials/introductory/ev_charging/ev_charging_5.py
    :language: python
    :start-after: [Charging_discharging_with_dynamic_prices_start]
    :end-before: [Charging_discharging_with_dynamic_prices_end]


Looking at the results the battery is loaded before 6 a.m. with the cheap price of 5 ct/kWh right before the first leaving
to get 50 ct/kWh. The battery is recharged for free at the work and in the evening discharged to get 70 ct/kWh.

.. figure:: /./_files/tutorial_ev-charging/drivining_bidirectional_dynamic_costs.svg
    :align: center
    :alt: Driving pattern
    :figclass: only-light

.. figure:: /./_files/tutorial_ev-charging/drivining_bidirectional_dynamic_costs_dark_mode.svg
    :align: center
    :alt: Driving pattern
    :figclass: only-dark

.. admonition:: Learning
    :class: important

    Costs can be time-dependent. The optimal operation can be changed this way
    if the model includes a storage.


You can get the complete (uncommented) code for this step:
:download:`ev_charging_5.py </../tutorials/introductory/ev_charging/ev_charging_5.py>`

.. dropdown:: Click to display the code

    .. literalinclude:: /../tutorials/introductory/ev_charging/ev_charging_5.py
        :language: python
