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
from pyomo.core import BuildAction
from pyomo.core import Constraint
from pyomo.core import Expression
from pyomo.core import NonNegativeReals
from pyomo.core import Set
from pyomo.core import Var
from pyomo.core.base.block import ScalarBlock

from . import _non_convex_constraint_factories as nccf


class NonConvexInvestFlowBlock(ScalarBlock):
    r"""
    **The following sets are created similar to the
    <class 'oemof.solph.flows.NonConvexFlow'> class:**
    (-> see basic sets at :class:`.Model` )

    A set of flows with the attribute `nonconvex` of type
        :class:`.options.NonConvex`.
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


    **The following variables are created similar to the
    <class 'oemof.solph.flows.InvestmentFlow'> class:**

    * :math:`P_{invest}`
        Value of the investment variable, i.e. equivalent to the nominal
        value of the flows after optimization.


    **The following variable is a new variable created in the
    <class 'oemof.solph.flows.NonConvexInvestFlow'> class:**

    * :math: `invest_non_convex(i,o,t)` (non-negative real number)
        New paramater representing the multiplication of `P_{invest}`
        (from the <class 'oemof.solph.flows.InvestmentFlow'>) and
        `status(i,o,t)` (from the <class 'oemof.solph.flows.NonConvexFlow'>)
        used for the constraints on the minimum and maximum flow constraints.


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
            flow(i, o, t) \geq min(i, o, t) \cdot invest_non_convex(i, o, t),\\
            \forall t \in \textrm{TIMESTEPS}, \\
            \forall (i, o) \in \textrm{NONCONVEX\_INVESTMENT\_FLOWS}.

    Maximum flow constraint `om.NonConvexInvestFlowBlock.max[i,o,t]`
        .. math::
            flow(i, o, t) \leq max(i, o, t) invest_non_convex(i, o, t), \\
            \forall t \in \textrm{TIMESTEPS}, \\
            \forall (i, o) \in \textrm{NONCONVEX\_INVESTMENT\_FLOWS}.

    Additional constraints that must be used because the new
        parameter `invest_non_convex(i,o,t)` was introduced to deal with
        nonlinearity of the minimum and maximum flow constraints.

        .. math::
            invest_non_convex(i,o,t)
            \leq status(i,o,t) \cdot P_{invest, max}
            \\ \\
            invest_non_convex(i,o,t) \leq P_{invest}
            \\ \\
            invest_non_convex(i,o,t) \geq
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
            \sum_{i, o \in POSITIVE_GRADIENT_FLOWS} \sum_t
            positive_gradient(i, o, t) \cdot positive\_gradient\_costs(i, o)

    If `nonconvex.negative_gradient["costs"]` is set by the user:
        .. math::
            \sum_{i, o \in NEGATIVE_GRADIENT_FLOWS} \sum_t
            negative_gradient(i, o, t) \cdot negative\_gradient\_costs(i, o)


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
        self._create_variables(group)
        self._create_constraints()

    def _create_sets(self, group):
        """
        Nonconvex-related sets similar to the
        <class 'oemof.solph.flows.NonconvexFlow'> class.
        """
        self.MIN_FLOWS = Set(
            initialize=[(g[0], g[1]) for g in group if g[2].min[0] is not None]
        )
        self.STARTUPFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.startup_costs[0] is not None
                or g[2].nonconvex.maximum_startups is not None
            ]
        )
        self.MAXSTARTUPFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.maximum_startups is not None
            ]
        )
        self.SHUTDOWNFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.shutdown_costs[0] is not None
                or g[2].nonconvex.maximum_shutdowns is not None
            ]
        )
        self.MAXSHUTDOWNFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.maximum_shutdowns is not None
            ]
        )
        self.MINUPTIMEFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.minimum_uptime is not None
            ]
        )

        self.MINDOWNTIMEFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.minimum_downtime is not None
            ]
        )

        self.NEGATIVE_GRADIENT_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.negative_gradient["ub"][0] is not None
            ]
        )

        self.POSITIVE_GRADIENT_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.positive_gradient["ub"][0] is not None
            ]
        )

        # New nonconvex-investment-related set defines in the
        # <class 'oemof.solph.flows.NonconvexInvestFlow'> class.
        self.NON_CONVEX_INVEST_FLOWS = Set(
            initialize=[(g[0], g[1]) for g in group]
        )

    def _create_variables(self, groups):
        """
        Nonconvex-related variables similar to the
        <class 'oemof.solph.flows.NonConvexFlow'> class.
        """

        m = self.parent_block()
        # Create `status` variable representing the status of the flow
        # at each time step
        self.status = Var(
            self.NON_CONVEX_INVEST_FLOWS, m.TIMESTEPS, within=Binary
        )

        if self.STARTUPFLOWS:
            self.startup = Var(self.STARTUPFLOWS, m.TIMESTEPS, within=Binary)

        if self.SHUTDOWNFLOWS:
            self.shutdown = Var(self.SHUTDOWNFLOWS, m.TIMESTEPS, within=Binary)

        if self.POSITIVE_GRADIENT_FLOWS:
            self.positive_gradient = Var(
                self.POSITIVE_GRADIENT_FLOWS, m.TIMESTEPS
            )

        if self.NEGATIVE_GRADIENT_FLOWS:
            self.negative_gradient = Var(
                self.NEGATIVE_GRADIENT_FLOWS, m.TIMESTEPS
            )

        # Investment-related variable similar to the
        # <class 'oemof.solph.flows.InvestmentFlow'> class.

        def _investvar_bound_rule(block, i, o):
            """Rule definition for bounds of the invest variable."""
            if (i, o) in self.NON_CONVEX_INVEST_FLOWS:
                return 0, m.flows[i, o].investment.maximum

        # Create the `invest` variable for the nonconvex investment flow.
        self.invest = Var(
            self.NON_CONVEX_INVEST_FLOWS,
            within=NonNegativeReals,
            bounds=_investvar_bound_rule,
        )

        # New nonconvex-investment-related variable defined in the
        # <class 'oemof.solph.flows.NonConvexInvestFlow'> class.

        # `invest_non_convex` is a new parameter which represents the
        # multiplication of a binary variable (`status`) and a continuous
        # variable (`invest`):
        # self.invest_non_convex[i, o, t] = self.status[i, o, t]
        # * self.invest[i, o]
        self.invest_non_convex = Var(
            self.MIN_FLOWS, m.TIMESTEPS, within=NonNegativeReals
        )

    def _create_constraints(self):
        """
        Nonconvex-related constraints similar to the
        # <class 'oemof.solph.flows.NonConvexFlow'> class.
        """
        m = self.parent_block()

        self.startup_constr = nccf.startup_constraint(self)
        self.max_startup_constr = nccf.max_startup_constraint(self)
        self.shutdown_constr = nccf.shutdown_constraint(self)
        self.max_shutdown_constr = nccf.max_shutdown_constraint(self)

        self.min_uptime_constr = nccf.min_uptime_constraint(self)
        self.min_downtime_constr = nccf.min_downtime_constraint(self)

        def _positive_gradient_flow_rule(block):
            """Rule definition for positive gradient constraint."""
            for i, o in self.POSITIVE_GRADIENT_FLOWS:
                for t in m.TIMESTEPS:
                    if t > 0:
                        lhs = (
                            m.flow[i, o, t] * self.status[i, o, t]
                            - m.flow[i, o, t - 1] * self.status[i, o, t - 1]
                        )
                        rhs = self.positive_gradient[i, o, t]
                        self.positive_gradient_constr.add(
                            (i, o, t), lhs <= rhs
                        )
                    else:
                        pass  # return(Constraint.Skip)

        self.positive_gradient_constr = Constraint(
            self.POSITIVE_GRADIENT_FLOWS, m.TIMESTEPS, noruleinit=True
        )
        self.positive_gradient_build = BuildAction(
            rule=_positive_gradient_flow_rule
        )

        def _negative_gradient_flow_rule(block):
            """Rule definition for negative gradient constraint."""
            for i, o in self.NEGATIVE_GRADIENT_FLOWS:
                for t in m.TIMESTEPS:
                    if t > 0:
                        lhs = (
                            m.flow[i, o, t - 1] * self.status[i, o, t - 1]
                            - m.flow[i, o, t] * self.status[i, o, t]
                        )
                        rhs = self.negative_gradient[i, o, t]
                        self.negative_gradient_constr.add(
                            (i, o, t), lhs <= rhs
                        )
                    else:
                        pass  # return(Constraint.Skip)

        self.negative_gradient_constr = Constraint(
            self.NEGATIVE_GRADIENT_FLOWS, m.TIMESTEPS, noruleinit=True
        )
        self.negative_gradient_build = BuildAction(
            rule=_negative_gradient_flow_rule
        )

        # Investment-related constraints similar to the
        # <class 'oemof.solph.flows.InvestmentFlow'> class.

        def _min_invest_rule(block, i, o):
            """Rule definition for applying a minimum investment"""
            expr = m.flows[i, o].investment.minimum <= self.invest[i, o]
            return expr

        self.minimum_rule = Constraint(
            self.NON_CONVEX_INVEST_FLOWS, rule=_min_invest_rule
        )

        def _max_invest_rule(block, i, o):
            """Rule definition for applying a minimum investment"""
            expr = self.invest[i, o] <= (m.flows[i, o].investment.maximum)
            return expr

        self.maximum_rule = Constraint(
            self.NON_CONVEX_INVEST_FLOWS, rule=_max_invest_rule
        )

        # New nonconvex-investment-related constraints defined in the
        # <class 'oemof.solph.flows.NonConvexInvestFlow'> class.

        def _minimum_flow_rule(block, i, o, t):
            """Rule definition for MILP minimum flow constraints."""
            expr = (
                self.invest_non_convex[i, o, t] * m.flows[i, o].min[t]
                <= m.flow[i, o, t]
            )
            return expr

        self.min = Constraint(
            self.MIN_FLOWS, m.TIMESTEPS, rule=_minimum_flow_rule
        )

        def _maximum_flow_rule(block, i, o, t):
            """Rule definition for MILP maximum flow constraints."""
            expr = (
                self.invest_non_convex[i, o, t] * m.flows[i, o].max[t]
                >= m.flow[i, o, t]
            )
            return expr

        self.max = Constraint(
            self.MIN_FLOWS, m.TIMESTEPS, rule=_maximum_flow_rule
        )

        # z = x * y, where x is a binary variable (in our case `status`),
        # y is a continuous variable (in our case `invest`), and z denotes
        # the new parameter `invest_non_convex`.
        # We define M as the upper bound of y (i.e., `investment.maximum`).
        # In order to linearize x * y, which is nonlinear, the following three
        # constraints are built.
        # These constraints are only needed for the CBC solver (and probably
        # other free open-source solvers) as Gurobi handles multiplication of
        # binary and continuous variables automatically.
        def _linearization_rule_invest_non_convex_one(block, i, o, t):
            """Rule definition for the linearization of the new parameter.
            :math:`xM \\ge z`

            """
            expr = (
                self.status[i, o, t] * m.flows[i, o].investment.maximum
                >= self.invest_non_convex[i, o, t]
            )
            return expr

        self.linearization_one = Constraint(
            self.MIN_FLOWS,
            m.TIMESTEPS,
            rule=_linearization_rule_invest_non_convex_one,
        )

        def _linearization_rule_invest_non_convex_two(block, i, o, t):
            """Rule definition for the linearization of the new parameter.

            :math:`y \\ge z`
            """
            expr = self.invest[i, o] >= self.invest_non_convex[i, o, t]
            return expr

        self.linearization_two = Constraint(
            self.MIN_FLOWS,
            m.TIMESTEPS,
            rule=_linearization_rule_invest_non_convex_two,
        )

        def _linearization_rule_invest_non_convex_three(block, i, o, t):
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
                <= self.invest_non_convex[i, o, t]
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
        if not hasattr(self, "NON_CONVEX_INVEST_FLOWS"):
            return 0

        m = self.parent_block()

        startup_costs = 0
        shutdown_costs = 0
        gradient_costs = 0
        investment_costs = 0

        if self.STARTUPFLOWS:
            for i, o in self.STARTUPFLOWS:
                if m.flows[i, o].nonconvex.startup_costs[0] is not None:
                    startup_costs += sum(
                        self.startup[i, o, t]
                        * m.flows[i, o].nonconvex.startup_costs[t]
                        for t in m.TIMESTEPS
                    )
            self.startup_costs = Expression(expr=startup_costs)

        if self.SHUTDOWNFLOWS:
            for i, o in self.SHUTDOWNFLOWS:
                if m.flows[i, o].nonconvex.shutdown_costs[0] is not None:
                    shutdown_costs += sum(
                        self.shutdown[i, o, t]
                        * m.flows[i, o].nonconvex.shutdown_costs[t]
                        for t in m.TIMESTEPS
                    )
            self.shutdown_costs = Expression(expr=shutdown_costs)

        for i, o in self.NON_CONVEX_INVEST_FLOWS:
            investment_costs += (
                self.invest[i, o] * m.flows[i, o].investment.ep_costs
                + m.flows[i, o].investment.offset
            )

        self.investment_costs = Expression(expr=investment_costs)

        return (
            startup_costs + shutdown_costs + gradient_costs + investment_costs
        )
