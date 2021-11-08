# -*- coding: utf-8 -*-

"""
solph version of oemof.network.Transformer including
sets, variables, constraints and parts of the objective function
for TransformerBlock objects.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: jmloenneberga

SPDX-License-Identifier: MIT

"""

from pyomo.core import BuildAction
from pyomo.core import Constraint
from pyomo.core.base.block import SimpleBlock

from oemof.network import network as on

from oemof.solph._plumbing import sequence

from oemof.solph._helpers import check_node_object_for_missing_attribute


class Transformer(on.Transformer):
    """A linear TransformerBlock object with n inputs and n outputs.

    Parameters
    ----------
    conversion_factors : dict
        Dictionary containing conversion factors for conversion of each flow.
        Keys are the connected bus objects.
        The dictionary values can either be a scalar or an iterable with length
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
    <class 'oemof.solph.network.transformer.TransformerBlock'>

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
     * :py:class:`~oemof.solph.components.transformer.TransformerBlock`
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        check_node_object_for_missing_attribute(self, "inputs")
        check_node_object_for_missing_attribute(self, "outputs")

        self.conversion_factors = {
            k: sequence(v)
            for k, v in kwargs.get("conversion_factors", {}).items()
        }

        missing_conversion_factor_keys = (
            set(self.outputs) | set(self.inputs)
        ) - set(self.conversion_factors)

        for cf in missing_conversion_factor_keys:
            self.conversion_factors[cf] = sequence(1)

    def constraint_group(self):
        return TransformerBlock


class TransformerBlock(SimpleBlock):
    r"""Block for the linear relation of nodes with type
    :class:`~oemof.solph.network.TransformerBlock`

    **The following sets are created:** (-> see basic sets at
    :class:`.Model` )

    TRANSFORMERS
        A set with all :class:`~oemof.solph.network.TransformerBlock` objects.

    **The following constraints are created:**

    Linear relation :attr:`om.TransformerBlock.relation[i,o,t]`
        .. math::
            \P_{i,n}(t) \times \eta_{n,o}(t) = \
            \P_{n,o}(t) \times \eta_{n,i}(t), \\
            \forall t \in \textrm{TIMESTEPS}, \\
            \forall n \in \textrm{TRANSFORMERS}, \\
            \forall i \in \textrm{INPUTS(n)}, \\
            \forall o \in \textrm{OUTPUTS(n)},

    ======================  ============================  =============
    symbol                  attribute                     explanation
    ======================  ============================  =============
    :math:`P_{i,n}(t)`      `flow[i, n, t]`               TransformerBlock
                                                                  inflow

    :math:`P_{n,o}(t)`      `flow[n, o, t]`               TransformerBlock
                                                                  outflow

    :math:`\eta_{i,n}(t)`   `conversion_factor[i, n, t]`  Conversion
                                                                  efficiency

    ======================  ============================  =============
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """Creates the linear constraint for the class:`TransformerBlock`
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
