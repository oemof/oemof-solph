# -*- coding: utf-8 -*-

"""
Implementation of demand-side management (demand response) which allows for

* modeling load shifting and/or shedding of a given baseline demand
  for a demand response portfolio,
* assessing both, a pure dispatch and an investment model and
* choosing among different (storage-alike) implementations.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Johannes Röder
SPDX-FileCopyrightText: jakob-wo
SPDX-FileCopyrightText: gplssm
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: Julian Endres
SPDX-FileCopyrightText: Johannes Kochems

SPDX-License-Identifier: MIT

"""
import itertools
from warnings import warn

import numpy as np
from oemof.tools import debugging
from oemof.tools import economics
from pyomo.core.base.block import ScalarBlock
from pyomo.environ import BuildAction
from pyomo.environ import Constraint
from pyomo.environ import Expression
from pyomo.environ import NonNegativeReals
from pyomo.environ import Set
from pyomo.environ import Var

from oemof.solph._options import Investment
from oemof.solph._plumbing import sequence
from oemof.solph._plumbing import valid_sequence
from oemof.solph.components._sink import Sink


class SinkDSM(Sink):
    r"""
    Demand Side Management implemented as a Sink with flexibility potential
    to deviate from the baseline demand in upwards or downwards direction.

    There are several approaches possible which can be selected:

    * DIW: Based on the paper by Zerrahn, Alexander and Schill, Wolf-Peter
      (2015): On the representation of demand-side management in power system
      models, in: Energy (84), pp. 840-845,
      `10.1016/j.energy.2015.03.037
      <https://doi.org/10.1016/j.energy.2015.03.037>`_,
      accessed 08.01.2021, pp. 842-843.
    * DLR: Based on the PhD thesis of Gils, Hans Christian (2015):
      `Balancing of Intermittent Renewable Power Generation by Demand Response
      and Thermal Energy Storage`, Stuttgart,
      `<https://doi.org/10.18419/opus-6888>`_,
      accessed 08.01.2021, pp. 67-70.
    * oemof: Created by Julian Endres. A fairly simple DSM representation which
      demands the energy balance to be levelled out in fixed cycles

    An evaluation of different modeling approaches has been carried out and
    presented at the INREC 2020. Some of the results are as follows:

    * DIW: A solid implementation with the tendency of slight overestimization
      of potentials since a `shift_time` is not included. It may get
      computationally expensive due to a high time-interlinkage in constraint
      formulations.
    * DLR: An extensive modeling approach for demand response which neither
      leads to an over- nor underestimization of potentials and balances
      modeling detail and computation intensity. `fixes` and
      `addition` should both be set to True which is the default value.
    * oemof: A very computationally efficient approach which only requires the
      energy balance to be levelled out in certain intervals. If demand
      response is not at the center of the research and/or parameter
      availability is limited, this approach should be chosen.
      Note that approach `oemof` does allow for load shedding,
      but does not impose a limit on maximum amount of shedded energy.

    SinkDSM adds additional constraints that allow to shift energy in certain
    time window constrained by `capacity_up` and `capacity_down`.

    Parameters
    ----------
    demand: numeric
        original electrical demand (normalized)
        For investment modeling, it is advised to use the maximum of the
        demand timeseries and the cumulated (fixed) infeed time series
        for normalization, because the balancing potential may be determined by
        both. Else, underinvestments may occur.
    capacity_up: int or iterable
        maximum DSM capacity that may be increased (normalized)
    capacity_down: int or iterable
        maximum DSM capacity that may be reduced (normalized)
    approach: str, one of 'oemof', 'DIW', 'DLR'
        Choose one of the DSM modeling approaches. Read notes about which
        parameters to be applied for which approach.

        oemof :

            Simple model in which the load shift must be compensated in a
            predefined fixed interval (`shift_interval` is mandatory).
            Within time windows of the length `shift_interval` DSM
            up and down shifts are balanced. For details see
            :class:`~SinkDSMOemofBlock` resp.
            :class:`~SinkDSMOemofInvestmentBlock`.

        DIW :

            Sophisticated model based on the formulation by
            Zerrahn & Schill (2015a). The load shift of the component must be
            compensated in a predefined delay time (`delay_time` is
            mandatory).
            For details see
            :class:`~SinkDSMDIWBlock` resp.
            :class:`~SinkDSMDIWInvestmentBlock`.

        DLR :

            Sophisticated model based on the formulation by
            Gils (2015). The load shift of the component must be
            compensated in a predefined delay time (`delay_time` is
            mandatory).
            For details see
            :class:`~SinkDSMDLRBlock` resp.
            :class:`~SinkDSMDLRInvestmentBlock`.
    shift_interval: int
        Only used when `approach` is set to "oemof". Otherwise, can be
        None.
        It's the interval in which between :math:`DSM_{t}^{up}` and
        :math:`DSM_{t}^{down}` have to be compensated.
    delay_time: int or iterable
        Only used when :attr:`~approach` is set to "DIW" or "DLR". Otherwise,
        can be None. Iterable only allowed in case approach "DLR" is used.
        Length of symmetrical time windows around :math:`t` in which
        :math:`DSM_{t}^{up}` and :math:`DSM_{t,tt}^{down}` have to be
        compensated.
        Note: For approach 'DLR', if an integer is passed,
        an iterable is constructed in order to model flexible delay times.
        In case an iterable is passed, this will be used directly.
    shift_time: int
        Only used when `approach` is set to "DLR".
        Duration of a single upwards or downwards shift (half a shifting cycle
        if there is immediate compensation)
    shed_time: int
        Only used when `shed_eligibility` is set to True.
        Maximum length of a load shedding process at full capacity
        (used within energy limit constraint)
    max_demand: numeric or iterable
        Maximum demand prior to demand response (per period)
    max_capacity_down: numeric
        Maximum capacity eligible for downshifts
        prior to demand response (used only for dispatch mode)
    max_capacity_up: numeric
        Maximum capacity eligible for upshifts
        prior to demand response (used only for dispatch mode)
    cost_dsm_up : float
        Cost per unit of DSM activity that increases the demand
    cost_dsm_down_shift : float
        Cost per unit of DSM activity that decreases the demand
        for load shifting
    cost_dsm_down_shed : float
        Cost per unit of DSM activity that decreases the demand
        for load shedding
    efficiency : float
        Efficiency factor for load shifts (between 0 and 1)
    recovery_time_shift : int
        Only used when `approach` is set to "DIW".
        Minimum time between the end of one load shifting process
        and the start of another for load shifting processes
    recovery_time_shed : int
        Minimum time between the end of one load shifting process
        and the start of another for load shedding processes
    ActivateYearLimit : boolean
        Only used when `approach` is set to "DLR".
        Control parameter; activates constraints for year limit if set to True
    ActivateDayLimit : boolean
        Only used when `approach` is set to "DLR".
        Control parameter; activates constraints for day limit if set to True
    n_yearLimit_shift : int
        Only used when `approach` is set to "DLR".
        Maximum number of load shifts at full capacity per year, used to limit
        the amount of energy shifted per year. Optional parameter that is only
        needed when ActivateYearLimit is True
    n_yearLimit_shed : int
        Only used when `approach` is set to "DLR".
        Maximum number of load sheds at full capacity per year, used to limit
        the amount of energy shedded per year. Mandatory parameter if load
        shedding is allowed by setting `shed_eligibility` to True
    t_dayLimit: int
        Only used when `approach` is set to "DLR".
        Maximum duration of load shifts at full capacity per day, used to limit
        the amount of energy shifted per day. Optional parameter that is only
        needed when ActivateDayLimit is True
    addition : boolean
        Only used when `approach` is set to "DLR".
        Boolean parameter indicating whether or not to include additional
        constraint (which corresponds to Eq. 10
        from Zerrahn and Schill (2015a))
    fixes : boolean
        Only used when `approach` is set to "DLR".
        Boolean parameter indicating whether or not to include additional
        fixes. These comprise prohibiting shifts which cannot be balanced
        within the optimization timeframe
    shed_eligibility : boolean
        Boolean parameter indicating whether unit is eligible for
        load shedding
    shift_eligibility : boolean
        Boolean parameter indicating whether unit is eligible for
        load shifting
    fixed_costs : numeric
        Nominal value of fixed costs (per year)

    Note
    ----

    * `method` has been renamed to `approach`.
    * As many constraints and dependencies are created in approach "DIW",
      computational cost might be high with a large `delay_time` and with model
      of high temporal resolution.
    * The approach "DLR" preforms better in terms of calculation time,
      compared to the approach "DIW".
    * Using `approach` "DIW" or "DLR" might result in demand shifts that
      exceed the specified delay time by activating up and down simultaneously
      in the time steps between to DSM events. Thus, the purpose of this
      component is to model demand response portfolios rather than individual
      demand units.
    * It's not recommended to assign cost to the flow that connects
      :class:`~SinkDSM` with a bus. Instead, use `cost_dsm_up`
      or `cost_dsm_down_shift`.
    * Variable costs may be attributed to upshifts, downshifts or both.
      Costs for shedding may deviate from that for shifting
      (usually costs for shedding are much larger and equal to the value
      of lost load).

    """

    def __init__(
        self,
        demand,
        capacity_up,
        capacity_down,
        approach,
        label=None,
        inputs=None,
        shift_interval=None,
        delay_time=None,
        shift_time=None,
        shed_time=None,
        max_demand=None,
        max_capacity_down=None,
        max_capacity_up=None,
        cost_dsm_up=0,
        cost_dsm_down_shift=0,
        cost_dsm_down_shed=0,
        efficiency=1,
        recovery_time_shift=None,
        recovery_time_shed=None,
        ActivateYearLimit=False,
        ActivateDayLimit=False,
        n_yearLimit_shift=None,
        n_yearLimit_shed=None,
        t_dayLimit=None,
        addition=True,
        fixes=True,
        shed_eligibility=True,
        shift_eligibility=True,
        fixed_costs=0,
        investment=None,
        custom_properties=None,
    ):
        if custom_properties is None:
            custom_properties = {}
        super().__init__(
            label=label, inputs=inputs, custom_properties=custom_properties
        )

        self.capacity_up = sequence(capacity_up)
        self.capacity_down = sequence(capacity_down)
        self.demand = sequence(demand)
        self.approach = approach
        self.shift_interval = shift_interval
        if not approach == "DLR":
            if approach == "DIW":
                if not isinstance(delay_time, int):
                    raise ValueError(
                        "If approach 'DIW' is used, "
                        "delay time has to be of type int."
                    )
            self.delay_time = delay_time
        else:
            if isinstance(delay_time, int):
                self.delay_time = [el for el in range(1, delay_time + 1)]
            else:
                self.delay_time = delay_time
        self.shift_time = shift_time
        self.shed_time = shed_time
        self.max_capacity_down = max_capacity_down
        self.max_capacity_up = max_capacity_up
        self.max_demand = sequence(max_demand)
        self.cost_dsm_up = sequence(cost_dsm_up)
        self.cost_dsm_down_shift = sequence(cost_dsm_down_shift)
        self.cost_dsm_down_shed = sequence(cost_dsm_down_shed)
        self.efficiency = efficiency
        self.capacity_down_mean = np.mean(capacity_down)
        self.capacity_up_mean = np.mean(capacity_up)
        self.recovery_time_shift = recovery_time_shift
        self.recovery_time_shed = recovery_time_shed
        self.ActivateYearLimit = ActivateYearLimit
        self.ActivateDayLimit = ActivateDayLimit
        self.n_yearLimit_shift = n_yearLimit_shift
        self.n_yearLimit_shed = n_yearLimit_shed
        self.t_dayLimit = t_dayLimit
        self.addition = addition
        self.fixes = fixes
        self.shed_eligibility = shed_eligibility
        self.shift_eligibility = shift_eligibility
        self.fixed_costs = sequence(fixed_costs)

        # Check whether investment mode is active or not
        self.investment = investment
        self._invest_group = isinstance(self.investment, Investment)

        if (
            self.max_capacity_up is None or self.max_capacity_down is None
        ) and not self._invest_group:
            e1 = (
                "If you are using the dispatch mode, "
                "you have to specify `max_capacity_up` "
                "and `max_capacity_down`."
            )
            raise AttributeError(e1)

        if self._invest_group:
            self._check_invest_attributes()

    def _check_invest_attributes(self):
        if (
            self.max_capacity_down or self.max_capacity_up
        ) and self.investment is not None:
            e2 = (
                "If you are using the investment mode, the invest variable "
                "replaces the `max_capacity_down` "
                "as well as the `max_capacity_up` values.\n"
                "Therefore, `max_capacity_up` and `max_capacity_down` "
                "values should be None (which is their default value)."
            )
            raise AttributeError(e2)

    def constraint_group(self):
        possible_approaches = ["DIW", "DLR", "oemof"]

        if not self.shed_eligibility and not self.shift_eligibility:
            raise ValueError(
                "At least one of shed_eligibility"
                " and shift_eligibility must be True"
            )
        if self.shed_eligibility:
            if self.recovery_time_shed is None:
                raise ValueError(
                    "If unit is eligible for load shedding,"
                    " recovery_time_shed must be defined"
                )

        if self.approach in [possible_approaches[0], possible_approaches[1]]:
            if self.delay_time is None:
                raise ValueError(
                    f"Please define: delay_time.\n"
                    f"It is a mandatory parameter when using"
                    f" approach {self.approach}."
                )

        if self.approach == possible_approaches[0]:
            if self._invest_group is True:
                return SinkDSMDIWInvestmentBlock
            else:
                return SinkDSMDIWBlock

        elif self.approach == possible_approaches[1]:
            if self._invest_group is True:
                return SinkDSMDLRInvestmentBlock
            else:
                return SinkDSMDLRBlock

        elif self.approach == possible_approaches[2]:
            if self.shift_interval is None:
                raise ValueError(
                    f"Please define: shift_interval.\n"
                    f"It is a mandatory parameter when using"
                    f" approach {self.approach}."
                )
            if self._invest_group is True:
                return SinkDSMOemofInvestmentBlock
            else:
                return SinkDSMOemofBlock
        else:
            raise ValueError(
                'The "approach" must be one of the following set: '
                '"{}"'.format('" or "'.join(possible_approaches))
            )


class SinkDSMOemofBlock(ScalarBlock):
    r"""Constraints for SinkDSM with "oemof" approach

    **The following constraints are created for approach = "oemof":**

    .. _SinkDSMOemofBlock equations:

    .. math::
        &
        (1) \quad DSM_{t}^{up} = 0 \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T}
        \quad \textrm{if} \quad e_{shift} = \textrm{False} \\
        & \\
        &
        (2) \quad DSM_{t}^{do, shed} = 0 \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T}
        \quad \textrm{if} \quad e_{shed} = \textrm{False} \\
        & \\
        &
        (3) \quad \dot{E}_{t} = demand_{t} \cdot demand_{max} + DSM_{t}^{up}
        - DSM_{t}^{do, shift} - DSM_{t}^{do, shed} \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T} \\
        & \\
        &
        (4) \quad  DSM_{t}^{up} \leq E_{t}^{up} \cdot E_{up, max} \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T} \\
        & \\
        &
        (5) \quad DSM_{t}^{do, shift} + DSM_{t}^{do, shed}
        \leq  E_{t}^{do} \cdot E_{do, max} \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T} \\
        & \\
        &
        (6) \quad  \sum_{t=t_s}^{t_s+\tau} DSM_{t}^{up} \cdot \eta =
        \sum_{t=t_s}^{t_s+\tau} DSM_{t}^{do, shift} \\
        & \quad \quad \quad \quad \forall t_s \in \{k \in \mathbb{T}
        \mid k \mod \tau = 0\} \\

    **The following parts of the objective function are created:**

    .. math::
        &
        (DSM_{t}^{up} \cdot cost_{t}^{dsm, up}
        + DSM_{t}^{do, shift} \cdot cost_{t}^{dsm, do, shift}\\
        &
        + DSM_{t}^{do, shed} \cdot cost_{t}^{dsm, do, shed})
        \cdot \omega_{t} \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T} \\

    * :attr:`fixed_costs` not None

    .. math::
        \displaystyle \sum_{pp=0}^{year_{max}} max\{E_{up, max}, E_{do, max}\}
        \cdot c_{fixed}(pp) \cdot DF^{-pp}

    **Table: Symbols and attribute names of variables and parameters**

    .. table:: Variables (V), Parameters (P) and Sets (S)
        :widths: 25, 25, 10, 40

        ================================= ======================== ==== =======================================
        symbol                            attribute                type explanation
        ================================= ======================== ==== =======================================
        :math:`DSM_{t}^{up}`              `dsm_up[g, t]`           V    DSM up shift (capacity shifted upwards)
        :math:`DSM_{t}^{do, shift}`       `dsm_do_shift[g, t]`     V    DSM down shift (capacity shifted downwards)
        :math:`DSM_{t}^{do, shed}`        `dsm_do_shed[g, t]`      V    DSM shedded (capacity shedded, i.e. not compensated for)
        :math:`\dot{E}_{t}`               `SinkDSM.inputs`         V    Energy flowing in from (electrical) inflow bus
        :math:`demand_{t}`                `demand[t]`              P    (Electrical) demand series before shifting (normalized)
        :math:`demand_{max}(p)`           `max_demand`             P    Maximum demand value in period p
        :math:`E_{t}^{do}`                `capacity_down[t]`       P    | Capacity  allowed for a load adjustment downwards
                                                                        | (normalized; shifting + shedding)
        :math:`E_{t}^{up}`                `capacity_up[t]`         P    Capacity allowed for a shift upwards (normalized)
        :math:`E_{do, max}`               `max_capacity_down`      P    | Maximum capacity allowed for a load adjustment downwards
                                                                        | (shifting + shedding)
        :math:`E_{up, max}`               `max_capacity_up`        P    Maximum capacity allowed for a shift upwards
        :math:`\tau`                      `shift_interval`         P    | interval (time within which the
                                                                        | energy balance must be levelled out)
        :math:`\eta`                      `efficiency`             P    Efficiency for load shifting processes
        :math:`\mathbb{T}`                                         S    Time steps of the model
        :math:`e_{shift}`                 `shift_eligibility`      P    | Boolean parameter indicating if unit can be used
                                                                        | for load shifting
        :math:`e_{shed}`                  `shed_eligibility`       P    | Boolean parameter indicating if unit can be used
                                                                        | for load shedding
        :math:`cost_{t}^{dsm, up}`        `cost_dsm_up[t]`         P    Variable costs for an upwards shift
        :math:`cost_{t}^{dsm, do, shift}` `cost_dsm_down_shift[t]` P    Variable costs for a downwards shift (load shifting)
        :math:`cost_{t}^{dsm, do, shed}`  `cost_dsm_down_shift[t]` P    Variable costs for shedding load
        :math:`\omega_{t}`                                         P    Objective weighting of the model for timestep t
        :math:`year_{max}`                                         P    Last year of the optimization horizon
        ================================= ======================== ==== =======================================

    """  # noqa: E501

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        if group is None:
            return None

        m = self.parent_block()

        # for all DSM components get inflow from a bus
        for n in group:
            n.inflow = list(n.inputs)[0]

        #  ************* SETS *********************************

        # Set of DSM Components
        self.dsm = Set(initialize=[n for n in group])

        #  ************* VARIABLES *****************************

        # Variable load shift down
        self.dsm_do_shift = Var(
            self.dsm, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        # Variable load shedding
        self.dsm_do_shed = Var(
            self.dsm, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        # Variable load shift up
        self.dsm_up = Var(
            self.dsm, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        #  ************* CONSTRAINTS *****************************

        def _shift_shed_vars_rule(block):
            """Force shifting resp. shedding variables to zero dependent
            on how boolean parameters for shift resp. shed eligibility
            are set.
            """
            for t in m.TIMESTEPS:
                for g in group:
                    if not g.shift_eligibility:
                        lhs = self.dsm_up[g, t]
                        rhs = 0

                        block.shift_shed_vars.add((g, t), (lhs == rhs))

                    if not g.shed_eligibility:
                        lhs = self.dsm_do_shed[g, t]
                        rhs = 0

                        block.shift_shed_vars.add((g, t), (lhs == rhs))

        self.shift_shed_vars = Constraint(group, m.TIMESTEPS, noruleinit=True)
        self.shift_shed_vars_build = BuildAction(rule=_shift_shed_vars_rule)

        # Demand Production Relation
        def _input_output_relation_rule(block):
            """Relation between input data and pyomo variables.
            The actual demand after DSM.
            Generator Production == Demand_el +- DSM
            """
            for p, t in m.TIMEINDEX:
                for g in group:
                    # Inflow from bus
                    lhs = m.flow[g.inflow, g, t]

                    # Demand + DSM_up - DSM_down
                    rhs = (
                        g.demand[t] * g.max_demand[p]
                        + self.dsm_up[g, t]
                        - self.dsm_do_shift[g, t]
                        - self.dsm_do_shed[g, t]
                    )

                    # add constraint
                    block.input_output_relation.add((g, p, t), (lhs == rhs))

        self.input_output_relation = Constraint(
            group, m.TIMEINDEX, noruleinit=True
        )
        self.input_output_relation_build = BuildAction(
            rule=_input_output_relation_rule
        )

        # Upper bounds relation
        def dsm_up_constraint_rule(block):
            """Realised upward load shift at time t has to be smaller than
            upward DSM capacity at time t.
            """
            for t in m.TIMESTEPS:
                for g in group:
                    # DSM up
                    lhs = self.dsm_up[g, t]
                    # Capacity dsm_up
                    rhs = g.capacity_up[t] * g.max_capacity_up

                    # add constraint
                    block.dsm_up_constraint.add((g, t), (lhs <= rhs))

        self.dsm_up_constraint = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.dsm_up_constraint_build = BuildAction(rule=dsm_up_constraint_rule)

        # Upper bounds relation
        def dsm_down_constraint_rule(block):
            """Realised downward load shift at time t has to be smaller than
            downward DSM capacity at time t.
            """
            for t in m.TIMESTEPS:
                for g in group:
                    # DSM down
                    lhs = self.dsm_do_shift[g, t] + self.dsm_do_shed[g, t]
                    # Capacity dsm_down
                    rhs = g.capacity_down[t] * g.max_capacity_down

                    # add constraint
                    block.dsm_down_constraint.add((g, t), (lhs <= rhs))

        self.dsm_down_constraint = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.dsm_down_constraint_build = BuildAction(
            rule=dsm_down_constraint_rule
        )

        def dsm_sum_constraint_rule(block):
            """Relation to compensate the total amount of positive
            and negative DSM in between the shift_interval.
            This constraint is building balance in full intervals starting
            with index 0. The last interval might not be full.
            """
            for g in group:
                intervals = range(
                    m.TIMESTEPS.at(1), m.TIMESTEPS.at(-1), g.shift_interval
                )

                for interval in intervals:
                    if (interval + g.shift_interval - 1) > m.TIMESTEPS.at(-1):
                        timesteps = range(interval, m.TIMESTEPS.at(-1) + 1)
                    else:
                        timesteps = range(
                            interval, interval + g.shift_interval
                        )

                    # DSM up/down
                    lhs = (
                        sum(self.dsm_up[g, tt] for tt in timesteps)
                        * g.efficiency
                    )
                    # value
                    rhs = sum(self.dsm_do_shift[g, tt] for tt in timesteps)

                    # add constraint
                    block.dsm_sum_constraint.add((g, interval), (lhs == rhs))

        self.dsm_sum_constraint = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.dsm_sum_constraint_build = BuildAction(
            rule=dsm_sum_constraint_rule
        )

    def _objective_expression(self):
        r"""Objective expression with variable costs for DSM activity"""

        m = self.parent_block()

        variable_costs = 0
        fixed_costs = 0

        if m.es.periods is None:
            for t in m.TIMESTEPS:
                for g in self.dsm:
                    variable_costs += (
                        self.dsm_up[g, t]
                        * g.cost_dsm_up[t]
                        * m.objective_weighting[t]
                    )
                    variable_costs += (
                        self.dsm_do_shift[g, t] * g.cost_dsm_down_shift[t]
                        + self.dsm_do_shed[g, t] * g.cost_dsm_down_shed[t]
                    ) * m.objective_weighting[t]

        else:
            for g in self.dsm:
                for p, t in m.TIMEINDEX:
                    variable_costs += (
                        self.dsm_up[g, t]
                        * m.objective_weighting[t]
                        * g.cost_dsm_up[t]
                    )
                    variable_costs += (
                        self.dsm_do_shift[g, t] * g.cost_dsm_down_shift[t]
                        + self.dsm_do_shed[g, t] * g.cost_dsm_down_shed[t]
                    ) * m.objective_weighting[t]

                if valid_sequence(g.fixed_costs, len(m.PERIODS)):
                    fixed_costs += sum(
                        max(g.max_capacity_up, g.max_capacity_down)
                        * g.fixed_costs[pp]
                        for pp in range(m.es.end_year_of_optimization)
                    )

        self.variable_costs = Expression(expr=variable_costs)
        self.fixed_costs = Expression(expr=fixed_costs)
        self.costs = Expression(expr=variable_costs + fixed_costs)

        return self.costs


class SinkDSMOemofInvestmentBlock(ScalarBlock):
    r"""Constraints for SinkDSM with "oemof" approach and `investment`
    defined

    **The following constraints are created for approach = "oemof"
    with an investment object defined:**

    .. _SinkDSMOemofInvestmentBlock equations:

    .. math::
        &
        (1) \quad invest_{min}(p) \leq invest(p) \leq invest_{max}(p) \\
        & \quad \quad \quad \quad \forall p \in \mathbb{P}
        & \\
        &
        (2) \quad DSM_{t}^{up} = 0 \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T}
        \quad \textrm{if} \quad e_{shift} = \textrm{False} \\
        & \\
        &
        (3) \quad DSM_{t}^{do, shed} = 0 \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T}
        \quad \textrm{if} \quad e_{shed} = \textrm{False} \\
        & \\
        &
        (4) \quad \dot{E}_{t} = demand_{t} \cdot demand_{max}(p)
        + DSM_{t}^{up}
        - DSM_{t}^{do, shift} - DSM_{t}^{do, shed} \\
        & \quad \quad \quad \quad \forall p, t \in \textrm{TIMEINDEX} \\
        & \\
        &
        (5) \quad  DSM_{t}^{up} \leq E_{t}^{up} \cdot P_{total}(p) \\
        & \quad \quad \quad \quad \forall p, t \in \textrm{TIMEINDEX} \\
        & \\
        &
        (6) \quad DSM_{t}^{do, shift} +  DSM_{t}^{do, shed} \leq
        E_{t}^{do} \cdot P_{total}(p) \\
        & \quad \quad \quad \quad \forall p, t \in \textrm{TIMEINDEX} \\
        & \\
        &
        (7) \quad  \sum_{t=t_s}^{t_s+\tau} DSM_{t}^{up} \cdot \eta =
        \sum_{t=t_s}^{t_s+\tau} DSM_{t}^{do, shift} \\
        & \quad \quad \quad \quad \forall t_s \in
        \{k \in \mathbb{T} \mid k \mod \tau = 0\} \\


    **The following parts of the objective function are created:**

    *Standard model*

        * Investment annuity:

            .. math::
                P_{invest}(0) \cdot c_{invest}(0)

        * Variable costs:

            .. math::
                &
                (DSM_{t}^{up} \cdot cost_{t}^{dsm, up}
                + DSM_{t}^{do, shift} \cdot cost_{t}^{dsm, do, shift} \\
                & + DSM_{t}^{do, shed} \cdot cost_{t}^{dsm, do, shed})
                \cdot \omega_{t} \\
                & \quad \quad \quad \quad \forall t \in \mathbb{T} \\

    *Multi-period model*

        * Investment annuity:

            .. math::
                &
                P_{invest}(p) \cdot A(c_{invest}(p), l, ir)
                \cdot \frac {1}{ANF(d, ir)} \cdot DF^{-p} \\
                &\\
                &
                \forall p \in \mathbb{P}

        In case, the remaining lifetime of a DSM unit is greater than 0 and
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

        * :attr:`fixed_costs` not None for investments

            .. math::
                &
                (\sum_{pp=year(p)}^{limit_{end}}
                P_{invest}(p) \cdot c_{fixed}(pp) \cdot DF^{-pp})
                \cdot DF^{-p} \\
                &\\
                &
                \forall p \in \mathbb{P}

        * Variable costs:

            .. math::
                &
                (DSM_{t}^{up} \cdot cost_{t}^{dsm, up}
                + DSM_{t}^{do, shift} \cdot cost_{t}^{dsm, do, shift} \\
                & + DSM_{t}^{do, shed} \cdot cost_{t}^{dsm, do, shed})
                \cdot \omega_{t}
                \cdot DF^{-p} \\
                & \quad \quad \quad \quad
                \forall p, t \in \textrm{TIMEINDEX} \\

    where:

    * :math:`A(c_{invest,var}(p), l, ir)` A is the annuity for
      investment expenses :math:`c_{invest,var}(p)`, lifetime :math:`l`
      and interest rate :math:`ir`.
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
    * :math:`DF=(1+dr)` is the discount factor.

    The annuity / annuity factor hereby is:

        .. math::
            &
            A(c_{invest,var}(p), l, ir) = c_{invest,var}(p) \cdot
                \frac {(1+ir)^l \cdot ir} {(1+ir)^l - 1}\\
            &\\
            &
            ANF(d, ir)=\frac {(1+dr)^d \cdot dr} {(1+dr)^d - 1}

    They are retrieved, using oemof.tools.economics annuity function. The
    interest rate :math:`ir` for the annuity is defined as weighted
    average costs of capital (wacc) and assumed constant over time.

    See remarks in
    :class:`oemof.solph.components.experimental._sink_dsm.SinkDSMOemofBlock`.


    **Symbols and attribute names of variables and parameters**

    * Please refer to
      :class:`oemof.solph.components.experimental._sink_dsm.SinkDSMOemofBlock`.
      for a variables and parameter description.
    * The following variables and parameters are exclusively used for
      investment modeling:

    .. table:: Variables (V), Parameters (P) and Sets (S)
        :widths: 25, 25, 10, 40

        ================================= ======================== ==== =======================================
        symbol                            attribute                type explanation
        ================================= ======================== ==== =======================================
        :math:`P_{invest}(p)`             `invest[p]`              V    | DSM capacity invested into in period p.
                                                                        | Equals to the additionally shiftable resp. sheddable capacity.
        :math:`invest_{min}(p)`           `investment.minimum[p]`  P    minimum investment in period p
        :math:`invest_{max}(p)`           `investment.maximum[p]`  P    maximum investment in period p
        :math:`P_{total}`                 `investment.total[p]`    P    total DSM capacity
        :math:`costs_{invest}(p)`         `investment.ep_costs[p]` P    | specific investment annuity (standard model) resp.
                                                                        | specific investment expenses (multi-period model)
        :math:`\mathbb{P}`                                         S    Periods of the model
        :math:`\textrm{TIMEINDEX}`                                 S    Timeindex set of the model (periods, timesteps)
        ================================= ======================== ==== =======================================

    """  # noqa: E501

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        if group is None:
            return None

        m = self.parent_block()

        # for all DSM components get inflow from a bus
        for n in group:
            n.inflow = list(n.inputs)[0]

        #  ************* SETS *********************************

        # Set of DSM Components
        self.investdsm = Set(initialize=[n for n in group])

        self.OVERALL_MAXIMUM_INVESTDSM = Set(
            initialize=[
                g for g in group if g.investment.overall_maximum is not None
            ]
        )

        self.OVERALL_MINIMUM_INVESTDSM = Set(
            initialize=[
                g for g in group if g.investment.overall_minimum is not None
            ]
        )

        self.EXISTING_INVESTDSM = Set(
            initialize=[g for g in group if g.investment.existing is not None]
        )

        #  ************* VARIABLES *****************************

        # Define bounds for investments in demand response
        def _dsm_investvar_bound_rule(block, g, p):
            """Rule definition to bound the
            invested demand response capacity `invest`.
            """
            return g.investment.minimum[p], g.investment.maximum[p]

        # Investment in DR capacity
        self.invest = Var(
            self.investdsm,
            m.PERIODS,
            within=NonNegativeReals,
            bounds=_dsm_investvar_bound_rule,
        )

        # Total capacity
        self.total = Var(self.investdsm, m.PERIODS, within=NonNegativeReals)

        if m.es.periods is not None:
            # Old capacity to be decommissioned (due to lifetime)
            self.old = Var(self.investdsm, m.PERIODS, within=NonNegativeReals)

            # Old endogenous capacity to be decommissioned (due to lifetime)
            self.old_end = Var(
                self.investdsm, m.PERIODS, within=NonNegativeReals
            )

            # Old exogenous capacity to be decommissioned (due to lifetime)
            self.old_exo = Var(
                self.investdsm, m.PERIODS, within=NonNegativeReals
            )

        # Variable load shift down
        self.dsm_do_shift = Var(
            self.investdsm, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        # Variable load shedding
        self.dsm_do_shed = Var(
            self.investdsm, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        # Variable load shift up
        self.dsm_up = Var(
            self.investdsm, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        #  ************* CONSTRAINTS *****************************

        # Handle unit lifetimes
        def _total_dsm_capacity_rule(block):
            """Rule definition for determining total installed
            capacity (taking decommissioning into account)
            """
            for g in group:
                for p in m.PERIODS:
                    if p == 0:
                        expr = (
                            self.total[g, p]
                            == self.invest[g, p] + g.investment.existing
                        )
                        self.total_dsm_rule.add((g, p), expr)
                    else:
                        expr = (
                            self.total[g, p]
                            == self.invest[g, p]
                            + self.total[g, p - 1]
                            - self.old[g, p]
                        )
                        self.total_dsm_rule.add((g, p), expr)

        self.total_dsm_rule = Constraint(group, m.PERIODS, noruleinit=True)
        self.total_dsm_rule_build = BuildAction(rule=_total_dsm_capacity_rule)

        if m.es.periods is not None:

            def _old_dsm_capacity_rule_end(block):
                """Rule definition for determining old endogenously installed
                capacity to be decommissioned due to reaching its lifetime.
                Investment and decommissioning periods are linked within
                the constraint. The respective decommissioning period is
                determined for every investment period based on the components
                lifetime and a matrix describing its age of each endogenous
                investment. Decommissioning can only occur at the beginning of
                each period.

                Note
                ----
                For further information on the implementation check
                PR#957 https://github.com/oemof/oemof-solph/pull/957
                """
                for g in group:
                    lifetime = g.investment.lifetime
                    if lifetime is None:
                        msg = (
                            "You have to specify a lifetime "
                            "for a Flow with an associated "
                            "investment object in "
                            f"a multi-period model! Value for {(g)} "
                            "is missing."
                        )
                        raise ValueError(msg)

                    # get the period matrix describing the temporal distance
                    # between all period combinations.
                    periods_matrix = m.es.periods_matrix

                    # get the index of the minimum value in each row greater
                    # equal than the lifetime. This value equals the
                    # decommissioning period if not zero. The index of this
                    # value represents the investment period. If np.where
                    # condition is not met in any row, min value will be zero
                    decomm_periods = np.argmin(
                        np.where(
                            (periods_matrix >= lifetime),
                            periods_matrix,
                            np.inf,
                        ),
                        axis=1,
                    )

                    # no decommissioning in first period
                    expr = self.old_end[g, 0] == 0
                    self.old_dsm_rule_end.add((g, 0), expr)

                    # all periods not in decomm_periods have no decommissioning
                    # zero is excluded
                    for p in m.PERIODS:
                        if p not in decomm_periods and p != 0:
                            expr = self.old_end[g, p] == 0
                            self.old_dsm_rule_end.add((g, p), expr)

                    # multiple invests can be decommissioned in the same period
                    # but only sequential ones, thus a bookkeeping is
                    # introduced andconstraints are added to equation one
                    # iteration later.
                    last_decomm_p = np.nan
                    # loop over invest periods (values are decomm_periods)
                    for invest_p, decomm_p in enumerate(decomm_periods):
                        # Add constraint of iteration before
                        # (skipped in first iteration by last_decomm_p = nan)
                        if (decomm_p != last_decomm_p) and (
                            last_decomm_p is not np.nan
                        ):
                            expr = self.old_end[g, last_decomm_p] == expr
                            self.old_dsm_rule_end.add((g, last_decomm_p), expr)

                        # no decommissioning if decomm_p is zero
                        if decomm_p == 0:
                            # overwrite decomm_p with zero to avoid
                            # chaining invest periods in next iteration
                            last_decomm_p = 0

                        # if decomm_p is the same as the last one chain invest
                        # period
                        elif decomm_p == last_decomm_p:
                            expr += self.invest[g, invest_p]
                            # overwrite decomm_p
                            last_decomm_p = decomm_p

                        # if decomm_p is not zero, not the same as the last one
                        # and it's not the first period
                        else:
                            expr = self.invest[g, invest_p]
                            # overwrite decomm_p
                            last_decomm_p = decomm_p

                    # Add constraint of very last iteration
                    if last_decomm_p != 0:
                        expr = self.old_end[g, last_decomm_p] == expr
                        self.old_dsm_rule_end.add((g, last_decomm_p), expr)

            self.old_dsm_rule_end = Constraint(
                group, m.PERIODS, noruleinit=True
            )
            self.old_dsm_rule_end_build = BuildAction(
                rule=_old_dsm_capacity_rule_end
            )

            def _old_dsm_capacity_rule_exo(block):
                """Rule definition for determining old exogenously given
                capacity to be decommissioned due to reaching its lifetime
                """
                for g in group:
                    age = g.investment.age
                    lifetime = g.investment.lifetime
                    is_decommissioned = False
                    for p in m.PERIODS:
                        # No shutdown in first period
                        if p == 0:
                            expr = self.old_exo[g, p] == 0
                            self.old_dsm_rule_exo.add((g, p), expr)
                        elif lifetime - age <= m.es.periods_years[p]:
                            # Track decommissioning status
                            if not is_decommissioned:
                                expr = (
                                    self.old_exo[g, p] == g.investment.existing
                                )
                                is_decommissioned = True
                            else:
                                expr = self.old_exo[g, p] == 0
                            self.old_dsm_rule_exo.add((g, p), expr)
                        else:
                            expr = self.old_exo[g, p] == 0
                            self.old_dsm_rule_exo.add((g, p), expr)

            self.old_dsm_rule_exo = Constraint(
                group, m.PERIODS, noruleinit=True
            )
            self.old_dsm_rule_exo_build = BuildAction(
                rule=_old_dsm_capacity_rule_exo
            )

            def _old_dsm_capacity_rule(block):
                """Rule definition for determining (overall) old capacity
                to be decommissioned due to reaching its lifetime
                """
                for g in group:
                    for p in m.PERIODS:
                        expr = (
                            self.old[g, p]
                            == self.old_end[g, p] + self.old_exo[g, p]
                        )
                        self.old_dsm_rule.add((g, p), expr)

            self.old_dsm_rule = Constraint(group, m.PERIODS, noruleinit=True)
            self.old_dsm_rule_build = BuildAction(rule=_old_dsm_capacity_rule)

        def _shift_shed_vars_rule(block):
            """Force shifting resp. shedding variables to zero dependent
            on how boolean parameters for shift resp. shed eligibility
            are set.
            """
            for t in m.TIMESTEPS:
                for g in group:
                    if not g.shift_eligibility:
                        lhs = self.dsm_up[g, t]
                        rhs = 0

                        block.shift_shed_vars.add((g, t), (lhs == rhs))

                    if not g.shed_eligibility:
                        lhs = self.dsm_do_shed[g, t]
                        rhs = 0

                        block.shift_shed_vars.add((g, t), (lhs == rhs))

        self.shift_shed_vars = Constraint(group, m.TIMESTEPS, noruleinit=True)
        self.shift_shed_vars_build = BuildAction(rule=_shift_shed_vars_rule)

        # Demand Production Relation
        def _input_output_relation_rule(block):
            """Relation between input data and pyomo variables.
            The actual demand after DSM.
            Generator Production == Demand_el +- DSM
            """
            for p, t in m.TIMEINDEX:
                for g in group:
                    # Inflow from bus
                    lhs = m.flow[g.inflow, g, t]

                    # Demand + DSM_up - DSM_down
                    rhs = (
                        g.demand[t] * g.max_demand[p]
                        + self.dsm_up[g, t]
                        - self.dsm_do_shift[g, t]
                        - self.dsm_do_shed[g, t]
                    )

                    # add constraint
                    block.input_output_relation.add((g, p, t), (lhs == rhs))

        self.input_output_relation = Constraint(
            group, m.TIMEINDEX, noruleinit=True
        )
        self.input_output_relation_build = BuildAction(
            rule=_input_output_relation_rule
        )

        # Upper bounds relation
        def dsm_up_constraint_rule(block):
            """Realised upward load shift at time t has to be smaller than
            upward DSM capacity at time t.
            """
            for p, t in m.TIMEINDEX:
                for g in group:
                    # DSM up
                    lhs = self.dsm_up[g, t]
                    # Capacity dsm_up
                    rhs = g.capacity_up[t] * self.total[g, p]

                    # add constraint
                    block.dsm_up_constraint.add((g, p, t), (lhs <= rhs))

        self.dsm_up_constraint = Constraint(
            group, m.TIMEINDEX, noruleinit=True
        )
        self.dsm_up_constraint_build = BuildAction(rule=dsm_up_constraint_rule)

        # Upper bounds relation
        def dsm_down_constraint_rule(block):
            """Realised downward load shift at time t has to be smaller than
            downward DSM capacity at time t.
            """
            for p, t in m.TIMEINDEX:
                for g in group:
                    # DSM down
                    lhs = self.dsm_do_shift[g, t] + self.dsm_do_shed[g, t]
                    # Capacity dsm_down
                    rhs = g.capacity_down[t] * self.total[g, p]

                    # add constraint
                    block.dsm_down_constraint.add((g, p, t), (lhs <= rhs))

        self.dsm_down_constraint = Constraint(
            group, m.TIMEINDEX, noruleinit=True
        )
        self.dsm_down_constraint_build = BuildAction(
            rule=dsm_down_constraint_rule
        )

        def dsm_sum_constraint_rule(block):
            """Relation to compensate the total amount of positive
            and negative DSM in between the shift_interval.
            This constraint is building balance in full intervals starting
            with index 0. The last interval might not be full.
            """
            for g in group:
                intervals = range(
                    m.TIMESTEPS.at(1), m.TIMESTEPS.at(-1), g.shift_interval
                )

                for interval in intervals:
                    if (interval + g.shift_interval - 1) > m.TIMESTEPS.at(-1):
                        timesteps = range(interval, m.TIMESTEPS.at(-1) + 1)
                    else:
                        timesteps = range(
                            interval, interval + g.shift_interval
                        )

                    # DSM up/down
                    lhs = (
                        sum(self.dsm_up[g, tt] for tt in timesteps)
                        * g.efficiency
                    )
                    # value
                    rhs = sum(self.dsm_do_shift[g, tt] for tt in timesteps)

                    # add constraint
                    block.dsm_sum_constraint.add((g, interval), (lhs == rhs))

        self.dsm_sum_constraint = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.dsm_sum_constraint_build = BuildAction(
            rule=dsm_sum_constraint_rule
        )

        if m.es.periods is not None:

            def _overall_dsm_maximum_investflow_rule(block):
                """Rule definition for maximum overall investment
                in investment case.
                """
                for g in self.OVERALL_MAXIMUM_INVESTDSM:
                    for p in m.PERIODS:
                        expr = self.total[g, p] <= g.investment.overall_maximum
                        self.overall_dsm_maximum.add((g, p), expr)

            self.overall_dsm_maximum = Constraint(
                self.OVERALL_MAXIMUM_INVESTDSM, m.PERIODS, noruleinit=True
            )

            self.overall_maximum_build = BuildAction(
                rule=_overall_dsm_maximum_investflow_rule
            )

            def _overall_minimum_dsm_investflow_rule(block):
                """Rule definition for minimum overall investment
                in investment case.

                Note: This is only applicable for the last period
                """
                for g in self.OVERALL_MINIMUM_INVESTDSM:
                    expr = (
                        g.investment.overall_minimum
                        <= self.total[g, m.PERIODS.at(-1)]
                    )
                    self.overall_minimum.add(g, expr)

            self.overall_minimum = Constraint(
                self.OVERALL_MINIMUM_INVESTDSM, noruleinit=True
            )

            self.overall_minimum_build = BuildAction(
                rule=_overall_minimum_dsm_investflow_rule
            )

    def _objective_expression(self):
        r"""Objective expression with variable and investment costs for DSM"""

        m = self.parent_block()

        investment_costs = 0
        period_investment_costs = {p: 0 for p in m.PERIODS}
        variable_costs = 0
        fixed_costs = 0

        if m.es.periods is None:
            for g in self.investdsm:
                for p in m.PERIODS:
                    if g.investment.ep_costs is not None:
                        investment_costs += (
                            self.invest[g, p] * g.investment.ep_costs[p]
                        )
                    else:
                        raise ValueError("Missing value for investment costs!")

                for t in m.TIMESTEPS:
                    variable_costs += (
                        self.dsm_up[g, t]
                        * g.cost_dsm_up[t]
                        * m.objective_weighting[t]
                    )
                    variable_costs += (
                        self.dsm_do_shift[g, t] * g.cost_dsm_down_shift[t]
                        + self.dsm_do_shed[g, t] * g.cost_dsm_down_shed[t]
                    ) * m.objective_weighting[t]

        else:
            msg = (
                "You did not specify an interest rate.\n"
                "It will be set equal to the discount_rate of {} "
                "of the model as a default.\nThis corresponds to a "
                "social planner point of view and does not reflect "
                "microeconomic interest requirements."
            )
            for g in self.investdsm:
                if g.investment.ep_costs is not None:
                    lifetime = g.investment.lifetime
                    interest = 0
                    if interest == 0:
                        warn(
                            msg.format(m.discount_rate),
                            debugging.SuspiciousUsageWarning,
                        )
                        interest = m.discount_rate
                    for p in m.PERIODS:
                        annuity = economics.annuity(
                            capex=g.investment.ep_costs[p],
                            n=lifetime,
                            wacc=interest,
                        )
                        duration = min(
                            m.es.end_year_of_optimization
                            - m.es.periods_years[p],
                            lifetime,
                        )
                        present_value_factor = 1 / economics.annuity(
                            capex=1, n=duration, wacc=interest
                        )
                        investment_costs_increment = (
                            self.invest[g, p] * annuity * present_value_factor
                        )
                        remaining_value_difference = (
                            self._evaluate_remaining_value_difference(
                                m,
                                p,
                                g,
                                m.es.end_year_of_optimization,
                                lifetime,
                                interest,
                            )
                        )
                        investment_costs += (
                            investment_costs_increment
                            + remaining_value_difference
                        )
                        period_investment_costs[
                            p
                        ] += investment_costs_increment
                else:
                    raise ValueError("Missing value for investment costs!")

                for p, t in m.TIMEINDEX:
                    variable_costs += (
                        self.dsm_up[g, t]
                        * m.objective_weighting[t]
                        * g.cost_dsm_up[t]
                    )
                    variable_costs += (
                        self.dsm_do_shift[g, t] * g.cost_dsm_down_shift[t]
                        + self.dsm_do_shed[g, t] * g.cost_dsm_down_shed[t]
                    ) * m.objective_weighting[t]

                if valid_sequence(g.investment.fixed_costs, len(m.PERIODS)):
                    lifetime = g.investment.lifetime
                    for p in m.PERIODS:
                        range_limit = min(
                            m.es.end_year_of_optimization,
                            m.es.periods_years[p] + lifetime,
                        )
                        fixed_costs += sum(
                            self.invest[g, p] * g.investment.fixed_costs[pp]
                            for pp in range(
                                m.es.periods_years[p],
                                range_limit,
                            )
                        )

            for g in self.EXISTING_INVESTDSM:
                if valid_sequence(g.investment.fixed_costs, len(m.PERIODS)):
                    lifetime = g.investment.lifetime
                    age = g.investment.age
                    range_limit = min(
                        m.es.end_year_of_optimization, lifetime - age
                    )
                    fixed_costs += sum(
                        g.investment.existing * g.investment.fixed_costs[pp]
                        for pp in range(range_limit)
                    )

        self.variable_costs = Expression(expr=variable_costs)
        self.fixed_costs = Expression(expr=fixed_costs)
        self.investment_costs = Expression(expr=investment_costs)
        self.period_investment_costs = period_investment_costs
        self.costs = Expression(
            expr=investment_costs + variable_costs + fixed_costs
        )

        return self.costs

    def _evaluate_remaining_value_difference(
        self,
        m,
        p,
        g,
        end_year_of_optimization,
        lifetime,
        interest,
    ):
        """Evaluate and return the remaining value difference of an investment

        The remaining value difference in the net present values if the asset
        was to be liquidated at the end of the optimization horizon and the
        net present value using the original investment expenses.

        Parameters
        ----------
        m : oemof.solph.models.Model
            Optimization model

        p : int
            Period in which investment occurs

        g : oemof.solph.components.experimental.SinkDSM
            storage unit

        end_year_of_optimization : int
            Last year of the optimization horizon

        lifetime : int
            lifetime of investment considered

        interest : float
            Demanded interest rate for investment
        """
        if m.es.use_remaining_value:
            if end_year_of_optimization - m.es.periods_years[p] < lifetime:
                remaining_lifetime = lifetime - (
                    end_year_of_optimization - m.es.periods_years[p]
                )
                remaining_annuity = economics.annuity(
                    capex=g.investment.ep_costs[-1],
                    n=remaining_lifetime,
                    wacc=interest,
                )
                original_annuity = economics.annuity(
                    capex=g.investment.ep_costs[p],
                    n=remaining_lifetime,
                    wacc=interest,
                )
                present_value_factor_remaining = 1 / economics.annuity(
                    capex=1, n=remaining_lifetime, wacc=interest
                )
                return (
                    self.invest[g, p]
                    * (remaining_annuity - original_annuity)
                    * present_value_factor_remaining
                )
            else:
                return 0
        else:
            return 0


class SinkDSMDIWBlock(ScalarBlock):
    r"""Constraints for SinkDSM with "DIW" approach

    **The following constraints are created for approach = "DIW":**

    .. _SinkDSMDIWBlock equations:

    .. math::
        &
        (1) \quad DSM_{t}^{up} = 0 \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T}
        \quad \textrm{if} \quad e_{shift} = \textrm{False} \\
        & \\
        &
        (2) \quad DSM_{t}^{do, shed} = 0 \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T}
        \quad \textrm{if} \quad e_{shed} = \textrm{False} \\
        & \\
        &
        (3) \quad \dot{E}_{t} = demand_{t} \cdot demand_{max} + DSM_{t}^{up} -
        \sum_{tt=t-L}^{t+L} DSM_{tt,t}^{do, shift} - DSM_{t}^{do, shed} \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T} \\
        & \\
        &
        (4) \quad DSM_{t}^{up} \cdot \eta =
        \sum_{tt=t-L}^{t+L} DSM_{t,tt}^{do, shift} \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T} \\
        & \\
        &
        (5) \quad DSM_{t}^{up} \leq E_{t}^{up} \cdot E_{up, max} \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T} \\
        & \\
        &
        (6) \quad \sum_{t=tt-L}^{tt+L} DSM_{t,tt}^{do, shift}
        + DSM_{tt}^{do, shed} \leq E_{tt}^{do} \cdot E_{do, max} \\
        & \quad \quad \quad \quad \forall tt \in \mathbb{T} \\
        & \\
        &
        (7) \quad DSM_{tt}^{up} + \sum_{t=tt-L}^{tt+L} DSM_{t,tt}^{do, shift}
        + DSM_{tt}^{do, shed} \leq
        max \{ E_{tt}^{up} \cdot E_{up, max},
        E_{tt}^{do} \cdot E_{do, max} \} \\
        & \quad \quad \quad \quad \forall tt \in \mathbb{T} \\
        & \\
        &
        (8) \quad \sum_{tt=t}^{t+R_{shi}-1} DSM_{tt}^{up}
        \leq E_{t}^{up} \cdot E_{up, max} \cdot L \cdot \Delta t \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T} \\
        & \\
        &
        (9) \quad \sum_{tt=t}^{t+R_{she}-1} DSM_{tt}^{do, shed}
        \leq E_{t}^{do} \cdot E_{do, max} \cdot t_{shed} \cdot \Delta t \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T} \\


    Note
    ----

    For the sake of readability, the handling of indices is not
    displayed here. E.g. evaluating a variable for `t-L` may lead to a negative
    and therefore infeasible index.
    This is addressed by limiting the sums to non-negative indices within the
    model index bounds. Please refer to the constraints implementation
    themselves.


    **The following parts of the objective function are created:**

    .. math::
        &
        DSM_{t}^{up} \cdot cost_{t}^{dsm, up}
        + (\sum_{tt=0}^{|T|} DSM_{tt, t}^{do, shift} \cdot
        cost_{t}^{dsm, do, shift}
        + DSM_{t}^{do, shed} \cdot cost_{t}^{dsm, do, shed})
        \cdot \omega_{t} \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T} \\

    * :attr:`fixed_costs` not None

    .. math::
        \displaystyle \sum_{pp=0}^{year_{max}} max\{E_{up, max}, E_{do, max}\}
        \cdot c_{fixed}(pp) \cdot DF^{-pp}

    **Table: Symbols and attribute names of variables and parameters**

    .. table:: Variables (V), Parameters (P) and Sets (S)
        :widths: 25, 25, 10, 40

        ================================= ======================== ==== =======================================
        symbol                            attribute                type explanation
        ================================= ======================== ==== =======================================
        :math:`DSM_{t}^{up}`              `dsm_up[g, t]`           V    DSM up shift (additional load) in hour t
        :math:`DSM_{t, tt}^{do, shift}`   `dsm_do_shift[g, t, tt]` V    | DSM down shift (less load) in hour tt
                                                                        | to compensate for upwards shifts in hour t
        :math:`DSM_{t}^{do, shed}`        `dsm_do_shed[g, t]`      V    DSM shedded (capacity shedded, i.e. not compensated for)
        :math:`\dot{E}_{t}`               `SinkDSM.inputs`         V    Energy flowing in from (electrical) inflow bus
        :math:`L`                         `delay_time`             P    | Maximum delay time for load shift
                                                                        | (time until the energy balance has to be levelled out again;
                                                                        | roundtrip time of one load shifting cycle, i.e. time window
                                                                        | for upshift and compensating downshift)
        :math:`t_{she}`                   `shed_time`              P    Maximum time for one load shedding process
        :math:`demand_{t}`                `demand[t]`              P    (Electrical) demand series (normalized)
        :math:`demand_{max}`              `max_demand`             P    Maximum demand value
        :math:`E_{t}^{do}`                `capacity_down[t]`       P    | Capacity  allowed for a load adjustment downwards
                                                                        | (normalized; shifting + shedding)
        :math:`E_{t}^{up}`                `capacity_up[t]`         P    Capacity allowed for a shift upwards (normalized)
        :math:`E_{do, max}`               `max_capacity_down`      P    | Maximum capacity allowed for a load adjustment downwards
                                                                        | (shifting + shedding)
        :math:`E_{up, max}`               `max_capacity_up`        P    Maximum capacity allowed for a shift upwards
        :math:`\eta`                      `efficiency`             P    Efficiency for load shifting processes
        :math:`\mathbb{T}`                                         S    Time steps of the model
        :math:`e_{shift}`                 `shift_eligibility`      P    | Boolean parameter indicating if unit can be used
                                                                        | for load shifting
        :math:`e_{shed}`                  `shed_eligibility`       P    | Boolean parameter indicating if unit can be used
                                                                        | for load shedding
        :math:`cost_{t}^{dsm, up}`        `cost_dsm_up[t]`         P    Variable costs for an upwards shift
        :math:`cost_{t}^{dsm, do, shift}` `cost_dsm_down_shift[t]` P    Variable costs for a downwards shift (load shifting)
        :math:`cost_{t}^{dsm, do, shed}`  `cost_dsm_down_shift[t]` P    Variable costs for shedding load
        :math:`\omega_{t}`                                         P    Objective weighting of the model for timestep t
        :math:`R_{shi}`                   `recovery_time_shift`    P    | Minimum time between the end of one load shifting process
                                                                        | and the start of another
        :math:`R_{she}`                   `recovery_time_shed`     P    | Minimum time between the end of one load shedding process
                                                                        | and the start of another
        :math:`\Delta t`                                           P    The time increment of the model
        :math:`\omega_{t}`                                         P    Objective weighting of the model for timestep t
        :math:`year_{max}`                                         P    Last year of the optimization horizon
        ================================= ======================== ==== =======================================

    """  # noqa E:501

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        if group is None:
            return None

        m = self.parent_block()

        # for all DSM components get inflow from a bus
        for n in group:
            n.inflow = list(n.inputs)[0]

        #  ************* SETS *********************************

        # Set of DSM Components
        self.dsm = Set(initialize=[g for g in group])

        #  ************* VARIABLES *****************************

        # Variable load shift down
        self.dsm_do_shift = Var(
            self.dsm,
            m.TIMESTEPS,
            m.TIMESTEPS,
            initialize=0,
            within=NonNegativeReals,
        )

        # Variable load shedding
        self.dsm_do_shed = Var(
            self.dsm, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        # Variable load shift up
        self.dsm_up = Var(
            self.dsm, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        #  ************* CONSTRAINTS *****************************

        def _shift_shed_vars_rule(block):
            """Force shifting resp. shedding variables to zero dependent
            on how boolean parameters for shift resp. shed eligibility
            are set.
            """
            for t in m.TIMESTEPS:
                for g in group:
                    if not g.shift_eligibility:
                        lhs = self.dsm_up[g, t]
                        rhs = 0

                        block.shift_shed_vars.add((g, t), (lhs == rhs))

                    if not g.shed_eligibility:
                        lhs = self.dsm_do_shed[g, t]
                        rhs = 0

                        block.shift_shed_vars.add((g, t), (lhs == rhs))

        self.shift_shed_vars = Constraint(group, m.TIMESTEPS, noruleinit=True)
        self.shift_shed_vars_build = BuildAction(rule=_shift_shed_vars_rule)

        # Demand Production Relation
        def _input_output_relation_rule(block):
            """Relation between input data and pyomo variables.
            The actual demand after DSM.
            Sink Inflow == Demand +- DSM
            """
            for p, t in m.TIMEINDEX:
                for g in group:
                    # first time steps: 0 + delay time
                    if t <= g.delay_time:
                        # Inflow from bus
                        lhs = m.flow[g.inflow, g, t]
                        # Demand +- DSM
                        rhs = (
                            g.demand[t] * g.max_demand[p]
                            + self.dsm_up[g, t]
                            - sum(
                                self.dsm_do_shift[g, tt, t]
                                for tt in range(t + g.delay_time + 1)
                            )
                            - self.dsm_do_shed[g, t]
                        )

                        # add constraint
                        block.input_output_relation.add(
                            (g, p, t), (lhs == rhs)
                        )

                    # main use case
                    elif g.delay_time < t <= m.TIMESTEPS.at(-1) - g.delay_time:
                        # Inflow from bus
                        lhs = m.flow[g.inflow, g, t]
                        # Demand +- DSM
                        rhs = (
                            g.demand[t] * g.max_demand[p]
                            + self.dsm_up[g, t]
                            - sum(
                                self.dsm_do_shift[g, tt, t]
                                for tt in range(
                                    t - g.delay_time, t + g.delay_time + 1
                                )
                            )
                            - self.dsm_do_shed[g, t]
                        )

                        # add constraint
                        block.input_output_relation.add(
                            (g, p, t), (lhs == rhs)
                        )

                    # last time steps: end - delay time
                    else:
                        # Inflow from bus
                        lhs = m.flow[g.inflow, g, t]
                        # Demand +- DSM
                        rhs = (
                            g.demand[t] * g.max_demand[p]
                            + self.dsm_up[g, t]
                            - sum(
                                self.dsm_do_shift[g, tt, t]
                                for tt in range(
                                    t - g.delay_time, m.TIMESTEPS.at(-1) + 1
                                )
                            )
                            - self.dsm_do_shed[g, t]
                        )

                        # add constraint
                        block.input_output_relation.add(
                            (g, p, t), (lhs == rhs)
                        )

        self.input_output_relation = Constraint(
            group, m.TIMEINDEX, noruleinit=True
        )
        self.input_output_relation_build = BuildAction(
            rule=_input_output_relation_rule
        )

        # Equation 7 (resp. 7')
        def dsm_up_down_constraint_rule(block):
            """Equation 7 (resp. 7') by Zerrahn & Schill:
            Every upward load shift has to be compensated by downward load
            shifts in a defined time frame. Slightly modified equations for
            the first and last time steps due to variable initialization.
            Efficiency value depicts possible energy losses through
            load shifting (Equation 7').
            """
            for t in m.TIMESTEPS:
                for g in group:
                    # first time steps: 0 + delay time
                    if t <= g.delay_time:
                        # DSM up
                        lhs = self.dsm_up[g, t] * g.efficiency
                        # DSM down
                        rhs = sum(
                            self.dsm_do_shift[g, t, tt]
                            for tt in range(t + g.delay_time + 1)
                        )

                        # add constraint
                        block.dsm_updo_constraint.add((g, t), (lhs == rhs))

                    # main use case
                    elif g.delay_time < t <= m.TIMESTEPS.at(-1) - g.delay_time:
                        # DSM up
                        lhs = self.dsm_up[g, t] * g.efficiency
                        # DSM down
                        rhs = sum(
                            self.dsm_do_shift[g, t, tt]
                            for tt in range(
                                t - g.delay_time, t + g.delay_time + 1
                            )
                        )

                        # add constraint
                        block.dsm_updo_constraint.add((g, t), (lhs == rhs))

                    # last time steps: end - delay time
                    else:
                        # DSM up
                        lhs = self.dsm_up[g, t] * g.efficiency
                        # DSM down
                        rhs = sum(
                            self.dsm_do_shift[g, t, tt]
                            for tt in range(
                                t - g.delay_time, m.TIMESTEPS.at(-1) + 1
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
            """Equation 8 by Zerrahn & Schill:
            Realised upward load shift at time t has to be smaller than
            upward DSM capacity at time t.
            """
            for t in m.TIMESTEPS:
                for g in group:
                    # DSM up
                    lhs = self.dsm_up[g, t]
                    # Capacity dsm_up
                    rhs = g.capacity_up[t] * g.max_capacity_up

                    # add constraint
                    block.dsm_up_constraint.add((g, t), (lhs <= rhs))

        self.dsm_up_constraint = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.dsm_up_constraint_build = BuildAction(rule=dsm_up_constraint_rule)

        # Equation 9 (modified)
        def dsm_do_constraint_rule(block):
            """Equation 9 by Zerrahn & Schill:
            Realised downward load shift at time t has to be smaller than
            downward DSM capacity at time t.
            """
            for tt in m.TIMESTEPS:
                for g in group:
                    # first times steps: 0 + delay
                    if tt <= g.delay_time:
                        # DSM down
                        lhs = (
                            sum(
                                self.dsm_do_shift[g, t, tt]
                                for t in range(tt + g.delay_time + 1)
                            )
                            + self.dsm_do_shed[g, tt]
                        )
                        # Capacity DSM down
                        rhs = g.capacity_down[tt] * g.max_capacity_down

                        # add constraint
                        block.dsm_do_constraint.add((g, tt), (lhs <= rhs))

                    # main use case
                    elif (
                        g.delay_time < tt <= m.TIMESTEPS.at(-1) - g.delay_time
                    ):
                        # DSM down
                        lhs = (
                            sum(
                                self.dsm_do_shift[g, t, tt]
                                for t in range(
                                    tt - g.delay_time, tt + g.delay_time + 1
                                )
                            )
                            + self.dsm_do_shed[g, tt]
                        )
                        # Capacity DSM down
                        rhs = g.capacity_down[tt] * g.max_capacity_down

                        # add constraint
                        block.dsm_do_constraint.add((g, tt), (lhs <= rhs))

                    # last time steps: end - delay time
                    else:
                        # DSM down
                        lhs = (
                            sum(
                                self.dsm_do_shift[g, t, tt]
                                for t in range(
                                    tt - g.delay_time, m.TIMESTEPS.at(-1) + 1
                                )
                            )
                            + self.dsm_do_shed[g, tt]
                        )
                        # Capacity DSM down
                        rhs = g.capacity_down[tt] * g.max_capacity_down

                        # add constraint
                        block.dsm_do_constraint.add((g, tt), (lhs <= rhs))

        self.dsm_do_constraint = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.dsm_do_constraint_build = BuildAction(rule=dsm_do_constraint_rule)

        # Equation 10
        def c2_constraint_rule(block):
            """Equation 10 by Zerrahn & Schill:
            The realised DSM up or down at time T has to be smaller than
            the maximum downward or upward capacity at time T. Therefore, in
            total each individual DSM unit within the modeled portfolio
            can only be shifted up OR down at a given time.
            """
            for tt in m.TIMESTEPS:
                for g in group:
                    # first times steps: 0 + delay time
                    if tt <= g.delay_time:
                        # DSM up/down
                        lhs = (
                            self.dsm_up[g, tt]
                            + sum(
                                self.dsm_do_shift[g, t, tt]
                                for t in range(tt + g.delay_time + 1)
                            )
                            + self.dsm_do_shed[g, tt]
                        )
                        # max capacity at tt
                        rhs = max(
                            g.capacity_up[tt] * g.max_capacity_up,
                            g.capacity_down[tt] * g.max_capacity_down,
                        )

                        # add constraint
                        block.C2_constraint.add((g, tt), (lhs <= rhs))

                    elif (
                        g.delay_time < tt <= m.TIMESTEPS.at(-1) - g.delay_time
                    ):
                        # DSM up/down
                        lhs = (
                            self.dsm_up[g, tt]
                            + sum(
                                self.dsm_do_shift[g, t, tt]
                                for t in range(
                                    tt - g.delay_time, tt + g.delay_time + 1
                                )
                            )
                            + self.dsm_do_shed[g, tt]
                        )
                        # max capacity at tt
                        rhs = max(
                            g.capacity_up[tt] * g.max_capacity_up,
                            g.capacity_down[tt] * g.max_capacity_down,
                        )

                        # add constraint
                        block.C2_constraint.add((g, tt), (lhs <= rhs))

                    else:
                        # DSM up/down
                        lhs = (
                            self.dsm_up[g, tt]
                            + sum(
                                self.dsm_do_shift[g, t, tt]
                                for t in range(
                                    tt - g.delay_time, m.TIMESTEPS.at(-1) + 1
                                )
                            )
                            + self.dsm_do_shed[g, tt]
                        )
                        # max capacity at tt
                        rhs = max(
                            g.capacity_up[tt] * g.max_capacity_up,
                            g.capacity_down[tt] * g.max_capacity_down,
                        )

                        # add constraint
                        block.C2_constraint.add((g, tt), (lhs <= rhs))

        self.C2_constraint = Constraint(group, m.TIMESTEPS, noruleinit=True)
        self.C2_constraint_build = BuildAction(rule=c2_constraint_rule)

        def recovery_constraint_rule(block):
            """Equation 11 by Zerrahn & Schill:
            A recovery time is introduced to account for the fact that
            there may be some restrictions before the next load shift
            may take place. Rule is only applicable if a recovery time
            is defined.
            """
            for t in m.TIMESTEPS:
                for g in group:
                    # No need to build constraint if no recovery
                    # time is defined.
                    if g.recovery_time_shift not in [None, 0]:
                        # main use case
                        if t <= m.TIMESTEPS.at(-1) - g.recovery_time_shift:
                            # DSM up
                            lhs = sum(
                                self.dsm_up[g, tt]
                                for tt in range(t, t + g.recovery_time_shift)
                            )
                            # max energy shift for shifting process
                            rhs = (
                                g.capacity_up[t]
                                * g.max_capacity_up
                                * g.delay_time
                                * m.timeincrement[t]
                            )
                            # add constraint
                            block.recovery_constraint.add((g, t), (lhs <= rhs))

                        # last time steps: end - recovery time
                        else:
                            # DSM up
                            lhs = sum(
                                self.dsm_up[g, tt]
                                for tt in range(t, m.TIMESTEPS.at(-1) + 1)
                            )
                            # max energy shift for shifting process
                            rhs = (
                                g.capacity_up[t]
                                * g.max_capacity_up
                                * g.delay_time
                                * m.timeincrement[t]
                            )
                            # add constraint
                            block.recovery_constraint.add((g, t), (lhs <= rhs))

                    else:
                        pass  # return(Constraint.Skip)

        self.recovery_constraint = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.recovery_constraint_build = BuildAction(
            rule=recovery_constraint_rule
        )

        # Equation 9a from Zerrahn and Schill (2015b)
        def shed_limit_constraint_rule(block):
            """The following constraint is highly similar to equation 9a
            from Zerrahn and Schill (2015b): A recovery time for load
            shedding is introduced in order to limit the overall amount
            of shedded energy.
            """
            for t in m.TIMESTEPS:
                for g in group:
                    # Only applicable for load shedding
                    if g.shed_eligibility:
                        # main use case
                        if t <= m.TIMESTEPS.at(-1) - g.recovery_time_shed:
                            # DSM up
                            lhs = sum(
                                self.dsm_do_shed[g, tt]
                                for tt in range(t, t + g.recovery_time_shed)
                            )
                            # max energy shift for shifting process
                            rhs = (
                                g.capacity_down[t]
                                * g.max_capacity_down
                                * g.shed_time
                                * m.timeincrement[t]
                            )
                            # add constraint
                            block.shed_limit_constraint.add(
                                (g, t), (lhs <= rhs)
                            )

                        # last time steps: end - recovery time
                        else:
                            # DSM up
                            lhs = sum(
                                self.dsm_do_shed[g, tt]
                                for tt in range(t, m.TIMESTEPS.at(-1) + 1)
                            )
                            # max energy shift for shifting process
                            rhs = (
                                g.capacity_down[t]
                                * g.max_capacity_down
                                * g.shed_time
                                * m.timeincrement[t]
                            )
                            # add constraint
                            block.shed_limit_constraint.add(
                                (g, t), (lhs <= rhs)
                            )

                    else:
                        pass  # return(Constraint.Skip)

        self.shed_limit_constraint = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.shed_limit_constraint_build = BuildAction(
            rule=shed_limit_constraint_rule
        )

    def _objective_expression(self):
        r"""Objective expression with variable costs for DSM activity"""

        m = self.parent_block()

        variable_costs = 0
        fixed_costs = 0

        if m.es.periods is None:
            for t in m.TIMESTEPS:
                for g in self.dsm:
                    variable_costs += (
                        self.dsm_up[g, t]
                        * g.cost_dsm_up[t]
                        * m.objective_weighting[t]
                    )
                    variable_costs += (
                        sum(self.dsm_do_shift[g, tt, t] for tt in m.TIMESTEPS)
                        * g.cost_dsm_down_shift[t]
                        + self.dsm_do_shed[g, t] * g.cost_dsm_down_shed[t]
                    ) * m.objective_weighting[t]

        else:
            for g in self.dsm:
                for p, t in m.TIMEINDEX:
                    variable_costs += (
                        self.dsm_up[g, t]
                        * m.objective_weighting[t]
                        * g.cost_dsm_up[t]
                    )
                    variable_costs += (
                        sum(self.dsm_do_shift[g, tt, t] for tt in m.TIMESTEPS)
                        * g.cost_dsm_down_shift[t]
                        + self.dsm_do_shed[g, t] * g.cost_dsm_down_shed[t]
                    ) * m.objective_weighting[t]

                if valid_sequence(g.fixed_costs, len(m.PERIODS)):
                    fixed_costs += sum(
                        max(g.max_capacity_up, g.max_capacity_down)
                        * g.fixed_costs[pp]
                        for pp in range(m.es.end_year_of_optimization)
                    )

        self.variable_costs = Expression(expr=variable_costs)
        self.fixed_costs = Expression(expr=fixed_costs)
        self.costs = Expression(expr=variable_costs + fixed_costs)

        return self.costs


class SinkDSMDIWInvestmentBlock(ScalarBlock):
    r"""Constraints for SinkDSM with "DIW" approach and `investment` defined

    **The following constraints are created for approach = "DIW" with an
    investment object defined:**

    .. _SinkDSMDIWInvestmentBlock equations:

    .. math::
        &
        (1) \quad invest_{min}(p) \leq invest(p) \leq invest_{max}(p) \\
        & \quad \quad \quad \quad \forall p \in \mathbb{P}
        & \\
        &
        (2) \quad DSM_{t}^{up} = 0 \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T}
        \quad \textrm{if} \quad e_{shift} = \textrm{False} \\
        & \\
        &
        (3) \quad DSM_{t}^{do, shed} = 0 \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T}
        \quad \textrm{if} \quad e_{shed} = \textrm{False} \\
        & \\
        &
        (4) \quad \dot{E}_{t} = demand_{t} \cdot demand_{max}(p)
        + DSM_{t}^{up} -
        \sum_{tt=t-L}^{t+L} DSM_{tt,t}^{do, shift} - DSM_{t}^{do, shed} \\
        & \quad \quad \quad \quad \forall p, t \in \textrm{TIMEINDEX} \\
        & \\
        &
        (5) \quad DSM_{t}^{up} \cdot \eta =
        \sum_{tt=t-L}^{t+L} DSM_{t,tt}^{do, shift} \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T} \\
        & \\
        &
        (6) \quad DSM_{t}^{up} \leq E_{t}^{up} \cdot P_{total}(p) \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T} \\
        & \\
        &
        (7) \quad \sum_{t=tt-L}^{tt+L} DSM_{t,tt}^{do, shift}
        + DSM_{tt}^{do, shed} \leq E_{tt}^{do} \cdot P_{total}(p) \\
        & \quad \quad \quad \quad \forall p, t \in \textrm{TIMEINDEX} \\
        & \\
        &
        (8) \quad DSM_{tt}^{up} + \sum_{t=tt-L}^{tt+L} DSM_{t,tt}^{do, shift}
        + DSM_{tt}^{do, shed} \\
        & \quad \quad \leq max \{ E_{tt}^{up}, E_{tt}^{do} \}
        \cdot P_{total}(p) \\
        & \quad \quad \quad \quad \forall p, t \in \textrm{TIMEINDEX} \\
        & \\
        &
        (9) \quad \sum_{tt=t}^{t+R-1} DSM_{tt}^{up}
        \leq E_{t}^{up} \cdot P_{total}(p)
        \cdot L \cdot \Delta t \\
        & \quad \quad \quad \quad \forall p, t \in \textrm{TIMEINDEX} \\
        & \quad \quad \quad \quad \forall p, t \in \textrm{TIMEINDEX} \\
        & \\
        &
        (10) \quad \sum_{tt=t}^{t+R-1} DSM_{tt}^{do, shed}
        \leq E_{t}^{do} \cdot P_{total}(p)
        \cdot t_{shed}
        \cdot \Delta t \\
        & \quad \quad \quad \quad \forall p, t \in \textrm{TIMEINDEX} \\

    Note
    ----

    For the sake of readability, the handling of indices is not
    displayed here. E.g. evaluating a variable for `t-L` may lead to a negative
    and therefore infeasible index.
    This is addressed by limiting the sums to non-negative indices within the
    model index bounds. Please refer to the constraints implementation
    themselves.


    **The following parts of the objective function are created:**

    *Standard model*

        * Investment annuity:

            .. math::
                P_{invest}(0) \cdot c_{invest}(0)

        * Variable costs:

            .. math::
                &
                (DSM_{t}^{up} \cdot cost_{t}^{dsm, up}
                + DSM_{t}^{do, shift} \cdot cost_{t}^{dsm, do, shift} \\
                & + DSM_{t}^{do, shed} \cdot cost_{t}^{dsm, do, shed})
                \cdot \omega_{t} \\
                & \quad \quad \quad \quad \forall t \in \mathbb{T} \\

    *Multi-period model*

        * Investment annuity:

            .. math::
                &
                P_{invest}(p) \cdot A(c_{invest}(p), l, ir)
                \frac {1}{ANF(d, ir)} \cdot DF^{-p} \\
                &\\
                & \quad \quad \quad \quad \forall p \in \mathbb{P}

        In case, the remaining lifetime of a DSM unit is greater than 0 and
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

        * :attr:`fixed_costs` not None for investments

            .. math::
                &
                (\sum_{pp=year(p)}^{limit_{end}}
                P_{invest}(p) \cdot c_{fixed}(pp) \cdot DF^{-pp})
                \cdot DF^{-p} \\
                &\\
                & \quad \quad \quad \quad \forall p \in \mathbb{P}

        * Variable costs:

            .. math::
                &
                (DSM_{t}^{up} \cdot cost_{t}^{dsm, up}
                + DSM_{t}^{do, shift} \cdot cost_{t}^{dsm, do, shift} \\
                & + DSM_{t}^{do, shed} \cdot cost_{t}^{dsm, do, shed})
                \cdot \omega_{t}
                \cdot DF^{-p} \\
                & \quad \quad \quad \quad
                \forall p, t \in \textrm{TIMEINDEX} \\

    where:

    * :math:`A(c_{invest,var}(p), l, ir)` A is the annuity for
      investment expenses :math:`c_{invest,var}(p)`, lifetime :math:`l`
      and interest rate :math:`ir`.
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
    * :math:`DF=(1+dr)` is the discount factor.

    The annuity / annuity factor hereby is:

        .. math::
            &
            A(c_{invest,var}(p), l, ir) = c_{invest,var}(p) \cdot
                \frac {(1+ir)^l \cdot ir} {(1+ir)^l - 1}\\
            &\\
            &
            ANF(d, ir)=\frac {(1+dr)^d \cdot dr} {(1+dr)^d - 1}

    They are retrieved, using oemof.tools.economics annuity function. The
    interest rate :math:`ir` for the annuity is defined as weighted
    average costs of capital (wacc) and assumed constant over time.

    See remarks in
    :class:`oemof.solph.components.experimental._sink_dsm.SinkDSMOemofBlock`.


    **Table: Symbols and attribute names of variables and parameters**

    * Please refer to
      :class:`oemof.solph.components.experimental._sink_dsm.SinkDSMDIWBlock`
      for a variables and parameter description.
    * The following variables and parameters are exclusively used for
      investment modeling:

    .. table:: Variables (V), Parameters (P) and Sets (S)
        :widths: 25, 25, 10, 40

        ================================= ======================== ==== =======================================
        symbol                            attribute                type explanation
        ================================= ======================== ==== =======================================
        :math:`P_{invest}(p)`             `invest[p]`              V    | DSM capacity invested into in period p.
                                                                        | Equals to the additionally shiftable resp. sheddable capacity.
        :math:`invest_{min}(p)`           `investment.minimum[p]`  P    minimum investment in period p
        :math:`invest_{max}(p)`           `investment.maximum[p]`  P    maximum investment in period p
        :math:`P_{total}`                 `investment.total[p]`    P    total DSM capacity
        :math:`costs_{invest}(p)`         `investment.ep_costs[p]` P    | specific investment annuity (standard model) resp.
                                                                        | specific investment expenses (multi-period model)
        :math:`\mathbb{P}`                                         S    Periods of the model
        :math:`\textrm{TIMEINDEX}`                                 S    Timeindex set of the model (periods, timesteps)
        ================================= ======================== ==== =======================================

    """  # noqa: E501

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        if group is None:
            return None

        m = self.parent_block()

        # for all DSM components get inflow from a bus
        for n in group:
            n.inflow = list(n.inputs)[0]

        #  ************* SETS *********************************

        # Set of DSM Components
        self.investdsm = Set(initialize=[g for g in group])

        self.OVERALL_MAXIMUM_INVESTDSM = Set(
            initialize=[
                g for g in group if g.investment.overall_maximum is not None
            ]
        )

        self.OVERALL_MINIMUM_INVESTDSM = Set(
            initialize=[
                g for g in group if g.investment.overall_minimum is not None
            ]
        )

        self.EXISTING_INVESTDSM = Set(
            initialize=[g for g in group if g.investment.existing is not None]
        )

        #  ************* VARIABLES *****************************

        # Define bounds for investments in demand response
        def _dsm_investvar_bound_rule(block, g, p):
            """Rule definition to bound the
            demand response capacity invested in (`invest`).
            """
            return g.investment.minimum[p], g.investment.maximum[p]

        # Investment in DR capacity
        self.invest = Var(
            self.investdsm,
            m.PERIODS,
            within=NonNegativeReals,
            bounds=_dsm_investvar_bound_rule,
        )

        # Total capacity
        self.total = Var(self.investdsm, m.PERIODS, within=NonNegativeReals)

        if m.es.periods is not None:
            # Old capacity to be decommissioned (due to lifetime)
            # Old capacity built out of old exogenous and endogenous capacities
            self.old = Var(self.investdsm, m.PERIODS, within=NonNegativeReals)

            # Old endogenous capacity to be decommissioned (due to lifetime)
            self.old_end = Var(
                self.investdsm, m.PERIODS, within=NonNegativeReals
            )

            # Old exogenous capacity to be decommissioned (due to lifetime)
            self.old_exo = Var(
                self.investdsm, m.PERIODS, within=NonNegativeReals
            )

        # Variable load shift down
        self.dsm_do_shift = Var(
            self.investdsm,
            m.TIMESTEPS,
            m.TIMESTEPS,
            initialize=0,
            within=NonNegativeReals,
        )

        # Variable load shedding
        self.dsm_do_shed = Var(
            self.investdsm, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        # Variable load shift up
        self.dsm_up = Var(
            self.investdsm, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        #  ************* CONSTRAINTS *****************************

        # Handle unit lifetimes
        def _total_dsm_capacity_rule(block):
            """Rule definition for determining total installed
            capacity (taking decommissioning into account)
            """
            for g in group:
                for p in m.PERIODS:
                    if p == 0:
                        expr = (
                            self.total[g, p]
                            == self.invest[g, p] + g.investment.existing
                        )
                        self.total_dsm_rule.add((g, p), expr)
                    else:
                        expr = (
                            self.total[g, p]
                            == self.invest[g, p]
                            + self.total[g, p - 1]
                            - self.old[g, p]
                        )
                        self.total_dsm_rule.add((g, p), expr)

        self.total_dsm_rule = Constraint(group, m.PERIODS, noruleinit=True)
        self.total_dsm_rule_build = BuildAction(rule=_total_dsm_capacity_rule)

        if m.es.periods is not None:

            def _old_dsm_capacity_rule_end(block):
                """Rule definition for determining old endogenously installed
                capacity to be decommissioned due to reaching its lifetime.
                Investment and decommissioning periods are linked within
                the constraint. The respective decommissioning period is
                determined for every investment period based on the components
                lifetime and a matrix describing its age of each endogenous
                investment. Decommissioning can only occur at the beginning of
                each period.

                Note
                ----
                For further information on the implementation check
                PR#957 https://github.com/oemof/oemof-solph/pull/957
                """
                for g in group:
                    lifetime = g.investment.lifetime
                    if lifetime is None:
                        msg = (
                            "You have to specify a lifetime "
                            "for a Flow with an associated "
                            "investment object in "
                            f"a multi-period model! Value for {g} "
                            "is missing."
                        )
                        raise ValueError(msg)
                    # get the period matrix describing the temporal distance
                    # between all period combinations.
                    periods_matrix = m.es.periods_matrix

                    # get the index of the minimum value in each row greater
                    # equal than the lifetime. This value equals the
                    # decommissioning period if not zero. The index of this
                    # value represents the investment period. If np.where
                    # condition is not met in any row, min value will be zero
                    decomm_periods = np.argmin(
                        np.where(
                            (periods_matrix >= lifetime),
                            periods_matrix,
                            np.inf,
                        ),
                        axis=1,
                    )

                    # no decommissioning in first period
                    expr = self.old_end[g, 0] == 0
                    self.old_dsm_rule_end.add((g, 0), expr)

                    # all periods not in decomm_periods have no decommissioning
                    # zero is excluded
                    for p in m.PERIODS:
                        if p not in decomm_periods and p != 0:
                            expr = self.old_end[g, p] == 0
                            self.old_dsm_rule_end.add((g, p), expr)

                    # multiple invests can be decommissioned in the same period
                    # but only sequential ones, thus a bookkeeping is
                    # introduced andconstraints are added to equation one
                    # iteration later.
                    last_decomm_p = np.nan
                    # loop over invest periods (values are decomm_periods)
                    for invest_p, decomm_p in enumerate(decomm_periods):
                        # Add constraint of iteration before
                        # (skipped in first iteration by last_decomm_p = nan)
                        if (decomm_p != last_decomm_p) and (
                            last_decomm_p is not np.nan
                        ):
                            expr = self.old_end[g, last_decomm_p] == expr
                            self.old_dsm_rule_end.add((g, last_decomm_p), expr)

                        # no decommissioning if decomm_p is zero
                        if decomm_p == 0:
                            # overwrite decomm_p with zero to avoid
                            # chaining invest periods in next iteration
                            last_decomm_p = 0

                        # if decomm_p is the same as the last one chain invest
                        # period
                        elif decomm_p == last_decomm_p:
                            expr += self.invest[g, invest_p]
                            # overwrite decomm_p
                            last_decomm_p = decomm_p

                        # if decomm_p is not zero, not the same as the last one
                        # and it's not the first period
                        else:
                            expr = self.invest[g, invest_p]
                            # overwrite decomm_p
                            last_decomm_p = decomm_p

                    # Add constraint of very last iteration
                    if last_decomm_p != 0:
                        expr = self.old_end[g, last_decomm_p] == expr
                        self.old_dsm_rule_end.add((g, last_decomm_p), expr)

            self.old_dsm_rule_end = Constraint(
                group, m.PERIODS, noruleinit=True
            )
            self.old_dsm_rule_end_build = BuildAction(
                rule=_old_dsm_capacity_rule_end
            )

            def _old_dsm_capacity_rule_exo(block):
                """Rule definition for determining old exogenously given
                capacity to be decommissioned due to reaching its lifetime
                """
                for g in group:
                    age = g.investment.age
                    lifetime = g.investment.lifetime
                    is_decommissioned = False
                    for p in m.PERIODS:
                        # No shutdown in first period
                        if p == 0:
                            expr = self.old_exo[g, p] == 0
                            self.old_dsm_rule_exo.add((g, p), expr)
                        elif lifetime - age <= m.es.periods_years[p]:
                            # Track decommissioning status
                            if not is_decommissioned:
                                expr = (
                                    self.old_exo[g, p] == g.investment.existing
                                )
                                is_decommissioned = True
                            else:
                                expr = self.old_exo[g, p] == 0
                            self.old_dsm_rule_exo.add((g, p), expr)
                        else:
                            expr = self.old_exo[g, p] == 0
                            self.old_dsm_rule_exo.add((g, p), expr)

            self.old_dsm_rule_exo = Constraint(
                group, m.PERIODS, noruleinit=True
            )
            self.old_dsm_rule_exo_build = BuildAction(
                rule=_old_dsm_capacity_rule_exo
            )

            def _old_dsm_capacity_rule(block):
                """Rule definition for determining (overall) old capacity
                to be decommissioned due to reaching its lifetime
                """
                for g in group:
                    for p in m.PERIODS:
                        expr = (
                            self.old[g, p]
                            == self.old_end[g, p] + self.old_exo[g, p]
                        )
                        self.old_dsm_rule.add((g, p), expr)

            self.old_dsm_rule = Constraint(group, m.PERIODS, noruleinit=True)
            self.old_dsm_rule_build = BuildAction(rule=_old_dsm_capacity_rule)

        def _shift_shed_vars_rule(block):
            """Force shifting resp. shedding variables to zero dependent
            on how boolean parameters for shift resp. shed eligibility
            are set.
            """
            for t in m.TIMESTEPS:
                for g in group:
                    if not g.shift_eligibility:
                        lhs = self.dsm_up[g, t]
                        rhs = 0

                        block.shift_shed_vars.add((g, t), (lhs == rhs))

                    if not g.shed_eligibility:
                        lhs = self.dsm_do_shed[g, t]
                        rhs = 0

                        block.shift_shed_vars.add((g, t), (lhs == rhs))

        self.shift_shed_vars = Constraint(group, m.TIMESTEPS, noruleinit=True)
        self.shift_shed_vars_build = BuildAction(rule=_shift_shed_vars_rule)

        # Demand Production Relation
        def _input_output_relation_rule(block):
            """Relation between input data and pyomo variables.
            The actual demand after DSM.
            Sink Inflow == Demand +- DSM
            """
            for p, t in m.TIMEINDEX:
                for g in group:
                    # first time steps: 0 + delay time
                    if t <= g.delay_time:
                        # Inflow from bus
                        lhs = m.flow[g.inflow, g, t]
                        # Demand +- DSM
                        rhs = (
                            g.demand[t] * g.max_demand[p]
                            + self.dsm_up[g, t]
                            - sum(
                                self.dsm_do_shift[g, tt, t]
                                for tt in range(t + g.delay_time + 1)
                            )
                            - self.dsm_do_shed[g, t]
                        )

                        # add constraint
                        block.input_output_relation.add(
                            (g, p, t), (lhs == rhs)
                        )

                    # main use case
                    elif g.delay_time < t <= m.TIMESTEPS.at(-1) - g.delay_time:
                        # Inflow from bus
                        lhs = m.flow[g.inflow, g, t]
                        # Demand +- DSM
                        rhs = (
                            g.demand[t] * g.max_demand[p]
                            + self.dsm_up[g, t]
                            - sum(
                                self.dsm_do_shift[g, tt, t]
                                for tt in range(
                                    t - g.delay_time, t + g.delay_time + 1
                                )
                            )
                            - self.dsm_do_shed[g, t]
                        )

                        # add constraint
                        block.input_output_relation.add(
                            (g, p, t), (lhs == rhs)
                        )

                    # last time steps: end - delay time
                    else:
                        # Inflow from bus
                        lhs = m.flow[g.inflow, g, t]
                        # Demand +- DSM
                        rhs = (
                            g.demand[t] * g.max_demand[p]
                            + self.dsm_up[g, t]
                            - sum(
                                self.dsm_do_shift[g, tt, t]
                                for tt in range(
                                    t - g.delay_time, m.TIMESTEPS.at(-1) + 1
                                )
                            )
                            - self.dsm_do_shed[g, t]
                        )

                        # add constraint
                        block.input_output_relation.add(
                            (g, p, t), (lhs == rhs)
                        )

        self.input_output_relation = Constraint(
            group, m.TIMEINDEX, noruleinit=True
        )
        self.input_output_relation_build = BuildAction(
            rule=_input_output_relation_rule
        )

        # Equation 7 (resp. 7')
        def dsm_up_down_constraint_rule(block):
            """Equation 7 (resp. 7') by Zerrahn & Schill:
            Every upward load shift has to be compensated by downward load
            shifts in a defined time frame. Slightly modified equations for
            the first and last time steps due to variable initialization.
            Efficiency value depicts possible energy losses through
            load shifting (Equation 7').
            """
            for t in m.TIMESTEPS:
                for g in group:
                    # first time steps: 0 + delay time
                    if t <= g.delay_time:
                        # DSM up
                        lhs = self.dsm_up[g, t] * g.efficiency
                        # DSM down
                        rhs = sum(
                            self.dsm_do_shift[g, t, tt]
                            for tt in range(t + g.delay_time + 1)
                        )

                        # add constraint
                        block.dsm_updo_constraint.add((g, t), (lhs == rhs))

                    # main use case
                    elif g.delay_time < t <= m.TIMESTEPS.at(-1) - g.delay_time:
                        # DSM up
                        lhs = self.dsm_up[g, t] * g.efficiency
                        # DSM down
                        rhs = sum(
                            self.dsm_do_shift[g, t, tt]
                            for tt in range(
                                t - g.delay_time, t + g.delay_time + 1
                            )
                        )

                        # add constraint
                        block.dsm_updo_constraint.add((g, t), (lhs == rhs))

                    # last time steps: end - delay time
                    else:
                        # DSM up
                        lhs = self.dsm_up[g, t] * g.efficiency
                        # DSM down
                        rhs = sum(
                            self.dsm_do_shift[g, t, tt]
                            for tt in range(
                                t - g.delay_time, m.TIMESTEPS.at(-1) + 1
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
            """Equation 8 by Zerrahn & Schill:
            Realised upward load shift at time t has to be smaller than
            upward DSM capacity at time t.
            """
            for p, t in m.TIMEINDEX:
                for g in group:
                    # DSM up
                    lhs = self.dsm_up[g, t]
                    # Capacity dsm_up
                    rhs = g.capacity_up[t] * self.total[g, p]

                    # add constraint
                    block.dsm_up_constraint.add((g, p, t), (lhs <= rhs))

        self.dsm_up_constraint = Constraint(
            group, m.TIMEINDEX, noruleinit=True
        )
        self.dsm_up_constraint_build = BuildAction(rule=dsm_up_constraint_rule)

        # Equation 9 (modified)
        def dsm_do_constraint_rule(block):
            """Equation 9 by Zerrahn & Schill:
            Realised downward load shift at time t has to be smaller than
            downward DSM capacity at time t.
            """
            for p, tt in m.TIMEINDEX:
                for g in group:
                    # first times steps: 0 + delay
                    if tt <= g.delay_time:
                        # DSM down
                        lhs = (
                            sum(
                                self.dsm_do_shift[g, t, tt]
                                for t in range(tt + g.delay_time + 1)
                            )
                            + self.dsm_do_shed[g, tt]
                        )
                        # Capacity DSM down
                        rhs = g.capacity_down[tt] * self.total[g, p]

                        # add constraint
                        block.dsm_do_constraint.add((g, p, tt), (lhs <= rhs))

                    # main use case
                    elif (
                        g.delay_time < tt <= m.TIMESTEPS.at(-1) - g.delay_time
                    ):
                        # DSM down
                        lhs = (
                            sum(
                                self.dsm_do_shift[g, t, tt]
                                for t in range(
                                    tt - g.delay_time, tt + g.delay_time + 1
                                )
                            )
                            + self.dsm_do_shed[g, tt]
                        )
                        # Capacity DSM down
                        rhs = g.capacity_down[tt] * self.total[g, p]

                        # add constraint
                        block.dsm_do_constraint.add((g, p, tt), (lhs <= rhs))

                    # last time steps: end - delay time
                    else:
                        # DSM down
                        lhs = (
                            sum(
                                self.dsm_do_shift[g, t, tt]
                                for t in range(
                                    tt - g.delay_time, m.TIMESTEPS.at(-1) + 1
                                )
                            )
                            + self.dsm_do_shed[g, tt]
                        )
                        # Capacity DSM down
                        rhs = g.capacity_down[tt] * self.total[g, p]

                        # add constraint
                        block.dsm_do_constraint.add((g, p, tt), (lhs <= rhs))

        self.dsm_do_constraint = Constraint(
            group, m.TIMEINDEX, noruleinit=True
        )
        self.dsm_do_constraint_build = BuildAction(rule=dsm_do_constraint_rule)

        # Equation 10
        def c2_constraint_rule(block):
            """Equation 10 by Zerrahn & Schill:
            The realised DSM up or down at time T has to be smaller than
            the maximum downward or upward capacity at time T. Therefore, in
            total each individual DSM unit within the modeled portfolio
            can only be shifted up OR down at a given time.
            """
            for p, tt in m.TIMEINDEX:
                for g in group:
                    # first times steps: 0 + delay time
                    if tt <= g.delay_time:
                        # DSM up/down
                        lhs = (
                            self.dsm_up[g, tt]
                            + sum(
                                self.dsm_do_shift[g, t, tt]
                                for t in range(tt + g.delay_time + 1)
                            )
                            + self.dsm_do_shed[g, tt]
                        )
                        # max capacity at tt
                        rhs = (
                            max(
                                g.capacity_up[tt],
                                g.capacity_down[tt],
                            )
                            * self.total[g, p]
                        )

                        # add constraint
                        block.C2_constraint.add((g, p, tt), (lhs <= rhs))

                    elif (
                        g.delay_time < tt <= m.TIMESTEPS.at(-1) - g.delay_time
                    ):
                        # DSM up/down
                        lhs = (
                            self.dsm_up[g, tt]
                            + sum(
                                self.dsm_do_shift[g, t, tt]
                                for t in range(
                                    tt - g.delay_time, tt + g.delay_time + 1
                                )
                            )
                            + self.dsm_do_shed[g, tt]
                        )
                        # max capacity at tt
                        rhs = (
                            max(
                                g.capacity_up[tt],
                                g.capacity_down[tt],
                            )
                            * self.total[g, p]
                        )

                        # add constraint
                        block.C2_constraint.add((g, p, tt), (lhs <= rhs))

                    else:
                        # DSM up/down
                        lhs = (
                            self.dsm_up[g, tt]
                            + sum(
                                self.dsm_do_shift[g, t, tt]
                                for t in range(
                                    tt - g.delay_time, m.TIMESTEPS.at(-1) + 1
                                )
                            )
                            + self.dsm_do_shed[g, tt]
                        )
                        # max capacity at tt
                        rhs = (
                            max(
                                g.capacity_up[tt],
                                g.capacity_down[tt],
                            )
                            * self.total[g, p]
                        )

                        # add constraint
                        block.C2_constraint.add((g, p, tt), (lhs <= rhs))

        self.C2_constraint = Constraint(group, m.TIMEINDEX, noruleinit=True)
        self.C2_constraint_build = BuildAction(rule=c2_constraint_rule)

        def recovery_constraint_rule(block):
            """Equation 11 by Zerrahn & Schill:
            A recovery time is introduced to account for the fact that
            there may be some restrictions before the next load shift
            may take place. Rule is only applicable if a recovery time
            is defined.
            """
            for p, t in m.TIMEINDEX:
                for g in group:
                    # No need to build constraint if no recovery
                    # time is defined.
                    if g.recovery_time_shift not in [None, 0]:
                        # main use case
                        if t <= m.TIMESTEPS.at(-1) - g.recovery_time_shift:
                            # DSM up
                            lhs = sum(
                                self.dsm_up[g, tt]
                                for tt in range(t, t + g.recovery_time_shift)
                            )
                            # max energy shift for shifting process
                            rhs = (
                                g.capacity_up[t]
                                * self.total[g, p]
                                * g.delay_time
                                * m.timeincrement[t]
                            )
                            # add constraint
                            block.recovery_constraint.add(
                                (g, p, t), (lhs <= rhs)
                            )

                        # last time steps: end - recovery time
                        else:
                            # DSM up
                            lhs = sum(
                                self.dsm_up[g, tt]
                                for tt in range(t, m.TIMESTEPS.at(-1) + 1)
                            )
                            # max energy shift for shifting process
                            rhs = (
                                g.capacity_up[t]
                                * self.total[g, p]
                                * g.delay_time
                                * m.timeincrement[t]
                            )
                            # add constraint
                            block.recovery_constraint.add(
                                (g, p, t), (lhs <= rhs)
                            )

                    else:
                        pass  # return(Constraint.Skip)

        self.recovery_constraint = Constraint(
            group, m.TIMEINDEX, noruleinit=True
        )
        self.recovery_constraint_build = BuildAction(
            rule=recovery_constraint_rule
        )

        # Equation 9a from Zerrahn and Schill (2015b)
        def shed_limit_constraint_rule(block):
            """The following constraint is highly similar to equation 9a
            from Zerrahn and Schill (2015b): A recovery time for load
            shedding is introduced in order to limit the overall amount
            of shedded energy.
            """
            for p, t in m.TIMEINDEX:
                for g in group:
                    # Only applicable for load shedding
                    if g.shed_eligibility:
                        # main use case
                        if t <= m.TIMESTEPS.at(-1) - g.recovery_time_shed:
                            # DSM up
                            lhs = sum(
                                self.dsm_do_shed[g, tt]
                                for tt in range(t, t + g.recovery_time_shed)
                            )
                            # max energy shift for shifting process
                            rhs = (
                                g.capacity_down[t]
                                * self.total[g, p]
                                * g.shed_time
                                * m.timeincrement[t]
                            )
                            # add constraint
                            block.shed_limit_constraint.add(
                                (g, p, t), (lhs <= rhs)
                            )

                        # last time steps: end - recovery time
                        else:
                            # DSM up
                            lhs = sum(
                                self.dsm_do_shed[g, tt]
                                for tt in range(t, m.TIMESTEPS.at(-1) + 1)
                            )
                            # max energy shift for shifting process
                            rhs = (
                                g.capacity_down[t]
                                * self.total[g, p]
                                * g.shed_time
                                * m.timeincrement[t]
                            )
                            # add constraint
                            block.shed_limit_constraint.add(
                                (g, p, t), (lhs <= rhs)
                            )

                    else:
                        pass  # return(Constraint.Skip)

        self.shed_limit_constraint = Constraint(
            group, m.TIMEINDEX, noruleinit=True
        )
        self.shed_limit_constraint_build = BuildAction(
            rule=shed_limit_constraint_rule
        )

        if m.es.periods is not None:

            def _overall_dsm_maximum_investflow_rule(block):
                """Rule definition for maximum overall investment
                in investment case.
                """
                for g in self.OVERALL_MAXIMUM_INVESTDSM:
                    for p in m.PERIODS:
                        expr = self.total[g, p] <= g.investment.overall_maximum
                        self.overall_dsm_maximum.add((g, p), expr)

            self.overall_dsm_maximum = Constraint(
                self.OVERALL_MAXIMUM_INVESTDSM, m.PERIODS, noruleinit=True
            )

            self.overall_maximum_build = BuildAction(
                rule=_overall_dsm_maximum_investflow_rule
            )

            def _overall_minimum_dsm_investflow_rule(block):
                """Rule definition for minimum overall investment
                in investment case.

                Note: This is only applicable for the last period
                """
                for g in self.OVERALL_MINIMUM_INVESTDSM:
                    expr = (
                        g.investment.overall_minimum
                        <= self.total[g, m.PERIODS.at(-1)]
                    )
                    self.overall_minimum.add(g, expr)

            self.overall_minimum = Constraint(
                self.OVERALL_MINIMUM_INVESTDSM, noruleinit=True
            )

            self.overall_minimum_build = BuildAction(
                rule=_overall_minimum_dsm_investflow_rule
            )

    def _objective_expression(self):
        r"""Objective expression with variable and investment costs for DSM"""

        m = self.parent_block()

        investment_costs = 0
        period_investment_costs = {p: 0 for p in m.PERIODS}
        variable_costs = 0
        fixed_costs = 0

        if m.es.periods is None:
            for g in self.investdsm:
                for p in m.PERIODS:
                    if g.investment.ep_costs is not None:
                        investment_costs += (
                            self.invest[g, p] * g.investment.ep_costs[p]
                        )
                    else:
                        raise ValueError("Missing value for investment costs!")

                for t in m.TIMESTEPS:
                    variable_costs += (
                        self.dsm_up[g, t]
                        * g.cost_dsm_up[t]
                        * m.objective_weighting[t]
                    )
                    variable_costs += (
                        sum(self.dsm_do_shift[g, tt, t] for tt in m.TIMESTEPS)
                        * g.cost_dsm_down_shift[t]
                        + self.dsm_do_shed[g, t] * g.cost_dsm_down_shed[t]
                    ) * m.objective_weighting[t]

        else:
            msg = (
                "You did not specify an interest rate.\n"
                "It will be set equal to the discount_rate of {} "
                "of the model as a default.\nThis corresponds to a "
                "social planner point of view and does not reflect "
                "microeconomic interest requirements."
            )
            for g in self.investdsm:
                if g.investment.ep_costs is not None:
                    lifetime = g.investment.lifetime
                    interest = 0
                    if interest == 0:
                        warn(
                            msg.format(m.discount_rate),
                            debugging.SuspiciousUsageWarning,
                        )
                        interest = m.discount_rate
                    for p in m.PERIODS:
                        annuity = economics.annuity(
                            capex=g.investment.ep_costs[p],
                            n=lifetime,
                            wacc=interest,
                        )
                        duration = min(
                            m.es.end_year_of_optimization
                            - m.es.periods_years[p],
                            lifetime,
                        )
                        present_value_factor = 1 / economics.annuity(
                            capex=1, n=duration, wacc=interest
                        )
                        investment_costs_increment = (
                            self.invest[g, p] * annuity * present_value_factor
                        )
                        remaining_value_difference = (
                            self._evaluate_remaining_value_difference(
                                m,
                                p,
                                g,
                                m.es.end_year_of_optimization,
                                lifetime,
                                interest,
                            )
                        )
                        investment_costs += (
                            investment_costs_increment
                            + remaining_value_difference
                        )
                        period_investment_costs[
                            p
                        ] += investment_costs_increment
                else:
                    raise ValueError("Missing value for investment costs!")

                for p, t in m.TIMEINDEX:
                    variable_costs += (
                        self.dsm_up[g, t]
                        * m.objective_weighting[t]
                        * g.cost_dsm_up[t]
                    )
                    variable_costs += (
                        sum(self.dsm_do_shift[g, tt, t] for tt in m.TIMESTEPS)
                        * g.cost_dsm_down_shift[t]
                        + self.dsm_do_shed[g, t] * g.cost_dsm_down_shed[t]
                    ) * m.objective_weighting[t]

                if valid_sequence(g.investment.fixed_costs, len(m.PERIODS)):
                    lifetime = g.investment.lifetime
                    for p in m.PERIODS:
                        range_limit = min(
                            m.es.end_year_of_optimization,
                            m.es.periods_years[p] + lifetime,
                        )
                        fixed_costs += sum(
                            self.invest[g, p] * g.investment.fixed_costs[pp]
                            for pp in range(
                                m.es.periods_years[p],
                                range_limit,
                            )
                        )

            for g in self.EXISTING_INVESTDSM:
                if valid_sequence(g.investment.fixed_costs, len(m.PERIODS)):
                    lifetime = g.investment.lifetime
                    age = g.investment.age
                    range_limit = min(
                        m.es.end_year_of_optimization, lifetime - age
                    )
                    fixed_costs += sum(
                        g.investment.existing * g.investment.fixed_costs[pp]
                        for pp in range(range_limit)
                    )

        self.variable_costs = Expression(expr=variable_costs)
        self.fixed_costs = Expression(expr=fixed_costs)
        self.investment_costs = Expression(expr=investment_costs)
        self.period_investment_costs = period_investment_costs
        self.costs = Expression(
            expr=investment_costs + variable_costs + fixed_costs
        )

        return self.costs

    def _evaluate_remaining_value_difference(
        self,
        m,
        p,
        g,
        end_year_of_optimization,
        lifetime,
        interest,
    ):
        """Evaluate and return the remaining value difference of an investment

        The remaining value difference in the net present values if the asset
        was to be liquidated at the end of the optimization horizon and the
        net present value using the original investment expenses.

        Parameters
        ----------
        m : oemof.solph.models.Model
            Optimization model

        p : int
            Period in which investment occurs

        g : oemof.solph.components.experimental.SinkDSM
            storage unit

        end_year_of_optimization : int
            Last year of the optimization horizon

        lifetime : int
            lifetime of investment considered

        interest : float
            Demanded interest rate for investment
        """
        if m.es.use_remaining_value:
            if end_year_of_optimization - m.es.periods_years[p] < lifetime:
                remaining_lifetime = lifetime - (
                    end_year_of_optimization - m.es.periods_years[p]
                )
                remaining_annuity = economics.annuity(
                    capex=g.investment.ep_costs[-1],
                    n=remaining_lifetime,
                    wacc=interest,
                )
                original_annuity = economics.annuity(
                    capex=g.investment.ep_costs[p],
                    n=remaining_lifetime,
                    wacc=interest,
                )
                present_value_factor_remaining = 1 / economics.annuity(
                    capex=1, n=remaining_lifetime, wacc=interest
                )
                return (
                    self.invest[g, p]
                    * (remaining_annuity - original_annuity)
                    * present_value_factor_remaining
                )
            else:
                return 0
        else:
            return 0


class SinkDSMDLRBlock(ScalarBlock):
    r"""Constraints for SinkDSM with "DLR" approach

    **The following constraints are created for approach = "DLR":**

    .. _SinkDSMDLRBlock equations:

    .. math::
        &
        (1) \quad DSM_{h, t}^{up} = 0 \\
        & \quad \quad \quad \quad \forall h \in H_{DR}, t \in \mathbb{T}
        \quad \textrm{if} \quad e_{shift} = \textrm{False} \\
        & \\
        &
        (2) \quad DSM_{t}^{do, shed} = 0 \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T}
        \quad \textrm{if} \quad e_{shed} = \textrm{False} \\
        & \\
        &
        (3) \quad \dot{E}_{t} = demand_{t} \cdot demand_{max} \\
        & \quad \quad \quad \quad + \displaystyle\sum_{h=1}^{H_{DR}}
        (DSM_{h, t}^{up}
        + DSM_{h, t}^{balanceDo} - DSM_{h, t}^{do, shift}
        - DSM_{h, t}^{balanceUp}) - DSM_{t}^{do, shed} \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T} \\
        & \\
        &
        (4) \quad DSM_{h, t}^{balanceDo} =
        \frac{DSM_{h, t - h}^{do, shift}}{\eta} \\
        & \quad \quad \quad \quad \forall h \in H_{DR}, t \in [h..T] \\
        & \\
        &
        (5) \quad DSM_{h, t}^{balanceUp} =
        DSM_{h, t-h}^{up} \cdot \eta \\
        & \quad \quad \quad \quad \forall h \in H_{DR}, t \in [h..T] \\
        & \\
        &
        (6) \quad DSM_{h, t}^{do, shift} = 0
        \quad \forall h \in H_{DR} \\
        & \quad \quad \quad \quad \forall t \in [T - h..T] \\
        & \\
        &
        (7) \quad DSM_{h, t}^{up} = 0
        \quad \forall h \in H_{DR}  \\
        & \quad \quad \quad \quad \forall t \in [T - h..T] \\
        & \\
        &
        (8) \quad \displaystyle\sum_{h=1}^{H_{DR}} (DSM_{h, t}^{do, shift}
        + DSM_{h, t}^{balanceUp}) + DSM_{t}^{do, shed}
        \leq E_{t}^{do} \cdot E_{max, do} \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T} \\
        & \\
        &
        (9) \quad \displaystyle\sum_{h=1}^{H_{DR}} (DSM_{h, t}^{up}
        + DSM_{h, t}^{balanceDo})
        \leq E_{t}^{up} \cdot E_{max, up} \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T} \\
        & \\
        &
        (10) \quad \Delta t \cdot \displaystyle\sum_{h=1}^{H_{DR}}
        (DSM_{h, t}^{do, shift} - DSM_{h, t}^{balanceDo} \cdot \eta)
        = W_{t}^{levelDo} - W_{t-1}^{levelDo} \\
        & \quad \quad \quad \quad  \forall t \in [1..T] \\
        & \\
        &
        (11) \quad \Delta t \cdot \displaystyle\sum_{h=1}^{H_{DR}}
        (DSM_{h, t}^{up} \cdot \eta - DSM_{h, t}^{balanceUp})
        = W_{t}^{levelUp} - W_{t-1}^{levelUp} \\
        & \quad \quad \quad \quad  \forall t \in [1..T] \\
        & \\
        &
        (12) \quad W_{t}^{levelDo} \leq \overline{E}_{t}^{do}
        \cdot E_{max, do} \cdot t_{shift} \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T} \\
        & \\
        &
        (13) \quad W_{t}^{levelUp} \leq \overline{E}_{t}^{up}
        \cdot E_{max, up} \cdot t_{shift} \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T} \\
        & \\
        &
        (14) \quad \displaystyle\sum_{t=0}^{T} DSM_{t}^{do, shed}
        \leq E_{max, do} \cdot \overline{E}_{t}^{do} \cdot t_{shed}
        \cdot n^{yearLimitShed} \\
        & \\
        &
        (15) \quad \displaystyle\sum_{t=0}^{T} \sum_{h=1}^{H_{DR}}
        DSM_{h, t}^{do, shift}
        \leq E_{max, do} \cdot \overline{E}_{t}^{do} \cdot t_{shift}
        \cdot n^{yearLimitShift} \\
        & \quad \quad \textrm{(optional constraint)} \\
        & \\
        &
        (16) \quad \displaystyle\sum_{t=0}^{T} \sum_{h=1}^{H_{DR}}
        DSM_{h, t}^{up}
        \leq E_{max, up} \cdot \overline{E}_{t}^{up} \cdot t_{shift}
        \cdot n^{yearLimitShift} \\
        & \quad \quad \textrm{(optional constraint)} \\
        & \\
        &
        (17) \quad \displaystyle\sum_{h=1}^{H_{DR}} DSM_{h, t}^{do, shift}
        \leq E_{max, do} \cdot \overline{E}_{t}^{do}
        \cdot t_{shift} -
        \displaystyle\sum_{t'=1}^{t_{dayLimit}} \sum_{h=1}^{H_{DR}}
        DSM_{h, t - t'}^{do, shift} \\
        & \quad \quad \quad \quad \forall t \in [t-t_{dayLimit}..T] \\
        & \quad \quad \textrm{(optional constraint)} \\
        & \\
        &
        (18) \quad \displaystyle\sum_{h=1}^{H_{DR}} DSM_{h, t}^{up}
        \leq E_{max, up} \cdot \overline{E}_{t}^{up}
        \cdot t_{shift} -
        \displaystyle\sum_{t'=1}^{t_{dayLimit}} \sum_{h=1}^{H_{DR}}
        DSM_{h, t - t'}^{up} \\
        & \quad \quad \quad \quad \forall t \in [t-t_{dayLimit}..T] \\
        & \quad \quad \textrm{(optional constraint)}  \\
        & \\
        &
        (19) \quad \displaystyle\sum_{h=1}^{H_{DR}} (DSM_{h, t}^{up}
        + DSM_{h, t}^{balanceDo}
        + DSM_{h, t}^{do, shift} + DSM_{h, t}^{balanceUp})
        + DSM_{t}^{do, shed} \\
        & \quad \quad \leq \max \{E_{t}^{up} \cdot E_{max, up},
        E_{t}^{do} \cdot E_{max, do} \} \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T} \\
        & \quad \quad \textrm{(optional constraint)}  \\


    Note
    ----

    For the sake of readability, the handling of indices is not
    displayed here. E.g. evaluating a variable for `t-L` may lead to a negative
    and therefore infeasible index.
    This is addressed by limiting the sums to non-negative indices within the
    model index bounds. Please refer to the constraints implementation
    themselves.


    **The following parts of the objective function are created:**

    .. math::
        &
        (\sum_{h=1}^{H_{DR}} (DSM_{h, t}^{up} + DSM_{h, t}^{balanceDo})
        \cdot cost_{t}^{dsm, up} \\
        & + \sum_{h=1}^{H_{DR}} (DSM_{h, t}^{do, shift}
        + DSM_{h, t}^{balanceUp})
        \cdot cost_{t}^{dsm, do, shift} \\
        & + DSM_{t}^{do, shed} \cdot cost_{t}^{dsm, do, shed})
        \cdot \omega_{t} \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T} \\

    * :attr:`fixed_costs` not None

    .. math::
        \displaystyle \sum_{pp=0}^{year_{max}} max\{E_{up, max}, E_{do, max}\}
        \cdot c_{fixed}(pp) \cdot DF^{-pp}

    **Table: Symbols and attribute names of variables and parameters**

        .. table:: Variables (V), Parameters (P) and (additional) Sets (S)
            :widths: 25, 25, 10, 40

            =========================================== ================================= ==== =======================================
            symbol                                      attribute                         type explanation
            =========================================== ================================= ==== =======================================
            :math:`DSM_{h, t}^{up}`                     `dsm_up[g, h, t]`                 V    DSM up shift (additional load) in hour t with delay time h
            :math:`DSM_{h, t}^{do, shift}`              `dsm_do_shift[g, h, t]`           V    DSM down shift (less load) in hour t with delay time h
            :math:`DSM_{h, t}^{balanceUp}`              `balance_dsm_up[g, h, t]`         V    | DSM down shift (less load) in hour t with delay time h
                                                                                               | to balance previous upshift
            :math:`DSM_{h, t}^{balanceDo}`              `balance_dsm_do[g, h, t]`         V    | DSM up shift (additional load) in hour t with delay time h
                                                                                               | to balance previous downshift
            :math:`DSM_{t}^{do, shed}`                  `dsm_do_shed[g, t]`               V    DSM shedded (capacity shedded, i.e. not compensated for)
            :math:`\dot{E}_{t}`                         `SinkDSM.inputs`                  V    Energy flowing in from (electrical) inflow bus
            :math:`h`                                   `delay_time`                      P    | Maximum delay time for load shift
                                                                                               | (integer value from set of feasible delay times per DSM portfolio;
                                                                                               | time until the energy balance has to be levelled out again;
                                                                                               | roundtrip time of one load shifting cycle, i.e. time window
                                                                                               | for upshift and compensating downshift)
            :math:`H_{DR}`                              `range(len(delay_time))`          S    | Set of feasible delay times for load shift
                                                                                               | of a certain DSM portfolio
            :math:`t_{shift}`                           `shift_time`                      P    | Maximum time for a shift in one direction,
                                                                                               | i. e. maximum time for an upshift *or* a downshift
                                                                                               | in a load shifting cycle
            :math:`t_{she}`                             `shed_time`                       P    Maximum time for one load shedding process
            :math:`demand_{t}`                          `demand[t]`                       P    (Electrical) demand series (normalized)
            :math:`demand_{max}`                        `max_demand`                      P    Maximum demand value
            :math:`E_{t}^{do}`                          `capacity_down[t]`                P    | Capacity  allowed for a load adjustment downwards
                                                                                               | (normalized; shifting + shedding)
            :math:`E_{t}^{up}`                          `capacity_up[t]`                  P    Capacity allowed for a shift upwards (normalized)
            :math:`E_{do, max}`                         `max_capacity_down`               P    | Maximum capacity allowed for a load adjustment downwards
                                                                                               | (shifting + shedding)
            :math:`E_{up, max}`                         `max_capacity_up`                 P    Maximum capacity allowed for a shift upwards
            :math:`\eta`                                `efficiency`                      P    Efficiency for load shifting processes
            :math:`\mathbb{T}`                                                            S    Time steps of the model
            :math:`e_{shift}`                           `shift_eligibility`               P    | Boolean parameter indicating if unit can be used
                                                                                               | for load shifting
            :math:`e_{shed}`                            `shed_eligibility`                P    | Boolean parameter indicating if unit can be used
                                                                                               | for load shedding
            :math:`cost_{t}^{dsm, up}`                  `cost_dsm_up[t]`                  P    Variable costs for an upwards shift
            :math:`cost_{t}^{dsm, do, shift}`           `cost_dsm_down_shift[t]`          P    Variable costs for a downwards shift (load shifting)
            :math:`cost_{t}^{dsm, do, shed}`            `cost_dsm_down_shift[t]`          P    Variable costs for shedding load
            :math:`\omega_{t}`                                                            P    Objective weighting of the model for timestep t
            :math:`R_{shi}`                             `recovery_time_shift`             P    | Minimum time between the end of one load shifting process
                                                                                               | and the start of another
            :math:`R_{she}`                             `recovery_time_shed`              P    | Minimum time between the end of one load shedding process
                                                                                               | and the start of another
            :math:`\Delta t`                                                              P    The time increment of the model
            :math:`\omega_{t}`                                                            P    Objective weighting of the model for timestep t
            :math:`n_{yearLimitShift}`                  `n_yeaLimitShift`                 P    | Maximum allowed number of load shifts (at full capacity)
                                                                                               | in the optimization timeframe
            :math:`n_{yearLimitShed}`                   `n_yeaLimitShed`                  P    | Maximum allowed number of load sheds (at full capacity)
                                                                                               | in the optimization timeframe
            :math:`t_{dayLimit}`                        `t_dayLimit`                      P    | Maximum duration of load shifts at full capacity per day
                                                                                               | resp. in the last hours before the current"
            :math:`year_{max}`                                                            P    Last year of the optimization horizon
            =========================================== ================================= ==== =======================================

    """  # noqa: E501

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        if group is None:
            return None

        m = self.parent_block()

        # for all DSM components get inflow from a bus
        for n in group:
            n.inflow = list(n.inputs)[0]

        #  ************* SETS *********************************

        # Set of DR Components
        self.DR = Set(initialize=[n for n in group])

        # Depict different delay_times per unit via a mapping
        map_DR_H = {
            k: v
            for k, v in zip([n for n in group], [n.delay_time for n in group])
        }

        unique_H = list(set(itertools.chain.from_iterable(map_DR_H.values())))
        self.H = Set(initialize=unique_H)

        self.DR_H = Set(
            within=self.DR * self.H,
            initialize=[(dr, h) for dr in map_DR_H for h in map_DR_H[dr]],
        )

        #  ************* VARIABLES *****************************

        # Variable load shift down (capacity)
        self.dsm_do_shift = Var(
            self.DR_H, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        # Variable for load shedding (capacity)
        self.dsm_do_shed = Var(
            self.DR, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        # Variable load shift up (capacity)
        self.dsm_up = Var(
            self.DR_H, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        # Variable balance load shift down through upwards shift (capacity)
        self.balance_dsm_do = Var(
            self.DR_H, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        # Variable balance load shift up through downwards shift (capacity)
        self.balance_dsm_up = Var(
            self.DR_H, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        # Variable fictious DR storage level for downwards load shifts (energy)
        self.dsm_do_level = Var(
            self.DR, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        # Variable fictious DR storage level for upwards load shifts (energy)
        self.dsm_up_level = Var(
            self.DR, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        #  ************* CONSTRAINTS *****************************

        def _shift_shed_vars_rule(block):
            """Force shifting resp. shedding variables to zero dependent
            on how boolean parameters for shift resp. shed eligibility
            are set.
            """
            for t in m.TIMESTEPS:
                for g in group:
                    for h in g.delay_time:
                        if not g.shift_eligibility:
                            lhs = self.dsm_up[g, h, t]
                            rhs = 0

                            block.shift_shed_vars.add((g, h, t), (lhs == rhs))

                        if not g.shed_eligibility:
                            lhs = self.dsm_do_shed[g, t]
                            rhs = 0

                            block.shift_shed_vars.add((g, h, t), (lhs == rhs))

        self.shift_shed_vars = Constraint(
            group, self.H, m.TIMESTEPS, noruleinit=True
        )
        self.shift_shed_vars_build = BuildAction(rule=_shift_shed_vars_rule)

        # Relation between inflow and effective Sink consumption
        def _input_output_relation_rule(block):
            """Relation between input data and pyomo variables.
            The actual demand after DR.
            BusBlock outflow == Demand +- DR (i.e. effective Sink consumption)
            """
            for p, t in m.TIMEINDEX:
                for g in group:
                    # outflow from bus
                    lhs = m.flow[g.inflow, g, t]

                    # Demand +- DR
                    rhs = (
                        g.demand[t] * g.max_demand[p]
                        + sum(
                            self.dsm_up[g, h, t]
                            + self.balance_dsm_do[g, h, t]
                            - self.dsm_do_shift[g, h, t]
                            - self.balance_dsm_up[g, h, t]
                            for h in g.delay_time
                        )
                        - self.dsm_do_shed[g, t]
                    )

                    # add constraint
                    block.input_output_relation.add((g, p, t), (lhs == rhs))

        self.input_output_relation = Constraint(
            group, m.TIMEINDEX, noruleinit=True
        )
        self.input_output_relation_build = BuildAction(
            rule=_input_output_relation_rule
        )

        # Equation 4.8
        def capacity_balance_red_rule(block):
            """Load reduction must be balanced by load increase
            within delay_time
            """
            for t in m.TIMESTEPS:
                for g in group:
                    for h in g.delay_time:
                        if g.shift_eligibility:
                            # main use case
                            if t >= h:
                                # balance load reduction
                                lhs = self.balance_dsm_do[g, h, t]

                                # load reduction (efficiency considered)
                                rhs = (
                                    self.dsm_do_shift[g, h, t - h]
                                    / g.efficiency
                                )

                                # add constraint
                                block.capacity_balance_red.add(
                                    (g, h, t), (lhs == rhs)
                                )

                            # no balancing for the first timestep
                            elif t == m.TIMESTEPS.at(1):
                                lhs = self.balance_dsm_do[g, h, t]
                                rhs = 0

                                block.capacity_balance_red.add(
                                    (g, h, t), (lhs == rhs)
                                )

                            else:
                                pass  # return(Constraint.Skip)

                        # if only shedding is possible, balancing variable is 0
                        else:
                            lhs = self.balance_dsm_do[g, h, t]
                            rhs = 0

                            block.capacity_balance_red.add(
                                (g, h, t), (lhs == rhs)
                            )

        self.capacity_balance_red = Constraint(
            group, self.H, m.TIMESTEPS, noruleinit=True
        )
        self.capacity_balance_red_build = BuildAction(
            rule=capacity_balance_red_rule
        )

        # Equation 4.9
        def capacity_balance_inc_rule(block):
            """Load increased must be balanced by load reduction
            within delay_time
            """
            for t in m.TIMESTEPS:
                for g in group:
                    for h in g.delay_time:
                        if g.shift_eligibility:
                            # main use case
                            if t >= h:
                                # balance load increase
                                lhs = self.balance_dsm_up[g, h, t]

                                # load increase (efficiency considered)
                                rhs = self.dsm_up[g, h, t - h] * g.efficiency

                                # add constraint
                                block.capacity_balance_inc.add(
                                    (g, h, t), (lhs == rhs)
                                )

                            # no balancing for the first timestep
                            elif t == m.TIMESTEPS.at(1):
                                lhs = self.balance_dsm_up[g, h, t]
                                rhs = 0

                                block.capacity_balance_inc.add(
                                    (g, h, t), (lhs == rhs)
                                )

                            else:
                                pass  # return(Constraint.Skip)

                        # if only shedding is possible, balancing variable is 0
                        else:
                            lhs = self.balance_dsm_up[g, h, t]
                            rhs = 0

                            block.capacity_balance_inc.add(
                                (g, h, t), (lhs == rhs)
                            )

        self.capacity_balance_inc = Constraint(
            group, self.H, m.TIMESTEPS, noruleinit=True
        )
        self.capacity_balance_inc_build = BuildAction(
            rule=capacity_balance_inc_rule
        )

        # Fix: prevent shifts which cannot be compensated
        def no_comp_red_rule(block):
            """Prevent downwards shifts that cannot be balanced anymore
            within the optimization timeframe
            """
            for t in m.TIMESTEPS:
                for g in group:
                    if g.fixes:
                        for h in g.delay_time:
                            if t > m.TIMESTEPS.at(-1) - h:
                                # no load reduction anymore (dsm_do_shift = 0)
                                lhs = self.dsm_do_shift[g, h, t]
                                rhs = 0
                                block.no_comp_red.add((g, h, t), (lhs == rhs))

                    else:
                        pass  # return(Constraint.Skip)

        self.no_comp_red = Constraint(
            group, self.H, m.TIMESTEPS, noruleinit=True
        )
        self.no_comp_red_build = BuildAction(rule=no_comp_red_rule)

        # Fix: prevent shifts which cannot be compensated
        def no_comp_inc_rule(block):
            """Prevent upwards shifts that cannot be balanced anymore
            within the optimization timeframe
            """
            for t in m.TIMESTEPS:
                for g in group:
                    if g.fixes:
                        for h in g.delay_time:
                            if t > m.TIMESTEPS.at(-1) - h:
                                # no load increase anymore (dsm_up = 0)
                                lhs = self.dsm_up[g, h, t]
                                rhs = 0
                                block.no_comp_inc.add((g, h, t), (lhs == rhs))

                    else:
                        pass  # return(Constraint.Skip)

        self.no_comp_inc = Constraint(
            group, self.H, m.TIMESTEPS, noruleinit=True
        )
        self.no_comp_inc_build = BuildAction(rule=no_comp_inc_rule)

        # Equation 4.11
        def availability_red_rule(block):
            """Load reduction must be smaller than or equal to the
            (time-dependent) capacity limit
            """
            for t in m.TIMESTEPS:
                for g in group:
                    # load reduction
                    lhs = (
                        sum(
                            self.dsm_do_shift[g, h, t]
                            + self.balance_dsm_up[g, h, t]
                            for h in g.delay_time
                        )
                        + self.dsm_do_shed[g, t]
                    )

                    # upper bound
                    rhs = g.capacity_down[t] * g.max_capacity_down

                    # add constraint
                    block.availability_red.add((g, t), (lhs <= rhs))

        self.availability_red = Constraint(group, m.TIMESTEPS, noruleinit=True)
        self.availability_red_build = BuildAction(rule=availability_red_rule)

        # Equation 4.12
        def availability_inc_rule(block):
            """Load increase must be smaller than or equal to the
            (time-dependent) capacity limit
            """
            for t in m.TIMESTEPS:
                for g in group:
                    # load increase
                    lhs = sum(
                        self.dsm_up[g, h, t] + self.balance_dsm_do[g, h, t]
                        for h in g.delay_time
                    )

                    # upper bound
                    rhs = g.capacity_up[t] * g.max_capacity_up

                    # add constraint
                    block.availability_inc.add((g, t), (lhs <= rhs))

        self.availability_inc = Constraint(group, m.TIMESTEPS, noruleinit=True)
        self.availability_inc_build = BuildAction(rule=availability_inc_rule)

        # Equation 4.13
        def dr_storage_red_rule(block):
            """Fictious demand response storage level for load reductions
            transition equation
            """
            for t in m.TIMESTEPS:
                for g in group:
                    # avoid timesteps prior to t = 0
                    if t > 0:
                        # reduction minus balancing of reductions
                        lhs = m.timeincrement[t] * sum(
                            (
                                self.dsm_do_shift[g, h, t]
                                - self.balance_dsm_do[g, h, t] * g.efficiency
                            )
                            for h in g.delay_time
                        )

                        # load reduction storage level transition
                        rhs = (
                            self.dsm_do_level[g, t]
                            - self.dsm_do_level[g, t - 1]
                        )

                        # add constraint
                        block.dr_storage_red.add((g, t), (lhs == rhs))

                    else:
                        lhs = self.dsm_do_level[g, t]
                        rhs = m.timeincrement[t] * sum(
                            self.dsm_do_shift[g, h, t] for h in g.delay_time
                        )
                        block.dr_storage_red.add((g, t), (lhs == rhs))

        self.dr_storage_red = Constraint(group, m.TIMESTEPS, noruleinit=True)
        self.dr_storage_red_build = BuildAction(rule=dr_storage_red_rule)

        # Equation 4.14
        def dr_storage_inc_rule(block):
            """Fictious demand response storage level for load increase
            transition equation
            """
            for t in m.TIMESTEPS:
                for g in group:
                    # avoid timesteps prior to t = 0
                    if t > 0:
                        # increases minus balancing of reductions
                        lhs = m.timeincrement[t] * sum(
                            (
                                self.dsm_up[g, h, t] * g.efficiency
                                - self.balance_dsm_up[g, h, t]
                            )
                            for h in g.delay_time
                        )

                        # load increase storage level transition
                        rhs = (
                            self.dsm_up_level[g, t]
                            - self.dsm_up_level[g, t - 1]
                        )

                        # add constraint
                        block.dr_storage_inc.add((g, t), (lhs == rhs))

                    else:
                        # pass  # return(Constraint.Skip)
                        lhs = self.dsm_up_level[g, t]
                        rhs = m.timeincrement[t] * sum(
                            self.dsm_up[g, h, t] for h in g.delay_time
                        )
                        block.dr_storage_inc.add((g, t), (lhs == rhs))

        self.dr_storage_inc = Constraint(group, m.TIMESTEPS, noruleinit=True)
        self.dr_storage_inc_build = BuildAction(rule=dr_storage_inc_rule)

        # Equation 4.15
        def dr_storage_limit_red_rule(block):
            """
            Fictious demand response storage level for load reduction limit
            """
            for t in m.TIMESTEPS:
                for g in group:
                    if g.shift_eligibility:
                        # fictious demand response load reduction storage level
                        lhs = self.dsm_do_level[g, t]

                        # maximum (time-dependent) available shifting capacity
                        rhs = (
                            g.capacity_down_mean
                            * g.max_capacity_down
                            * g.shift_time
                        )

                        # add constraint
                        block.dr_storage_limit_red.add((g, t), (lhs <= rhs))

                    else:
                        lhs = self.dsm_do_level[g, t]
                        # Force storage level and thus dsm_do_shift to 0
                        rhs = 0

                        # add constraint
                        block.dr_storage_limit_red.add((g, t), (lhs <= rhs))

        self.dr_storage_limit_red = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.dr_storage_level_red_build = BuildAction(
            rule=dr_storage_limit_red_rule
        )

        # Equation 4.16
        def dr_storage_limit_inc_rule(block):
            """
            Fictious demand response storage level for load increase limit
            """
            for t in m.TIMESTEPS:
                for g in group:
                    # fictious demand response load reduction storage level
                    lhs = self.dsm_up_level[g, t]

                    # maximum (time-dependent) available shifting capacity
                    rhs = g.capacity_up_mean * g.max_capacity_up * g.shift_time

                    # add constraint
                    block.dr_storage_limit_inc.add((g, t), (lhs <= rhs))

        self.dr_storage_limit_inc = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.dr_storage_level_inc_build = BuildAction(
            rule=dr_storage_limit_inc_rule
        )

        # Equation 4.17' -> load shedding
        def dr_yearly_limit_shed_rule(block):
            """Introduce overall annual (energy) limit for load shedding resp.
            overall limit for optimization timeframe considered
            A year limit in contrast to Gils (2015) is defined a mandatory
            parameter here in order to achieve an approach comparable
            to the others.
            """
            for g in group:
                if g.shed_eligibility:
                    for p in m.PERIODS:
                        # sum of all load reductions
                        lhs = sum(
                            self.dsm_do_shed[g, t]
                            for pp, t in m.TIMEINDEX
                            if pp == p
                        )

                        # year limit
                        rhs = (
                            g.capacity_down_mean
                            * g.max_capacity_down
                            * g.shed_time
                            * g.n_yearLimit_shed
                        )

                        # add constraint
                        block.dr_yearly_limit_shed.add((g, p), (lhs <= rhs))

                else:
                    pass  # return(Constraint.Skip)

        self.dr_yearly_limit_shed = Constraint(
            group, m.PERIODS, noruleinit=True
        )
        self.dr_yearly_limit_shed_build = BuildAction(
            rule=dr_yearly_limit_shed_rule
        )

        # ************* Optional Constraints *****************************

        # Equation 4.17
        def dr_yearly_limit_red_rule(block):
            """Introduce overall annual (energy) limit for load reductions
            resp. overall limit for optimization timeframe considered
            """
            for g in group:
                if g.ActivateYearLimit:
                    for p in m.PERIODS:
                        # sum of all load reductions
                        lhs = sum(
                            sum(
                                self.dsm_do_shift[g, h, t]
                                for h in g.delay_time
                            )
                            for pp, t in m.TIMEINDEX
                            if pp == p
                        )

                        # year limit
                        rhs = (
                            g.capacity_down_mean
                            * g.max_capacity_down
                            * g.shift_time
                            * g.n_yearLimit_shift
                        )

                        # add constraint
                        block.dr_yearly_limit_red.add((g, p), (lhs <= rhs))

                else:
                    pass  # return(Constraint.Skip)

        self.dr_yearly_limit_red = Constraint(
            group, m.PERIODS, noruleinit=True
        )
        self.dr_yearly_limit_red_build = BuildAction(
            rule=dr_yearly_limit_red_rule
        )

        # Equation 4.18
        def dr_yearly_limit_inc_rule(block):
            """Introduce overall annual (energy) limit for load increases
            resp. overall limit for optimization timeframe considered
            """
            for g in group:
                if g.ActivateYearLimit:
                    for p in m.PERIODS:
                        # sum of all load increases
                        lhs = sum(
                            sum(self.dsm_up[g, h, t] for h in g.delay_time)
                            for pp, t in m.TIMEINDEX
                            if pp == p
                        )

                        # year limit
                        rhs = (
                            g.capacity_up_mean
                            * g.max_capacity_up
                            * g.shift_time
                            * g.n_yearLimit_shift
                        )

                        # add constraint
                        block.dr_yearly_limit_inc.add((g, p), (lhs <= rhs))

                else:
                    pass  # return(Constraint.Skip)

        self.dr_yearly_limit_inc = Constraint(
            group, m.PERIODS, noruleinit=True
        )
        self.dr_yearly_limit_inc_build = BuildAction(
            rule=dr_yearly_limit_inc_rule
        )

        # Equation 4.19
        def dr_daily_limit_red_rule(block):
            """Introduce rolling (energy) limit for load reductions
            This effectively limits DR utilization dependent on
            activations within previous hours.
            """
            for t in m.TIMESTEPS:
                for g in group:
                    if g.ActivateDayLimit:
                        # main use case
                        if t >= g.t_dayLimit:
                            # load reduction
                            lhs = sum(
                                self.dsm_do_shift[g, h, t]
                                for h in g.delay_time
                            )

                            # daily limit
                            rhs = (
                                g.capacity_down_mean
                                * g.max_capacity_down
                                * g.shift_time
                                - sum(
                                    sum(
                                        self.dsm_do_shift[g, h, t - t_dash]
                                        for h in g.delay_time
                                    )
                                    for t_dash in range(
                                        1, int(g.t_dayLimit) + 1
                                    )
                                )
                            )

                            # add constraint
                            block.dr_daily_limit_red.add((g, t), (lhs <= rhs))

                        else:
                            pass  # return(Constraint.Skip)

                    else:
                        pass  # return(Constraint.Skip)

        self.dr_daily_limit_red = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.dr_daily_limit_red_build = BuildAction(
            rule=dr_daily_limit_red_rule
        )

        # Equation 4.20
        def dr_daily_limit_inc_rule(block):
            """Introduce rolling (energy) limit for load increases
            This effectively limits DR utilization dependent on
            activations within previous hours.
            """
            for t in m.TIMESTEPS:
                for g in group:
                    if g.ActivateDayLimit:
                        # main use case
                        if t >= g.t_dayLimit:
                            # load increase
                            lhs = sum(
                                self.dsm_up[g, h, t] for h in g.delay_time
                            )

                            # daily limit
                            rhs = (
                                g.capacity_up_mean
                                * g.max_capacity_up
                                * g.shift_time
                                - sum(
                                    sum(
                                        self.dsm_up[g, h, t - t_dash]
                                        for h in g.delay_time
                                    )
                                    for t_dash in range(
                                        1, int(g.t_dayLimit) + 1
                                    )
                                )
                            )

                            # add constraint
                            block.dr_daily_limit_inc.add((g, t), (lhs <= rhs))

                        else:
                            pass  # return(Constraint.Skip)

                    else:
                        pass  # return(Constraint.Skip)

        self.dr_daily_limit_inc = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.dr_daily_limit_inc_build = BuildAction(
            rule=dr_daily_limit_inc_rule
        )

        # Addition: avoid simultaneous activations
        def dr_logical_constraint_rule(block):
            """Similar to equation 10 from Zerrahn and Schill (2015):
            The sum of upwards and downwards shifts may not be greater
            than the (bigger) capacity limit.
            """
            for t in m.TIMESTEPS:
                for g in group:
                    if g.addition:
                        # sum of load increases and reductions
                        lhs = (
                            sum(
                                self.dsm_up[g, h, t]
                                + self.balance_dsm_do[g, h, t]
                                + self.dsm_do_shift[g, h, t]
                                + self.balance_dsm_up[g, h, t]
                                for h in g.delay_time
                            )
                            + self.dsm_do_shed[g, t]
                        )

                        # maximum capacity eligibly for load shifting
                        rhs = max(
                            g.capacity_down[t] * g.max_capacity_down,
                            g.capacity_up[t] * g.max_capacity_up,
                        )

                        # add constraint
                        block.dr_logical_constraint.add((g, t), (lhs <= rhs))

                    else:
                        pass  # return(Constraint.Skip)

        self.dr_logical_constraint = Constraint(
            group, m.TIMESTEPS, noruleinit=True
        )
        self.dr_logical_constraint_build = BuildAction(
            rule=dr_logical_constraint_rule
        )

    # Equation 4.23
    def _objective_expression(self):
        r"""Objective expression with variable costs for DSM activity;
        Equation 4.23 from Gils (2015)
        """
        m = self.parent_block()

        variable_costs = 0
        fixed_costs = 0

        if m.es.periods is None:
            for t in m.TIMESTEPS:
                for g in self.DR:
                    variable_costs += (
                        sum(
                            self.dsm_up[g, h, t] + self.balance_dsm_do[g, h, t]
                            for h in g.delay_time
                        )
                        * g.cost_dsm_up[t]
                        * m.objective_weighting[t]
                    )
                    variable_costs += (
                        sum(
                            self.dsm_do_shift[g, h, t]
                            + self.balance_dsm_up[g, h, t]
                            for h in g.delay_time
                        )
                        * g.cost_dsm_down_shift[t]
                        + self.dsm_do_shed[g, t] * g.cost_dsm_down_shed[t]
                    ) * m.objective_weighting[t]

        else:
            for g in self.DR:
                for p, t in m.TIMEINDEX:
                    variable_costs += (
                        sum(
                            self.dsm_up[g, h, t] + self.balance_dsm_do[g, h, t]
                            for h in g.delay_time
                        )
                        * g.cost_dsm_up[t]
                    ) * m.objective_weighting[t]
                    variable_costs += (
                        sum(
                            self.dsm_do_shift[g, h, t]
                            + self.balance_dsm_up[g, h, t]
                            for h in g.delay_time
                        )
                        * g.cost_dsm_down_shift[t]
                        + self.dsm_do_shed[g, t] * g.cost_dsm_down_shed[t]
                    ) * m.objective_weighting[t]

                if valid_sequence(g.fixed_costs, len(m.PERIODS)):
                    fixed_costs += sum(
                        max(g.max_capacity_up, g.max_capacity_down)
                        * g.fixed_costs[pp]
                        for pp in range(m.es.end_year_of_optimization)
                    )

        self.variable_costs = Expression(expr=variable_costs)
        self.fixed_costs = Expression(expr=fixed_costs)
        self.costs = Expression(expr=variable_costs + fixed_costs)

        return self.costs


class SinkDSMDLRInvestmentBlock(ScalarBlock):
    r"""Constraints for SinkDSM with "DLR" approach and `investment` defined

    **The following constraints are created for approach = "DLR" with an
    investment object defined:**

    .. _SinkDSMDLRInvestmentBlock equations:

    .. math::
        &
        (1) \quad invest_{min}(p) \leq invest(p) \leq invest_{max}(p) \\
        & \quad \quad \quad \quad \forall p \in \mathbb{P}
        & \\
        &
        (2) \quad DSM_{h, t}^{up} = 0 \\
        & \quad \quad \quad \quad \forall h \in H_{DR}, t \in \mathbb{T}
        \quad \textrm{if} \quad e_{shift} = \textrm{False} \\
        &
        (3) \quad DSM_{t}^{do, shed} = 0 \\
        & \quad \quad \quad \quad \forall t \in \mathbb{T}
        \quad \textrm{if} \quad e_{shed} = \textrm{False} \\
        & \\
        &
        (4) \quad \dot{E}_{t} = demand_{t} \cdot demand_{max}(p) \\
        & \displaystyle\sum_{h=1}^{H_{DR}} (DSM_{h, t}^{up}
        + DSM_{h, t}^{balanceDo} - DSM_{h, t}^{do, shift}
        - DSM_{h, t}^{balanceUp}) - DSM_{t}^{do, shed} \\
        & \quad \quad \quad \quad \forall p, t \in \textrm{TIMEINDEX} \\
        & \\
        &
        (5) \quad DSM_{h, t}^{balanceDo} =
        \frac{DSM_{h, t - h}^{do, shift}}{\eta} \\
        & \quad \quad \quad \quad \forall h \in H_{DR}, t \in [h..T] \\
        & \\
        &
        (6) \quad DSM_{h, t}^{balanceUp} =
        DSM_{h, t-h}^{up} \cdot \eta \\
        & \quad \quad \quad \quad \forall h \in H_{DR}, t \in [h..T] \\
        & \\
        &
        (7) \quad DSM_{h, t}^{do, shift} = 0
        \quad \forall h \in H_{DR} \\
        & \quad \quad \quad \quad \forall t \in [T - h..T] \\
        & \\
        &
        (8) \quad DSM_{h, t}^{up} = 0 \\
        & \quad \quad \quad \quad \forall h \in H_{DR}, t \in [T - h..T] \\
        & \\
        &
        (9) \quad \displaystyle\sum_{h=1}^{H_{DR}} (DSM_{h, t}^{do, shift}
        + DSM_{h, t}^{balanceUp}) + DSM_{t}^{do, shed}
        \leq E_{t}^{do} \cdot P_{total}(p) \\
        & \quad \quad \quad \quad  \forall p, t \in \textrm{TIMEINDEX} \\
        & \\
        &
        (10) \quad \displaystyle\sum_{h=1}^{H_{DR}} (DSM_{h, t}^{up}
        + DSM_{h, t}^{balanceDo})
        \leq E_{t}^{up} \cdot P_{total}(p) \\
        & \quad \quad \quad \quad  \forall p, t \in \textrm{TIMEINDEX} \\
        & \\
        &
        (11) \quad \Delta t \cdot \displaystyle\sum_{h=1}^{H_{DR}}
        (DSM_{h, t}^{do, shift} - DSM_{h, t}^{balanceDo} \cdot \eta)
        = W_{t}^{levelDo} - W_{t-1}^{levelDo} \\
        & \quad \quad \quad \quad \forall t \in [1..T] \\
        & \\
        &
        (12) \quad \Delta t \cdot \displaystyle\sum_{h=1}^{H_{DR}}
        (DSM_{h, t}^{up} \cdot \eta - DSM_{h, t}^{balanceUp})
        = W_{t}^{levelUp} - W_{t-1}^{levelUp} \\
        & \quad \quad \quad \quad \forall t \in [1..T] \\
        & \\
        &
        (13) \quad W_{t}^{levelDo} \leq \overline{E}_{t}^{do}
        \cdot P_{total}(p) \cdot t_{shift} \\
        & \quad \quad \quad \quad \forall p, t \in \textrm{TIMEINDEX} \\
        & \\
        &
        (14) \quad W_{t}^{levelUp} \leq \overline{E}_{t}^{up}
        \cdot P_{total}(p)  \cdot t_{shift} \\
        & \quad \quad \quad \quad \forall p, t \in \textrm{TIMEINDEX} \\
        & \\
        &
        (15) \quad \displaystyle\sum_{t=0}^{T} DSM_{t}^{do, shed}
        \leq P_{total}(p) \cdot \overline{E}_{t}^{do}
        \cdot t_{shed}
        \cdot n^{yearLimitShed} \\
        & \\
        &
        (16) \quad \displaystyle\sum_{t=0}^{T} \sum_{h=1}^{H_{DR}}
        DSM_{h, t}^{do, shift}
        \leq P_{total}(p)
        \cdot \overline{E}_{t}^{do}
        \cdot t_{shift}
        \cdot n^{yearLimitShift} \\
        & \quad \quad \textrm{(optional constraint)} \\
        & \\
        &
        (17) \quad \displaystyle\sum_{t=0}^{T} \sum_{h=1}^{H_{DR}}
        DSM_{h, t}^{up}
        \leq P_{total}(p)
        \cdot \overline{E}_{t}^{up}
        \cdot t_{shift}
        \cdot n^{yearLimitShift} \\
        & \quad \quad \textrm{(optional constraint)} \\
        &
        (18) \quad \displaystyle\sum_{h=1}^{H_{DR}} DSM_{h, t}^{do, shift}
        \leq P_{total}(p)
        \cdot \overline{E}_{t}^{do}
        \cdot t_{shift} -
        \displaystyle\sum_{t'=1}^{t_{dayLimit}} \sum_{h=1}^{H_{DR}}
        DSM_{h, t - t'}^{do, shift} \\
        & \quad \quad \quad \quad \forall t \in [t-t_{dayLimit}..T] \\
        & \quad \quad \textrm{(optional constraint)} \\
        & \\
        &
        (19) \quad \displaystyle\sum_{h=1}^{H_{DR}} DSM_{h, t}^{up}
        \leq (invest + E_{exist})
        \cdot \overline{E}_{t}^{up}
        \cdot t_{shift} -
        \displaystyle\sum_{t'=1}^{t_{dayLimit}} \sum_{h=1}^{H_{DR}}
        DSM_{h, t - t'}^{up} \\
        & \quad \quad \quad \quad \forall t \in [t-t_{dayLimit}..T] \\
        & \quad \quad \textrm{(optional constraint)} \\
        & \\
        &
        (20) \quad \displaystyle\sum_{h=1}^{H_{DR}} (DSM_{h, t}^{up}
        + DSM_{h, t}^{balanceDo}
        + DSM_{h, t}^{do, shift} + DSM_{h, t}^{balanceUp}) \\
        & + DSM_{t}^{shed}
        \leq \max \{E_{t}^{up}, E_{t}^{do} \} \cdot P_{total}(p) \\
        & \quad \quad \quad \quad \forall p, t \in \textrm{TIMEINDEX} \\
        & \quad \quad \textrm{(optional constraint)} \\
        &

    Note
    ----

    For the sake of readability, the handling of indices is not
    displayed here. E.g. evaluating a variable for `t-L` may lead to a negative
    and therefore infeasible index.
    This is addressed by limiting the sums to non-negative indices within the
    model index bounds. Please refer to the constraints implementation
    themselves.


    **The following parts of the objective function are created:**

    *Standard model*

        * Investment annuity:

            .. math::
                P_{invest}(0) \cdot c_{invest}(0)

        * Variable costs:

            .. math::
                &
                (\sum_{h=1}^{H_{DR}} (DSM_{h, t}^{up} + DSM_{h, t}^{balanceDo})
                \cdot cost_{t}^{dsm, up} \\
                & + \sum_{h=1}^{H_{DR}} (DSM_{h, t}^{do, shift}
                + DSM_{h, t}^{balanceUp})
                \cdot cost_{t}^{dsm, do, shift} \\
                & + DSM_{t}^{do, shed} \cdot cost_{t}^{dsm, do, shed})
                \cdot \omega_{t} \\
                & \quad \quad \quad \quad \forall t \in \mathbb{T} \\

    *Multi-period model*

        * Investment annuity:

            .. math::
                &
                P_{invest}(p) \cdot A(c_{invest}(p), l, ir)
                \cdot \frac {1}{ANF(d, ir)} \cdot DF^{-p} \\
                &\\
                &
                \forall p \in \mathbb{P}

        In case, the remaining lifetime of a DSM unit is greater than 0 and
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

        * :attr:`fixed_costs` not None for investments

            .. math::
                &
                (\sum_{pp=year(p)}^{limit_{end}}
                P_{invest}(p) \cdot c_{fixed}(pp) \cdot DF^{-pp})
                \cdot DF^{-p} \\
                &\\
                &
                \forall p \in \mathbb{P}

        * Variable costs:

            .. math::
                &
                (\sum_{h=1}^{H_{DR}} (DSM_{h, t}^{up} + DSM_{h, t}^{balanceDo})
                \cdot cost_{t}^{dsm, up} \\
                & + \sum_{h=1}^{H_{DR}} (DSM_{h, t}^{do, shift}
                + DSM_{h, t}^{balanceUp})
                \cdot cost_{t}^{dsm, do, shift} \\
                & + DSM_{t}^{do, shed} \cdot cost_{t}^{dsm, do, shed})
                \cdot \omega_{t} \cdot DF^{-p} \\
                & \quad \quad \quad \quad \forall p, t \in \textrm{TIMEINDEX} \\

    where:

    * :math:`A(c_{invest,var}(p), l, ir)` A is the annuity for
      investment expenses :math:`c_{invest,var}(p)`, lifetime :math:`l`
      and interest rate :math:`ir`.
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
    * :math:`DF=(1+dr)` is the discount factor.

    The annuity / annuity factor hereby is:

        .. math::
            &
            A(c_{invest,var}(p), l, ir) = c_{invest,var}(p) \cdot
                \frac {(1+ir)^l \cdot ir} {(1+ir)^l - 1}\\
            &\\
            &
            ANF(d, ir)=\frac {(1+dr)^d \cdot dr} {(1+dr)^d - 1}

    They are retrieved, using oemof.tools.economics annuity function. The
    interest rate :math:`ir` for the annuity is defined as weighted
    average costs of capital (wacc) and assumed constant over time.

    See remarks in
    :class:`oemof.solph.components.experimental._sink_dsm.SinkDSMOemofBlock`.


    **Table: Symbols and attribute names of variables and parameters**

    * Please refer to
      :class:`oemof.solph.components.experimental._sink_dsm.SinkDSMDLRBlock`.
    * The following variables and parameters are exclusively used for
      investment modeling:

    .. table:: Variables (V), Parameters (P) and Sets (S)
        :widths: 25, 25, 10, 40

        ================================= ======================== ==== =======================================
        symbol                            attribute                type explanation
        ================================= ======================== ==== =======================================
        :math:`P_{invest}(p)`             `invest[p]`              V    | DSM capacity invested into in period p.
                                                                        | Equals to the additionally shiftable resp. sheddable capacity.
        :math:`invest_{min}(p)`           `investment.minimum[p]`  P    minimum investment in period p
        :math:`invest_{max}(p)`           `investment.maximum[p]`  P    maximum investment in period p
        :math:`P_{total}`                 `investment.total[p]`    P    total DSM capacity
        :math:`costs_{invest}(p)`         `investment.ep_costs[p]` P    | specific investment annuity (standard model) resp.
                                                                        | specific investment expenses (multi-period model)
        :math:`\mathbb{P}`                                         S    Periods of the model
        :math:`\textrm{TIMEINDEX}`                                 S    Timeindex set of the model (periods, timesteps)
        ================================= ======================== ==== =======================================

    """  # noqa: E501

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        if group is None:
            return None

        m = self.parent_block()

        # for all DSM components get inflow from a bus
        for n in group:
            n.inflow = list(n.inputs)[0]

        #  ************* SETS *********************************

        self.INVESTDR = Set(initialize=[n for n in group])

        # Depict different delay_times per unit via a mapping
        map_INVESTDR_H = {
            k: v
            for k, v in zip([n for n in group], [n.delay_time for n in group])
        }

        unique_H = list(
            set(itertools.chain.from_iterable(map_INVESTDR_H.values()))
        )
        self.H = Set(initialize=unique_H)

        self.INVESTDR_H = Set(
            within=self.INVESTDR * self.H,
            initialize=[
                (dr, h) for dr in map_INVESTDR_H for h in map_INVESTDR_H[dr]
            ],
        )

        self.OVERALL_MAXIMUM_INVESTDSM = Set(
            initialize=[
                g for g in group if g.investment.overall_maximum is not None
            ]
        )

        self.OVERALL_MINIMUM_INVESTDSM = Set(
            initialize=[
                g for g in group if g.investment.overall_minimum is not None
            ]
        )

        self.EXISTING_INVESTDSM = Set(
            initialize=[g for g in group if g.investment.existing is not None]
        )

        #  ************* VARIABLES *****************************

        # Define bounds for investments in demand response
        def _dr_investvar_bound_rule(block, g, p):
            """Rule definition to bound the
            invested demand response capacity `invest`.
            """
            return g.investment.minimum[p], g.investment.maximum[p]

        # Investment in DR capacity
        self.invest = Var(
            self.INVESTDR,
            m.PERIODS,
            within=NonNegativeReals,
            bounds=_dr_investvar_bound_rule,
        )

        # Total capacity
        self.total = Var(self.INVESTDR, m.PERIODS, within=NonNegativeReals)

        if m.es.periods is not None:
            # Old capacity to be decommissioned (due to lifetime)
            self.old = Var(self.INVESTDR, m.PERIODS, within=NonNegativeReals)

            # Old endogenous capacity to be decommissioned (due to lifetime)
            self.old_end = Var(
                self.INVESTDR, m.PERIODS, within=NonNegativeReals
            )

            # Old exogenous capacity to be decommissioned (due to lifetime)
            self.old_exo = Var(
                self.INVESTDR, m.PERIODS, within=NonNegativeReals
            )

        # Variable load shift down (capacity)
        self.dsm_do_shift = Var(
            self.INVESTDR_H, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        # Variable for load shedding (capacity)
        self.dsm_do_shed = Var(
            self.INVESTDR, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        # Variable load shift up (capacity)
        self.dsm_up = Var(
            self.INVESTDR_H, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        # Variable balance load shift down through upwards shift (capacity)
        self.balance_dsm_do = Var(
            self.INVESTDR_H, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        # Variable balance load shift up through downwards shift (capacity)
        self.balance_dsm_up = Var(
            self.INVESTDR_H, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        # Variable fictious DR storage level for downwards load shifts (energy)
        self.dsm_do_level = Var(
            self.INVESTDR, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        # Variable fictious DR storage level for upwards load shifts (energy)
        self.dsm_up_level = Var(
            self.INVESTDR, m.TIMESTEPS, initialize=0, within=NonNegativeReals
        )

        #  ************* CONSTRAINTS *****************************

        # Handle unit lifetimes
        def _total_capacity_rule(block):
            """Rule definition for determining total installed
            capacity (taking decommissioning into account)
            """
            for g in group:
                for p in m.PERIODS:
                    if p == 0:
                        expr = (
                            self.total[g, p]
                            == self.invest[g, p] + g.investment.existing
                        )
                        self.total_dsm_rule.add((g, p), expr)
                    else:
                        expr = (
                            self.total[g, p]
                            == self.invest[g, p]
                            + self.total[g, p - 1]
                            - self.old[g, p]
                        )
                        self.total_dsm_rule.add((g, p), expr)

        self.total_dsm_rule = Constraint(group, m.PERIODS, noruleinit=True)
        self.total_dsm_rule_build = BuildAction(rule=_total_capacity_rule)

        if m.es.periods is not None:

            def _old_dsm_capacity_rule_end(block):
                """Rule definition for determining old endogenously installed
                capacity to be decommissioned due to reaching its lifetime.
                Investment and decommissioning periods are linked within
                the constraint. The respective decommissioning period is
                determined for every investment period based on the components
                lifetime and a matrix describing its age of each endogenous
                investment. Decommissioning can only occur at the beginning of
                each period.

                Note
                ----
                For further information on the implementation check
                PR#957 https://github.com/oemof/oemof-solph/pull/957
                """
                for g in group:
                    lifetime = g.investment.lifetime
                    if lifetime is None:
                        msg = (
                            "You have to specify a lifetime "
                            "for a Flow with an associated "
                            "investment object in "
                            f"a multi-period model! Value for {(g)} "
                            "is missing."
                        )
                        raise ValueError(msg)

                    # get the period matrix describing the temporal distance
                    # between all period combinations.
                    periods_matrix = m.es.periods_matrix

                    # get the index of the minimum value in each row greater
                    # equal than the lifetime. This value equals the
                    # decommissioning period if not zero. The index of this
                    # value represents the investment period. If np.where
                    # condition is not met in any row, min value will be zero
                    decomm_periods = np.argmin(
                        np.where(
                            (periods_matrix >= lifetime),
                            periods_matrix,
                            np.inf,
                        ),
                        axis=1,
                    )

                    # no decommissioning in first period
                    expr = self.old_end[g, 0] == 0
                    self.old_dsm_rule_end.add((g, 0), expr)

                    # all periods not in decomm_periods have no decommissioning
                    # zero is excluded
                    for p in m.PERIODS:
                        if p not in decomm_periods and p != 0:
                            expr = self.old_end[g, p] == 0
                            self.old_dsm_rule_end.add((g, p), expr)

                    # multiple invests can be decommissioned in the same period
                    # but only sequential ones, thus a bookkeeping is
                    # introduced andconstraints are added to equation one
                    # iteration later.
                    last_decomm_p = np.nan
                    # loop over invest periods (values are decomm_periods)
                    for invest_p, decomm_p in enumerate(decomm_periods):
                        # Add constraint of iteration before
                        # (skipped in first iteration by last_decomm_p = nan)
                        if (decomm_p != last_decomm_p) and (
                            last_decomm_p is not np.nan
                        ):
                            expr = self.old_end[g, last_decomm_p] == expr
                            self.old_dsm_rule_end.add((g, last_decomm_p), expr)

                        # no decommissioning if decomm_p is zero
                        if decomm_p == 0:
                            # overwrite decomm_p with zero to avoid
                            # chaining invest periods in next iteration
                            last_decomm_p = 0

                        # if decomm_p is the same as the last one chain invest
                        # period
                        elif decomm_p == last_decomm_p:
                            expr += self.invest[g, invest_p]
                            # overwrite decomm_p
                            last_decomm_p = decomm_p

                        # if decomm_p is not zero, not the same as the last one
                        # and it's not the first period
                        else:
                            expr = self.invest[g, invest_p]
                            # overwrite decomm_p
                            last_decomm_p = decomm_p

                    # Add constraint of very last iteration
                    if last_decomm_p != 0:
                        expr = self.old_end[g, last_decomm_p] == expr
                        self.old_dsm_rule_end.add((g, last_decomm_p), expr)

            self.old_dsm_rule_end = Constraint(
                group, m.PERIODS, noruleinit=True
            )
            self.old_dsm_rule_end_build = BuildAction(
                rule=_old_dsm_capacity_rule_end
            )

            def _old_dsm_capacity_rule_exo(block):
                """Rule definition for determining old exogenously given
                capacity to be decommissioned due to reaching its lifetime
                """
                for g in group:
                    age = g.investment.age
                    lifetime = g.investment.lifetime
                    is_decommissioned = False
                    for p in m.PERIODS:
                        # No shutdown in first period
                        if p == 0:
                            expr = self.old_exo[g, p] == 0
                            self.old_dsm_rule_exo.add((g, p), expr)
                        elif lifetime - age <= m.es.periods_years[p]:
                            # Track decommissioning status
                            if not is_decommissioned:
                                expr = (
                                    self.old_exo[g, p] == g.investment.existing
                                )
                                is_decommissioned = True
                            else:
                                expr = self.old_exo[g, p] == 0
                            self.old_dsm_rule_exo.add((g, p), expr)
                        else:
                            expr = self.old_exo[g, p] == 0
                            self.old_dsm_rule_exo.add((g, p), expr)

            self.old_dsm_rule_exo = Constraint(
                group, m.PERIODS, noruleinit=True
            )
            self.old_dsm_rule_exo_build = BuildAction(
                rule=_old_dsm_capacity_rule_exo
            )

            def _old_dsm_capacity_rule(block):
                """Rule definition for determining (overall) old capacity
                to be decommissioned due to reaching its lifetime
                """
                for g in group:
                    for p in m.PERIODS:
                        expr = (
                            self.old[g, p]
                            == self.old_end[g, p] + self.old_exo[g, p]
                        )
                        self.old_dsm_rule.add((g, p), expr)

            self.old_dsm_rule = Constraint(group, m.PERIODS, noruleinit=True)
            self.old_dsm_rule_build = BuildAction(rule=_old_dsm_capacity_rule)

        def _shift_shed_vars_rule(block):
            """Force shifting resp. shedding variables to zero dependent
            on how boolean parameters for shift resp. shed eligibility
            are set.
            """
            for t in m.TIMESTEPS:
                for g in group:
                    for h in g.delay_time:
                        if not g.shift_eligibility:
                            lhs = self.dsm_up[g, h, t]
                            rhs = 0

                            block.shift_shed_vars.add((g, h, t), (lhs == rhs))

                        if not g.shed_eligibility:
                            lhs = self.dsm_do_shed[g, t]
                            rhs = 0

                            block.shift_shed_vars.add((g, h, t), (lhs == rhs))

        self.shift_shed_vars = Constraint(
            group, self.H, m.TIMESTEPS, noruleinit=True
        )
        self.shift_shed_vars_build = BuildAction(rule=_shift_shed_vars_rule)

        # Relation between inflow and effective Sink consumption
        def _input_output_relation_rule(block):
            """Relation between input data and pyomo variables.
            The actual demand after DR.
            BusBlock outflow == Demand +- DR (i.e. effective Sink consumption)
            """
            for p, t in m.TIMEINDEX:
                for g in group:
                    # outflow from bus
                    lhs = m.flow[g.inflow, g, t]

                    # Demand +- DR
                    rhs = (
                        g.demand[t] * g.max_demand[p]
                        + sum(
                            self.dsm_up[g, h, t]
                            + self.balance_dsm_do[g, h, t]
                            - self.dsm_do_shift[g, h, t]
                            - self.balance_dsm_up[g, h, t]
                            for h in g.delay_time
                        )
                        - self.dsm_do_shed[g, t]
                    )

                    # add constraint
                    block.input_output_relation.add((g, p, t), (lhs == rhs))

        self.input_output_relation = Constraint(
            group, m.TIMEINDEX, noruleinit=True
        )
        self.input_output_relation_build = BuildAction(
            rule=_input_output_relation_rule
        )

        # Equation 4.8
        def capacity_balance_red_rule(block):
            """Load reduction must be balanced by load increase
            within delay_time
            """
            for t in m.TIMESTEPS:
                for g in group:
                    for h in g.delay_time:
                        if g.shift_eligibility:
                            # main use case
                            if t >= h:
                                # balance load reduction
                                lhs = self.balance_dsm_do[g, h, t]

                                # load reduction (efficiency considered)
                                rhs = (
                                    self.dsm_do_shift[g, h, t - h]
                                    / g.efficiency
                                )

                                # add constraint
                                block.capacity_balance_red.add(
                                    (g, h, t), (lhs == rhs)
                                )

                            # no balancing for the first timestep
                            elif t == m.TIMESTEPS.at(1):
                                lhs = self.balance_dsm_do[g, h, t]
                                rhs = 0

                                block.capacity_balance_red.add(
                                    (g, h, t), (lhs == rhs)
                                )

                            else:
                                pass  # return(Constraint.Skip)

                        # if only shedding is possible, balancing variable is 0
                        else:
                            lhs = self.balance_dsm_do[g, h, t]
                            rhs = 0

                            block.capacity_balance_red.add(
                                (g, h, t), (lhs == rhs)
                            )

        self.capacity_balance_red = Constraint(
            group, self.H, m.TIMESTEPS, noruleinit=True
        )
        self.capacity_balance_red_build = BuildAction(
            rule=capacity_balance_red_rule
        )

        # Equation 4.9
        def capacity_balance_inc_rule(block):
            """Load increased must be balanced by load reduction
            within delay_time
            """
            for t in m.TIMESTEPS:
                for g in group:
                    for h in g.delay_time:
                        if g.shift_eligibility:
                            # main use case
                            if t >= h:
                                # balance load increase
                                lhs = self.balance_dsm_up[g, h, t]

                                # load increase (efficiency considered)
                                rhs = self.dsm_up[g, h, t - h] * g.efficiency

                                # add constraint
                                block.capacity_balance_inc.add(
                                    (g, h, t), (lhs == rhs)
                                )

                            # no balancing for the first timestep
                            elif t == m.TIMESTEPS.at(1):
                                lhs = self.balance_dsm_up[g, h, t]
                                rhs = 0

                                block.capacity_balance_inc.add(
                                    (g, h, t), (lhs == rhs)
                                )

                            else:
                                pass  # return(Constraint.Skip)

                        # if only shedding is possible, balancing variable is 0
                        else:
                            lhs = self.balance_dsm_up[g, h, t]
                            rhs = 0

                            block.capacity_balance_inc.add(
                                (g, h, t), (lhs == rhs)
                            )

        self.capacity_balance_inc = Constraint(
            group, self.H, m.TIMESTEPS, noruleinit=True
        )
        self.capacity_balance_inc_build = BuildAction(
            rule=capacity_balance_inc_rule
        )

        # Own addition: prevent shifts which cannot be compensated
        def no_comp_red_rule(block):
            """Prevent downwards shifts that cannot be balanced anymore
            within the optimization timeframe
            """
            for t in m.TIMESTEPS:
                for g in group:
                    if g.fixes:
                        for h in g.delay_time:
                            if t > m.TIMESTEPS.at(-1) - h:
                                # no load reduction anymore (dsm_do_shift = 0)
                                lhs = self.dsm_do_shift[g, h, t]
                                rhs = 0
                                block.no_comp_red.add((g, h, t), (lhs == rhs))

                    else:
                        pass  # return(Constraint.Skip)

        self.no_comp_red = Constraint(
            group, self.H, m.TIMESTEPS, noruleinit=True
        )
        self.no_comp_red_build = BuildAction(rule=no_comp_red_rule)

        # Own addition: prevent shifts which cannot be compensated
        def no_comp_inc_rule(block):
            """Prevent upwards shifts that cannot be balanced anymore
            within the optimization timeframe
            """
            for t in m.TIMESTEPS:
                for g in group:
                    if g.fixes:
                        for h in g.delay_time:
                            if t > m.TIMESTEPS.at(-1) - h:
                                # no load increase anymore (dsm_up = 0)
                                lhs = self.dsm_up[g, h, t]
                                rhs = 0
                                block.no_comp_inc.add((g, h, t), (lhs == rhs))

                    else:
                        pass  # return(Constraint.Skip)

        self.no_comp_inc = Constraint(
            group, self.H, m.TIMESTEPS, noruleinit=True
        )
        self.no_comp_inc_build = BuildAction(rule=no_comp_inc_rule)

        # Equation 4.11
        def availability_red_rule(block):
            """Load reduction must be smaller than or equal to the
            (time-dependent) capacity limit
            """
            for p, t in m.TIMEINDEX:
                for g in group:
                    # load reduction
                    lhs = (
                        sum(
                            self.dsm_do_shift[g, h, t]
                            + self.balance_dsm_up[g, h, t]
                            for h in g.delay_time
                        )
                        + self.dsm_do_shed[g, t]
                    )

                    # upper bound
                    rhs = g.capacity_down[t] * self.total[g, p]

                    # add constraint
                    block.availability_red.add((g, p, t), (lhs <= rhs))

        self.availability_red = Constraint(group, m.TIMEINDEX, noruleinit=True)
        self.availability_red_build = BuildAction(rule=availability_red_rule)

        # Equation 4.12
        def availability_inc_rule(block):
            """Load increase must be smaller than or equal to the
            (time-dependent) capacity limit
            """
            for p, t in m.TIMEINDEX:
                for g in group:
                    # load increase
                    lhs = sum(
                        self.dsm_up[g, h, t] + self.balance_dsm_do[g, h, t]
                        for h in g.delay_time
                    )

                    # upper bound
                    rhs = g.capacity_up[t] * self.total[g, p]

                    # add constraint
                    block.availability_inc.add((g, p, t), (lhs <= rhs))

        self.availability_inc = Constraint(group, m.TIMEINDEX, noruleinit=True)
        self.availability_inc_build = BuildAction(rule=availability_inc_rule)

        # Equation 4.13
        def dr_storage_red_rule(block):
            """Fictious demand response storage level for load reductions
            transition equation
            """
            for t in m.TIMESTEPS:
                for g in group:
                    # avoid timesteps prior to t = 0
                    if t > 0:
                        # reduction minus balancing of reductions
                        lhs = m.timeincrement[t] * sum(
                            (
                                self.dsm_do_shift[g, h, t]
                                - self.balance_dsm_do[g, h, t] * g.efficiency
                            )
                            for h in g.delay_time
                        )

                        # load reduction storage level transition
                        rhs = (
                            self.dsm_do_level[g, t]
                            - self.dsm_do_level[g, t - 1]
                        )

                        # add constraint
                        block.dr_storage_red.add((g, t), (lhs == rhs))

                    else:
                        # pass  # return(Constraint.Skip)
                        lhs = self.dsm_do_level[g, t]
                        rhs = m.timeincrement[t] * sum(
                            self.dsm_do_shift[g, h, t] for h in g.delay_time
                        )
                        block.dr_storage_red.add((g, t), (lhs == rhs))

        self.dr_storage_red = Constraint(group, m.TIMESTEPS, noruleinit=True)
        self.dr_storage_red_build = BuildAction(rule=dr_storage_red_rule)

        # Equation 4.14
        def dr_storage_inc_rule(block):
            """Fictious demand response storage level for load increase
            transition equation
            """
            for t in m.TIMESTEPS:
                for g in group:
                    # avoid timesteps prior to t = 0
                    if t > 0:
                        # increases minus balancing of reductions
                        lhs = m.timeincrement[t] * sum(
                            (
                                self.dsm_up[g, h, t] * g.efficiency
                                - self.balance_dsm_up[g, h, t]
                            )
                            for h in g.delay_time
                        )

                        # load increase storage level transition
                        rhs = (
                            self.dsm_up_level[g, t]
                            - self.dsm_up_level[g, t - 1]
                        )

                        # add constraint
                        block.dr_storage_inc.add((g, t), (lhs == rhs))

                    else:
                        # pass  # return(Constraint.Skip)
                        lhs = self.dsm_up_level[g, t]
                        rhs = m.timeincrement[t] * sum(
                            self.dsm_up[g, h, t] for h in g.delay_time
                        )
                        block.dr_storage_inc.add((g, t), (lhs == rhs))

        self.dr_storage_inc = Constraint(group, m.TIMESTEPS, noruleinit=True)
        self.dr_storage_inc_build = BuildAction(rule=dr_storage_inc_rule)

        # Equation 4.15
        def dr_storage_limit_red_rule(block):
            """
            Fictious demand response storage level for load reduction limit
            """
            for p, t in m.TIMEINDEX:
                for g in group:
                    if g.shift_eligibility:
                        # fictious demand response load reduction storage level
                        lhs = self.dsm_do_level[g, t]

                        # maximum (time-dependent) available shifting capacity
                        rhs = (
                            g.capacity_down_mean
                            * self.total[g, p]
                            * g.shift_time
                        )

                        # add constraint
                        block.dr_storage_limit_red.add((g, p, t), (lhs <= rhs))

                    else:
                        lhs = self.dsm_do_level[g, t]
                        # Force storage level and thus dsm_do_shift to 0
                        rhs = 0

                        # add constraint
                        block.dr_storage_limit_red.add((g, p, t), (lhs <= rhs))

        self.dr_storage_limit_red = Constraint(
            group, m.TIMEINDEX, noruleinit=True
        )
        self.dr_storage_level_red_build = BuildAction(
            rule=dr_storage_limit_red_rule
        )

        # Equation 4.16
        def dr_storage_limit_inc_rule(block):
            """Fictious demand response storage level
            for load increase limit"""
            for p, t in m.TIMEINDEX:
                for g in group:
                    # fictious demand response load reduction storage level
                    lhs = self.dsm_up_level[g, t]

                    # maximum (time-dependent) available shifting capacity
                    rhs = g.capacity_up_mean * self.total[g, p] * g.shift_time

                    # add constraint
                    block.dr_storage_limit_inc.add((g, p, t), (lhs <= rhs))

        self.dr_storage_limit_inc = Constraint(
            group, m.TIMEINDEX, noruleinit=True
        )
        self.dr_storage_level_inc_build = BuildAction(
            rule=dr_storage_limit_inc_rule
        )

        # Equation 4.17' -> load shedding
        def dr_yearly_limit_shed_rule(block):
            """Introduce overall annual (energy) limit for load shedding
            resp. overall limit for optimization timeframe considered
            A year limit in contrast to Gils (2015) is defined a mandatory
            parameter here in order to achieve an approach comparable
            to the others.
            """
            for g in group:
                for p in m.PERIODS:
                    if g.shed_eligibility:
                        # sum of all load reductions
                        lhs = sum(
                            self.dsm_do_shed[g, t]
                            for pp, t in m.TIMEINDEX
                            if pp == p
                        )

                        # year limit
                        rhs = (
                            g.capacity_down_mean
                            * self.total[g, p]
                            * g.shed_time
                            * g.n_yearLimit_shed
                        )

                        # add constraint
                        block.dr_yearly_limit_shed.add((g, p), (lhs <= rhs))

        self.dr_yearly_limit_shed = Constraint(
            group, m.PERIODS, noruleinit=True
        )
        self.dr_yearly_limit_shed_build = BuildAction(
            rule=dr_yearly_limit_shed_rule
        )

        # ************* Optional Constraints *****************************

        # Equation 4.17
        def dr_yearly_limit_red_rule(block):
            """Introduce overall annual (energy) limit for load reductions
            resp. overall limit for optimization timeframe considered
            """
            for g in group:
                if g.ActivateYearLimit:
                    for p in m.PERIODS:
                        # sum of all load reductions
                        lhs = sum(
                            sum(
                                self.dsm_do_shift[g, h, t]
                                for h in g.delay_time
                            )
                            for pp, t in m.TIMEINDEX
                            if pp == p
                        )

                        # year limit
                        rhs = (
                            g.capacity_down_mean
                            * self.total[g, p]
                            * g.shift_time
                            * g.n_yearLimit_shift
                        )

                        # add constraint
                        block.dr_yearly_limit_red.add((g, p), (lhs <= rhs))

                else:
                    pass  # return(Constraint.Skip)

        self.dr_yearly_limit_red = Constraint(
            group, m.PERIODS, noruleinit=True
        )
        self.dr_yearly_limit_red_build = BuildAction(
            rule=dr_yearly_limit_red_rule
        )

        # Equation 4.18
        def dr_yearly_limit_inc_rule(block):
            """Introduce overall annual (energy) limit for load increases
            resp. overall limit for optimization timeframe considered
            """
            for g in group:
                if g.ActivateYearLimit:
                    for p in m.PERIODS:
                        # sum of all load increases
                        lhs = sum(
                            sum(self.dsm_up[g, h, t] for h in g.delay_time)
                            for pp, t in m.TIMEINDEX
                            if pp == p
                        )

                        # year limit
                        rhs = (
                            g.capacity_up_mean
                            * self.total[g, p]
                            * g.shift_time
                            * g.n_yearLimit_shift
                        )

                        # add constraint
                        block.dr_yearly_limit_inc.add((g, p), (lhs <= rhs))

                else:
                    pass  # return(Constraint.Skip)

        self.dr_yearly_limit_inc = Constraint(
            group, m.PERIODS, noruleinit=True
        )
        self.dr_yearly_limit_inc_build = BuildAction(
            rule=dr_yearly_limit_inc_rule
        )

        # Equation 4.19
        def dr_daily_limit_red_rule(block):
            """Introduce rolling (energy) limit for load reductions
            This effectively limits DR utilization dependent on
            activations within previous hours.
            """
            for p, t in m.TIMEINDEX:
                for g in group:
                    if g.ActivateDayLimit:
                        # main use case
                        if t >= g.t_dayLimit:
                            # load reduction
                            lhs = sum(
                                self.dsm_do_shift[g, h, t]
                                for h in g.delay_time
                            )

                            # daily limit
                            rhs = g.capacity_down_mean * self.total[
                                g, p
                            ] * g.shift_time - sum(
                                sum(
                                    self.dsm_do_shift[g, h, t - t_dash]
                                    for h in g.delay_time
                                )
                                for t_dash in range(1, int(g.t_dayLimit) + 1)
                            )

                            # add constraint
                            block.dr_daily_limit_red.add(
                                (g, p, t), (lhs <= rhs)
                            )

                        else:
                            pass  # return(Constraint.Skip)

                    else:
                        pass  # return(Constraint.Skip)

        self.dr_daily_limit_red = Constraint(
            group, m.TIMEINDEX, noruleinit=True
        )
        self.dr_daily_limit_red_build = BuildAction(
            rule=dr_daily_limit_red_rule
        )

        # Equation 4.20
        def dr_daily_limit_inc_rule(block):
            """Introduce rolling (energy) limit for load increases
            This effectively limits DR utilization dependent on
            activations within previous hours.
            """
            for p, t in m.TIMEINDEX:
                for g in group:
                    if g.ActivateDayLimit:
                        # main use case
                        if t >= g.t_dayLimit:
                            # load increase
                            lhs = sum(
                                self.dsm_up[g, h, t] for h in g.delay_time
                            )

                            # daily limit
                            rhs = g.capacity_up_mean * self.total[
                                g, p
                            ] * g.shift_time - sum(
                                sum(
                                    self.dsm_up[g, h, t - t_dash]
                                    for h in g.delay_time
                                )
                                for t_dash in range(1, int(g.t_dayLimit) + 1)
                            )

                            # add constraint
                            block.dr_daily_limit_inc.add(
                                (g, p, t), (lhs <= rhs)
                            )

                        else:
                            pass  # return(Constraint.Skip)

                    else:
                        pass  # return(Constraint.Skip)

        self.dr_daily_limit_inc = Constraint(
            group, m.TIMEINDEX, noruleinit=True
        )
        self.dr_daily_limit_inc_build = BuildAction(
            rule=dr_daily_limit_inc_rule
        )

        # Addition: avoid simultaneous activations
        def dr_logical_constraint_rule(block):
            """Similar to equation 10 from Zerrahn and Schill (2015):
            The sum of upwards and downwards shifts may not be greater
            than the (bigger) capacity limit.
            """
            for p, t in m.TIMEINDEX:
                for g in group:
                    if g.addition:
                        # sum of load increases and reductions
                        lhs = (
                            sum(
                                self.dsm_up[g, h, t]
                                + self.balance_dsm_do[g, h, t]
                                + self.dsm_do_shift[g, h, t]
                                + self.balance_dsm_up[g, h, t]
                                for h in g.delay_time
                            )
                            + self.dsm_do_shed[g, t]
                        )

                        # maximum capacity eligibly for load shifting
                        rhs = (
                            max(
                                g.capacity_down[t],
                                g.capacity_up[t],
                            )
                            * self.total[g, p]
                        )

                        # add constraint
                        block.dr_logical_constraint.add(
                            (g, p, t), (lhs <= rhs)
                        )

                    else:
                        pass  # return(Constraint.Skip)

        self.dr_logical_constraint = Constraint(
            group, m.TIMEINDEX, noruleinit=True
        )
        self.dr_logical_constraint_build = BuildAction(
            rule=dr_logical_constraint_rule
        )

        if m.es.periods is not None:

            def _overall_dsm_maximum_investflow_rule(block):
                """Rule definition for maximum overall investment
                in investment case.
                """
                for g in self.OVERALL_MAXIMUM_INVESTDSM:
                    for p in m.PERIODS:
                        expr = self.total[g, p] <= g.investment.overall_maximum
                        self.overall_dsm_maximum.add((g, p), expr)

            self.overall_dsm_maximum = Constraint(
                self.OVERALL_MAXIMUM_INVESTDSM, m.PERIODS, noruleinit=True
            )

            self.overall_maximum_build = BuildAction(
                rule=_overall_dsm_maximum_investflow_rule
            )

            def _overall_minimum_dsm_investflow_rule(block):
                """Rule definition for minimum overall investment
                in investment case.

                Note: This is only applicable for the last period
                """
                for g in self.OVERALL_MINIMUM_INVESTDSM:
                    expr = (
                        g.investment.overall_minimum
                        <= self.total[g, m.PERIODS.at(-1)]
                    )
                    self.overall_minimum.add(g, expr)

            self.overall_minimum = Constraint(
                self.OVERALL_MINIMUM_INVESTDSM, noruleinit=True
            )

            self.overall_minimum_build = BuildAction(
                rule=_overall_minimum_dsm_investflow_rule
            )

    def _objective_expression(self):
        r"""Objective expression with variable and investment costs for DSM;
        Equation 4.23 from Gils (2015)
        """
        m = self.parent_block()

        investment_costs = 0
        period_investment_costs = {p: 0 for p in m.PERIODS}
        variable_costs = 0
        fixed_costs = 0

        if m.es.periods is None:
            for g in self.INVESTDR:
                for p in m.PERIODS:
                    if g.investment.ep_costs is not None:
                        investment_costs += (
                            self.invest[g, p] * g.investment.ep_costs[p]
                        )
                    else:
                        raise ValueError("Missing value for investment costs!")

                for t in m.TIMESTEPS:
                    variable_costs += (
                        sum(
                            self.dsm_up[g, h, t] + self.balance_dsm_do[g, h, t]
                            for h in g.delay_time
                        )
                        * g.cost_dsm_up[t]
                        * m.objective_weighting[t]
                    )
                    variable_costs += (
                        sum(
                            self.dsm_do_shift[g, h, t]
                            + self.balance_dsm_up[g, h, t]
                            for h in g.delay_time
                        )
                        * g.cost_dsm_down_shift[t]
                        + self.dsm_do_shed[g, t] * g.cost_dsm_down_shed[t]
                    ) * m.objective_weighting[t]

        else:
            msg = (
                "You did not specify an interest rate.\n"
                "It will be set equal to the discount_rate of {} "
                "of the model as a default.\nThis corresponds to a "
                "social planner point of view and does not reflect "
                "microeconomic interest requirements."
            )
            for g in self.INVESTDR:
                if g.investment.ep_costs is not None:
                    lifetime = g.investment.lifetime
                    interest = 0
                    if interest == 0:
                        warn(
                            msg.format(m.discount_rate),
                            debugging.SuspiciousUsageWarning,
                        )
                        interest = m.discount_rate
                    for p in m.PERIODS:
                        annuity = economics.annuity(
                            capex=g.investment.ep_costs[p],
                            n=lifetime,
                            wacc=interest,
                        )
                        duration = min(
                            m.es.end_year_of_optimization
                            - m.es.periods_years[p],
                            lifetime,
                        )
                        present_value_factor = 1 / economics.annuity(
                            capex=1, n=duration, wacc=interest
                        )
                        investment_costs_increment = (
                            self.invest[g, p] * annuity * present_value_factor
                        )
                        remaining_value_difference = (
                            self._evaluate_remaining_value_difference(
                                m,
                                p,
                                g,
                                m.es.end_year_of_optimization,
                                lifetime,
                                interest,
                            )
                        )
                        investment_costs += (
                            investment_costs_increment
                            + remaining_value_difference
                        )
                        period_investment_costs[
                            p
                        ] += investment_costs_increment
                else:
                    raise ValueError("Missing value for investment costs!")

                for p, t in m.TIMEINDEX:
                    variable_costs += (
                        sum(
                            self.dsm_up[g, h, t] + self.balance_dsm_do[g, h, t]
                            for h in g.delay_time
                        )
                        * g.cost_dsm_up[t]
                    ) * m.objective_weighting[t]
                    variable_costs += (
                        sum(
                            self.dsm_do_shift[g, h, t]
                            + self.balance_dsm_up[g, h, t]
                            for h in g.delay_time
                        )
                        * g.cost_dsm_down_shift[t]
                        + self.dsm_do_shed[g, t] * g.cost_dsm_down_shed[t]
                    ) * m.objective_weighting[t]

                if valid_sequence(g.investment.fixed_costs, len(m.PERIODS)):
                    lifetime = g.investment.lifetime
                    for p in m.PERIODS:
                        range_limit = min(
                            m.es.end_year_of_optimization,
                            m.es.periods_years[p] + lifetime,
                        )
                        fixed_costs += sum(
                            self.invest[g, p] * g.investment.fixed_costs[pp]
                            for pp in range(
                                m.es.periods_years[p],
                                range_limit,
                            )
                        )

            for g in self.EXISTING_INVESTDSM:
                if valid_sequence(g.investment.fixed_costs, len(m.PERIODS)):
                    lifetime = g.investment.lifetime
                    age = g.investment.age
                    range_limit = min(
                        m.es.end_year_of_optimization, lifetime - age
                    )
                    fixed_costs += sum(
                        g.investment.existing * g.investment.fixed_costs[pp]
                        for pp in range(range_limit)
                    )

        self.variable_costs = Expression(expr=variable_costs)
        self.fixed_costs = Expression(expr=fixed_costs)
        self.investment_costs = Expression(expr=investment_costs)
        self.period_investment_costs = period_investment_costs
        self.costs = Expression(
            expr=investment_costs + variable_costs + fixed_costs
        )

        return self.costs

    def _evaluate_remaining_value_difference(
        self,
        m,
        p,
        g,
        end_year_of_optimization,
        lifetime,
        interest,
    ):
        """Evaluate and return the remaining value difference of an investment

        The remaining value difference in the net present values if the asset
        was to be liquidated at the end of the optimization horizon and the
        net present value using the original investment expenses.

        Parameters
        ----------
        m : oemof.solph.models.Model
            Optimization model

        p : int
            Period in which investment occurs

        g : oemof.solph.components.experimental.SinkDSM
            storage unit

        end_year_of_optimization : int
            Last year of the optimization horizon

        lifetime : int
            lifetime of investment considered

        interest : float
            Demanded interest rate for investment
        """
        if m.es.use_remaining_value:
            if end_year_of_optimization - m.es.periods_years[p] < lifetime:
                remaining_lifetime = lifetime - (
                    end_year_of_optimization - m.es.periods_years[p]
                )
                remaining_annuity = economics.annuity(
                    capex=g.investment.ep_costs[-1],
                    n=remaining_lifetime,
                    wacc=interest,
                )
                original_annuity = economics.annuity(
                    capex=g.investment.ep_costs[p],
                    n=remaining_lifetime,
                    wacc=interest,
                )
                present_value_factor_remaining = 1 / economics.annuity(
                    capex=1, n=remaining_lifetime, wacc=interest
                )
                return (
                    self.invest[g, p]
                    * (remaining_annuity - original_annuity)
                    * present_value_factor_remaining
                )
            else:
                return 0
        else:
            return 0
