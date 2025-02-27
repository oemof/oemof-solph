.. _basic_concepts_energy_system_label:

~~~~~~~~~~~~~
Energy System
~~~~~~~~~~~~~

In most cases an EnergySystem object is defined when we start to build up an energy system model. The EnergySystem object will be the main container for the model's elements.

The model time is defined by the number of intervals and the length of intervals. The length of each interval does not have to be the same. This can be defined in two ways:

1. Define the length of each interval in an array/Series where the number of the elements is the number of intervals.
2. Define a `pandas.DatetimeIndex` with all time steps that encloses an interval. Be aware that you have to define n+1 time points to get n intervals. For non-leap year with hourly values that means 8761 time points to get 8760 interval e.g. 2018-01-01 00:00 to 2019-01-01 00:00.

The index will also be used for the results. For a numeric index the resulting time series will indexed with a numeric index starting with 0.

One can use the function
:py:func:`create_time_index` to create an equidistant datetime index. By default the function creates an hourly index for one year, so online the year has to be passed to the function. But it is also possible to change the length of the interval to quarter hours etc. The default number of intervals is the number needed to cover the given year but the value can be overwritten by the user.

It is also possible to define the datetime index using pandas. See `pandas date_range guide <https://pandas.pydata.org/pandas-docs/stable/generated/pandas.date_range.html>`_ for more information.

Both code blocks will create an hourly datetime index for 2011:

.. code-block:: python

    from oemof.solph import create_time_index
    my_index = create_time_index(2011)

.. code-block:: python

    import pandas as pd
    my_index = pd.date_range('1/1/2011', periods=8761, freq='h')

This index can be used to define the EnergySystem:

.. code-block:: python

    import oemof.solph as solph
    my_energysystem = solph.EnergySystem(timeindex=my_index)

Now you can start to add the components of the network.

After defining an instance of the EnergySystem class, in the following you have to add all nodes you define  to your EnergySystem.

Basically, there are two types of *nodes* - *components* and *buses*. Every Component has to be connected with one or more *buses*. The connection between a *component* and a *bus* is the *flow*.

All solph *components* can be used to set up an energy system model but you should read the documentation of each *component* to learn about usage and restrictions. For example it is not possible to combine every *component* with every *flow*. Furthermore, you can add your own *components* in your application (see below) but we would be pleased to integrate them into solph if they are of general interest (see :ref:`feature_requests_and_feedback`).

An example of a simple energy system shows the usage of the nodes for
real world representations:

.. 	figure:: /_files/oemof_solph_example_darkmode.svg
   :alt: oemof_solph_example_darkmode.svgt
   :align: center
   :figclass: only-dark

.. 	figure:: /_files/oemof_solph_example.svg
   :alt: oemof_solph_example.svg
   :align: center
   :figclass: only-light

The figure shows a simple energy system using the four basic network classes and the Bus class.
If you remove the transmission line (transport 1 and transport 2) you get two systems but they are still one energy system in terms of solph and will be optimised at once.

There are different ways to add components to an *energy system*. The following line adds a *bus* object to the *energy system* defined above.

.. code-block:: python

    my_energysystem.add(solph.buses.Bus())

It is also possible to assign the bus to a variable and add it afterwards. In that case it is easy to add as many objects as you like.

.. code-block:: python

    my_bus1 = solph.buses.Bus()
    my_bus2 = solph.buses.Bus()
    my_energysystem.add(my_bus1, my_bus2)

Therefore it is also possible to add lists or dictionaries with components but you have to dissolve them.

.. code-block:: python

    # add a list
    my_energysystem.add(*my_list)

    # add a dictionary
    my_energysystem.add(*my_dictionary.values())



