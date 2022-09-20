# -*- coding: utf-8 -*-

"""Creating sets, variables, constraints and parts of the objective function
for NonConvexInvestFlowBlock objects with both Nonconvex and Investment
options.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: jmloenneberga
SPDX-FileCopyrightText: Johannes Kochems (jokochems)
SPDX-FileCopyrightText: Saeed Sayadi
SPDX-FileCopyrightText: Pierre-François Duc

SPDX-License-Identifier: MIT

"""
from pyomo.core import Binary
from pyomo.core import Constraint
from pyomo.core import Expression
from pyomo.core import NonNegativeReals
from pyomo.core import Set
from pyomo.core import Var

from ._non_convex_flow_block import NonConvexFlowBlock


class InvestNonConvexFlowBlock(NonConvexFlowBlock):
    r"""
    .. automethod:: _create_constraints
    .. automethod:: _create_variables
    .. automethod:: _create_sets

    .. automethod:: _objective_expression


    **The following parts of the objective function are created similar
    to the <class 'oemof.solph.flows.NonConvexFlow'> class:**

    If `nonconvex.startup_costs` is set by the user:
        .. math::
            \sum_{i, o \in STARTUPFLOWS} \sum_t  startup(i, o, t) \
            \cdot startup\_costs(i, o)

    If `nonconvex.shutdown_costs` is set by the user:
        .. math::
            \sum_{i, o \in SHUTDOWNFLOWS} \sum_t shutdown(i, o, t) \
            \cdot shutdown\_costs(i, o)

    **The following parts of the objective function are created similar
    to the <class 'oemof.solph.flows.InvestmentFlow'> class:**

    .. math::
        P_{invest} \cdot c_{invest,var}
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """Creates set, variables, constraints for all flow object with
        an attribute flow of type class:`.NonConvexInvestFlowBlock`.

        Parameters
        ----------
        group : list
            List of oemof.solph.NonConvexInvestFlowBlock objects for which
            the constraints are build.
        """
        if group is None:
            return None

        self._create_sets(group)
        self._create_variables()
        self._create_constraints()

    def _create_sets(self, group):
        """
        Creates all sets for investment non-convex flows.

        .. glossary::

            INVEST_NON_CONVEX_FLOWS
                A set of flows with the attribute `nonconvex` of type
                :class:`.options.NonConvex` and the attribute `invest`
                of type :class:`.options.Invest`.

            MIN_FLOWS
                A subset of set NONCONVEX_FLOWS with the attribute `min`
                being not None in the first timestep.

            STARTUPFLOWS
                A subset of set NONCONVEX_FLOWS with the attribute
                `maximum_startups` or `startup_costs`
                being not None.

            MAXSTARTUPFLOWS
                A subset of set STARTUPFLOWS with the attribute
                `maximum_startups` being not None.

            SHUTDOWNFLOWS
                A subset of set NONCONVEX_FLOWS with the attribute
                `maximum_shutdowns` or `shutdown_costs`
                being not None.

            MAXSHUTDOWNFLOWS
                A subset of set SHUTDOWNFLOWS with the attribute
                `maximum_shutdowns` being not None.

            MINUPTIMEFLOWS
                A subset of set NONCONVEX_FLOWS with the attribute
                `minimum_uptime` being not None.

            MINDOWNTIMEFLOWS
                A subset of set NONCONVEX_FLOWS with the attribute
                `minimum_downtime` being not None.

            POSITIVE_GRADIENT_FLOWS
                A subset of set NONCONVEX_FLOWS with the attribute
                `positive_gradient` being not None.

            NEGATIVE_GRADIENT_FLOWS
                A subset of set NONCONVEX_FLOWS with the attribute
                `negative_gradient` being not None.
        """
        self.INVEST_NON_CONVEX_FLOWS = Set(
            initialize=[(g[0], g[1]) for g in group]
        )

        self._sets_for_non_convex_flows(group)

    def _create_variables(self):
        r"""
        Status variable (binary) `om.NonConvexInvestFlowBlock.status`:
            Variable indicating if flow is >= 0 indexed by FLOWS

        :math:`P_{invest}` `NonConvexInvestFlowBlock.invest`
            Value of the investment variable, i.e. equivalent to the nominal
            value of the flows after optimization.

        :math:`status\_nominal(i,o,t)` (non-negative real number)
            New paramater representing the multiplication of `P_{invest}`
            (from the <class 'oemof.solph.flows.InvestmentFlow'>) and
            `status(i,o,t)` (from the
            <class 'oemof.solph.flows.NonConvexFlow'>)
            used for the constraints on the minimum and maximum
            flow constraints.

        .. automethod:: _variables_for_non_convex_flows
        """

        m = self.parent_block()
        # Create `status` variable representing the status of the flow
        # at each time step
        self.status = Var(
            self.INVEST_NON_CONVEX_FLOWS, m.TIMESTEPS, within=Binary
        )

        self._variables_for_non_convex_flows()

        # Investment-related variable similar to the
        # <class 'oemof.solph.flows.InvestmentFlow'> class.

        def _investvar_bound_rule(block, i, o):
            """Rule definition for bounds of the invest variable."""
            if (i, o) in self.INVEST_NON_CONVEX_FLOWS:
                return 0, m.flows[i, o].investment.maximum

        # Create the `invest` variable for the nonconvex investment flow.
        self.invest = Var(
            self.INVEST_NON_CONVEX_FLOWS,
            within=NonNegativeReals,
            bounds=_investvar_bound_rule,
        )

        # `status_nominal` is a parameter which represents the
        # multiplication of a binary variable (`status`)
        # and a continuous variable (`invest` or `nominal_value`)
        self.status_nominal = Var(
            self.INVEST_NON_CONVEX_FLOWS, m.TIMESTEPS, within=NonNegativeReals
        )

    def _create_constraints(self):
        r"""
        .. automethod:: _shared_constraints_for_non_convex_flows
        .. automethod:: _minimum_invest_constraint
        .. automethod:: _maximum_invest_constraint
        .. automethod:: _minimum_flow_constraint
        .. automethod:: _maximum_flow_constraint
        .. automethod:: _linearised_investment_constraints
        """
        self._shared_constraints_for_non_convex_flows()

        self.minimum_investment = self._minimum_invest_constraint()
        self.maximum_investment = self._maximum_invest_constraint()

        self.min = self._minimum_flow_constraint()
        self.max = self._maximum_flow_constraint()

        self._linearised_investment_constraints()

    def _linearised_investment_constraints(self):
        r"""
        The resulting constraint is equivalent to

        .. math::
            status\_nominal(i,o,t) = status(i,o,t) \cdot P_{invest}.

        However, :math:`status` and :math:`invest` are variables
        (binary and continuous, respectively).
        Thus, three constraints are created which combination is equivalent.


        .. automethod:: _linearised_investment_constraint_1
        .. automethod:: _linearised_investment_constraint_2
        .. automethod:: _linearised_investment_constraint_3

        The following cases may occur:

        * Case :math:`status = 0`
            .. math::
                (1) \Rightarrow status\_nominal = 0,\\
                (2) \Rightarrow \text{ trivially fulfilled},\\
                (3) \Rightarrow \text{ trivially fulfilled}.

        * Case :math:`status = 1`
            .. math::
                (1) \Rightarrow \text{ trivially fulfilled},\\
                (2) \Rightarrow status\_nominal \leq P_{invest},\\
                (3) \Rightarrow status\_nominal \geq P_{invest}.

            So, in total :math:`status\_nominal = P_{invest}`,
            which is the desired result.
        """
        self.invest_nc_one = self._linearised_investment_constraint_1()
        self.invest_nc_two = self._linearised_investment_constraint_2()
        self.invest_nc_three = self._linearised_investment_constraint_3()

    def _linearised_investment_constraint_1(self):
        r"""
        .. math::
            status\_nominal(i,o,t)
            \leq status(i,o,t) \cdot P_{invest, max}\quad (1)
        """
        m = self.parent_block()

        def _linearization_rule_invest_non_convex_one(_, i, o, t):
            expr = (
                self.status[i, o, t] * m.flows[i, o].investment.maximum
                >= self.status_nominal[i, o, t]
            )
            return expr

        return Constraint(
            self.MIN_FLOWS,
            m.TIMESTEPS,
            rule=_linearization_rule_invest_non_convex_one,
        )

    def _linearised_investment_constraint_2(self):
        r"""
        .. math::
            status\_nominal(i,o,t) \leq P_{invest}\quad (2)
        """

        m = self.parent_block()

        def _linearization_rule_invest_non_convex_two(_, i, o, t):
            expr = self.invest[i, o] >= self.status_nominal[i, o, t]
            return expr

        return Constraint(
            self.MIN_FLOWS,
            m.TIMESTEPS,
            rule=_linearization_rule_invest_non_convex_two,
        )

    def _linearised_investment_constraint_3(self):
        r"""
        .. math::
            status\_nominal(i,o,t) \geq
            P_{invest} - (1 - status(i,o,t)) \cdot P_{invest, max}\quad (3)
        """

        m = self.parent_block()

        def _linearization_rule_invest_non_convex_three(_, i, o, t):
            expr = (
                self.invest[i, o]
                - (1 - self.status[i, o, t]) * m.flows[i, o].investment.maximum
                <= self.status_nominal[i, o, t]
            )
            return expr

        return Constraint(
            self.MIN_FLOWS,
            m.TIMESTEPS,
            rule=_linearization_rule_invest_non_convex_three,
        )

    def _objective_expression(self):
        r"""Objective expression for nonconvex investment flows."""
        if not hasattr(self, "INVEST_NON_CONVEX_FLOWS"):
            return 0

        m = self.parent_block()

        startup_costs = self._startup_costs()
        shutdown_costs = self._shutdown_costs()
        activity_costs = self._activity_costs()
        inactivity_costs = self._inactivity_costs()
        investment_costs = 0

        for i, o in self.INVEST_NON_CONVEX_FLOWS:
            investment_costs += (
                self.invest[i, o] * m.flows[i, o].investment.ep_costs
                + m.flows[i, o].investment.offset
            )

        self.investment_costs = Expression(expr=investment_costs)

        return (
            startup_costs
            + shutdown_costs
            + activity_costs
            + inactivity_costs
            + investment_costs
        )

    def _minimum_invest_constraint(self):
        r"""
        .. math::
                P_{invest, min} \le P_{invest}
        """
        m = self.parent_block()

        def _min_invest_rule(_, i, o):
            """Rule definition for applying a minimum investment"""
            expr = m.flows[i, o].investment.minimum <= self.invest[i, o]
            return expr

        return Constraint(self.INVEST_NON_CONVEX_FLOWS, rule=_min_invest_rule)

    def _maximum_invest_constraint(self):
        r"""
        .. math::
            P_{invest} \le P_{invest, max}
        """
        m = self.parent_block()

        def _max_invest_rule(_, i, o):
            """Rule definition for applying a minimum investment"""
            expr = self.invest[i, o] <= m.flows[i, o].investment.maximum
            return expr

        return Constraint(
            self.INVEST_NON_CONVEX_FLOWS, rule=_max_invest_rule
        )
