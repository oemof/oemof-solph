# -*- coding: utf-8 -*-

"""
In-development electrical line components.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Johannes Röder
SPDX-FileCopyrightText: jakob-wo
SPDX-FileCopyrightText: gplssm
SPDX-FileCopyrightText: jnnr

SPDX-License-Identifier: MIT

"""

import logging

from pyomo.core.base.block import SimpleBlock
from pyomo.environ import BuildAction
from pyomo.environ import Constraint
from pyomo.environ import Set
from pyomo.environ import Var

from oemof.solph.network import Bus
from oemof.solph.network import Flow
from oemof.solph.plumbing import sequence as solph_sequence


class ElectricalBus(Bus):
    r"""A electrical bus object. Every node has to be connected to Bus. This
    Bus is used in combination with ElectricalLine objects for linear optimal
    power flow (lopf) calculations.

    Parameters
    ----------
    slack: boolean
        If True Bus is slack bus for network
    v_max: numeric
        Maximum value of voltage angle at electrical bus
    v_min: numeric
        Mininum value of voltag angle at electrical bus

    Note: This component is experimental. Use it with care.

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.bus.Bus`
    The objects are also used inside:
     * :py:class:`~oemof.solph.custom.electrical_line.ElectricalLine`

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slack = kwargs.get("slack", False)
        self.v_max = kwargs.get("v_max", 1000)
        self.v_min = kwargs.get("v_min", -1000)


class ElectricalLine(Flow):
    r"""An ElectricalLine to be used in linear optimal power flow calculations.
    based on angle formulation. Check out the Notes below before using this
    component!

    Parameters
    ----------
    reactance : float or array of floats
        Reactance of the line to be modelled

    Note: This component is experimental. Use it with care.

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
     * :py:class:`~oemof.solph.custom.electrical_line.ElectricalLineBlock`

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reactance = solph_sequence(kwargs.get("reactance", 0.00001))

        # set input / output flow values to -1 by default if not set by user
        if self.nonconvex is not None:
            raise ValueError(
                (
                    "Attribute `nonconvex` must be None for "
                    + "component `ElectricalLine` from {} to {}!"
                ).format(self.input, self.output)
            )
        if self.min is None:
            self.min = -1
        # to be used in grouping for all bidi flows
        self.bidirectional = True

    def constraint_group(self):
        return ElectricalLineBlock


class ElectricalLineBlock(SimpleBlock):
    r"""Block for the linear relation of nodes with type
    class:`.ElectricalLine`

    Note: This component is experimental. Use it with care.

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
        """Creates the linear constraint for the class:`ElectricalLine`
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

        # create voltage angle variables
        self.ELECTRICAL_BUSES = Set(
            initialize=[n for n in m.es.nodes if isinstance(n, ElectricalBus)]
        )

        def _voltage_angle_bounds(block, b, t):
            return b.v_min, b.v_max

        self.voltage_angle = Var(
            self.ELECTRICAL_BUSES, m.TIMESTEPS, bounds=_voltage_angle_bounds
        )

        if True not in [b.slack for b in self.ELECTRICAL_BUSES]:
            # TODO: Make this robust to select the same slack bus for
            # the same problems
            bus = [b for b in self.ELECTRICAL_BUSES][0]
            logging.info(
                "No slack bus set,setting bus {0} as slack bus".format(
                    bus.label
                )
            )
            bus.slack = True

        def _voltage_angle_relation(block):
            for t in m.TIMESTEPS:
                for n in group:
                    if n.input.slack is True:
                        self.voltage_angle[n.output, t].value = 0
                        self.voltage_angle[n.output, t].fix()
                    try:
                        lhs = m.flow[n.input, n.output, t]
                        rhs = (
                            1
                            / n.reactance[t]
                            * (
                                self.voltage_angle[n.input, t]
                                - self.voltage_angle[n.output, t]
                            )
                        )
                    except ValueError:
                        raise ValueError(
                            "Error in constraint creation",
                            "of node {}".format(n.label),
                        )
                    block.electrical_flow.add((n, t), (lhs == rhs))

        self.electrical_flow = Constraint(group, m.TIMESTEPS, noruleinit=True)

        self.electrical_flow_build = BuildAction(rule=_voltage_angle_relation)
