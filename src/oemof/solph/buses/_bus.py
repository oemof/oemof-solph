# -*- coding: utf-8 -*-

"""
solph version of oemof.network.bus

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: jmloenneberga

SPDX-License-Identifier: MIT

"""

from oemof.network import network as on

from pyomo.core import BuildAction
from pyomo.core import Constraint
from pyomo.core.base.block import SimpleBlock


class Bus(on.Bus):
    """A balance object. Every node has to be connected to BusBlock.

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.buses.bus.BusBlock`

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.balanced = kwargs.get("balanced", True)

    def constraint_group(self):
        if self.balanced:
            return BusBlock
        else:
            return None


class BusBlock(SimpleBlock):
    r"""Block for all balanced buses.

    **The following constraints are build:**

    BusBlock balance  :attr:`om.BusBlock.balance[i, o, t]`
      .. math::
        \sum_{i \in INPUTS(n)} flow(i, n, t) =
        \sum_{o \in OUTPUTS(n)} flow(n, o, t), \\
        \forall n \in \textrm{BUSES},
        \forall t \in \textrm{TIMESTEPS}.
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
