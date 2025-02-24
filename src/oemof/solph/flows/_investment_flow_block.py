# -*- coding: utf-8 -*-

"""Creating sets, variables, constraints and parts of the objective function
for Flow objects with investment but without nonconvex option.

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

import numpy as np
from oemof.tools import debugging
from oemof.tools import economics
from pyomo.core import Binary
from pyomo.core import BuildAction
from pyomo.core import Constraint
from pyomo.core import Expression
from pyomo.core import NonNegativeReals
from pyomo.core import Set
from pyomo.core import Var
from pyomo.core.base.block import ScalarBlock

from oemof.solph._plumbing import valid_sequence


class InvestmentFlowBlock(ScalarBlock):
    r"""Block for all flows with :attr:`Investment` being not None.

    .. automethod:: _create_constraints
    .. automethod:: _create_variables
    .. automethod:: _create_sets

    .. automethod:: _objective_expression

    See :class:`oemof.solph.options.Investment` for all parameters of the
    *Investment* class.

    See :class:`oemof.solph.flows._simple_flow_block.SimpleFlowBlock`
    for all parameters of the *SimpleFlowBlock* class.

    The overall summed cost expressions for all *InvestmentFlowBlock* objects
    can be accessed by

    * :attr:`om.InvestmentFlowBlock.investment_costs`,
    * :attr:`om.InvestmentFlowBlock.fixed_costs` and
    * :attr:`om.InvestmentFlowBlock.costs`.

    Their values  after optimization can be retrieved by

    * :meth:`om.InvestmentFlowBlock.investment_costs`,
    * :meth:`om.InvestmentFlowBlock.fixed_costs` and
    * :meth:`om.InvestmentFlowBlock.costs`.

    Note
    ----
    In case of a nonconvex investment flow (:attr:`nonconvex=True`),
    the existing flow capacity :math:`P_{exist}` needs to be zero.

    Note
    ----
    See also :class:`~oemof.solph.flows._flow.Flow`,
    :class:`~oemof.solph.flows._simple_flow_block.SimpleFlowBlock` and
    :class:`~oemof.solph._options.Investment`

    """  # noqa: E501

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        r"""Creates sets, variables and constraints for SimpleFlowBlock
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

        self._create_sets(group)
        self._create_variables(group)
        self._create_constraints()

    def _create_sets(self, group):
        """
        Creates all sets for investment flows.
        """
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

        self.FULL_LOAD_TIME_MAX_INVESTFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].full_load_time_max is not None
            ]
        )

        self.FULL_LOAD_TIME_MIN_INVESTFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].full_load_time_min is not None
            ]
        )

        self.MIN_INVESTFLOWS = Set(
            initialize=[(g[0], g[1]) for g in group if g[2].min.min() != 0]
        )

        self.EXISTING_INVESTFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].investment.existing is not None
            ]
        )

    def _create_variables(self, _):
        r"""Creates all variables for investment flows.

        All *InvestmentFlowBlock* objects are indexed by a starting and
        ending node :math:`(i, o)`, which is omitted in the following
        for the sake of convenience. The following variables are created:

        * :math:`P(t)`

            Actual flow value
            (created in :class:`oemof.solph.models.Model`)

        * :math:`P_{invest}`

            Value of the investment variable in period p,
            equal to what is being invested and equivalent resp. similar to
            the nominal capacity of the flows after optimization.

        * :math:`P_{total}`

            Total installed capacity / energy in period p,
            equivalent to the nominal capacity of the flows after optimization.

        * :math:`Y_{invest}(p)`

            Binary variable for the status of the investment, if
            :attr:`nonconvex` is `True`.
        """
        m = self.parent_block()

        def _investvar_bound_rule(block, i, o):
            """Rule definition for bounds of invest variable."""
            if (i, o) in self.CONVEX_INVESTFLOWS:
                return (
                    m.flows[i, o].investment.minimum,
                    m.flows[i, o].investment.maximum,
                )
            elif (i, o) in self.NON_CONVEX_INVESTFLOWS:
                return 0, m.flows[i, o].investment.maximum

        # create invest variable for an investment flow
        self.invest = Var(
            self.INVESTFLOWS,
            within=NonNegativeReals,
            bounds=_investvar_bound_rule,
        )

        # Total capacity
        self.total_capacity = Var(self.INVESTFLOWS, within=NonNegativeReals)

        # create status variable for a non-convex investment flow
        self.invest_status = Var(
            self.NON_CONVEX_INVESTFLOWS, within=Binary
        )

    def _create_constraints(self):
        r"""Creates all constraints for standard flows.

        Depending on the attributes of the *InvestmentFlowBlock*
        and *SimpleFlowBlock*, different constraints are created.
        The following constraints are created
        for all *InvestmentFlowBlock* objects:\

            Total capacity / energy

            .. math::
                &
                if \quad p=0:\\
                &
                P_{total}(p) = P_{invest}(p) + P_{exist}(p) \\
                &\\
                &
                else:\\
                &
                P_{total}(p) = P_{total}(p-1) + P_{invest}(p) - P_{old}(p) \\
                &\\
                &
                \forall p \in \textrm{PERIODS}

            Upper bound for the flow value

            .. math::
                &
                P(p, t) \le ( P_{total}(p) ) \cdot f_{max}(t) \\
                &
                \forall p, t \in \textrm{TIMEINDEX}

        For a multi-period model, the old capacity is defined as follows:

            .. math::
                &
                P_{old}(p) = P_{old,exo}(p) + P_{old,end}(p)\\
                &\\
                &
                if \quad p=0:\\
                &
                P_{old,end}(p) = 0\\
                &\\
                &
                else \quad if \quad l \leq year(p):\\
                &
                P_{old,end}(p) = P_{invest}(p_{comm})\\
                &\\
                &
                else:\\
                &
                P_{old,end}(p) = 0\\
                &\\
                &
                if \quad p=0:\\
                &
                P_{old,exo}(p) = 0\\
                &\\
                &
                else \quad if \quad l - a \leq year(p):\\
                &
                P_{old,exo}(p) = P_{exist} (*)\\
                &\\
                &
                else:\\
                &
                P_{old,exo}(p) = 0\\
                &\\
                &
                \forall p \in \textrm{PERIODS}

            where:

            * (*) is only performed for the first period the condition
              is True. A decommissioning flag is then set to True
              to prevent having falsely added old capacity in future periods.
            * :math:`year(p)` is the year corresponding to period p
            * :math:`p_{comm}` is the commissioning period of the flow
              (which is determined by the model itself)

        Depending on the attribute :attr:`nonconvex`, the constraints for the
        bounds of the decision variable :math:`P_{invest}(p)` are different:\

            * :attr:`nonconvex = False`

            .. math::
                &
                P_{invest, min}(p) \le P_{invest}(p) \le P_{invest, max}(p) \\
                &
                \forall p \in \textrm{PERIODS}

            * :attr:`nonconvex = True`

            .. math::
                &
                P_{invest, min}(p) \cdot Y_{invest}(p) \le P_{invest}(p)\\
                &
                P_{invest}(p) \le P_{invest, max}(p) \cdot Y_{invest}(p)\\
                &\\
                &
                \forall p \in \textrm{PERIODS}

        For all *InvestmentFlowBlock* objects
        (independent of the attribute :attr:`nonconvex`),
        the following additional constraints are created, if the appropriate
        attribute of the *SimpleFlowBlock*
        (see :class:`oemof.solph.flows._simple_flow_block.SimpleFlowBlock`)
        is set:

            * :attr:`fix` is not None

                Actual value constraint for investments with fixed flow values

            .. math::
                &
                P(p, t) = P_{total}(p) \cdot f_{fix}(t) \\
                &\\
                &
                \forall p, t \in \textrm{TIMEINDEX}

            * :attr:`min != 0`

                Lower bound for the flow values

            .. math::
                &
                P(p, t) \geq P_{total}(p) \cdot f_{min}(t) \\
                &\\
                &
                \forall p, t \in \textrm{TIMEINDEX}

            * :attr:`full_load_time_max is not None`

                Upper bound for the sum of all flow values
                (e.g. maximum full load hours)

            .. math::
                \sum_{p, t} P(p, t) \cdot \tau(t) \leq P_{total}(p)
                \cdot t_{full\_load, min}

            * :attr:`full_load_time_min is not None`

                Lower bound for the sum of all flow values
                (e.g. minimum full load hours)

            .. math::
                \sum_{p, t} P(t) \cdot \tau(t) \geq P_{total}
                \cdot t_{full\_load, min}

            * :attr:`overall_maximum` is not None
              (for multi-period model only)

                Overall maximum of total installed capacity / energy for flow

            .. math::
                &
                P_{total}(p) \leq P_{overall,max} \\
                &\\
                &
                \forall p \in \textrm{PERIODS}

            * :attr:`overall_minimum` is not None
              (for multi-period model only)

                Overall minimum of total installed capacity / energy for flow;
                applicable only in last period

            .. math::
                P_{total}(p_{last}) \geq P_{overall,min}
        """
        m = self.parent_block()

        self.minimum_rule = self._minimum_investment_constraint()
        self.maximum_rule = self._maximum_investment_constraint()

        # Handle unit lifetimes
        def _total_capacity_rule(block):
            """Rule definition for determining total installed
            capacity (taking decommissioning into account)
            """
            for i, o in self.INVESTFLOWS:
                expr = (
                        self.total_capacity[i, o]
                        == self.invest[i, o]
                        + m.flows[i, o].investment.existing
                    )
                self.total_rule.add((i, o), expr)

        self.total_rule = Constraint(
            self.INVESTFLOWS, noruleinit=True
        )
        self.total_rule_build = BuildAction(rule=_total_capacity_rule)

        def _investflow_fixed_rule(block):
            """Rule definition of constraint to fix flow variable
            of investment flow to (normed) actual value
            """
            for i, o in self.FIXED_INVESTFLOWS:
                for t in m.TIMESTEPS:
                    expr = (
                        m.flow[i, o, t]
                        == self.total_capacity[i, o] * m.flows[i, o].fix[t]
                    )
                    self.fixed.add((i, o, t), expr)

        self.fixed = Constraint(
            self.FIXED_INVESTFLOWS, m.TIMESTEPS, noruleinit=True
        )
        self.fixed_build = BuildAction(rule=_investflow_fixed_rule)

        def _max_investflow_rule(block):
            """Rule definition of constraint setting an upper bound of flow
            variable in investment case.
            """
            for i, o in self.NON_FIXED_INVESTFLOWS:
                for t in m.TIMESTEPS:
                    expr = (
                        m.flow[i, o, t]
                        <= self.total_capacity[i, o] * m.flows[i, o].max[t]
                    )
                    self.max.add((i, o, t), expr)

        self.max = Constraint(
            self.NON_FIXED_INVESTFLOWS, m.TIMESTEPS, noruleinit=True
        )
        self.max_build = BuildAction(rule=_max_investflow_rule)

        def _min_investflow_rule(block):
            """Rule definition of constraint setting a lower bound on flow
            variable in investment case.
            """
            for i, o in self.MIN_INVESTFLOWS:
                for t in m.TIMESTEPS:
                    expr = (
                        m.flow[i, o, t]
                        >= self.total_capacity[i, o] * m.flows[i, o].min[t]
                    )
                    self.min.add((i, o, t), expr)

        self.min = Constraint(
            self.MIN_INVESTFLOWS, m.TIMESTEPS, noruleinit=True
        )
        self.min_build = BuildAction(rule=_min_investflow_rule)

        def _full_load_time_max_investflow_rule(_, i, o):
            """Rule definition for build action of max. sum flow constraint
            in investment case.
            """
            expr = sum(
                m.flow[i, o, t] * m.timeincrement[t] for t in m.TIMESTEPS
            ) <= (
                m.flows[i, o].full_load_time_max * self.total_capacity[i, o]
            )
            return expr

        self.full_load_time_max = Constraint(
            self.FULL_LOAD_TIME_MAX_INVESTFLOWS,
            rule=_full_load_time_max_investflow_rule,
        )

        def _full_load_time_min_investflow_rule(_, i, o):
            """Rule definition for build action of min. sum flow constraint
            in investment case.
            """
            expr = sum(
                m.flow[i, o, t] * m.timeincrement[t] for t in m.TIMESTEPS
            ) >= (
                self.total_capacity[i, o] * m.flows[i, o].full_load_time_min
            )
            return expr

        self.full_load_time_min = Constraint(
            self.FULL_LOAD_TIME_MIN_INVESTFLOWS,
            rule=_full_load_time_min_investflow_rule,
        )

    def _objective_expression(self):
        r"""Objective expression for flows with investment attribute of type
        class:`.Investment`. The returned costs are fixed and
        investment costs. Variable costs are added from the standard flow
        objective expression.

        Objective terms for a standard model and a multi-period model differ
        quite strongly. Besides, the part of the objective function added by
        the *InvestmentFlowBlock* also depends on whether a convex
        or nonconvex *InvestmentFlowBlock* is selected.
        The following parts of the objective function are created:

        *Standard model*

            * :attr:`nonconvex = False`

                .. math::
                    P_{invest}(0) \cdot c_{invest,var}(0)

            * :attr:`nonconvex = True`

                .. math::
                    P_{invest}(0) \cdot c_{invest,var}(0)
                    + c_{invest,fix}(0) \cdot Y_{invest}(0) \\

        Where 0 denotes the 0th (investment) period since
        in a standard model, there is only this one period.

        *Multi-period model*

            * :attr:`nonconvex = False`

                .. math::
                    &
                    P_{invest}(p) \cdot A(c_{invest,var}(p), l, ir)
                    \cdot \frac {1}{ANF(d, ir)} \cdot DF^{-p}\\
                    &\\
                    &
                    \forall p \in \textrm{PERIODS}

            In case, the remaining lifetime of an asset is greater than 0 and
            attribute `use_remaining_value` of the energy system is True,
            the difference in value for the investment period compared to the
            last period of the optimization horizon is accounted for
            as an adder to the investment costs:

                .. math::
                    &
                    P_{invest}(p) \cdot (A(c_{invest,var}(p), l_{r}, ir) -
                    A(c_{invest,var}(|P|), l_{r}, ir)\\
                    & \cdot \frac {1}{ANF(l_{r}, ir)} \cdot DF^{-|P|}\\
                    &\\
                    &
                    \forall p \in \textrm{PERIODS}

            * :attr:`nonconvex = True`

                .. math::
                    &
                    (P_{invest}(p) \cdot A(c_{invest,var}(p), l, ir)
                    \cdot \frac {1}{ANF(d, ir)}\\
                    &
                    +  c_{invest,fix}(p) \cdot b_{invest}(p)) \cdot DF^{-p}\\
                    &\\
                    &
                    \forall p \in \textrm{PERIODS}

            In case, the remaining lifetime of an asset is greater than 0 and
            attribute `use_remaining_value` of the energy system is True,
            the difference in value for the investment period compared to the
            last period of the optimization horizon is accounted for
            as an adder to the investment costs:

                .. math::
                    &
                    (P_{invest}(p) \cdot (A(c_{invest,var}(p), l_{r}, ir) -
                    A(c_{invest,var}(|P|), l_{r}, ir)\\
                    & \cdot \frac {1}{ANF(l_{r}, ir)} \cdot DF^{-|P|}\\
                    &
                    +  (c_{invest,fix}(p) - c_{invest,fix}(|P|))
                    \cdot b_{invest}(p)) \cdot DF^{-p}\\
                    &\\
                    &
                    \forall p \in \textrm{PERIODS}

            * :attr:`fixed_costs` not None for investments

                .. math::
                    &
                    (\sum_{pp=year(p)}^{limit_{end}}
                    P_{invest}(p) \cdot c_{fixed}(pp) \cdot DF^{-pp})
                    \cdot DF^{-p}\\
                    &\\
                    &
                    \forall p \in \textrm{PERIODS}

            * :attr:`fixed_costs` not None for existing capacity

                .. math::
                    \sum_{pp=0}^{limit_{exo}} P_{exist} \cdot c_{fixed}(pp)
                    \cdot DF^{-pp}


        where:

        * :math:`A(c_{invest,var}(p), l, ir)` A is the annuity for
          investment expenses :math:`c_{invest,var}(p)`, lifetime :math:`l`
          and interest rate :math:`ir`.
        * :math:`l_{r}` is the remaining lifetime at the end of the
          optimization horizon (in case it is greater than 0 and
          smaller than the actual lifetime).
        * :math:`ANF(d, ir)` is the annuity factor for duration :math:`d`
          and interest rate :math:`ir`.
        * :math:`d=min\{year_{max} - year(p), l\}` defines the
          number of years within the optimization horizon that investment
          annuities are accounted for.
        * :math:`year(p)` denotes the start year of period :math:`p`.
        * :math:`year_{max}` denotes the last year of the optimization
          horizon, i.e. at the end of the last period.
        * :math:`limit_{end}=min\{year_{max}, year(p) + l\}` is used as an
          upper bound to ensure fixed costs for endogenous investments
          to occur within the optimization horizon.
        * :math:`limit_{exo}=min\{year_{max}, l - a\}` is used as an
          upper bound to ensure fixed costs for existing capacities to occur
          within the optimization horizon. :math:`a` is the initial age
          of an asset.
        * :math:`DF=(1+dr)` is the discount factor.

        The annuity / annuity factor hereby is:

            .. math::
                &
                A(c_{invest,var}(p), l, ir) = c_{invest,var}(p) \cdot
                    \frac {(1+ir)^l \cdot ir} {(1+ir)^l - 1}\\
                &\\
                &
                ANF(d, ir)=\frac {(1+ir)^d \cdot ir} {(1+ir)^d - 1}

        They are derived using the reciprocal of the oemof.tools.economics
        annuity function with a capex of 1.
        The interest rate :math:`ir` for the annuity is defined as weighted
        average costs of capital (wacc) and assumed constant over time.
        """
        if not hasattr(self, "INVESTFLOWS"):
            return 0

        m = self.parent_block()
        investment_costs = 0
        fixed_costs = 0

        for i, o in self.CONVEX_INVESTFLOWS:
            investment_costs += (
                self.invest[i, o]
                * m.flows[i, o].investment.ep_costs
            )

        for i, o in self.NON_CONVEX_INVESTFLOWS:
            investment_costs += (
                self.invest[i, o]
                * m.flows[i, o].investment.ep_costs
                + self.invest_status[i, o]
                * m.flows[i, o].investment.offset
            )

        self.investment_costs = Expression(expr=investment_costs)
        self.fixed_costs = Expression(expr=fixed_costs)
        self.costs = Expression(expr=investment_costs + fixed_costs)

        return self.costs


    def _minimum_investment_constraint(self):
        """Constraint factory for a minimum investment"""
        m = self.parent_block()

        def _min_invest_rule(_):
            """Rule definition for applying a minimum investment"""
            for i, o in self.NON_CONVEX_INVESTFLOWS:
                expr = (
                    m.flows[i, o].investment.minimum
                    * self.invest_status[i, o]
                    <= self.invest[i, o]
                )
                self.minimum_rule.add((i, o), expr)

        self.minimum_rule = Constraint(
            self.NON_CONVEX_INVESTFLOWS, noruleinit=True
        )
        self.minimum_rule_build = BuildAction(rule=_min_invest_rule)

        return self.minimum_rule

    def _maximum_investment_constraint(self):
        """Constraint factory for a maximum investment"""
        m = self.parent_block()

        def _max_invest_rule(_):
            """Rule definition for applying a minimum investment"""
            for i, o in self.NON_CONVEX_INVESTFLOWS:
                expr = self.invest[i, o, p] <= (
                    m.flows[i, o].investment.maximum
                    * self.invest_status[i, o]
                )
                self.maximum_rule.add((i, o), expr)

        self.maximum_rule = Constraint(
            self.NON_CONVEX_INVESTFLOWS, noruleinit=True
        )
        self.maximum_rule_build = BuildAction(rule=_max_invest_rule)

        return self.maximum_rule
