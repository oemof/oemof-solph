# -*- coding: utf-8 -*-

"""Creating sets, variables, constraints and parts of the objective function
for FlowBlock objects with investment option.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: jmloenneberga
SPDX-FileCopyrightText: Johannes Kochems

SPDX-License-Identifier: MIT

"""
from warnings import warn

from oemof.tools import debugging
from oemof.tools import economics
from pyomo.core import Binary
from pyomo.core import BuildAction
from pyomo.core import Constraint
from pyomo.core import Expression
from pyomo.core import NonNegativeReals
from pyomo.core import Set
from pyomo.core import Var
from pyomo.core.base.block import SimpleBlock

from ._flow import Flow


class InvestmentFlow(Flow):
    r"""
    Wrapper class to prepare separation of flow classes.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class InvestmentFlowBlock(SimpleBlock):
    r"""Block for all flows with :attr:`Investment` being not None.

    See :class:`oemof.solph.options.Investment` for all parameters of the
    *Investment* class.

    See :class:`oemof.solph.network.FlowBlock` for all parameters of the *FlowBlock*
    class.

    **Variables**

    All *InvestmentFlowBlock* are indexed by a starting and ending node
    :math:`(i, o)`, which is omitted in the following for the sake
    of convenience. The following variables are created:

    * :math:`P(t)`

        Actual flow value (created in :class:`oemof.solph.models.BaseModel`).

    * :math:`P_{invest}`

        Value of the investment variable, i.e. equivalent to the nominal
        value of the flows after optimization.

    * :math:`b_{invest}`

        Binary variable for the status of the investment, if
        :attr:`nonconvex` is `True`.

    **Constraints**

    Depending on the attributes of the *InvestmentFlowBlock* and *FlowBlock*, different
    constraints are created. The following constraint is created for all
    *InvestmentFlowBlock*:\

            Upper bound for the flow value

        .. math::
            P(t) \le ( P_{invest} + P_{exist} ) \cdot f_{max}(t)

    Depeding on the attribute :attr:`nonconvex`, the constraints for the bounds
    of the decision variable :math:`P_{invest}` are different:\

        * :attr:`nonconvex = False`

        .. math::
            P_{invest, min} \le P_{invest} \le P_{invest, max}

        * :attr:`nonconvex = True`

        .. math::
            &
            P_{invest, min} \cdot b_{invest} \le P_{invest}\\
            &
            P_{invest} \le P_{invest, max} \cdot b_{invest}\\

    For all *InvestmentFlowBlock* (independent of the attribute :attr:`nonconvex`),
    the following additional constraints are created, if the appropriate
    attribute of the *FlowBlock* (see :class:`oemof.solph.network.FlowBlock`) is set:

        * :attr:`fix` is not None

            Actual value constraint for investments with fixed flow values

        .. math::
            P(t) = ( P_{invest} + P_{exist} ) \cdot f_{fix}(t)

        * :attr:`min != 0`

            Lower bound for the flow values

        .. math::
            P(t) \geq ( P_{invest} + P_{exist} ) \cdot f_{min}(t)

        * :attr:`summed_max is not None`

            Upper bound for the sum of all flow values (e.g. maximum full load
            hours)

        .. math::
            \sum_t P(t) \cdot \tau(t) \leq ( P_{invest} + P_{exist} )
            \cdot f_{sum, min}

        * :attr:`summed_min is not None`

            Lower bound for the sum of all flow values (e.g. minimum full load
            hours)

        .. math::
            \sum_t P(t) \cdot \tau(t) \geq ( P_{invest} + P_{exist} )
            \cdot f_{sum, min}


    **Objective function**

    The part of the objective function added by the *InvestmentFlowBlock*
    also depends on whether a convex or nonconvex
    *InvestmentFlowBlock* is selected. The following parts of the objective function
    are created:

        * :attr:`nonconvex = False`

            .. math::
                P_{invest} \cdot c_{invest,var}

        * :attr:`nonconvex = True`

            .. math::
                P_{invest} \cdot c_{invest,var}
                + c_{invest,fix} \cdot b_{invest}\\

    The total value of all costs of all *InvestmentFlowBlock* can be retrieved
    calling :meth:`om.InvestmentFlowBlock.investment_costs.expr()`.

    .. csv-table:: List of Variables (in csv table syntax)
        :header: "symbol", "attribute", "explanation"
        :widths: 1, 1, 1

        ":math:`P(t)`", ":py:obj:`flow[n, o, t]`", "Actual flow value"
        ":math:`P_{invest}`", ":py:obj:`invest[i, o]`", "Invested flow
        capacity"
        ":math:`b_{invest}`", ":py:obj:`invest_status[i, o]`", "Binary status
        of investment"

    List of Variables (in rst table syntax):

    ===================  =============================  =========
    symbol               attribute                      explanation
    ===================  =============================  =========
    :math:`P(t)`         :py:obj:`flow[n, o, t]`         Actual flow value

    :math:`P_{invest}`   :py:obj:`invest[i, o]`          Invested flow capacity

    :math:`b_{invest}`   :py:obj:`invest_status[i, o]`   Binary status of investment

    ===================  =============================  =========

    Grid table style:

    +--------------------+-------------------------------+-----------------------------+
    | symbol             | attribute                     | explanation                 |
    +====================+===============================+=============================+
    | :math:`P(t)`       | :py:obj:`flow[n, o, t]`       | Actual flow value           |
    +--------------------+-------------------------------+-----------------------------+
    | :math:`P_{invest}` | :py:obj:`invest[i, o]`        | Invested flow capacity      |
    +--------------------+-------------------------------+-----------------------------+
    | :math:`b_{invest}` | :py:obj:`invest_status[i, o]` | Binary status of investment |
    +--------------------+-------------------------------+-----------------------------+

    .. csv-table:: List of Parameters
        :header: "symbol", "attribute", "explanation"
        :widths: 1, 1, 1

        ":math:`P_{exist}`", ":py:obj:`flows[i, o].investment.existing`", "
        Existing flow capacity"
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
    See also :class:`oemof.solph.network.FlowBlock`,
    :class:`oemof.solph.blocks.FlowBlock` and
    :class:`oemof.solph.options.Investment`

    """  # noqa: E501

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        r"""Creates sets, variables and constraints for FlowBlock
        with investment attribute of type class:`.Investment`.

        Parameters
        ----------
        group : list
            List containing tuples containing flow (f) objects that have an
            attribute investment and the associated source (s) and target (t)
            of flow e.g. groups=[(s1, t1, f1), (s2, t2, f2),..]
        """
        if group is None:
            return None

        m = self.parent_block()

        # ######################### SETS #####################################
        self.INVESTFLOWS = Set(initialize=[(g[0], g[1]) for g in group])

        self.CONVEX_INVESTFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].investment.nonconvex is False
            ]
        )

        self.NON_CONVEX_INVESTFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].investment.nonconvex is True
            ]
        )

        self.FIXED_INVESTFLOWS = Set(
            initialize=[(g[0], g[1]) for g in group if g[2].fix[0] is not None]
        )

        self.NON_FIXED_INVESTFLOWS = Set(
            initialize=[(g[0], g[1]) for g in group if g[2].fix[0] is None]
        )

        self.SUMMED_MAX_INVESTFLOWS = Set(
            initialize=[
                (g[0], g[1]) for g in group if g[2].summed_max is not None
            ]
        )

        self.SUMMED_MIN_INVESTFLOWS = Set(
            initialize=[
                (g[0], g[1]) for g in group if g[2].summed_min is not None
            ]
        )

        self.MIN_INVESTFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if (g[2].min[0] != 0 or len(g[2].min) > 1)
            ]
        )

        self.OVERALL_MAXIMUM_INVESTFLOWS = Set(
            initialize=[
                (g[0], g[1]) for g in group
                if g[2].investment.overall_maximum is not None]
        )

        self.OVERALL_MINIMUM_INVESTFLOWS = Set(
            initialize=[
                (g[0], g[1]) for g in group
                if g[2].investment.overall_minimum is not None]
        )

        # ######################### VARIABLES #################################
        def _investvar_bound_rule(block, i, o, p):
            """Rule definition for bounds of invest variable."""
            if (i, o) in self.CONVEX_INVESTFLOWS:
                return (
                    m.flows[i, o].investment.minimum[p],
                    m.flows[i, o].investment.maximum[p],
                )
            elif (i, o) in self.NON_CONVEX_INVESTFLOWS:
                return 0, m.flows[i, o].investment.maximum[p]

        # create invest variable for an investment flow
        self.invest = Var(
            self.INVESTFLOWS,
            m.PERIODS,
            within=NonNegativeReals,
            bounds=_investvar_bound_rule,
        )

        # Total capacity
        self.total = Var(
            self.INVESTFLOWS,
            m.PERIODS,
            within=NonNegativeReals
        )

        # Old capacity is built out of old exogenous and endogenous capacities
        self.old = Var(
            self.INVESTFLOWS,
            m.PERIODS,
            within=NonNegativeReals
        )

        # Old endogenous capacity to be decommissioned (due to lifetime)
        self.old_end = Var(
            self.INVESTFLOWS,
            m.PERIODS,
            within=NonNegativeReals
        )

        # Old exogenous capacity to be decommissioned (due to lifetime)
        self.old_exo = Var(
            self.INVESTFLOWS,
            m.PERIODS,
            within=NonNegativeReals
        )

        # create status variable for a non-convex investment flow
        self.invest_status = Var(
            self.NON_CONVEX_INVESTFLOWS,
            m.PERIODS,
            within=Binary
        )

        # ######################### CONSTRAINTS ###############################
        def _min_invest_rule(block):
            """Rule definition for applying a minimum investment"""
            for i, o in self.NON_CONVEX_INVESTFLOWS:
                for p in m.PERIODS:
                    expr = (
                        m.flows[i, o].investment.minimum[p]
                        * self.invest_status[i, o, p]
                        <= self.invest[i, o, p]
                    )
                    self.minimum_rule.add((i, o, p), expr)

        self.minimum_rule = Constraint(
            self.NON_CONVEX_INVESTFLOWS, m.PERIODS,
            noruleinit=True
        )
        self.minimum_rule_build = BuildAction(
            rule=_min_invest_rule
        )

        def _max_invest_rule(block):
            """Rule definition for applying a minimum investment"""
            for i, o in self.NON_CONVEX_INVESTFLOWS:
                for p in m.PERIODS:
                    expr = (
                        self.invest[i, o, p]
                        <= (m.flows[i, o].investment.maximum[p]
                            * self.invest_status[i, o, p])
                    )
                    self.maximum_rule.add((i, o, p), expr)

        self.maximum_rule = Constraint(
            self.NON_CONVEX_INVESTFLOWS, m.PERIODS,
            noruleinit=True
        )
        self.maximum_rule_build = BuildAction(
            rule=_max_invest_rule
        )

        # Handle unit lifetimes
        def _total_capacity_rule(block):
            """Rule definition for determining total installed
            capacity (taking decommissioning into account)
            """
            for i, o in self.INVESTFLOWS:
                for p in m.PERIODS:
                    if p == 0:
                        expr = (self.total[i, o, p]
                                == self.invest[i, o, p]
                                + m.flows[i, o].investment.existing)
                        self.total_rule.add((i, o, p), expr)
                    else:
                        expr = (self.total[i, o, p]
                                == self.invest[i, o, p]
                                + self.total[i, o, p - 1]
                                - self.old[i, o, p])
                        self.total_rule.add((i, o, p), expr)

        self.total_rule = Constraint(
            self.INVESTFLOWS, m.PERIODS,
            noruleinit=True
        )
        self.total_rule_build = BuildAction(
            rule=_total_capacity_rule)

        def _old_capacity_rule_end(block):
            """Rule definition for determining old endogenously installed
            capacity to be decommissioned due to reaching its lifetime
            """
            for i, o in self.INVESTFLOWS:
                lifetime = m.flows[i, o].investment.lifetime
                for p in m.PERIODS:
                    # No shutdown in first period
                    if p == 0:
                        expr = (self.old_end[i, o, p] == 0)
                        self.old_rule_end.add((i, o, p), expr)
                    elif lifetime <= m.es.periods_years[p]:
                        # Obtain commissioning period
                        comm_p = 0
                        for k, v in m.es.periods_years.items():
                            if m.es.periods_years[p] - lifetime - v < 0:
                                comm_p = k - 1
                                break
                        expr = (self.old_end[i, o, p]
                                == self.invest[i, o, comm_p])
                        self.old_rule_end.add((i, o, p), expr)
                    else:
                        expr = (self.old_end[i, o, p] == 0)
                        self.old_rule_end.add((i, o, p), expr)

        self.old_rule_end = Constraint(
            self.INVESTFLOWS, m.PERIODS,
            noruleinit=True
        )
        self.old_rule_end_build = BuildAction(
            rule=_old_capacity_rule_end
        )

        def _old_capacity_rule_exo(block):
            """Rule definition for determining old exogenously given capacity
            to be decommissioned due to reaching its lifetime
            """
            for i, o in self.INVESTFLOWS:
                age = m.flows[i, o].investment.age
                lifetime = m.flows[i, o].investment.lifetime
                for p in m.PERIODS:
                    if lifetime - age == p:
                        expr = (
                            self.old_exo[i, o, p]
                            == m.flows[i, o].investment.existing)
                        self.old_rule_exo.add((i, o, p), expr)
                    else:
                        expr = (self.old_exo[i, o, p] == 0)
                        self.old_rule_exo.add((i, o, p), expr)

        self.old_rule_exo = Constraint(
            self.INVESTFLOWS, m.PERIODS,
            noruleinit=True
        )
        self.old_rule_exo_build = BuildAction(
            rule=_old_capacity_rule_exo
        )

        def _old_capacity_rule(block):
            """Rule definition for determining (overall) old capacity
            to be decommissioned due to reaching its lifetime
            """
            for i, o in self.INVESTFLOWS:
                for p in m.PERIODS:
                    expr = (
                        self.old[i, o, p]
                        == self.old_end[i, o, p] + self.old_exo[i, o, p])
                    self.old_rule.add((i, o, p), expr)

        self.old_rule = Constraint(
            self.INVESTFLOWS, m.PERIODS,
            noruleinit=True
        )
        self.old_rule_build = BuildAction(
            rule=_old_capacity_rule
        )

        def _investflow_fixed_rule(block):
            """Rule definition of constraint to fix flow variable
            of investment flow to (normed) actual value
            """
            for i, o in self.FIXED_INVESTFLOWS:
                for p, t in m.TIMEINDEX:
                    expr = (
                        m.flow[i, o, p, t]
                        == self.total[i, o, p] * m.flows[i, o].fix[t]
                    )
                    self.fixed.add((i, o, p, t), expr)

        self.fixed = Constraint(
            self.FIXED_INVESTFLOWS,
            m.TIMEINDEX,
            noruleinit=True
        )
        self.fixed_build = BuildAction(
            rule=_investflow_fixed_rule
        )

        def _max_investflow_rule(block):
            """Rule definition of constraint setting an upper bound of flow
            variable in investment case.
            """
            for i, o in self.NON_FIXED_INVESTFLOWS:
                for p, t in m.TIMEINDEX:
                    expr = (
                        m.flow[i, o, p, t]
                        <= self.total[i, o, p] * m.flows[i, o].max[t]
                    )
                    self.max.add((i, o, p, t), expr)

        self.max = Constraint(
            self.NON_FIXED_INVESTFLOWS,
            m.TIMEINDEX,
            noruleinit=True
        )
        self.max_build = BuildAction(
            rule=_max_investflow_rule
        )

        def _min_investflow_rule(block):
            """Rule definition of constraint setting a lower bound on flow
            variable in investment case.
            """
            for i, o in self.MIN_INVESTFLOWS:
                for p, t in m.TIMEINDEX:
                    expr = (
                        m.flow[i, o, p, t]
                        >= self.total[i, o, p] * m.flows[i, o].min[t]
                    )
                    self.min.add((i, o, p, t), expr)

        self.min = Constraint(
            self.MIN_INVESTFLOWS,
            m.TIMEINDEX,
            noruleinit=True
        )
        self.min_build = BuildAction(
            rule=_min_investflow_rule
        )

        def _summed_max_investflow_rule(block, i, o):
            """Rule definition for build action of max. sum flow constraint
            in investment case.
            """
            expr = (
                sum(m.flow[i, o, p, t] * m.timeincrement[t]
                    for p, t in m.TIMEINDEX)
                <= (m.flows[i, o].summed_max
                    * sum(self.total[i, o, p] for p in m.PERIODS))
            )
            return expr

        self.summed_max = Constraint(
            self.SUMMED_MAX_INVESTFLOWS,
            rule=_summed_max_investflow_rule
        )

        def _summed_min_investflow_rule(block, i, o):
            """Rule definition for build action of min. sum flow constraint
            in investment case.
            """
            expr = (
                sum(m.flow[i, o, p, t] * m.timeincrement[t]
                    for p, t in m.TIMEINDEX)
                >= (sum(self.total[i, o, p] for p in m.PERIODS)
                    * m.flows[i, o].summed_min)
            )
            return expr

        self.summed_min = Constraint(
            self.SUMMED_MIN_INVESTFLOWS,
            rule=_summed_min_investflow_rule
        )

        def _overall_maximum_investflow_rule(block):
            """Rule definition for maximum overall investment
            in investment case.

            Note: In general, there are two different options to define
            an overall maximum:
            1.) overall_max = limit for (net) installed capacity
            for each period. This is the constraint used here
            2.) overall max = sum of all (gross) investments occurring
            """
            for i, o in self.OVERALL_MAXIMUM_INVESTFLOWS:
                for p in m.PERIODS:
                    expr = (
                        self.total[i, o, p]
                        <= m.flows[i, o].investment.overall_maximum
                    )
                    self.overall_maximum.add((i, o, p), expr)

        self.overall_maximum = Constraint(
            self.OVERALL_MAXIMUM_INVESTFLOWS,
            m.PERIODS,
            noruleinit=True
        )
        self.overall_maximum_build = BuildAction(
            rule=_overall_maximum_investflow_rule
        )

        def _overall_minimum_investflow_rule(block, i, o):
            """Rule definition for minimum overall investment
            in investment case.

            Note: This is only applicable for the last period
            """
            expr = (
                m.flows[i, o].investment.overall_minimum
                <= self.total[i, o, m.PERIODS[-1]]
            )
            return expr

        self.overall_minimum = Constraint(
            self.OVERALL_MINIMUM_INVESTFLOWS,
            rule=_overall_minimum_investflow_rule
        )

    def _objective_expression(self):
        r"""Objective expression for flows with investment attribute of type
        class:`.Investment`. The returned costs are fixed and
        investment costs. Variable costs are added from the standard flow
        objective expression.
        """
        if not hasattr(self, "INVESTFLOWS"):
            return 0

        m = self.parent_block()
        investment_costs = 0
        period_investment_costs = {p: 0 for p in m.PERIODS}
        fixed_costs = 0

        if not m.es.multi_period:
            for i, o in self.CONVEX_INVESTFLOWS:
                for p in m.PERIODS:
                    investment_costs += (
                        self.invest[i, o, p]
                        * m.flows[i, o].investment.ep_costs[p]
                    )

            for i, o in self.NON_CONVEX_INVESTFLOWS:
                for p in m.PERIODS:
                    investment_costs += (
                        self.invest[i, o, p]
                        * m.flows[i, o].investment.ep_costs[p]
                        + self.invest_status[i, o, p]
                        * m.flows[i, o].investment.offset[p]
                    )

        else:
            msg = ("You did not specify an interest rate.\n"
                   "It will be set equal to the discount_rate of {} "
                   "of the model as a default.\nThis corresponds to a "
                   "social planner point of view and does not reflect "
                   "microeconomic interest requirements.")

            for i, o in self.CONVEX_INVESTFLOWS:
                lifetime = m.flows[i, o].investment.lifetime
                interest = m.flows[i, o].investment.interest_rate
                if interest == 0:
                    warn(msg.format(m.discount_rate),
                         debugging.SuspiciousUsageWarning)
                    interest = m.discount_rate
                for p in m.PERIODS:
                    annuity = economics.annuity(
                        capex=m.flows[i, o].investment.ep_costs[p],
                        n=lifetime,
                        wacc=interest
                    )
                    investment_costs_increment = (
                        self.invest[i, o, p] * annuity * lifetime
                        * ((1 + m.discount_rate) ** (-p))
                    )
                    investment_costs += investment_costs_increment
                    period_investment_costs[p] += investment_costs_increment

            for i, o in self.NON_CONVEX_INVESTFLOWS:
                lifetime = m.flows[i, o].investment.lifetime
                interest = m.flows[i, o].investment.interest_rate
                if interest == 0:
                    warn(msg.format(m.discount_rate),
                         debugging.SuspiciousUsageWarning)
                    interest = m.discount_rate
                for p in m.PERIODS:
                    annuity = economics.annuity(
                        capex=m.flows[i, o].investment.ep_costs[p],
                        n=lifetime,
                        wacc=interest
                    )
                    investment_costs_increment = (
                        (self.invest[i, o, p] * annuity * lifetime
                         + self.invest_status[i, o, p]
                         * m.flows[i, o].investment.offset[p])
                        * ((1 + m.discount_rate) ** (-p))
                    )
                    investment_costs += investment_costs_increment
                    period_investment_costs[p] += investment_costs_increment

            for i, o in self.INVESTFLOWS:
                if m.flows[i, o].investment.fixed_costs[0] is not None:
                    lifetime = m.flows[i, o].investment.lifetime
                    for p in m.PERIODS:
                        fixed_costs += (
                            sum(self.invest[i, o, p]
                                * m.flows[i, o].investment.fixed_costs[pp]
                                * ((1 + m.discount_rate) ** (-pp))
                                for pp in range(p, p + lifetime))
                            * ((1 + m.discount_rate) ** (-p))
                        )

        self.investment_costs = Expression(expr=investment_costs)
        self.period_investment_costs = period_investment_costs
        self.costs = Expression(expr=investment_costs + fixed_costs)

        return self.costs
