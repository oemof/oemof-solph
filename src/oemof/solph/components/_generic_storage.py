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

SPDX-License-Identifier: MIT

"""

from oemof.network import network
from pyomo.core.base.block import ScalarBlock
from pyomo.environ import Binary
from pyomo.environ import Constraint
from pyomo.environ import Expression
from pyomo.environ import NonNegativeReals
from pyomo.environ import Set
from pyomo.environ import Var

from oemof.solph._helpers import check_node_object_for_missing_attribute
from oemof.solph._options import Investment
from oemof.solph._plumbing import sequence as solph_sequence


class GenericStorage(network.Node):
    r"""
    Component `GenericStorage` to model with basic characteristics of storages.

    The GenericStorage is designed for one input and one output.

    Parameters
    ----------
    nominal_storage_capacity : numeric, :math:`E_{nom}`
        Absolute nominal capacity of the storage
    invest_relation_input_capacity : numeric or None, :math:`r_{cap,in}`
        Ratio between the investment variable of the input Flow and the
        investment variable of the storage:
        :math:`\dot{E}_{in,invest} = E_{invest} \cdot r_{cap,in}`
    invest_relation_output_capacity : numeric or None, :math:`r_{cap,out}`
        Ratio between the investment variable of the output Flow and the
        investment variable of the storage:
        :math:`\dot{E}_{out,invest} = E_{invest} \cdot r_{cap,out}`
    invest_relation_input_output : numeric or None, :math:`r_{in,out}`
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
    balanced : boolean
        Couple storage level of first and last time step.
        (Total inflow and total outflow are balanced.)
    loss_rate : numeric (iterable or scalar)
        The relative loss of the storage content per hour.
    fixed_losses_relative : numeric (iterable or scalar), :math:`\gamma(t)`
        Losses per hour that are independent of the storage content but
        proportional to nominal storage capacity.
    fixed_losses_absolute : numeric (iterable or scalar), :math:`\delta(t)`
        Losses per hour that are independent of storage content and independent
        of nominal storage capacity.
    inflow_conversion_factor : numeric (iterable or scalar), :math:`\eta_i(t)`
        The relative conversion factor, i.e. efficiency associated with the
        inflow of the storage.
    outflow_conversion_factor : numeric (iterable or scalar), :math:`\eta_o(t)`
        see: inflow_conversion_factor
    min_storage_level : numeric (iterable or scalar), :math:`c_{min}(t)`
        The normed minimum storage content as fraction of the
        nominal storage capacity (between 0 and 1).
        To set different values in every time step use a sequence.
    max_storage_level : numeric (iterable or scalar), :math:`c_{max}(t)`
        see: min_storage_level
    investment : :class:`oemof.solph.options.Investment` object
        Object indicating if a nominal_value of the flow is determined by
        the optimization problem. Note: This will refer all attributes to an
        investment variable instead of to the nominal_storage_capacity. The
        nominal_storage_capacity should not be set (or set to None) if an
        investment object is used.

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
    ...     nominal_storage_capacity=1000,
    ...     inputs={my_bus: solph.flows.Flow(nominal_value=200, variable_costs=10)},
    ...     outputs={my_bus: solph.flows.Flow(nominal_value=200)},
    ...     loss_rate=0.01,
    ...     initial_storage_level=0,
    ...     max_storage_level = 0.9,
    ...     inflow_conversion_factor=0.9,
    ...     outflow_conversion_factor=0.93)

    >>> my_investment_storage = solph.components.GenericStorage(
    ...     label='storage',
    ...     investment=solph.Investment(ep_costs=50),
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
        nominal_storage_capacity=None,
        initial_storage_level=None,
        investment=None,
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
        outflow_conversion_factor=1
    ):
        if inputs is None:
            inputs = {}
        if outputs is None:
            outputs = {}
        super().__init__(label=label, inputs=inputs, outputs=outputs)
        self.nominal_storage_capacity = nominal_storage_capacity
        self.initial_storage_level = initial_storage_level
        self.balanced = balanced
        self.loss_rate = solph_sequence(loss_rate)
        self.fixed_losses_relative = solph_sequence(fixed_losses_relative)
        self.fixed_losses_absolute = solph_sequence(fixed_losses_absolute)
        self.inflow_conversion_factor = solph_sequence(
            inflow_conversion_factor)
        self.outflow_conversion_factor = solph_sequence(
            outflow_conversion_factor)
        self.max_storage_level = solph_sequence(max_storage_level)
        self.min_storage_level = solph_sequence(min_storage_level)
        self.investment = investment
        self.invest_relation_input_output = invest_relation_input_output
        self.invest_relation_input_capacity = invest_relation_input_capacity
        self.invest_relation_output_capacity = invest_relation_output_capacity
        self._invest_group = isinstance(self.investment, Investment)

        # Check number of flows.
        self._check_number_of_flows()
        # Check for infeasible parameter combinations
        self._check_infeasible_parameter_combinations()

        # Check attributes for the investment mode.
        if self._invest_group is True:
            self._check_invest_attributes()

    def _set_flows(self):
        for flow in self.inputs.values():
            if (
                self.invest_relation_input_capacity is not None
                and not isinstance(flow.investment, Investment)
            ):
                flow.investment = Investment()
        for flow in self.outputs.values():
            if (
                self.invest_relation_output_capacity is not None
                and not isinstance(flow.investment, Investment)
            ):
                flow.investment = Investment()

    def _check_invest_attributes(self):
        if self.investment and self.nominal_storage_capacity is not None:
            e1 = (
                "If an investment object is defined the invest variable "
                "replaces the nominal_storage_capacity.\n Therefore the "
                "nominal_storage_capacity should be 'None'.\n"
            )
            raise AttributeError(e1)
        if (
            self.invest_relation_input_output is not None
            and self.invest_relation_output_capacity is not None
            and self.invest_relation_input_capacity is not None
        ):
            e2 = (
                "Overdetermined. Three investment object will be coupled"
                "with three constraints. Set one invest relation to 'None'."
            )
            raise AttributeError(e2)
        if (
            self.investment
            and sum(solph_sequence(self.fixed_losses_absolute)) != 0
            and self.investment.existing == 0
            and self.investment.minimum == 0
        ):
            e3 = (
                "With fixed_losses_absolute > 0, either investment.existing "
                "or investment.minimum has to be non-zero."
            )
            raise AttributeError(e3)

        self._set_flows()

    def _check_number_of_flows(self):
        msg = "Only one {0} flow allowed in the GenericStorage {1}."
        check_node_object_for_missing_attribute(self, "inputs")
        check_node_object_for_missing_attribute(self, "outputs")
        if len(self.inputs) > 1:
            raise AttributeError(msg.format("input", self.label))
        if len(self.outputs) > 1:
            raise AttributeError(msg.format("output", self.label))

    def _check_infeasible_parameter_combinations(self):
        """Checks for infeasible parameter combinations and raises error"""
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
        A set with all :class:`.Storage` objects, which do not have an
         attr:`investment` of type :class:`.Investment`.

    STORAGES_BALANCED
        A set of  all :py:class:`~.GenericStorage` objects, with 'balanced' attribute set
        to True.

    STORAGES_WITH_INVEST_FLOW_REL
        A set with all :class:`.Storage` objects with two investment flows
        coupled with the 'invest_relation_input_output' attribute.

    **The following variables are created:**

    storage_content
        Storage content for every storage and timestep. The value for the
        storage content at the beginning is set by the parameter
        `initial_storage_level` or not set if `initial_storage_level` is None.
        The variable of storage s and timestep t can be accessed by:
        `om.Storage.storage_content[s, t]`

    **The following constraints are created:**

    Set storage_content of last time step to one at t=0 if balanced == True
        .. math::
            E(t_{last}) = &E(-1)

    Storage balance :attr:`om.Storage.balance[n, t]`
        .. math:: E(t) = &E(t-1) \cdot
            (1 - \beta(t)) ^{\tau(t)/(t_u)} \\
            &- \gamma(t)\cdot E_{nom} \cdot {\tau(t)/(t_u)}\\
            &- \delta(t) \cdot {\tau(t)/(t_u)}\\
            &- \frac{\dot{E}_o(t)}{\eta_o(t)} \cdot \tau(t)
            + \dot{E}_i(t) \cdot \eta_i(t) \cdot \tau(t)

    Connect the invest variables of the input and the output flow.
        .. math::
          InvestmentFlowBlock.invest(source(n), n) + existing = \\
          (InvestmentFlowBlock.invest(n, target(n)) + existing) * \\
          invest\_relation\_input\_output(n) \\
          \forall n \in \textrm{INVEST\_REL\_IN\_OUT}



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
                                relative to
                                :math:`E_{nom}` per
                                hour
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
    =========================== ======================= =========

    **The following parts of the objective function are created:**

    Nothing added to the objective function.


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
                n for n in group if n.invest_relation_input_output is not None
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

        self.storage_content = Var(
            self.STORAGES, m.TIMEPOINTS, bounds=_storage_content_bound_rule
        )

        # set the initial storage content
        # ToDo: More elegant code possible?
        for n in group:
            if n.initial_storage_level is not None:
                self.storage_content[n, 0] = (
                    n.initial_storage_level * n.nominal_storage_capacity
                )
                self.storage_content[n, 0].fix()

        #  ************* Constraints ***************************

        def _storage_balance_rule(block, n, t):
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

        self.balance = Constraint(
            self.STORAGES, m.TIMESTEPS, rule=_storage_balance_rule
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

        self.balanced_cstr = Constraint(
            self.STORAGES_BALANCED, rule=_balanced_storage_rule
        )

        def _power_coupled(block, n):
            """
            Rule definition for constraint to connect the input power
            and output power
            """
            expr = (
                m.InvestmentFlowBlock.invest[n, o[n]]
                + m.flows[n, o[n]].investment.existing
            ) * n.invest_relation_input_output == (
                m.InvestmentFlowBlock.invest[i[n], n]
                + m.flows[i[n], n].investment.existing
            )
            return expr

        self.power_coupled = Constraint(
            self.STORAGES_WITH_INVEST_FLOW_REL, rule=_power_coupled
        )

    def _objective_expression(self):
        r"""
        Objective expression for storages with no investment.
        Note: This adds nothing as variable costs are already
        added in the Block :class:`SimpleFlowBlock`.
        """
        if not hasattr(self, "STORAGES"):
            return 0

        return 0


class GenericInvestmentStorageBlock(ScalarBlock):
    r"""
    Block for all storages with :attr:`Investment` being not None.
    See :class:`oemof.solph.options.Investment` for all parameters of the
    Investment class.

    **Variables**

    All Storages are indexed by :math:`n`, which is omitted in the following
    for the sake of convenience.
    The following variables are created as attributes of
    :attr:`om.InvestmentStorage`:

    * :math:`P_i(t)`

        Inflow of the storage
        (created in :class:`oemof.solph.models.BaseModel`).

    * :math:`P_o(t)`

        Outflow of the storage
        (created in :class:`oemof.solph.models.BaseModel`).

    * :math:`E(t)`

        Current storage content (Absolute level of stored energy).

    * :math:`E_{invest}`

        Invested (nominal) capacity of the storage.

    * :math:`E(-1)`

        Initial storage content (before timestep 0).

    * :math:`b_{invest}`

        Binary variable for the status of the investment, if
        :attr:`nonconvex` is `True`.

    **Constraints**

    The following constraints are created for all investment storages:

            Storage balance (Same as for :class:`.GenericStorageBlock`)

        .. math:: E(t) = &E(t-1) \cdot
            (1 - \beta(t)) ^{\tau(t)/(t_u)} \\
            &- \gamma(t)\cdot (E_{exist} + E_{invest}) \cdot {\tau(t)/(t_u)}\\
            &- \delta(t) \cdot {\tau(t)/(t_u)}\\
            &- \frac{P_o(t)}{\eta_o(t)} \cdot \tau(t)
            + P_i(t) \cdot \eta_i(t) \cdot \tau(t)

    Depending on the attribute :attr:`nonconvex`, the constraints for the
    bounds of the decision variable :math:`E_{invest}` are different:\

        * :attr:`nonconvex = False`

        .. math::
            E_{invest, min} \le E_{invest} \le E_{invest, max}

        * :attr:`nonconvex = True`

        .. math::
            &
            E_{invest, min} \cdot b_{invest} \le E_{invest}\\
            &
            E_{invest} \le E_{invest, max} \cdot b_{invest}\\

    The following constraints are created depending on the attributes of
    the :class:`.components.GenericStorage`:

        * :attr:`initial_storage_level is None`

            Constraint for a variable initial storage content:

        .. math::
               E(-1) \le E_{invest} + E_{exist}

        * :attr:`initial_storage_level is not None`

            An initial value for the storage content is given:

        .. math::
               E(-1) = (E_{invest} + E_{exist}) \cdot c(-1)

        * :attr:`balanced=True`

            The energy content of storage of the first and the last timestep
            are set equal:

        .. math::
            E(-1) = E(t_{last})

        * :attr:`invest_relation_input_capacity is not None`

            Connect the invest variables of the storage and the input flow:

        .. math::
            P_{i,invest} + P_{i,exist} =
            (E_{invest} + E_{exist}) \cdot r_{cap,in}

        * :attr:`invest_relation_output_capacity is not None`

            Connect the invest variables of the storage and the output flow:

        .. math::
            P_{o,invest} + P_{o,exist} =
            (E_{invest} + E_{exist}) \cdot r_{cap,out}

        * :attr:`invest_relation_input_output is not None`

            Connect the invest variables of the input and the output flow:

        .. math::
            P_{i,invest} + P_{i,exist} =
            (P_{o,invest} + P_{o,exist}) \cdot r_{in,out}

        * :attr:`max_storage_level`

            Rule for upper bound constraint for the storage content:

        .. math::
            E(t) \leq E_{invest} \cdot c_{max}(t)

        * :attr:`min_storage_level`

            Rule for lower bound constraint for the storage content:

        .. math:: E(t) \geq E_{invest} \cdot c_{min}(t)


    **Objective function**

    The part of the objective function added by the investment storages
    also depends on whether a convex or nonconvex
    investment option is selected. The following parts of the objective
    function are created:

        * :attr:`nonconvex = False`

            .. math::
                E_{invest} \cdot c_{invest,var}

        * :attr:`nonconvex = True`

            .. math::
                E_{invest} \cdot c_{invest,var}
                + c_{invest,fix} \cdot b_{invest}\\

    The total value of all investment costs of all *InvestmentStorages*
    can be retrieved calling
    :meth:`om.GenericInvestmentStorageBlock.investment_costs.expr()`.

    .. csv-table:: List of Variables
        :header: "symbol", "attribute", "explanation"
        :widths: 1, 1, 1

        ":math:`P_i(t)`", ":attr:`flow[i[n], n, t]`", "Inflow of the storage"
        ":math:`P_o(t)`", ":attr:`flow[n, o[n], t]`", "Outlfow of the storage"
        ":math:`E(t)`", ":attr:`storage_content[n, t]`", "Current storage
        content (current absolute stored energy)"
        ":math:`E_{invest}`", ":attr:`invest[n, t]`", "Invested (nominal)
        capacity of the storage"
        ":math:`E(-1)`", ":attr:`init_cap[n]`", "Initial storage capacity
        (before timestep 0)"
        ":math:`b_{invest}`", ":attr:`invest_status[i, o]`", "Binary variable
        for the status of investment"
        ":math:`P_{i,invest}`", ":attr:`InvestmentFlowBlock.invest[i[n], n]`",
            "Invested (nominal) inflow (Investmentflow)"
        ":math:`P_{o,invest}`", ":attr:`InvestmentFlowBlock.invest[n, o[n]]`",
            "Invested (nominal) outflow (Investmentflow)"

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
        ", "Existing outlfow capacity"
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
        as share of :math:`E(t)` per time unit"
        ":math:`\gamma(t)`", "`fixed_losses_relative[t]`", "Fixed loss
        of energy relative to :math:`E_{invest} + E_{exist}` per time unit"
        ":math:`\delta(t)`", "`fixed_losses_absolute[t]`", "Absolute
        fixed loss of energy per time unit"
        ":math:`\eta_i(t)`", "`inflow_conversion_factor[t]`", "
        Conversion factor (i.e. efficiency) when storing energy"
        ":math:`\eta_o(t)`", "`outflow_conversion_factor[t]`", "
        Conversion factor when (i.e. efficiency) taking stored energy"
        ":math:`c(-1)`", "`initial_storage_level`", "Initial relativ
        storage content (before timestep 0)"
        ":math:`c_{max}`", "`flows[i, o].max[t]`", "Normed maximum
        value of storage content"
        ":math:`c_{min}`", "`flows[i, o].min[t]`", "Normed minimum
        value of storage content"
        ":math:`\tau(t)`", "", "Duration of time step"
        ":math:`t_u`", "", "Time unit of losses :math:`\beta(t)`,
        :math:`\gamma(t)`, :math:`\delta(t)` and timeincrement :math:`\tau(t)`"

    """

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """ """
        m = self.parent_block()
        if group is None:
            return None

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
                if n.invest_relation_input_capacity is not None
            ]
        )

        self.INVEST_REL_CAP_OUT = Set(
            initialize=[
                n
                for n in group
                if n.invest_relation_output_capacity is not None
            ]
        )

        self.INVEST_REL_IN_OUT = Set(
            initialize=[
                n for n in group if n.invest_relation_input_output is not None
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

        # ######################### Variables  ################################
        self.storage_content = Var(
            self.INVESTSTORAGES, m.TIMESTEPS, within=NonNegativeReals
        )

        def _storage_investvar_bound_rule(block, n):
            """
            Rule definition to bound the invested storage capacity `invest`.
            """
            if n in self.CONVEX_INVESTSTORAGES:
                return n.investment.minimum, n.investment.maximum
            elif n in self.NON_CONVEX_INVESTSTORAGES:
                return 0, n.investment.maximum

        self.invest = Var(
            self.INVESTSTORAGES,
            within=NonNegativeReals,
            bounds=_storage_investvar_bound_rule,
        )

        self.init_content = Var(self.INVESTSTORAGES, within=NonNegativeReals)

        # create status variable for a non-convex investment storage
        self.invest_status = Var(self.NON_CONVEX_INVESTSTORAGES, within=Binary)

        # ######################### CONSTRAINTS ###############################
        i = {n: [i for i in n.inputs][0] for n in group}
        o = {n: [o for o in n.outputs][0] for n in group}

        reduced_timesteps = [x for x in m.TIMESTEPS if x > 0]

        def _inv_storage_init_content_max_rule(block, n):
            """Constraint for a variable initial storage capacity."""
            return (
                block.init_content[n]
                <= n.investment.existing + block.invest[n]
            )

        self.init_content_limit = Constraint(
            self.INVESTSTORAGES_NO_INIT_CONTENT,
            rule=_inv_storage_init_content_max_rule,
        )

        def _inv_storage_init_content_fix_rule(block, n):
            """Constraint for a fixed initial storage capacity."""
            return block.init_content[n] == n.initial_storage_level * (
                n.investment.existing + block.invest[n]
            )

        self.init_content_fix = Constraint(
            self.INVESTSTORAGES_INIT_CONTENT,
            rule=_inv_storage_init_content_fix_rule,
        )

        def _storage_balance_first_rule(block, n):
            """
            Rule definition for the storage balance of every storage n for the
            first time step.
            """
            expr = 0
            expr += block.storage_content[n, 0]
            expr += (
                -block.init_content[n]
                * (1 - n.loss_rate[0]) ** m.timeincrement[0]
            )
            expr += (
                n.fixed_losses_relative[0]
                * (n.investment.existing + self.invest[n])
                * m.timeincrement[0]
            )
            expr += n.fixed_losses_absolute[0] * m.timeincrement[0]
            expr += (
                -m.flow[i[n], n, 0] * n.inflow_conversion_factor[0]
            ) * m.timeincrement[0]
            expr += (
                m.flow[n, o[n], 0] / n.outflow_conversion_factor[0]
            ) * m.timeincrement[0]
            return expr == 0

        self.balance_first = Constraint(
            self.INVESTSTORAGES, rule=_storage_balance_first_rule
        )

        def _storage_balance_rule(block, n, t):
            """
            Rule definition for the storage balance of every storage n for the
            every time step but the first.
            """
            expr = 0
            expr += block.storage_content[n, t]
            expr += (
                -block.storage_content[n, t - 1]
                * (1 - n.loss_rate[t]) ** m.timeincrement[t]
            )
            expr += (
                n.fixed_losses_relative[t]
                * (n.investment.existing + self.invest[n])
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

        self.balance = Constraint(
            self.INVESTSTORAGES, reduced_timesteps, rule=_storage_balance_rule
        )

        def _balanced_storage_rule(block, n):
            return (
                block.storage_content[n, m.TIMESTEPS[-1]]
                == block.init_content[n]
            )

        self.balanced_cstr = Constraint(
            self.INVESTSTORAGES_BALANCED, rule=_balanced_storage_rule
        )

        def _power_coupled(block, n):
            """
            Rule definition for constraint to connect the input power
            and output power
            """
            expr = (
                m.InvestmentFlowBlock.invest[n, o[n]]
                + m.flows[n, o[n]].investment.existing
            ) * n.invest_relation_input_output == (
                m.InvestmentFlowBlock.invest[i[n], n]
                + m.flows[i[n], n].investment.existing
            )
            return expr

        self.power_coupled = Constraint(
            self.INVEST_REL_IN_OUT, rule=_power_coupled
        )

        def _storage_capacity_inflow_invest_rule(block, n):
            """
            Rule definition of constraint connecting the inflow
            `InvestmentFlowBlock.invest of storage with invested capacity
            `invest` by nominal_storage_capacity__inflow_ratio
            """
            expr = (
                m.InvestmentFlowBlock.invest[i[n], n]
                + m.flows[i[n], n].investment.existing
            ) == (
                n.investment.existing + self.invest[n]
            ) * n.invest_relation_input_capacity
            return expr

        self.storage_capacity_inflow = Constraint(
            self.INVEST_REL_CAP_IN, rule=_storage_capacity_inflow_invest_rule
        )

        def _storage_capacity_outflow_invest_rule(block, n):
            """
            Rule definition of constraint connecting outflow
            `InvestmentFlowBlock.invest` of storage and invested capacity
            `invest` by nominal_storage_capacity__outflow_ratio
            """
            expr = (
                m.InvestmentFlowBlock.invest[n, o[n]]
                + m.flows[n, o[n]].investment.existing
            ) == (
                n.investment.existing + self.invest[n]
            ) * n.invest_relation_output_capacity
            return expr

        self.storage_capacity_outflow = Constraint(
            self.INVEST_REL_CAP_OUT, rule=_storage_capacity_outflow_invest_rule
        )

        def _max_storage_content_invest_rule(block, n, t):
            """
            Rule definition for upper bound constraint for the
            storage content.
            """
            expr = (
                self.storage_content[n, t]
                <= (n.investment.existing + self.invest[n])
                * n.max_storage_level[t]
            )
            return expr

        self.max_storage_content = Constraint(
            self.INVESTSTORAGES,
            m.TIMESTEPS,
            rule=_max_storage_content_invest_rule,
        )

        def _min_storage_content_invest_rule(block, n, t):
            """
            Rule definition of lower bound constraint for the
            storage content.
            """
            expr = (
                self.storage_content[n, t]
                >= (n.investment.existing + self.invest[n])
                * n.min_storage_level[t]
            )
            return expr

        # Set the lower bound of the storage content if the attribute exists
        self.min_storage_content = Constraint(
            self.MIN_INVESTSTORAGES,
            m.TIMESTEPS,
            rule=_min_storage_content_invest_rule,
        )

        def maximum_invest_limit(block, n):
            """
            Constraint for the maximal investment in non convex investment
            storage.
            """
            return (
                n.investment.maximum * self.invest_status[n] - self.invest[n]
            ) >= 0

        self.limit_max = Constraint(
            self.NON_CONVEX_INVESTSTORAGES, rule=maximum_invest_limit
        )

        def smallest_invest(block, n):
            """
            Constraint for the minimal investment in non convex investment
            storage if the invest is greater than 0. So the invest variable
            can be either 0 or greater than the minimum.
            """
            return (
                self.invest[n] - (n.investment.minimum * self.invest_status[n])
                >= 0
            )

        self.limit_min = Constraint(
            self.NON_CONVEX_INVESTSTORAGES, rule=smallest_invest
        )

    def _objective_expression(self):
        """Objective expression with fixed and investement costs."""
        if not hasattr(self, "INVESTSTORAGES"):
            return 0

        investment_costs = 0

        for n in self.CONVEX_INVESTSTORAGES:
            investment_costs += self.invest[n] * n.investment.ep_costs
        for n in self.NON_CONVEX_INVESTSTORAGES:
            investment_costs += (
                self.invest[n] * n.investment.ep_costs
                + self.invest_status[n] * n.investment.offset
            )
        self.investment_costs = Expression(expr=investment_costs)

        return investment_costs
