.. _basic_concepts_results_label:

~~~~~~~~~~~~~~~~
Results handling
~~~~~~~~~~~~~~~~

The main purpose of the processing module is to collect and organise results.
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
to its label. Thus, the above code is completely equivalent to:

.. code-block:: python

    [...]
    results = model.solve(solver=solver)
    flow_from_to = results["flow"][("from_node_label", "to_node_label")]
    storage_content = results["storage_content"]["storage_node_label"]

However, there is a big advantage in having the original nodes in the
column name. This way, you can use information not provided within the label.
For example, to collect all flows going to a GenericStorage,
the following code can be used:

.. code-block:: python

    flows = results["flow"]
    storage_inflow_columns = []
    for column in flows.columns:
        if isinstance(column[1], solph.components.GenericStorage):
            storage_inflow_columns.append(column)

    storage_inflows = flows[storage_inflow_columns]

Quickly plotting the Node balance
---------------------------------

The following code snippet is meant to give an idea how results can be
visualised. See how you can extract flows from the results to plot them:

.. code-block:: python

    [...]
    results = model.solve(solver=solver)
    flows = results["flow"]
    outflows = flows.xs("b_el", axis=1, level=0, drop_level=False)
    inflows = flows.xs("b_el", axis=1, level=1, drop_level=False)

    fig = plt.figure()
    ax = fig.add_subplot()

    ax.stackplot(
        inflows.index,
        inflows.T,
        labels=[f"supply: {col[0]}" for col in inflows.columns],
    )
    ax.plot(outflows, "k--", label="demand")

    ax.legend()
    plt.show()

If you want to have a DataFrame that contains all flows from and to
a specific node, you can also use masking.

.. code-block:: python

    [...]
    mask_bel = (
        flows.columns.to_frame(index=False).eq("b_el").any(axis=1).to_numpy()
    )

    flows_bel = flows.loc[:, mask_bel]

This way, you can also migrate from ``solph.views``.
That module was designed to extract node specific from
the nested result dictionary that is returned by calling
``solph.processing.results(Model)``. With the new results object,
this approach is no longer advised.
