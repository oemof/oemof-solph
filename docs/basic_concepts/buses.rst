.. _basic_concepts_buses_label:

~~~~~
Buses
~~~~~

All flows into and out of a *bus* are balanced (by default). To define an instance of a Bus only a unique label is necessary. If you do not set a label a random label is assigned but this makes it difficult to track the results later on.

To make it easier to connect the bus to a component you can assign it to a variable for later use.

.. code-block:: python

    solph.buses.Bus(label='natural_gas')
    electricity_bus = solph.buses.Bus(label='electricity')

.. note:: See the :py:class:`~oemof.solph.buses._bus.Bus` class for all parameters and the mathematical background.

