.. _basic_concepts_energy_system_label:

~~~~~~~~~~~~~
Energy System
~~~~~~~~~~~~~

In most cases an `EnergySystem` instance is defined when we start to build up an energy system model. The `EnergySystem` instance will contain the model's elements and a time index.

The model time is defined by the number of intervals and the length of intervals. The length of each interval does not have to be the same. The intervals are defined by giving a `pandas.DatetimeIndex` with all time steps that define the intervals. Be aware that you have to define n+1 time points to get n intervals. For non-leap year with hourly values that means 8761 time points to get 8760 interval e.g. 2018-01-01 00:00 to 2019-01-01 00:00.

The index will also be used for the results. For a numeric index the resulting time series will indexed with a numeric index starting with 0.

One can use the function
:py:func:`create_time_index` to create an equidistant datetime index.

.. code-block:: python

    from oemof.solph import create_time_index
    my_index = create_time_index(2011)


By default, the function creates an hourly index for one year. But it is possible to change the length of the interval to quarter hours for example. The default number of intervals is the number needed to cover the given year but the value can be overwritten by the user.

It is also possible to define the datetime index using pandas. See `pandas date_range guide <https://pandas.pydata.org/pandas-docs/stable/generated/pandas.date_range.html>`_ for more information.

.. code-block:: python

    import pandas as pd
    my_index = pd.date_range('1/1/2011', periods=8761, freq='h')




This index is used at initialisation of the energy system:

.. code-block:: python

    import oemof.solph as solph
    my_energysystem = solph.EnergySystem(timeindex=my_index)




After defining an instance of the `EnergySystem` class, one need to add nodes and links between them to define the underlying network of the energy system.

There are two types of *nodes* : *components* and *buses*. Every Component has to be connected with one or more *buses*. The link between a *component* and a *bus* (or between *two buses*) is called a *flow*.

All solph *components* can be used to set up an energy system model. However you should read the documentation of each *component* to learn about usage and restrictions. For example it is not possible to combine every *component* with every *flow*. Furthermore, you can add your own *components* in your application (see below) but we would be pleased to integrate them into solph if they are of general interest (see :ref:`feature_requests_and_feedback`).

There are different ways to add components. The following line adds a *bus* object to the energy system defined above.

.. code-block:: python

    my_energysystem.add(solph.buses.Bus())

It is also possible to assign the bus to a variable and add it afterwards. In that case it is easy to add as many objects as you like.

.. code-block:: python

    my_bus1 = solph.buses.Bus()
    my_bus2 = solph.buses.Bus()
    my_energysystem.add(my_bus1, my_bus2)

Therefore it is also possible to add lists or dictionaries of components.

.. code-block:: python

    # add a list
    my_energysystem.add(*my_list)

    # add a dictionary
    my_energysystem.add(*my_dictionary.values())




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

The figure shows a simple energy system using the four basic component classes and the Bus class.
If you remove the transmission line (transport 1 and transport 2) you get two systems but they still represent one energy system which will be optimised at once.




