.. _oemof_solph_label:

~~~~~~~~~~~
oemof-solph
~~~~~~~~~~~

Solph is an oemof-package, designed to create and solve linear or mixed-integer linear optimization problems. The packages is based on pyomo. To create an energy system model the :ref:`oemof_network_label` ist used and extended by components such as storages. To get started with solph, checkout the solph-examples in the :ref:`solph_examples_label` section.

.. contents::
    :depth: 2
    :local:
    :backlinks: top


How can I use solph?
--------------------

To use solph you have to install oemof and at least one solver, which can be used together with pyomo. See `pyomo installation guide <https://software.sandia.gov/downloads/pub/pyomo/PyomoInstallGuide.html#Solvers>`_.
You can test it by executing one of the existing examples. Be aware that the examples require the CBC solver but you can change the solver name in the example files to your solver.

Once the example work you are close to your first energy model.

Set up an energy system
^^^^^^^^^^^^^^^^^^^^^^^

In most cases an EnergySystem object is defined when we start to build up an energy system model. The EnergySystem object will be the main container for the model.

To define an EnergySystem we need a Datetime index to define the time range and increment of our model. An easy way to this is to use the pandas time_range function.
The following code example defines the year 2011 in hourly steps. See `pandas date_range guide <http://pandas.pydata.org/pandas-docs/stable/generated/pandas.date_range.html>`_ for more information.

.. code-block:: python

    import pandas as pd
    my_index = pd.date_range('1/1/2011', periods=8760, freq='H')

This index can be used to define the EnergySystem:

.. code-block:: python

    import oemof.solph as solph
    my_energysystem = solph.EnergySystem(timeindex=my_index)

Now you can start to add the components of the network.


Add your components to the energy system
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have defined an instance of the EnergySystem class all components you define will automatically be added to your EnergySystem.

Basically, there are four types of Nodes and every node has to be connected with one or more buses. The connection between a component and a bus is the flow.

 * Sink (one input, no output)
 * Source (one output, no input)
 * LinearTransformer (one input, n outputs)
 * Storage (one input, one output)

Using these types it is already possible to set up an simple energy model. But more types (e.g. flexible CHP transformer) are currently being developed.
You can add your own types in your application (see below) but we would be pleased to integrate them into solph if they are of general interest.

.. 	image:: _files/oemof_solph_example.svg
   :scale: 10 %
   :alt: alternate text
   :align: center

The figure shows a simple energy system using the four basic network classes and the Bus class.
If you remove the transmission line (transport 1 and transport 2) you get two systems but they are still one energy system in terms of solph and will be optimised at once.

Bus
+++

All flows into and out of a bus are balanced. Therefore an instance of the Bus class represents a grid or network without losses. To define an instance of a Bus only a unique name is necessary.
To make it easier to connect the bus to a component you can optionally assign a variable for later use.


.. code-block:: python

    solph.Bus(label='natural_gas')
    electricity_bus = solph.Bus(label='electricity')

The following code shows the difference between a bus that is assigned to a variable and one that is not.

.. code-block:: python

    print(my_energsystem.groups['natural_gas']
    print(electricity_bus)

.. note:: See the :py:class:`~oemof.solph.network.Bus` class for all parameters and the mathematical background.


Flow
++++

The flow class has to be used to connect. An instance of the Flow class is normally used in combination with the definition of a component.
A Flow can be limited by upper and lower bounds (constant or time-dependent) or by summarised limits.
For all parameters see the API documentation of the :py:class:`~oemof.solph.network.Flow` class or the examples of the nodes below. A basic flow can be defined without any parameter.

.. code-block:: python

    solph.Flow()

.. note:: See the :py:class:`~oemof.solph.network.Flow` class for all parameters and the mathematical background.


Sink
++++

A sink is normally used to define the demand within an energy model but it can also be used to detect excesses.

The example shows the electricity demand of the electricity_bus defined above.
The *'my_demand_series'* should be sequence of normalised values while the *'nominal_value'* is the maximum demand the normalised sequence is multiplied with.
The parameter *'fixed=True'* means that the actual_value can not be changed by the solver.

.. code-block:: python

    solph.Sink(label='electricity_demand', inputs={electricity_bus: solph.Flow(
        actual_value=my_demand_series, fixed=True, nominal_value=nominal_demand)})

In contrast to the demand sink the excess sink has normally less restrictions but is open to take the whole excess.

.. code-block:: python

    solph.Sink(label='electricity_excess', inputs={electricity_bus: solph.Flow()})

.. note:: The Sink class is only a plug and provides no additional constraints or variables.


Source
++++++

A source can represent a pv-system, a wind power plant, an import of natural gas or a slack variable to avoid creating an in-feasible model.

While a wind power plant will have an hourly feed-in depending on the weather conditions the natural_gas import might be restricted by maximum value (*nominal_value*) and an annual limit (*summed_max*).
As we do have to pay for imported gas we should set variable costs.
Comparable to the demand series an *actual_value* in combination with *'fixed=True'* is used to define the normalised output of a wind power plan. The *nominal_value* sets the installed capacity.

.. code-block:: python

    solph.Source(
        label='import_natural_gas',
        outputs={my_energsystem.groups['natural_gas']: solph.Flow(
            nominal_value=1000, summed_max=1000000, variable_costs=50)})

    solph.Source(label='wind', outputs={electricity_bus: solph.Flow(
        actual_value=wind_power_feedin_series, nominal_value=1000000, fixed=True)})

.. note:: The Source class is only a plug and provides no additional constraints or variables.

.. _linear_transformer_class_label:

LinearTransformer (1xM)
+++++++++++++++++++++++

An instance of the LinearTransformer class can represent a node with one input flow an m output flows such as a power plant, a transport line or any kind of a transforming process as electrolysis or a cooling device.
As the name indicates the efficiency has to be constant within one time step to get a linear transformation.
You can define a different efficiency for every time step (e.g. the thermal powerplant efficiency according to the ambient temperature) but this series has to be predefined and cannot be changed within the optimisation.

.. code-block:: python

    solph.LinearTransformer(
        label="pp_gas",
        inputs={my_energsystem.groups['natural_gas']: solph.Flow()},
        outputs={electricity_bus: solph.Flow(nominal_value=10e10)},
        conversion_factors={electricity_bus: 0.58})

A CHP power plant would be defined in the same manner. New buses are defined to make the code cleaner:

.. code-block:: python

    b_el = solph.Bus(label='electricity')
    b_th = solph.Bus(label='heat')

    solph.LinearTransformer(
        label='pp_chp',
        inputs={bgas: Flow()},
        outputs={b_el: Flow(nominal_value=30),
                 b_th: Flow(nominal_value=40)},
        conversion_factors={b_el: 0.3, b_th: 0.4})

.. note:: See the :py:class:`~oemof.solph.network.LinearTransformer` class for all parameters and the mathematical background.

VariableFractionTransformer
+++++++++++++++++++++++++++

The VariableFractionTransformer inherits from the :ref:`linear_transformer_class_label` class. An instance of this class can represent a component with one input and two output flows and a flexible ratio between these flows. By now this class is restricted to one input and two output flows. One application example would be a flexible combined heat and power (chp) plant. The class allows to define a different efficiency for every time step but this series has to be predefined a parameter for the optimisation. In contrast to the LinearTransformer, a main flow and a tapped flow is defined. For the main flow you can define a conversion factor if the second flow is zero (conversion_factor_single_flow).

.. code-block:: python

    solph.VariableFractionTransformer(
        label='variable_chp_gas',
        inputs={bgas: solph.Flow(nominal_value=10e10)},
        outputs={bel: solph.Flow(), bth: solph.Flow()},
        conversion_factors={bel: 0.3, bth: 0.5},
        conversion_factor_single_flow={bel: 0.5}
        )

The key of the parameter *'conversion_factor_single_flow'* will indicate the main flow. In the example above, the flow to the Bus *'bel'* is the main flow and the flow to the Bus *'bth'* is the tapped flow. The following plot shows how the variable chp (right) shedules it's electrical and thermal power production in contrast to a fixed chp (left). The plot is the output of the :ref:`variable_chp_examples_label` below.

.. 	image:: _files/variable_chp_plot.svg
   :scale: 10 %
   :alt: variable_chp_plot.svg
   :align: center

.. note:: See the :py:class:`~oemof.solph.network.VariableFractionTransformer` class for all parameters and the mathematical background.

LinearTransformer (Nx1)
+++++++++++++++++++++++

An instance of the LinearTransformer class can represent a node with m input flows an one output flows such as a heat pump, additional heat supply or any kind of a process where two input flows are reduced to one output flow.
As the name indicates the efficiency has be to constant within one time step to get a linear transformation.
You can define a different efficiency for every time step (e.g. the COP of an air heat pump according to the ambient temperature) but this series has to be predefined and cannot be changed within the optimisation.

.. code-block:: python

    solph.LinearN1Transformer(
        label="pp_gas",
        inputs={my_energsystem.groups['natural_gas']: solph.Flow()},
        outputs={electricity_bus: solph.Flow(nominal_value=10e10)},
        conversion_factors={electricity_bus: 0.58})

A heat pump would be defined in the same manner. New buses are defined to make the code cleaner:

.. code-block:: python

    b_el = solph.Bus(label='electricity')
    b_th_low = solph.Bus(label='low_temp_heat')
    b_th_high = solph.Bus(label='high_temp_heat')

    cop = 3  # coefficient of performance of the heat pump

    solph.LinearN1Transformer(
        label='heat_pump',
        inputs={bus_elec: Flow(), bus_low_temp_heat: Flow()},
        outputs={bus_th_high: Flow()},
        conversion_factors={bus_elec: cop,
                            b_th_low: cop/(cop-1)})

If the low temperature reservoir is nearly infinite (ambient air heat pump) the low temperature bus is not needed and therefore 1x1-Transformer is sufficient.

.. note:: See the :py:class:`~oemof.solph.network.LinearN1Transformer` class for all parameters and the mathematical background.


Storage
+++++++

In contrast to the three classes above the storage class is a pure solph class and is not inherited from the oemof-network module.
The *nominal_value* of the storage signifies the nominal capacity. To limit the input and output flows you can define the ratio between these flows and the capacity using *nominal_input_capacity_ratio* and *nominal_output_capacity_ratio*.
Furthermore an efficiency for loading, unloading and a capacity loss per time increment can be defined. For more information see the definition of the  :py:class:`~oemof.solph.network.Storage` class.

.. code-block:: python

    solph.Storage(
        label='storage',
        inputs={b_el: solph.Flow(variable_costs=10)},
        outputs={b_el: solph.Flow(variable_costs=10)},
        capacity_loss=0.001, nominal_value=50,
        nominal_input_capacity_ratio=1/6,
        nominal_output_capacity_ratio=1/6,
        inflow_conversion_factor=0.98, outflow_conversion_factor=0.8)

.. note:: See the :py:class:`~oemof.solph.network.Storage` class for all parameters and the mathematical background.


.. _oemof_solph_optimise_es_label:

Optimise your energy system
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The typical optimisation of a energy system in solph is the dispatch optimisation which means that the use of the sources is optimised to satisfy the demand at least costs.
Therefore variable cost can be defined for all components. The cost for gas should be defined in the gas source while the variable costs of the gas power plant are caused by operating material.
You can deviate from this scheme but you should keep it consistent to make it understandable for others.

Cost do have to be monitory cost but could be emissions or other variable units.

Furthermore it is possible to optimise the capacity of different components (see :ref:`investment_mode_label`).

.. code-block:: python

    import os
    # set up a simple least cost optimisation
    om = solph.OperationalModel(my_energysystem)

    # write the lp file for debugging or other reasons
    om.write(os.path.join(path, 'my_model.lp'), io_options={'symbolic_solver_labels': True})

    # solve the energy model using the CBC solver
    om.solve(solver='cbc', solve_kwargs={'tee': True})


Analysing your results
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to analyse your results, you should first dump your EnergySystem instance, otherwise you have to run the simulation again.

.. code-block:: python

    my_energysystem.dump('my_path', 'my_dump.oemof')

To restore the dump you can simply create an EnergySystem instance and restore your dump into it.

.. code-block:: python

    import pandas as pd
    import oemof.solph as solph
    my_index = pd.date_range('1/1/2011', periods=8760, freq='H')
    new_energysystem = solph.EnergySystem(timeindex=my_index)
    new_energysystem.restore('my_path', 'my_dump.oemof')

If you call dump/restore with any parameters, the dump will be stored as *'es_dump.oemof'* into the *'.oemof/dumps/'* folder created in your HOME directory.

In the outputlib the results will be converted to a pandas MultiIndex DataFrame. This makes it easy to plot, save or process the results. See :ref:`oemof_outputlib_label` for more information.


.. _investment_mode_label:

Using the investment mode
-------------------------

As described in :ref:`oemof_solph_optimise_es_label` the typical way to optimise an energy system is the dispatch optimisation based on marginal costs. Solph also provides a combined dispatch and investment optimisation.
Based on investment costs you can compare the usage of existing components against building up new capacity.
The annual savings by building up new capacity has therefore compensate the annuity of the investment costs (the time period does not have to be on year but depends on your Datetime index).

See the API of the :py:class:`~oemof.solph.options.Investment` class to see all possible parameters.

Basically an instance of the investment class can be added to a Flow or a Storage. Adding an investment object the *nominal_value* or *nominal_capacity* should not be set.
All parameters that usually refer to the *nominal_value/capacity* will now refer to the investment variable. It is also possible to set a maximum limit for the capacity that can be build.

For example if you want to find out what would be the optimal capacity of a wind power plant to decrease the costs of an existing energy system you can define this model and add an investment source.
The *wind_power_time_series* has to be a normalised feed-in time series of you wind power plant. The maximum value might be caused by limited space for wind turbines.

.. code-block:: python

    solph.Source(label='new_wind_pp', outputs={electricity: solph.Flow(
        actual_value=wind_power_time_series, fixed=True,
	investment=solph.Investment(ep_costs=epc, maximum=50000))})

The periodical cost are typically calculated as follows:

.. code-block:: python

    capex = 1000  # investment cost
    lifetime = 20  # llife expectancy
    wacc = 0.05  # weighted average capital cost
    epc = capex * (wacc * (1 + wacc) ** lifetime) / ((1 + wacc) ** lifetime - 1)

The following code shows a storage with an investment object.

.. code-block:: python

    solph.Storage(
        label='storage', capacity_loss=0.01,
        inputs={electricity: solph.Flow()}, outputs={electricity: solph.Flow()},
        nominal_input_capacity_ratio=1/6, nominal_output_capacity_ratio=1/6,
        inflow_conversion_factor=0.99, outflow_conversion_factor=0.8,
        investment=solph.Investment(ep_costs=epc))

.. note:: At the moment the investment class is not compatible with the MIP classes :py:class:`~oemof.solph.options.BinaryFlow` and :py:class:`~oemof.solph.options.DiscreteFlow`.


Mixed Integer (Linear) Problems
-------------------------------

Solph also allows you to model components with respect to more technical details.
For example you can model a mimimal power production (Pmin-Constraint) within
oemof. Therefore, the following two classes exist in the oemof.solph.options
module: :py:class:`~oemof.solph.options.BinaryFlow` and :py:class:`~oemof.solph.options.DiscreteFlow`.
Note that the usage of these classes is not compatible with the
:py:class:`~oemof.solph.options.Investment` class at the moment.

If you want to use the functionalities of the options-module the only thing
you have to do is invoke class instance inside your Flow() - declaration:

.. code-block:: python

    b_el = solph.Bus(label='electricity')
    b_th = solph.Bus(label='heat')

    solph.LinearTransformer(
        label='pp_chp',
        inputs={bgas: Flow(discrete=DiscreteFlow())},
        outputs={b_el: Flow(nominal_value=30, binary=BinaryFlow()),
                 b_th: Flow(nominal_value=40)},
        conversion_factors={b_el: 0.3, b_th: 0.4})

The created LinearTransformer will now force the flow variable of its input (gas)
to be of the domain discrete, i.e. {min, ... 10, 11, 12, ..., max}. The BinaryFlow()
object of the 'electrical' flow will create a 'status' variable for the flow.
This will be used to model for example Pmin/Pmax constraints if the attribute `min`
of the flow is set. It will also be used to include start up constraints and costs
if correponding attributes of the class are provided. For more
information see API of BinaryFlow() class and its corresponding block class:
:py:class:`~oemof.solph.blocks.BinaryFlow`.

.. note:: The usage of these classes can sometimes be tricky as there are many interdenpendencies. So
          check out the examples and do not hesitate to ask the developers, if your model does
          not work as exspected.



Adding additional constraints
-----------------------------

You can add additional constraints to your :py:class:`~oemof.solph.models.OperationalModel`.
For now, you have to check out the examples in the :ref:`solph_examples_flex_label` example.



The Grouping module (Sets)
-----------------------------------------------------
To construct constraints,
variables and objective expressions inside the :py:mod:`~oemof.solph.blocks`
and the :py:mod:`~oemof.solph.models` modules, so called groups are used. Consequently,
certain constraints are created for all elements of a sepecific group. Thus
mathematically the groups depict sets of elements inside the model.

The grouping is handeld by the solph grouping module :py:mod:`~oemof.solph.groupings`
which is based on the oemof core :py:mod:`~oemof.groupings` functionalities. You
do not need to understand how the underlying functionality works. Instead, checkout
how the solph grouping module is used to create groups.

The simpelst form is a function that looks at every node of the energy system and
returns a key for the group depending e.g. on node attributes:

.. code-block:: python

    def constraint_grouping(node):
        if isinstance(node, Bus) and node.balanced:
            return blocks.Bus
        if isinstance(node, LinearTransformer):
            return blocks.LinearTransformer
   GROUPINGS = [constraint_grouping]

This function can be passed in a list to :attr:`groupings` of
:class:`oemof.solph.network.EnergySystem`. So that we end up with two groups,
one with all LinearTransformers and one with all Buses that are balanced. These
groups are simply stored in a dictionary. There are some advanced functionalities
to group two connected nodes with their connecting flow and others
(see for example: :py:class:`~oemof.groupings.FlowsWithNodes`).


Using the CSV reader
-----------------------------------------------------

Alternatively to a manual creation of energy system component objects as describe above, these can also be created from a pre-defined csv-structure via a csv-reader.
Technically speaking, the csv-reader is a simple parser that creates oemof nodes and their respective flows by interating line by line through texts files of a specific format.
The original idea behind this approach was to lower the entry barrier for new users, to have some sort of GUI in form of platform independent spreadsheet software and to make data and models exchangeable in one archive.

Both, investment and dispatch (operational) models can be modelled. Two examples and more information about the functionality can be found in the :ref:`solph_examples_csv_label` section.


.. _solph_examples_label:

Solph Examples
--------------

The following examples are available for solph. See section ":ref:`check_installation_label`" to learn how to execute the examples directly. Be aware that the CBC solver has to be installed to run the examples (:ref:`solver_label`). If you want to use a different solver you can download the examples below and change the solver name manually.

.. _solph_examples_csv_label:

Csv_reader
^^^^^^^^^^

The csv-reader provides an easy to use interface to the solph library. The objects are defined using csv-files and are automatically created. There are two examples available.

 * Dispatch example (:download:`source file <../examples/solph/csv_reader/dispatch/dispatch.py>`, :download:`data file 1 <../examples/solph/csv_reader/dispatch/scenarios/example_energy_system.csv>`, :download:`data file 2 <../examples/solph/csv_reader/dispatch/scenarios/example_energy_system_seq.csv>`)
 * Investment example (:download:`source file <../examples/solph/csv_reader/investment/investment.py>`, :download:`data file 1 <../examples/solph/csv_reader/investment/data/nodes_flows.csv>`, :download:`data file 2 <../examples/solph/csv_reader/investment/data/nodes_flows_seq.csv>`).

.. _solph_examples_flex_label:

Flexible modelling
^^^^^^^^^^^^^^^^^^^^

It is also possible to pass constraints to the model that are not provided by solph but defined in your application.
Inside this example two different kind of constraints are added: (1) emission constraints, (2)
shared constraints between flows. To understand the example it might be useful to know a little bit about
the pyomo-package and how constraints are defined, moreover you should have understood the basic underlying oemof
structure. This example shows how to do it (:download:`source file <../examples/solph/flexible_modelling/add_constraints.py>`).

Dispatch modelling
^^^^^^^^^^^^^^^^^^^

Dispatch modelling is a typical thing to do with solph. However cost does not have to be monetary but can be emissions etc. In this example
a least cost dispatch of different generators that meet an inelastic demand is undertaken. Some of the generators are renewable energies with
marginal costs if zero. Additionally, it shows how combined heat and power units may be easily modelled as well.
(:download:`source file <../examples/solph/simple_dispatch/simple_dispatch.py>`, :download:`data file <../examples/solph/simple_dispatch/input_data.csv>`).

Storage investment
^^^^^^^^^^^^^^^^^^

The investment object can be used to optimise the capacity of a component. In this example all components are given but the electrical storage. The optimal size of the storage will be determined (:download:`source file <../examples/solph/storage_investment/storage_investment.py>`, :download:`data file <../examples/solph/storage_investment/storage_investment.csv>`).

.. _variable_chp_examples_label:

Variable chp
^^^^^^^^^^^^

This example is not a real use case of an energy system but an example to show how a variable combined heat and power plant (chp) works in contrast to a fixed chp (eg. block device).

.. 	image:: _files/example_variable_chp.svg
   :scale: 10 %
   :alt: example_variable_chp.svg
   :align: center

Both chp plants distribute power and heat to a separate heat and power Bus with a heat and power demand. The plot shows that the fixed chp plant produces heat and power excess and therefore needs more natural gas. (:download:`source file <../examples/solph/variable_chp/variable_chp.py>`, :download:`data file <../examples/solph/variable_chp/variable_chp.csv>`)
