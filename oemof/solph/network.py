# -*- coding: utf-8 -*-
"""

"""
import warnings
import oemof.network as on
import oemof.energy_system as es
from .options import Investment
from .plumbing import sequence


class EnergySystem(es.EnergySystem):
    """
    A variant of :class:`EnergySystem <oemof.core.energy_system.EnergySystem>`
    specially tailored to solph.

    In order to work in tandem with solph, instances of this class always use
    :const:`solph.GROUPINGS <oemof.solph.GROUPINGS>`. If custom groupings are
    supplied via the `groupings` keyword argument, :const:`solph.GROUPINGS
    <oemof.solph.GROUPINGS>` is prepended to those.

    If you know what you are doing and want to use solph without
    :const:`solph.GROUPINGS <oemof.solph.GROUPINGS>`, you can just use
    :class:`core's EnergySystem <oemof.core.energy_system.EnergySystem>`
    directly.
    """

    def __init__(self, **kwargs):
        # Doing imports at runtime is generally frowned upon, but should work
        # for now. See the TODO in :func:`constraint_grouping
        # <oemof.solph.groupings.constraint_grouping>` for more information.
        from . import GROUPINGS
        kwargs['groupings'] = GROUPINGS + kwargs.get('groupings', [])
        super().__init__(**kwargs)


class Flow:
    """
    Define a flow between two nodes. Note: Some attributes can only take
    numeric scalar as some may either take scalar or sequences (array-like).
    If for latter a scalar is passed, this will be internally converted to a
    sequence.

    Parameters
    ----------
    nominal_value : numeric
        The nominal value of the flow. If this value is set the corresponding
        optimization variable of the flow object will be bounded by this value
        multiplied with min(lower bound)/max(upper bound).
    min : numeric (sequence or scalar)
        Normed minimum value of the flow. The flow absolute maximum will be
        calculated by multiplying :attr:`nominal_value` with :attr:`min`
    max : numeric (sequence or scalar)
        Nominal maximum value of the flow. (see. :attr:`min`)
    actual_value: numeric (sequence or scalar)
        Specific value for the flow variable. Will be multiplied with the
        nominal\_value to get the absolute value. If fixed attr is set to True
        the flow variable will be fixed to actual_value * :attr:`nominal_value`
        , I.e. this value is set exogenous.
    positive_gradient : numeric (sequence or scalar)
        The normed maximal positive difference (flow[t-1] < flow[t])
        of two consecutive flow values.
    negative_gradient : numeric (sequence or scalar)
        The normed maximum negative difference (from[t-1] > flow[t]) of two
        consecutive timesteps.
    summed_max : numeric
        Specific maximum value summed over all timesteps. Will be multiplied
        with the nominal_value to get the absolute limit.
    summed_min : numeric
        see above
    variable_costs : numeric (sequence or scalar)
        The costs associated with one unit of the flow. If this is set the
        costs will be added to the objective expression of the optimization
        problem.
    fixed_costs : numeric
        The costs of the whole period associated with the absolute
        nominal_value of the flow.
    fixed : boolean
        Boolean value indicating if a flow is fixed during the optimization
        problem to its ex-ante set value. Used in combination with the
        :attr:`actual_value`.
    investment : :class:`oemof.solph.options.Investment` object
        Object indicating if a nominal_value of the flow is determined by
        the optimization problem. Note: This will refer all attributes to an
        investment variable instead of to the nominal_value. The nominal_value
        should not be set (or set to None) if an investment object is used.
    binary :  :class:`oemof.solph.options.BinaryFlow` object
        If an binary flow object is added here, the flow constraints will
        be altered significantly as the mathematical model for the flow
        will be different, i.e. constraint etc from
        :class:`oemof.solph.blocks.BinaryFlow` will be used instead of
        :class:`oemof.solph.blocks.Flow`. Note: this does not work in
        combination with the investment attribute set at the moment.

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.Flow`
     * :py:class:`~oemof.solph.blocks.InvestmentFlow` (additionally if
       Investment object is present)
     * :py:class:`~oemof.solph.blocks.BinaryFlow` (If
        binary  object is present, CAUTION: replaces
        :py:class:`~oemof.solph.blocks.Flow` class)

    Examples
    --------
    Creating a fixed flow object:

    >>> f = Flow(actual_value=[10, 4, 4], fixed=True, variable_costs=5)
    >>> f.variable_costs[2]
    5
    >>> f.actual_value[2]
    4

    Creating a flow object with time-depended lower and upper bounds:

    >>> f1 = Flow(min=[0.2, 0.3], max=0.99, nominal_value=100)
    >>> f1.max[1]
    0.99

    """
    def __init__(self, **kwargs):
        # TODO: Check if we can inherit from pyomo.core.base.var _VarData
        # then we need to create the var object with
        # pyomo.core.base.IndexedVarWithDomain before any Flow is created.
        # E.g. create the variable in the energy system and populate with
        # information afterwards when creating objects.

        self.nominal_value = kwargs.get('nominal_value')
        self.min = sequence(kwargs.get('min', 0))
        self.max = sequence(kwargs.get('max', 1))
        self.actual_value = sequence(kwargs.get('actual_value'))
        self.positive_gradient = sequence(kwargs.get('positive_gradient'))
        self.negative_gradient = sequence(kwargs.get('negative_gradient'))
        self.variable_costs = sequence(kwargs.get('variable_costs'))
        self.fixed_costs = kwargs.get('fixed_costs')
        self.summed_max = kwargs.get('summed_max')
        self.summed_min = kwargs.get('summed_min')
        self.fixed = kwargs.get('fixed', False)
        self.investment = kwargs.get('investment')
        if self.fixed and self.actual_value is None:
            raise ValueError("Can not fix flow value to None. "
                             "Please set actual_value of the flow")

        elif self.fixed:
            # ToDo: Check if min/max are set by user than raise warning
            # warnings.warn(
            #     "Values for min/max will be ignored if fixed is True.",
            #     SyntaxWarning)
            self.min = sequence(0)
            self.max = sequence(1)
        if self.investment and self.nominal_value is not None:
            self.nominal_value = None
            warnings.warn(
                "Using the investment object the nominal_value" +
                " is set to None.",
                SyntaxWarning)
        self.binary = kwargs.get('binary')
        self.discrete = kwargs.get('discrete')
        if self.investment and self.binary:
            raise ValueError("Investment flows cannot be combined with " +
                             "binary flows!")


class Bus(on.Bus):
    """A balance object. Every node has to be connected to Bus.

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.Bus`

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.balanced = kwargs.get('balanced', True)


class Sink(on.Sink):
    """An object with one input flow.
    """
    pass


class Source(on.Source):
    """An object with one output flow.
    """
    pass


class LinearTransformer(on.Transformer):
    """A Linear Transformer object.

    Parameters
    ----------
    conversion_factors : dict
        Dictionary containing conversion factors for conversion of inflow
        to specified outflow. Keys are output bus objects.
        The dictionary values can either be a scalar or a sequence with length
        of time horizon for simulation.

    Examples
    --------
    Defining an linear transformer:

    >>> bel = Bus()
    >>> bth = Bus()
    >>> bng = Bus()
    >>> trsf = LinearTransformer(conversion_factors={bel: 0.4,
    ...                                              bth: [1, 2, 3]},
    ...                          inputs={bng: Flow()})
    >>> trsf.conversion_factors[bel][3]
    0.4

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.LinearTransformer`
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversion_factors = {
            k: sequence(v)
            for k, v in kwargs.get('conversion_factors', {}).items()}


class LinearN1Transformer(on.Transformer):
    """A Linear N:1 Transformer object.

    Parameters
    ----------

    conversion_factors : dict
        Dictionary containing conversion factors for conversion of inflow(s)
        to specified outflow. Keys are output bus objects.
        The dictionary values can either be a scalar or a sequence with length
        of time horizon for simulation.

    Examples
    --------
    Defining an linear transformer:

    >>> gas = Bus()
    >>> biomass = Bus()
    >>> trsf = LinearN1Transformer(conversion_factors={gas: 0.4,
    ...                                                biomass: [1, 2, 3]})
    >>> trsf.conversion_factors[gas][3]
    0.4

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.LinearN1Transformer`
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversion_factors = {
            k: sequence(v)
            for k, v in kwargs.get('conversion_factors', {}).items()}


class VariableFractionTransformer(LinearTransformer):
    """A linear transformer with more than one output, where the fraction of
    the output flows is variable. By now it is restricted to two output flows.

    One main output flow has to be defined and is tapped by the remaining flow.
    Thus, the main output will be reduced if the tapped output increases.
    Therefore a loss index has to be defined. Furthermore a maximum efficiency
    has to be specified if the whole flow is led to the main output
    (tapped_output = 0). The state with the maximum tapped_output is described
    through conversion factors equivalent to the LinearTransformer.

    Parameters
    ----------
    conversion_factors : dict
        Dictionary containing conversion factors for conversion of inflow
        to specified outflow. Keys are output bus objects.
        The dictionary values can either be a scalar or a sequence with length
        of time horizon for simulation.
    conversion_factor_single_flow : dict
        The efficiency of the main flow if there is no tapped flow. Only one
        key is allowed. Use one of the keys of the conversion factors. The key
        indicates the main flow. The other output flow is the tapped flow.

    Examples
    --------
    >>> bel = Bus(label='electricityBus')
    >>> bth = Bus(label='heatBus')
    >>> bgas = Bus(label='commodityBus')
    >>> vft = VariableFractionTransformer(
    ...    label='variable_chp_gas',
    ...    inputs={bgas: Flow(nominal_value=10e10)},
    ...    outputs={bel: Flow(), bth: Flow()},
    ...    conversion_factors={bel: 0.3, bth: 0.5},
    ...    conversion_factor_single_flow={bel: 0.5})

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.VariableFractionTransformer`
    """
    def __init__(self, conversion_factor_single_flow, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversion_factor_single_flow = {
            k: sequence(v) for k, v in conversion_factor_single_flow.items()}


class Storage(on.Transformer):
    """

    Parameters
    ----------
    nominal_capacity : numeric
        Absolute nominal capacity of the storage
    nominal_input_capacity_ratio :  numeric
        Ratio between the nominal inflow of the storage and its capacity.
    nominal_output_capacity_ratio : numeric
        Ratio between the nominal outflow of the storage and its capacity.
        Note: This ratio is used to create the Flow object for the outflow
        and set its nominal value of the storage in the constructor.
    nominal_input_capacity_ratio : numeric
        see: nominal_output_capacity_ratio
    initial_capacity : numeric
        The capacity of the storage in the first (and last) time step of
        optimization.
    capacity_loss : numeric (sequence or scalar)
        The relative loss of the storage capacity from between two consecutive
        timesteps.
    inflow_conversion_factor : numeric (sequence or scalar)
        The relative conversion factor, i.e. efficiency associated with the
        inflow of the storage.
    outflow_conversion_factor : numeric (sequence or scalar)
        see: inflow_conversion_factor
    capacity_min : numeric (sequence or scalar)
        The nominal minimum capacity of the storage as fraction of the
        nominal capacity (between 0 and 1, default: 0).
        To set different values in every time step use a sequence.
    capacity_max : numeric (sequence or scalar)
        see: capacity_min
    investment : :class:`oemof.solph.options.Investment` object
        Object indicating if a nominal_value of the flow is determined by
        the optimization problem. Note: This will refer all attributes to an
        investment variable instead of to the nominal_capacity. The
        nominal_capacity should not be set (or set to None) if an investment
        object is used.

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.Storage` (if no Investment object
       present)
     * :py:class:`~oemof.solph.blocks.InvestmentStorage` (if Investment object
       present)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nominal_capacity = kwargs.get('nominal_capacity')
        self.nominal_input_capacity_ratio = kwargs.get(
            'nominal_input_capacity_ratio', 0.2)
        self.nominal_output_capacity_ratio = kwargs.get(
            'nominal_output_capacity_ratio', 0.2)
        self.initial_capacity = kwargs.get('initial_capacity')
        self.capacity_loss = sequence(kwargs.get('capacity_loss', 0))
        self.inflow_conversion_factor = sequence(
            kwargs.get(
                'inflow_conversion_factor', 1))
        self.outflow_conversion_factor = sequence(
            kwargs.get(
                'outflow_conversion_factor', 1))
        self.capacity_max = sequence(kwargs.get('capacity_max', 1))
        self.capacity_min = sequence(kwargs.get('capacity_min', 0))
        self.fixed_costs = kwargs.get('fixed_costs')
        self.investment = kwargs.get('investment')
        # Check investment
        if self.investment and self.nominal_capacity is not None:
            self.nominal_capacity = None
            warnings.warn(
                "Using the investment object the nominal_capacity is set to" +
                "None.", SyntaxWarning)
        # Check input flows for nominal value
        for flow in self.inputs.values():
            if flow.nominal_value is not None:
                storage_nominal_value_warning('output')
            if self.nominal_capacity is None:
                flow.nominal_value = None
            else:
                flow.nominal_value = (self.nominal_input_capacity_ratio *
                                      self.nominal_capacity)
            if self.investment:
                if not isinstance(flow.investment, Investment):
                    flow.investment = Investment()

        # Check output flows for nominal value
        for flow in self.outputs.values():
            if flow.nominal_value is not None:
                storage_nominal_value_warning('input')
            if self.nominal_capacity is None:
                flow.nominal_value = None
            else:
                flow.nominal_value = (self.nominal_output_capacity_ratio *
                                      self.nominal_capacity)
            if self.investment:
                if not isinstance(flow.investment, Investment):
                    flow.investment = Investment()


def storage_nominal_value_warning(flow):
    msg = ("The nominal_value should not be set for {0} flows of storages." +
           "The value will be overwritten by the product of the " +
           "nominal_capacity and the nominal_{0}_capacity_ratio.")
    warnings.warn(msg.format(flow), SyntaxWarning)
