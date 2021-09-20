# -*- coding: utf-8 -*-

"""Creating sets, variables, constraints and parts of the objective function
for Flow objects.

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
from pyomo.core import NonNegativeIntegers
from pyomo.core import Set
from pyomo.core import Var
from pyomo.core.base.block import SimpleBlock


class Flow(SimpleBlock):
    r""" Flow block with definitions for standard flows.

    For standard flows the attributes `investment` and `nonconvex` are None.

    See :class:`~oemof.solph.network.Flow` for all parameters of the *Flow*
    class.

    **Variables**

    All *Flow* objects are indexed by a starting and ending node
    :math:`(i, o)`, which is omitted in the following for the sake of
    convenience. The creation of some variables depend on the values of
    *Flow* attributes. The following variables are created:

    * :math:`P(t)`
        Actual flow value (created in :class:`oemof.solph.models.BaseModel`).
        The variable is bound to :math:`f_{min}(t) \ge P(t) \le f_{max}(t)`.

        If `Flow.fix` is not None the variable is bound to
        :math:`P(t) = f_{fix}`.

    * :math:`ve_n` (`Flow.negative_gradient` is not `None`)
        Difference of a flow in consecutive timesteps if flow is reduced. The
        variable is not bound.

    * :math:`ve_p` (`Flow.positive_gradient` is not `None`)
        Difference of a flow in consecutive timesteps if flow is increased. The
        variable is not bound.

    The following variable is build for Flows with the attribute
    `integer_flows` being not None.

    **Constraints**

    The following constraints are created, if the appropriate attribute of the
    *Flow* (see :class:`oemof.solph.network.Flow`) object is set:

    * `Flow.summed_max` is not `None` (`om.Flow.summed_max[i, o]`):
        .. math::
            \sum_t P(t) \cdot \tau \leq F_{max} \cdot P_{nom}

    * `Flow.summed_min` is not `None` (`om.Flow.summed_min[i, o]`):
        .. math::
            \sum_t P(t) \cdot \tau \geq F_{min} \cdot P_{nom}


    * `Flow.negative_gradient` is not `None` (`om.Flow.negative_gradient_constr[i, o]`):
        .. math::
          P(t-1) - P(t) \geq ve_n(t)

    * `Flow.positive_gradient` is not `None` (`om.Flow.positive_gradient_constr[i, o]`):
        .. math::
          P(t) - P(t-1) \geq ve_p(t)

    **Objective function**

    Depending on the attributes of the `Flow` object the following parts of
    the objective function are created:

    * `Flow.variable_costs` is not `None`:
        .. math::
          \sum_{(i,o)} \sum_t flow(i, o, t) \cdot variable\_costs(i, o, t)

    .. csv-table:: List of Variables
        :header: "symbol", "attribute", "explanation"
        :widths: 1, 1, 1

        ":math:`P(t)`", ":command:`flow[i, o][t]`", "Actual flow value"

        ":math:`ve_n`", ":command:`negative_gradient[n, o, t]`", "Invested flow
        capacity"
        ":math:`ve_p`", ":command:`positive_gradient[n, o, t]`", "Binary status
        of investment"



    .. csv-table:: List of Parameters
        :header: "symbol", "attribute", "explanation"
        :widths: 1, 1, 1

        ":math:`F_{max}`",":command:`flow[i, o].summed_max`", "Maximal full
        load time"
        ":math:`F_{min}`",":command:`flow[i, o].summed_max`", "Minimal full
        load time"

        ":math:`P_{invest,min}`", ":py:obj:`flows[i, o].investment.minimum`", "
        Minimum investment capacity"
        ":math:`P_{invest,max}`", ":py:obj:`flows[i, o].investment.maximum`", "
        Maximum investment capacity"
        ":math:`c_{invest,var}`", ":py:obj:`flows[i, o].investment.ep_costs`
        ", "Variable investment costs"
        ":math:`c_{invest,fix}`", ":py:obj:`flows[i, o].investment.offset`", "
        Fix investment costs"
        ":math:`f_{actual}`", ":py:obj:`flows[i, o].fix[t]`", "Normed
        fixed value for the flow variable"
        ":math:`f_{max}`", ":py:obj:`flows[i, o].max[t]`", "Normed maximum
        value of the flow"
        ":math:`f_{min}`", ":py:obj:`flows[i, o].min[t]`", "Normed minimum
        value of the flow"
        ":math:`f_{sum,max}`", ":py:obj:`flows[i, o].summed_max`", "Specific
        maximum of summed flow values (per installed capacity)"
        ":math:`f_{sum,min}`", ":py:obj:`flows[i, o].summed_min`", "Specific
        minimum of summed flow values (per installed capacity)"
        ":math:`\tau(t)`", ":py:obj:`timeincrement[t]`", "Time step width for
        each time step"

    Note
    ----
    In case of a nonconvex investment flow (:attr:`nonconvex=True`),
    the existing flow capacity :math:`P_{exist}` needs to be zero.
    At least, it is not tested yet, whether this works out, or makes any sense
    at all.

    Note
    ----
    See also :class:`oemof.solph.network.Flow`,
    :class:`oemof.solph.blocks.Flow` and
    :class:`oemof.solph.options.Investment`

    **The following variables are created**: (-> see basic constraints at
    :class:`.Model` )

    negative_gradient :
        Difference of a flow in consecutive timesteps if flow is reduced
        indexed by NEGATIVE_GRADIENT_FLOWS, TIMESTEPS.

    positive_gradient :
        Difference of a flow in consecutive timesteps if flow is increased
        indexed by NEGATIVE_GRADIENT_FLOWS, TIMESTEPS.

    The following variable is build for Flows with the attribute
    `integer_flows` being not None.



    **The following sets are created:** (-> see basic sets at :class:`.Model` )

    INTEGER_FLOWS
        A set of flows where the attribute :attr:`integer` is True (forces flow
        to only take integer values)

    **The following constraints are build:**



    **The following parts of the objective function are created:**

    If :attr:`variable_costs` are set by the user:
      .. math::
          \sum_{(i,o)} \sum_t flow(i, o, t) \cdot variable\_costs(i, o, t)

    The expression can be accessed by `om.Flow.variable_costs` and
    their value after optimization by `om.Flow.variable_costs()` .

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

        m = self.parent_block()

        # ########################## SETS #################################
        # set for all flows with an global limit on the flow over time
        self.SUMMED_MAX_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].summed_max is not None
                and g[2].nominal_value is not None
            ]
        )

        self.SUMMED_MIN_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].summed_min is not None
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
        # ######################### Variables  ################################

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

        # ######################### CONSTRAINTS ###############################

        def _flow_summed_max_rule(model):
            """Rule definition for build action of max. sum flow constraint."""
            for inp, out in self.SUMMED_MAX_FLOWS:
                lhs = sum(
                    m.flow[inp, out, ts] * m.timeincrement[ts]
                    for ts in m.TIMESTEPS
                )
                rhs = (
                    m.flows[inp, out].summed_max
                    * m.flows[inp, out].nominal_value
                )
                self.summed_max.add((inp, out), lhs <= rhs)

        self.summed_max = Constraint(self.SUMMED_MAX_FLOWS, noruleinit=True)
        self.summed_max_build = BuildAction(rule=_flow_summed_max_rule)

        def _flow_summed_min_rule(model):
            """Rule definition for build action of min. sum flow constraint."""
            for inp, out in self.SUMMED_MIN_FLOWS:
                lhs = sum(
                    m.flow[inp, out, ts] * m.timeincrement[ts]
                    for ts in m.TIMESTEPS
                )
                rhs = (
                    m.flows[inp, out].summed_min
                    * m.flows[inp, out].nominal_value
                )
                self.summed_min.add((inp, out), lhs >= rhs)

        self.summed_min = Constraint(self.SUMMED_MIN_FLOWS, noruleinit=True)
        self.summed_min_build = BuildAction(rule=_flow_summed_min_rule)

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
                    else:
                        pass  # return(Constraint.Skip)

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
                    else:
                        pass  # return(Constraint.Skip)

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
        gradient_costs = 0

        for i, o in m.FLOWS:
            if m.flows[i, o].variable_costs[0] is not None:
                for t in m.TIMESTEPS:
                    variable_costs += (
                        m.flow[i, o, t]
                        * m.objective_weighting[t]
                        * m.flows[i, o].variable_costs[t]
                    )
            if m.flows[i, o].positive_gradient["costs"] != 0:
                for t in self.TIMESTEPS_ge_1:
                    gradient_costs += (
                        self.positive_gradient[i, o, t]
                        * m.flows[i, o].negative_gradient["costs"]
                    )
            if m.flows[i, o].negative_gradient["costs"] != 0:
                for t in self.TIMESTEPS_ge_1:
                    gradient_costs += (
                        self.negative_gradient[i, o, t]
                        * m.flows[i, o].negative_gradient["costs"]
                    )

        return variable_costs + gradient_costs
