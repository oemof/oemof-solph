# -*- coding: utf-8 -*-

"""
SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: jmloenneberga
SPDX-FileCopyrightText: Johannes Kochems

SPDX-License-Identifier: MIT

"""

from oemof.network import Node
from pyomo.core import BuildAction
from pyomo.core import Constraint
from pyomo.core.base.block import ScalarBlock


class Bus(Node):
    """A balance object. Every component has to be connected to buses.

    The sum of all inputs of a Bus object must equal the sum of all outputs
    within one time step.

    Attributes
    ----------
    balanced: boolean
        Indicates if bus is balanced, i.e. if the sum of inflows equals to
        the sum of outflows for each timestep; defaults to True

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.buses._bus.BusBlock`

    """

    def __init__(
        self,
        label=None,
        *,
        inputs=None,
        outputs=None,
        balanced=True,
        custom_properties=None,
    ):
        if inputs is None:
            inputs = {}
        if outputs is None:
            outputs = {}
        super().__init__(
            label,
            inputs=inputs,
            outputs=outputs,
            custom_properties=custom_properties,
        )
        self.balanced = balanced

    def constraint_group(self):
        if self.balanced:
            return BusBlock
        else:
            return None


class BusBlock(ScalarBlock):
    r"""Block for all balanced buses.

     The sum of all inputs of a Bus object must equal the sum of all outputs
     within one time step.

     **The following constraints are build:**

     Bus balance: `om.Bus.balance[i, o, t]`
       .. math::
         \sum_{i \in INPUTS(n)} P_{i}(t) =
         \sum_{o \in OUTPUTS(n)} P_{o}(t), \\
         \forall t \in \textrm{TIMESTEPS}, \\
         \forall i \in \textrm{INPUTS}, \\
         \forall o \in \textrm{OUTPUTS}

     While INPUTS is the set of Component objects connected with the input of
     the Bus object and OUPUTS the set of Component objects connected with the
     output of the Bus object.

     The index :math:`n` is the index for the Bus node itself. Therefore,
     a :math:`flow[i, n, t]` is a flow from the Component i to the Bus n at
     time index p, t.

     ======================  =========================  ====================
     symbol                  attribute                  explanation
     ======================  =========================  ====================
     :math:`P_{i}(p, t)`     `flow[i, n, t]`            Bus, inflow

     :math:`P_{o}(p, t)`     `flow[n, o, t]`            Bus, outflow

     ======================  =========================  ====================
     """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """Creates the balance constraints for the class:`BusBlock` block.

        Parameters
        ----------
        group : list
            List of oemof bus (b) object for which the bus balance is created
            e.g. group = [b1, b2, b3, .....]
        """
        if group is None:
            return None

        m = self.parent_block()

        ins = {}
        outs = {}
        for n in group:
            ins[n] = [i for i in n.inputs]
            outs[n] = [o for o in n.outputs]

        def _busbalance_rule(block):
            for t in m.TIMESTEPS:
                for g in group:
                    lhs = sum(m.flow[i, g, t] for i in ins[g])
                    rhs = sum(m.flow[g, o, t] for o in outs[g])
                    expr = lhs == rhs
                    # no inflows no outflows yield: 0 == 0 which is True
                    if expr is not True:
                        block.balance.add((g, t), expr)

        self.balance = Constraint(group, m.TIMESTEPS, noruleinit=True)
        self.balance_build = BuildAction(rule=_busbalance_rule)
