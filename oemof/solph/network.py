# -*- coding: utf-8 -*-
"""

"""
import warnings
import oemof.network as on
from .options import Investment
from .options import Sequence


class Flow:
    """
    Define a flow between two nodes.

    Parameters
    ----------
    summed_max : float
        Specific maximum value summed over all timesteps. Will be multiplied
        with the nominal_value to get the absolute limit. If investment is set
        the summed_max will be multiplied with the nominal_value_variable.
    summed_min : float
        see above
    actual_value : float or array-like
        Specific value for the flow variable. Will be multiplied with the
        nominal_value to get the absolute value. If fixed is True the flow
        variable will be fixed to actual_value * nominal_value.

    """
    def __init__(self, **kwargs):
        """
        """
        # TODO: Check if we can inherit form pyomo.core.base.var _VarData
        # then we need to create the var object with
        # pyomo.core.base.IndexedVarWithDomain before any Flow is created.
        # E.g. create the variable in the energy system and populate with
        # information afterwards when creating objects.

        self.nominal_value = kwargs.get('nominal_value')
        self.min = Sequence(kwargs.get('min', 0))
        self.max = Sequence(kwargs.get('max', 1))
        self.actual_value = Sequence(kwargs.get('actual_value'))
        self.positive_gradient = Sequence(kwargs.get('positive_gradient'))
        self.negative_gradient = Sequence(kwargs.get('negative_gradient'))
        self.variable_costs = Sequence(kwargs.get('variable_costs'))
        self.fixed_costs = kwargs.get('fixed_costs')
        self.summed_max = kwargs.get('summed_max')
        self.summed_min = kwargs.get('summed_min')
        self.fixed = kwargs.get('fixed', False)
        self.investment = kwargs.get('investment')
        if self.fixed:
            # ToDo: Check if min/max are set by user than raise warning
            # warnings.warn(
            #     "Values for min/max will be ignored if fixed is True.",
            #     SyntaxWarning)
            self.min = Sequence(0)
            self.max = Sequence(1)
        if self.investment and self.nominal_value is not None:
            self.nominal_value = None
            warnings.warn(
                "Using the investment object the nominal_value is set to None.",
                SyntaxWarning)
        self.discrete = kwargs.get('discrete')
        if self.investment and self.discrete:
            raise ValueError("Investment flows cannot be combined with " +
                             "discrete flows!")


class Bus(on.Bus):
    """A balance object.
    """
    pass


class Sink(on.Sink):
    """An object with one input flow.
    """
    pass


class Source(on.Source):
    """An object with one output flow.
    """
    pass


class LinearTransformer(on.Transformer):
    """
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
    >>> trsf = LinearTransformer(conversion_factors={bel: 0.4,
    ...                                              bth: [1, 2, 3]})
    >>> trsf.conversion_factors[bel][3]
    0.4
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversion_factors = {
            k: Sequence(v)
            for k, v in kwargs.get('conversion_factors').items()}


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
        The capacity of the storage in the first (and last) timestep of
        optimization.
    capacity_loss : numeric (sequence or scalar)
        The relative loss of the storage capacity from between two consecutive
        timesteps.
    inflow_conversion_factor : numeric (sequence or scalar)
        The relative conversion factor, i.e. efficiency associated with the
        inflow of the storage.
    outflow_conversion_factor : numeric (sequence or scalar)
        see: inflow_conversion_factor
    capacity_min : numeric (scalar or array-like)
        The nominal minimum capacity of the storage as fraction of the
        nominal capacity (between 0 and 1, default: 0).
        To set different values in every timestep use an array-like object.
    capacity_max : numeric (sequence or scalar)
        see: capacity_min

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nominal_capacity = kwargs.get('nominal_capacity')
        self.nominal_input_capacity_ratio = kwargs.get(
            'nominal_input_capacity_ratio', 0.2)
        self.nominal_output_capacity_ratio = kwargs.get(
            'nominal_output_capacity_ratio', 0.2)
        self.initial_capacity = kwargs.get('initial_capacity')
        self.capacity_loss = Sequence(kwargs.get('capacity_loss', 0))
        self.inflow_conversion_factor = Sequence(
            kwargs.get(
                'inflow_conversion_factor', 1))
        self.outflow_conversion_factor = Sequence(
            kwargs.get(
                'outflow_conversion_factor', 1))
        self.capacity_max = Sequence(kwargs.get('capacity_max', 1))
        self.capacity_min = Sequence(kwargs.get('capacity_min', 0))
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
