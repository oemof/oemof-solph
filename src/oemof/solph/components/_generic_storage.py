# -*- coding: utf-8 -

"""
GenericStorage and associated individual constraints (blocks) and groupings.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: FranziPl
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: FabianTU
SPDX-FileCopyrightText: Johannes Röder
SPDX-FileCopyrightText: Ekaterina Zolotarevskaia
SPDX-FileCopyrightText: Johannes Kochems
SPDX-FileCopyrightText: Johannes Giehl
SPDX-FileCopyrightText: Raul Ciria Aylagas

SPDX-License-Identifier: MIT

"""
import math
import numbers
from warnings import warn

from oemof.network import Node
from pyomo.core.base.block import ScalarBlock
from pyomo.environ import Binary
from pyomo.environ import BuildAction
from pyomo.environ import Constraint
from pyomo.environ import Expression
from pyomo.environ import NonNegativeReals
from pyomo.environ import Set
from pyomo.environ import Var

from oemof.solph._helpers import check_node_object_for_missing_attribute
from oemof.solph._options import Investment
from oemof.solph._plumbing import sequence
from oemof.solph._plumbing import valid_sequence


class GenericStorage(Node):
    r"""
    Component `GenericStorage` to model with basic characteristics of storages.

    The GenericStorage is designed for one input and one output.

    Parameters
    ----------
    nominal_capacity : numeric, :math:`E_{nom}` or
            :class:`oemof.solph.options.Investment` object
        Absolute nominal capacity of the storage, fixed value or
        object describing parameter of investment optimisations.
    invest_relation_input_capacity : numeric (iterable or scalar) or None, :math:`r_{cap,in}`
        Ratio between the investment variable of the input Flow and the
        investment variable of the storage:
        :math:`\dot{E}_{in,invest} = E_{invest} \cdot r_{cap,in}`
    invest_relation_output_capacity : numeric (iterable or scalar) or None, :math:`r_{cap,out}`
        Ratio between the investment variable of the output Flow and the
        investment variable of the storage:
        :math:`\dot{E}_{out,invest} = E_{invest} \cdot r_{cap,out}`
    invest_relation_input_output : numeric (iterable or scalar) or None, :math:`r_{in,out}`
        Ratio between the investment variable of the output Flow and the
        investment variable of the input flow. This ratio used to fix the
        flow investments to each other.
        Values < 1 set the input flow lower than the output and > 1 will
        set the input flow higher than the output flow. If None no relation
        will be set:
        :math:`\dot{E}_{in,invest} = \dot{E}_{out,invest} \cdot r_{in,out}`
    initial_storage_level : numeric, :math:`c(-1)`
        The relative storage content in the timestep before the first
        time step of optimization (between 0 and 1).

        Note: When investment mode is used in a multi-period model,
        `initial_storage_level` is not supported.
        Storage output is forced to zero until the storage unit is invested in.
    balanced : boolean
        Couple storage level of first and last time step.
        (Total inflow and total outflow are balanced.)
    loss_rate : numeric (iterable or scalar)
        The relative loss of the storage content per hour.
    fixed_losses_relative : numeric (iterable or scalar), :math:`\gamma(t)`
        Losses per hour that are independent of the storage content but
        proportional to nominal storage capacity.

        Note: Fixed losses are not supported in investment mode.
    fixed_losses_absolute : numeric (iterable or scalar), :math:`\delta(t)`
        Losses per hour that are independent of storage content and independent
        of nominal storage capacity.

        Note: Fixed losses are not supported in investment mode.
    inflow_conversion_factor : numeric (iterable or scalar), :math:`\eta_i(t)`
        The relative conversion factor, i.e. efficiency associated with the
        inflow of the storage.
    outflow_conversion_factor : numeric (iterable or scalar), :math:`\eta_o(t)`
        see: inflow_conversion_factor
    min_storage_level : numeric (iterable or scalar), :math:`c_{min}(t)`
        The normed minimum storage content as fraction of the
        nominal storage capacity or the capacity that has been invested into
        (between 0 and 1).
        To set different values in every time step use a sequence.
    max_storage_level : numeric (iterable or scalar), :math:`c_{max}(t)`
        see: min_storage_level
    storage_costs : numeric (iterable or scalar), :math:`c_{storage}(t)`
        Cost (per energy) for having energy in the storage, starting from
        time point :math:`t_{1}`. (:math:`t_{0}` is left out to avoid counting
        it twice if balanced=True.)
    lifetime_inflow : int, :math:`n_{in}`
        Determine the lifetime of an inflow; only applicable for multi-period
        models which can invest in storage capacity and have an
        invest_relation_input_capacity defined
    lifetime_outflow : int, :math:`n_{in}`
        Determine the lifetime of an outflow; only applicable for multi-period
        models which can invest in storage capacity and have an
        invest_relation_output_capacity defined

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.components._generic_storage.GenericStorageBlock`
       (if no Investment object present)
     * :py:class:`~oemof.solph.components._generic_storage.GenericInvestmentStorageBlock`
       (if Investment object present)

    Examples
    --------
    Basic usage examples of the GenericStorage with a random selection of
    attributes. See the Flow class for all Flow attributes.

    >>> from oemof import solph

    >>> my_bus = solph.buses.Bus('my_bus')

    >>> my_storage = solph.components.GenericStorage(
    ...     label='storage',
    ...     nominal_capacity=1000,
    ...     inputs={my_bus: solph.flows.Flow(nominal_capacity=200, variable_costs=10)},
    ...     outputs={my_bus: solph.flows.Flow(nominal_capacity=200)},
    ...     loss_rate=0.01,
    ...     initial_storage_level=0,
    ...     max_storage_level = 0.9,
    ...     inflow_conversion_factor=0.9,
    ...     outflow_conversion_factor=0.93)

    >>> my_investment_storage = solph.components.GenericStorage(
    ...     label='storage',
    ...     nominal_capacity=solph.Investment(ep_costs=50),
    ...     inputs={my_bus: solph.flows.Flow()},
    ...     outputs={my_bus: solph.flows.Flow()},
    ...     loss_rate=0.02,
    ...     initial_storage_level=None,
    ...     invest_relation_input_capacity=1/6,
    ...     invest_relation_output_capacity=1/6,
    ...     inflow_conversion_factor=1,
    ...     outflow_conversion_factor=0.8)
    """  # noqa: E501

    def __init__(
        self,
        label=None,
        inputs=None,
        outputs=None,
        parent_node=None,
        nominal_capacity=None,
        nominal_storage_capacity=None,  # Can be removed for versions >= v0.7
        initial_storage_level=None,
        invest_relation_input_output=None,
        invest_relation_input_capacity=None,
        invest_relation_output_capacity=None,
        min_storage_level=0,
        max_storage_level=1,
        balanced=True,
        loss_rate=0,
        fixed_losses_relative=0,
        fixed_losses_absolute=0,
        inflow_conversion_factor=1,
        outflow_conversion_factor=1,
        storage_costs=None,
        lifetime_inflow=None,
        lifetime_outflow=None,
        custom_attributes=None,
    ):
        if inputs is None:
            inputs = {}
        if outputs is None:
            outputs = {}
        if custom_attributes is None:
            custom_attributes = {}
        super().__init__(
            label,
            inputs=inputs,
            outputs=outputs,
            parent_node=parent_node,
            custom_properties=custom_attributes,
        )
        # --- BEGIN: The following code can be removed for versions >= v0.7 ---
        if nominal_storage_capacity is not None:
            msg = (
                "For backward compatibility,"
                + " the option nominal_storage_capacity overwrites the option"
                + " nominal_capacity."
                + " Both options cannot be set at the same time."
            )
            if nominal_capacity is not None:
                raise AttributeError(msg)
            else:
                warn(msg, FutureWarning)
            nominal_capacity = nominal_storage_capacity
        # --- END ---

        self.nominal_storage_capacity = None
        self.investment = None
        self._invest_group = False
        if isinstance(nominal_capacity, numbers.Real):
            self.nominal_storage_capacity = nominal_capacity
        elif isinstance(nominal_capacity, Investment):
            self.investment = nominal_capacity
            self._invest_group = True

        self.initial_storage_level = initial_storage_level
        self.balanced = balanced
        self.loss_rate = sequence(loss_rate)
        self.fixed_losses_relative = sequence(fixed_losses_relative)
        self.fixed_losses_absolute = sequence(fixed_losses_absolute)
        self.inflow_conversion_factor = sequence(inflow_conversion_factor)
        self.outflow_conversion_factor = sequence(outflow_conversion_factor)
        self.max_storage_level = sequence(max_storage_level)
        self.min_storage_level = sequence(min_storage_level)
        self.storage_costs = sequence(storage_costs)
        self.invest_relation_input_output = sequence(
            invest_relation_input_output
        )
        self.invest_relation_input_capacity = sequence(
            invest_relation_input_capacity
        )
        self.invest_relation_output_capacity = sequence(
            invest_relation_output_capacity
        )
        self.lifetime_inflow = lifetime_inflow
        self.lifetime_outflow = lifetime_outflow

        # Check number of flows.
        self._check_number_of_flows()
        # Check for infeasible parameter combinations
        self._check_infeasible_parameter_combinations()

        if self._invest_group:
            self._check_invest_attributes()

    def _set_flows(self):
        """Define inflow / outflow as investment flows when they are
        coupled with storage capacity via invest relations
        """
        for flow in self.inputs.values():
            if self.invest_relation_input_capacity[
                0
            ] is not None and not isinstance(flow.investment, Investment):
                flow.investment = Investment()
        for flow in self.outputs.values():
            if self.invest_relation_output_capacity[
                0
            ] is not None and not isinstance(flow.investment, Investment):
                flow.investment = Investment()

    def _check_invest_attributes(self):
        """Raise errors for infeasible investment attribute combinations"""
        if (
            self.invest_relation_input_output[0] is not None
            and self.invest_relation_output_capacity[0] is not None
            and self.invest_relation_input_capacity[0] is not None
        ):
            e2 = (
                "Overdetermined. Three investment object will be coupled"
                "with three constraints. Set one invest relation to 'None'."
            )
            raise AttributeError(e2)
        if (
            self.investment
            and self.fixed_losses_absolute.max() != 0
            and self.investment.existing == 0
            and self.investment.minimum.min() == 0
        ):
            e3 = (
                "With fixed_losses_absolute > 0, either investment.existing "
                "or investment.minimum has to be non-zero."
            )
            raise AttributeError(e3)

        self._set_flows()

    def _check_number_of_flows(self):
        """Ensure that there is only one inflow and outflow to the storage"""
        msg = "Only one {0} flow allowed in the GenericStorage {1}."
        check_node_object_for_missing_attribute(self, "inputs")
        check_node_object_for_missing_attribute(self, "outputs")
        if len(self.inputs) > 1:
            raise AttributeError(msg.format("input", self.label))
        if len(self.outputs) > 1:
            raise AttributeError(msg.format("output", self.label))

    def _check_infeasible_parameter_combinations(self):
        """Check for infeasible parameter combinations and raise error"""
        msg = (
            "initial_storage_level must be greater or equal to "
            "min_storage_level and smaller or equal to "
            "max_storage_level."
        )
        if self.initial_storage_level is not None:
            if (
                self.initial_storage_level < self.min_storage_level[0]
                or self.initial_storage_level > self.max_storage_level[0]
            ):
                raise ValueError(msg)

    def constraint_group(self):
        if self._invest_group is True:
            return GenericInvestmentStorageBlock
        else:
            return GenericStorageBlock


class GenericStorageBlock(ScalarBlock):
    r"""Storage without an :class:`.Investment` object.

    **The following sets are created:** (-> see basic sets at
    :class:`.Model` )

    STORAGES
        A set with all :py:class:`~.GenericStorage` objects, which do not have an
        :attr:`investment` of type :class:`.Investment`.

    STORAGES_BALANCED
        A set of  all :py:class:`~.GenericStorage` objects, with 'balanced' attribute set
        to True.

    STORAGES_WITH_INVEST_FLOW_REL
        A set with all :py:class:`~.GenericStorage` objects with two investment
        flows coupled with the 'invest_relation_input_output' attribute.

    **The following variables are created:**

    storage_content
        Storage content for every storage and timestep. The value for the
        storage content at the beginning is set by the parameter
        `initial_storage_level` or not set if `initial_storage_level` is None.
        The variable of storage s and timestep t can be accessed by:
        `om.GenericStorageBlock.storage_content[s, t]`

    intra_storage_delta
        Storage content for every storage and timestep of typical periods
        (only used in TSAM-mode). The variable of storage s and timestep t can
        be accessed by: `om.GenericStorageBlock.intra_storage_delta[s, k, t]`

    **The following constraints are created:**

    Set storage_content of last time step to one at t=0 if balanced == True
        .. math::
            E(t_{last}) = E(-1)

    Storage losses :attr:`om.Storage.losses[n, t]`
        .. math:: E_{loss}(t) = &E(t-1) \cdot
            1 - (1 - \beta(t))^{\tau(t)/(t_u)} \\
            &- \gamma(t)\cdot E_{nom} \cdot {\tau(t)/(t_u)}\\
            &- \delta(t) \cdot {\tau(t)/(t_u)}

    Storage balance :attr:`om.Storage.balance[n, t]`
        .. math:: E(t) = &E(t-1) - E_{loss}(t)\\
            &- \frac{\dot{E}_o(p, t)}{\eta_o(t)} \cdot \tau(t)\\
            &+ \dot{E}_i(p, t) \cdot \eta_i(t) \cdot \tau(t)

    Connect the invest variables of the input and the output flow.
        .. math::
          InvestmentFlowBlock.invest(source(n), n, p) + existing = \\
          (InvestmentFlowBlock.invest(n, target(n), p) + existing) \\
          * invest\_relation\_input\_output(n) \\
          \forall n \in \textrm{INVEST\_REL\_IN\_OUT} \\
          \forall p \in \textrm{CAPACITY_PERIODS}



    =========================== ======================= =========
    symbol                      explanation             attribute
    =========================== ======================= =========
    :math:`E(t)`                energy currently stored `storage_content`
    :math:`E_{nom}`             nominal capacity of     `nominal_storage_capacity`
                                the energy storage
    :math:`c(-1)`               state before            `initial_storage_level`
                                initial time step
    :math:`c_{min}(t)`          minimum allowed storage `min_storage_level[t]`
    :math:`c_{max}(t)`          maximum allowed storage `max_storage_level[t]`
    :math:`\beta(t)`            fraction of lost energy `loss_rate[t]`
                                as share of
                                :math:`E(t)` per hour
    :math:`\gamma(t)`           fixed loss of energy    `fixed_losses_relative[t]`
                                per hour relative to
                                :math:`E_{nom}`
    :math:`\delta(t)`           absolute fixed loss     `fixed_losses_absolute[t]`
                                of energy per hour
    :math:`\dot{E}_i(t)`        energy flowing in       `inputs`
    :math:`\dot{E}_o(t)`        energy flowing out      `outputs`
    :math:`\eta_i(t)`           conversion factor       `inflow_conversion_factor[t]`
                                (i.e. efficiency)
                                when storing energy
    :math:`\eta_o(t)`           conversion factor when  `outflow_conversion_factor[t]`
                                (i.e. efficiency)
                                taking stored energy
    :math:`\tau(t)`             duration of time step
    :math:`t_u`                 time unit of losses
                                :math:`\beta(t)`,
                                :math:`\gamma(t)`
                                :math:`\delta(t)` and
                                timeincrement
                                :math:`\tau(t)`
    :math:`c_{storage}(t)`      costs of having         `storage_costs`
                                energy stored
    =========================== ======================= =========

    **The following parts of the objective function are created:**

    * :attr: `storage_costs` not 0

        .. math::
            \sum_{t \in \textrm{TIMEPOINTS} > 0} c_{storage}(t) \cdot E(t)

    """  # noqa: E501

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """
        Parameters
        ----------
        group : list
            List containing storage objects.
            e.g. groups=[storage1, storage2,..]
        """
        m = self.parent_block()

        if group is None:
            return None

        i = {n: [i for i in n.inputs][0] for n in group}
        o = {n: [o for o in n.outputs][0] for n in group}

        #  ************* SETS *********************************

        self.STORAGES = Set(initialize=[n for n in group])

        self.STORAGES_BALANCED = Set(
            initialize=[n for n in group if n.balanced is True]
        )

        self.STORAGES_INITITAL_LEVEL = Set(
            initialize=[
                n for n in group if n.initial_storage_level is not None
            ]
        )

        self.STORAGES_WITH_INVEST_FLOW_REL = Set(
            initialize=[
                n
                for n in group
                if n.invest_relation_input_output[0] is not None
            ]
        )

        #  ************* VARIABLES *****************************

        def _storage_content_bound_rule(block, n, t):
            """
            Rule definition for bounds of storage_content variable of
            storage n in timestep t.
            """
            bounds = (
                n.nominal_storage_capacity * n.min_storage_level[t],
                n.nominal_storage_capacity * n.max_storage_level[t],
            )
            return bounds

        if not m.TSAM_MODE:
            self.storage_content = Var(
                self.STORAGES, m.TIMEPOINTS, bounds=_storage_content_bound_rule
            )

            self.storage_losses = Var(self.STORAGES, m.TIMESTEPS)

            # set the initial storage content
            # ToDo: More elegant code possible?
            for n in group:
                if n.initial_storage_level is not None:
                    self.storage_content[n, 0] = (
                        n.initial_storage_level * n.nominal_storage_capacity
                    )
                    self.storage_content[n, 0].fix()
        else:
            # called "inter" in https://doi.org/10.1016/j.apenergy.2018.01.023
            self.inter_storage_content = Var(
                self.STORAGES, m.CLUSTERS_OFFSET, within=NonNegativeReals
            )
            # called "intra" in https://doi.org/10.1016/j.apenergy.2018.01.023
            self.intra_storage_delta = Var(
                self.STORAGES, m.TIMEINDEX_TYPICAL_CLUSTER_OFFSET
            )
            # set the initial intra storage content
            # first timestep in intra storage is always zero
            for n in group:
                for p, k in m.TYPICAL_CLUSTERS:
                    self.intra_storage_delta[n, p, k, 0] = 0
                    self.intra_storage_delta[n, p, k, 0].fix()
                if n.initial_storage_level is not None:
                    self.inter_storage_content[n, 0] = (
                        n.initial_storage_level * n.nominal_storage_capacity
                    )
                    self.inter_storage_content[n, 0].fix()
        #  ************* Constraints ***************************

        def _storage_inter_minimum_level_rule(block):
            # See FINE implementation at
            # https://github.com/FZJ-IEK3-VSA/FINE/blob/
            # 57ec32561fb95e746c505760bd0d61c97d2fd2fb/FINE/storage.py#L1329
            for n in self.STORAGES:
                for p, i, g in m.TIMEINDEX_CLUSTER:
                    t = m.get_timestep_from_tsam_timestep(p, i, g)
                    lhs = n.nominal_storage_capacity * n.min_storage_level[t]
                    k = m.es.tsa_parameters[p]["order"][i]
                    tk = m.get_timestep_from_tsam_timestep(p, k, g)
                    inter_i = (
                        sum(
                            len(m.es.tsa_parameters[ip]["order"])
                            for ip in range(p)
                        )
                        + i
                    )
                    rhs = (
                        self.inter_storage_content[n, inter_i]
                        * (1 - n.loss_rate[t]) ** (g * m.timeincrement[tk])
                        + self.intra_storage_delta[n, p, k, g]
                    )
                    self.storage_inter_minimum_level.add(
                        (n, p, i, g), lhs <= rhs
                    )

        if m.TSAM_MODE:
            self.storage_inter_minimum_level = Constraint(
                self.STORAGES, m.TIMEINDEX_CLUSTER, noruleinit=True
            )

            self.storage_inter_minimum_level_build = BuildAction(
                rule=_storage_inter_minimum_level_rule
            )

        def _storage_inter_maximum_level_rule(block):
            for n in self.STORAGES:
                for p, i, g in m.TIMEINDEX_CLUSTER:
                    t = m.get_timestep_from_tsam_timestep(p, i, g)
                    k = m.es.tsa_parameters[p]["order"][i]
                    tk = m.get_timestep_from_tsam_timestep(p, k, g)
                    inter_i = (
                        sum(
                            len(m.es.tsa_parameters[ip]["order"])
                            for ip in range(p)
                        )
                        + i
                    )
                    lhs = (
                        self.inter_storage_content[n, inter_i]
                        * (1 - n.loss_rate[t]) ** (g * m.timeincrement[tk])
                        + self.intra_storage_delta[n, p, k, g]
                    )
                    rhs = n.nominal_storage_capacity * n.max_storage_level[t]
                    self.storage_inter_maximum_level.add(
                        (n, p, i, g), lhs <= rhs
                    )

        if m.TSAM_MODE:
            self.storage_inter_maximum_level = Constraint(
                self.STORAGES, m.TIMEINDEX_CLUSTER, noruleinit=True
            )

            self.storage_inter_maximum_level_build = BuildAction(
                rule=_storage_inter_maximum_level_rule
            )

        def _storage_losses_rule(block, n, t):
            expr = block.storage_content[n, t] * (
                1 - (1 - n.loss_rate[t]) ** m.timeincrement[t]
            )
            expr += (
                n.fixed_losses_relative[t]
                * n.nominal_storage_capacity
                * m.timeincrement[t]
            )
            expr += n.fixed_losses_absolute[t] * m.timeincrement[t]

            return expr == block.storage_losses[n, t]

        if not m.TSAM_MODE:
            self.losses = Constraint(
                self.STORAGES, m.TIMESTEPS, rule=_storage_losses_rule
            )

        def _storage_balance_rule(block, n, t):
            """
            Rule definition for the storage balance of every storage n and
            every timestep.
            """
            expr = block.storage_content[n, t]
            expr -= block.storage_losses[n, t]
            expr += (
                m.flow[i[n], n, t] * n.inflow_conversion_factor[t]
            ) * m.timeincrement[t]
            expr -= (
                m.flow[n, o[n], t] / n.outflow_conversion_factor[t]
            ) * m.timeincrement[t]
            return expr == block.storage_content[n, t + 1]

        def _intra_storage_balance_rule(block, n, p, k, g):
            """
            Rule definition for the storage balance of every storage n and
            every timestep.
            """
            t = m.get_timestep_from_tsam_timestep(p, k, g)
            expr = 0
            expr += block.intra_storage_delta[n, p, k, g + 1]
            expr += (
                -block.intra_storage_delta[n, p, k, g]
                * (1 - n.loss_rate[t]) ** m.timeincrement[t]
            )
            expr += (
                n.fixed_losses_relative[t]
                * n.nominal_storage_capacity
                * m.timeincrement[t]
            )
            expr += n.fixed_losses_absolute[t] * m.timeincrement[t]
            expr += (
                -m.flow[i[n], n, t] * n.inflow_conversion_factor[t]
            ) * m.timeincrement[t]
            expr += (
                m.flow[n, o[n], t] / n.outflow_conversion_factor[t]
            ) * m.timeincrement[t]
            return expr == 0

        if not m.TSAM_MODE:
            self.balance = Constraint(
                self.STORAGES, m.TIMESTEPS, rule=_storage_balance_rule
            )
        else:
            self.intra_balance = Constraint(
                self.STORAGES,
                m.TIMEINDEX_TYPICAL_CLUSTER,
                rule=_intra_storage_balance_rule,
            )

        def _inter_storage_balance_rule(block, n, i):
            """
            Rule definition for the storage balance of every storage n and
            every timestep.
            """
            ii = 0
            for p in m.CAPACITY_PERIODS:
                ii += len(m.es.tsa_parameters[p]["order"])
                if ii > i:
                    ii -= len(m.es.tsa_parameters[p]["order"])
                    ii = i - ii
                    break

            k = m.es.tsa_parameters[p]["order"][ii]

            # Calculate inter losses over whole typical period
            t0 = m.get_timestep_from_tsam_timestep(p, k, 0)
            losses = math.prod(
                (
                    (1 - n.loss_rate[t0 + s])
                    ** m.es.tsa_parameters[p]["segments"][(k, s)]
                    if "segments" in m.es.tsa_parameters[p]
                    else 1 - n.loss_rate[t0 + s]
                )
                for s in range(m.es.tsa_parameters[p]["timesteps"])
            )

            expr = 0
            expr += block.inter_storage_content[n, i + 1]
            expr += -block.inter_storage_content[n, i] * losses
            expr += -self.intra_storage_delta[
                n, p, k, m.es.tsa_parameters[p]["timesteps"]
            ]
            return expr == 0

        if m.TSAM_MODE:
            self.inter_balance = Constraint(
                self.STORAGES,
                m.CLUSTERS,
                rule=_inter_storage_balance_rule,
            )

        def _balanced_storage_rule(block, n):
            """
            Storage content of last time step == initial storage content
            if balanced.
            """
            return (
                block.storage_content[n, m.TIMEPOINTS.at(-1)]
                == block.storage_content[n, m.TIMEPOINTS.at(1)]
            )

        def _balanced_inter_storage_rule(block, n):
            """
            Storage content of last time step == initial storage content
            if balanced.
            """
            return (
                block.inter_storage_content[n, m.CLUSTERS_OFFSET.at(-1)]
                == block.inter_storage_content[n, m.CLUSTERS_OFFSET.at(1)]
            )

        if not m.TSAM_MODE:
            self.balanced_cstr = Constraint(
                self.STORAGES_BALANCED, rule=_balanced_storage_rule
            )
        else:
            self.balanced_cstr = Constraint(
                self.STORAGES_BALANCED, rule=_balanced_inter_storage_rule
            )

        def _power_coupled(_):
            """
            Rule definition for constraint to connect the input power
            and output power
            """
            for n in self.STORAGES_WITH_INVEST_FLOW_REL:
                for p in m.CAPACITY_PERIODS:
                    expr = (
                        m.InvestmentFlowBlock.total[n, o[n], p]
                    ) * n.invest_relation_input_output[p] == (
                        m.InvestmentFlowBlock.total[i[n], n, p]
                    )
                    self.power_coupled.add((n, p), expr)

        self.power_coupled = Constraint(
            self.STORAGES_WITH_INVEST_FLOW_REL,
            m.CAPACITY_PERIODS,
            noruleinit=True,
        )

        self.power_coupled_build = BuildAction(rule=_power_coupled)

    def _objective_expression(self):
        r"""
        Objective expression for storages with no investment.

        * Fixed costs (will not have an impact on the actual optimisation).
        * Variable costs for storage content.
        """
        m = self.parent_block()

        storage_costs = 0

        for n in self.STORAGES:
            if valid_sequence(n.storage_costs, len(m.TIMESTEPS)):
                # We actually want to iterate over all TIMEPOINTS except the
                # 0th. As integers are used for the index, this is equicalent
                # to iterating over the TIMESTEPS with one offset.
                if not m.TSAM_MODE:
                    for t in m.TIMESTEPS:
                        storage_costs += (
                            self.storage_content[n, t + 1] * n.storage_costs[t]
                        )
                else:
                    for t in m.TIMESTEPS_ORIGINAL:
                        storage_costs += (
                            self.storage_content[n, t + 1]
                            * n.storage_costs[t + 1]
                        )

        self.storage_costs = Expression(expr=storage_costs)
        self.costs = Expression(expr=storage_costs)

        return self.costs


class GenericInvestmentStorageBlock(ScalarBlock):
    r"""
    Block for all storages with :attr:`Investment` being not None.
    See :class:`.Investment` for all parameters of the
    Investment class.

    **Variables**

    All Storages are indexed by :math:`n` (denoting the respective storage
    unit), which is omitted in the following for the sake of convenience.
    The following variables are created as attributes of
    :attr:`om.GenericInvestmentStorageBlock`:

    * :math:`P_i(p, t)`

        Inflow of the storage
        (created in :class:`oemof.solph.models.Model`).

    * :math:`P_o(p, t)`

        Outflow of the storage
        (created in :class:`oemof.solph.models.Model`).

    * :math:`E(t)`

        Current storage content (Absolute level of stored energy).

    * :math:`E_{invest}(p)`

        Invested (nominal) capacity of the storage in period p.

    * :math:`E_{total}(p)`

        Total installed (nominal) capacity of the storage in period p.

    * :math:`E_{old}(p)`

        Old (nominal) capacity of the storage to be decommissioned in period p.

    * :math:`E_{old,exo}(p)`

        Exogenous old (nominal) capacity of the storage to be decommissioned
        in period p; existing capacity reaching its lifetime.

    * :math:`E_{old,endo}(p)`

        Endogenous old (nominal) capacity of the storage to be decommissioned
        in period p; endgenous investments reaching their lifetime.

    * :math:`E(-1)`

        Initial storage content (before timestep 0).
        Not applicable for a multi-period model.

    * :math:`b_{invest}(p)`

        Binary variable for the status of the investment, if
        :attr:`nonconvex` is `True`.

    **Constraints**

    The following constraints are created for all investment storages:

        Storage balance (Same as for :class:`.GenericStorageBlock`)

        .. math:: E(t) = &E(t-1) \cdot
            (1 - \beta(t)) ^{\tau(t)/(t_u)} \\
            &- \gamma(t)\cdot (E_{total}(p)) \cdot {\tau(t)/(t_u)}\\
            &- \delta(t) \cdot {\tau(t)/(t_u)}\\
            &- \frac{\dot{E}_o(p, t))}{\eta_o(t)} \cdot \tau(t)
            + \dot{E}_i(p, t) \cdot \eta_i(t) \cdot \tau(t)

        Total storage capacity (p > 0 for multi-period model only)

        .. math::
            &
            if \quad p=0:\\
            &
            E_{total}(p) = E_{exist} + E_{invest}(p)\\
            &\\
            &
            else:\\
            &
            E_{total}(p) = E_{total}(p-1) + E_{invest}(p) - E_{old}(p)\\
            &\\
            &
            \forall p \in \textrm{CAPACITY_PERIODS}

        Old storage capacity (p > 0 for multi-period model only)

        .. math::
            &
            E_{old}(p) = E_{old,exo}(p) + E_{old,end}(p)\\
            &\\
            &
            if \quad p=0:\\
            &
            E_{old,end}(p) = 0\\
            &\\
            &
            else \quad if \quad l \leq year(p):\\
            &
            E_{old,end}(p) = E_{invest}(p_{comm})\\
            &\\
            &
            else:\\
            &
            E_{old,end}(p)\\
            &\\
            &
            if \quad p=0:\\
            &
            E_{old,exo}(p) = 0\\
            &\\
            &
            else \quad if \quad l - a \leq year(p):\\
            &
            E_{old,exo}(p) = E_{exist} (*)\\
            &\\
            &
            else:\\
            &
            E_{old,exo}(p) = 0\\
            &\\
            &
            \forall p \in \textrm{CAPACITY_PERIODS}

        where:

        * (*) is only performed for the first period the condition is True.
          A decommissioning flag is then set to True to prevent having falsely
          added old capacity in future periods.
        * :math:`year(p)` is the year corresponding to period p
        * :math:`p_{comm}` is the commissioning period of the storage

    Depending on the attribute :attr:`nonconvex`, the constraints for the
    bounds of the decision variable :math:`E_{invest}(p)` are different:\

        * :attr:`nonconvex = False`

        .. math::
            &
            E_{invest, min}(p) \le E_{invest}(p) \le E_{invest, max}(p) \\
            &
            \forall p \in \textrm{CAPACITY_PERIODS}

        * :attr:`nonconvex = True`

        .. math::
            &
            E_{invest, min}(p) \cdot b_{invest}(p) \le E_{invest}(p)\\
            &
            E_{invest}(p) \le E_{invest, max}(p) \cdot b_{invest}(p)\\
            &
            \forall p \in \textrm{CAPACITY_PERIODS}

    The following constraints are created depending on the attributes of
    the :class:`.GenericStorage`:

        * :attr:`initial_storage_level is None`;
          not applicable for multi-period model

            Constraint for a variable initial storage content:

        .. math::
               E(-1) \le E_{exist} + E_{invest}(0)

        * :attr:`initial_storage_level is not None`;
          not applicable for multi-period model

            An initial value for the storage content is given:

        .. math::
               E(-1) = (E_{invest}(0) + E_{exist}) \cdot c(-1)

        * :attr:`balanced=True`;
          not applicable for multi-period model

            The energy content of storage of the first and the last timestep
            are set equal:

        .. math::
            E(-1) = E(t_{last})

        * :attr:`invest_relation_input_capacity is not None`

            Connect the invest variables of the storage and the input flow:

        .. math::
            &
            P_{i,total}(p) =
            E_{total}(p) \cdot r_{cap,in} \\
            &
            \forall p \in \textrm{CAPACITY_PERIODS}

        * :attr:`invest_relation_output_capacity is not None`

            Connect the invest variables of the storage and the output flow:

        .. math::
            &
            P_{o,total}(p) =
            E_{total}(p) \cdot r_{cap,out}\\
            &
            \forall p \in \textrm{CAPACITY_PERIODS}

        * :attr:`invest_relation_input_output is not None`

            Connect the invest variables of the input and the output flow:

        .. math::
            &
            P_{i,total}(p) =
            P_{o,total}(p) \cdot r_{in,out}\\
            &
            \forall p \in \textrm{CAPACITY_PERIODS}

        * :attr:`max_storage_level`

            Rule for upper bound constraint for the storage content:

        .. math::
            &
            E(t) \leq E_{total}(p) \cdot c_{max}(t)\\
            &
            \forall p, t \in \textrm{TIMEINDEX}

        * :attr:`min_storage_level`

            Rule for lower bound constraint for the storage content:

        .. math::
            &
            E(t) \geq E_{total}(p) \cdot c_{min}(t)\\
            &
            \forall p, t \in \textrm{TIMEINDEX}


    **Objective function**

    Objective terms for a standard model and a multi-period model differ
    quite strongly. Besides, the part of the objective function added by the
    investment storages also depends on whether a convex or nonconvex
    investment option is selected. The following parts of the objective
    function are created:

    *Standard model*

        * :attr:`nonconvex = False`

            .. math::
                E_{invest}(0) \cdot c_{invest,var}(0)

        * :attr:`nonconvex = True`

            .. math::
                E_{invest}(0) \cdot c_{invest,var}(0)
                + c_{invest,fix}(0) \cdot b_{invest}(0)\\

    Where 0 denotes the 0th (investment) period since
    in a standard model, there is only this one period.

    *Multi-period model*

        * :attr:`nonconvex = False`

            .. math::
                &
                E_{invest}(p) \cdot A(c_{invest,var}(p), l, ir)
                \cdot \frac {1}{ANF(d, ir)} \cdot DF^{-p}\\
                &
                \forall p \in \textrm{CAPACITY_PERIODS}

        In case, the remaining lifetime of a storage is greater than 0 and
        attribute `use_remaining_value` of the energy system is True,
        the difference in value for the investment period compared to the
        last period of the optimization horizon is accounted for
        as an adder to the investment costs:

            .. math::
                &
                E_{invest}(p) \cdot (A(c_{invest,var}(p), l_{r}, ir) -
                A(c_{invest,var}(|P|), l_{r}, ir)\\
                & \cdot \frac {1}{ANF(l_{r}, ir)} \cdot DF^{-|P|}\\
                &\\
                &
                \forall p \in \textrm{CAPACITY_PERIODS}

        * :attr:`nonconvex = True`

            .. math::
                &
                (E_{invest}(p) \cdot A(c_{invest,var}(p), l, ir)
                \cdot \frac {1}{ANF(d, ir)}\\
                &
                +  c_{invest,fix}(p) \cdot b_{invest}(p)) \cdot DF^{-p} \\
                &
                \forall p \in \textrm{CAPACITY_PERIODS}

        In case, the remaining lifetime of a storage is greater than 0 and
        attribute `use_remaining_value` of the energy system is True,
        the difference in value for the investment period compared to the
        last period of the optimization horizon is accounted for
        as an adder to the investment costs:

            .. math::
                &
                (E_{invest}(p) \cdot (A(c_{invest,var}(p), l_{r}, ir) -
                A(c_{invest,var}(|P|), l_{r}, ir)\\
                & \cdot \frac {1}{ANF(l_{r}, ir)} \cdot DF^{-|P|}\\
                &
                +  (c_{invest,fix}(p) - c_{invest,fix}(|P|))
                \cdot b_{invest}(p)) \cdot DF^{-p}\\
                &\\
                &
                \forall p \in \textrm{CAPACITY_PERIODS}

    .. csv-table:: List of Variables
        :header: "symbol", "attribute", "explanation"
        :widths: 1, 1, 1

        ":math:`P_i(p, t)`", ":attr:`flow[i[n], n, p, t]`", "Inflow
        of the storage"
        ":math:`P_o(p, t)`", ":attr:`flow[n, o[n], p, t]`", "Outflow
        of the storage"
        ":math:`E(t)`", ":attr:`storage_content[n, t]`", "Current storage
        content (current absolute stored energy)"
        ":math:`E_{loss}(t)`", ":attr:`storage_losses[n, t]`", "Current storage
        losses (absolute losses per time step)"
        ":math:`E_{invest}(p)`", ":attr:`invest[n, p]`", "Invested (nominal)
        capacity of the storage"
        ":math:`E_{old}(p)`", ":attr:`old[n, p]`", "
        | Old (nominal) capacity of the storage
        | to be decommissioned in period p"
        ":math:`E_{old,exo}(p)`", ":attr:`old_exo[n, p]`", "
        | Old (nominal) capacity of the storage
        | to be decommissioned in period p
        | which was exogenously given by :math:`E_{exist}`"
        ":math:`E_{old,end}(p)`", ":attr:`old_end[n, p]`", "
        | Old (nominal) capacity of the storage
        | to be decommissioned in period p
        | which was endogenously determined by :math:`E_{invest}(p_{comm})`
        | where :math:`p_{comm}` is the commissioning period"
        ":math:`E(-1)`", ":attr:`init_cap[n]`", "Initial storage capacity
        (before timestep 0)"
        ":math:`b_{invest}(p)`", ":attr:`invest_status[i, o, p]`", "Binary
        variable for the status of investment"
        ":math:`P_{i,invest}(p)`", "
        :attr:`InvestmentFlowBlock.invest[i[n], n, p]`", "
        Invested (nominal) inflow (InvestmentFlowBlock)"
        ":math:`P_{o,invest}`", "
        :attr:`InvestmentFlowBlock.invest[n, o[n]]`", "
        Invested (nominal) outflow (InvestmentFlowBlock)"

    .. csv-table:: List of Parameters
        :header: "symbol", "attribute", "explanation"
        :widths: 1, 1, 1

        ":math:`E_{exist}`", "`flows[i, o].investment.existing`", "
        Existing storage capacity"
        ":math:`E_{invest,min}`", "`flows[i, o].investment.minimum`", "
        Minimum investment value"
        ":math:`E_{invest,max}`", "`flows[i, o].investment.maximum`", "
        Maximum investment value"
        ":math:`P_{i,exist}`", "`flows[i[n], n].investment.existing`
        ", "Existing inflow capacity"
        ":math:`P_{o,exist}`", "`flows[n, o[n]].investment.existing`
        ", "Existing outflow capacity"
        ":math:`c_{invest,var}`", "`flows[i, o].investment.ep_costs`
        ", "Variable investment costs"
        ":math:`c_{invest,fix}`", "`flows[i, o].investment.offset`", "
        Fix investment costs"
        ":math:`r_{cap,in}`", ":attr:`invest_relation_input_capacity`", "
        Relation of storage capacity and nominal inflow"
        ":math:`r_{cap,out}`", ":attr:`invest_relation_output_capacity`", "
        Relation of storage capacity and nominal outflow"
        ":math:`r_{in,out}`", ":attr:`invest_relation_input_output`", "
        Relation of nominal in- and outflow"
        ":math:`\beta(t)`", "`loss_rate[t]`", "Fraction of lost energy
        as share of :math:`E(t)` per hour"
        ":math:`\gamma(t)`", "`fixed_losses_relative[t]`", "Fixed loss
        of energy relative to :math:`E_{invest} + E_{exist}` per hour"
        ":math:`\delta(t)`", "`fixed_losses_absolute[t]`", "Absolute
        fixed loss of energy per hour"
        ":math:`\eta_i(t)`", "`inflow_conversion_factor[t]`", "
        Conversion factor (i.e. efficiency) when storing energy"
        ":math:`\eta_o(t)`", "`outflow_conversion_factor[t]`", "
        Conversion factor when (i.e. efficiency) taking stored energy"
        ":math:`c(-1)`", "`initial_storage_level`", "Initial relative
        storage content (before timestep 0)"
        ":math:`c_{max}`", "`flows[i, o].max[t]`", "Normed maximum
        value of storage content"
        ":math:`c_{min}`", "`flows[i, o].min[t]`", "Normed minimum
        value of storage content"
        ":math:`l`", "`flows[i, o].investment.lifetime`", "
        Lifetime for investments in storage capacity"
        ":math:`a`", "`flows[i, o].investment.age`", "
        Initial age of existing capacity / energy"
        ":math:`\tau(t)`", "", "Duration of time step"
        ":math:`t_u`", "", "Time unit of losses :math:`\beta(t)`,
        :math:`\gamma(t)`, :math:`\delta(t)` and timeincrement :math:`\tau(t)`"

    """

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group):
        """Create a storage block for investment modeling"""
        m = self.parent_block()

        # ########################## SETS #####################################

        self.INVESTSTORAGES = Set(initialize=[n for n in group])

        self.CONVEX_INVESTSTORAGES = Set(
            initialize=[n for n in group if n.investment.nonconvex is False]
        )

        self.NON_CONVEX_INVESTSTORAGES = Set(
            initialize=[n for n in group if n.investment.nonconvex is True]
        )

        self.INVESTSTORAGES_BALANCED = Set(
            initialize=[n for n in group if n.balanced is True]
        )

        self.INVESTSTORAGES_NO_INIT_CONTENT = Set(
            initialize=[n for n in group if n.initial_storage_level is None]
        )

        self.INVESTSTORAGES_INIT_CONTENT = Set(
            initialize=[
                n for n in group if n.initial_storage_level is not None
            ]
        )

        self.INVEST_REL_CAP_IN = Set(
            initialize=[
                n
                for n in group
                if n.invest_relation_input_capacity[0] is not None
            ]
        )

        self.INVEST_REL_CAP_OUT = Set(
            initialize=[
                n
                for n in group
                if n.invest_relation_output_capacity[0] is not None
            ]
        )

        self.INVEST_REL_IN_OUT = Set(
            initialize=[
                n
                for n in group
                if n.invest_relation_input_output[0] is not None
            ]
        )

        # The storage content is a non-negative variable, therefore it makes no
        # sense to create an additional constraint if the lower bound is zero
        # for all time steps.
        self.MIN_INVESTSTORAGES = Set(
            initialize=[
                n
                for n in group
                if sum([n.min_storage_level[t] for t in m.TIMESTEPS]) > 0
            ]
        )

        self.OVERALL_MAXIMUM_INVESTSTORAGES = Set(
            initialize=[
                n for n in group if n.investment.overall_maximum is not None
            ]
        )

        self.OVERALL_MINIMUM_INVESTSTORAGES = Set(
            initialize=[
                n for n in group if n.investment.overall_minimum is not None
            ]
        )

        self.EXISTING_INVESTSTORAGES = Set(
            initialize=[n for n in group if n.investment.existing is not None]
        )

        # ######################### Variables  ################################
        if not m.TSAM_MODE:
            self.storage_content = Var(
                self.INVESTSTORAGES, m.TIMEPOINTS, within=NonNegativeReals
            )
        else:
            self.inter_storage_content = Var(
                self.INVESTSTORAGES, m.CLUSTERS_OFFSET, within=NonNegativeReals
            )
            self.intra_storage_delta = Var(
                self.INVESTSTORAGES, m.TIMEINDEX_TYPICAL_CLUSTER_OFFSET
            )
            # set the initial intra storage content
            # first timestep in intra storage is always zero
            for n in group:
                for p, k in m.TYPICAL_CLUSTERS:
                    self.intra_storage_delta[n, p, k, 0] = 0
                    self.intra_storage_delta[n, p, k, 0].fix()

        def _storage_investvar_bound_rule(_, n, p):
            """
            Rule definition to bound the invested storage capacity `invest`.
            """
            if n in self.CONVEX_INVESTSTORAGES:
                return n.investment.minimum[p], n.investment.maximum[p]
            else:  # n in self.NON_CONVEX_INVESTSTORAGES
                return 0, n.investment.maximum[p]

        self.invest = Var(
            self.INVESTSTORAGES,
            m.CAPACITY_PERIODS,
            within=NonNegativeReals,
            bounds=_storage_investvar_bound_rule,
        )

        # Total capacity
        self.total = Var(
            self.INVESTSTORAGES,
            m.CAPACITY_PERIODS,
            within=NonNegativeReals,
            initialize=0,
        )

        # create status variable for a non-convex investment storage
        self.invest_status = Var(
            self.NON_CONVEX_INVESTSTORAGES, m.CAPACITY_PERIODS, within=Binary
        )

        # ######################### CONSTRAINTS ###############################
        i = {n: [i for i in n.inputs][0] for n in group}
        o = {n: [o for o in n.outputs][0] for n in group}

        def _total_storage_capacity_rule(block):
            """Rule definition for determining total installed
            capacity (taking decommissioning into account)
            """
            for n in self.INVESTSTORAGES:
                for p in m.CAPACITY_PERIODS:
                    if p == 0:
                        expr = (
                            self.total[n, p]
                            == self.invest[n, p] + n.investment.existing
                        )
                        self.total_storage_rule.add((n, p), expr)
                    else:
                        expr = (
                            self.total[n, p]
                            == self.invest[n, p] + self.total[n, p - 1]
                        )
                        self.total_storage_rule.add((n, p), expr)

        self.total_storage_rule = Constraint(
            self.INVESTSTORAGES, m.CAPACITY_PERIODS, noruleinit=True
        )

        self.total_storage_rule_build = BuildAction(
            rule=_total_storage_capacity_rule
        )

        def _inv_storage_init_content_max_rule(block, n):
            """Constraint for a variable initial storage capacity."""
            if not m.TSAM_MODE:
                lhs = block.storage_content[n, 0]
            else:
                lhs = block.intra_storage_delta[n, 0, 0, 0]
            return lhs <= n.investment.existing + block.invest[n, 0]

        self.init_content_limit = Constraint(
            self.INVESTSTORAGES_NO_INIT_CONTENT,
            rule=_inv_storage_init_content_max_rule,
        )

        def _inv_storage_init_content_fix_rule(block, n):
            """Constraint for a fixed initial storage capacity."""
            if not m.TSAM_MODE:
                lhs = block.storage_content[n, 0]
            else:
                lhs = block.intra_storage_delta[n, 0, 0, 0]
            return lhs == n.initial_storage_level * (
                n.investment.existing + block.invest[n, 0]
            )

        self.init_content_fix = Constraint(
            self.INVESTSTORAGES_INIT_CONTENT,
            rule=_inv_storage_init_content_fix_rule,
        )

        def _storage_balance_rule(block, n, p, t):
            """
            Rule definition for the storage balance of every storage n and
            every timestep.
            """
            expr = 0
            expr += block.storage_content[n, t + 1]
            expr += (
                -block.storage_content[n, t]
                * (1 - n.loss_rate[t]) ** m.timeincrement[t]
            )
            expr += (
                n.fixed_losses_relative[t]
                * self.total[n, p]
                * m.timeincrement[t]
            )
            expr += n.fixed_losses_absolute[t] * m.timeincrement[t]
            expr += (
                -m.flow[i[n], n, t] * n.inflow_conversion_factor[t]
            ) * m.timeincrement[t]
            expr += (
                m.flow[n, o[n], t] / n.outflow_conversion_factor[t]
            ) * m.timeincrement[t]
            return expr == 0

        def _intra_storage_balance_rule(block, n, p, k, g):
            """
            Rule definition for the storage balance of every storage n and
            every timestep.
            """
            t = m.get_timestep_from_tsam_timestep(p, k, g)
            expr = 0
            expr += block.intra_storage_delta[n, p, k, g + 1]
            expr += (
                -block.intra_storage_delta[n, p, k, g]
                * (1 - n.loss_rate[t]) ** m.timeincrement[t]
            )
            expr += (
                n.fixed_losses_relative[t]
                * self.total[n, p]
                * m.timeincrement[t]
            )
            expr += n.fixed_losses_absolute[t] * m.timeincrement[t]
            expr += (
                -m.flow[i[n], n, t] * n.inflow_conversion_factor[t]
            ) * m.timeincrement[t]
            expr += (
                m.flow[n, o[n], t] / n.outflow_conversion_factor[t]
            ) * m.timeincrement[t]
            return expr == 0

        if not m.TSAM_MODE:
            self.balance = Constraint(
                self.INVESTSTORAGES,
                m.TIMEINDEX,
                rule=_storage_balance_rule,
            )
        else:
            self.intra_balance = Constraint(
                self.INVESTSTORAGES,
                m.TIMEINDEX_TYPICAL_CLUSTER,
                rule=_intra_storage_balance_rule,
            )

        def _inter_storage_balance_rule(block, n, i):
            """
            Rule definition for the storage balance of every storage n and
            every timestep.
            """
            ii = 0
            for p in m.CAPACITY_PERIODS:
                ii += len(m.es.tsa_parameters[p]["order"])
                if ii > i:
                    ii -= len(m.es.tsa_parameters[p]["order"])
                    ii = i - ii
                    break

            k = m.es.tsa_parameters[p]["order"][ii]
            t = m.get_timestep_from_tsam_timestep(
                p, k, m.es.tsa_parameters[p]["timesteps"] - 1
            )
            expr = 0
            expr += block.inter_storage_content[n, i + 1]
            expr += -block.inter_storage_content[n, i] * (
                1 - n.loss_rate[t]
            ) ** (m.timeincrement[t] * m.es.tsa_parameters[p]["timesteps"])
            expr += -self.intra_storage_delta[
                n, p, k, m.es.tsa_parameters[p]["timesteps"]
            ]
            return expr == 0

        if m.TSAM_MODE:
            self.inter_balance = Constraint(
                self.INVESTSTORAGES,
                m.CLUSTERS,
                rule=_inter_storage_balance_rule,
            )

        if m.es.investment_times is None and not m.TSAM_MODE:

            def _balanced_storage_rule(block, n):
                return (
                    block.storage_content[n, m.TIMEPOINTS.at(-1)]
                    == block.storage_content[n, m.TIMEPOINTS.at(1)]
                )

            self.balanced_cstr = Constraint(
                self.INVESTSTORAGES_BALANCED, rule=_balanced_storage_rule
            )

        def _power_coupled(block):
            """
            Rule definition for constraint to connect the input power
            and output power
            """
            for n in self.INVEST_REL_IN_OUT:
                for p in m.CAPACITY_PERIODS:
                    expr = (
                        m.InvestmentFlowBlock.total[n, o[n], p]
                    ) * n.invest_relation_input_output[p] == (
                        m.InvestmentFlowBlock.total[i[n], n, p]
                    )
                    self.power_coupled.add((n, p), expr)

        self.power_coupled = Constraint(
            self.INVEST_REL_IN_OUT, m.CAPACITY_PERIODS, noruleinit=True
        )

        self.power_coupled_build = BuildAction(rule=_power_coupled)

        def _storage_capacity_inflow_invest_rule(block):
            """
            Rule definition of constraint connecting the inflow
            `InvestmentFlowBlock.invest of storage with invested capacity
            `invest` by nominal_storage_capacity__inflow_ratio
            """
            for n in self.INVEST_REL_CAP_IN:
                for p in m.CAPACITY_PERIODS:
                    expr = (
                        m.InvestmentFlowBlock.total[i[n], n, p]
                        == self.total[n, p]
                        * n.invest_relation_input_capacity[p]
                    )
                    self.storage_capacity_inflow.add((n, p), expr)

        self.storage_capacity_inflow = Constraint(
            self.INVEST_REL_CAP_IN, m.CAPACITY_PERIODS, noruleinit=True
        )

        self.storage_capacity_inflow_build = BuildAction(
            rule=_storage_capacity_inflow_invest_rule
        )

        def _storage_capacity_outflow_invest_rule(block):
            """
            Rule definition of constraint connecting outflow
            `InvestmentFlowBlock.invest` of storage and invested capacity
            `invest` by nominal_storage_capacity__outflow_ratio
            """
            for n in self.INVEST_REL_CAP_OUT:
                for p in m.CAPACITY_PERIODS:
                    expr = (
                        m.InvestmentFlowBlock.total[n, o[n], p]
                        == self.total[n, p]
                        * n.invest_relation_output_capacity[p]
                    )
                    self.storage_capacity_outflow.add((n, p), expr)

        self.storage_capacity_outflow = Constraint(
            self.INVEST_REL_CAP_OUT, m.CAPACITY_PERIODS, noruleinit=True
        )

        self.storage_capacity_outflow_build = BuildAction(
            rule=_storage_capacity_outflow_invest_rule
        )

        self._add_storage_limit_constraints()

        def maximum_invest_limit(block, n, p):
            """
            Constraint for the maximal investment in non convex investment
            storage.
            """
            return (
                n.investment.maximum[p] * self.invest_status[n, p]
                - self.invest[n, p]
            ) >= 0

        self.limit_max = Constraint(
            self.NON_CONVEX_INVESTSTORAGES,
            m.CAPACITY_PERIODS,
            rule=maximum_invest_limit,
        )

        def smallest_invest(block, n, p):
            """
            Constraint for the minimal investment in non convex investment
            storage if the invest is greater than 0. So the invest variable
            can be either 0 or greater than the minimum.
            """
            return (
                self.invest[n, p]
                - n.investment.minimum[p] * self.invest_status[n, p]
                >= 0
            )

        self.limit_min = Constraint(
            self.NON_CONVEX_INVESTSTORAGES,
            m.CAPACITY_PERIODS,
            rule=smallest_invest,
        )

        if m.es.investment_times is not None:

            def _overall_storage_maximum_investflow_rule(block):
                """Rule definition for maximum overall investment
                in investment case.
                """
                for n in self.OVERALL_MAXIMUM_INVESTSTORAGES:
                    for p in m.CAPACITY_PERIODS:
                        expr = self.total[n, p] <= n.investment.overall_maximum
                        self.overall_storage_maximum.add((n, p), expr)

            self.overall_storage_maximum = Constraint(
                self.OVERALL_MAXIMUM_INVESTSTORAGES,
                m.CAPACITY_PERIODS,
                noruleinit=True,
            )

            self.overall_maximum_build = BuildAction(
                rule=_overall_storage_maximum_investflow_rule
            )

            def _overall_minimum_investflow_rule(block):
                """Rule definition for minimum overall investment
                in investment case.

                Note: This is only applicable for the last period
                """
                for n in self.OVERALL_MINIMUM_INVESTSTORAGES:
                    expr = (
                        n.investment.overall_minimum
                        <= self.total[n, m.CAPACITY_PERIODS[-1]]
                    )
                    self.overall_minimum.add(n, expr)

            self.overall_minimum = Constraint(
                self.OVERALL_MINIMUM_INVESTSTORAGES, noruleinit=True
            )

            self.overall_minimum_build = BuildAction(
                rule=_overall_minimum_investflow_rule
            )

    def _add_storage_limit_constraints(self):
        m = self.parent_block()
        if not m.TSAM_MODE:

            def _max_storage_content_invest_rule(_, n, t):
                """
                Rule definition for upper bound constraint for the
                storage content.
                """
                expr = (
                    self.storage_content[n, t]
                    <= self.total[n, 0] * n.max_storage_level[t]
                )
                return expr

            self.max_storage_content = Constraint(
                self.INVESTSTORAGES,
                m.TIMEPOINTS,
                rule=_max_storage_content_invest_rule,
            )

            def _min_storage_content_invest_rule(_, n, t):
                """
                Rule definition of lower bound constraint for the
                storage content.
                """
                expr = (
                    self.storage_content[n, t]
                    >= self.total[n, 0] * n.min_storage_level[t]
                )
                return expr

            self.min_storage_content = Constraint(
                self.MIN_INVESTSTORAGES,
                m.TIMEPOINTS,
                rule=_min_storage_content_invest_rule,
            )
        else:

            def _storage_inter_maximum_level_rule(block):
                for n in self.INVESTSTORAGES:
                    for p, i, g in m.TIMEINDEX_CLUSTER:
                        t = m.get_timestep_from_tsam_timestep(p, i, g)
                        k = m.es.tsa_parameters[p]["order"][i]
                        tk = m.get_timestep_from_tsam_timestep(p, k, g)
                        inter_i = (
                            sum(
                                len(m.es.tsa_parameters[ip]["order"])
                                for ip in range(p)
                            )
                            + i
                        )
                        lhs = (
                            self.inter_storage_content[n, inter_i]
                            * (1 - n.loss_rate[t]) ** (g * m.timeincrement[tk])
                            + self.intra_storage_delta[n, p, k, g]
                        )
                        rhs = self.total[n, p] * n.max_storage_level[t]
                        self.storage_inter_maximum_level.add(
                            (n, p, i, g), lhs <= rhs
                        )

            self.storage_inter_maximum_level = Constraint(
                self.INVESTSTORAGES, m.TIMEINDEX_CLUSTER, noruleinit=True
            )

            self.storage_inter_maximum_level_build = BuildAction(
                rule=_storage_inter_maximum_level_rule
            )

            def _storage_inter_minimum_level_rule(block):
                # See FINE implementation at
                # https://github.com/FZJ-IEK3-VSA/FINE/blob/
                # 57ec32561fb95e746c505760bd0d61c97d2fd2fb/FINE/storage.py#L1329
                for n in self.INVESTSTORAGES:
                    for p, i, g in m.TIMEINDEX_CLUSTER:
                        t = m.get_timestep_from_tsam_timestep(p, i, g)
                        lhs = self.total[n, p] * n.min_storage_level[t]
                        k = m.es.tsa_parameters[p]["order"][i]
                        tk = m.get_timestep_from_tsam_timestep(p, k, g)
                        inter_i = (
                            sum(
                                len(m.es.tsa_parameters[ip]["order"])
                                for ip in range(p)
                            )
                            + i
                        )
                        rhs = (
                            self.inter_storage_content[n, inter_i]
                            * (1 - n.loss_rate[t]) ** (g * m.timeincrement[tk])
                            + self.intra_storage_delta[n, p, k, g]
                        )
                        self.storage_inter_minimum_level.add(
                            (n, p, i, g), lhs <= rhs
                        )

            self.storage_inter_minimum_level = Constraint(
                self.INVESTSTORAGES, m.TIMEINDEX_CLUSTER, noruleinit=True
            )

            self.storage_inter_minimum_level_build = BuildAction(
                rule=_storage_inter_minimum_level_rule
            )

    def _objective_expression(self):
        """Objective expression with fixed and investment costs."""
        m = self.parent_block()

        investment_costs = 0
        storage_costs = 0

        for n in self.CONVEX_INVESTSTORAGES:
            for p in m.CAPACITY_PERIODS:
                investment_costs += (
                    self.invest[n, p] * n.investment.ep_costs[p]
                )
        for n in self.NON_CONVEX_INVESTSTORAGES:
            for p in m.CAPACITY_PERIODS:
                investment_costs += (
                    self.invest[n, p] * n.investment.ep_costs[p]
                    + self.invest_status[n, p] * n.investment.offset[p]
                )

        for n in self.INVESTSTORAGES:
            if valid_sequence(n.storage_costs, len(m.TIMESTEPS)):
                # We actually want to iterate over all TIMEPOINTS except the
                # 0th. As integers are used for the index, this is equicalent
                # to iterating over the TIMESTEPS with one offset.
                if not m.TSAM_MODE:
                    for t in m.TIMESTEPS:
                        storage_costs += (
                            self.storage_content[n, t + 1] * n.storage_costs[t]
                        )
                else:
                    for t in m.TIMESTEPS_ORIGINAL:
                        storage_costs += (
                            self.storage_content[n, t + 1]
                            * n.storage_costs[t + 1]
                        )

        self.storage_costs = Expression(expr=storage_costs)

        self.investment_costs = Expression(expr=investment_costs)
        self.costs = Expression(expr=investment_costs + storage_costs)

        return self.costs
