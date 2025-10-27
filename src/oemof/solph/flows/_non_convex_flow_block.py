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
from pyomo.core import Constraint
from pyomo.core import Expression
from pyomo.core import NonNegativeReals
from pyomo.core import Set
from pyomo.core import Var
from pyomo.core.base.block import ScalarBlock

from ._shared import _activity_costs
from ._shared import _inactivity_costs
from ._shared import _maximum_flow_constraint
from ._shared import _minimum_flow_constraint
from ._shared import _sets_for_non_convex_flows
from ._shared import _shared_constraints_for_non_convex_flows
from ._shared import _shutdown_costs
from ._shared import _startup_costs
from ._shared import _variables_for_non_convex_flows


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
            :class:`.options.NonConvex`.


        .. automethod:: _sets_for_non_convex_flows
        """
        self.FIXED_CAPACITY_NONCONVEX_FLOWS = Set(
            initialize=[(g[0], g[1]) for g in group]
        )

        _sets_for_non_convex_flows(self, group)

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

        _variables_for_non_convex_flows(self)

    def _create_constraints(self):
        """
        The following constraints are created:

        .. automethod:: _status_nominal_constraint
        .. automethod:: _minimum_flow_constraint
        .. automethod:: _maximum_flow_constraint
        .. automethod:: _shared_constraints_for_non_convex_flows

        """

        self.status_nominal_constraint = self._status_nominal_constraint()
        self.min = _minimum_flow_constraint(self)
        self.max = _maximum_flow_constraint(self)

        _shared_constraints_for_non_convex_flows(self)

    def _objective_expression(self):
        r"""
        The following terms are to the cost function:

        .. automethod:: _startup_costs
        .. automethod:: _shutdown_costs
        .. automethod:: _activity_costs
        .. automethod:: _inactivity_costs
        """
        if not hasattr(self, "FIXED_CAPACITY_NONCONVEX_FLOWS"):
            return 0

        startup_costs = _startup_costs(self)
        shutdown_costs = _shutdown_costs(self)
        activity_costs = _activity_costs(self)
        inactivity_costs = _inactivity_costs(self)

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
