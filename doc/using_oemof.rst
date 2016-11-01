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

.. 	image:: _files/example_network.svg
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
    Sink(label='sink_1', inputs={bus_1: []})
    
    # create sink 2
    Sink(label='sink_2', inputs={bus_2: []})    

    # create source
    Source(label='source', outputs={bus_1: []})

    # create transformer
    Transformer(label='transformer', inputs={bus_1: []}, outputs={bus_2: []})
    
The network class is aimed to be very generic and might have some network analyse tools in the future. By now the network library is mainly used as the base for the solph library.  

oemof-solph
===========
The :ref:`oemof_solph_label` library is part of the oemof installation. Solph is designed to create and solve linear or mixed-integer 
linear optimization problems. It is based on optimization modelling language pyomo.

To use solph at least one linear solver has to installed on you system. See the `pyomo installation guide <https://software.sandia.gov/downloads/pub/pyomo/PyomoInstallGuide.html#Solvers>`_ to learn which solvers are supported. Solph is tested with the open source solver `cbc` and the `gurobi` solver (free for academic use). The open `glpk` solver recently showed some odd behaviour.

The formulation of the energy system is based on the oemof-network library but contains additional components such as storages. Furthermore the network class are enhanced with additional parameters such as efficiencies, bounds, cost and more. See the API documentation for more details. Try the `solph examples <https://github.com/oemof/oemof/tree/master/examples>`_ to learn how to build a linear energy system.

oemof-outputlib
===============
The :ref:`oemof_outputlib_label` library is part of the oemof installation. The outputlib presents the results of an optimisation as a `pandas MultiIndex DataFrame <http://pandas.pydata.org/pandas-docs/stable/advanced.html>`_. This makes it easy to process or plot the results using the capabilities of the pandas library.

The following code returns the output (flow from power plant to electricity bus) of a power plant. The result is written to a csv file using the pandas `i/o methods <http://pandas.pydata.org/pandas-docs/stable/io.html>`_. To get the input of the power plant the type has to be changed to `from_bus`.

.. code-block:: python
    
    pp_gas = myresults.slice_by(obj_label='pp_gas', type='to_bus',
                                date_from='2012-01-01 00:00:00',
                                date_to='2012-12-31 23:00:00')
    pp_gas.to_csv('pp_gas.csv')
    
Beside this the outputlib provides some basic plot methods to create nice plots. The oemof plot methods can be used additionally and can easily be combined with the plot capabilities of pandas and matplotlib.

.. 	image:: _files/example_figures.png
   :scale: 100 %
   :alt: alternate text
   :align: center


feedinlib
=========
The `feedinlib <http://pythonhosted.org/feedinlib/getting_started.html>`_ library is not part of the oemof installation and has to be installed separately using pypi. At the current state the feedinlib can calculate the output from a wind and a pv power plant passing parameters describing the power plant and a weather data set.

.. code-block:: python

    my_weather = weather.FeedinWeather()
    my_weather.read_feedinlib_csv(filename='weather.csv')
    
    E126_power_plant = plants.WindPowerPlant(**enerconE126)
    E126_feedin = E126_power_plant.feedin(weather=my_weather,
                                          installed_capacity=15000000)  # 15 MW
    
    yingli_module = plants.Photovoltaic(**yingli210)
    pv_feedin = yingli_module.feedin(weather=my_weather, number=30000)  # 30000 modules
    
See the `documentation of the feedinlib <http://pythonhosted.org/feedinlib/>`_ for a full description of the library and the example above.

demandlib
=========
The `demandlib <http://demandlib.readthedocs.io/en/latest/getting_started.html>`_ library is not part of the oemof installation and has to be installed separately using pypi. At the current state the demandlib can be used to create load profiles for elctricity and heat knowing the annual demand. See the `documentation of the demandlib <http://demandlib.readthedocs.io/en/latest/>`_ for examples and a full description of the library.
