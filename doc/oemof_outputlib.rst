.. _oemof_outputlib_label:

#####################
oemof-outputlib
#####################

For version 0.2.0, the outputlib has been refactored. Tools for plotting optimization
results that were part of the outputlib in earlier versions are no longer part of this module,
as the requirements to plotting functions greatly depend on the situation and are thus
not generic. Basic functions for plotting of optimisation results are now found in
a separate repository `oemof_visio <https://github.com/oemof/oemof_visio>`. 

.. contents::
    :depth: 1
    :local:
    :backlinks: top

The main purpose of the outputlib is to collect and organise results.
The outputlib converts the results to a pandas MultiIndex DataFrame. 
In this way we make the full power of the pandas package available to process the results. 

See the `pandas documentation <http://pandas.pydata.org/pandas-docs/stable/>`_  to learn how to `visualise <http://pandas.pydata.org/pandas-docs/version/0.18.1/visualization.html>`_, `read or write <http://pandas.pydata.org/pandas-docs/stable/io.html>`_ or how to `access parts of the DataFrame <http://pandas.pydata.org/pandas-docs/stable/advanced.html>`_ to process them.

Collecting results
------------------

Collecting the results can be done with the help of the processing module:

.. code-block:: python

    results = outputlib.processing.results(om)
    

Collecting meta results, i.e. information on the objective function, the problem
and the solver:

.. code-block:: python

    meta_results = outputlib.processing.meta_results(om)

Collecting information on specific nodes
----------------------------------------

Information on specific node can be collected using the views module: 

.. code-block:: python

    heat = outputlib.views.node(results, 'heat')


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

