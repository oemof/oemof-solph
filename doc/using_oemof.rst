.. _using_oemof_label:

#####################
Using oemof
#####################

Oemof is a framework and even though it is in an early stage it already provides useful tools to model energy systems. To model an energy system you have to write your own application in which you combine the oemof libraries for you specific task. The `example section <https://github.com/oemof/oemof/tree/master/examples>`_ shows how an oemof application may look like. 

.. contents:: `Current oemof libraries`
    :depth: 1
    :local:
    :backlinks: top


oemof-network
=============
The :ref:`oemof_network_label` library is part of the oemof installation. By now it can be used to define energy systems as a network with components and buses. Every component should be connected to one or more buses. Allowed components are sources, sinks and transformer.

.. 	image:: example_network.svg
   :scale: 30 %
   :alt: alternate text
   :align: center
   
The code of the example above:

.. code-block:: python

    from oemof.network import *
    from oemof.energy_system import *

    # create the energy system
    es = EnergySystem()
    
    # create bus 1
    bus_1 = Bus(label="bus_1")

    # create bus 2
    bus_2 = Bus(label="bus_2")

    # create sink 1
    Sink(label='sink_1', inputs={bus_1: Flow()})
    
    # create sink 2
    Sink(label='sink_2', inputs={bus_2: Flow()})    

    # create source
    Source(label='source', outputs={bus_1: Flow()})

    # create transformer
    Transformer(label='transformer', inputs={bus_1: Flow()}, outputs={bus_2: Flow()})

oemof-solph
===========
The :ref:`oemof_solph_label` library is... (short paragraph)

oemof-outputlib
===============
The :ref:`oemof_outputlib_label` library is... (short paragraph)

feedinlib
=========
The `feedinlib <http://pythonhosted.org/feedinlib/getting_started.html>`_ library is... (short paragraph)

demandlib
=========
The `demandlib <http://demandlib.readthedocs.io/en/latest/getting_started.html>`_ library is (short paragraph)