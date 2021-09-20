# -*- coding: utf-8 -*-

"""Creating sets, variables, constraints and parts of the objective function
for Transformer objects.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: jmloenneberga

SPDX-License-Identifier: MIT

"""

from pyomo.core import BuildAction
from pyomo.core import Constraint
from pyomo.core.base.block import SimpleBlock


class Transformer(SimpleBlock):
    r"""
    Block for the linear relation of nodes with type
    :class:`~oemof.solph.network.transformer.Transformer`

    **The following constraints are created:**

    Linear relation `om.Transformer.relation[i,o,t]`
        .. math::
            P_{i}(t) \cdot \eta_{o}(t) =
            P_{o}(t) \cdot \eta_{i}(t), \\
            \forall t \in \textrm{TIMESTEPS}, \\
            \forall i \in \textrm{INPUTS}, \\
            \forall o \in \textrm{OUTPUTS}

    While INPUTS is the set of Bus objects connected with the input of the
    Transformer and OUPUTS the set of Bus objects connected with the output of
    the Transformer. The constraint above will be created for all combinations
    of INPUTS and OUTPUTS for all TIMESTEPS. A Transformer with two inflows and
    two outflows for one day with an hourly resolution will lead to 96
    constraints.

    The index :math: n is the index for the Transformer node itself. Therefore,
    a `flow[i, n, t]` is a flow from the Bus i to the Transformer n at
    time step t.

    ======================  ============================  ====================
    symbol                  attribute                     explanation
    ======================  ============================  ====================
    :math:`P_{i}(t)`        `flow[i, n, t]`               Transformer, inflow

    :math:`P_{o}(t)`        `flow[n, o, t]`               Transformer, outflow

    :math:`\eta_{i}(t)`     `conversion_factor[i, n, t]`  Inflow, efficiency

    :math:`\eta_{o}(t)`     `conversion_factor[n, o, t]`  Outflow, efficiency

    ======================  ============================  ====================

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """Creates the linear constraint for the class:`Transformer`
        block.
        Parameters
        ----------
        group : list
            List of oemof.solph.Transformers objects for which
            the linear relation of inputs and outputs is created
            e.g. group = [trsf1, trsf2, trsf3, ...]. Note that the relation
            is created for all existing relations of all inputs and all outputs
            of the transformer. The components inside the list need to hold
            an attribute `conversion_factors` of type dict containing the
            conversion factors for all inputs to outputs.
        """
        if group is None:
            return None

        m = self.parent_block()

        in_flows = {n: [i for i in n.inputs.keys()] for n in group}
        out_flows = {n: [o for o in n.outputs.keys()] for n in group}

        self.relation = Constraint(
            [
                (n, i, o, t)
                for t in m.TIMESTEPS
                for n in group
                for o in out_flows[n]
                for i in in_flows[n]
            ],
            noruleinit=True,
        )

        def _input_output_relation(block):
            for t in m.TIMESTEPS:
                for n in group:
                    for o in out_flows[n]:
                        for i in in_flows[n]:
                            try:
                                lhs = (
                                    m.flow[i, n, t]
                                    * n.conversion_factors[o][t]
                                )
                                rhs = (
                                    m.flow[n, o, t]
                                    * n.conversion_factors[i][t]
                                )
                            except ValueError:
                                raise ValueError(
                                    "Error in constraint creation",
                                    "source: {0}, target: {1}".format(
                                        n.label, o.label
                                    ),
                                )
                            block.relation.add((n, i, o, t), (lhs == rhs))

        self.relation_build = BuildAction(rule=_input_output_relation)
