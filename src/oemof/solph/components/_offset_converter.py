# -*- coding: utf-8 -

"""
OffsetConverter and associated individual constraints (blocks) and groupings.

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
SPDX-FileCopyrightText: Johannes Kochems

SPDX-License-Identifier: MIT

"""

from warnings import warn

from oemof.network import Node
from pyomo.core import BuildAction
from pyomo.core.base.block import ScalarBlock
from pyomo.environ import Constraint
from pyomo.environ import Set

from oemof.solph._plumbing import sequence


class OffsetConverter(Node):
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
     * :py:class:`~oemof.solph.components._offset_converter.OffsetConverterBlock`

    Examples
    --------
    >>> from oemof import solph
    >>> bel = solph.buses.Bus(label='bel')
    >>> bth = solph.buses.Bus(label='bth')
    >>> ostf = solph.components.OffsetConverter(
    ...    label='ostf',
    ...    inputs={bel: solph.flows.Flow()},
    ...    outputs={bth: solph.flows.Flow(
    ...         nominal_value=60, min=0.5, max=1.0,
    ...         nonconvex=solph.NonConvex())},
    ...    coefficients=(20, 0.5))
    >>> type(ostf)
    <class 'oemof.solph.components._offset_converter.OffsetConverter'>
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

        # `OffsetConverter` always needs the `NonConvex` attribute, but the
        # `Investment` attribute is optional. If it is used, the
        # `InvestNonConvexFlow` will be used in the definition of constraints,
        # otherwise, the `NonConvexFlow` will be used.
        if len(self.outputs):
            for v in self.outputs.values():
                if not v.nonconvex:
                    raise TypeError(
                        "Output flow must have the `NonConvex` attribute!"
                    )

        # `Investment` and `NonConvex` attributes cannot be defined for the
        # input flow.
        if len(self.inputs):
            for v in self.inputs.values():
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
                "Component `OffsetConverter` must not have "
                + "more than 1 input and 1 output!"
            )

    def constraint_group(self):
        return OffsetConverterBlock


# --- BEGIN: To be removed for versions >= v0.6 ---
class OffsetTransformer(OffsetConverter):
    def __init__(
        self,
        inputs,
        outputs,
        label=None,
        coefficients=None,
        custom_attributes=None,
    ):
        super().__init__(
            label=label,
            inputs=inputs,
            outputs=outputs,
            coefficients=coefficients,
            custom_attributes=custom_attributes,
        )
        warn(
            "solph.components.OffsetTransformer has been renamed to"
            " solph.components.OffsetConverter. The transitional wrapper"
            " will be deleted in the future.",
            FutureWarning,
        )


# --- END ---


class OffsetConverterBlock(ScalarBlock):
    r"""Block for the relation of nodes with type
    :class:`~oemof.solph.components._offset_converter.OffsetConverter`

    **The following constraints are created:**

    .. _OffsetConverter-equations:

    .. math::
        &
        P_{in}(p, t) = C_1(t) \cdot P_{out}(p, t) + C_0(t) \cdot P_max(p) \cdot Y(t) \\


    The symbols used are defined as follows (with Variables (V) and Parameters (P)):

    +--------------------+------------------------+------+--------------------------------------------+
    | symbol             | attribute              | type | explanation                                |
    +====================+========================+======+============================================+
    | :math:`P_{out}(t)` | `flow[n,o,p,t]`        | V    | Outflow of converter                       |
    +--------------------+------------------------+------+--------------------------------------------+
    | :math:`P_{in}(t)`  | `flow[i,n,p,t]`        | V    | Inflow of converter                        |
    +--------------------+------------------------+------+--------------------------------------------+
    | :math:`Y(t)`       |                        | V    | Binary status variable of nonconvex inflow |
    +--------------------+------------------------+------+--------------------------------------------+
    | :math:`P_{max}(t)` |                        | V    | Maximum Outflow of converter               |
    +--------------------+------------------------+------+--------------------------------------------+
    | :math:`C_1(t)`     | `coefficients[1][n,t]` | P    | Linear coefficient 1 (slope)               |
    +--------------------+------------------------+------+--------------------------------------------+
    | :math:`C_0(t)`     | `coefficients[0][n,t]` | P    | Linear coefficient 0 (y-intersection)      |
    +--------------------+------------------------+------+--------------------------------------------+

    Note that :math:`P_{max}(t) \cdot Y(t)` is merged into one variable,
    called `status_nominal[n, o, p, t]`.
    """  # noqa: E501
    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """Creates the relation for the class:`OffsetConverter`.

        Parameters
        ----------
        group : list
            List of oemof.solph.experimental.OffsetConverter objects for
            which the relation of inputs and outputs is created
            e.g. group = [ostf1, ostf2, ostf3, ...]. The components inside
            the list need to hold an attribute `coefficients` of type dict
            containing the conversion factors for all inputs to outputs.
        """
        if group is None:
            return None

        m = self.parent_block()

        self.OFFSETCONVERTERS = Set(initialize=[n for n in group])

        in_flows = {n: [i for i in n.inputs.keys()] for n in group}
        out_flows = {n: [o for o in n.outputs.keys()] for n in group}

        self.relation = Constraint(
            [
                (n, i, o, p, t)
                for p, t in m.TIMEINDEX
                for n in group
                for o in out_flows[n]
                for i in in_flows[n]
            ],
            noruleinit=True,
        )

        def _relation_rule(block):
            """Link binary input and output flow to component outflow."""
            for p, t in m.TIMEINDEX:
                for n in group:
                    for o in out_flows[n]:
                        for i in in_flows[n]:
                            expr = 0
                            expr += -m.flow[n, o, p, t]
                            expr += m.flow[i, n, p, t] * n.coefficients[1][t]
                            # `Y(t)` in the last term of the constraint
                            # (":math:`C_0(t) \cdot Y(t)`") is different for
                            # different cases. If both `Investment` and
                            # `NonConvex` attributes are used for the
                            # `OffsetConverter`, `Y(t)` would represent the
                            # `status_nominal[n,o,t]` in the
                            # `InvestNonConvexFlow`. But if only the
                            # `NonConvex` attribute is defined for the
                            # `OffsetConverter`, `Y(t)` would correspond to
                            # the `status_nominal[n,o,t]` in the
                            # `NonConvexFlow`.
                            try:
                                expr += (
                                    m.InvestNonConvexFlowBlock.status_nominal[
                                        n, o, t
                                    ]
                                    * n.coefficients[0][t]
                                )
                            # `KeyError` occurs when more than one
                            # `OffsetConverter` is defined, and in some of
                            # them only the `NonConvex` attribute is
                            # considered, while in others both `NonConvex`
                            # and `Investment` attributes are defined.
                            # `AttributeError` only occurs when the
                            # `OffsetConverter` has only the `NonConvex`
                            # attribute, and therefore,
                            # `m.InvestNonConvexFlowBlock.status_nominal`
                            # (inside the `try` block) does not exist.
                            except (KeyError, AttributeError):
                                expr += (
                                    m.NonConvexFlowBlock.status_nominal[
                                        n, o, t
                                    ]
                                    * n.coefficients[0][t]
                                )
                            block.relation.add((n, i, o, p, t), (expr == 0))

        self.relation_build = BuildAction(rule=_relation_rule)
