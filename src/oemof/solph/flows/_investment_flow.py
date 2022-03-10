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

    See :class:`.Investment` for all parameters of the
    *Investment* class.

    See :class:`.FlowBlock` for all parameters of the *FlowBlock*
    class.

    **Variables**

    All *InvestmentFlowBlock*s are indexed by a starting and ending node
    :math:`(i, o)`, which is omitted in the following for the sake
    of convenience. The following variables are created:

    * :math:`P(p, t)`

        Actual flow value (created in :class:`.BaseModel`),
        indexed by tuple of periods p and timestep t

    * :math:`P_{invest}(p)`

        Value of the investment variable in period p,
        equal to what is being invested and equivalent / similar to
        the nominal value of the flows after optimization.

    * :math:`P_{total}(p)`

        Total installed capacity / energy in period p,
        equivalent to the nominal value of the flows after optimization.

    * :math:`P_{old}(p)`

        Old capacity / energy to be decommissioned in period p
        due to reaching its lifetime; applicable only for multi-period models.

    * :math:`P_{old,exo}(p)`

        Old exogenous capacity / energy to be decommissioned in period p
        due to reaching its lifetime, i.e. the amount that has been specified
        by :attr:`existing` when it is decommisioned;
        applicable only for multi-period models.

    * :math:`P_{old,end}(p)`

        Old endogenous capacity / energy to be decommissioned in period p
        due to reaching its lifetime, i.e. the amount that has been invested in
        by the model itself that is decommissioned in a later period because
        of reaching its lifetime;
        applicable only for multi-period models.

    * :math:`b_{invest}(p)`

        Binary variable for the status of the investment, if
        :attr:`nonconvex` is `True`.

    **Constraints**

    Depending on the attributes of the *InvestmentFlowBlock* and *FlowBlock*,
    different constraints are created. The following constraints are created
    for all *InvestmentFlowBlock*s:\

        Total capacity / energy

        .. math::
            &
            if \quad p=0:\\
            &
            P_{total}(p) = P_{invest}(p) + P_{exist}(p) \\
            &
            else:\\
            &
            P_{total}(p) = P_{total}(p-1) + P_{invest}(p) - P_{old}(p) \\
            &
            \forall p \in \textrm{PERIODS}

        Upper bound for the flow value

        .. math::
            P(p, t) \le ( P_{total}(p) ) \cdot f_{max}(t) \\
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
            &
            else \quad if \quad l \leq year(p):\\
            &
            P_{old,end}(p) = P_{invest}(p_{comm})\\
            &
            else:\\
            &
            P_{old,end}(p)\\
            &\\
            &
            if \quad p=0:\\
            &
            P_{old,exo}(p) = 0\\
            &
            else \quad if \quad l - a \leq year(p):\\
            &
            P_{old,exo}(p) = P_{exist} (*)\\
            &
            else:\\
            &
            P_{old,exo}(p) = 0\\
            &
            \forall p \in \textrm{PERIODS}

        whereby:

        * (*) is only performed for the first period the condition is True.
          A decommissioning flag is set to True.
        * :math:`year(p)` is the year corresponding to period p
        * :math:`p_{comm}` is the commissioning period of the flow

    Depending on the attribute :attr:`nonconvex`, the constraints for the
    bounds of the decision variable :math:`P_{invest}(p)` are different:\

        * :attr:`nonconvex = False`

        .. math::
            P_{invest, min}(p) \le P_{invest}(p) \le P_{invest, max}(p) \\
            \forall p \in \textrm{PERIODS}

        * :attr:`nonconvex = True`

        .. math::
            &
            P_{invest, min}(P) \cdot b_{invest}(P) \le P_{invest}(p)\\
            &
            P_{invest}(p) \le P_{invest, max}(p) \cdot b_{invest}(p)\\
            &
            \forall p \in \textrm{PERIODS}

    For all *InvestmentFlowBlock* (independent of the attribute :attr:`nonconvex`),
    the following additional constraints are created, if the appropriate
    attribute of the *FlowBlock* (see :class:`oemof.solph.network.FlowBlock`) is set:

        * :attr:`fix` is not None

            Actual value constraint for investments with fixed flow values

        .. math::
            P(p, t) = P_{total}(p) \cdot f_{fix}(t) \\
            \forall p, t \in \textrm{TIMEINDEX}

        * :attr:`min != 0`

            Lower bound for the flow values

        .. math::
            P(p, t) \geq P_{total}(p) \cdot f_{min}(t) \\
            \forall p, t \in \textrm{TIMEINDEX}

        * :attr:`summed_max` is not None

            Upper bound for the sum of all flow values (e.g. maximum full load
            hours)

        .. math::
            \sum_{p, t} P(p, t) \cdot \tau(t) \leq P_{total}(p)
            \cdot f_{sum, min}

        * :attr:`summed_min` is not None

            Lower bound for the sum of all flow values (e.g. minimum full load
            hours)

        .. math::
            \sum_{p, t} P(t) \cdot \tau(t) \geq P_{total}
            \cdot f_{sum, min}

        * :attr:`overall_maximum` is not None (for multi-period model only)

            Overall maximum of total installed capacity / energy for flow

        .. math::
            P_{total}(p) \leq P_{overall,max} \\
            \forall p \in \textrm{PERIODS}

        * :attr:`overall_minimum` is not None (for multi-period model only)

            Overall minimum of total installed capacity / energy for flow

        .. math::
            P_{total}(p_{last}) \geq P_{overall,min}


    **Objective function**

    Objective terms for a standard model and a multi-period model differ
    quite strongly. Besides, the part of the objective function added by the
    *InvestmentFlowBlock* also depends on whether a convex or nonconvex
    *InvestmentFlowBlock* is selected. The following parts of the objective
    function are created:

    *Standard model*

        * :attr:`nonconvex = False`

            .. math::
                P_{invest}(0) \cdot c_{invest,var}(0)

        * :attr:`nonconvex = True`

            .. math::
                P_{invest}(0) \cdot c_{invest,var}(0)
                + c_{invest,fix}(0) \cdot b_{invest}(0) \\


    *Multi-period model*

        * :attr:`nonconvex = False`

            .. math::
                &
                P_{invest}(p) \cdot A(c_{invest,var}(p), l, ir) \cdot l
                \cdot DF^{-p}\\
                &
                \forall p \in \textrm{PERIODS}

        * :attr:`nonconvex = True`

            .. math::
                &
                P_{invest}(p) \cdot A(c_{invest,var}(p), l, ir) \cdot l
                \cdot DF^{-p} +  c_{invest,fix}(p) \cdot b_{invest}(p)\\
                &
                \forall p \in \textrm{PERIODS}

        * :attr:`fixed_costs` not None for investments

            .. math::
                &
                \sum_{pp=year(p)}^{year(p)+l}
                P_{invest}(p) \cdot c_{fixed}(pp) \cdot DF^{-pp})
                \cdot DF^{-p}\\
                &
                \forall p \in \textrm{PERIODS}

        * :attr:`fixed_costs` not None for existing capacity

            .. math::
                \sum_{pp=0}^{l-a} P_{exist} \cdot c_{fixed}(pp)
                \cdot DF^{-pp}


        whereby:

        * :math:`A(c_{invest,var}(p), l, ir)` A is the annuity for
          investment expenses :math:`c_{invest,var}(p)` lifetime :math:`l` and
          interest rate :math:`ir`
        * :math:`DF=(1+dr)` is the discount factor with discount rate math:`dr`

    The total value of all costs of all *InvestmentFlowBlock* can be retrieved
    calling :meth:`om.InvestmentFlowBlock.investment_costs.expr()`.

    .. csv-table:: List of Variables (in csv table syntax)
        :header: "symbol", "attribute", "explanation"
        :widths: 1, 1, 1

        ":math:`P(p, t)`", ":py:obj:`flow[n, o, p, t]`", "Actual flow value"
        ":math:`P_{invest}(p)`", ":py:obj:`invest[i, o, p]`", "Invested flow
        capacity"
        ":math:`P_{total}(p, t)`", ":py:obj:`total[n, o, p]`", "Total flow capacity / energy"
        ":math:`P_{old}(p, t)`", ":py:obj:`old[n, o, p]`", "Old flow capacity / energy"
        ":math:`P_{old,exo}(p, t)`", ":py:obj:`old_exo[n, o, p]`", "Old exogenous flow capacity / energy"
        ":math:`P_{old,end}(p, t)`", ":py:obj:`old_end[n, o, p]`", "Old endogenous flow capacity / energy"
        ":math:`b_{invest}(p)`", ":py:obj:`invest_status[i, o, p]`", "Binary status
        of investment"

    List of Variables (in rst table syntax):

    =========================  =================================  =========
    symbol                     attribute                          explanation
    =========================  =================================  =========
    :math:`P(p, t)`            :py:obj:`flow[n, o, p, t]`         Actual flow value

    :math:`P_{invest}(p)`      :py:obj:`invest[i, o, p]`          Invested flow capacity

    :math:`P_{total}(p, t)`    :py:obj:`total[n, o, p]`           Total flow capacity / energy

    :math:`P_{old}(p, t)`      :py:obj:`old[n, o, p]`             Old flow capacity / energy

    :math:`P_{old,exo}(p, t)`  :py:obj:`old_exo[n, o, p]`         Old exogenous flow capacity / energy

    :math:`P_{old,end}(p, t)`  :py:obj:`old_end[n, o, p]`         Old endogenous flow capacity / energy

    :math:`b_{invest}(p)`      :py:obj:`invest_status[i, o, p]`   Binary status of investment

    =========================  =================================  =========

    Grid table style:

    +------------------------+----------------------------------+--------------------------------------------+
    | symbol                 | attribute                        | explanation                                |
    +========================+==================================+============================================+
    | :math:`P(p, t)`        | :py:obj:`flow[n, o, p, t]`       | Actual flow value                          |
    +------------------------+----------------------------------+--------------------------------------------+
    | :math:`P_{invest}(p)`  | :py:obj:`invest[i, o, p]`        | Invested flow capacity                     |
    +------------------------+----------------------------------+--------------------------------------------+
    | :math:`P_{total}(p)`  | :py:obj:`total[i, o, p]`          | Total flow capacity / energy               |
    +------------------------+----------------------------------+--------------------------------------------+
    | :math:`P_{old}(p)`     | :py:obj:`old[n, o, p]`           | Old flow capacity / energy                 |
    +------------------------+----------------------------------+--------------------------------------------+
    | :math:`P_{old,exo}(p)` | :py:obj:`old_exo[n, o, p]`       | Old exogenous flow capacity / energy       |
    +------------------------+----------------------------------+--------------------------------------------+
    | :math:`P_{old,end}(p)` | :py:obj:`old_end[n, o, p]`       | Old endogenous flow capacity / energy      |
    +------------------------+----------------------------------+--------------------------------------------+
    | :math:`b_{invest}(p)`  | :py:obj:`invest_status[n, o, p]` | Binary status of investment                |
    +------------------------+----------------------------------+--------------------------------------------+

    .. csv-table:: List of Parameters
        :header: "symbol", "attribute", "explanation"
        :widths: 1, 1, 1

        ":math:`P_{exist}`", ":py:obj:`flows[i, o].investment.existing`", "
        Existing flow capacity"
        ":math:`P_{invest,min}(p)`", ":py:obj:`flows[i, o].investment.minimum[p]`", "
        Minimum investment capacity"
        ":math:`P_{invest,max}(p)`", ":py:obj:`flows[i, o].investment.maximum[p]`", "
        Maximum investment capacity"
        ":math:`c_{invest,var}(p)`", ":py:obj:`flows[i, o].investment.ep_costs[p]`
        ", "Variable investment costs"
        ":math:`c_{invest,fix}(p)`", ":py:obj:`flows[i, o].investment.offset[p]`", "
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
    See also :class:`.FlowBlock`,
    :class:`.FlowBlock` and
    :class:`.Investment`

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

        self.EXISTING_INVESTFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].investment.existing is not None
            ]
        )

        self.OVERALL_MAXIMUM_INVESTFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].investment.overall_maximum is not None
            ]
        )

        self.OVERALL_MINIMUM_INVESTFLOWS = Set(
            initialize=[
                (g[0], g[1])
                for g in group
                if g[2].investment.overall_minimum is not None
            ]
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
        self.total = Var(self.INVESTFLOWS, m.PERIODS, within=NonNegativeReals)

        if m.es.multi_period:
            self.old = Var(
                self.INVESTFLOWS, m.PERIODS, within=NonNegativeReals
            )

            # Old endogenous capacity to be decommissioned (due to lifetime)
            self.old_end = Var(
                self.INVESTFLOWS, m.PERIODS, within=NonNegativeReals
            )

            # Old exogenous capacity to be decommissioned (due to lifetime)
            self.old_exo = Var(
                self.INVESTFLOWS, m.PERIODS, within=NonNegativeReals
            )

        # create status variable for a non-convex investment flow
        self.invest_status = Var(
            self.NON_CONVEX_INVESTFLOWS, m.PERIODS, within=Binary
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
            self.NON_CONVEX_INVESTFLOWS, m.PERIODS, noruleinit=True
        )
        self.minimum_rule_build = BuildAction(rule=_min_invest_rule)

        def _max_invest_rule(block):
            """Rule definition for applying a minimum investment"""
            for i, o in self.NON_CONVEX_INVESTFLOWS:
                for p in m.PERIODS:
                    expr = self.invest[i, o, p] <= (
                        m.flows[i, o].investment.maximum[p]
                        * self.invest_status[i, o, p]
                    )
                    self.maximum_rule.add((i, o, p), expr)

        self.maximum_rule = Constraint(
            self.NON_CONVEX_INVESTFLOWS, m.PERIODS, noruleinit=True
        )
        self.maximum_rule_build = BuildAction(rule=_max_invest_rule)

        # Handle unit lifetimes
        def _total_capacity_rule(block):
            """Rule definition for determining total installed
            capacity (taking decommissioning into account)
            """
            for i, o in self.INVESTFLOWS:
                for p in m.PERIODS:
                    if p == 0:
                        expr = (
                            self.total[i, o, p]
                            == self.invest[i, o, p]
                            + m.flows[i, o].investment.existing
                        )
                        self.total_rule.add((i, o, p), expr)
                    # applicable for multi-period model only
                    else:
                        expr = (
                            self.total[i, o, p]
                            == self.invest[i, o, p]
                            + self.total[i, o, p - 1]
                            - self.old[i, o, p]
                        )
                        self.total_rule.add((i, o, p), expr)

        self.total_rule = Constraint(
            self.INVESTFLOWS, m.PERIODS, noruleinit=True
        )
        self.total_rule_build = BuildAction(rule=_total_capacity_rule)

        if m.es.multi_period:

            def _old_capacity_rule_end(block):
                """Rule definition for determining old endogenously installed
                capacity to be decommissioned due to reaching its lifetime
                """
                for i, o in self.INVESTFLOWS:
                    lifetime = m.flows[i, o].investment.lifetime
                    if lifetime is None:
                        msg = (
                            "You have to specify a lifetime "
                            "for an InvestmentFlow in "
                            "a multi-period model! Value for {} "
                            "is missing.".format((i, o))
                        )
                        raise ValueError(msg)
                    for p in m.PERIODS:
                        # No shutdown in first period
                        if p == 0:
                            expr = self.old_end[i, o, p] == 0
                            self.old_rule_end.add((i, o, p), expr)
                        elif lifetime <= m.es.periods_years[p]:
                            # Obtain commissioning period
                            comm_p = 0
                            for k, v in m.es.periods_years.items():
                                if m.es.periods_years[p] - lifetime - v < 0:
                                    # change of sign is detected
                                    comm_p = k - 1
                                    break
                            expr = (
                                self.old_end[i, o, p]
                                == self.invest[i, o, comm_p]
                            )
                            self.old_rule_end.add((i, o, p), expr)
                        else:
                            expr = self.old_end[i, o, p] == 0
                            self.old_rule_end.add((i, o, p), expr)

            self.old_rule_end = Constraint(
                self.INVESTFLOWS, m.PERIODS, noruleinit=True
            )
            self.old_rule_end_build = BuildAction(rule=_old_capacity_rule_end)

            def _old_capacity_rule_exo(block):
                """Rule definition for determining old exogenously given
                capacity to be decommissioned due to reaching its lifetime
                """
                for i, o in self.INVESTFLOWS:
                    age = m.flows[i, o].investment.age
                    lifetime = m.flows[i, o].investment.lifetime
                    is_decommissioned = False
                    for p in m.PERIODS:
                        # No shutdown in first period
                        if p == 0:
                            expr = self.old_exo[i, o, p] == 0
                            self.old_rule_exo.add((i, o, p), expr)
                        elif lifetime - age <= m.es.periods_years[p]:
                            # Track decommissioning status
                            if not is_decommissioned:
                                expr = (
                                    self.old_exo[i, o, p]
                                    == m.flows[i, o].investment.existing
                                )
                                is_decommissioned = True
                            else:
                                expr = self.old_exo[i, o, p] == 0
                            self.old_rule_exo.add((i, o, p), expr)
                        else:
                            expr = self.old_exo[i, o, p] == 0
                            self.old_rule_exo.add((i, o, p), expr)

            self.old_rule_exo = Constraint(
                self.INVESTFLOWS, m.PERIODS, noruleinit=True
            )
            self.old_rule_exo_build = BuildAction(rule=_old_capacity_rule_exo)

            def _old_capacity_rule(block):
                """Rule definition for determining (overall) old capacity
                to be decommissioned due to reaching its lifetime
                """
                for i, o in self.INVESTFLOWS:
                    for p in m.PERIODS:
                        expr = (
                            self.old[i, o, p]
                            == self.old_end[i, o, p] + self.old_exo[i, o, p]
                        )
                        self.old_rule.add((i, o, p), expr)

            self.old_rule = Constraint(
                self.INVESTFLOWS, m.PERIODS, noruleinit=True
            )
            self.old_rule_build = BuildAction(rule=_old_capacity_rule)

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
            self.FIXED_INVESTFLOWS, m.TIMEINDEX, noruleinit=True
        )
        self.fixed_build = BuildAction(rule=_investflow_fixed_rule)

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
            self.NON_FIXED_INVESTFLOWS, m.TIMEINDEX, noruleinit=True
        )
        self.max_build = BuildAction(rule=_max_investflow_rule)

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
            self.MIN_INVESTFLOWS, m.TIMEINDEX, noruleinit=True
        )
        self.min_build = BuildAction(rule=_min_investflow_rule)

        def _summed_max_investflow_rule(block, i, o):
            """Rule definition for build action of max. sum flow constraint
            in investment case.
            """
            expr = sum(
                m.flow[i, o, p, t] * m.timeincrement[t] for p, t in m.TIMEINDEX
            ) <= (
                m.flows[i, o].summed_max
                * sum(self.total[i, o, p] for p in m.PERIODS)
            )
            return expr

        self.summed_max = Constraint(
            self.SUMMED_MAX_INVESTFLOWS, rule=_summed_max_investflow_rule
        )

        def _summed_min_investflow_rule(block, i, o):
            """Rule definition for build action of min. sum flow constraint
            in investment case.
            """
            expr = sum(
                m.flow[i, o, p, t] * m.timeincrement[t] for p, t in m.TIMEINDEX
            ) >= (
                sum(self.total[i, o, p] for p in m.PERIODS)
                * m.flows[i, o].summed_min
            )
            return expr

        self.summed_min = Constraint(
            self.SUMMED_MIN_INVESTFLOWS, rule=_summed_min_investflow_rule
        )

        if m.es.multi_period:

            def _overall_maximum_investflow_rule(block):
                """Rule definition for maximum overall investment
                in investment case.
                """
                for i, o in self.OVERALL_MAXIMUM_INVESTFLOWS:
                    for p in m.PERIODS:
                        expr = (
                            self.total[i, o, p]
                            <= m.flows[i, o].investment.overall_maximum
                        )
                        self.overall_maximum.add((i, o, p), expr)

            self.overall_maximum = Constraint(
                self.OVERALL_MAXIMUM_INVESTFLOWS, m.PERIODS, noruleinit=True
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
                rule=_overall_minimum_investflow_rule,
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
            msg = (
                "You did not specify an interest rate.\n"
                "It will be set equal to the discount_rate of {} "
                "of the model as a default.\nThis corresponds to a "
                "social planner point of view and does not reflect "
                "microeconomic interest requirements."
            )

            for i, o in self.CONVEX_INVESTFLOWS:
                lifetime = m.flows[i, o].investment.lifetime
                interest = m.flows[i, o].investment.interest_rate
                if interest == 0:
                    warn(
                        msg.format(m.discount_rate),
                        debugging.SuspiciousUsageWarning,
                    )
                    interest = m.discount_rate
                for p in m.PERIODS:
                    annuity = economics.annuity(
                        capex=m.flows[i, o].investment.ep_costs[p],
                        n=lifetime,
                        wacc=interest,
                    )
                    investment_costs_increment = (
                        self.invest[i, o, p]
                        * annuity
                        * lifetime
                        * ((1 + m.discount_rate) ** (-m.es.periods_years[p]))
                    )
                    investment_costs += investment_costs_increment
                    period_investment_costs[p] += investment_costs_increment

            for i, o in self.NON_CONVEX_INVESTFLOWS:
                lifetime = m.flows[i, o].investment.lifetime
                interest = m.flows[i, o].investment.interest_rate
                if interest == 0:
                    warn(
                        msg.format(m.discount_rate),
                        debugging.SuspiciousUsageWarning,
                    )
                    interest = m.discount_rate
                for p in m.PERIODS:
                    annuity = economics.annuity(
                        capex=m.flows[i, o].investment.ep_costs[p],
                        n=lifetime,
                        wacc=interest,
                    )
                    investment_costs_increment = (
                        self.invest[i, o, p] * annuity * lifetime
                        + self.invest_status[i, o, p]
                        * m.flows[i, o].investment.offset[p]
                    ) * ((1 + m.discount_rate) ** (-m.es.periods_years[p]))
                    investment_costs += investment_costs_increment
                    period_investment_costs[p] += investment_costs_increment

            for i, o in self.INVESTFLOWS:
                if m.flows[i, o].investment.fixed_costs[0] is not None:
                    lifetime = m.flows[i, o].investment.lifetime
                    for p in m.PERIODS:
                        fixed_costs += (
                            sum(
                                self.invest[i, o, p]
                                * m.flows[i, o].investment.fixed_costs[pp]
                                * ((1 + m.discount_rate) ** (-pp))
                                for pp in range(
                                    m.es.periods_years[p],
                                    m.es.periods_years[p] + lifetime,
                                )
                            )
                            * (
                                (1 + m.discount_rate)
                                ** (-m.es.periods_years[p])
                            )
                        )

            for i, o in self.EXISTING_INVESTFLOWS:
                if m.flows[i, o].investment.fixed_costs[0] is not None:
                    lifetime = m.flows[i, o].investment.lifetime
                    age = m.flows[i, o].investment.age
                    fixed_costs += sum(
                        m.flows[i, o].investment.existing
                        * m.flows[i, o].investment.fixed_costs[pp]
                        * ((1 + m.discount_rate) ** (-pp))
                        for pp in range(0, lifetime - age)
                    )

        self.investment_costs = Expression(expr=investment_costs)
        self.period_investment_costs = period_investment_costs
        self.fixed_costs = Expression(expr=fixed_costs)
        self.costs = Expression(expr=investment_costs + fixed_costs)

        return self.costs
