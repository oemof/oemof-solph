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
    """An object with one input and multiple outputs and two coefficients
    per output to model part load behaviour.
    The output must contain a NonConvex object.

    Parameters
    ----------
    coefficients : dict of tuples, (:math:`C_0(t)`, :math:`C_1(t)`)
        Dict of tuples containing the respective output bus as key and
        as value a tuple with the parameters :math:`C_0(t)` and :math:`C_1(t)`.
        Here, :math:`C_1(t)` represents the slope of a linear equation and
        :math:`C_0(t)` is the y-intercept devided by the `nominal_value` of the
        output flow (this is for internal purposes).

        The tuple values can either be a scalar or a sequence with length
        of time horizon for simulation.

    Notes
    -----
    **C_1 and C_0 can be calculated as follows:**

    .. _OffsetConverterCoefficients-equations:

    .. math::

        C_1 = (l_{max}-l_{min})/(l_{max}/\\eta_{max}-l_{min}/\\eta_{min})

        C_0 = l_{min} \\cdot (1-C_1/\\eta_{min})

    Where :math:`l_{max}` and :math:`l_{min}` are the maximum and minimum
    partload share (e.g. 1.0 and 0.3) and :math:`\\eta_{max}` and
    :math:`\\eta_{min}` are the efficiencies/conversion factors at these
    partloads.

    The sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.components._offset_converter.OffsetConverterBlock`

    Examples
    --------
    >>> from oemof import solph
    >>> bel = solph.buses.Bus(label='bel')
    >>> bth = solph.buses.Bus(label='bth')
    >>> l_max = 1
    >>> l_min = 0.5
    >>> eta_max = 0.5
    >>> eta_min = 0.3
    >>> c1 = (l_max-l_min)/(l_max/eta_max-l_min/eta_min)
    >>> c0 = l_min*(1-c1/eta_min)
    >>> ostf = solph.components.OffsetConverter(
    ...    label='ostf',
    ...    inputs={bel: solph.flows.Flow()},
    ...    outputs={bth: solph.flows.Flow(
    ...         nominal_value=60, min=l_min, max=l_max,
    ...         nonconvex=solph.NonConvex())},
    ...    coefficients={bth: (c0, c1)}
    ... )
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
            custom_properties=custom_attributes,
        )

        if coefficients is not None:
            self.coefficients = dict()
            if isinstance(coefficients, tuple):
                # TODO: add the correct version in the message
                msg = (
                    "Passing a tuple to the keyword `coefficients` will be"
                    " deprecated in a later version. Please use a dict to"
                    " specify the corresponding output flow. The first output"
                    " flow will be assumed as target by default."
                )
                warn(msg, DeprecationWarning)
                if len(coefficients) != 2:
                    raise ValueError(
                        "Two coefficients or coefficient series have to be"
                        " given."
                    )
                self.coefficients.update(
                    {
                        [k for k in self.outputs.keys()][0]: tuple(
                            [sequence(i) for i in coefficients]
                        )
                    }
                )
            elif isinstance(coefficients, dict):
                for k, v in coefficients.items():
                    if len(v) != 2:
                        raise ValueError(
                            "Two coefficients or coefficient series have to be"
                            " given."
                        )
                    self.coefficients.update(
                        {k: (sequence(v[0]), sequence(v[1]))}
                    )
            else:
                raise TypeError(
                    "`coefficiencts` needs to be either dict or tuple"
                    " (deprecated)."
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

        if len(self.inputs) > 1:
            raise ValueError(
                "Component `OffsetConverter` must not have more than 1 input!"
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
        P_{out}(p, t) = P_{in}(p, t) \cdot C_1(t) + P_nom(p) \cdot Y(t) \cdot C_0(t) \\


    The symbols used are defined as follows (with Variables (V) and Parameters (P)):

    +--------------------+---------------------------+------+--------------------------------------------------+
    | symbol             | attribute                 | type | explanation                                      |
    +====================+===========================+======+==================================================+
    | :math:`P_{out}(t)` | `flow[n,o,p,t]`           | V    | Outflow of converter                             |
    +--------------------+---------------------------+------+--------------------------------------------------+
    | :math:`P_{in}(t)`  | `flow[i,n,p,t]`           | V    | Inflow of converter                              |
    +--------------------+---------------------------+------+--------------------------------------------------+
    | :math:`Y(t)`       |                           | V    | Binary status variable of nonconvex outflow      |
    +--------------------+---------------------------+------+--------------------------------------------------+
    | :math:`P_{nom}(t)` |                           | V    | Nominal value (max. capacity) of the outflow     |
    +--------------------+---------------------------+------+--------------------------------------------------+
    | :math:`C_1(t)`     | `coefficients[o][1][n,t]` | P    | Linear coefficient 1 (slope)                     |
    +--------------------+---------------------------+------+--------------------------------------------------+
    | :math:`C_0(t)`     | `coefficients[o][0][n,t]` | P    | Linear coefficient 0 (y-intersection)/P_{nom}(t) |
    +--------------------+---------------------------+------+--------------------------------------------------+

    Note that :math:`P_{nom}(t) \cdot Y(t)` is merged into one variable,
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
                (n, i, o, t)
                for t in m.TIMESTEPS
                for n in group
                for o in out_flows[n]
                for i in in_flows[n]
            ],
            noruleinit=True,
        )

        def _relation_rule(block):
            """Link binary input and output flow to component outflow."""
            for t in m.TIMESTEPS:
                for n in group:
                    for o in out_flows[n]:
                        for i in in_flows[n]:
                            expr = 0
                            expr += -m.flow[n, o, t]
                            expr += m.flow[i, n, t] * n.coefficients[o][1][t]
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
                                    * n.coefficients[o][0][t]
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
                                    * n.coefficients[o][0][t]
                                )
                            block.relation.add((n, i, o, t), (expr == 0))

        self.relation_build = BuildAction(rule=_relation_rule)
