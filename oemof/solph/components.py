# -*- coding: utf-8 -
"""
This module is designed to hold custom components with their classes and
associated individual constraints (blocks) and groupings. Therefore this
module holds the class definition and the block directly located by each other.
"""

from pyomo.core.base.block import SimpleBlock
from pyomo.environ import (Binary, Set, NonNegativeReals, Var, Constraint,
                           Expression, BuildAction)
import numpy as np
import warnings
from oemof.network import Bus, Transformer
from oemof.solph import Flow, LinearTransformer
from .options import Investment
from .plumbing import sequence


# ------------------------------------------------------------------------------
# Start of generic storage component
# ------------------------------------------------------------------------------

class GenericStorage(Transformer):
    """
    Component `GenericStorage` to model with basic characteristics of storages.

    Parameters
    ----------
    nominal_capacity : numeric
        Absolute nominal capacity of the storage
    nominal_input_capacity_ratio :  numeric
        Ratio between the nominal inflow of the storage and its capacity.
    nominal_output_capacity_ratio : numeric
        Ratio between the nominal outflow of the storage and its capacity.
        Note: This ratio is used to create the Flow object for the outflow
        and set its nominal value of the storage in the constructor.
    nominal_input_capacity_ratio : numeric
        see: nominal_output_capacity_ratio
    initial_capacity : numeric
        The capacity of the storage in the first (and last) time step of
        optimization.
    capacity_loss : numeric (sequence or scalar)
        The relative loss of the storage capacity from between two consecutive
        timesteps.
    inflow_conversion_factor : numeric (sequence or scalar)
        The relative conversion factor, i.e. efficiency associated with the
        inflow of the storage.
    outflow_conversion_factor : numeric (sequence or scalar)
        see: inflow_conversion_factor
    capacity_min : numeric (sequence or scalar)
        The nominal minimum capacity of the storage as fraction of the
        nominal capacity (between 0 and 1, default: 0).
        To set different values in every time step use a sequence.
    capacity_max : numeric (sequence or scalar)
        see: capacity_min
    investment : :class:`oemof.solph.options.Investment` object
        Object indicating if a nominal_value of the flow is determined by
        the optimization problem. Note: This will refer all attributes to an
        investment variable instead of to the nominal_capacity. The
        nominal_capacity should not be set (or set to None) if an investment
        object is used.

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.Storage` (if no Investment object
       present)
     * :py:class:`~oemof.solph.blocks.InvestmentStorage` (if Investment object
       present)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nominal_capacity = kwargs.get('nominal_capacity')
        self.nominal_input_capacity_ratio = kwargs.get(
            'nominal_input_capacity_ratio', 0.2)
        self.nominal_output_capacity_ratio = kwargs.get(
            'nominal_output_capacity_ratio', 0.2)
        self.initial_capacity = kwargs.get('initial_capacity')
        self.capacity_loss = sequence(kwargs.get('capacity_loss', 0))
        self.inflow_conversion_factor = sequence(
            kwargs.get(
                'inflow_conversion_factor', 1))
        self.outflow_conversion_factor = sequence(
            kwargs.get(
                'outflow_conversion_factor', 1))
        self.capacity_max = sequence(kwargs.get('capacity_max', 1))
        self.capacity_min = sequence(kwargs.get('capacity_min', 0))
        self.fixed_costs = kwargs.get('fixed_costs')
        self.investment = kwargs.get('investment')
        # Check investment
        if self.investment and self.nominal_capacity is not None:
            self.nominal_capacity = None
            warnings.warn(
                "Using the investment object the nominal_capacity is set to" +
                "None.", SyntaxWarning)
        # Check input flows for nominal value
        for flow in self.inputs.values():
            if flow.nominal_value is not None:
                storage_nominal_value_warning('output')
            if self.nominal_capacity is None:
                flow.nominal_value = None
            else:
                flow.nominal_value = (self.nominal_input_capacity_ratio *
                                      self.nominal_capacity)
            if self.investment:
                if not isinstance(flow.investment, Investment):
                    flow.investment = Investment()

        # Check output flows for nominal value
        for flow in self.outputs.values():
            if flow.nominal_value is not None:
                storage_nominal_value_warning('input')
            if self.nominal_capacity is None:
                flow.nominal_value = None
            else:
                flow.nominal_value = (self.nominal_output_capacity_ratio *
                                      self.nominal_capacity)
            if self.investment:
                if not isinstance(flow.investment, Investment):
                    flow.investment = Investment()


def storage_nominal_value_warning(flow):
    msg = ("The nominal_value should not be set for {0} flows of storages." +
           "The value will be overwritten by the product of the " +
           "nominal_capacity and the nominal_{0}_capacity_ratio.")
    warnings.warn(msg.format(flow), SyntaxWarning)

# ------------------------------------------------------------------------------
# End of generic storage component
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Start of generic storage block
# ------------------------------------------------------------------------------

class GenericStorageBlock(SimpleBlock):
    r"""Storage without an :class:`.Investment` object.

    **The following sets are created:** (-> see basic sets at
    :class:`.OperationalModel` )

    STORAGES
        A set with all :class:`.Storage` objects
        (and no attr:`investement` of type :class:`.Investment`)

    **The following variables are created:**

    capacity
        Capacity (level) for every storage and timestep. The value for the
        capacity at the beginning is set by the parameter `initial_capacity` or
        not set if `initial_capacity` is None.
        The variable of storage s and timestep t can be accessed by:
        `om.Storage.capacity[s, t]`

    **The following constraints are created:**

    Storage balance :attr:`om.Storage.balance[n, t]`
        .. math:: capacity(n, t) = capacity(n, previous(t)) \\cdot  \
            (1 - capacity\\_loss_n(t))) \
            - \\frac{flow(n, o, t)}{\\eta(n, o, t)} \\cdot \\tau \
            + flow(i, n, t) \\cdot \\eta(i, n, t) \\cdot \\tau

    **The following parts of the objective function are created:**

    If :attr:`fixed_costs` is set by the user:
        .. math:: \\sum_n nominal\\_capacity(n, t) \cdot fixed\\_costs(n)

    The fixed costs expression can be accessed by `om.Storage.fixed_costs`
    and their value after optimization by: `om.Storage.fixed_costs()`.
    """

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

        I = {n: [i for i in n.inputs][0] for n in group}
        O = {n: [o for o in n.outputs][0] for n in group}

        self.STORAGES = Set(initialize=[n for n in group])

        def _storage_capacity_bound_rule(block, n, t):
            """Rule definition for bounds of capacity variable of storage n
            in timestep t
            """
            bounds = (n.nominal_capacity * n.capacity_min[t],
                      n.nominal_capacity * n.capacity_max[t])
            return bounds
        self.capacity = Var(self.STORAGES, m.TIMESTEPS,
                            bounds=_storage_capacity_bound_rule)

        # set the initial capacity of the storage
        for n in group:
            if n.initial_capacity is not None:
                self.capacity[n, m.timesteps[-1]] = (n.initial_capacity *
                                                     n.nominal_capacity)
                self.capacity[n, m.timesteps[-1]].fix()

        # storage balance constraint
        def _storage_balance_rule(block, n, t):
            """Rule definition for the storage balance of every storage n and
            timestep t
            """
            expr = 0
            expr += block.capacity[n, t]
            expr += - block.capacity[n, m.previous_timesteps[t]] * (
                1 - n.capacity_loss[t])
            expr += (- m.flow[I[n], n, t] *
                     n.inflow_conversion_factor[t]) * m.timeincrement[t]
            expr += (m.flow[n, O[n], t] /
                     n.outflow_conversion_factor[t]) * m.timeincrement[t]
            return expr == 0
        self.balance = Constraint(self.STORAGES, m.TIMESTEPS,
                                  rule=_storage_balance_rule)

    def _objective_expression(self):
        """Objective expression for storages with no investment.
        Note: This adds only fixed costs as variable costs are already
        added in the Block :class:`Flow`.
        """
        if not hasattr(self, 'STORAGES'):
            return 0

        fixed_costs = 0

        for n in self.STORAGES:
            if n.fixed_costs is not None:
                fixed_costs += n.nominal_capacity * n.fixed_costs

        self.fixed_costs = Expression(expr=fixed_costs)

        return fixed_costs

# ------------------------------------------------------------------------------
# End of generic storage block
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Start of generic storage invest block
# ------------------------------------------------------------------------------
class GenericInvestmentStorageBlock(SimpleBlock):
    r"""Storage with an :class:`.Investment` object.

    **The following sets are created:** (-> see basic sets at
    :class:`.OperationalModel` )

    INVESTSTORAGES
        A set with all storages containing an Investment object.
    INITIAL_CAPACITY
        A subset of the set INVESTSTORAGES where elements of the set have an
        initial_capacity attribute.
    MIN_INVESTSTORAGES
        A subset of INVESTSTORAGES where elements of the set have an
        capacity_min attribute greater than zero for at least one time step.

    **The following variables are created:**

    capacity :attr:`om.InvestmentStorage.capacity[n, t]`
        Level of the storage (indexed by STORAGES and TIMESTEPS)

    invest :attr:`om.InvestmentStorage.invest[n, t]`
        Nominal capacity of the storage (indexed by STORAGES)


    **The following constraints are build:**

    Storage balance
      .. math::
        capacity(n, t) =  &capacity(n, t\_previous(t)) \\cdot \
        (1 - capacity\_loss(n)) \\\\
        &- (flow(n, target(n), t)) / (outflow\_conversion\_factor(n) \\cdot \
           \\tau) \\\\
        &+ flow(source(n), n, t) \\cdot inflow\_conversion\_factor(n) \\cdot \
           \\tau, \\\\
        &\\forall n \\in \\textrm{INVESTSTORAGES} \\textrm{,} \\\\
        &\\forall t \\in \\textrm{TIMESTEPS}.

    Initial capacity of :class:`.network.Storage`
        .. math::
          capacity(n, t_{last}) = invest(n) \\cdot
          initial\_capacity(n), \\\\
          \\forall n \\in \\textrm{INITIAL\_CAPACITY,} \\\\
          \\forall t \\in \\textrm{TIMESTEPS}.

    Connect the invest variables of the storage and the input flow.
        .. math:: InvestmentFlow.invest(source(n), n) =
          invest(n) * nominal\_input\_capacity\_ratio(n) \\\\
          \\forall n \\in \\textrm{INVESTSTORAGES}

    Connect the invest variables of the storage and the output flow.
        .. math:: InvestmentFlow.invest(n, target(n)) ==
          invest(n) * nominal_output_capacity_ratio(n) \\\\
          \\forall n \\in \\textrm{INVESTSTORAGES}

    Maximal capacity :attr:`om.InvestmentStorage.max_capacity[n, t]`
        .. math:: capacity(n, t) \leq invest(n) \\cdot capacity\_min(n, t),
            \\\\
            \\forall n \\in \\textrm{MAX\_INVESTSTORAGES,} \\\\
            \\forall t \\in \\textrm{TIMESTEPS}.

    Minimal capacity :attr:`om.InvestmentStorage.min_capacity[n, t]`
        .. math:: capacity(n, t) \geq invest(n) \\cdot capacity\_min(n, t),
            \\\\
            \\forall n \\in \\textrm{MIN\_INVESTSTORAGES,} \\\\
            \\forall t \\in \\textrm{TIMESTEPS}.


    **The following parts of the objective function are created:**

    Equivalent periodical costs (investment costs):
        .. math::
            \\sum_n invest(n) \\cdot ep\_costs(n)

    Additionally, if fixed costs are set by the user:
        .. math::
            \\sum_n invest(n) \\cdot fixed\_costs(n)

    The expression can be accessed by :attr:`om.InvestStorages.fixed_costs` and
    their value after optimization by :meth:`om.InvestStorages.fixed_costs()` .
    This works similar for investment costs with :attr:`*.investment_costs`.
    """

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """
        """
        m = self.parent_block()
        if group is None:
            return None

        # ########################## SETS #####################################

        self.INVESTSTORAGES = Set(initialize=[n for n in group])

        self.INITIAL_CAPACITY = Set(initialize=[
            n for n in group if n.initial_capacity is not None])

        # The capacity is set as a non-negative variable, therefore it makes no
        # sense to create an additional constraint if the lower bound is zero
        # for all time steps.
        self.MIN_INVESTSTORAGES = Set(
            initialize=[n for n in group if sum(
                [n.capacity_min[t] for t in m.TIMESTEPS]) > 0])

        # ######################### Variables  ################################
        self.capacity = Var(self.INVESTSTORAGES, m.TIMESTEPS,
                            within=NonNegativeReals)

        def _storage_investvar_bound_rule(block, n):
            """Rule definition to bound the invested storage capacity `invest`.
            """
            return 0, n.investment.maximum
        self.invest = Var(self.INVESTSTORAGES, within=NonNegativeReals,
                          bounds=_storage_investvar_bound_rule)

        # ######################### CONSTRAINTS ###############################
        i = {n: [i for i in n.inputs][0] for n in group}
        o = {n: [o for o in n.outputs][0] for n in group}

        def _storage_balance_rule(block, n, t):
            """Rule definition for the storage energy balance.
            """
            expr = 0
            expr += block.capacity[n, t]
            expr += - block.capacity[n, m.previous_timesteps[t]] * (
                1 - n.capacity_loss[t])
            expr += (- m.flow[i[n], n, t] *
                     n.inflow_conversion_factor[t]) * m.timeincrement[t]
            expr += (m.flow[n, o[n], t] /
                     n.outflow_conversion_factor[t]) * m.timeincrement[t]
            return expr == 0
        self.balance = Constraint(self.INVESTSTORAGES, m.TIMESTEPS,
                                  rule=_storage_balance_rule)

        def _initial_capacity_invest_rule(block, n):
            """Rule definition for constraint to connect initial storage
            capacity with capacity of last timesteps.
            """
            expr = (self.capacity[n, m.TIMESTEPS[-1]] == (n.initial_capacity *
                                                          self.invest[n]))
            return expr
        self.initial_capacity = Constraint(
            self.INITIAL_CAPACITY, rule=_initial_capacity_invest_rule)

        def _storage_capacity_inflow_invest_rule(block, n):
            """Rule definition of constraint connecting the inflow
            `InvestmentFlow.invest of storage with invested capacity `invest`
            by nominal_capacity__inflow_ratio
            """
            expr = (m.InvestmentFlow.invest[i[n], n] ==
                    self.invest[n] * n.nominal_input_capacity_ratio)
            return expr
        self.storage_capacity_inflow = Constraint(
            self.INVESTSTORAGES, rule=_storage_capacity_inflow_invest_rule)

        def _storage_capacity_outflow_invest_rule(block, n):
            """Rule definition of constraint connecting outflow
            `InvestmentFlow.invest` of storage and invested capacity `invest`
            by nominal_capacity__outflow_ratio
            """
            expr = (m.InvestmentFlow.invest[n, o[n]] ==
                    self.invest[n] * n.nominal_output_capacity_ratio)
            return expr
        self.storage_capacity_outflow = Constraint(
            self.INVESTSTORAGES, rule=_storage_capacity_outflow_invest_rule)

        def _max_capacity_invest_rule(block, n, t):
            """Rule definition for upper bound constraint for the storage cap.
            """
            expr = (self.capacity[n, t] <= (n.capacity_max[t] *
                                            self.invest[n]))
            return expr
        self.max_capacity = Constraint(
            self.INVESTSTORAGES, m.TIMESTEPS, rule=_max_capacity_invest_rule)

        def _min_capacity_invest_rule(block, n, t):
            """Rule definition of lower bound constraint for the storage cap.
            """
            expr = (self.capacity[n, t] >= (n.capacity_min[t] *
                                            self.invest[n]))
            return expr
        # Set the lower bound of the storage capacity if the attribute exists
        self.min_capacity = Constraint(
            self.MIN_INVESTSTORAGES, m.TIMESTEPS,
            rule=_min_capacity_invest_rule)

    def _objective_expression(self):
        """Objective expression with fixed and investement costs."""
        if not hasattr(self, 'INVESTSTORAGES'):
            return 0

        investment_costs = 0
        fixed_costs = 0

        for n in self.INVESTSTORAGES:
            if n.investment.ep_costs is not None:
                investment_costs += self.invest[n] * n.investment.ep_costs
            else:
                raise ValueError("Missing value for investment costs!")

            if n.fixed_costs is not None:
                fixed_costs += self.invest[n] * n.fixed_costs
        self.investment_costs = Expression(expr=investment_costs)
        self.fixed_costs = Expression(expr=fixed_costs)

        return fixed_costs + investment_costs

# ------------------------------------------------------------------------------
# End of generic storage invest block
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Start of generic CHP component
# ------------------------------------------------------------------------------

class GenericCHP(Transformer):
    """
    Component `GenericCHP` to model combined heat and power plants.

    Can be used to model (combined cycle) extraction or back-pressure turbines
    and used a mixed-integer linear formulation. Thus, it induces more
    computational effort than the `VariableFractionTransformer` for the
    benefit of higher accuracy.

    The full set of equations is described in:
    Mollenhauer, E., Christidis, A. & Tsatsaronis, G.
    Evaluation of an energy- and exergy-based generic modeling
    approach of combined heat and power plants
    Int J Energy Environ Eng (2016) 7: 167.
    https://doi.org/10.1007/s40095-016-0204-6

    Only one adaption for the parameter `H_L_FG_share`has been made to
    set the flue gas losses `H_L_FG` as share of the fuel flow `H_F`.

    Also have a look at the examples on how to use it.

    Parameters
    ----------
    fuel_input : dict
        Dictionary with key-value-pair of `oemof.Bus` and `oemof.Flow` object
        for the fuel input.
    electrical_output : dict
        Dictionary with key-value-pair of `oemof.Bus` and `oemof.Flow` object
        for the electrical output. Related parameters like `P_max_woDH` are
        passed as attributes of the `oemof.Flow` object.
    heat_output : dict
        Dictionary with key-value-pair of `oemof.Bus` and `oemof.Flow` object
        for the heat output. Related parameters like `Q_CW_min` are passed as
        attributes of the `oemof.Flow` object.
    Beta : list of numerical values
        Beta values in same dimension as all other parameters (length of
        optimization period).
    back_pressure : boolean
        Flag to use back-pressure characteristics. Works of set to `True` and
        `Q_CW_min` set to zero. See paper above for more information.
    fixed_costs : numerical value
        Fixed costs for length of optimization period.

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.GenericCHP`
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fuel_input = kwargs.get('fuel_input')
        self.electrical_output = kwargs.get('electrical_output')
        self.heat_output = kwargs.get('heat_output')
        self.Beta = sequence(kwargs.get('Beta'))
        self.back_pressure = kwargs.get('back_pressure')
        self.fixed_costs = kwargs.get('fixed_costs')
        self._alphas = None

        # map specific flows to standard API
        fuel_bus = list(self.fuel_input.keys())[0]
        fuel_flow = list(self.fuel_input.values())[0]
        fuel_bus.outputs.update({self: fuel_flow})
        self.outputs.update(kwargs.get('electrical_output'))
        self.outputs.update(kwargs.get('heat_output'))

    def _calculate_alphas(self):
        """
        Calculate alpha coefficients.

        A system of linear equations is created from passed capacities and
        efficiencies and solved to calculate both coefficients.
        """
        alphas = [[], []]

        eb = list(self.electrical_output.keys())[0]

        attrs = [self.electrical_output[eb].P_min_woDH,
                 self.electrical_output[eb].Eta_el_min_woDH,
                 self.electrical_output[eb].P_max_woDH,
                 self.electrical_output[eb].Eta_el_max_woDH]

        length = [len(a) for a in attrs if not isinstance(a, (int, float))]
        max_length = max(length)

        if all(len(a) == max_length for a in attrs):
            if max_length == 0:
                max_length += 1  # increment dimension for scalars from 0 to 1
            for i in range(0, max_length):
                A = np.array([[1, self.electrical_output[eb].P_min_woDH[i]],
                              [1, self.electrical_output[eb].P_max_woDH[i]]])
                b = np.array([self.electrical_output[eb].P_min_woDH[i] /
                              self.electrical_output[eb].Eta_el_min_woDH[i],
                              self.electrical_output[eb].P_max_woDH[i] /
                              self.electrical_output[eb].Eta_el_max_woDH[i]])
                x = np.linalg.solve(A, b)
                alphas[0].append(x[0])
                alphas[1].append(x[1])
        else:
            error_message = ('Attributes to calculate alphas ' +
                             'must be of same dimension.')
            raise ValueError(error_message)

        self._alphas = alphas

    @property
    def alphas(self):
        """Compute or return the _alphas attribute."""
        if self._alphas is None:
            self._calculate_alphas()

        return self._alphas

# ------------------------------------------------------------------------------
# End of generic CHP component
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Start of generic CHP block
# ------------------------------------------------------------------------------

class GenericCHPBlock(SimpleBlock):
    """Block for the linear relation of nodes with type class:`.GenericCHP`."""

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """
        Create constraints for GenericCHPBlock.

        Parameters
        ----------
        group : list
            List containing `GenericCHP` objects.
            e.g. groups=[ghcp1, gchp2,..]
        """
        m = self.parent_block()

        if group is None:
            return None

        self.GENERICCHPS = Set(initialize=[n for n in group])

        # variables
        self.H_F = Var(self.GENERICCHPS, m.TIMESTEPS, within=NonNegativeReals)
        self.H_L_FG_max = Var(self.GENERICCHPS, m.TIMESTEPS,
                              within=NonNegativeReals)
        self.P_woDH = Var(self.GENERICCHPS, m.TIMESTEPS,
                          within=NonNegativeReals)
        self.P = Var(self.GENERICCHPS, m.TIMESTEPS, within=NonNegativeReals)
        self.Q = Var(self.GENERICCHPS, m.TIMESTEPS, within=NonNegativeReals)
        self.Y = Var(self.GENERICCHPS, m.TIMESTEPS, within=Binary)

        def _h_flow_connection_rule(block, n, t):
            """Link fuel consumption to component inflow."""
            expr = 0
            expr += self.H_F[n, t]
            expr += - m.flow[list(n.fuel_input.keys())[0], n, t]
            return expr == 0
        self.h_flow_connection = Constraint(self.GENERICCHPS, m.TIMESTEPS,
                                            rule=_h_flow_connection_rule)

        def _q_flow_connection_rule(block, n, t):
            """Link heat flow to component outflow."""
            expr = 0
            expr += self.Q[n, t]
            expr += - m.flow[n, list(n.heat_output.keys())[0], t]
            return expr == 0
        self.q_flow_connection = Constraint(self.GENERICCHPS, m.TIMESTEPS,
                                            rule=_q_flow_connection_rule)

        def _p_flow_connection_rule(block, n, t):
            """Link power flow to component outflow."""
            expr = 0
            expr += self.P[n, t]
            expr += - m.flow[n, list(n.electrical_output.keys())[0], t]
            return expr == 0
        self.p_flow_connection = Constraint(self.GENERICCHPS, m.TIMESTEPS,
                                            rule=_p_flow_connection_rule)

        def _H_F_1_rule(block, n, t):
            """Set P_woDH depending on H_F."""
            expr = 0
            expr += - self.H_F[n, t]
            expr += n.alphas[0][t] * self.Y[n, t]
            expr += n.alphas[1][t] * self.P_woDH[n, t]
            return expr == 0
        self.H_F_1 = Constraint(self.GENERICCHPS, m.TIMESTEPS,
                                rule=_H_F_1_rule)

        def _H_F_2_rule(block, n, t):
            """Determine relation between H_F, P and Q."""
            expr = 0
            expr += - self.H_F[n, t]
            expr += n.alphas[0][t] * self.Y[n, t]
            expr += n.alphas[1][t] * (self.P[n, t] + n.Beta[t] * self.Q[n, t])
            return expr == 0
        self.H_F_2 = Constraint(self.GENERICCHPS, m.TIMESTEPS,
                                rule=_H_F_2_rule)

        def _H_F_3_rule(block, n, t):
            """Set upper value of operating range via H_F."""
            expr = 0
            expr += self.H_F[n, t]
            expr += - self.Y[n, t] * \
                (list(n.electrical_output.values())[0].P_max_woDH[t] /
                 list(n.electrical_output.values())[0].Eta_el_max_woDH[t])
            return expr <= 0
        self.H_F_3 = Constraint(self.GENERICCHPS, m.TIMESTEPS,
                                rule=_H_F_3_rule)

        def _H_F_4_rule(block, n, t):
            """Set lower value of operating range via H_F."""
            expr = 0
            expr += self.H_F[n, t]
            expr += - self.Y[n, t] * \
                (list(n.electrical_output.values())[0].P_min_woDH[t] /
                 list(n.electrical_output.values())[0].Eta_el_min_woDH[t])
            return expr >= 0
        self.H_F_4 = Constraint(self.GENERICCHPS, m.TIMESTEPS,
                                rule=_H_F_4_rule)

        def _H_L_FG_max_rule(block, n, t):
            """Set max. flue gas loss as share fuel flow share."""
            expr = 0
            expr += - self.H_L_FG_max[n, t]
            expr += self.H_F[n, t] * \
                list(n.fuel_input.values())[0].H_L_FG_share_max[t]
            return expr == 0
        self.H_L_FG_max_definition = Constraint(self.GENERICCHPS, m.TIMESTEPS,
                                                rule=_H_L_FG_max_rule)

        def _Q_max_restriction_rule(block, n, t):
            """Set maximum Q depending on fuel and eletrical flow."""
            expr = 0
            expr += self.P[n, t] + self.Q[n, t] + self.H_L_FG_max[n, t]
            expr += list(n.heat_output.values())[0].Q_CW_min[t] * self.Y[n, t]
            expr += - self.H_F[n, t]
            if n.back_pressure is True:
                return expr == 0
            else:
                return expr <= 0
        self.Q_max_restriction = Constraint(self.GENERICCHPS, m.TIMESTEPS,
                                            rule=_Q_max_restriction_rule)

        # for motoric CHPs a minimum restriction for heat flows can be added
        for n in group:
            if hasattr(list(n.fuel_input.values())[0], 'H_L_FG_share_min'):

                self.H_L_FG_min = Var(self.GENERICCHPS, m.TIMESTEPS,
                                      within=NonNegativeReals)

                def _H_L_FG_min_rule(block, n, t):
                    """Set min. flue gas loss as fuel flow share."""
                    expr = 0
                    expr += - self.H_L_FG_min[n, t]
                    expr += self.H_F[n, t] * \
                        list(n.fuel_input.values())[0].H_L_FG_share_min[t]
                    return expr == 0
                self.H_L_FG_min_definition = Constraint(self.GENERICCHPS,
                                                        m.TIMESTEPS,
                                                        rule=_H_L_FG_min_rule)

                def _Q_min_restriction_rule(block, n, t):
                    """Set minimum Q depending on fuel and eletrical flow."""
                    expr = 0
                    expr += self.P[n, t] + self.Q[n, t] + self.H_L_FG_min[n, t]
                    expr += list(n.heat_output.values())[0].Q_CW_min[t] \
                        * self.Y[n, t]
                    expr += - self.H_F[n, t]
                    return expr >= 0
                self.Q_min_restriction = Constraint(self.GENERICCHPS,
                                                    m.TIMESTEPS,
                                                    rule=_Q_min_restriction_rule)

    def _objective_expression(self):
        """Objective expression for generic CHPs with no investment.

        Note: This adds only fixed costs as variable costs are already
        added in the Block :class:`Flow`.
        """
        if not hasattr(self, 'GENERICCHPS'):
            return 0

        fixed_costs = 0

        m = self.parent_block()

        for n in self.GENERICCHPS:
            if n.fixed_costs is not None:
                P_max = [list(n.electrical_output.values())[0].P_max_woDH[t]
                         for t in m.TIMESTEPS]
                fixed_costs += max(P_max) * n.fixed_costs

        self.fixed_costs = Expression(expr=fixed_costs)

        return fixed_costs

# ------------------------------------------------------------------------------
# End of generic CHP block
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Start of VariableFractionTransformer component
# ------------------------------------------------------------------------------

class VariableFractionTransformer(LinearTransformer):
    """
    Component `GenericCHP` to model combined heat and power plants.

    A linear transformer with more than one output, where the fraction of
    the output flows is variable. By now it is restricted to two output flows.

    One main output flow has to be defined and is tapped by the remaining flow.
    Thus, the main output will be reduced if the tapped output increases.
    Therefore a loss index has to be defined. Furthermore a maximum efficiency
    has to be specified if the whole flow is led to the main output
    (tapped_output = 0). The state with the maximum tapped_output is described
    through conversion factors equivalent to the LinearTransformer.

    Parameters
    ----------
    conversion_factors : dict
        Dictionary containing conversion factors for conversion of inflow
        to specified outflow. Keys are output bus objects.
        The dictionary values can either be a scalar or a sequence with length
        of time horizon for simulation.
    conversion_factor_single_flow : dict
        The efficiency of the main flow if there is no tapped flow. Only one
        key is allowed. Use one of the keys of the conversion factors. The key
        indicates the main flow. The other output flow is the tapped flow.

    Examples
    --------
    >>> bel = Bus(label='electricityBus')
    >>> bth = Bus(label='heatBus')
    >>> bgas = Bus(label='commodityBus')
    >>> vft = VariableFractionTransformer(
    ...    label='variable_chp_gas',
    ...    inputs={bgas: Flow(nominal_value=10e10)},
    ...    outputs={bel: Flow(), bth: Flow()},
    ...    conversion_factors={bel: 0.3, bth: 0.5},
    ...    conversion_factor_single_flow={bel: 0.5})

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.VariableFractionTransformer`
    """

    def __init__(self, conversion_factor_single_flow, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversion_factor_single_flow = {
            k: sequence(v) for k, v in conversion_factor_single_flow.items()}


# ------------------------------------------------------------------------------
# End of VariableFractionTransformer component
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Start of VariableFractionTransformer block
# ------------------------------------------------------------------------------

class VariableFractionTransformerBlock(SimpleBlock):
    """Block for the linear relation of nodes with type
    :class:`~oemof.solph.network.VariableFractionTransformer`

    **The following sets are created:** (-> see basic sets at
    :class:`.OperationalModel` )

    VARIABLE_FRACTION_TRANSFORMERS
        A set with all
        :class:`~oemof.solph.network.VariableFractionTransformer` objects.

    **The following constraints are created:**

    Variable i/o relation :attr:`om.VariableFractionTransformer.relation[i,o,t]`
        .. math::
            flow(input, n, t) = \\\\
            (flow(n, main\_output, t) + flow(n, tapped\_output, t) \\cdot \
            main\_flow\_loss\_index(n, t)) /\\\\
            efficiency\_condensing(n, t)\\\\
            \\forall t \\in \\textrm{TIMESTEPS}, \\\\
            \\forall n \\in \\textrm{VARIABLE\_FRACTION\_TRANSFORMERS}.

    Out flow relation :attr:`om.VariableFractionTransformer.relation[i,o,t]`
        .. math::
            flow(n, main\_output, t) = flow(n, tapped\_output, t) \\cdot \\\\
            conversion\_factor(n, main\_output, t) / \
            conversion\_factor(n, tapped\_output, t\\\\
            \\forall t \\in \\textrm{TIMESTEPS}, \\\\
            \\forall n \\in \\textrm{VARIABLE\_FRACTION\_TRANSFORMERS}.
    """

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_value(self, value):
        pass

    def clear(self):
        pass

    def _create(self, group=None):
        """ Creates the linear constraint for the class:`LinearTransformer`
        block.

        Parameters
        ----------
        group : list
            List of oemof.solph.LinearTransformers (trsf) objects for which
            the linear relation of inputs and outputs is created
            e.g. group = [trsf1, trsf2, trsf3, ...]. Note that the relation
            is created for all existing relations of the inputs and all outputs
            of the transformer. The components inside the list need to hold
            a attribute `conversion_factors` of type dict containing the
            conversion factors from inputs to outputs.
        """
        if group is None:
            return None

        m = self.parent_block()

        for n in group:
            n.inflow = list(n.inputs)[0]
            n.label_main_flow = str(
                [k for k, v in n.conversion_factor_single_flow.items()][0])
            n.main_output = [o for o in n.outputs
                             if n.label_main_flow == o.label][0]
            n.tapped_output = [o for o in n.outputs
                               if n.label_main_flow != o.label][0]
            n.conversion_factor_single_flow_sq = (
                n.conversion_factor_single_flow[
                    m.es.groups[n.main_output.label]])
            n.flow_relation_index = [
                n.conversion_factors[m.es.groups[n.main_output.label]][t] /
                n.conversion_factors[m.es.groups[n.tapped_output.label]][t]
                for t in m.TIMESTEPS]
            n.main_flow_loss_index = [
                (n.conversion_factor_single_flow_sq[t] -
                 n.conversion_factors[m.es.groups[n.main_output.label]][t]) /
                n.conversion_factors[m.es.groups[n.tapped_output.label]][t]
                for t in m.TIMESTEPS]

        def _input_output_relation_rule(block):
            """Connection between input, main output and tapped output.
            """
            for t in m.TIMESTEPS:
                for g in group:
                    lhs = m.flow[g.inflow, g, t]
                    rhs = (
                        (m.flow[g, g.main_output, t] +
                         m.flow[g, g.tapped_output, t] *
                         g.main_flow_loss_index[t]) /
                        g.conversion_factor_single_flow_sq[t]
                        )
                    block.input_output_relation.add((n, t), (lhs == rhs))
        self.input_output_relation = Constraint(group, noruleinit=True)
        self.input_output_relation_build = BuildAction(
            rule=_input_output_relation_rule)

        def _out_flow_relation_rule(block):
            """Relation between main and tapped output in full chp mode.
            """
            for t in m.TIMESTEPS:
                for g in group:
                    lhs = m.flow[g, g.main_output, t]
                    rhs = (m.flow[g, g.tapped_output, t] *
                           g.flow_relation_index[t])
                    block.out_flow_relation.add((g, t), (lhs >= rhs))
        self.out_flow_relation = Constraint(group, noruleinit=True)
        self.out_flow_relation_build = BuildAction(
                rule=_out_flow_relation_rule)

# ------------------------------------------------------------------------------
# End of VariableFractionTransformer block
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Start of generic CAES component
# ------------------------------------------------------------------------------

class GenericCAES(Transformer):
    """
    Component `GenericCAES` to model arbitrary compressed air energy storages.

    The full set of equations is described in:
    Kaldemeyer, C.; Boysen, C.; Tuschy, I.
    A Generic Formulation of Compressed Air Energy Storage as
    Mixed Integer Linear Program – Unit Commitment of Specific
    Technical Concepts in Arbitrary Market Environments
    Materials Today: Proceedings 00 (2018) 0000–0000
    [currently in review]

    Parameters
    ----------
    fuel_input : dict
        Dictionary with key-value-pair of `oemof.Bus` and `oemof.Flow` object
        for the fuel input.
    electrical_output : dict
        Dictionary with key-value-pair of `oemof.Bus` and `oemof.Flow` object
        for the electrical output.
    heat_output : dict
        Dictionary with key-value-pair of `oemof.Bus` and `oemof.Flow` object
        for the electrical output.

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.GenericCAES`
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fuel_input = kwargs.get('fuel_input')
        self.electrical_output = kwargs.get('electrical_output')
        self.heat_output = kwargs.get('electrical_output')
        self.params = kwargs.get('params')

# ------------------------------------------------------------------------------
# End of generic CAES component
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Start of CAES block
# ------------------------------------------------------------------------------

class GenericCAESBlock(SimpleBlock):
    """Block for nodes of class:`.GenericCAES`."""

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """
        Create constraints for GenericCAESBlock.

        Parameters
        ----------
        group : list
            List containing `.GenericCAES` objects.
            e.g. groups=[gcaes1, gcaes2,..]
        """
        m = self.parent_block()

        if group is None:
            return None

        self.GENERICCAES = Set(initialize=[n for n in group])

        # variables
        self.H_F = Var(self.GENERICCHPS, m.TIMESTEPS, within=NonNegativeReals)

        def _h_flow_connection_rule(block, n, t):
            """Link fuel consumption to component inflow."""
            expr = 0
            expr += self.H_F[n, t]
            expr += - m.flow[list(n.fuel_input.keys())[0], n, t]
            return expr == 0
        self.h_flow_connection = Constraint(self.GENERICCHPS, m.TIMESTEPS,
                                            rule=_h_flow_connection_rule)

# ------------------------------------------------------------------------------
# End of CAES block
# ------------------------------------------------------------------------------


def component_grouping(node):
    if isinstance(node, GenericStorage) and isinstance(node.investment,
                                                       Investment):
        return GenericInvestmentStorageBlock
    if isinstance(node, GenericStorage) and not isinstance(node.investment,
                                                           Investment):
        return GenericStorageBlock
    if isinstance(node, GenericCHP):
        return GenericCHPBlock
    if isinstance(node, VariableFractionTransformer):
        return VariableFractionTransformerBlock
