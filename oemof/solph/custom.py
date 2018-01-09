# -*- coding: utf-8 -*-

"""This module is designed to hold custom components with their classes and
associated individual constraints (blocks) and groupings. Therefore this
module holds the class definition and the block directly located by each other.
"""

__copyright__ = "oemof developer group"
__license__ = "GPLv3"

from pyomo.core.base.block import SimpleBlock
import pyomo.environ as po
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
     * :py:class:`~oemof.solph.blocks.ElectricalLine`

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
    ------
    * To use this object the connected buses need to be of the type
   `py:class:`~oemof.solph.network.ElectricalBus`.
    * It does not work together with flows that have set the attr.`nonconvex`,
    i.e. unit commitment constraints are not possible
    * Input and output of this component are set equal, therefore just use
    either only the input or the output to parameterize.
    * Default attribute `min` of in/outflows is overwritten by -1 if not set
    differently by the user

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
        self.ELECTRICAL_BUSES = po.Set(initialize=[n for n in m.es.nodes
                                       if isinstance(n, ElectricalBus)])

        def _voltage_angle_bounds(block, b, t):
            return b.v_min, b.v_max
        self.voltage_angle = po.Var(self.ELECTRICAL_BUSES, m.TIMESTEPS,
                                    bounds=_voltage_angle_bounds)

        if True not in [b.slack for b in self.ELECTRICAL_BUSES]:
            # TODO: Make this robust to select the same slack bus for
            # the same problems
            bus = [b for b in self.ELECTRICAL_BUSES][0]
            logging.info("No slack bus set, setting bus {0} as slack bus".format(bus.label))
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

        self.electrical_flow = po.Constraint(group, noruleinit=True)

        self._equate_electrical_flows = po.Constraint(group, noruleinit=True)

        self.electrical_flow_build = po.BuildAction(
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

    Notes
    -----
    The sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.custom.LinkBlock`
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if len(self.inputs) > 2 or len(self.outputs) > 2:
            raise ValueError("Component `Link` must not have more than \
                             2 inputs and 2 outputs!")

        self.conversion_factors = {
            k: sequence(v)
            for k, v in kwargs.get('conversion_factors', {}).items()}


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
            the relation of inputs and outputs is created
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

        self.relation = po.Constraint(group, noruleinit=True)

        self.relation_build = po.BuildAction(rule=_input_output_relation)


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

    Notes
    -----
    The sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.custom.OffsetTransformer`
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

        self.OFFSETTRANSFORMERS = po.Set(initialize=[n for n in group])

        def _relation_rule(block, n, t):
            """Link binary input and output flow to component outflow."""
            expr = 0
            expr += - m.flow[n, list(n.outputs.keys())[0], t]
            expr += m.flow[list(n.inputs.keys())[0], n, t] * \
                n.coefficients[1][t]
            expr += m.NonConvexFlow.status[list(n.inputs.keys())[0], n, t] * \
                n.coefficients[0][t]
            return expr == 0
        self.relation = po.Constraint(self.OFFSETTRANSFORMERS, m.TIMESTEPS,
                                      rule=_relation_rule)


def custom_component_grouping(node):
    if isinstance(node, ElectricalLine):
        return ElectricalLineBlock
    if type(node) is Link:
        return LinkBlock
    if isinstance(node, OffsetTransformer):
        return OffsetTransformerBlock
