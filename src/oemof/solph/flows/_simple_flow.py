# -*- coding: utf-8 -*-

"""
solph version of oemof.network.Edge including base constraints

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: jmloenneberga
SPDX-FileCopyrightText: Pierre-François Duc
SPDX-FileCopyrightText: Saeed Sayadi

SPDX-License-Identifier: MIT

"""
from pyomo.core import BuildAction
from pyomo.core import Constraint
from pyomo.core import NonNegativeIntegers
from pyomo.core import Set
from pyomo.core import Var
from pyomo.core.base.block import ScalarBlock


class SimpleFlowBlock(ScalarBlock):
    r"""Flow block with definitions for standard flows.

    See :class:`~oemof.solph.flows._flow.Flow` class for all parameters of the *Flow*.

    **Variables**

    All *Flow* objects are indexed by a starting and ending node
    :math:`(i, o)`, which is omitted in the following for the sake of
    convenience. The creation of some variables depend on the values of
    *Flow* attributes. The following variables are created:

    * :math:`P(t)`
        Actual flow value (created in :class:`~oemof.solph._models.Model`).
        The variable is bound to: :math:`f_{min}(t) \cdot P_{nom} \ge P(t) \le f_{max}(t) \cdot P_{nom}`.

        If `Flow.fix` is not None the variable is bound to
        :math:`P(t) = f_{fix}`.

    * :math:`ve_n` (`Flow.negative_gradient` is not `None`)
        Difference of a flow in consecutive timesteps if flow is reduced. The
        variable is bound to: :math:`0 \ge ve_n \ge ve_n^{max}`.

    * :math:`ve_p` (`Flow.positive_gradient` is not `None`)
        Difference of a flow in consecutive timesteps if flow is increased. The
        variable is bound to: :math:`0 \ge ve_p \ge ve_p^{max}`.

    The following variable is build for Flows with the attribute
    `integer_flows` being not None.

    * :math:`i`(`Flow.integer` is `True`)
        All flow values are integers. Variable is bound to non-negative
        integers.

    **Constraints**

    The following constraints are created, if the appropriate attribute of the
    *Flow* (see :class:`oemof.solph.network.Flow`) object is set:

    * `Flow.full_load_time_max` is not `None` (full_load_time_max_constr):
        .. math::
            \sum_t P(t) \cdot \tau \leq F_{max} \cdot P_{nom}

    * `Flow.full_load_time_min` is not `None` (full_load_time_min_constr):
        .. math::
            \sum_t P(t) \cdot \tau \geq F_{min} \cdot P_{nom}


    * `Flow.negative_gradient` is not `None` (negative_gradient_constr):
        .. math::
          P(t-1) - P(t) \geq ve_n(t)

    * `Flow.positive_gradient` is not `None` (positive_gradient_constr):
        .. math::
          P(t) - P(t-1) \geq ve_p(t)

    * `Flow.integer` is `True`
        .. math::
          P(t) = i(t)

    **Objective function**

    Depending on the attributes of the `Flow` object the following parts of
    the objective function are created:

    * `Flow.variable_costs` is not `None`:
        .. math::
          \sum_{(i,o)} \sum_t P(t) \cdot c_{var}(i, o, t)

    .. csv-table:: List of Variables
        :header: "symbol", "attribute", "explanation"
        :widths: 1, 1, 1

        ":math:`P(t)`", ":command:`flow[i, o][t]`", "Actual flow value"
        ":math:`ve_n`", ":command:`negative_gradient[n, o, t]`", "Negative gradient of the flow"
        ":math:`ve_p`", ":command:`positive_gradient[n, o, t]`", "Positive gradient of the flow"
        ":math:`i`", ":command:`integer_flow[i, o, t]`","Integer flow"


    .. csv-table:: List of Parameters
        :header: "symbol", "attribute", "explanation"
        :widths: 1, 1, 1

        ":math:`P_{nom}`", ":command:`flows[i, o].nominal_value`","Nominal value of the flow"
        ":math:`F_{max}`",":command:`flow[i, o].full_load_time_max`", "Maximal full
        load time"
        ":math:`F_{min}`",":command:`flow[i, o].full_load_time_min`", "Minimal full
        load time"
        ":math:`c_{var}`", ":command:`variable\_costs[t]`", "Variable cost of the flow"
        ":math:`f_{max}`", ":command:`flows[i, o].max[t]`", "Normed maximum value of the flow, the absolute maximum is :math:`f_{max} \cdot P_{nom}`"
        ":math:`f_{min}`", ":command:`flows[i, o].min[t]`", "Normed minimum value of the flow, the absolute minimum is :math:`f_{min} \cdot P_{nom}`"
        ":math:`f_{fix}`", ":command:`flows[i, o].min[t]`", "Normed fixed value of the flow, the absolute fixed value is :math:`f_{fix} \cdot P_{nom}`"
        ":math:`ve_n^{max}`",":command:`flows[i, o].negative_gradient`","Normed maximal negative gradient of the flow, the absolute maximum gradient is :math:`ve_n^{max} \cdot P_{nom}`"
        ":math:`ve_p^{max}`",":command:`flows[i, o].positive_gradient`","Normed maximal positive gradient of the flow, the absolute maximum gradient is :math:`ve_n^{max} \cdot P_{nom}`"

    Note
    ----
    See the :class:`~oemof.solph.flows._flow.Flow` class for the definition of
    all parameters from the "List of Parameters above.

    """  # noqa: E501

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        r"""Creates sets, variables and constraints for all standard flows.

        Parameters
        ----------
        group : list
            List containing tuples containing flow (f) objects and the
            associated source (s) and target (t)
            of flow e.g. groups=[(s1, t1, f1), (s2, t2, f2),..]
        """
        if group is None:
            return None

        self._create_sets(group)
        self._create_variables(group)
        self._create_constraints()

    def _create_sets(self, group):
        """
        Creates all sets for standard flows.
        """
        self.FULL_LOAD_TIME_MAX_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].full_load_time_max is not None
                and g[2].nominal_value is not None
            ]
        )

        self.FULL_LOAD_TIME_MIN_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].full_load_time_min is not None
                and g[2].nominal_value is not None
            ]
        )

        self.NEGATIVE_GRADIENT_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].negative_gradient["ub"][0] is not None
            ]
        )

        self.POSITIVE_GRADIENT_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].positive_gradient["ub"][0] is not None
            ]
        )

        self.INTEGER_FLOWS = Set(
            initialize=[(g[0], g[1]) for g in group if g[2].integer]
        )

    def _create_variables(self, group):
        """
        Creates all variables for standard flows.
        """
        m = self.parent_block()

        self.positive_gradient = Var(self.POSITIVE_GRADIENT_FLOWS, m.TIMESTEPS)

        self.negative_gradient = Var(self.NEGATIVE_GRADIENT_FLOWS, m.TIMESTEPS)

        self.integer_flow = Var(
            self.INTEGER_FLOWS, m.TIMESTEPS, within=NonNegativeIntegers
        )
        # set upper bound of gradient variable
        for i, o, f in group:
            if m.flows[i, o].positive_gradient["ub"][0] is not None:
                for t in m.TIMESTEPS:
                    self.positive_gradient[i, o, t].setub(
                        f.positive_gradient["ub"][t] * f.nominal_value
                    )
            if m.flows[i, o].negative_gradient["ub"][0] is not None:
                for t in m.TIMESTEPS:
                    self.negative_gradient[i, o, t].setub(
                        f.negative_gradient["ub"][t] * f.nominal_value
                    )

    def _create_constraints(self):
        """
        Creates all constraints for standard flows.
        """
        m = self.parent_block()

        def _flow_full_load_time_max_rule(model):
            """Rule definition for build action of max. sum flow constraint."""
            for inp, out in self.FULL_LOAD_TIME_MAX_FLOWS:
                lhs = sum(
                    m.flow[inp, out, ts] * m.timeincrement[ts]
                    for ts in m.TIMESTEPS
                )
                rhs = (
                    m.flows[inp, out].full_load_time_max
                    * m.flows[inp, out].nominal_value
                )
                self.full_load_time_max_constr.add((inp, out), lhs <= rhs)

        self.full_load_time_max_constr = Constraint(
            self.FULL_LOAD_TIME_MAX_FLOWS, noruleinit=True
        )
        self.full_load_time_max_build = BuildAction(
            rule=_flow_full_load_time_max_rule
        )

        def _flow_full_load_time_min_rule(model):
            """Rule definition for build action of min. sum flow constraint."""
            for inp, out in self.FULL_LOAD_TIME_MIN_FLOWS:
                lhs = sum(
                    m.flow[inp, out, ts] * m.timeincrement[ts]
                    for ts in m.TIMESTEPS
                )
                rhs = (
                    m.flows[inp, out].full_load_time_min
                    * m.flows[inp, out].nominal_value
                )
                self.full_load_time_min_constr.add((inp, out), lhs >= rhs)

        self.full_load_time_min_constr = Constraint(
            self.FULL_LOAD_TIME_MIN_FLOWS, noruleinit=True
        )
        self.full_load_time_min_build = BuildAction(
            rule=_flow_full_load_time_min_rule
        )

        def _positive_gradient_flow_rule(model):
            """Rule definition for positive gradient constraint."""
            for inp, out in self.POSITIVE_GRADIENT_FLOWS:
                for ts in m.TIMESTEPS:
                    if ts > 0:
                        lhs = m.flow[inp, out, ts] - m.flow[inp, out, ts - 1]
                        rhs = self.positive_gradient[inp, out, ts]
                        self.positive_gradient_constr.add(
                            (inp, out, ts), lhs <= rhs
                        )

        self.positive_gradient_constr = Constraint(
            self.POSITIVE_GRADIENT_FLOWS, m.TIMESTEPS, noruleinit=True
        )
        self.positive_gradient_build = BuildAction(
            rule=_positive_gradient_flow_rule
        )

        def _negative_gradient_flow_rule(model):
            """Rule definition for negative gradient constraint."""
            for inp, out in self.NEGATIVE_GRADIENT_FLOWS:
                for ts in m.TIMESTEPS:
                    if ts > 0:
                        lhs = m.flow[inp, out, ts - 1] - m.flow[inp, out, ts]
                        rhs = self.negative_gradient[inp, out, ts]
                        self.negative_gradient_constr.add(
                            (inp, out, ts), lhs <= rhs
                        )

        self.negative_gradient_constr = Constraint(
            self.NEGATIVE_GRADIENT_FLOWS, m.TIMESTEPS, noruleinit=True
        )
        self.negative_gradient_build = BuildAction(
            rule=_negative_gradient_flow_rule
        )

        def _integer_flow_rule(block, ii, oi, ti):
            """Force flow variable to NonNegativeInteger values."""
            return self.integer_flow[ii, oi, ti] == m.flow[ii, oi, ti]

        self.integer_flow_constr = Constraint(
            self.INTEGER_FLOWS, m.TIMESTEPS, rule=_integer_flow_rule
        )

    def _objective_expression(self):
        r"""Objective expression for all standard flows with fixed costs
        and variable costs.
        """
        m = self.parent_block()

        variable_costs = 0

        for i, o in m.FLOWS:
            if m.flows[i, o].variable_costs[0] is not None:
                for t in m.TIMESTEPS:
                    variable_costs += (
                        m.flow[i, o, t]
                        * m.objective_weighting[t]
                        * m.flows[i, o].variable_costs[t]
                    )

        return variable_costs
