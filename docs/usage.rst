.. _oemof_solph_label:

.. _using_oemof_label:

~~~~~~~~~~~~
User's guide
~~~~~~~~~~~~

Solph is an oemof-package, designed to create and solve linear or mixed-integer linear optimization problems. The package is based on pyomo. To create an energy system model generic and specific components are available. To get started with solph, checkout the examples in the :ref:`examples_label` section.

This User's guide provides a user-friendly introduction into oemof.solph,
which includes small examples and nice illustrations.
However, the functionalities of oemof.solph go beyond the content of this User's guide section.
So, if you want to know all details of a certain component or a function,
please go the :ref:`api_reference_label`. There, you will find
a detailed and complete description of all oemof.solph modules.

How can I use solph?
--------------------

To use solph you have to install oemof.solph and at least one solver (see :ref:`installation_label`),
which can be used together with `pyomo <https://pyomo.readthedocs.io/en/stable/getting_started/installation.html>`_
(e.g. CBC, GLPK, Gurobi, Cplex).
You can test it by executing one of the existing examples (see :ref:`examples_label`).
Be aware that the examples require the CBC solver but you can change the solver name in the example files to your
solver.

Once the examples work you are close to your first energy model.


Handling of Warnings
^^^^^^^^^^^^^^^^^^^^

The solph library is designed to be as generic as possible to make it possible
to use it in different use cases. This concept makes it difficult to raise
Errors or Warnings because sometimes untypical combinations of parameters are
allowed even though they might be wrong in over 99% of the use cases.

Therefore, a SuspiciousUsageWarning was introduced. This warning will warn you
if you do something untypical. If you are sure that you know what you are doing
you can switch the warning off.

See `the debugging module of oemof-tools <https://oemof-tools.readthedocs.io/en/latest/usage.html#debugging>`_ for more
information.







Analysing your results
^^^^^^^^^^^^^^^^^^^^^^

If you want to analyse your results, you should first dump your EnergySystem instance to permanently store results. Otherwise you would have to run the simulation again.

.. code-block:: python

    my_energysystem.results = processing.results(om)
    my_energysystem.dump('my_path', 'my_dump.oemof')

If you need the meta results of the solver you can do the following:

.. code-block:: python

    my_energysystem.results['main'] = processing.results(om)
    my_energysystem.results['meta'] = processing.meta_results(om)
    my_energysystem.dump('my_path', 'my_dump.oemof')

To restore the dump you can simply create an EnergySystem instance and restore your dump into it.

.. code-block:: python

    import oemof.solph as solph
    my_energysystem = solph.EnergySystem()
    my_energysystem.restore('my_path', 'my_dump.oemof')
    results = my_energysystem.results

    # If you use meta results do the following instead of the previous line.
    results = my_energysystem.results['main']
    meta = my_energysystem.results['meta']


If you call dump/restore without any parameters, the dump will be stored as *'es_dump.oemof'* into the *'.oemof/dumps/'* folder created in your HOME directory.

See :ref:`oemof_outputlib_label` to learn how to process, plot and analyse the results.


.. _oemof_solph_components_label:



The Grouping module (Sets)
--------------------------
To construct constraints,
variables and objective expressions inside all Block classes
and the :py:mod:`~oemof.solph.models` modules, so called groups are used. Consequently,
certain constraints are created for all elements of a specific group. Thus,
mathematically the groups depict sets of elements inside the model.

The grouping is handled by the solph grouping module :py:mod:`~oemof.solph.groupings`
which is based on the groupings module functionality of oemof network. You
do not need to understand how the underlying functionality works. Instead, checkout
how the solph grouping module is used to create groups.

The simplest form is a function that looks at every node of the energy system and
returns a key for the group depending e.g. on node attributes:

.. code-block:: python

    def constraint_grouping(node):
        if isinstance(node, Bus) and node.balanced:
            return blocks.Bus
        if isinstance(node, Converter):
            return blocks.Converter
   GROUPINGS = [constraint_grouping]

This function can be passed in a list to `groupings` of
:class:`oemof.solph.network.energy_system.EnergySystem`. So that we end up with two groups,
one with all Converters and one with all Buses that are balanced. These
groups are simply stored in a dictionary. There are some advanced functionalities
to group two connected nodes with their connecting flow and others
(see for example: FlowsWithNodes class in the oemof.network package).


Using the Excel (csv) reader
----------------------------

Alternatively to a manual creation of energy system component objects as describe above, can also be created from a excel sheet (libreoffice, gnumeric...).

The idea is to create different sheets within one spreadsheet file for different components. Afterwards you can loop over the rows with the attributes in the columns. The name of the columns may differ from the name of the attribute. You may even create two sheets for the GenericStorage class with attributes such as C-rate for batteries or capacity of turbine for a PHES.

Once you have create your specific excel reader you can lower the entry barrier for other users. It is some sort of a GUI in form of platform independent spreadsheet software and to make data and models exchangeable in one archive.

See :ref:`excel_reader_example_label` for an excel reader example.


