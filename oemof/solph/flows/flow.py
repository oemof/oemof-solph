# -*- coding: utf-8 -*-
"""

"""
import warnings
from oemof.solph.plumbing import sequence


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
