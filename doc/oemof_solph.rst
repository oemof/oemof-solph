.. _oemof_solph_label:

~~~~~~~~~~~
oemof-solph
~~~~~~~~~~~

Solph is an oemof-package, designed to create and solve linear or mixed-integer
linear optimization problems. The packages is based on pyomo. To get started
with solph, checkout the solph-examples in the `oemof/examples/solph` directory.

.. contents::
    :depth: 2
    :local:
    :backlinks: top


How can I use solph?
--------------------

To use solph you have to install oemof and at least one solver, that can be used together with pyomo. See `pyomo installation guide <https://software.sandia.gov/downloads/pub/pyomo/PyomoInstallGuide.html#Solvers>`_. You can test it by executing one of the existing examples. Be aware that the examples require the CBC solver but you can change the solver name in the example files to your solver.

Once the example work you are close to your first energy model.

Set up an energy system
^^^^^^^^^^^^^^^^^^^^^^^

In most cases an EnergySystem object is defined when we start to build up an energy system model. The EnergySystem object will be the main container for the model.

To define an EnergySystem we need a Datetime index to define the time range and increment of our model. An easy way to this is to use the pandas time_range function. the following code example defines the year 2011 in hourly steps. See `pandas date_range guide <http://pandas.pydata.org/pandas-docs/stable/generated/pandas.date_range.html>`_ for more information.

.. code-block:: python

    import pandas as pd
    my_index = pd.date_range('1/1/2011', periods=8760, freq='H')

This index can be used to define the EnergySystem:

.. code-block:: python

    import oemof.solph as solph
    my_energysystem = solph.EnergySystem(time_idx=my_index)

Now you can start to add the components of the network.


Add your components to the energy system
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have defined an instance of the EnergySystem class all components you define will automatically added to your EnergySystem.

Basically there are four types of Nodes and every node has to be connected with one or more buses. The connection between a component and a bus is the flow.

 * Sink (one input, no output)
 * Source (one output, no input)
 * Linear_Transformer (one input, n outputs)
 * Storage (one input, one output)

Using these types it is already possible to set up an simple energy model but more types (e.g. flexible CHP transformer) are being developed. You can add your own types in your application (see below) but we would be pleased to integrate them into solph if they are of general interest.

.. 	image:: _files/oemof_solph_example.svg
   :scale: 10 %
   :alt: alternate text
   :align: center

the figure shows a simple energy system using the four basic network classes and the Bus class. If you remove the transmission line (transport 1 and transport 2) you get two systems but they are still one energy system in terms of solph and will be optimised at once.

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
.. note:: See the :py:class:`~oemof.solph.blocks.Bus` block for all information about the mathematical background.


Flow
++++

The flow class has to be used to connect. An instance of the Flow class is normally used in combination with the definition of a component. A Flow can be limited by upper and lower bounds (constant or time-dependent) or by summarised limits. For all parameters see the API documentation of the :py:class:`~oemof.solph.network.Flow` class or the examples of the nodes below. A basic flow can be defined without any parameter.

.. code-block:: python

    solph.Flow()

.. note:: See the :py:class:`~oemof.solph.blocks.Flow` block for all information about the mathematical background.


Sink
++++

A sink is normally used to define the demand within an energy model but it can also be used to detect excesses.

The example shows the electricity demand of the electricity_bus defined above. The *'my_demand_series'* should be sequence of normalised values while the *'nominal_value'* is the maximum demand the normalised sequence is multiplied with. The parameter *'fixed=True'* means that the actual_value can not be changed by the solver.

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

While a wind power plant will have an hourly feed-in depending on the weather conditions the natural_gas import might be restricted by maximum value (*nominal_value*) and an annual limit (*summed_max*). As we do have to pay for imported gas we should set variable costs. Comparable to the demand series an *actual_value* in combination with *'fixed=True'* is used to define the normalised output of a wind power plan. The *nominal_value* sets the installed capacity.

.. code-block:: python

    solph.Source(
        label='import_natural_gas',
        outputs={my_energsystem.groups['natural_gas']: solph.Flow(
            nominal_value=1000, summed_max=1000000, variable_costs=50)})

    solph.Source(label='wind', outputs={electricity_bus: solph.Flow(
        actual_value=wind_power_feedin_series, nominal_value=1000000, fixed=True)})

.. note:: The Source class is only a plug and provides no additional constraints or variables.


LinearTransformer
+++++++++++++++++

An instance of the LinearTransformer class can represent a power plant, a transport line or any kind of a transforming process as electrolysis or a cooling device. As the name indicates the efficiency has to constant within one time step to get a linear transformation. You can define a different efficiency for every time step (e.g. the COP of an air heat pump according to the ambient temperature) but this series has to be predefined and cannot be changed within the optimisation.

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

.. note:: See the :py:class:`~oemof.solph.blocks.LinearTransformer` block for all information about the mathematical background.


Storage
+++++++

In contrast to the three classes above the storage class is a pure solph class and is not inherited from the oemof-network module. The *nominal_value* of the storage signifies the nominal capacity. To limit the input and output flows you can define the ratio between these flows and the capacity using *nominal_input_capacity_ratio* and *nominal_output_capacity_ratio*. Furthermore an efficiency for loading, unloading and a capacity loss per time increment can be defined. For more information see the definition of the  :py:class:`~oemof.solph.network.Storage` class.

.. code-block:: python

    solph.Storage(
        label='storage',
        inputs={b_el: solph.Flow(variable_costs=10)},
        outputs={b_el: solph.Flow(variable_costs=10)},
        capacity_loss=0.001, nominal_value=50,
        nominal_input_capacity_ratio=1/6,
        nominal_output_capacity_ratio=1/6,
        inflow_conversion_factor=0.98, outflow_conversion_factor=0.8)

.. note:: See the :py:class:`~oemof.solph.blocks.Storage` block for all information about the mathematical background.



.. _oemof_solph_optimise_es_label:

Optimise your energy system

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The typical optimisation of a energy system in solph is the dispatch optimisation which means that the use of the sources is optimised to satisfy the demand. Therefore variable cost can be defined for all components. The cost for gas should be defined in the gas source while the variable costs of the gas power plant are caused by operating material. You can deviate from this scheme but you should keep it consistent to make it understandable for others.

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

If you want to analyse your results, you should first dump you EnergySystem instance, otherwise you have to run the simulation ever again.

.. code-block:: python

    my_energysystem.dump('my_path', 'my_dump.oemof')

To restore the dump you can simply create an EnergySystem instance and restore your dump into it.

.. code-block:: python

    import pandas as pd
    import oemof.solph as solph
    my_index = pd.date_range('1/1/2011', periods=8760, freq='H')
    new_energysystem = solph.EnergySystem(time_idx=my_index)
    new_energysystem.restore('my_path', 'my_dump.oemof')

If you call dump/restore with any parameters, the dump will be stored as *'es_dump.oemof'* into the *'.oemof/dumps/'* folder created in your HOME directory.

In the outputlib the results will be converted to a pandas MultiIndex DataFrame. This makes it easy to plot, save or process the results. See :ref:`oemof_outputlib_label` for more information.


.. _investment_mode_label:

Using the investment mode
-------------------------


As described in :ref:`oemof_solph_optimise_es_label` the typical way to optimise an energy system is the dispatch optimisation based on marginal costs. Solph also provides a combined dispatch and investment optimisation. Based on investment costs you can compare the usage of existing components against building up new capacity. The annual savings by building up new capacity has therefore compensate the annuity of the investment costs (the time period does not have to be on year but depends on your Datetime index).

See the API of the :py:class:`~oemof.solph.options.Investment` class to see all possible parameters.

Basically an instance of the investment class can be added to a Flow or a Storage. Adding an investment object the *nominal_value* or *nominal_capacity* should not be set. All parameters the usually refer to the *nominal_value/capacity* will now refer to the investment variable. There it is still possible to set bounds depending on the capacity that will be build.

For example if you want to find out what would be the optimal capacity of a wind power plant to decrease the costs of an existing energy system you can define this model and add an investment source. The *wind_power_time_series* has to be a normalised feed-in time series of you wind power plant.

.. code-block:: python

    solph.Source(label='new_wind_pp', outputs={electricity: solph.Flow(
        actual_value=wind_power_time_series, fixed=True,
	investment=solph.Investment(ep_costs=epc))})

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
For now, you have to check out the examples in the directory
exmaples/solph/flexible_modelling.



Mathematical description of solph
------------------------------------

To get the the mathematical equations you have to check out the docstrings
of the classes in the modules: :py:mod:`~oemof.solph.blocks` and
:py:mod:`~oemof.solph.models`.


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
