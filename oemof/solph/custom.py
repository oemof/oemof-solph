# -*- coding: utf-8 -*-
"""
This module is designed to hold custom components with their classes and
associated individual constraints (blocks) and groupings. Therefore this
module holds the class definition and the block directly located by each other.
"""

from pyomo.core.base.block import SimpleBlock
import pyomo.environ as po
import logging

from oemof.solph.network import Bus, Transformer
from oemof.solph.plumbing import sequence


class ElectricalBus(Bus):
    r"""A electrical bus object. Every node has to be connected to Bus. This
    Bus is used in combination with ElectricalLine objects for linear optimal
    power flow (lopf) simulations

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
    based on angle formulation

    Parameters
    ----------
    reactance : float or array of floats
        Reactance of the line to be modelled

    Notes
    ------
    * To use this object the connected buses need to be of the type
   `py:class:`~oemof.solph.network.ElectricalBus`.

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
            if f.min is None:
                f.min = -1
        for f in self.outputs.values():
            if f.min is None:
                f.min = -1

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
            return (b.v_min, b.v_max)
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


def custom_component_grouping(node):
    if isinstance(node, ElectricalLine):
        return ElectricalLineBlock
