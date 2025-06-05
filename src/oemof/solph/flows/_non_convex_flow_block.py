# -*- coding: utf-8 -*-

"""Creating sets, variables, constraints and parts of the objective function
for Flow objects with nonconvex but without investment options.

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

from pyomo.core import Binary
from pyomo.core import BuildAction
from pyomo.core import Constraint
from pyomo.core import Expression
from pyomo.core import NonNegativeReals
from pyomo.core import Set
from pyomo.core import Var
from pyomo.core.base.block import ScalarBlock

from oemof.solph._plumbing import valid_sequence


class NonConvexFlowBlock(ScalarBlock):
    r"""
    .. automethod:: _create_constraints
    .. automethod:: _create_variables
    .. automethod:: _create_sets

    .. automethod:: _objective_expression

    Parameters are defined in :class:`Flow`.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """Creates set, variables, constraints for all flow object with
        an attribute flow of type class:`.NonConvexFlowBlock`.

        Parameters
        ----------
        group : list
            List of oemof.solph.NonConvexFlowBlock objects for which
            the constraints are build.
        """
        if group is None:
            return None

        self._create_sets(group)
        self._create_variables()
        self._create_constraints()

    def _create_sets(self, group):
        r"""
        **The following sets are created:** (-> see basic sets at
        :class:`.Model` )

        FIXED_CAPACITY_NONCONVEX_FLOWS
            A set of flows with the attribute `nonconvex` of type
            :class:`.options.NonConvex` and no investment.


        .. automethod:: _sets_for_non_convex_flows
        """
        self.FIXED_CAPACITY_NONCONVEX_FLOWS = Set(
            initialize=[(g[0], g[1]) for g in group]
        )

        NonConvexFlowBlock._sets_for_non_convex_flows(self, group)

    def _create_variables(self):
        r"""
        :math:`Y_{status}` (binary) `om.NonConvexFlowBlock.status`:
            Variable indicating if flow is >= 0

        :math:`P_{max,status}` Status_nominal (continuous)
            Variable indicating if flow is >= 0

        .. automethod:: _variables_for_non_convex_flows
        """
        m = self.parent_block()
        self.status = Var(
            self.FIXED_CAPACITY_NONCONVEX_FLOWS, m.TIMESTEPS, within=Binary
        )
        for o, i in self.FIXED_CAPACITY_NONCONVEX_FLOWS:
            if m.flows[o, i].nonconvex.initial_status is not None:
                for t in range(
                    0, m.flows[o, i].nonconvex.first_flexible_timestep
                ):
                    self.status[o, i, t] = m.flows[
                        o, i
                    ].nonconvex.initial_status
                    self.status[o, i, t].fix()

        # `status_nominal` is a parameter which represents the
        # multiplication of a binary variable (`status`)
        # and a continuous variable (`invest` or `nominal_capacity`)
        self.status_nominal = Var(
            self.FIXED_CAPACITY_NONCONVEX_FLOWS,
            m.TIMESTEPS,
            within=NonNegativeReals,
        )

        NonConvexFlowBlock._variables_for_non_convex_flows(self)

    def _create_constraints(self):
        """
        The following constraints are created:

        .. automethod:: _status_nominal_constraint
        .. automethod:: _minimum_flow_constraint
        .. automethod:: _maximum_flow_constraint
        .. automethod:: _shared_constraints_for_non_convex_flows

        """

        self.status_nominal_constraint = self._status_nominal_constraint()
        self.min = self._minimum_flow_constraint()
        self.max = self._maximum_flow_constraint()

        NonConvexFlowBlock._shared_constraints_for_non_convex_flows(self)

    def _objective_expression(self):
        r"""
        The following terms are to the cost function:

        .. automethod:: _startup_costs
        .. automethod:: _shutdown_costs
        .. automethod:: _activity_costs
        .. automethod:: _inactivity_costs
        """
        if not hasattr(self, "NONCONVEX_FLOWS"):
            return 0

        startup_costs = self._startup_costs()
        shutdown_costs = self._shutdown_costs()
        activity_costs = self._activity_costs()
        inactivity_costs = self._inactivity_costs()

        self.activity_costs = Expression(expr=activity_costs)
        self.inactivity_costs = Expression(expr=inactivity_costs)
        self.startup_costs = Expression(expr=startup_costs)
        self.shutdown_costs = Expression(expr=shutdown_costs)

        self.costs = Expression(
            expr=(
                startup_costs
                + shutdown_costs
                + activity_costs
                + inactivity_costs
            )
        )

        return self.costs

    @staticmethod
    def _sets_for_non_convex_flows(block, group):
        r"""Creates all sets for non-convex flows.

        MIN_FLOWS
            A subset of set NONCONVEX_FLOWS with the attribute `min`
            being not None in the first timestep.
        ACTIVITYCOSTFLOWS
            A subset of set NONCONVEX_FLOWS with the attribute
            `activity_costs` being not None.
        INACTIVITYCOSTFLOWS
            A subset of set NONCONVEX_FLOWS with the attribute
            `inactivity_costs` being not None.
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
            `minimum_uptime` being > 0.
        MINDOWNTIMEFLOWS
            A subset of set NONCONVEX_FLOWS with the attribute
            `minimum_downtime` being > 0.
        POSITIVE_GRADIENT_FLOWS
            A subset of set NONCONVEX_FLOWS with the attribute
            `positive_gradient` being not None.
        NEGATIVE_GRADIENT_FLOWS
            A subset of set NONCONVEX_FLOWS with the attribute
            `negative_gradient` being not None.
        """
        block.MIN_FLOWS = Set(
            initialize=[(g[0], g[1]) for g in group if g[2].min[0] is not None]
        )
        block.STARTUPFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.startup_costs[0] is not None
                or g[2].nonconvex.maximum_startups is not None
            ]
        )
        block.MAXSTARTUPFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.maximum_startups is not None
            ]
        )
        block.SHUTDOWNFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.shutdown_costs[0] is not None
                or g[2].nonconvex.maximum_shutdowns is not None
            ]
        )
        block.MAXSHUTDOWNFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.maximum_shutdowns is not None
            ]
        )
        block.MINUPTIMEFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.minimum_uptime.max() > 0
            ]
        )
        block.MINDOWNTIMEFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.minimum_downtime.max() > 0
            ]
        )
        block.NEGATIVE_GRADIENT_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.negative_gradient_limit[0] is not None
            ]
        )
        block.POSITIVE_GRADIENT_FLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.positive_gradient_limit[0] is not None
            ]
        )
        block.ACTIVITYCOSTFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.activity_costs[0] is not None
            ]
        )

        block.INACTIVITYCOSTFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.inactivity_costs[0] is not None
            ]
        )

    @staticmethod
    def _variables_for_non_convex_flows(block):
        r"""
        :math:`Y_{startup}` (binary) `NonConvexFlowBlock.startup`:
            Variable indicating startup of flow (component) indexed by
            STARTUPFLOWS

        :math:`Y_{shutdown}` (binary) `NonConvexFlowBlock.shutdown`:
            Variable indicating shutdown of flow (component) indexed by
            SHUTDOWNFLOWS

        :math:`\dot{P}_{up}` (continuous)
            `NonConvexFlowBlock.positive_gradient`:
            Variable indicating the positive gradient, i.e. the load increase
            between two consecutive timesteps, indexed by
            POSITIVE_GRADIENT_FLOWS

        :math:`\dot{P}_{down}` (continuous)
            `NonConvexFlowBlock.negative_gradient`:
            Variable indicating the negative gradient, i.e. the load decrease
            between two consecutive timesteps, indexed by
            NEGATIVE_GRADIENT_FLOWS
        """
        m = block.parent_block()

        if block.STARTUPFLOWS:
            block.startup = Var(block.STARTUPFLOWS, m.TIMESTEPS, within=Binary)

        if block.SHUTDOWNFLOWS:
            block.shutdown = Var(
                block.SHUTDOWNFLOWS, m.TIMESTEPS, within=Binary
            )

        if block.POSITIVE_GRADIENT_FLOWS:
            block.positive_gradient = Var(
                block.POSITIVE_GRADIENT_FLOWS,
                m.TIMESTEPS,
                within=NonNegativeReals,
            )

        if block.NEGATIVE_GRADIENT_FLOWS:
            block.negative_gradient = Var(
                block.NEGATIVE_GRADIENT_FLOWS,
                m.TIMESTEPS,
                within=NonNegativeReals,
            )

    def _startup_costs(self):
        r"""
        .. math::
            \sum_{i, o \in STARTUPFLOWS} \sum_t  Y_{startup}(t) \
            \cdot c_{startup}
        """
        startup_costs = 0

        if self.STARTUPFLOWS:
            m = self.parent_block()

            for i, o in self.STARTUPFLOWS:
                if valid_sequence(
                    m.flows[i, o].nonconvex.startup_costs, len(m.TIMESTEPS)
                ):
                    startup_costs += sum(
                        self.startup[i, o, t]
                        * m.flows[i, o].nonconvex.startup_costs[t]
                        for t in m.TIMESTEPS
                    )

            self.startup_costs = Expression(expr=startup_costs)

        return startup_costs

    def _shutdown_costs(self):
        r"""
        .. math::
            \sum_{SHUTDOWNFLOWS} \sum_t Y_{shutdown}(t) \
            \cdot c_{shutdown}
        """
        shutdown_costs = 0

        if self.SHUTDOWNFLOWS:
            m = self.parent_block()

            for i, o in self.SHUTDOWNFLOWS:
                if valid_sequence(
                    m.flows[i, o].nonconvex.shutdown_costs,
                    len(m.TIMESTEPS),
                ):
                    shutdown_costs += sum(
                        self.shutdown[i, o, t]
                        * m.flows[i, o].nonconvex.shutdown_costs[t]
                        * m.tsam_weighting[t]
                        for t in m.TIMESTEPS
                    )

            self.shutdown_costs = Expression(expr=shutdown_costs)

        return shutdown_costs

    def _activity_costs(self):
        r"""
        .. math::
            \sum_{ACTIVITYCOSTFLOWS} \sum_t Y_{status}(t) \
            \cdot c_{activity}
        """
        activity_costs = 0

        if self.ACTIVITYCOSTFLOWS:
            m = self.parent_block()

            for i, o in self.ACTIVITYCOSTFLOWS:
                if valid_sequence(
                    m.flows[i, o].nonconvex.activity_costs,
                    len(m.TIMESTEPS),
                ):
                    activity_costs += sum(
                        self.status[i, o, t]
                        * m.flows[i, o].nonconvex.activity_costs[t]
                        * m.tsam_weighting[t]
                        for t in m.TIMESTEPS
                    )

            self.activity_costs = Expression(expr=activity_costs)

        return activity_costs

    def _inactivity_costs(self):
        r"""
        .. math::
            \sum_{INACTIVITYCOSTFLOWS} \sum_t (1 - Y_{status}(t)) \
            \cdot c_{inactivity}
        """
        inactivity_costs = 0

        if self.INACTIVITYCOSTFLOWS:
            m = self.parent_block()

            for i, o in self.INACTIVITYCOSTFLOWS:
                if valid_sequence(
                    m.flows[i, o].nonconvex.inactivity_costs,
                    len(m.TIMESTEPS),
                ):
                    inactivity_costs += sum(
                        (1 - self.status[i, o, t])
                        * m.flows[i, o].nonconvex.inactivity_costs[t]
                        * m.tsam_weighting[t]
                        for t in m.TIMESTEPS
                    )

            self.inactivity_costs = Expression(expr=inactivity_costs)

        return inactivity_costs

    def _min_downtime_constraint(self):
        r"""
        .. math::
            (Y_{status}(t-1) - Y_{status}(t)) \
            \cdot t_{down,minimum} \\
            \leq t_{down,minimum} \
            - \sum_{n=0}^{t_{down,minimum}-1} Y_{status}(t+n) \\
            \forall t \in \textrm{TIMESTEPS} | \\
            t \neq \{0..t_{down,minimum}\} \cup \
            \{t\_max-t_{down,minimum}..t\_max\} , \\
            \forall (i,o) \in \textrm{MINDOWNTIMEFLOWS}.
            \\ \\
            Y_{status}(t) = Y_{status,0} \\
            \forall t \in \textrm{TIMESTEPS} | \\
            t = \{0..t_{down,minimum}\} \cup \
            \{t\_max-t_{down,minimum}..t\_max\} , \\
            \forall (i,o) \in \textrm{MINDOWNTIMEFLOWS}.
        """
        m = self.parent_block()

        def min_downtime_rule(_, i, o, t):
            """
            Rule definition for min-downtime constraints of non-convex flows.
            """
            if (
                m.flows[i, o].nonconvex.first_flexible_timestep
                < t
                < m.TIMESTEPS.at(-1)
            ):
                # We have a 2D matrix of constraints,
                # so testing is easier then just calling the rule for valid t.

                expr = 0
                expr += (
                    self.status[i, o, t - 1] - self.status[i, o, t]
                ) * m.flows[i, o].nonconvex.minimum_downtime[t]
                expr += -m.flows[i, o].nonconvex.minimum_downtime[t]
                expr += sum(
                    self.status[i, o, d]
                    for d in range(
                        t,
                        min(
                            t + m.flows[i, o].nonconvex.minimum_downtime[t],
                            len(m.TIMESTEPS),
                        ),
                    )
                )
                return expr <= 0
            else:
                return Constraint.Skip

        return Constraint(
            self.MINDOWNTIMEFLOWS, m.TIMESTEPS, rule=min_downtime_rule
        )

    def _min_uptime_constraint(self):
        r"""
        .. math::
            (Y_{status}(t)-Y_{status}(t-1)) \cdot t_{up,minimum} \\
            \leq \sum_{n=0}^{t_{up,minimum}-1} Y_{status}(t+n) \\
            \forall t \in \textrm{TIMESTEPS} | \\
            t \neq \{0..t_{up,minimum}\} \cup \
            \{t\_max-t_{up,minimum}..t\_max\} , \\
            \forall (i,o) \in \textrm{MINUPTIMEFLOWS}.
            \\ \\
            Y_{status}(t) = Y_{status,0} \\
            \forall t \in \textrm{TIMESTEPS} | \\
            t = \{0..t_{up,minimum}\} \cup \
            \{t\_max-t_{up,minimum}..t\_max\} , \\
            \forall (i,o) \in \textrm{MINUPTIMEFLOWS}.
        """
        m = self.parent_block()

        def _min_uptime_rule(_, i, o, t):
            """
            Rule definition for min-uptime constraints of non-convex flows.
            """
            if (
                m.flows[i, o].nonconvex.first_flexible_timestep
                < t
                < m.TIMESTEPS.at(-1)
            ):
                # We have a 2D matrix of constraints,
                # so testing is easier then just calling the rule for valid t.
                expr = 0
                expr += (
                    self.status[i, o, t] - self.status[i, o, t - 1]
                ) * m.flows[i, o].nonconvex.minimum_uptime[t]
                expr += -sum(
                    self.status[i, o, u]
                    for u in range(
                        t,
                        min(
                            t + m.flows[i, o].nonconvex.minimum_uptime[t],
                            len(m.TIMESTEPS),
                        ),
                    )
                )
                return expr <= 0
            else:
                return Constraint.Skip

        return Constraint(
            self.MINUPTIMEFLOWS, m.TIMESTEPS, rule=_min_uptime_rule
        )

    def _shutdown_constraint(self):
        r"""
        .. math::
            Y_{shutdown}(t) \geq Y_{status}(t-1) - Y_{status}(t) \\
            \forall t \in \textrm{TIMESTEPS}, \\
            \forall \textrm{SHUTDOWNFLOWS}.
        """
        m = self.parent_block()

        def _shutdown_rule(_, i, o, t):
            """Rule definition for shutdown constraints of non-convex flows."""
            if t > m.TIMESTEPS.at(1):
                expr = (
                    self.shutdown[i, o, t]
                    >= self.status[i, o, t - 1] - self.status[i, o, t]
                )
            else:
                expr = (
                    self.shutdown[i, o, t]
                    >= m.flows[i, o].nonconvex.initial_status
                    - self.status[i, o, t]
                )
            return expr

        return Constraint(self.SHUTDOWNFLOWS, m.TIMESTEPS, rule=_shutdown_rule)

    def _startup_constraint(self):
        r"""
        .. math::
            Y_{startup}(t) \geq Y_{status}(t) - Y_{status}(t-1) \\
            \forall t \in \textrm{TIMESTEPS}, \\
            \forall \textrm{STARTUPFLOWS}.
        """
        m = self.parent_block()

        def _startup_rule(_, i, o, t):
            """Rule definition for startup constraint of nonconvex flows."""
            if t > m.TIMESTEPS.at(1):
                expr = (
                    self.startup[i, o, t]
                    >= self.status[i, o, t] - self.status[i, o, t - 1]
                )
            else:
                expr = (
                    self.startup[i, o, t]
                    >= self.status[i, o, t]
                    - m.flows[i, o].nonconvex.initial_status
                )
            return expr

        return Constraint(self.STARTUPFLOWS, m.TIMESTEPS, rule=_startup_rule)

    def _max_startup_constraint(self):
        r"""
        .. math::
            \sum_{t \in \textrm{TIMESTEPS}} Y_{startup}(t) \leq \
                N_{start}(i,o)\\
            \forall (i,o) \in \textrm{MAXSTARTUPFLOWS}.
        """
        m = self.parent_block()

        def _max_startup_rule(_, i, o):
            """Rule definition for maximum number of start-ups."""
            lhs = sum(self.startup[i, o, t] for t in m.TIMESTEPS)
            return lhs <= m.flows[i, o].nonconvex.maximum_startups

        return Constraint(self.MAXSTARTUPFLOWS, rule=_max_startup_rule)

    def _max_shutdown_constraint(self):
        r"""
        .. math::
            \sum_{t \in \textrm{TIMESTEPS}} Y_{startup}(t) \leq \
                N_{shutdown}(i,o)\\
            \forall (i,o) \in \textrm{MAXSHUTDOWNFLOWS}.
        """
        m = self.parent_block()

        def _max_shutdown_rule(_, i, o):
            """Rule definition for maximum number of start-ups."""
            lhs = sum(self.shutdown[i, o, t] for t in m.TIMESTEPS)
            return lhs <= m.flows[i, o].nonconvex.maximum_shutdowns

        return Constraint(self.MAXSHUTDOWNFLOWS, rule=_max_shutdown_rule)

    def _maximum_flow_constraint(self):
        r"""
        .. math::
            P(t) \leq max(i, o, t) \cdot P_{nom} \
                \cdot status(t), \\
            \forall t \in \textrm{TIMESTEPS}, \\
            \forall (i, o) \in \textrm{NONCONVEX_FLOWS}.
        """
        m = self.parent_block()

        def _maximum_flow_rule(_, i, o, t):
            """Rule definition for MILP maximum flow constraints."""
            expr = (
                self.status_nominal[i, o, t] * m.flows[i, o].max[t]
                >= m.flow[i, o, t]
            )
            return expr

        return Constraint(self.MIN_FLOWS, m.TIMESTEPS, rule=_maximum_flow_rule)

    def _minimum_flow_constraint(self):
        r"""
        .. math::
            P(t) \geq min(i, o, t) \cdot P_{nom} \
                \cdot Y_{status}(t), \\
            \forall (i, o) \in \textrm{NONCONVEX_FLOWS}, \\
            \forall t \in \textrm{TIMESTEPS}.
        """
        m = self.parent_block()

        def _minimum_flow_rule(_, i, o, t):
            """Rule definition for MILP minimum flow constraints."""
            expr = (
                self.status_nominal[i, o, t] * m.flows[i, o].min[t]
                <= m.flow[i, o, t]
            )
            return expr

        return Constraint(self.MIN_FLOWS, m.TIMESTEPS, rule=_minimum_flow_rule)

    def _status_nominal_constraint(self):
        r"""
        .. math::
            P_{max,status}(t) =  Y_{status}(t) \cdot P_{nom}, \\
            \forall t \in \textrm{TIMESTEPS}.
        """
        m = self.parent_block()

        def _status_nominal_rule(_, i, o, t):
            """Rule definition for status_nominal"""
            expr = (
                self.status_nominal[i, o, t]
                == self.status[i, o, t] * m.flows[i, o].nominal_capacity
            )
            return expr

        return Constraint(
            self.FIXED_CAPACITY_NONCONVEX_FLOWS,
            m.TIMESTEPS,
            rule=_status_nominal_rule,
        )

    @staticmethod
    def _shared_constraints_for_non_convex_flows(block):
        r"""

        .. automethod:: _startup_constraint
        .. automethod:: _max_startup_constraint
        .. automethod:: _shutdown_constraint
        .. automethod:: _max_shutdown_constraint
        .. automethod:: _min_uptime_constraint
        .. automethod:: _min_downtime_constraint

        positive_gradient_constraint
            .. math::

                P(t) \cdot Y_{status}(t)
                - P(t-1) \cdot Y_{status}(t-1)  \leq \
                \dot{P}_{up}(t), \\
                \forall t \in \textrm{TIMESTEPS}.

        negative_gradient_constraint
            .. math::
                P(t-1) \cdot Y_{status}(t-1)
                - P(t) \cdot Y_{status}(t) \leq \
                \dot{P}_{down}(t), \\
                \forall t \in \textrm{TIMESTEPS}.
        """
        m = block.parent_block()

        block.startup_constr = block._startup_constraint()
        block.max_startup_constr = block._max_startup_constraint()
        block.shutdown_constr = block._shutdown_constraint()
        block.max_shutdown_constr = block._max_shutdown_constraint()
        block.min_uptime_constr = block._min_uptime_constraint()
        block.min_downtime_constr = block._min_downtime_constraint()

        def _positive_gradient_flow_constraint(_):
            r"""Rule definition for positive gradient constraint."""
            for i, o in block.POSITIVE_GRADIENT_FLOWS:
                for index in range(1, len(m.TIMEINDEX) + 1):
                    if m.TIMEINDEX[index][1] > 0:
                        lhs = (
                            m.flow[
                                i,
                                o,
                                m.TIMESTEPS[index],
                            ]
                            * block.status[i, o, m.TIMESTEPS[index]]
                            - m.flow[i, o, m.TIMESTEPS[index - 1]]
                            * block.status[i, o, m.TIMESTEPS[index - 1]]
                        )
                        rhs = block.positive_gradient[
                            i, o, m.TIMEINDEX[index][1]
                        ]
                        block.positive_gradient_constr.add(
                            (
                                i,
                                o,
                                m.TIMESTEPS[index],
                            ),
                            lhs <= rhs,
                        )
                    else:
                        lhs = block.positive_gradient[i, o, 0]
                        rhs = 0
                        block.positive_gradient_constr.add(
                            (
                                i,
                                o,
                                m.TIMESTEPS[index],
                            ),
                            lhs == rhs,
                        )

        block.positive_gradient_constr = Constraint(
            block.POSITIVE_GRADIENT_FLOWS, m.TIMESTEPS, noruleinit=True
        )
        block.positive_gradient_build = BuildAction(
            rule=_positive_gradient_flow_constraint
        )

        def _negative_gradient_flow_constraint(_):
            r"""Rule definition for negative gradient constraint."""
            for i, o in block.NEGATIVE_GRADIENT_FLOWS:
                for index in range(1, len(m.TIMESTEPS) + 1):
                    if m.TIMESTEPS[index] > 0:
                        lhs = (
                            m.flow[
                                i,
                                o,
                                m.TIMESTEPS[index - 1],
                            ]
                            * block.status[i, o, m.TIMESTEPS[index - 1]]
                            - m.flow[
                                i,
                                o,
                                m.TIMESTEPS[index],
                            ]
                            * block.status[i, o, m.TIMESTEPS[index]]
                        )
                        rhs = block.negative_gradient[i, o, m.TIMESTEPS[index]]
                        block.negative_gradient_constr.add(
                            (
                                i,
                                o,
                                m.TIMESTEPS[index],
                            ),
                            lhs <= rhs,
                        )
                    else:
                        lhs = block.negative_gradient[i, o, 0]
                        rhs = 0
                        block.negative_gradient_constr.add(
                            (
                                i,
                                o,
                                m.TIMESTEPS[index],
                            ),
                            lhs == rhs,
                        )

        block.negative_gradient_constr = Constraint(
            block.NEGATIVE_GRADIENT_FLOWS, m.TIMESTEPS, noruleinit=True
        )
        block.negative_gradient_build = BuildAction(
            rule=_negative_gradient_flow_constraint
        )
