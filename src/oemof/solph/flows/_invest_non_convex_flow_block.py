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
    **The following sets are created similar to the
    <class 'oemof.solph.flows.NonConvexFlow'> class:**
    (-> see basic sets at :class:`.Model` )

    .. automethod:: _create_variables
    .. automethod:: _create_sets

    **The following variables are created similar to the
    <class 'oemof.solph.flows.NonConvexFlow'> class:**

    Status variable (binary) `om.NonConvexInvestFlowBlock.status`:
        Variable indicating if flow is >= 0 indexed by FLOWS

    Startup variable (binary) `om.NonConvexInvestFlowBlock.startup`:
        Variable indicating startup of flow (component) indexed by
        STARTUPFLOWS

    Shutdown variable (binary) `om.NonConvexInvestFlowBlock.shutdown`:
        Variable indicating shutdown of flow (component) indexed by
        SHUTDOWNFLOWS

    Positive gradient (continuous)
        `om.NonConvexInvestFlowBlock.positive_gradient`:
        Variable indicating the positive gradient, i.e. the load increase
        between two consecutive timesteps, indexed by
        POSITIVE_GRADIENT_FLOWS

    Negative gradient (continuous)
        `om.NonConvexInvestFlowBlock.negative_gradient`:
        Variable indicating the negative gradient, i.e. the load decrease
        between two consecutive timesteps, indexed by
        NEGATIVE_GRADIENT_FLOWS


    **The following constraints are created similar to the
    <class 'oemof.solph.flows.NonConvexFlow'> class:**

    Startup constraint `om.NonConvexInvestFlowBlock.startup_constr[i,o,t]`
        .. math::
            startup(i, o, t) \geq \
                status(i,o,t) - status(i, o, t-1) \\
            \forall t \in \textrm{TIMESTEPS}, \\
            \forall (i,o) \in \textrm{STARTUPFLOWS}.

    Maximum startups constraint
      `om.NonConvexInvestFlowBlock.max_startup_constr[i,o,t]`
        .. math::
            \sum_{t \in \textrm{TIMESTEPS}} startup(i, o, t) \leq \
                N_{start}(i,o)
            \forall (i,o) \in \textrm{MAXSTARTUPFLOWS}.

    Shutdown constraint
        `om.NonConvexInvestFlowBlock.shutdown_constr[i,o,t]`
            .. math::
                shutdown(i, o, t) \geq \
                    status(i, o, t-1) - status(i, o, t) \\
                \forall t \in \textrm{TIMESTEPS}, \\
                \forall (i, o) \in \textrm{SHUTDOWNFLOWS}.

    Maximum shutdowns constraint
        `om.NonConvexInvestFlowBlock.max_startup_constr[i,o,t]`
            .. math::
                \sum_{t \in \textrm{TIMESTEPS}} startup(i, o, t) \leq \
                    N_{shutdown}(i,o)
                \forall (i,o) \in \textrm{MAXSHUTDOWNFLOWS}.

    Minimum uptime constraint
        `om.NonConvexInvestFlowBlock.uptime_constr[i,o,t]`
            .. math::
                (status(i, o, t)-status(i, o, t-1))
                \cdot minimum\_uptime(i, o) \\
                \leq \sum_{n=0}^{minimum\_uptime-1} status(i,o,t+n) \\
                \forall t \in \textrm{TIMESTEPS} | \\
                t \neq \{0..minimum\_uptime\} \cup \
                \{t\_max-minimum\_uptime..t\_max\} , \\
                \forall (i,o) \in \textrm{MINUPTIMEFLOWS}.
                \\ \\
                status(i, o, t) = initial\_status(i, o) \\
                \forall t \in \textrm{TIMESTEPS} | \\
                t = \{0..minimum\_uptime\} \cup \
                \{t\_max-minimum\_uptime..t\_max\} , \\
                \forall (i,o) \in \textrm{MINUPTIMEFLOWS}.

    Minimum downtime constraint
        `om.NonConvexInvestFlowBlock.downtime_constr[i,o,t]`
            .. math::
                (status(i, o, t-1)-status(i, o, t)) \
                \cdot minimum\_downtime(i, o) \\
                \leq minimum\_downtime(i, o) \
                - \sum_{n=0}^{minimum\_downtime-1} status(i,o,t+n) \\
                \forall t \in \textrm{TIMESTEPS} | \\
                t \neq \{0..minimum\_downtime\} \cup \
                \{t\_max-minimum\_downtime..t\_max\} , \\
                \forall (i,o) \in \textrm{MINDOWNTIMEFLOWS}.
                \\ \\
                status(i, o, t) = initial\_status(i, o) \\
                \forall t \in \textrm{TIMESTEPS} | \\
                t = \{0..minimum\_downtime\} \cup \
                \{t\_max-minimum\_downtime..t\_max\} , \\
                \forall (i,o) \in \textrm{MINDOWNTIMEFLOWS}.

    Positive gradient constraint
        `om.NonConvexInvestFlowBlock.positive_gradient_constr[i, o]`:
            .. math:: flow(i, o, t) \cdot status(i, o, t)
                - flow(i, o, t-1) \cdot status(i, o, t-1)  \geq \
                positive\_gradient(i, o, t), \\
                \forall (i, o) \in \textrm{POSITIVE\_GRADIENT\_FLOWS}, \\
                \forall t \in \textrm{TIMESTEPS}.

    Negative gradient constraint
        `om.NonConvexInvestFlowBlock.negative_gradient_constr[i, o]`:
            .. math::
                flow(i, o, t-1) \cdot status(i, o, t-1)
                - flow(i, o, t) \cdot status(i, o, t) \geq \
                negative\_gradient(i, o, t), \\
                \forall (i, o) \in \textrm{NEGATIVE\_GRADIENT\_FLOWS}, \\
                \forall t \in \textrm{TIMESTEPS}.


    **The following constraints are created similar to the
    <class 'oemof.solph.flows.InvestmentFlow'> class:**

    Upper and lower bounds for the investment
        .. math::
            P_{invest, min} \le P_{invest} \le P_{invest, max}


    **The following constraints are new and created in the
    <class 'oemof.solph.flows.NonConvexInvestFlow'> class:**

    Minimum flow constraint `om.NonConvexInvestFlowBlock.min[i,o,t]`
        .. math::
            flow(i, o, t) \geq min(i, o, t)
            \cdot invest\_non\_convex(i, o, t),\\
            \forall t \in \textrm{TIMESTEPS}, \\
            \forall (i, o) \in \textrm{NONCONVEX\_INVESTMENT\_FLOWS}.

    Maximum flow constraint `om.NonConvexInvestFlowBlock.max[i,o,t]`
        .. math::
            flow(i, o, t) \leq max(i, o, t) invest\_non\_convex(i, o, t), \\
            \forall t \in \textrm{TIMESTEPS}, \\
            \forall (i, o) \in \textrm{NONCONVEX\_INVESTMENT\_FLOWS}.

    Additional constraints that must be used because the new
        parameter `invest\_non\_convex(i,o,t)` was introduced to deal with
        nonlinearity of the minimum and maximum flow constraints.

        .. math::
            invest\_non\_convex(i,o,t)
            \leq status(i,o,t) \cdot P_{invest, max}
            \\ \\
            invest\_non\_convex(i,o,t) \leq P_{invest}
            \\ \\
            invest\_non\_convex(i,o,t) \geq
            P_{invest} - (1 - status(i,o,t)) \cdot P_{invest, max}


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

    If `nonconvex.positive_gradient["costs"]` is set by the user:
        .. math::
            \sum_{i, o \in POSITIVE\_GRADIENT\_FLOWS} \sum_t
            positive\_gradient(i, o, t) \cdot positive\_gradient\_costs(i, o)

    If `nonconvex.negative_gradient["costs"]` is set by the user:
        .. math::
            \sum_{i, o \in NEGATIVE\_GRADIENT\_FLOWS} \sum_t
            negative\_gradient(i, o, t) \cdot negative\_gradient\_costs(i, o)


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
        **The following variables are created:**

        * :math:`P_{invest}`
            Value of the investment variable, i.e. equivalent to the nominal
            value of the flows after optimization.

        * :math:`invest\_non\_convex(i,o,t)` (non-negative real number)
            New paramater representing the multiplication of `P_{invest}`
            (from the <class 'oemof.solph.flows.InvestmentFlow'>) and
            `status(i,o,t)` (from the
            <class 'oemof.solph.flows.NonConvexFlow'>)
            used for the constraints on the minimum and maximum
            flow constraints.
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
        """
        Nonconvex-related constraints similar to the
        # <class 'oemof.solph.flows.NonConvexFlow'> class.
        """
        m = self.parent_block()

        self._shared_constraints_for_non_convex_flows()

        # Investment-related constraints similar to the
        # <class 'oemof.solph.flows.InvestmentFlow'> class.

        def _min_invest_rule(_, i, o):
            """Rule definition for applying a minimum investment"""
            expr = m.flows[i, o].investment.minimum <= self.invest[i, o]
            return expr

        self.minimum_rule = Constraint(
            self.INVEST_NON_CONVEX_FLOWS, rule=_min_invest_rule
        )

        def _max_invest_rule(_, i, o):
            """Rule definition for applying a minimum investment"""
            expr = self.invest[i, o] <= m.flows[i, o].investment.maximum
            return expr

        self.maximum_rule = Constraint(
            self.INVEST_NON_CONVEX_FLOWS, rule=_max_invest_rule
        )

        self.min = self._minimum_flow_constraint()
        self.max = self._maximum_flow_constraint()

        # z = x * y, where x is a binary variable (in our case `status`),
        # y is a continuous variable (in our case `status_nominal`),
        # and z denotes the new parameter `invest_non_convex`.
        # We define M as the upper bound of y (i.e., `investment.maximum`).
        # In order to linearize x * y, which is nonlinear, the following three
        # constraints are built.
        # These constraints are only needed for the CBC solver (and probably
        # other free open-source solvers) as Gurobi handles multiplication of
        # binary and continuous variables automatically.
        def _linearization_rule_invest_non_convex_one(_, i, o, t):
            """Rule definition for the linearization of the new parameter.
            :math:`xM \\ge z`

            """
            expr = (
                self.status[i, o, t] * m.flows[i, o].investment.maximum
                >= self.status_nominal[i, o, t]
            )
            return expr

        self.linearization_one = Constraint(
            self.MIN_FLOWS,
            m.TIMESTEPS,
            rule=_linearization_rule_invest_non_convex_one,
        )

        def _linearization_rule_invest_non_convex_two(_, i, o, t):
            """Rule definition for the linearization of the new parameter.

            :math:`y \\ge z`
            """
            expr = self.invest[i, o] >= self.status_nominal[i, o, t]
            return expr

        self.linearization_two = Constraint(
            self.MIN_FLOWS,
            m.TIMESTEPS,
            rule=_linearization_rule_invest_non_convex_two,
        )

        def _linearization_rule_invest_non_convex_three(_, i, o, t):
            """Rule definition for the linearization of the new parameter.

            :math:`z \\ge y - (1-x) M`

            when  :math:`x = 1`, then in combination with linearization rule 2
            :math:`z` is forced to be equal to :math:`y`

            when  :math:`x = 1`, then in combination with linearization rule 1
            :math:`z` is forced to be smaller or equal to 0 but since :math:`z`
            is defined as a non-negative value it is forced to be equal to 0
            """
            expr = (
                self.invest[i, o]
                - (1 - self.status[i, o, t]) * m.flows[i, o].investment.maximum
                <= self.status_nominal[i, o, t]
            )
            return expr

        self.linearization_three = Constraint(
            self.MIN_FLOWS,
            m.TIMESTEPS,
            rule=_linearization_rule_invest_non_convex_three,
        )

    # ################### OBJECTIVE FUNCTION #######################
    def _objective_expression(self):
        r"""Objective expression for nonconvex investment flows."""
        if not hasattr(self, "INVEST_NON_CONVEX_FLOWS"):
            return 0

        m = self.parent_block()

        startup_costs = self._startup_costs()
        shutdown_costs = self._shutdown_costs()
        activity_costs = self._activity_costs()
        inactivity_costs = self._inactivity_costs()
        gradient_costs = 0
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
            + gradient_costs
            + investment_costs
        )
