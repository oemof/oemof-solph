# -*- coding: utf-8 -*-

"""
solph version of oemof.network.Converter including
sets, variables, constraints and parts of the objective function
for ConverterBlock objects.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: jmloenneberga
SPDX-FileCopyrightText: David Fuhrländer
SPDX-FileCopyrightText: Johannes Röder
SPDX-FileCopyrightText: Johannes Kochems

SPDX-License-Identifier: MIT

"""

from oemof.network import Node
from pyomo.core import BuildAction
from pyomo.core import Constraint
from pyomo.core.base.block import ScalarBlock

from oemof.solph._helpers import warn_if_missing_attribute
from oemof.solph._plumbing import sequence


class Converter(Node):
    """A linear ConverterBlock object with n inputs and n outputs.

    Node object that relates any number of inflow and outflows with
    conversion factors. Inputs and outputs must be given as dictinaries.

    Parameters
    ----------
    inputs : dict
        Dictionary with inflows. Keys must be the starting node(s) of the
        inflow(s).
    outputs : dict
        Dictionary with outflows. Keys must be the ending node(s) of the
        outflow(s).
    conversion_factors : dict
        Dictionary containing conversion factors for conversion of each flow.
        Keys must be the connected nodes (typically Buses).
        The dictionary values can either be a scalar or an iterable with
        individual conversion factors for each time step.
        Default: 1. If no conversion_factor is given for an in- or outflow, the
        conversion_factor is set to 1.

    Examples
    --------
    Defining an linear converter:

    >>> from oemof import solph
    >>> bgas = solph.buses.Bus(label='natural_gas')
    >>> bcoal = solph.buses.Bus(label='hard_coal')
    >>> bel = solph.buses.Bus(label='electricity')
    >>> bheat = solph.buses.Bus(label='heat')

    >>> trsf = solph.components.Converter(
    ...    label='pp_gas_1',
    ...    inputs={bgas: solph.flows.Flow(), bcoal: solph.flows.Flow()},
    ...    outputs={bel: solph.flows.Flow(), bheat: solph.flows.Flow()},
    ...    conversion_factors={bel: 0.3, bheat: 0.5,
    ...                        bgas: 0.8, bcoal: 0.2})
    >>> print(sorted([x[1][5] for x in trsf.conversion_factors.items()]))
    [0.2, 0.3, 0.5, 0.8]

    >>> type(trsf)
    <class 'oemof.solph.components._converter.Converter'>

    >>> sorted([str(i) for i in trsf.inputs])
    ['hard_coal', 'natural_gas']

    >>> trsf_new = solph.components.Converter(
    ...    label='pp_gas_2',
    ...    inputs={bgas: solph.flows.Flow()},
    ...    outputs={bel: solph.flows.Flow(), bheat: solph.flows.Flow()},
    ...    conversion_factors={bel: 0.3, bheat: 0.5})
    >>> trsf_new.conversion_factors[bgas][3]
    1

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.components._converter.ConverterBlock`
    """

    def __init__(
        self,
        label=None,
        inputs=None,
        outputs=None,
        conversion_factors=None,
        custom_properties=None,
    ):
        if inputs is None:
            inputs = {}
        if outputs is None:
            outputs = {}
        if custom_properties is None:
            custom_properties = {}

        super().__init__(
            label=label,
            inputs=inputs,
            outputs=outputs,
            custom_properties=custom_properties,
        )
        if not inputs:
            warn_if_missing_attribute(self, "inputs")
        if not outputs:
            warn_if_missing_attribute(self, "outputs")

        if conversion_factors is None:
            conversion_factors = {}

        self.conversion_factors = {
            k: sequence(v) for k, v in conversion_factors.items()
        }

        missing_conversion_factor_keys = (
            set(self.outputs) | set(self.inputs)
        ) - set(self.conversion_factors)

        for cf in missing_conversion_factor_keys:
            self.conversion_factors[cf] = sequence(1)

    def constraint_group(self):
        return ConverterBlock


class ConverterBlock(ScalarBlock):
    r"""Block for the linear relation of nodes with type
    :class:`~oemof.solph.components._converter.ConverterBlock`

    **The following sets are created:** (-> see basic sets at
    :class:`.Model` )

    CONVERTERS
        A set with all
        :class:`~oemof.solph.components._converter.Converter` objects.

    **The following constraints are created:**

    Linear relation :attr:`om.ConverterBlock.relation[i,o,t]`
        .. math::
            P_{i}(t) \cdot \eta_{o}(t) =
            P_{o}(t) \cdot \eta_{i}(t), \\
            \forall t \in \textrm{TIMESTEPS}, \\
            \forall n \in \textrm{CONVERTERS}, \\
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
    time index p, t.

    ======================  ============================  ====================
    symbol                  attribute                     explanation
    ======================  ============================  ====================
    :math:`P_{i,n}(p, t)`   `flow[i, n, t]`               Converter, inflow

    :math:`P_{n,o}(p, t)`   `flow[n, o, t]`               Converter, outflow

    :math:`\eta_{i}(t)`     `conversion_factor[i, n, t]`  Inflow, efficiency

    :math:`\eta_{o}(t)`     `conversion_factor[n, o, t]`  Outflow, efficiency

    ======================  ============================  ====================

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """Creates the linear constraint for the class:`ConverterBlock`
        block.

        Parameters
        ----------

        group : list
            List of oemof.solph.components.Converters objects for which
            the linear relation of inputs and outputs is created
            e.g. group = [trsf1, trsf2, trsf3, ...]. Note that the relation
            is created for all existing relations of all inputs and all outputs
            of the converter. The components inside the list need to hold
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
