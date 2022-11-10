# -*- coding: utf-8 -*-

"""Creating sets, variables, constraints and parts of the objective function
for SimpleFlowBlock objects with investment option.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: jmloenneberga

SPDX-License-Identifier: MIT

"""

from pyomo.core import Binary
from pyomo.core import Constraint
from pyomo.core import Expression
from pyomo.core import NonNegativeReals
from pyomo.core import Set
from pyomo.core import Var
from pyomo.core.base.block import ScalarBlock


class InvestmentFlowBlock(ScalarBlock):
    r"""Block for all flows with :attr:`Investment` being not None.

    .. automethod:: _create_constraints
    .. automethod:: _create_variables
    .. automethod:: _create_sets

    .. automethod:: _objective_expression

    See :class:`oemof.solph.options.Investment` for all parameters of the
    *Investment* class.

    See :class:`oemof.solph.network.SimpleFlowBlock` for all parameters of the *SimpleFlowBlock*
    class.

    The total value of all costs of all *InvestmentFlowBlock* can be retrieved
    calling :meth:`om.InvestmentFlowBlock.investment_costs.expr()`.

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
            initialize=[
                (g[0], g[1])
                for g in group
                if (g[2].min[0] != 0 or len(g[2].min) > 1)
            ]
        )

    def _create_variables(self, group):
        r""" Creates all variables for investment flows.

        All *InvestmentFlowBlock* are indexed by a starting and ending node
        :math:`(i, o)`, which is omitted in the following for the sake
        of convenience. The following variables are created:

        * :math:`P(t)`

            Actual flow value (created in :class:`oemof.solph.models.BaseModel`).

        * :math:`P_{invest}`

            Value of the investment variable, i.e. equivalent to the nominal
            value of the flows after optimization.

        * :math:`Y_{invest}`

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

        # create invest variable for a investment flow
        self.invest = Var(
            self.INVESTFLOWS,
            within=NonNegativeReals,
            bounds=_investvar_bound_rule,
        )

        # create status variable for a non-convex investment flow
        self.invest_status = Var(self.NON_CONVEX_INVESTFLOWS, within=Binary)

    def _create_constraints(self):
        r"""Creates all constraints for standard flows.

        Depending on the attributes of the *InvestmentFlowBlock* and *SimpleFlowBlock*, different
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
                P_{invest, min} \cdot Y_{invest} \le P_{invest}\\
                &
                P_{invest} \le P_{invest, max} \cdot Y_{invest}\\

        For all *InvestmentFlowBlock* (independent of the attribute :attr:`nonconvex`),
        the following additional constraints are created, if the appropriate
        attribute of the *SimpleFlowBlock* (see :class:`oemof.solph.network.SimpleFlowBlock`) is set:

            * :attr:`fix` is not None

                Actual value constraint for investments with fixed flow values

            .. math::
                P(t) = ( P_{invest} + P_{exist} ) \cdot f_{fix}(t)

            * :attr:`min != 0`

                Lower bound for the flow values

            .. math::
                P(t) \geq ( P_{invest} + P_{exist} ) \cdot f_{min}(t)

            * :attr:`full_load_time_max is not None`

                Upper bound for the sum of all flow values (e.g. maximum full load
                hours)

            .. math::
                \sum_t P(t) \cdot \tau(t) \leq ( P_{invest} + P_{exist} )
                \cdot t_{full\_load, min}

            * :attr:`full_load_time_min is not None`

                Lower bound for the sum of all flow values (e.g. minimum full load
                hours)

            .. math::
                \sum_t P(t) \cdot \tau(t) \geq ( P_{invest} + P_{exist} )
                \cdot t_{full\_load, min}
        """
        m = self.parent_block()

        self.minimum_rule = self._minimum_investment_constraint()
        self.maximum_rule = self._maximum_investment_constraint()

        def _investflow_fixed_rule(block, i, o, t):
            """Rule definition of constraint to fix flow variable
            of investment flow to (normed) actual value
            """
            expr = m.flow[i, o, t] == (
                (m.flows[i, o].investment.existing + self.invest[i, o])
                * m.flows[i, o].fix[t]
            )

            return expr

        self.fixed = Constraint(
            self.FIXED_INVESTFLOWS, m.TIMESTEPS, rule=_investflow_fixed_rule
        )

        def _max_investflow_rule(block, i, o, t):
            """Rule definition of constraint setting an upper bound of flow
            variable in investment case.
            """
            expr = m.flow[i, o, t] <= (
                (m.flows[i, o].investment.existing + self.invest[i, o])
                * m.flows[i, o].max[t]
            )
            return expr

        self.max = Constraint(
            self.NON_FIXED_INVESTFLOWS, m.TIMESTEPS, rule=_max_investflow_rule
        )

        def _min_investflow_rule(block, i, o, t):
            """Rule definition of constraint setting a lower bound on flow
            variable in investment case.
            """
            expr = m.flow[i, o, t] >= (
                (m.flows[i, o].investment.existing + self.invest[i, o])
                * m.flows[i, o].min[t]
            )
            return expr

        self.min = Constraint(
            self.MIN_INVESTFLOWS, m.TIMESTEPS, rule=_min_investflow_rule
        )

        def _full_load_time_max_investflow_rule(_, i, o):
            """Rule definition for build action of max. sum flow constraint
            in investment case.
            """
            expr = sum(
                m.flow[i, o, t] * m.timeincrement[t] for t in m.TIMESTEPS
            ) <= m.flows[i, o].full_load_time_max * (
                self.invest[i, o] + m.flows[i, o].investment.existing
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
                (m.flows[i, o].investment.existing + self.invest[i, o])
                * m.flows[i, o].full_load_time_min
            )
            return expr

        self.full_load_time_min = Constraint(
            self.FULL_LOAD_TIME_MIN_INVESTFLOWS,
            rule=_full_load_time_min_investflow_rule,
        )

    def _objective_expression(self):
        r"""Objective expression for flows with investment attribute of type
        class:`.Investment`. The returned costs are fixed, variable and
        investment costs.

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
            + c_{invest,fix} \cdot Y_{invest}\\
        """
        if not hasattr(self, "INVESTFLOWS"):
            return 0

        m = self.parent_block()
        investment_costs = 0

        for i, o in self.CONVEX_INVESTFLOWS:
            investment_costs += (
                self.invest[i, o] * m.flows[i, o].investment.ep_costs
            )
        for i, o in self.NON_CONVEX_INVESTFLOWS:
            investment_costs += (
                self.invest[i, o] * m.flows[i, o].investment.ep_costs
                + self.invest_status[i, o] * m.flows[i, o].investment.offset
            )

        self.investment_costs = Expression(expr=investment_costs)
        return investment_costs

    def _minimum_investment_constraint(self):
        """Constraint factory for a minimum investment"""
        m = self.parent_block()

        def _min_invest_rule(_, i, o):
            """Rule definition for applying a minimum investment"""
            expr = (
                m.flows[i, o].investment.minimum * self.invest_status[i, o]
                <= self.invest[i, o]
            )
            return expr

        return Constraint(self.NON_CONVEX_INVESTFLOWS, rule=_min_invest_rule)

    def _maximum_investment_constraint(self):
        """Constraint factory for a maximum investment"""
        m = self.parent_block()

        def _max_invest_rule(_, i, o):
            """Rule definition for applying a minimum investment"""
            expr = self.invest[i, o] <= (
                m.flows[i, o].investment.maximum * self.invest_status[i, o]
            )
            return expr

        return Constraint(self.NON_CONVEX_INVESTFLOWS, rule=_max_invest_rule)
