# -*- coding: utf-8 -*-

""" Classes used to model energy supply systems within solph.

Classes are derived from oemof core network classes and adapted for specific
optimization tasks. An energy system is modelled as a graph/network of nodes
with very specific constraints on which types of nodes are allowed to be
connected.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/solph/network.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

import oemof.network as on
import oemof.energy_system as es
from oemof.solph.plumbing import sequence
from oemof.solph import blocks


class EnergySystem(es.EnergySystem):
    """ A variant of :class:`EnergySystem
    <oemof.core.energy_system.EnergySystem>` specially tailored to solph.

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
        from oemof.solph.groupings import GROUPINGS

        kwargs['groupings'] = (GROUPINGS + kwargs.get('groupings', []))

        super().__init__(**kwargs)


class Flow(on.Edge):
    r""" Defines a flow between two nodes.

    Keyword arguments are used to set the attributes of this flow. Parameters
    which are handled specially are noted below.
    For the case where a parameter can be either a scalar or a sequence, a
    scalar value will be converted to a sequence containing the scalar value at
    every index. This sequence is then stored under the paramter's key.

    Parameters
    ----------
    nominal_value : numeric
        The nominal value of the flow. If this value is set the corresponding
        optimization variable of the flow object will be bounded by this value
        multiplied with min(lower bound)/max(upper bound).
    max : numeric (sequence or scalar)
        Normed maximum value of the flow. The flow absolute maximum will be
        calculated by multiplying :attr:`nominal_value` with :attr:`max`
    min : numeric (sequence or scalar)
        Nominal minimum value of the flow (see :attr:`max`).
    actual_value : numeric (sequence or scalar)
        Specific value for the flow variable. Will be multiplied with the
        :attr:`nominal_value` to get the absolute value. If :attr:`fixed` is
        set to :obj:`True` the flow variable will be fixed to :py:`actual_value
        * nominal_value`, i.e. this value is set exogenous.
    positive_gradient : :obj:`dict`, default: :py:`{'ub': None, 'costs': 0}`
        A dictionary containing the following two keys:

         * :py:`'ub'`: numeric (sequence, scalar or None), the normed *upper
           bound* on the positive difference (:py:`flow[t-1] < flow[t]`) of
           two consecutive flow values.
         * :py:`'costs``: numeric (scalar or None), the gradient cost per
           unit.

    negative_gradient : :obj:`dict`, default: :py:`{'ub': None, 'costs': 0}`

        A dictionary containing the following two keys:

          * :py:`'ub'`: numeric (sequence, scalar or None), the normed *upper
            bound* on the negative difference (:py:`flow[t-1] > flow[t]`) of
            two consecutive flow values.
          * :py:`'costs``: numeric (scalar or None), the gradient cost per
            unit.

    summed_max : numeric
        Specific maximum value summed over all timesteps. Will be multiplied
        with the nominal_value to get the absolute limit.
    summed_min : numeric
        see above
    variable_costs : numeric (sequence or scalar)
        The costs associated with one unit of the flow. If this is set the
        costs will be added to the objective expression of the optimization
        problem.
    fixed : boolean
        Boolean value indicating if a flow is fixed during the optimization
        problem to its ex-ante set value. Used in combination with the
        :attr:`actual_value`.
    investment : :class:`Investment <oemof.solph.options.Investment>`
        Object indicating if a nominal_value of the flow is determined by
        the optimization problem. Note: This will refer all attributes to an
        investment variable instead of to the nominal_value. The nominal_value
        should not be set (or set to None) if an investment object is used.
    nonconvex : :class:`NonConvex <oemof.solph.options.NonConvex>`
        If a nonconvex flow object is added here, the flow constraints will
        be altered significantly as the mathematical model for the flow
        will be different, i.e. constraint etc. from
        :class:`NonConvexFlow <oemof.solph.blocks.NonConvexFlow>`
        will be used instead of
        :class:`Flow <oemof.solph.blocks.Flow>`.
        Note: at the moment this does not work if the investment attribute is
        set .

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.Flow`
     * :py:class:`~oemof.solph.blocks.InvestmentFlow` (additionally if
       Investment object is present)
     * :py:class:`~oemof.solph.blocks.NonConvexFlow` (If
        nonconvex  object is present, CAUTION: replaces
        :py:class:`~oemof.solph.blocks.Flow` class and a MILP will be build)

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

        super().__init__()

        scalars = ['nominal_value', 'summed_max', 'summed_min',
                   'investment', 'nonconvex', 'integer', 'fixed']
        sequences = ['actual_value', 'variable_costs', 'min', 'max']
        dictionaries = ['positive_gradient', 'negative_gradient']
        defaults = {'fixed': False, 'min': 0, 'max': 1, 'variable_costs': 0,
                    'positive_gradient': {'ub': None, 'costs': 0},
                    'negative_gradient': {'ub': None, 'costs': 0},
                    }

        for attribute in set(scalars + sequences + dictionaries + list(kwargs)):
            value = kwargs.get(attribute, defaults.get(attribute))
            if attribute in dictionaries:
                setattr(self, attribute, {'ub': sequence(value['ub']),
                                          'costs': value['costs']})
            elif 'fixed_costs' in attribute:
                raise AttributeError(
                         "The `fixed_costs` attribute has been removed"
                         " with v0.2!")
            else:
                setattr(self, attribute,
                        sequence(value) if attribute in sequences else value)

        # Checking for impossible attribute combinations
        if self.fixed and self.actual_value[0] is None:
            raise ValueError("Cannot fix flow value to None.\n Please "
                             "set the actual_value attribute of the flow")
        if self.investment and self.nominal_value is not None:
            raise ValueError("Using the investment object the nominal_value"
                             " has to be set to None.")
        if self.investment and self.nonconvex:
            raise ValueError("Investment flows cannot be combined with " +
                             "nonconvex flows!")


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


    def constraint_group(self):
        if self.balanced:
            return blocks.Bus
        else:
            return None

class Sink(on.Sink):
    """An object with one input flow.
    """
    def constraint_group(self):
        pass

class Source(on.Source):
    """An object with one output flow.
    """
    def constraint_group(self):
        pass


class Transformer(on.Transformer):
    """A linear Transformer object with n inputs and n outputs.

    Parameters
    ----------
    conversion_factors : dict
        Dictionary containing conversion factors for conversion of each flow.
        Keys are the connected bus objects.
        The dictionary values can either be a scalar or a sequence with length
        of time horizon for simulation.

    Examples
    --------
    Defining an linear transformer:

    >>> from oemof import solph
    >>> bgas = solph.Bus(label='natural_gas')
    >>> bcoal = solph.Bus(label='hard_coal')
    >>> bel = solph.Bus(label='electricity')
    >>> bheat = solph.Bus(label='heat')

    >>> trsf = solph.Transformer(
    ...    label='pp_gas_1',
    ...    inputs={bgas: solph.Flow(), bcoal: solph.Flow()},
    ...    outputs={bel: solph.Flow(), bheat: solph.Flow()},
    ...    conversion_factors={bel: 0.3, bheat: 0.5,
    ...                        bgas: 0.8, bcoal: 0.2})
    >>> print(sorted([x[1][5] for x in trsf.conversion_factors.items()]))
    [0.2, 0.3, 0.5, 0.8]

    >>> type(trsf)
    <class 'oemof.solph.network.Transformer'>

    >>> sorted([str(i) for i in trsf.inputs])
    ['hard_coal', 'natural_gas']

    >>> trsf_new = solph.Transformer(
    ...    label='pp_gas_2',
    ...    inputs={bgas: solph.Flow()},
    ...    outputs={bel: solph.Flow(), bheat: solph.Flow()},
    ...    conversion_factors={bel: 0.3, bheat: 0.5})
    >>> trsf_new.conversion_factors[bgas][3]
    1

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.Transformer`
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.conversion_factors = {
            k: sequence(v)
            for k, v in kwargs.get('conversion_factors', {}).items()}

        missing_conversion_factor_keys = (
            (set(self.outputs) | set(self.inputs)) -
            set(self.conversion_factors))

        for cf in missing_conversion_factor_keys:
            self.conversion_factors[cf] = sequence(1)


    def constraint_group(self):
        return blocks.Transformer
