.. _basic_concepts_results_label:

~~~~~~~~~~~~~~~~
Results handling
~~~~~~~~~~~~~~~~

Handling Results
--------------------

The main purpose of the processing module is to collect and organise results.
The views module will provide some typical representations of the results.
Plots are not part of solph, because plots are highly individual. However, the
provided pandas.DataFrames are a good start for plots. Some basic functions
for plotting of optimisation results can be found in the separate repository
`oemof_visio <https://github.com/oemof/oemof-visio>`_.

The ``processing.results`` function gives back the results as a python
dictionary holding pandas Series for scalar values and pandas DataFrames for
all nodes and flows between them. This way we can make use of the full power
of the pandas package available to process the results.

See the `pandas documentation <https://pandas.pydata.org/pandas-docs/stable/>`_
to learn how to `visualise
<https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html>`_,
`read or write
<https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html>`_ or how to
`access parts of the DataFrame
<https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html>`_ to
process them.

The results chapter consists of three parts:

.. contents::
    :depth: 1
    :local:
    :backlinks: top

The first step is the processing of the results (:ref:`results_collect_results_label`)
This is followed by basic examples of the general analysis of the results
(:ref:`res_general_approach_label`) and finally the use of functionality already included in solph
for providing a quick access to your results (:ref:`results_easy_access_label`).
Especially for larger energy systems the general approach will help you to
write your own results processing functions.

.. _results_easy_access_label:

Easy access
^^^^^^^^^^^

The solph package provides some functions which will help you to access your
results directly via labels, which is helpful especially for small energy
systems.
So, if you want to address objects by their label, you can convert the results
dictionary such that the keys are changed to strings given by the labels:

.. code-block:: python

    views.convert_keys_to_strings(results)
    print(results[('wind', 'bus_electricity')]['sequences']


Another option is to access data belonging to a grouping by the name of the grouping
(`note also this section on groupings <https://oemof-solph.readthedocs.io/en/latest/usage.html#the-grouping-module-sets>`_).
Given the label of an object, e.g. 'wind' you can access the grouping by its label
and use this to extract data from the results dictionary.

.. code-block:: python

    node_wind = energysystem.groups['wind']
    print(results[(node_wind, bus_electricity)])


However, in many situations it might be convenient to use the views module to
collect information on a specific node. You can request all data related to a
specific node by using either the node's variable name or its label:

.. code-block:: python

    data_wind = solph.views.node(results, 'wind')


A function for collecting and printing meta results, i.e. information on the objective function,
the problem and the solver, is provided as well:

.. code-block:: python

    meta_results = solph.processing.meta_results(om)
    pp.pprint(meta_results)


.. _results_collect_results_label:

Collecting results
^^^^^^^^^^^^^^^^^^

Collecting results can be done with the help of the processing module. A solved
model is needed:

.. code-block:: python

    [...]
    model.solve(solver=solver)
    results = solph.processing.results(model)

The scalars and sequences describe nodes (with keys like (node, None)) and
flows between nodes (with keys like (node_1, node_2)). You can directly extract
the data in the dictionary by using these keys, where "node" is the name of
the object you want to address.
Processing the results is the prerequisite for the examples in the following
sections.

.. _res_general_approach_label:

General approach
^^^^^^^^^^^^^^^^

As stated above, after processing you will get a dictionary with all result
data.
If you want to access your results directly via labels, you
can continue with :ref:`results_easy_access_label`. For a systematic analysis list comprehensions
are the easiest way of filtering and analysing your results.

The keys of the results dictionary are tuples containing two nodes. Since flows
have a starting node and an ending node, you get a list of all flows by
filtering the results using the following expression:

.. code-block:: python

    flows = [x for x in results.keys() if x[1] is not None]

On the same way you can get a list of all nodes by applying:

.. code-block:: python

    nodes = [x for x in results.keys() if x[1] is None]

Probably you will just get storages as nodes, if you have some in your energy
system. Note, that just nodes containing decision variables are listed, e.g. a
Source or a Converter object does not have decision variables. These are in
the flows from or to the nodes.

All items within the results dictionary are dictionaries and have two items
with 'scalars' and 'sequences' as keys:

.. code-block:: python

    for flow in flows:
        print(flow)
        print(results[flow]['scalars'])
        print(results[flow]['sequences'])

There many options of filtering the flows and nodes as you prefer.
The following will give you all flows which are outputs of converter:

.. code-block:: python

    flows_from_converter = [x for x in flows if isinstance(
        x[0], solph.components.Converter)]

You can filter your flows, if the label of in- or output contains a given
string, e.g.:

.. code-block:: python

    flows_to_elec = [x for x in results.keys() if 'elec' in x[1].label]

Getting all labels of the starting node of your investment flows:

.. code-block:: python

    flows_invest = [x[0].label for x in flows if hasattr(
        results[x]['scalars'], 'invest')]
