.. _basic_concepts_flows_label:

~~~~~
Flows
~~~~~

The flow class has to be used to connect nodes and buses. An instance of the Flow class is normally used in combination with the definition of a component.
A Flow can be limited by upper and lower bounds (constant or time-dependent) or by summarised limits.
For all parameters see the API documentation of the :py:class:`~oemof.solph.flows._flow.Flow` class or the examples of the nodes below. A basic flow can be defined without any parameter.

.. code-block:: python

    solph.flows.Flow()

oemof.solph has different types of *flows* but you should be aware that you cannot connect every *flow* type with every *component*.

.. note:: See the :py:class:`~oemof.solph.flows._flow.Flow` class for all parameters and the mathematical background.
.
