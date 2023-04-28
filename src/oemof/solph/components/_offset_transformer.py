# -*- coding: utf-8 -

"""
OffsetTransformer and associated individual constraints (blocks) and groupings.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: FranziPl
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: FabianTU
SPDX-FileCopyrightText: Johannes Röder
SPDX-FileCopyrightText: Johannes Kochems

SPDX-License-Identifier: MIT

"""

from oemof.network import network
from pyomo.core.base.block import ScalarBlock
from pyomo.environ import Constraint
from pyomo.environ import Set

from oemof.solph._plumbing import sequence


class OffsetTransformer(network.Transformer):
    """An object with one input and one output and two coefficients to model
    part load behaviour.

    Parameters
    ----------
    coefficients : tuple, (:math:`C_0(t)`, :math:`C_1(t)`)
        Tuple containing the first two polynomial coefficients
        i.e. the y-intersection and slope of a linear equation.
        The tuple values can either be a scalar or a sequence with length
        of time horizon for simulation.

    Notes
    -----
    The sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.components._offset_transformer.OffsetTransformerBlock`

    Examples
    --------

    >>> from oemof import solph

    >>> bel = solph.buses.Bus(label='bel')
    >>> bth = solph.buses.Bus(label='bth')

    >>> ostf = solph.components.OffsetTransformer(
    ...    label='ostf',
    ...    inputs={bel: solph.flows.Flow(
    ...        nominal_value=60, min=0.5, max=1.0,
    ...        nonconvex=solph.NonConvex())},
    ...    outputs={bth: solph.flows.Flow()},
    ...    coefficients=(20, 0.5))

    >>> type(ostf)
    <class 'oemof.solph.components._offset_transformer.OffsetTransformer'>
    """  # noqa: E501

    def __init__(
        self,
        inputs,
        outputs,
        label=None,
        coefficients=None,
        custom_attributes=None,
    ):
        if custom_attributes is None:
            custom_attributes = {}
        super().__init__(
            inputs=inputs,
            outputs=outputs,
            label=label,
            **custom_attributes,
        )

        if coefficients is not None:
            self.coefficients = tuple([sequence(i) for i in coefficients])
            if len(self.coefficients) != 2:
                raise ValueError(
                    "Two coefficients or coefficient series have to be given."
                )

        if len(self.inputs) == 1:
            for k, v in self.inputs.items():
                if not v.nonconvex:
                    raise TypeError(
                        "Input flows must have NonConvex attribute!"
                    )

        if len(self.inputs) > 1 or len(self.outputs) > 1:
            raise ValueError(
                "Component `OffsetTransformer` must not have "
                + "more than 1 input and 1 output!"
            )

    def constraint_group(self):
        return OffsetTransformerBlock


class OffsetTransformerBlock(ScalarBlock):
    r"""Block for the relation of nodes with type
    :class:`~oemof.solph.components._offset_transformer.OffsetTransformer`

    **The following constraints are created:**

    .. _OffsetTransformer-equations:

    .. math::
        &
        P_{out}(p, t) = C_1(t) \cdot P_{in}(p, t) + C_0(t) \cdot Y(t) \\


    The symbols used are defined as follows (with Variables (V) and Parameters (P)):

    +--------------------+------------------------+------+--------------------------------------------+
    | symbol             | attribute              | type | explanation                                |
    +====================+========================+======+============================================+
    | :math:`P_{out}(t)` | `flow[n,o,p,t]`        | V    | Outflow of transformer                     |
    +--------------------+------------------------+------+--------------------------------------------+
    | :math:`P_{in}(t)`  | `flow[i,n,p,t]`        | V    | Inflow of transformer                      |
    +--------------------+------------------------+------+--------------------------------------------+
    | :math:`Y(t)`       | `status[i,n,t]`        | V    | Binary status variable of nonconvex inflow |
    +--------------------+------------------------+------+--------------------------------------------+
    | :math:`C_1(t)`     | `coefficients[1][n,t]` | P    | Linear coefficient 1 (slope)               |
    +--------------------+------------------------+------+--------------------------------------------+
    | :math:`C_0(t)`     | `coefficients[0][n,t]` | P    | Linear coefficient 0 (y-intersection)      |
    +--------------------+------------------------+------+--------------------------------------------+
    """  # noqa: E501
    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """Creates the relation for the class:`OffsetTransformer`.

        Parameters
        ----------
        group : list
            List of oemof.solph.experimental.OffsetTransformer objects for
            which the relation of inputs and outputs is created
            e.g. group = [ostf1, ostf2, ostf3, ...]. The components inside
            the list need to hold an attribute `coefficients` of type dict
            containing the conversion factors for all inputs to outputs.
        """
        if group is None:
            return None

        m = self.parent_block()

        self.OFFSETTRANSFORMERS = Set(initialize=[n for n in group])

        def _relation_rule(block, n, p, t):
            """Link binary input and output flow to component outflow."""
            expr = 0
            expr += -m.flow[n, list(n.outputs.keys())[0], p, t]
            expr += (
                m.flow[list(n.inputs.keys())[0], n, p, t]
                * n.coefficients[1][t]
            )
            expr += (
                m.NonConvexFlowBlock.status[list(n.inputs.keys())[0], n, t]
                * n.coefficients[0][t]
            )
            return expr == 0

        self.relation = Constraint(
            self.OFFSETTRANSFORMERS, m.TIMEINDEX, rule=_relation_rule
        )
