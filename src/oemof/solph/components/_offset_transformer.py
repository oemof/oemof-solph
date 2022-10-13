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
SPDX-FileCopyrightText: Saeed Sayadi

SPDX-License-Identifier: MIT

"""

from oemof.network import network
from pyomo.core.base.block import ScalarBlock
from pyomo.environ import Constraint
from pyomo.environ import Set

from oemof.solph._plumbing import sequence as solph_sequence


class OffsetTransformer(network.Transformer):
    """An object with one input and one output.

    Parameters
    ----------

    coefficients : tuple
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
    ...    inputs={bel: solph.flows.Flow()},
    ...    outputs={bth: solph.flows.Flow(
    ...         nominal_value=60, min=0.5, max=1.0,
    ...         nonconvex=solph.NonConvex())},
    ...    coefficients=(20, 0.5))
    >>> type(ostf)
    <class 'oemof.solph.components._offset_transformer.OffsetTransformer'>
    """  # noqa: E501

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if kwargs.get("coefficients") is not None:
            self.coefficients = tuple(
                [solph_sequence(i) for i in kwargs.get("coefficients")]
            )
            if len(self.coefficients) != 2:
                raise ValueError(
                    "Two coefficients or coefficient series have to be given."
                )

        # `OffsetTransformer` always needs the `NonConvex` attribute, but the
        # `Investment` attribute is optional. If it is used, the
        # `InvestNonConvexFlow` will be used in the definition of constraints,
        # otherwise, the `NonConvexFlow` will be used.
        if len(self.outputs):
            for k, v in self.outputs.items():
                if not v.nonconvex:
                    raise TypeError(
                        "Output flow must have the `NonConvex` attribute!"
                    )

        # `Investment` and `NonConvex` attributes cannot be defined for the
        # input flow.
        if len(self.inputs):
            for k, v in self.inputs.items():
                if v.investment:
                    raise TypeError(
                        "`Investment` attribute must be defined only for the "
                        + "output flow!"
                    )
                if v.nonconvex:
                    raise TypeError(
                        "`NonConvex` attribute must be defined only for the "
                        + "output flow!"
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
        P_{in}(t) = C_1(t) \cdot P_{out}(t) + C_0(t) \cdot Y(t) \\


    .. csv-table:: Variables (V) and Parameters (P)
        :header: "symbol", "attribute", "type", "explanation"
        :widths: 1, 1, 1, 1

        ":math:`P_{in}(t)`", "`flow[i, n, t]`", "V","Power of input"
        ":math:`P_{out}(t)`", "`flow[n, o, t]`", "V", "Power of output"
        ":math:`Y(t)`", "`status_nominal[n, o, t]`", "V","multiplication of a
        binary variable (`status` of the output) and a continuous variable
        (`invest` or `nominal_value` of the output)"
        ":math:`C_1(t)`", "`coefficients[1][n, t]`", "P", "linear
        coefficient 1 (slope)"
        ":math:`C_0(t)`", "`coefficients[0][n, t]`", "P", "linear
        coefficient 0 (y-intersection)"

    """

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

        def _relation_rule(block, n, t):
            """Link binary input and output flow to component outflow."""

            expr = 0
            expr += -m.flow[list(n.inputs.keys())[0], n, t]
            expr += (
                m.flow[n, list(n.outputs.keys())[0], t] * n.coefficients[1][t]
            )
            # `Y(t)` in the last term of the constraint
            # (":math:`C_0(t) \cdot Y(t)`") is different for different cases.
            # If both `Investment` and `NonConvex` attributes are used for the
            # `OffsetTransformer`, `Y(t)` would represent the
            # `status_nominal[n,o,t]` in the `InvestNonConvexFlow`.
            # But if only the `NonConvex` attribute is defined for the
            # `OffsetTransformer`, `Y(t)` would correspond to the
            # `status_nominal[n,o,t]` in the `NonConvexFlow`.
            try:
                expr += (
                    m.InvestNonConvexFlowBlock.status_nominal[
                        n, list(n.outputs.keys())[0], t
                    ]
                    * n.coefficients[0][t]
                )
            # `KeyError` occurs when more than one `OffsetTransformer` is
            # defined, and in some of them only the `NonConvex` attribute is
            # considered, while in others both `NonConvex` and `Investment`
            # attributes are defined.
            # `AttributeError` only occurs when the `OffsetTransformer` has
            # only the `NonConvex` attribute, and therefore,
            # `m.InvestNonConvexFlowBlock.status_nominal` (inside the `try`
            # block) does not exist.
            except (KeyError, AttributeError):
                expr += (
                    m.NonConvexFlowBlock.status_nominal[
                        n, list(n.outputs.keys())[0], t
                    ]
                    * n.coefficients[0][t]
                )
            return expr == 0

        self.relation = Constraint(
            self.OFFSETTRANSFORMERS, m.TIMESTEPS, rule=_relation_rule
        )
