.. _basic_concepts_components_label:

~~~~~~~~~~
Components
~~~~~~~~~~

The components are the core of the underlying network of the energy system. All component can be assigned a user-label when created. The user has to provide information regarding connections between busses and in/out of the component. A component which has only inputs defined is referred to as a *sink*. A component with only outputs is referred to as a *source*. A component with both input and outputs is a *converter*. These three very basic type of components are provided by the classes :ref:`oemof_solph_components_sink_label`, :ref:`oemof_solph_components_source_label` and :ref:`oemof_solph_components_converter_label`.

Components are divided in two categories. Well-tested components (:ref:`oemof_solph_components_label`) and experimental components (:ref:`oemof_experimental_components_label`), listed below

.. _oemof_solph_components_label:

Solph components
----------------

 * :ref:`oemof_solph_components_sink_label`
 * :ref:`oemof_solph_components_source_label`
 * :ref:`oemof_solph_components_converter_label`
 * :ref:`oemof_solph_components_generic_storage_label`
 * :ref:`oemof_solph_components_extraction_turbine_chp_label`
 * :ref:`oemof_solph_components_generic_chp_label`


.. _oemof_experimental_components_label:

Experimental components
-----------------------

The experimental section was created to lower the entry barrier to bring new components into oemof-solph. Be aware that these components might not be properly documented or even sometimes do not even work as intended. Let us know if you have successfully used and tested these components. This is the first step to move them to the regular components section.

 * :ref:`oemof_solph_custom_link_label`
 * :ref:`oemof_solph_components_generic_caes_label`
 * :ref:`oemof_solph_custom_electrical_line_label`
 * :ref:`oemof_solph_custom_sinkdsm_label`

.. _oemof_solph_components_sink_label:

Sink (basic)
^^^^^^^^^^^^

A sink is normally used to define the demand within an energy model but it can also be used to detect excesses.

The example shows the electricity demand of the electricity_bus defined above.
The *'my_demand_series'* should be sequence of normalised valueswhile the *'nominal_capacity'* is the maximum demand the normalised sequence is multiplied with.
Giving *'my_demand_series'* as parameter *'fix'* means that the demand cannot be changed by the solver.

.. code-block:: python

    solph.components.Sink(label='electricity_demand', inputs={electricity_bus: solph.flows.Flow(
        fix=my_demand_series, nominal_capacity=nominal_demand)})

In contrast to the demand sink the excess sink has normally less restrictions but is open to take the whole excess.

.. code-block:: python

    solph.components.Sink(label='electricity_excess', inputs={electricity_bus: solph.flows.Flow()})

.. note:: The Sink class is only a plug and provides no additional constraints or variables.


.. _oemof_solph_components_source_label:

Source (basic)
^^^^^^^^^^^^^^

A source can represent a pv-system, a wind power plant, an import of natural gas or a slack variable to avoid creating an in-feasible model.

While a wind power plant will have as feed-in depending on the weather conditions the natural_gas import might be restricted by maximum value (*nominal_capacity*) and an annual limit (*full_load_time_max*).
As we do have to pay for imported gas we should set variable costs.
Comparable to the demand series an *fix* is used to define a fixed the normalised output of a wind power plant.
Alternatively, you might use *max* to allow for easy curtailment.
The *nominal_capacity* sets the installed capacity.

.. code-block:: python

    solph.components.Source(
        label='import_natural_gas',
        outputs={my_energysystem.groups['natural_gas']: solph.flows.Flow(
            nominal_capacity=1000, full_load_time_max=1000000, variable_costs=50)})

    solph.components.Source(label='wind', outputs={electricity_bus: solph.flows.Flow(
        fix=wind_power_feedin_series, nominal_capacity=1000000)})

.. note:: The Source class is only a plug and provides no additional constraints or variables.

.. _oemof_solph_components_converter_label:

Converter (basic)
^^^^^^^^^^^^^^^^^

An instance of the Converter class can represent a node with multiple input and output flows such as a power plant, a transport line or any kind of a transforming process as electrolysis, a cooling device or a heat pump.
The efficiency has to be constant within one time step to get a linear transformation.
You can define a different efficiency for every time step (e.g. the thermal powerplant efficiency according to the ambient temperature) but this series has to be predefined and cannot be changed within the optimisation.

A condensing power plant can be defined by a converter with one input (fuel) and one output (electricity).

.. code-block:: python

    b_gas = solph.buses.Bus(label='natural_gas')
    b_el = solph.buses.Bus(label='electricity')

    solph.components.Converter(
        label="pp_gas",
        inputs={bgas: solph.flows.Flow()},
        outputs={b_el: solph.flows.Flow(nominal_capacity=10e10)},
        conversion_factors={electricity_bus: 0.58})

A CHP power plant would be defined in the same manner but with two outputs:

.. code-block:: python

    b_gas = solph.buses.Bus(label='natural_gas')
    b_el = solph.buses.Bus(label='electricity')
    b_th = solph.buses.Bus(label='heat')

    solph.components.Converter(
        label='pp_chp',
        inputs={b_gas: Flow()},
        outputs={b_el: Flow(nominal_capacity=30),
                 b_th: Flow(nominal_capacity=40)},
        conversion_factors={b_el: 0.3, b_th: 0.4})

A CHP power plant with 70% coal and 30% natural gas can be defined with two inputs and two outputs:

.. code-block:: python

    b_gas = solph.buses.Bus(label='natural_gas')
    b_coal = solph.buses.Bus(label='hard_coal')
    b_el = solph.buses.Bus(label='electricity')
    b_th = solph.buses.Bus(label='heat')

    solph.components.Converter(
        label='pp_chp',
        inputs={b_gas: Flow(), b_coal: Flow()},
        outputs={b_el: Flow(nominal_capacity=30),
                 b_th: Flow(nominal_capacity=40)},
        conversion_factors={b_el: 0.3, b_th: 0.4,
                            b_coal: 0.7, b_gas: 0.3})

A heat pump would be defined in the same manner. New buses are defined to make the code cleaner:

.. code-block:: python

    b_el = solph.buses.Bus(label='electricity')
    b_th_low = solph.buses.Bus(label='low_temp_heat')
    b_th_high = solph.buses.Bus(label='high_temp_heat')

    # The cop (coefficient of performance) of the heat pump can be defined as
    # a scalar or a sequence.
    cop = 3

    solph.components.Converter(
        label='heat_pump',
        inputs={b_el: Flow(), b_th_low: Flow()},
        outputs={b_th_high: Flow()},
        conversion_factors={b_el: 1/cop,
                            b_th_low: (cop-1)/cop})

If the low-temperature reservoir is nearly infinite (ambient air heat pump) the
low temperature bus is not needed and, therefore, a Converter with one input
is sufficient.

.. note:: See the :py:class:`~oemof.solph.components.converter.Converter` class for all parameters and the mathematical background.

.. _oemof_solph_components_extraction_turbine_chp_label:

ExtractionTurbineCHP (component)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :py:class:`~oemof.solph.components._extraction_turbine_chp.ExtractionTurbineCHP`
inherits from the :ref:`oemof_solph_components_converter_label` class. Like the name indicates,
the application example for the component is a flexible combined heat and power
(chp) plant. Of course, an instance of this class can represent also another
component with one input and two output flows and a flexible ratio between
these flows, with the following constraints:

.. include:: /../src/oemof/solph/components/_extraction_turbine_chp.py
  :start-after: _ETCHP-equations:
  :end-before: """

These constraints are applied in addition to those of a standard
:class:`~oemof.solph.components.Converter`. The constraints limit the range of
the possible operation points, like the following picture shows. For a certain
flow of fuel, there is a line of operation points, whose slope is defined by
the power loss factor :math:`\beta` (in some contexts also referred to as
:math:`C_v`). The second constraint limits the decrease of electrical power and
incorporates the backpressure coefficient :math:`C_b`.

.. 	figure:: /_files/ExtractionTurbine_range_of_operation.svg
   :alt: variable_chp_plot.svg
   :align: center
   :figclass: only-light

.. 	figure:: /_files/ExtractionTurbine_range_of_operation_darkmode.svg
   :alt: variable_chp_plot_darkmode.svg
   :align: center
   :figclass: only-dark

For now, :py:class:`~oemof.solph.components._extraction_turbine_chp.ExtractionTurbineCHP` instances must
have one input and two output flows. The class allows the definition
of a different efficiency for every time step that can be passed as a series
of parameters that are fixed before the optimisation. In contrast to the
:py:class:`~oemof.solph.components.Converter`, a main flow and a tapped flow is
defined. For the main flow you can define a separate conversion factor that
applies when the second flow is zero (*`conversion_factor_full_condensation`*).

.. code-block:: python

    solph.components._extractionTurbineCHP(
        label='variable_chp_gas',
        inputs={b_gas: solph.flows.Flow(nominal_capacity=10e10)},
        outputs={b_el: solph.flows.Flow(), b_th: solph.flows.Flow()},
        conversion_factors={b_el: 0.3, b_th: 0.5},
        conversion_factor_full_condensation={b_el: 0.5})

The key of the parameter *'conversion_factor_full_condensation'* defines which
of the two flows is the main flow. In the example above, the flow to the Bus
*'b_el'* is the main flow and the flow to the Bus *'b_th'* is the tapped flow.
The following plot shows how the variable chp (right) schedules it's electrical
and thermal power production in contrast to a fixed chp (left). The plot is the
output of an example in the `example directory
<https://github.com/oemof/oemof-solph/tree/dev/examples>`_.

.. 	figure:: /_files/variable_chp_plot.svg
   :scale: 10%
   :alt: variable_chp_plot.svg
   :align: center

.. note:: See the :py:class:`~oemof.solph.components._extraction_turbine_chp.ExtractionTurbineCHP` class for all parameters and the mathematical background.


.. _oemof_solph_components_generic_chp_label:

GenericCHP (component)
^^^^^^^^^^^^^^^^^^^^^^

With the GenericCHP class it is possible to model different types of CHP plants (combined cycle extraction turbines,
back pressure turbines and motoric CHP), which use different ranges of operation, as shown in the figure below.

.. 	figure:: /_files/GenericCHP.svg
   :scale: 70 %
   :alt: scheme of GenericCHP operation range
   :align: center
   :figclass: only-light

.. 	figure:: /_files/GenericCHP_darkmode.svg
   :scale: 70 %
   :alt: scheme of GenericCHP operation range
   :align: center
   :figclass: only-dark

Combined cycle extraction turbines: The minimal and maximal electric power without district heating
(red dots in the figure) define maximum load and minimum load of the plant. Beta defines electrical power loss through
heat extraction. The minimal thermal condenser load to cooling water and the share of flue gas losses
at maximal heat extraction determine the right boundary of the operation range.

.. code-block:: python

    solph.components.GenericCHP(
        label='combined_cycle_extraction_turbine',
        fuel_input={bgas: solph.flows.Flow(
            H_L_FG_share_max=[0.19 for p in range(0, periods)])},
        electrical_output={bel: solph.flows.Flow(
            P_max_woDH=[200 for p in range(0, periods)],
            P_min_woDH=[80 for p in range(0, periods)],
            Eta_el_max_woDH=[0.53 for p in range(0, periods)],
            Eta_el_min_woDH=[0.43 for p in range(0, periods)])},
        heat_output={bth: solph.flows.Flow(
            Q_CW_min=[30 for p in range(0, periods)])},
        Beta=[0.19 for p in range(0, periods)],
        back_pressure=False)

For modeling a back pressure CHP, the attribute `back_pressure` has to be set to True.
The ratio of power and heat production in a back pressure plant is fixed, therefore the operation range
is just a line (see figure). Again, the `P_min_woDH`  and `P_max_woDH`, the efficiencies at these points and the share of flue
gas losses at maximal heat extraction have to be specified. In this case “without district heating” is not to be taken
literally since an operation without heat production is not possible. It is advised to set `Beta` to zero, so the minimal and
maximal electric power without district heating are the same as in the operation point (see figure). The minimal
thermal condenser load to cooling water has to be zero, because there is no condenser besides the district heating unit.


.. code-block:: python

    solph.components.GenericCHP(
        label='back_pressure_turbine',
        fuel_input={bgas: solph.flows.Flow(
            H_L_FG_share_max=[0.19 for p in range(0, periods)])},
        electrical_output={bel: solph.flows.Flow(
            P_max_woDH=[200 for p in range(0, periods)],
            P_min_woDH=[80 for p in range(0, periods)],
            Eta_el_max_woDH=[0.53 for p in range(0, periods)],
            Eta_el_min_woDH=[0.43 for p in range(0, periods)])},
        heat_output={bth: solph.flows.Flow(
            Q_CW_min=[0 for p in range(0, periods)])},
        Beta=[0 for p in range(0, periods)],
        back_pressure=True)

A motoric chp has no condenser, so `Q_CW_min` is zero. Electrical power does not depend on the amount of heat used
so `Beta` is zero. The minimal and maximal electric power (without district heating) and the efficiencies at these
points are needed, whereas the use of electrical power without using thermal energy is not possible.
With `Beta=0` there is no difference between these points and the electrical output in the operation range.
As a consequence of the functionality of a motoric CHP, share of flue gas losses at maximal heat extraction but also
at minimal heat extraction have to be specified.


.. code-block:: python

    solph.components.GenericCHP(
        label='motoric_chp',
        fuel_input={bgas: solph.flows.Flow(
            H_L_FG_share_max=[0.18 for p in range(0, periods)],
            H_L_FG_share_min=[0.41 for p in range(0, periods)])},
        electrical_output={bel: solph.flows.Flow(
            P_max_woDH=[200 for p in range(0, periods)],
            P_min_woDH=[100 for p in range(0, periods)],
            Eta_el_max_woDH=[0.44 for p in range(0, periods)],
            Eta_el_min_woDH=[0.40 for p in range(0, periods)])},
        heat_output={bth: solph.flows.Flow(
            Q_CW_min=[0 for p in range(0, periods)])},
        Beta=[0 for p in range(0, periods)],
        back_pressure=False)

Modeling different types of plants means telling the component to use different constraints. Constraint 1 to 9
are active in all three cases. Constraint 10 depends on the attribute back_pressure. If true, the constraint is
an equality, if not it is a less or equal. Constraint 11 is only needed for modeling motoric CHP which is done by
setting the attribute `H_L_FG_share_min`.

.. include:: /../src/oemof/solph/components/_generic_chp.py
  :start-after: _GenericCHP-equations1-10:
  :end-before: **For the attribute**

If :math:`\dot{H}_{L,FG,min}` is given, e.g. for a motoric CHP:

.. include:: /../src/oemof/solph/components/_generic_chp.py
  :start-after: _GenericCHP-equations11:
  :end-before: """

.. note:: See the :py:class:`~oemof.solph.components._generic_chp.GenericCHP` class for all parameters and the mathematical background.


.. _oemof_solph_components_generic_storage_label:

GenericStorage (component)
^^^^^^^^^^^^^^^^^^^^^^^^^^

A component to model a storage with its basic characteristics. The
GenericStorage is designed for one input and one output.
The ``nominal_storage_capacity`` of the storage signifies the storage capacity. You can either set it to the net capacity or to the gross capacity and limit it using the min/max attribute.
To limit the input and output flows, you can define the ``nominal_capacity`` in the Flow objects.
Furthermore, an efficiency for loading, unloading and a loss rate can be defined.

.. code-block:: python

    solph.components.GenericStorage(
        label='storage',
        inputs={b_el: solph.flows.Flow(nominal_capacity=9, variable_costs=10)},
        outputs={b_el: solph.flows.Flow(nominal_capacity=25, variable_costs=10)},
        loss_rate=0.001, nominal_capacity=50,
        inflow_conversion_factor=0.98, outflow_conversion_factor=0.8)

For initialising the state of charge before the first time step (time step zero) the parameter ``initial_storage_level`` (default value: ``None``) can be set by a numeric value as fraction of the storage capacity.
Additionally the parameter ``balanced`` (default value: ``True``) sets the relation of the state of charge of time step zero and the last time step.
If ``balanced=True``, the state of charge in the last time step is equal to initial value in time step zero.
Use ``balanced=False`` with caution as energy might be added to or taken from the energy system due to different states of charge in time step zero and the last time step.
Generally, with these two parameters four configurations are possible, which might result in different solutions of the same optimization model:

    *	``initial_storage_level=None``, ``balanced=True`` (default setting): The state of charge in time step zero is a result of the optimization. The state of charge of the last time step is equal to time step zero. Thus, the storage is not violating the energy conservation by adding or taking energy from the system due to different states of charge at the beginning and at the end of the optimization period.
    *	``initial_storage_level=0.5``, ``balanced=True``: The state of charge in time step zero is fixed to 0.5 (50 % charged). The state of charge in the last time step is also constrained by 0.5 due to the coupling parameter ``balanced`` set to ``True``.
    *	``initial_storage_level=None``, ``balanced=False``: Both, the state of charge in time step zero and the last time step are a result of the optimization and not coupled.
    *	``initial_storage_level=0.5``, ``balanced=False``: The state of charge in time step zero is constrained by a given value. The state of charge of the last time step is a result of the optimization.

The following code block shows an example of the storage parametrization for the second configuration:

.. code-block:: python

    solph.components.GenericStorage(
        label='storage',
        inputs={b_el: solph.flows.Flow(nominal_capacity=9, variable_costs=10)},
        outputs={b_el: solph.flows.Flow(nominal_capacity=25, variable_costs=10)},
        loss_rate=0.001, nominal_capacity=50,
        initial_storage_level=0.5, balanced=True,
        inflow_conversion_factor=0.98, outflow_conversion_factor=0.8)

If you want to view the temporal course of the state of charge of your storage
after the optimisation, you need to check the ``storage_content`` in the results:

.. code-block:: python

    from oemof.solph import processing, views
    results = processing.results(om)
    column_name = (('your_storage_label', 'None'), 'storage_content')
    SC = views.node(results, 'your_storage_label')['sequences'][column_name]

The ``storage_content`` is the absolute value of the current stored energy.
By calling:

.. code-block:: python

    views.node(results, 'your_storage_label')['scalars']

you get the results of the scalar values of your storage, e.g. the initial
storage content before time step zero (``init_content``).

For more information see the definition of the  :py:class:`~oemof.solph.components._generic_storage.GenericStorage` class or check the :ref:`examples_label`.


Using an investment object with the GenericStorage component
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Based on the `GenericStorage` object the `GenericInvestmentStorageBlock` adds two main investment possibilities.

    *	Invest into the flow parameters e.g. a turbine or a pump
    *	Invest into capacity of the storage  e.g. a basin or a battery cell

Investment in this context refers to the value of the variable for the 'nominal_capacity' (installed capacity) in the investment mode.

As an addition to other flow-investments, the storage class implements the possibility to couple or decouple the flows
with the capacity of the storage.
Three parameters are responsible for connecting the flows and the capacity of the storage:

    *	``invest_relation_input_capacity`` fixes the input flow investment to the capacity investment. A ratio of 1 means that the storage can be filled within one time-period.
    *	``invest_relation_output_capacity`` fixes the output flow investment to the capacity investment. A ratio of 1 means that the storage can be emptied within one period.
    *	``invest_relation_input_output`` fixes the input flow investment to the output flow investment. For values <1, the input will be smaller and for values >1 the input flow will be larger.

You should not set all 3 parameters at the same time, since it will lead to overdetermination.

The following example pictures a Pumped Hydroelectric Energy Storage (PHES). Both flows and the storage itself (representing: pump, turbine, basin) are free in their investment. You can set the parameters to `None` or delete them as `None` is the default value.

.. code-block:: python

    solph.components.GenericStorage(
        label='PHES',
        inputs={b_el: solph.flows.Flow(nominal_capacity=solph.Investment(ep_costs=500))},
        outputs={b_el: solph.flows.Flow(nominal_capacity=solph.Investment(ep_costs=500)},
        loss_rate=0.001,
        inflow_conversion_factor=0.98, outflow_conversion_factor=0.8),
        investment = solph.Investment(ep_costs=40))

The following example describes a battery with flows coupled to the capacity of the storage.

.. code-block:: python

    solph.components.GenericStorage(
        label='battery',
        inputs={b_el: solph.flows.Flow()},
        outputs={b_el: solph.flows.Flow()},
        loss_rate=0.001,
        inflow_conversion_factor=0.98,
         outflow_conversion_factor=0.8,
        invest_relation_input_capacity = 1/6,
        invest_relation_output_capacity = 1/6,
        investment = solph.Investment(ep_costs=400))


.. note:: See the :py:class:`~oemof.solph.components._generic_storage.GenericStorage` class for all parameters and the mathematical background.


.. _oemof_solph_custom_link_label:

Link (experimental)
^^^^^^^^^^^^^^^^^^^

The `Link` allows to model connections between two busses, e.g. modeling the transshipment of electric energy between two regions.

.. note:: See the :py:class:`~oemof.solph.components.experimental._link.Link` class for all parameters and the mathematical background.



OffsetConverter (component)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The `OffsetConverter` object makes it possible to create a Converter with efficiencies depending on the part load condition.
For this it is necessary to define one flow as a nonconvex flow and to set a minimum load.
The following example illustrates how to define an OffsetConverter for given
information for an output, i.e. a combined heat and power plant. The plant
generates up to 100 kW electric energy at an efficiency of 40 %. In minimal
load the electric efficiency is at 30 %, and the minimum possible load is 50 %
of the nominal load. At the same time, heat is produced with a constant
efficiency. By using the `OffsetConverter` a linear relation of in- and output
power with a power dependent efficiency is generated.

.. code-block:: python

    >>> from oemof import solph

    >>> eta_el_min = 0.3                  # electrical efficiency at minimal operation point
    >>> eta_el_max = 0.4                  # electrical efficiency at nominal operation point
    >>> eta_th_min = 0.5                  # thermal efficiency at minimal operation point
    >>> eta_th_max = 0.5                  # thermal efficiency at nominal operation point
    >>> P_out_min = 20                    # absolute minimal output power
    >>> P_out_max = 100                   # absolute nominal output power

As reference for our system we use the input and will mark that flow as
nonconvex respectively. The efficiencies for electricity and heat output have
therefore to be defined with respect to the input flow. The same is true for
the minimal and maximal load. Therefore, we first calculate the minimum and
maximum input of fuel and then derive the slope and offset for both outputs.

.. code-block:: python

    >>> P_in_max = P_out_max / eta_el_max
    >>> P_in_min = P_out_min / eta_el_min
    >>> P_in_max
    250.0
    >>> round(P_in_min, 2)
    66.67

With that information, we can derive the normed minimal and maximal load of the
nonconvex flow, and calculate the slope and the offset for both outputs. Note,
that the offset for the heat output is 0, because the thermal heat output
efficiency is constant.

.. code-block:: python

    >>> l_max = 1
    >>> l_min = P_in_min / P_in_max
    >>> slope_el, offset_el = solph.components.slope_offset_from_nonconvex_input(
    ...     l_max, l_min, eta_el_max, eta_el_min
    ... )
    >>> slope_th, offset_th = solph.components.slope_offset_from_nonconvex_input(
    ...     l_max, l_min, eta_th_max, eta_th_min
    ... )
    >>> round(slope_el, 3)
    0.436
    >>> round(offset_el, 3)
    -0.036
    >>> round(slope_th, 3)
    0.5
    >>> round(offset_th, 3)
    0.0

Then we can create our component with the buses attached to it.

.. code-block:: python

    >>> bfuel = solph.Bus("fuel")
    >>> bel = solph.Bus("electricity")
    >>> bth = solph.Bus("heat")

    # define OffsetConverter
    >>> diesel_genset = solph.components.OffsetConverter(
    ...     label='boiler',
    ...     inputs={
    ...         bfuel: solph.flows.Flow(
    ...             nominal_capacity=P_out_max,
    ...             max=l_max,
    ...             min=l_min,
    ...             nonconvex=solph.NonConvex()
    ...         )
    ...     },
    ...     outputs={
    ...         bel: solph.flows.Flow(),
    ...         bth: solph.flows.Flow(),
    ...     },
    ...     conversion_factors={bel: slope_el, bth: slope_th},
    ...     normed_offsets={bel: offset_el, bth: offset_th},
    ... )

.. note::

    One of the inputs and outputs has to be a `NonConvex` flow and this flow
    will serve as the reference for the `conversion_factors` and the
    `normed_offsets`. The `NonConvex` flow also holds

    - the `nominal_capacity` (can be `Investment` in case of investment optimization),
    - the `min` and
    - the `max` attributes.

    The `conversion_factors` and `normed_offsets` are specified similar to the
    `Converter` API with dictionaries referencing the respective input and
    output buses. Note, that you cannot have the `conversion_factors` or
    `normed_offsets` point to the `NonConvex` flow.

The following figures show the power at the electrical and the thermal output
and the resepctive ratios to the nonconvex flow (normalized). The efficiency
becomes non-linear.

.. 	figure:: /_files/OffsetConverter_relations_1.svg
   :width: 70 %
   :alt: OffsetConverter_relations_1.svg
   :align: center

.. 	figure:: /_files/OffsetConverter_relations_2.svg
   :width: 70 %
   :alt: OffsetConverter_relations_2.svg
   :align: center

.. math::

    \eta = P(t) / P_\text{ref}(t)

It also becomes clear, why the component has been named `OffsetConverter`. The
linear equation of inflow to electrical outflow does not hit the origin, but is
offset. By multiplying the offset :math:`y_\text{0,normed}` with the binary
status variable of the `NonConvex` flow, the origin (0, 0) becomes part of the
solution space and the boiler is allowed to switch off.

.. include:: /../src/oemof/solph/components/_offset_converter.py
  :start-after: _OffsetConverter-equations:
  :end-before: """

The parameters :math:`y_\text{0,normed}` and :math:`m` can be given by scalars or by series in order to define a different efficiency equation for every timestep.
It is also possible to define multiple outputs.

.. note:: See the :py:class:`~oemof.solph.components._offset_converter.OffsetConverter` class for all parameters and the mathematical background.


.. _oemof_solph_custom_electrical_line_label:

ElectricalLine (experimental)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Electrical line.

.. note:: See the :py:class:`~oemof.solph.flows.experimental._electrical_line.ElectricalLine` class for all parameters and the mathematical background.


.. _oemof_solph_components_generic_caes_label:

GenericCAES (experimental)
^^^^^^^^^^^^^^^^^^^^^^^^^^

Compressed Air Energy Storage (CAES).
The following constraints describe the CAES:

.. include:: /../src/oemof/solph/components/experimental/_generic_caes.py
  :start-after: _GenericCAES-equations:
  :end-before: """

.. note:: See the :py:class:`~oemof.solph.components.experimental._generic_caes.GenericCAES` class for all parameters and the mathematical background.


.. _oemof_solph_custom_sinkdsm_label:

SinkDSM (experimental)
^^^^^^^^^^^^^^^^^^^^^^

:class:`~oemof.solph.custom.sink_dsm.SinkDSM` can used to represent flexibility in a demand time series.
It can represent both, load shifting or load shedding.
For load shifting, elasticity of the demand is described by upper (`~oemof.solph.custom.sink_dsm.SinkDSM.capacity_up`) and lower (`~oemof.solph.custom.SinkDSM.capacity_down`) bounds where within the demand is allowed to vary.
Upwards shifted demand is then balanced with downwards shifted demand.
For load shedding, shedding capability is described by `~oemof.solph.custom.SinkDSM.capacity_down`.
It both, load shifting and load shedding are allowed, `~oemof.solph.custom.SinkDSM.capacity_down` limits the sum of both downshift categories.

:class:`~oemof.solph.custom.sink_dsm.SinkDSM` provides three approaches how the Demand-Side Management (DSM) flexibility is represented in constraints
It can be used for both, dispatch and investments modeling.

* "DLR": Implementation of the DSM modeling approach from by Gils (2015): `Balancing of Intermittent Renewable Power Generation by Demand Response and Thermal Energy Storage, Stuttgart, <https://doi.org/10.18419/opus-6888>`_,
  Details: :class:`~oemof.solph.custom.sink_dsm.SinkDSMDLRBlock` and :class:`~oemof.solph.custom.sink_dsm.SinkDSMDLRInvestmentBlock`
* "DIW": Implementation of the DSM modeling approach by Zerrahn & Schill (2015): `On the representation of demand-side management in power system models <https://doi.org/10.1016/j.energy.2015.03.037>`_,
  in: Energy (84), pp. 840-845, 10.1016/j.energy.2015.03.037. Details: :class:`~oemof.solph.custom.sink_dsm.SinkDSMDIWBlock` and :class:`~oemof.solph.custom.sink_dsm.SinkDSMDIWInvestmentBlock`
* "oemof": Is a fairly simple approach. Within a defined windows of time steps, demand can be shifted within the defined bounds of elasticity.
  The window sequentially moves forwards. Details: :class:`~oemof.solph.custom.sink_dsm.SinkDSMOemofBlock` and :class:`~oemof.solph.custom.sink_dsm.SinkDSMOemofInvestmentBlock`

Cost can be associated to either demand up shifts or demand down shifts or both.

This small example of PV, grid and SinkDSM shows how to use the component

.. code-block:: python

    # Create some data
    pv_day = [(-(1 / 6 * x ** 2) + 6) / 6 for x in range(-6, 7)]
    pv_ts = [0] * 6 + pv_day + [0] * 6
    data_dict = {"demand_el": [3] * len(pv_ts),
                 "pv": pv_ts,
                 "Cap_up": [0.5] * len(pv_ts),
                 "Cap_do": [0.5] * len(pv_ts)}
    data = pd.DataFrame.from_dict(data_dict)

    # Do timestamp stuff
    datetimeindex = pd.date_range(start='1/1/2013', periods=len(data.index), freq='h')
    data['timestamp'] = datetimeindex
    data.set_index('timestamp', inplace=True)

    # Create Energy System
    es = solph.EnergySystem(timeindex=datetimeindex)

    # Create bus representing electricity grid
    b_elec = solph.buses.Bus(label='Electricity bus')
    es.add(b_elec)

    # Create a back supply
    grid = solph.components.Source(label='Grid',
                        outputs={
                            b_elec: solph.flows.Flow(
                                nominal_capacity=10000,
                                variable_costs=50)}
                        )
    es.add(grid)

    # PV supply from time series
    s_wind = solph.components.Source(label='wind',
                          outputs={
                              b_elec: solph.flows.Flow(
                                  fix=data['pv'],
                                  nominal_capacity=3.5)}
                          )
    es.add(s_wind)

    # Create DSM Sink
    demand_dsm = solph.custom.SinkDSM(label="DSM",
                                      inputs={b_elec: solph.flows.Flow()},
                                      demand=data['demand_el'],
                                      capacity_up=data["Cap_up"],
                                      capacity_down=data["Cap_do"],
                                      delay_time=6,
                                      max_demand=1,
                                      max_capacity_up=1,
                                      max_capacity_down=1,
                                      approach="DIW",
                                      cost_dsm_down=5)
    es.add(demand_dsm)

Yielding the following results

..  figure:: /_files/Plot_delay_2013-01-01.svg
   :width: 85 %
   :alt: Plot_delay_2013-01-01.svg
   :align: center


.. note::
    * Keyword argument `method` from v0.4.1 has been renamed to `approach` in v0.4.2 and methods have been renamed.
    * The parameters `demand`, `capacity_up` and `capacity_down` have been normalized to allow investments modeling. To retreive the original dispatch behaviour from v0.4.1, set `max_demand=1`, `max_capacity_up=1`, `max_capacity_down=1`.
    * This component is a candidate component. It's implemented as a custom component for users that like to use and test the component at early stage. Please report issues to improve the component.
    * See the :py:class:`~oemof.solph.custom.sink_dsm.SinkDSM` class for all parameters and the mathematical background.
