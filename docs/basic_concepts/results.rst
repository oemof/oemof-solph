.. _basic_concepts_results_label:

~~~~~~~~~~~~~~~~
Results handling
~~~~~~~~~~~~~~~~

The main purpose of the processing module is to collect and organise results.
The views module will provide some typical representations of the results.
Plots are not part of solph, because plots are highly individual. However, the
provided pandas.DataFrames are a good start for plots. Some basic functions
for plotting of optimisation results can be found in the separate repository
`oemof_visio <https://github.com/oemof/oemof-visio>`_.

The ``Model.solve`` function gives back the results in a form comparable
to a Python dictionary holding pandas Series and pandas DataFrames.
This way, we can make use of the full power
of the pandas package available to process the results.

See the `pandas documentation <https://pandas.pydata.org/pandas-docs/stable/>`_
to learn how to `visualise
<https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html>`_,
`read or write
<https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html>`_ or how to
`access parts of the DataFrame
<https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html>`_ to
process them.

Getting results
---------------

The results are returned when the model has been solved.
(An error will be risen ounbound or infeasible models.)
The entries of the ``Results`` object depend on the model,
i.e., only keys for existing variables are created.
You can receive a list by calling ``Results.keys()``.
Depending on the variable, you will receive a Sequence or a DataFrame.
The columns are typically indexed using nodes, e.g.:

.. code-block:: python

    [...]
    results = model.solve(solver=solver)
    flow_from_to = results["flow"][(from_node, to_node)]
    storage_content = results["storage_content"][storage_node]


Note that data is processed on demand, meaning that accessing data can trigger
calculations. So if you are not interested in every detail of you results,
some time can be saved here.

Working with results
--------------------

First of all, it should be mentioned that a Node is considered to be equal
to its label. Thus, the above code is completely equivilent to:

.. code-block:: python

    [...]
    results = model.solve(solver=solver)
    flow_from_to = results["flow"][("from_node_label", "to_node_label")]
    storage_content = results["storage_content"]["storage_node_label"]

However, there is a big advantage in having the original nodes in the
column name. This way, you can use information not provided in the label.
For example, to collect all Flows going to a GenericStorage,
the following code can be used:

.. code-block:: python

    flows = results["flow"]
    storage_inflow_columns = []
    for column in flows.columns:
        if isinstance(column[1], solph.components.GenericStorage):
            storage_inflow_columns.append(column)

    storage_inflows = flows[storage_inflow_columns]
