# -*- coding: utf-8 -*-

"""This module is designed to hold custom components with their classes and
associated individual constraints (blocks) and groupings.

Therefore this module holds the class definition and the block directly located
by each other.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Johannes Röder
SPDX-FileCopyrightText: jakob-wo
SPDX-FileCopyrightText: gplssm
SPDX-FileCopyrightText: jnnr

SPDX-License-Identifier: MIT

"""

from pyomo.core.base.block import SimpleBlock
from pyomo.environ import BuildAction
from pyomo.environ import Constraint
from pyomo.environ import Expression
from pyomo.environ import NonNegativeReals
from pyomo.environ import Set
from pyomo.environ import Var

from oemof.solph.network import Sink
from oemof.solph.plumbing import sequence


class SinkDSM(Sink):
    r"""
    Demand Side Management implemented as Sink with flexibility potential.

    Based on the paper by Zerrahn, Alexander and Schill, Wolf-Peter (2015):
    `On the representation of demand-side management in power system models
    <https://www.sciencedirect.com/science/article/abs/pii/S036054421500331X>`_,
    in: Energy (84), pp. 840-845, 10.1016/j.energy.2015.03.037,
    accessed 17.09.2019, pp. 842-843.

    SinkDSM adds additional constraints that allow to shift energy in certain
    time window constrained by :attr:`~capacity_up` and
    :attr:`~capacity_down`.

    Parameters
    ----------
    demand: numeric
        original electrical demand
    capacity_up: int or array
        maximum DSM capacity that may be increased
    capacity_down: int or array
        maximum DSM capacity that may be reduced
    method: 'interval' , 'delay'
        Choose one of the DSM modelling approaches. Read notes about which
        parameters to be applied for which approach.

        interval :

            Simple model in which the load shift must be compensated in a
            predefined fixed interval (:attr:`~shift_interval` is mandatory).
            Within time windows of the length :attr:`~shift_interval` DSM
            up and down shifts are balanced. See
            :class:`~SinkDSMIntervalBlock` for details.

        delay :

            Sophisticated model based on the formulation by
            Zerrahn & Schill (2015). The load-shift of the component must be
            compensated in a predefined delay-time (:attr:`~delay_time` is
            mandatory).
            For details see :class:`~SinkDSMDelayBlock`.
    shift_interval: int
        Only used when :attr:`~method` is set to 'interval'. Otherwise, can be
        None.
        It's the interval in which between :math:`DSM_{t}^{up}` and
        :math:`DSM_{t}^{down}` have to be compensated.
    delay_time: int
        Only used when :attr:`~method` is set to 'delay'. Otherwise, can be
        None.
        Length of symmetrical time windows around :math:`t` in which
        :math:`DSM_{t}^{up}` and :math:`DSM_{t,tt}^{down}` have to be
        compensated.
    cost_dsm_up : :obj:`int`
        Cost per unit of DSM activity that increases the demand
    cost_dsm_down : :obj:`int`
        Cost per unit of DSM activity that decreases the demand

    Note
    ----

    * This component is a candidate component. It's implemented as a custom
      component for users that like to use and test the component at early
      stage. Please report issues to improve the component.
    * As many constraints and dependencies are created in method 'delay',
      computational cost might be high with a large 'delay_time' and with model
      of high temporal resolution
    * Using :attr:`~method` 'delay' might result in demand shifts that exceed
      the specified delay time by activating up and down simultaneously in
      the time steps between to DSM events.
    * It's not recommended to assign cost to the flow that connects
      :class:`~SinkDSM` with a bus. Instead, use :attr:`~SinkDSM.cost_dsm_up`
      or :attr:`~cost_dsm_down`

    """

    def __init__(
        self,
        demand,
        capacity_up,
        capacity_down,
        method,
        shift_interval=None,
        delay_time=None,
        cost_dsm_up=0,
        cost_dsm_down=0,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.capacity_up = sequence(capacity_up)
        self.capacity_down = sequence(capacity_down)
        self.demand = sequence(demand)
        self.method = method
        self.shift_interval = shift_interval
        self.delay_time = delay_time
        self.cost_dsm_up = cost_dsm_up
        self.cost_dsm_down = cost_dsm_down

    def constraint_group(self):
        possible_methods = ["delay", "interval"]

        if self.method == possible_methods[0]:
            if self.delay_time is None:
                raise ValueError(
                    "Please define: **delay_time" "is a mandatory parameter"
                )
            return SinkDSMDelayBlock
        elif self.method == possible_methods[1]:
            if self.shift_interval is None:
                raise ValueError(
                    "Please define: **shift_interval"
                    " is a mandatory parameter"
                )
            return SinkDSMIntervalBlock
        else:
            raise ValueError(
                'The "method" must be one of the following set: '
                '"{}"'.format('" or "'.join(possible_methods))
            )


class SinkDSMIntervalBlock(SimpleBlock):
    r"""Constraints for SinkDSM with "interval" method

    **The following constraints are created for method = 'interval':**

    .. _SinkDSMInterval-equations:

    .. math::
        &
        (1) \quad \dot{E}_{t} = demand_{t} + DSM_{t}^{up} - DSM_{t}^{do}
        \quad \forall t \in \mathbb{T}\\
        &
        (2) \quad  DSM_{t}^{up} \leq E_{t}^{up} \quad \forall t \in
        \mathbb{T}\\
        &
        (3) \quad DSM_{t}^{do} \leq  E_{t}^{do} \quad \forall t \in
        \mathbb{T}\\
        &
        (4) \quad  \sum_{t=t_s}^{t_s+\tau} DSM_{t}^{up} =
        \sum_{t=t_s}^{t_s+\tau} DSM_{t}^{do} \quad \forall t_s \in \{k
        \in \mathbb{T} \mid k \mod \tau = 0\} \\
        &


    **Table: Symbols and attribute names of variables and parameters**

        .. csv-table:: Variables (V) and Parameters (P)
            :header: "symbol", "attribute", "type", "explanation"
            :widths: 1, 1, 1, 1

            ":math:`DSM_{t}^{up}` ",":attr:`~SinkDSM.capacity_up` ","V", "DSM
            up shift"
            ":math:`DSM_{t}^{do}` ",":attr:`~SinkDSM.capacity_down` ","V","DSM
            down shift"
            ":math:`\dot{E}_{t}`",":attr:`~SinkDSM.inputs`","V", "Energy
            flowing in from electrical bus"
            ":math:`demand_{t}`",":attr:`demand[t]`","P", "Electrical demand
            series"
            ":math:`E_{t}^{do}`",":attr:`capacity_down[tt]`","P", "Capacity
            DSM down shift capacity"
            ":math:`E_{t}^{up}`",":attr:`capacity_up[tt]`","P", "Capacity
            DSM up shift "
            ":math:`\tau` ",":attr:`~SinkDSM.shift_interval` ","P", "Shift
            interval"
            ":math:`\mathbb{T}` "," ","P", "Time steps"

    """
    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        if group is None:
            return None

        m = self.parent_block()

        # for all DSM components get inflow from bus_elec
        for n in group:
            n.inflow = list(n.inputs)[0]

        #  ************* SETS *********************************

        # Set of DSM Components
        self.dsm = Set(initialize=[n for n in group])

        #  ************* VARIABLES *****************************

        # Variable load shift down
        self.dsm_do = Var(
            self.dsm, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        # Variable load shift up
        self.dsm_up = Var(
            self.dsm, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        #  ************* CONSTRAINTS *****************************

        # Demand Production Relation
        def _input_output_relation_rule(block):
            """
            Relation between input data and pyomo variables.
            The actual demand after DSM.
            Generator Production == Demand_el +- DSM
            """
            for t in m.TIMESTEPS:
                for g in group:
                    # Generator loads directly from bus
                    lhs = m.flow[g.inflow, g, t]

                    # Demand + DSM_up - DSM_down
                    rhs = g.demand[t] + self.dsm_up[g, t] - self.dsm_do[g, t]

                    # add constraint
                    block.input_output_relation.add((g, t), (lhs == rhs))

        self.input_output_relation = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.input_output_relation_build = BuildAction(
            rule=_input_output_relation_rule
        )

        # Upper bounds relation
        def dsm_up_constraint_rule(block):
            """
            Realised upward load shift at time t has to be smaller than
            upward DSM capacity at time t.
            """

            for t in m.TIMESTEPS:
                for g in group:
                    # DSM up
                    lhs = self.dsm_up[g, t]
                    # Capacity dsm_up
                    rhs = g.capacity_up[t]

                    # add constraint
                    block.dsm_up_constraint.add((g, t), (lhs <= rhs))

        self.dsm_up_constraint = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.dsm_up_constraint_build = BuildAction(rule=dsm_up_constraint_rule)

        # Upper bounds relation
        def dsm_down_constraint_rule(block):
            """
            Realised downward load shift at time t has to be smaller than
            downward DSM capacity at time t.
            """

            for t in m.TIMESTEPS:
                for g in group:
                    # DSM down
                    lhs = self.dsm_do[g, t]
                    # Capacity dsm_down
                    rhs = g.capacity_down[t]

                    # add constraint
                    block.dsm_down_constraint.add((g, t), (lhs <= rhs))

        self.dsm_down_constraint = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.dsm_down_constraint_build = BuildAction(
            rule=dsm_down_constraint_rule
        )

        def dsm_sum_constraint_rule(block):
            """
            Relation to compensate the total amount of positive
            and negative DSM in between the shift_interval.
            This constraint is building balance in full intervals starting
            with index 0. The last interval might not be full.
            """

            for g in group:
                intervals = range(
                    m.TIMESTEPS.value_list[0],
                    m.TIMESTEPS.value_list[-1],
                    g.shift_interval,
                )

                for interval in intervals:
                    if (
                        interval + g.shift_interval - 1
                    ) > m.TIMESTEPS.value_list[-1]:
                        timesteps = range(
                            interval, m.TIMESTEPS.value_list[-1] + 1
                        )
                    else:
                        timesteps = range(
                            interval, interval + g.shift_interval
                        )

                    # DSM up/down
                    lhs = sum(self.dsm_up[g, tt] for tt in timesteps)
                    # value
                    rhs = sum(self.dsm_do[g, tt] for tt in timesteps)

                    # add constraint
                    block.dsm_sum_constraint.add((g, interval), (lhs == rhs))

        self.dsm_sum_constraint = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.dsm_sum_constraint_build = BuildAction(
            rule=dsm_sum_constraint_rule
        )

    def _objective_expression(self):
        """Adding cost terms for DSM activity to obj. function"""

        m = self.parent_block()

        dsm_cost = 0

        for t in m.TIMESTEPS:
            for g in self.dsm:
                dsm_cost += self.dsm_up[g, t] * g.cost_dsm_up
                dsm_cost += self.dsm_do[g, t] * g.cost_dsm_down

        self.cost = Expression(expr=dsm_cost)

        return self.cost


class SinkDSMDelayBlock(SimpleBlock):
    r"""Constraints for SinkDSM with "delay" method

    **The following constraints are created for method = 'delay':**

    .. _SinkDSMDelay-equations:

    .. math::


        &
        (1) \quad \dot{E}_{t} = demand_{t} + DSM_{t}^{up} -
        \sum_{tt=t-L}^{t+L} DSM_{t,tt}^{do}  \quad \forall t \in \mathbb{T} \\
        &
        (2) \quad DSM_{t}^{up} = \sum_{tt=t-L}^{t+L} DSM_{t,tt}^{do}
        \quad \forall t \in \mathbb{T} \\
        &
        (3) \quad DSM_{t}^{up} \leq  E_{t}^{up} \quad \forall t \in
        \mathbb{T} \\
        &
        (4) \quad \sum_{tt=t-L}^{t+L} DSM_{t,tt}^{do}  \leq E_{t}^{do}
        \quad \forall t \in \mathbb{T} \\
        &
        (5) \quad DSM_{t}^{up}  + \sum_{tt=t-L}^{t+L} DSM_{t,tt}^{do}
        \leq max \{ E_{t}^{up}, E_{t}^{do} \}\quad \forall t \in \mathbb{T} \\
        &



   **Table: Symbols and attribute names of variables and parameters**


        .. csv-table:: Variables (V) and Parameters (P)
            :header: "symbol", "attribute", "type", "explanation"
            :widths: 1, 1, 1, 1



            ":math:`DSM_{t}^{up}` ",":attr:`dsm_do[g,t,tt]`", "V","DSM up
            shift (additional load)"
            ":math:`DSM_{t,tt}^{do}` ",":attr:`dsm_up[g,t]`","V","DSM down
            shift (less load)"
            ":math:`\dot{E}_{t}` ",":attr:`flow[g,t]`","V","Energy
            flowing in from electrical bus"
            ":math:`L`",":attr:`delay_time`","P", "Delay time for
            load shift"
            ":math:`demand_{t}` ",":attr:`demand[t]`","P","Electrical
            demand series"
            ":math:`E_{t}^{do}` ",":attr:`capacity_down[tt]`","P","Capacity
            DSM down shift "
            ":math:`E_{t}^{up}` ", ":attr:`capacity_up[tt]`", "P","Capacity
            DSM up shift"
            ":math:`\mathbb{T}` "," ","P", "Time steps"


    """
    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        if group is None:
            return None

        m = self.parent_block()

        # for all DSM components get inflow from bus_elec
        for n in group:
            n.inflow = list(n.inputs)[0]

        #  ************* SETS *********************************

        # Set of DSM Components
        self.dsm = Set(initialize=[g for g in group])

        #  ************* VARIABLES *****************************

        # Variable load shift down
        self.dsm_do = Var(
            self.dsm,
            m.TIMESTEPS,
            m.TIMESTEPS,
            initialize=0,
            within=NonNegativeReals,
        )

        # Variable load shift up
        self.dsm_up = Var(
            self.dsm, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        #  ************* CONSTRAINTS *****************************

        # Demand Production Relation
        def _input_output_relation_rule(block):
            """
            Relation between input data and pyomo variables. The actual demand
            after DSM. Generator Production == Demand +- DSM
            """
            for t in m.TIMESTEPS:
                for g in group:

                    # first time steps: 0 + delay time
                    if t <= g.delay_time:

                        # Generator loads from bus
                        lhs = m.flow[g.inflow, g, t]
                        # Demand +- DSM
                        rhs = (
                            g.demand[t]
                            + self.dsm_up[g, t]
                            - sum(
                                self.dsm_do[g, tt, t]
                                for tt in range(t + g.delay_time + 1)
                            )
                        )

                        # add constraint
                        block.input_output_relation.add((g, t), (lhs == rhs))

                    # main use case
                    elif g.delay_time < t <= m.TIMESTEPS[-1] - g.delay_time:

                        # Generator loads from bus
                        lhs = m.flow[g.inflow, g, t]
                        # Demand +- DSM
                        rhs = (
                            g.demand[t]
                            + self.dsm_up[g, t]
                            - sum(
                                self.dsm_do[g, tt, t]
                                for tt in range(
                                    t - g.delay_time, t + g.delay_time + 1
                                )
                            )
                        )

                        # add constraint
                        block.input_output_relation.add((g, t), (lhs == rhs))

                    # last time steps: end - delay time
                    else:
                        # Generator loads from bus
                        lhs = m.flow[g.inflow, g, t]
                        # Demand +- DSM
                        rhs = (
                            g.demand[t]
                            + self.dsm_up[g, t]
                            - sum(
                                self.dsm_do[g, tt, t]
                                for tt in range(
                                    t - g.delay_time, m.TIMESTEPS[-1] + 1
                                )
                            )
                        )

                        # add constraint
                        block.input_output_relation.add((g, t), (lhs == rhs))

        self.input_output_relation = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.input_output_relation_build = BuildAction(
            rule=_input_output_relation_rule
        )

        # Equation 7
        def dsm_up_down_constraint_rule(block):
            """
            Equation 7 by Zerrahn, Schill:
            Every upward load shift has to be compensated by downward load
            shifts in a defined time frame. Slightly modified equations for
            the first and last time steps due to variable initialization.
            """

            for t in m.TIMESTEPS:
                for g in group:

                    # first time steps: 0 + delay time
                    if t <= g.delay_time:

                        # DSM up
                        lhs = self.dsm_up[g, t]
                        # DSM down
                        rhs = sum(
                            self.dsm_do[g, t, tt]
                            for tt in range(t + g.delay_time + 1)
                        )

                        # add constraint
                        block.dsm_updo_constraint.add((g, t), (lhs == rhs))

                    # main use case
                    elif g.delay_time < t <= (m.TIMESTEPS[-1] - g.delay_time):

                        # DSM up
                        lhs = self.dsm_up[g, t]
                        # DSM down
                        rhs = sum(
                            self.dsm_do[g, t, tt]
                            for tt in range(
                                t - g.delay_time, t + g.delay_time + 1
                            )
                        )

                        # add constraint
                        block.dsm_updo_constraint.add((g, t), (lhs == rhs))

                    # last time steps: end - delay time
                    else:

                        # DSM up
                        lhs = self.dsm_up[g, t]
                        # DSM down
                        rhs = sum(
                            self.dsm_do[g, t, tt]
                            for tt in range(
                                t - g.delay_time, m.TIMESTEPS[-1] + 1
                            )
                        )

                        # add constraint
                        block.dsm_updo_constraint.add((g, t), (lhs == rhs))

        self.dsm_updo_constraint = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.dsm_updo_constraint_build = BuildAction(
            rule=dsm_up_down_constraint_rule
        )

        # Equation 8
        def dsm_up_constraint_rule(block):
            """
            Equation 8 by Zerrahn, Schill:
            Realised upward load shift at time t has to be smaller than
            upward DSM capacity at time t.
            """

            for t in m.TIMESTEPS:
                for g in group:
                    # DSM up
                    lhs = self.dsm_up[g, t]
                    # Capacity dsm_up
                    rhs = g.capacity_up[t]

                    # add constraint
                    block.dsm_up_constraint.add((g, t), (lhs <= rhs))

        self.dsm_up_constraint = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.dsm_up_constraint_build = BuildAction(rule=dsm_up_constraint_rule)

        # Equation 9
        def dsm_do_constraint_rule(block):
            """
            Equation 9 by Zerrahn, Schill:
            Realised downward load shift at time t has to be smaller than
            downward DSM capacity at time t.
            """

            for tt in m.TIMESTEPS:
                for g in group:

                    # first times steps: 0 + delay
                    if tt <= g.delay_time:

                        # DSM down
                        lhs = sum(
                            self.dsm_do[g, t, tt]
                            for t in range(tt + g.delay_time + 1)
                        )
                        # Capacity DSM down
                        rhs = g.capacity_down[tt]

                        # add constraint
                        block.dsm_do_constraint.add((g, tt), (lhs <= rhs))

                    # main use case
                    elif g.delay_time < tt <= (m.TIMESTEPS[-1] - g.delay_time):

                        # DSM down
                        lhs = sum(
                            self.dsm_do[g, t, tt]
                            for t in range(
                                tt - g.delay_time, tt + g.delay_time + 1
                            )
                        )
                        # Capacity DSM down
                        rhs = g.capacity_down[tt]

                        # add constraint
                        block.dsm_do_constraint.add((g, tt), (lhs <= rhs))

                    # last time steps: end - delay time
                    else:

                        # DSM down
                        lhs = sum(
                            self.dsm_do[g, t, tt]
                            for t in range(
                                tt - g.delay_time, m.TIMESTEPS[-1] + 1
                            )
                        )
                        # Capacity DSM down
                        rhs = g.capacity_down[tt]

                        # add constraint
                        block.dsm_do_constraint.add((g, tt), (lhs <= rhs))

        self.dsm_do_constraint = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.dsm_do_constraint_build = BuildAction(rule=dsm_do_constraint_rule)

        # Equation 10
        def c2_constraint_rule(block):
            """
            Equation 10 by Zerrahn, Schill:
            The realised DSM up or down at time T has to be smaller than
            the maximum downward or upward capacity at time T. Therefore in
            total each DSM unit can only be shifted up OR down.
            """

            for tt in m.TIMESTEPS:
                for g in group:

                    # first times steps: 0 + delay time
                    if tt <= g.delay_time:

                        # DSM up/down
                        lhs = self.dsm_up[g, tt] + sum(
                            self.dsm_do[g, t, tt]
                            for t in range(tt + g.delay_time + 1)
                        )
                        # max capacity at tt
                        rhs = max(g.capacity_up[tt], g.capacity_down[tt])

                        # add constraint
                        block.C2_constraint.add((g, tt), (lhs <= rhs))

                    elif g.delay_time < tt <= (m.TIMESTEPS[-1] - g.delay_time):

                        # DSM up/down
                        lhs = self.dsm_up[g, tt] + sum(
                            self.dsm_do[g, t, tt]
                            for t in range(
                                tt - g.delay_time, tt + g.delay_time + 1
                            )
                        )
                        # max capacity at tt
                        rhs = max(g.capacity_up[tt], g.capacity_down[tt])

                        # add constraint
                        block.C2_constraint.add((g, tt), (lhs <= rhs))

                    else:

                        # DSM up/down
                        lhs = self.dsm_up[g, tt] + sum(
                            self.dsm_do[g, t, tt]
                            for t in range(
                                tt - g.delay_time, m.TIMESTEPS[-1] + 1
                            )
                        )
                        # max capacity at tt
                        rhs = max(g.capacity_up[tt], g.capacity_down[tt])

                        # add constraint
                        block.C2_constraint.add((g, tt), (lhs <= rhs))

        self.C2_constraint = Constraint(group, m.TIMESTEPS, noruleinit=True)
        self.C2_constraint_build = BuildAction(rule=c2_constraint_rule)

    def _objective_expression(self):
        """Adding cost terms for DSM activity to obj. function"""

        m = self.parent_block()

        dsm_cost = 0

        for t in m.TIMESTEPS:
            for g in self.dsm:
                dsm_cost += self.dsm_up[g, t] * g.cost_dsm_up
                dsm_cost += (
                    sum(self.dsm_do[g, t, tt] for tt in m.TIMESTEPS)
                    * g.cost_dsm_down
                )

        self.cost = Expression(expr=dsm_cost)

        return self.cost
