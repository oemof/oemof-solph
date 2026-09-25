# -*- coding: utf-8 -*-

"""
VariableSplitConverter and associated individual constraints (blocks)
and groupings.

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

from pyomo.core.base.block import ScalarBlock
from pyomo.environ import BuildAction
from pyomo.environ import Constraint
from pyomo.environ import Set

from oemof.solph._plumbing import Apply
from oemof.solph._plumbing import SequenceDict
from oemof.solph._plumbing import sequence
from oemof.solph.components import Converter


def _conversion_points_are_equal(point_1, point_2):
    """Check whether two conversion factor dicts are identical for all
    shared keys (same outputs, same values at every timestep)."""
    if set(point_1) != set(point_2):
        return False
    return all(point_1[k] == point_2[k] for k in point_1)


class VariableSplitConverter(Converter):
    r"""
    A converter with one input and two competing outputs, where the split
    between the outputs can vary linearly between two given, real
    operating points (e.g. an extraction/backpressure turbine, where the
    split between electricity and heat varies with the amount of heat
    extracted).

    The linear relation between the two output flows and the input flow is
    fully determined by **two real, measurable operating points**. At each
    point, conversion factors for *both* outputs must be given. Which point
    is passed as `conversion_factors` and which as
    `conversion_factors_at_second_point` does **not matter** -- the
    underlying relation is a straight line through both points and is
    computed symmetrically. Likewise, it does not matter which of the two
    outputs is listed first; both outputs are treated symmetrically.

    Note that neither point needs to correspond to a "degenerate" case
    (e.g. zero output of one flow, such as full condensation in a turbine)
    -- the converter will never operate outside the interval spanned by the
    two given points.

    Parameters
    ----------
    conversion_factors : dict
        Conversion factors for **both** outputs at the first operating
        point. Keys are the two output bus objects. Values can be scalar
        or a sequence with length of the simulation's time horizon.
    conversion_factors_secondary_state : dict
        Conversion factors for **both** outputs at the second operating
        point. Same structure as `conversion_factors`. Must use the same
        two output bus objects as keys.

    Notes
    -----
    The following sets, variables, constraints and objective parts are
    created:
     * :py:class:`~oemof.solph.components.variable_split_converter.VariableSplitConverterBlock`

    Examples
    --------
    Extraction turbine CHP (electricity / heat trade-off):

    >>> from oemof import solph
    >>> bel = solph.buses.Bus(label='electricityBus')
    >>> bth = solph.buses.Bus(label='heatBus')
    >>> bgas = solph.buses.Bus(label='commodityBus')
    >>> et_chp = solph.components.VariableSplitConverter(
    ...    label='variable_chp_gas',
    ...    inputs={bgas: solph.flows.Flow(nominal_capacity=10e10)},
    ...    outputs={bel: solph.flows.Flow(), bth: solph.flows.Flow()},
    ...    conversion_factors={bel: 0.30, bth: 0.50},
    ...    conversion_factors_secondary_state={bel: 0.48, bth: 0.10})
    """  # noqa: E501

    conversion_factors_secondary_state = Apply(SequenceDict)
    conversion_factors = Apply(SequenceDict)

    def __init__(
        self,
        label=None,
        inputs=None,
        outputs=None,
        parent_node=None,
        conversion_factors=None,
        conversion_factors_secondary_state=None,
        custom_properties=None,
        allow_equal_states=False,
    ):
        super().__init__(
            label=label,
            inputs=inputs,
            outputs=outputs,
            parent_node=parent_node,
            conversion_factors=conversion_factors,
            custom_properties=custom_properties,
        )
        self.conversion_factors_secondary_state = (
            conversion_factors_secondary_state
        )
        self.allow_equal_states = allow_equal_states

        if set(conversion_factors_secondary_state) != set(conversion_factors):
            raise ValueError("Use the same buses for both states.")
        try:
            length = len(
                conversion_factors_secondary_state[
                    list(conversion_factors_secondary_state.keys())[0]
                ]
            )
            if not allow_equal_states and any(
                [
                    any(
                        sequence(conversion_factors[k], length)
                        == sequence(
                            conversion_factors_secondary_state[k], length
                        )
                    )
                    for k in conversion_factors
                ]
            ):
                raise ValueError("That is not okay.")
        except TypeError:
            if not allow_equal_states and any(
                [
                    conversion_factors[k]
                    == conversion_factors_secondary_state[k]
                    for k in conversion_factors
                ]
            ):
                raise ValueError("That is not okay.")

    def constraint_group(self):
        return VariableSplitConverterBlock


class VariableSplitConverterBlock(ScalarBlock):
    r"""Block for all instances of
    :class:`~oemof.solph.components.experimental._VariableSplitConverter`

    **Variables**

    * :math:`\dot H_{in}`

        Input flow, represented in code as `flow[i, n, t]`

    * :math:`A`

        First output flow, represented in code as `flow[n, output_1, t]`

    * :math:`B`

        Second output flow, represented in code as `flow[n, output_2, t]`

    **Parameters**

    Given (real, measurable) operating points -- `output_1`/`output_2` are
    simply the two dictionary keys of `conversion_factors` in iteration
    order; which physical flow ends up as `output_1` is arbitrary and does
    not affect the result:

    * :math:`a_1, b_1`

        Conversion factors for output_1 / output_2 at the first point,
        `conversion_factors[output_1][n, t]` /
        `conversion_factors[output_2][n, t]`.

    * :math:`a_2, b_2`

        Conversion factors for output_1 / output_2 at the second point,
        `conversion_factors_at_second_point[output_1][n, t]` /
        `conversion_factors_at_second_point[output_2][n, t]`.

    Derived (computed internally in :py:meth:`_create`, no division
    involved):

    .. math::
        c_A(t) &= b_1(t) - b_2(t) \\
        c_B(t) &= a_2(t) - a_1(t) \\
        c_{in}(t) &= a_2(t)\, b_1(t) - a_1(t)\, b_2(t)

    **Constraints**

        .. math::
            &
            (1)\ c_A(t)\cdot A(t) + c_B(t)\cdot B(t) = c_{in}(t)\cdot
                \dot H_{in}(t) \\
            &
            (2)\ \min(b_1(t), b_2(t))\cdot \dot H_{in}(t) \leq B(t) \\
            &
            (3)\ B(t) \leq \max(b_1(t), b_2(t))\cdot \dot H_{in}(t)

    Equation (1) is the (symmetric) line through both given operating
    points. Equations (2) and (3) restrict operation to the interval
    spanned by the two points -- the converter can never move beyond
    either of them.

    ============ ======================================================== ==== =========
    symbol       attribute                                                type explanation
    ============ ======================================================== ==== =========
    :math:`\dot H_{in}` `flow[i, n, t]`                                   V    input flow
    :math:`A`    `flow[n, output_1, t]`                                   V    first output flow
    :math:`B`    `flow[n, output_2, t]`                                   V    second output flow
    :math:`a_1`  `conversion_factors[output_1][n, t]`                     P    efficiency of output_1 at point 1
    :math:`b_1`  `conversion_factors[output_2][n, t]`                     P    efficiency of output_2 at point 1
    :math:`a_2`  `conversion_factors_at_second_point[output_1][n, t]`     P    efficiency of output_1 at point 2
    :math:`b_2`  `conversion_factors_at_second_point[output_2][n, t]`     P    efficiency of output_2 at point 2
    ============ ======================================================== ==== =========

    """  # noqa: E501

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """Creates the constraints for
        :class:`oemof.solph.components.experimental._variable_split_converter.VariableSplitConverterBlock`.

        Parameters
        ----------
        group : list
            List of
            :class:`oemof.solph.components.experimental._variable_split_converter.VariableSplitConverter`
            (trsf) objects for which the linear relation of inputs
            and outputs is created e.g. group = [trsf1, trsf2, trsf3, ...].
            Note that the relation is created for all existing relations
            of the inputs and all outputs of the converter-like object.
            The components inside the list need to hold all needed attributes.
        """
        if group is None:
            return None

        m = self.parent_block()

        self.EQUAL_STATES = Set(
            initialize=[g for g in group if g.allow_equal_states]
        )

        for n in group:
            n.inflow = list(n.inputs)[0]

            n.output_a, n.output_b = list(n.outputs.keys())

            a1 = n.conversion_factors[n.output_a]
            b1 = n.conversion_factors[n.output_b]
            a2 = n.conversion_factors_secondary_state[n.output_a]
            b2 = n.conversion_factors_secondary_state[n.output_b]

            n.coef_out_b = [b1[t] - b2[t] for t in m.TIMESTEPS]
            n.coef_out_a = [a2[t] - a1[t] for t in m.TIMESTEPS]
            n.coef_in = [a2[t] * b1[t] - a1[t] * b2[t] for t in m.TIMESTEPS]

            n.out_b_min = [min(b1[t], b2[t]) for t in m.TIMESTEPS]
            n.out_b_max = [max(b1[t], b2[t]) for t in m.TIMESTEPS]

            if n.allow_equal_states:
                n.out_a_min = [min(a1[t], a2[t]) for t in m.TIMESTEPS]
                n.out_a_max = [max(a1[t], a2[t]) for t in m.TIMESTEPS]

        def _input_output_relation_rule(block):
            """Line through both given operating points"""
            for t in m.TIMESTEPS:
                for g in group:
                    lhs = (
                        g.coef_out_b[t] * m.flow[g, g.output_a, t]
                        + g.coef_out_a[t] * m.flow[g, g.output_b, t]
                    )
                    rhs = g.coef_in[t] * m.flow[g.inflow, g, t]
                    block.input_output_relation.add((g, t), (lhs == rhs))

        self.input_output_relation = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.input_output_relation_build = BuildAction(
            rule=_input_output_relation_rule
        )

        def _out_b_lower_bound_rule(block):
            """Restrict output_b to never fall below the smaller of the
            two given operating points."""
            for t in m.TIMESTEPS:
                for g in group:
                    lhs = g.out_b_min[t] * m.flow[g.inflow, g, t]
                    rhs = m.flow[g, g.output_b, t]
                    block.out_b_lower_bound.add((g, t), (lhs <= rhs))

        self.out_b_lower_bound = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.out_b_lower_bound_build = BuildAction(
            rule=_out_b_lower_bound_rule
        )

        def _out_b_upper_bound_rule(block):
            """Restrict output_b to never exceed the larger of the two
            given operating points."""
            for t in m.TIMESTEPS:
                for g in group:
                    lhs = m.flow[g, g.output_b, t]
                    rhs = g.out_b_max[t] * m.flow[g.inflow, g, t]
                    block.out_b_upper_bound.add((g, t), (lhs <= rhs))

        self.out_b_upper_bound = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.out_b_upper_bound_build = BuildAction(
            rule=_out_b_upper_bound_rule
        )

        def _out_a_lower_bound_rule(block):
            for t in m.TIMESTEPS:
                for g in self.EQUAL_STATES:
                    if g.coef_out_b[t] == 0:
                        lhs = g.out_a_min[t] * m.flow[g.inflow, g, t]
                        rhs = m.flow[g, g.output_a, t]
                        block.out_a_lower_bound.add((g, t), (lhs <= rhs))

        self.out_a_lower_bound = Constraint(
            self.EQUAL_STATES, m.TIMESTEPS, noruleinit=True
        )
        self.out_a_lower_bound_build = BuildAction(
            rule=_out_a_lower_bound_rule
        )

        def _out_a_upper_bound_rule(block):
            for t in m.TIMESTEPS:
                for g in self.EQUAL_STATES:
                    if g.coef_out_b[t] == 0:
                        lhs = m.flow[g, g.output_a, t]
                        rhs = g.out_a_max[t] * m.flow[g.inflow, g, t]
                        block.out_a_upper_bound.add((g, t), (lhs <= rhs))

        self.out_a_upper_bound = Constraint(
            self.EQUAL_STATES, m.TIMESTEPS, noruleinit=True
        )
        self.out_a_upper_bound_build = BuildAction(
            rule=_out_a_upper_bound_rule
        )
