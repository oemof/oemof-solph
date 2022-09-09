# -*- coding: utf-8 -*-

"""Creating sets, variables, constraints and parts of the objective function
for nonconvex SimpleFlowBlock objects.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: jmloenneberga
SPDX-FileCopyrightText: Johannes Kochems (jokochems)

SPDX-License-Identifier: MIT

"""

from pyomo.core import Binary
from pyomo.core import Constraint
from pyomo.core import Expression
from pyomo.core import NonNegativeReals
from pyomo.core import Set
from pyomo.core import Var
from pyomo.core.base.block import ScalarBlock

from ._shared import non_convex as nc


class NonConvexFlowBlock(ScalarBlock):
    r"""
    **The following sets are created:** (-> see basic sets at
    :class:`.Model` )

    A set of flows with the attribute `nonconvex` of type
        :class:`.options.NonConvex`.
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

    **The following variables are created:**

    Status variable (binary) `om.NonConvexFlowBlock.status`:
        Variable indicating if flow is >= 0 indexed by FLOWS

    Startup variable (binary) `om.NonConvexFlowBlock.startup`:
        Variable indicating startup of flow (component) indexed by
        STARTUPFLOWS

    Shutdown variable (binary) `om.NonConvexFlowBlock.shutdown`:
        Variable indicating shutdown of flow (component) indexed by
        SHUTDOWNFLOWS

    Positive gradient (continuous) `om.NonConvexFlowBlock.positive_gradient`:
        Variable indicating the positive gradient, i.e. the load increase
        between two consecutive timesteps, indexed by
        POSITIVE_GRADIENT_FLOWS

    Negative gradient (continuous) `om.NonConvexFlowBlock.negative_gradient`:
        Variable indicating the negative gradient, i.e. the load decrease
        between two consecutive timesteps, indexed by
        NEGATIVE_GRADIENT_FLOWS


    **The following constraints are created:**

    Minimum flow constraint `om.NonConvexFlowBlock.min[i,o,t]`
        .. math::
            flow(i, o, t) \geq min(i, o, t) \cdot nominal\_value \
                \cdot status(i, o, t), \\
            \forall t \in \textrm{TIMESTEPS}, \\
            \forall (i, o) \in \textrm{NONCONVEX\_FLOWS}.

    Maximum flow constraint `om.NonConvexFlowBlock.max[i,o,t]`
        .. math::
            flow(i, o, t) \leq max(i, o, t) \cdot nominal\_value \
                \cdot status(i, o, t), \\
            \forall t \in \textrm{TIMESTEPS}, \\
            \forall (i, o) \in \textrm{NONCONVEX\_FLOWS}.

    Startup constraint `om.NonConvexFlowBlock.startup_constr[i,o,t]`
        .. math::
            startup(i, o, t) \geq \
                status(i,o,t) - status(i, o, t-1) \\
            \forall t \in \textrm{TIMESTEPS}, \\
            \forall (i,o) \in \textrm{STARTUPFLOWS}.

    Maximum startups constraint
      `om.NonConvexFlowBlock.max_startup_constr[i,o,t]`
        .. math::
            \sum_{t \in \textrm{TIMESTEPS}} startup(i, o, t) \leq \
                N_{start}(i,o)
            \forall (i,o) \in \textrm{MAXSTARTUPFLOWS}.

    Shutdown constraint `om.NonConvexFlowBlock.shutdown_constr[i,o,t]`
        .. math::
            shutdown(i, o, t) \geq \
                status(i, o, t-1) - status(i, o, t) \\
            \forall t \in \textrm{TIMESTEPS}, \\
            \forall (i, o) \in \textrm{SHUTDOWNFLOWS}.

    Maximum shutdowns constraint
      `om.NonConvexFlowBlock.max_startup_constr[i,o,t]`
        .. math::
            \sum_{t \in \textrm{TIMESTEPS}} startup(i, o, t) \leq \
                N_{shutdown}(i,o)
            \forall (i,o) \in \textrm{MAXSHUTDOWNFLOWS}.

    Minimum uptime constraint `om.NonConvexFlowBlock.uptime_constr[i,o,t]`
        .. math::
            (status(i, o, t)-status(i, o, t-1)) \cdot minimum\_uptime(i, o) \\
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

    Minimum downtime constraint `om.NonConvexFlowBlock.downtime_constr[i,o,t]`
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
      `om.NonConvexFlowBlock.positive_gradient_constr[i, o]`:
        .. math:: flow(i, o, t) \cdot status(i, o, t)
            - flow(i, o, t-1) \cdot status(i, o, t-1)  \geq \
            positive\_gradient(i, o, t), \\
            \forall (i, o) \in \textrm{POSITIVE\_GRADIENT\_FLOWS}, \\
            \forall t \in \textrm{TIMESTEPS}.

    Negative gradient constraint
      `om.NonConvexFlowBlock.negative_gradient_constr[i, o]`:
        .. math::
            flow(i, o, t-1) \cdot status(i, o, t-1)
            - flow(i, o, t) \cdot status(i, o, t) \geq \
            negative\_gradient(i, o, t), \\
            \forall (i, o) \in \textrm{NEGATIVE\_GRADIENT\_FLOWS}, \\
            \forall t \in \textrm{TIMESTEPS}.


    **The following parts of the objective function are created:**

    If `nonconvex.startup_costs` is set by the user:
        .. math::
            \sum_{i, o \in STARTUPFLOWS} \sum_t  startup(i, o, t) \
            \cdot startup\_costs(i, o)

    If `nonconvex.shutdown_costs` is set by the user:
        .. math::
            \sum_{i, o \in SHUTDOWNFLOWS} \sum_t shutdown(i, o, t) \
            \cdot shutdown\_costs(i, o)

    If `nonconvex.activity_costs` is set by the user:
        .. math::
            \sum_{i, o \in ACTIVITYCOSTFLOWS} \sum_t status(i, o, t) \
            \cdot activity\_costs(i, o)

    If `nonconvex.inactivity_costs` is set by the user:
        .. math::
            \sum_{i, o \in INACTIVITYCOSTFLOWS} \sum_t (1 - status(i, o, t)) \
            \cdot inactivity\_costs(i, o)

    If `nonconvex.positive_gradient["costs"]` is set by the user:
        .. math::
            \sum_{i, o \in POSITIVE_GRADIENT_FLOWS} \sum_t
            positive_gradient(i, o, t) \cdot positive\_gradient\_costs(i, o)

    If `nonconvex.negative_gradient["costs"]` is set by the user:
        .. math::
            \sum_{i, o \in NEGATIVE_GRADIENT_FLOWS} \sum_t
            negative_gradient(i, o, t) \cdot negative\_gradient\_costs(i, o)

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
        self._create_variables(group)
        self._create_constraints()

    def _create_sets(self, group):
        """
        Creates all sets for non-convex flows.
        """
        self.NONCONVEX_FLOWS = Set(initialize=[(g[0], g[1]) for g in group])

        nc.add_sets_for_non_convex_flows_to_block(self, group)

        self.ACTIVITYCOSTFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.activity_costs[0] is not None
            ]
        )

        self.INACTIVITYCOSTFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].nonconvex.inactivity_costs[0] is not None
            ]
        )

    def _create_variables(self, group):
        """
        Creates all variables for non-convex flows.
        """
        m = self.parent_block()
        self.status = Var(self.NONCONVEX_FLOWS, m.TIMESTEPS, within=Binary)

        # `status_nominal` is a parameter which represents the
        # multiplication of a binary variable (`status`)
        # and a continuous variable (`invest` or `nominal_value`)
        self.status_nominal = Var(
            self.NONCONVEX_FLOWS, m.TIMESTEPS, within=NonNegativeReals
        )

        nc.add_variables_for_non_convex_flows_to_block(self)

    def _create_constraints(self):
        """
        Creates all constraints for non-convex flows.
        """
        m = self.parent_block()

        def _status_nominal_rule(_, i, o, t):
            """Rule definition for status_nominal"""
            expr = (
                self.status_nominal[i, o, t]
                == self.status[i, o, t] * m.flows[i, o].nominal_value
            )
            return expr

        self.status_nominal_constraint = Constraint(
            self.NONCONVEX_FLOWS, m.TIMESTEPS, rule=_status_nominal_rule
        )

        self.min = nc.minimum_flow_constraint(self)
        self.max = nc.maximum_flow_constraint(self)

        nc.add_constraints_to_non_convex_block(self)

    def _objective_expression(self):
        r"""Objective expression for nonconvex flows."""
        if not hasattr(self, "NONCONVEX_FLOWS"):
            return 0

        m = self.parent_block()

        startup_costs = nc.startup_costs(self)
        shutdown_costs = nc.shutdown_costs(self)
        activity_costs = 0
        inactivity_costs = 0
        gradient_costs = 0

        if self.ACTIVITYCOSTFLOWS:
            for i, o in self.ACTIVITYCOSTFLOWS:
                if m.flows[i, o].nonconvex.activity_costs[0] is not None:
                    activity_costs += sum(
                        self.status[i, o, t]
                        * m.flows[i, o].nonconvex.activity_costs[t]
                        for t in m.TIMESTEPS
                    )

            self.activity_costs = Expression(expr=activity_costs)

        if self.INACTIVITYCOSTFLOWS:
            for i, o in self.INACTIVITYCOSTFLOWS:
                if m.flows[i, o].nonconvex.inactivity_costs[0] is not None:
                    inactivity_costs += sum(
                        (1 - self.status[i, o, t])
                        * m.flows[i, o].nonconvex.inactivity_costs[t]
                        for t in m.TIMESTEPS
                    )

            self.inactivity_costs = Expression(expr=inactivity_costs)

        return (
            startup_costs
            + shutdown_costs
            + activity_costs
            + inactivity_costs
            + gradient_costs
        )
