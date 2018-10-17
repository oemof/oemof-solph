# -*- coding: utf-8 -*-

"""This module is designed to hold custom components with their classes and
associated individual constraints (blocks) and groupings. Therefore this
module holds the class definition and the block directly located by each other.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/solph/custom.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

from pyomo.core.base.block import SimpleBlock
from pyomo.environ import (Binary, Set, NonNegativeReals, Var, Constraint,
                           Expression, BuildAction)
import logging

from oemof.solph.network import Bus, Transformer
from oemof.solph.plumbing import sequence


class ElectricalBus(Bus):
    r"""A electrical bus object. Every node has to be connected to Bus. This
    Bus is used in combination with ElectricalLine objects for linear optimal
    power flow (lopf) simulations.

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.Bus`
    The objects are also used inside:
     * :py:class:`~oemof.solph.custom.ElectricalLine`

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slack = kwargs.get('slack', False)
        self.v_max = kwargs.get('v_max', 1000)
        self.v_min = kwargs.get('v_min', -1000)


class ElectricalLine(Transformer):
    r"""An ElectricalLine to be used in linear optimal power flow calculations.
    based on angle formulation. Check out the Notes below before using this
    component!

    Parameters
    ----------
    reactance : float or array of floats
        Reactance of the line to be modelled

    Notes
    -----
    * To use this object the connected buses need to be of the type
      :py:class:`~oemof.solph.custom.ElectricalBus`.
    * It does not work together with flows that have set the attr.`nonconvex`,
      i.e. unit commitment constraints are not possible
    * Input and output of this component are set equal, therefore just use
      either only the input or the output to parameterize.
    * Default attribute `min` of in/outflows is overwritten by -1 if not set
      differently by the user

    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.custom.ElectricalLineBlock`

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reactance = sequence(kwargs.get('reactance', 0.00001))

        if len(self.inputs) > 1 or len(self.outputs) > 1:
            raise ValueError("Component ElectricLine must not have more than \
                             one input and one output!")

        self.input = self._input()
        self.output = self._output()

        # set input / output flow values to -1 by default if not set by user
        for f in self.inputs.values():
            if f.nonconvex is not None:
                raise ValueError(
                    "Attribute `nonconvex` must be None for" +
                    " inflows of component `ElectricalLine`!")
            if f.min is None:
                f.min = -1
            # to be used in grouping for all bidi flows
            f.bidirectional = True

        for f in self.outputs.values():
            if f.nonconvex is not None:
                raise ValueError(
                    "Attribute `nonconvex` must be None for" +
                    " outflows of component `ElectricalLine`!")
            if f.min is None:
                f.min = -1
            # to be used in grouping for all bidi flows
            f.bidirectional = True

    def _input(self):
        r""" Returns the first (and only!) input of the line object
        """
        return [i for i in self.inputs][0]

    def _output(self):
        r""" Returns the first (and only!) output of the line object
        """
        return [o for o in self.outputs][0]

    def constraint_group(self):
        return ElectricalLineBlock


class ElectricalLineBlock(SimpleBlock):
    r"""Block for the linear relation of nodes with type
    class:`.ElectricalLine`


    **The following constraints are created:**

    Linear relation :attr:`om.ElectricalLine.electrical_flow[n,t]`
        .. math::
            flow(n, o, t) =  1 / reactance(n, t) \\cdot ()
            voltage_angle(i(n), t) - volatage_angle(o(n), t), \\
            \forall t \\in \\textrm{TIMESTEPS}, \\
            \forall n \\in \\textrm{ELECTRICAL\_LINES}.

    TODO: Add equate constraint of flows

    **The following variable are created:**

    TODO: Add voltage angle variable

    TODO: Add fix slack bus voltage angle to zero constraint / bound

    TODO: Add tests
    """

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """ Creates the linear constraint for the class:`ElectricalLine`
        block.

        Parameters
        ----------
        group : list
            List of oemof.solph.ElectricalLine (eline) objects for which
            the linear relation of inputs and outputs is created
            e.g. group = [eline1, eline2, ...]. The components inside the
            list need to hold a attribute `reactance` of type Sequence
            containing the reactance of the line.
        """
        if group is None:
            return None

        m = self.parent_block()

        I = {n: n.input for n in group}
        O = {n: n.output for n in group}

        # create voltage angle variables
        self.ELECTRICAL_BUSES = Set(initialize=[n for n in m.es.nodes
                                       if isinstance(n, ElectricalBus)])

        def _voltage_angle_bounds(block, b, t):
            return b.v_min, b.v_max
        self.voltage_angle = Var(self.ELECTRICAL_BUSES, m.TIMESTEPS,
                                    bounds=_voltage_angle_bounds)

        if True not in [b.slack for b in self.ELECTRICAL_BUSES]:
            # TODO: Make this robust to select the same slack bus for
            # the same problems
            bus = [b for b in self.ELECTRICAL_BUSES][0]
            logging.info(
                "No slack bus set,setting bus {0} as slack bus".format(
                    bus.label))
            bus.slack = True

        def _voltage_angle_relation(block):
            for t in m.TIMESTEPS:
                for n in group:
                    if O[n].slack is True:
                        self.voltage_angle[O[n], t].value = 0
                        self.voltage_angle[O[n], t].fix()
                    try:
                        lhs = m.flow[n, O[n], t]
                        rhs = 1 / n.reactance[t] * (
                            self.voltage_angle[I[n], t] -
                            self.voltage_angle[O[n], t])
                    except:
                        raise ValueError("Error in constraint creation",
                                         "of node {}".format(n.label))
                    block.electrical_flow.add((n, t), (lhs == rhs))
                    # add constraint to set in-outflow equal
                    block._equate_electrical_flows.add((n, t), (
                        m.flow[n, O[n], t] == m.flow[I[n], n, t]))

        self.electrical_flow = Constraint(group, m.TIMESTEPS, noruleinit=True)

        self._equate_electrical_flows = Constraint(group, m.TIMESTEPS,
                                                   noruleinit=True)

        self.electrical_flow_build = BuildAction(
                                         rule=_voltage_angle_relation)


class Link(Transformer):
    """A Link object with 1...2 inputs and 1...2 outputs.

    Parameters
    ----------
    conversion_factors : dict
        Dictionary containing conversion factors for conversion of each flow.
        Keys are the connected tuples (input, output) bus objects.
        The dictionary values can either be a scalar or a sequence with length
        of time horizon for simulation.

    Notes
    -----
    The sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.custom.LinkBlock`

    Examples
    --------

    >>> from oemof import solph
    >>> bel0 = solph.Bus(label="el0")
    >>> bel1 = solph.Bus(label="el1")

    >>> link = solph.custom.Link(
    ...    label="transshipment_link",
    ...    inputs={bel0: solph.Flow(), bel1: solph.Flow()},
    ...    outputs={bel0: solph.Flow(), bel1: solph.Flow()},
    ...    conversion_factors={(bel0, bel1): 0.92, (bel1, bel0): 0.99})
    >>> print(sorted([x[1][5] for x in link.conversion_factors.items()]))
    [0.92, 0.99]

    >>> type(link)
    <class 'oemof.solph.custom.Link'>

    >>> sorted([str(i) for i in link.inputs])
    ['el0', 'el1']

    >>> link.conversion_factors[(bel0, bel1)][3]
    0.92
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if len(self.inputs) > 2 or len(self.outputs) > 2:
            raise ValueError("Component `Link` must not have more than \
                             2 inputs and 2 outputs!")

        self.conversion_factors = {
            k: sequence(v)
            for k, v in kwargs.get('conversion_factors', {}).items()}

    def constraint_group(self):
        return LinkBlock

class LinkBlock(SimpleBlock):
    r"""Block for the relation of nodes with type
    :class:`~oemof.solph.custom.Link`

    **The following constraints are created:**

    TODO: Add description for constraints
    TODO: Add tests

    """
    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """ Creates the relation for the class:`Link`.

        Parameters
        ----------
        group : list
            List of oemof.solph.custom.Link objects for which
            the relation of inputs and outputs is createdBuildAction
            e.g. group = [link1, link2, link3, ...]. The components inside
            the list need to hold an attribute `conversion_factors` of type
            dict containing the conversion factors for all inputs to outputs.
        """
        if group is None:
            return None

        m = self.parent_block()

        all_conversions = {}
        for n in group:
            all_conversions[n] = {
                            k: v for k, v in n.conversion_factors.items()}

        def _input_output_relation(block):
            for t in m.TIMESTEPS:
                for n, conversion in all_conversions.items():
                    for cidx, c in conversion.items():
                        try:
                            expr = (m.flow[n, cidx[1], t] ==
                                    c[t] * m.flow[cidx[0], n, t])
                        except ValueError:
                            raise ValueError(
                                "Error in constraint creation",
                                "from: {0}, to: {1}, via: {3}".format(
                                    cidx[0], cidx[1], n))
                        block.relation.add((n, cidx[0], cidx[1], t), (expr))

        self.relation = Constraint(
            [(n, cidx[0], cidx[1], t)
             for t in m.TIMESTEPS
             for n, conversion in all_conversions.items()
             for cidx, c in conversion.items()], noruleinit=True)
        self.relation_build = BuildAction(rule=_input_output_relation)


class GenericCAES(Transformer):
    """
    Component `GenericCAES` to model arbitrary compressed air energy storages.

    The full set of equations is described in:
    Kaldemeyer, C.; Boysen, C.; Tuschy, I.
    A Generic Formulation of Compressed Air Energy Storage as
    Mixed Integer Linear Program – Unit Commitment of Specific
    Technical Concepts in Arbitrary Market Environments
    Materials Today: Proceedings 00 (2018) 0000–0000
    [currently in review]

    Parameters
    ----------
    electrical_input : dict
        Dictionary with key-value-pair of `oemof.Bus` and `oemof.Flow` object
        for the electrical input.
    fuel_input : dict
        Dictionary with key-value-pair of `oemof.Bus` and `oemof.Flow` object
        for the fuel input.
    electrical_output : dict
        Dictionary with key-value-pair of `oemof.Bus` and `oemof.Flow` object
        for the electrical output.

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.GenericCAES`

    TODO: Add description for constraints. See referenced paper until then!

    Examples
    --------

    >>> from oemof import solph
    >>> bel = solph.Bus(label='bel')
    >>> bth = solph.Bus(label='bth')
    >>> bgas = solph.Bus(label='bgas')
    >>> # dictionary with parameters for a specific CAES plant
    >>> concept = {
    ...    'cav_e_in_b': 0,
    ...    'cav_e_in_m': 0.6457267578,
    ...    'cav_e_out_b': 0,
    ...    'cav_e_out_m': 0.3739636077,
    ...    'cav_eta_temp': 1.0,
    ...    'cav_level_max': 211.11,
    ...    'cmp_p_max_b': 86.0918959849,
    ...    'cmp_p_max_m': 0.0679999932,
    ...    'cmp_p_min': 1,
    ...    'cmp_q_out_b': -19.3996965679,
    ...    'cmp_q_out_m': 1.1066036114,
    ...    'cmp_q_tes_share': 0,
    ...    'exp_p_max_b': 46.1294016678,
    ...    'exp_p_max_m': 0.2528340303,
    ...    'exp_p_min': 1,
    ...    'exp_q_in_b': -2.2073411014,
    ...    'exp_q_in_m': 1.129249765,
    ...    'exp_q_tes_share': 0,
    ...    'tes_eta_temp': 1.0,
    ...    'tes_level_max': 0.0}
    >>> # generic compressed air energy storage (caes) plant
    >>> caes = solph.custom.GenericCAES(
    ...    label='caes',
    ...    electrical_input={bel: solph.Flow()},
    ...    fuel_input={bgas: solph.Flow()},
    ...    electrical_output={bel: solph.Flow()},
    ...    params=concept, fixed_costs=0)
    >>> type(caes)
    <class 'oemof.solph.custom.GenericCAES'>
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.electrical_input = kwargs.get('electrical_input')
        self.fuel_input = kwargs.get('fuel_input')
        self.electrical_output = kwargs.get('electrical_output')
        self.params = kwargs.get('params')

        # map specific flows to standard API
        self.inputs.update(kwargs.get('electrical_input'))
        self.inputs.update(kwargs.get('fuel_input'))
        self.outputs.update(kwargs.get('electrical_output'))

    def constraint_group(self):
        return GenericCAESBlock


class GenericCAESBlock(SimpleBlock):
    """Block for nodes of class:`.GenericCAES`."""

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """
        Create constraints for GenericCAESBlock.

        Parameters
        ----------
        group : list
            List containing `.GenericCAES` objects.
            e.g. groups=[gcaes1, gcaes2,..]
        """
        m = self.parent_block()

        if group is None:
            return None

        self.GENERICCAES = Set(initialize=[n for n in group])

        # Compression: Binary variable for operation status
        self.cmp_st = Var(self.GENERICCAES, m.TIMESTEPS, within=Binary)

        # Compression: Realized capacity
        self.cmp_p = Var(self.GENERICCAES, m.TIMESTEPS,
                         within=NonNegativeReals)

        # Compression: Max. Capacity
        self.cmp_p_max = Var(self.GENERICCAES, m.TIMESTEPS,
                             within=NonNegativeReals)

        # Compression: Heat flow
        self.cmp_q_out_sum = Var(self.GENERICCAES, m.TIMESTEPS,
                                 within=NonNegativeReals)

        # Compression: Waste heat
        self.cmp_q_waste = Var(self.GENERICCAES, m.TIMESTEPS,
                               within=NonNegativeReals)

        # Expansion: Binary variable for operation status
        self.exp_st = Var(self.GENERICCAES, m.TIMESTEPS, within=Binary)

        # Expansion: Realized capacity
        self.exp_p = Var(self.GENERICCAES, m.TIMESTEPS,
                         within=NonNegativeReals)

        # Expansion: Max. Capacity
        self.exp_p_max = Var(self.GENERICCAES, m.TIMESTEPS,
                             within=NonNegativeReals)

        # Expansion: Heat flow of natural gas co-firing
        self.exp_q_in_sum = Var(self.GENERICCAES, m.TIMESTEPS,
                                within=NonNegativeReals)

        # Expansion: Heat flow of natural gas co-firing
        self.exp_q_fuel_in = Var(self.GENERICCAES, m.TIMESTEPS,
                                 within=NonNegativeReals)

        # Expansion: Heat flow of additional firing
        self.exp_q_add_in = Var(self.GENERICCAES, m.TIMESTEPS,
                                within=NonNegativeReals)

        # Cavern: Filling levelh
        self.cav_level = Var(self.GENERICCAES, m.TIMESTEPS,
                             within=NonNegativeReals)

        # Cavern: Energy inflow
        self.cav_e_in = Var(self.GENERICCAES, m.TIMESTEPS,
                            within=NonNegativeReals)

        # Cavern: Energy outflow
        self.cav_e_out = Var(self.GENERICCAES, m.TIMESTEPS,
                             within=NonNegativeReals)

        # TES: Filling levelh
        self.tes_level = Var(self.GENERICCAES, m.TIMESTEPS,
                             within=NonNegativeReals)

        # TES: Energy inflow
        self.tes_e_in = Var(self.GENERICCAES, m.TIMESTEPS,
                            within=NonNegativeReals)

        # TES: Energy outflow
        self.tes_e_out = Var(self.GENERICCAES, m.TIMESTEPS,
                             within=NonNegativeReals)

        # Spot market: Positive capacity
        self.exp_p_spot = Var(self.GENERICCAES, m.TIMESTEPS,
                              within=NonNegativeReals)

        # Spot market: Negative capacity
        self.cmp_p_spot = Var(self.GENERICCAES, m.TIMESTEPS,
                              within=NonNegativeReals)

        # Compression: Capacity on markets
        def cmp_p_constr_rule(block, n, t):
            expr = 0
            expr += -self.cmp_p[n, t]
            expr += m.flow[list(n.electrical_input.keys())[0], n, t]
            return expr == 0
        self.cmp_p_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_p_constr_rule)

        # Compression: Max. capacity depending on cavern filling level
        def cmp_p_max_constr_rule(block, n, t):
            if t != 0:
                return (self.cmp_p_max[n, t] ==
                        n.params['cmp_p_max_m'] * self.cav_level[n, t-1] +
                        n.params['cmp_p_max_b'])
            else:
                return (self.cmp_p_max[n, t] == n.params['cmp_p_max_b'])
        self.cmp_p_max_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_p_max_constr_rule)

        def cmp_p_max_area_constr_rule(block, n, t):
            return (self.cmp_p[n, t] <= self.cmp_p_max[n, t])
        self.cmp_p_max_area_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_p_max_area_constr_rule)

        # Compression: Status of operation (on/off)
        def cmp_st_p_min_constr_rule(block, n, t):
            return (
                self.cmp_p[n, t] >= n.params['cmp_p_min'] * self.cmp_st[n, t])
        self.cmp_st_p_min_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_st_p_min_constr_rule)

        def cmp_st_p_max_constr_rule(block, n, t):
            return (self.cmp_p[n, t] <=
                    (n.params['cmp_p_max_m'] * n.params['cav_level_max'] +
                    n.params['cmp_p_max_b']) * self.cmp_st[n, t])
        self.cmp_st_p_max_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_st_p_max_constr_rule)

        # Compression: Heat flow out
        def cmp_q_out_constr_rule(block, n, t):
            return (self.cmp_q_out_sum[n, t] ==
                    n.params['cmp_q_out_m'] * self.cmp_p[n, t] +
                    n.params['cmp_q_out_b'] * self.cmp_st[n, t])
        self.cmp_q_out_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_q_out_constr_rule)

        # Compression: Definition of single heat flows
        def cmp_q_out_sum_constr_rule(block, n, t):
            return (self.cmp_q_out_sum[n, t] == self.cmp_q_waste[n, t] +
                    self.tes_e_in[n, t])
        self.cmp_q_out_sum_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_q_out_sum_constr_rule)

        # Compression: Heat flow out ratio
        def cmp_q_out_shr_constr_rule(block, n, t):
            return (self.cmp_q_waste[n, t] * n.params['cmp_q_tes_share'] ==
                    self.tes_e_in[n, t] * (1 - n.params['cmp_q_tes_share']))
        self.cmp_q_out_shr_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_q_out_shr_constr_rule)

        # Expansion: Capacity on markets
        def exp_p_constr_rule(block, n, t):
            expr = 0
            expr += -self.exp_p[n, t]
            expr += m.flow[n, list(n.electrical_output.keys())[0], t]
            return expr == 0
        self.exp_p_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_p_constr_rule)

        # Expansion: Max. capacity depending on cavern filling level
        def exp_p_max_constr_rule(block, n, t):
            if t != 0:
                return (self.exp_p_max[n, t] ==
                        n.params['exp_p_max_m'] * self.cav_level[n, t-1] +
                        n.params['exp_p_max_b'])
            else:
                return (self.exp_p_max[n, t] == n.params['exp_p_max_b'])
        self.exp_p_max_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_p_max_constr_rule)

        def exp_p_max_area_constr_rule(block, n, t):
            return (self.exp_p[n, t] <= self.exp_p_max[n, t])
        self.exp_p_max_area_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_p_max_area_constr_rule)

        # Expansion: Status of operation (on/off)
        def exp_st_p_min_constr_rule(block, n, t):
            return (
                self.exp_p[n, t] >= n.params['exp_p_min'] * self.exp_st[n, t])
        self.exp_st_p_min_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_st_p_min_constr_rule)

        def exp_st_p_max_constr_rule(block, n, t):
            return (self.exp_p[n, t] <=
                    (n.params['exp_p_max_m'] * n.params['cav_level_max'] +
                     n.params['exp_p_max_b']) * self.exp_st[n, t])
        self.exp_st_p_max_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_st_p_max_constr_rule)

        # Expansion: Heat flow in
        def exp_q_in_constr_rule(block, n, t):
            return (self.exp_q_in_sum[n, t] ==
                    n.params['exp_q_in_m'] * self.exp_p[n, t] +
                    n.params['exp_q_in_b'] * self.exp_st[n, t])
        self.exp_q_in_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_q_in_constr_rule)

        # Expansion: Fuel allocation
        def exp_q_fuel_constr_rule(block, n, t):
            expr = 0
            expr += -self.exp_q_fuel_in[n, t]
            expr += m.flow[list(n.fuel_input.keys())[0], n, t]
            return expr == 0
        self.exp_q_fuel_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_q_fuel_constr_rule)

        # Expansion: Definition of single heat flows
        def exp_q_in_sum_constr_rule(block, n, t):
            return (self.exp_q_in_sum[n, t] == self.exp_q_fuel_in[n, t] +
                    self.tes_e_out[n, t] + self.exp_q_add_in[n, t])
        self.exp_q_in_sum_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_q_in_sum_constr_rule)

        # Expansion: Heat flow in ratio
        def exp_q_in_shr_constr_rule(block, n, t):
            return (n.params['exp_q_tes_share'] * self.exp_q_fuel_in[n, t] ==
                    (1 - n.params['exp_q_tes_share']) *
                    (self.exp_q_add_in[n, t] + self.tes_e_out[n, t]))
        self.exp_q_in_shr_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_q_in_shr_constr_rule)

        # Cavern: Energy inflow
        def cav_e_in_constr_rule(block, n, t):
            return (self.cav_e_in[n, t] ==
                    n.params['cav_e_in_m'] * self.cmp_p[n, t] +
                    n.params['cav_e_in_b'])
        self.cav_e_in_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cav_e_in_constr_rule)

        # Cavern: Energy outflow
        def cav_e_out_constr_rule(block, n, t):
            return (self.cav_e_out[n, t] ==
                    n.params['cav_e_out_m'] * self.exp_p[n, t] +
                    n.params['cav_e_out_b'])
        self.cav_e_out_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cav_e_out_constr_rule)

        # Cavern: Storage balance
        def cav_eta_constr_rule(block, n, t):
            if t != 0:
                return (n.params['cav_eta_temp'] * self.cav_level[n, t] ==
                        self.cav_level[n, t-1] + m.timeincrement[t] *
                        (self.cav_e_in[n, t] - self.cav_e_out[n, t]))
            else:
                return (n.params['cav_eta_temp'] * self.cav_level[n, t] ==
                        m.timeincrement[t] *
                        (self.cav_e_in[n, t] - self.cav_e_out[n, t]))
        self.cav_eta_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cav_eta_constr_rule)

        # Cavern: Upper bound
        def cav_ub_constr_rule(block, n, t):
            return (self.cav_level[n, t] <= n.params['cav_level_max'])
        self.cav_ub_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cav_ub_constr_rule)

        # TES: Storage balance
        def tes_eta_constr_rule(block, n, t):
            if t != 0:
                return (self.tes_level[n, t] ==
                        self.tes_level[n, t-1] + m.timeincrement[t] *
                        (self.tes_e_in[n, t] - self.tes_e_out[n, t]))
            else:
                return (self.tes_level[n, t] ==
                        m.timeincrement[t] *
                        (self.tes_e_in[n, t] - self.tes_e_out[n, t]))
        self.tes_eta_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=tes_eta_constr_rule)

        # TES: Upper bound
        def tes_ub_constr_rule(block, n, t):
            return (self.tes_level[n, t] <= n.params['tes_level_max'])
        self.tes_ub_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=tes_ub_constr_rule)


class OffsetTransformer(Transformer):
    """An object with one input and one output.

    Parameters
    ----------

    coefficients : dict
        Dictionary containing the first two polynomial coefficients
        i.e. the y-intersect and slope of a linear equation.
        Keys are the connected tuples (input, output) bus objects.
        The dictionary values can either be a scalar or a sequence with length
        of time horizon for simulation.

    Notes
    -----
    The sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.custom.OffsetTransformer`

    Examples
    --------

    >>> from oemof import solph

    >>> bel = solph.Bus(label='bel')
    >>> bth = solph.Bus(label='bth')

    >>> ostf = solph.custom.OffsetTransformer(
    ...    label='ostf',
    ...    inputs={bel: solph.Flow(
    ...        nominal_value=60, min=0.5, max=1.0,
    ...        nonconvex=solph.NonConvex())},
    ...    outputs={bth: solph.Flow()},
    ...    coefficients={(bel, bth): [20, 0.5]})

    >>> type(ostf)
    <class 'oemof.solph.custom.OffsetTransformer'>
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.coefficients = kwargs.get('coefficients')

        for k, v in self.inputs.items():
            if not v.nonconvex:
                raise TypeError('Input flows must be of type NonConvexFlow!')

        if len(self.inputs) > 1 or len(self.outputs) > 1:
            raise ValueError("Component `OffsetTransformer` must not have" +
                             "more than 1 input and 1 output!")

    def constraint_group(self):
        return OffsetTransformerBlock


class OffsetTransformerBlock(SimpleBlock):
    r"""Block for the relation of nodes with type
    :class:`~oemof.solph.custom.OffsetTransformer`

    **The following constraints are created:**

    TODO: Add description for constraints

    TODO: Add test

    """
    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """ Creates the relation for the class:`OffsetTransformer`.

        Parameters
        ----------
        group : list
            List of oemof.solph.custom.OffsetTransformer objects for which
            the relation of inputs and outputs is created
            e.g. group = [ostf1, ostf2, ostf3, ...]. The components inside
            the list need to hold an attribute `coefficients` of type dict
            containing the conversion factors for all inputs to outputs.
        """
        if group is None:
            return None

        m = self.parent_block()

        self.OFFSETTRANSFORMERS = Set(initialize=[n for n in group])

        def _relation_rule(block, n, t):
            """Link binary input and output flow to component outflow."""
            expr = 0
            expr += - m.flow[n, list(n.outputs.keys())[0], t]
            expr += m.flow[list(n.inputs.keys())[0], n, t] * \
                n.coefficients[1][t]
            expr += m.NonConvexFlow.status[list(n.inputs.keys())[0], n, t] * \
                n.coefficients[0][t]
            return expr == 0
        self.relation = Constraint(self.OFFSETTRANSFORMERS, m.TIMESTEPS,
                                   rule=_relation_rule)
