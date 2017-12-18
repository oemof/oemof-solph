.. _oemof_outputlib_label:

#####################
oemof-outputlib
#####################

For version 0.2.0, the outputlib has been refactored. Tools for plotting optimization
results that were part of the outputlib in earlier versions are no longer part of this module
as the requirements to plotting functions greatly depend on individial requirements.

Basic functions for plotting of optimisation results are now found in
a separate repository `oemof_visio <https://github.com/oemof/oemof_visio>`_. 

.. contents::
    :depth: 1
    :local:
    :backlinks: top

The main purpose of the outputlib is to collect and organise results.
It converts the results to a dictionary holding pandas DataFrames and Series for all nodes and flows.
This way we can make use of the full power of the pandas package available to process
the results. 

See the `pandas documentation <http://pandas.pydata.org/pandas-docs/stable/>`_  to learn how to `visualise <http://pandas.pydata.org/pandas-docs/version/0.18.1/visualization.html>`_, `read or write <http://pandas.pydata.org/pandas-docs/stable/io.html>`_ or how to `access parts of the DataFrame <http://pandas.pydata.org/pandas-docs/stable/advanced.html>`_ to process them.

Collecting results
------------------

Collecting results can be done with the help of the processing module:

.. code-block:: python
    
    results = outputlib.processing.results(om)

The results are returned in form of a python dictionary holding pandas dataframes.
The dataframes contain scalar data (e.g. investments) and sequences describing nodes
(with keys like (node, None)) and flows between nodes (with keys like (node_1, node_2)).
You can directly extract the dataframes in the dictionary by using these keys,
 where "node" is the name of the object you want to address. If you want to address objects
by their label, you can convert the results dictionary such that the keys are changed to
strings given by the labels:

.. code-block:: python

    views.convert_keys_to_strings(results)
    print(results[(wind, bus_electricity)]['sequences']
    

Another option is to access data belonging to a grouping by the name of the grouping 
(`note also this section on groupings <http://oemof.readthedocs.io/en/latest/oemof_solph.html#the-grouping-module-sets>`_.
Given the label of an object, e.g. 'wind' you can access the grouping by its label 
and use this to extract data from the results dictionary.

.. code-block:: python

    node_wind = energysystem.groups['wind']
    print(results[(node_wind, bus_electricity)])
    

However, in many situations it might be convenient to use the views module to 
collect information on a specific node. You can request all data related to a
specific node by using either the node's variable name or its label:
 
.. code-block:: python

    data_wind = outputlib.views.node(results, 'wind')
    

A function for collecting and printing meta results, i.e. information on the objective function,
the problem and the solver, is provided as well:

.. code-block:: python

    meta_results = outputlib.processing.meta_results(om)
    pp.pprint(meta_results)
    


Drawing a graph representation of the energy system
---------------------------------------------------

A new feature as of version 0.2.0 is a function to draw a graph representation of
the energy system.


.. code-block:: python

    import graph_tools as gt
    my_graph = gt.graph(energy_system=es, optimization_model=om, node_color={demand_el: 'r'}, plot=False)
    
    # export graph as .graphml for programs like Yed where it can be
    # sorted and customized. this is especially helpful for large graphs
    import networkx as nx
    nx.write_graphml(my_graph, "my_graph.graphml")

