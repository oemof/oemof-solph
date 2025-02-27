.. _ev_charging_label:

Load management of a single EV 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this tutorial we will optimize the loading of an EV.

The tutorial is set up in 5 different steps

1: Plugged EV as load 
2: Unidirektional charging (learning: incentive to re-charge)
3: Free charging with PV system at work (learning: dispatch with shifting under simple constraint)
4: Fix free charging artefact and allow bidirectional use of the battery (learning: looped energy flow as indicator for flawed model and understand the "balanced" keyword)
5: Variable electricity prices (learning: how to include time series for costs)

Each section contains a step by step explanation of how the a management of an ev loading can be done is using oemof.solph. Additionally, the repository contains a fully
functional python file of all five main steps for you to execute yourself or
modify and play around with.

Step 1: Plugged EV as load
-------------------------

Plugged EV as load with pre-calculated charging time series Charged EV with predefined trips for load (learning: trivial dispatch, but from battery)

.. TODO :: Add explanation

First of all, we create some input data. We use Pandas to do so and will also
import matplotlib to plot the data.
Further for plotting we use a helper function from helpers.py (within this folder)

.. literalinclude:: /../tutorial/introductory/ev_charging/ev_charging_1.py
    :language: python
    :start-after: [imports_start]
    :end-before: [imports_end]


Now we can begin the modeling process of ev loading management. Every
oemof.solph model starts be creating (also called "initializing") the ``EnergySystem``.
To create an instance of the :py:class:`solph.EnergySystem` class, we have to import the solph
package at first. Further we need a timeindex for the simulation.Within this example we will regard the first day of the year of 2025.
We will use the ``date_range`` function from the ``pandas``package to create a timeindex with 5 minute resolution for one day.


.. literalinclude:: /../tutorial/introductory/ev_charging/ev_charging_1.py
    :language: python
    :start-after: [create_time_index_set_up_energysystem_start]
    :end-before: [create_time_index_set_up_energysystem_end]


After that, we need to define the trip demand series for the real trip scenario. As the demand is a power time series, it has N-1 entries
when compared to the N entires of time axis for the energy.
There is a morning drive from 07:10 to 08:10. The power of 10 kW is required.
Further there is an evening drive from 16:13 to 17:45. The power of 9 kW is required.

.. literalinclude:: /../tutorial/introductory/ev_charging/ev_charging_1.py
    :language: python
    :start-after: [trip_data_start]
    :end-before: [trip_data_end]

.. note::
    Keep in mind that the units used in your energy system model are only implicit
    and that you have to check their consistency yourself.


Lets look at the driving pattern

.. literalinclude:: /../tutorial/introductory/ev_charging/ev_charging_1.py
    :language: python
    :start-after: [plot_trip_data_start]
    :end-before: [plot_trip_data_end]

.. figure:: /../tutorial/introductory/ev_charging/figures/driving_pattern.png
    :align: center
    :alt: Driving pattern
    :figclass: only-light

.. figure:: /../tutorial/introductory/ev_charging/figures/driving_pattern.png
    :align: center
    :alt: Driving pattern
    :figclass: only-dark

    Driving pattern


Now we need to set up the electric energy carrying bus. We make sure to set a label to reference them later when we
analyze the results. After initialization, we add them to the ``ev_energy_system`` object.

.. literalinclude:: /../tutorial/introductory/ev_charging/ev_charging_1.py
    :language: python
    :start-after: [energysystem_and_bus_start]
    :end-before: [energysystem_and_bus_end]

As we have a demand time series which is actually in kW, we use a common
"hack" here: We set the nominal capacity to 1 (kW), so that
multiplication by the time series will just yield the correct result.
We define a "storage revenue" (negative costs) for the last time step,
so that energy inside the storage in the last time step is worth
something. 

.. literalinclude:: /../tutorial/introductory/ev_charging/ev_charging_1.py
    :language: python
    :start-after: [car_start]
    :end-before: [car_end]


As our system is complete for this step, its time to start the unit commitment
optimization. For that, we first have to create a :py:class:`solph.Model` instance
from our ``ev_energy_system``. Then we can use its :py:func:`solve` method
to run the optimization. We decide to use the open source solver CBC and add the
additional :py:attr:`solve_kwargs` parameter ``'tee'`` to ``True``, in order to
get a more verbose solver logging output in the console.


.. literalinclude:: /../tutorial/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [solve_start]
    :end-before: [solve_end]


Now plot the results using the helper function from helpers.py.

.. literalinclude:: /../tutorial/introductory/district_heating_supply/district_heating_supply_1.py
    :language: python
    :start-after: [plot_results_start]
    :end-before: [plot_results_end]

.. figure:: /../tutorial/introductory/ev_charging/figures/driving_pattern.png
    :align: center
    :alt: Driving pattern
    :figclass: only-light

.. figure:: /../tutorial/introductory/ev_charging/figures/driving_pattern.png
    :align: center
    :alt: Driving pattern
    :figclass: only-dark

    Driving pattern
