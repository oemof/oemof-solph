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
import oemof.network as on
import warnings
from .options import Investment
from .plumbing import sequence


# ------------------------------------------------------------------------------
# Start of generic storage component
# ------------------------------------------------------------------------------
class GenericStorage(on.Transformer):
    """

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
    """ Storages (no investment)

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
    """Storage with an :class:`.Investment` object.


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

        # checking add. vars
        self.my_scalar_var = Var(self.INVESTSTORAGES, within=NonNegativeReals,
                                 bounds=(0, 10000), initialize=5000)
        self.my_sequence_var = Var(self.INVESTSTORAGES, m.TIMESTEPS,
                                   within=NonNegativeReals,
                                   bounds=(0, 10000), initialize=5000)

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
class GenericCHP(on.Transformer):
    """

    Parameters
    ----------
    Bla : numeric
        Some description

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.GenericCHP`
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.P = kwargs.get('P')
        self.Q = kwargs.get('Q')
        self.P_max_woDH = sequence(kwargs.get('P_max_woDH'))
        self.P_min_woDH = sequence(kwargs.get('P_min_woDH'))
        self.Q_CW_min = sequence(kwargs.get('Q_CW_min'))
        self.Eta_el_max_woDH = sequence(kwargs.get('Eta_el_max_woDH'))
        self.Eta_el_min_woDH = sequence(kwargs.get('Eta_el_min_woDH'))
        self.electrical_bus = kwargs.get('electrical_bus')
        self.heat_bus = kwargs.get('heat_bus')
        self.Beta = sequence(kwargs.get('Beta'))
        self.fixed_costs = sequence(kwargs.get('fixed_costs'))


def storage_nominal_value_warning(flow):
    msg = ("The nominal_value should not be set for {0} flows of storages." +
           "The value will be overwritten by the product of the " +
           "nominal_capacity and the nominal_{0}_capacity_ratio.")
    warnings.warn(msg.format(flow), SyntaxWarning)


# ------------------------------------------------------------------------------
# End of generic CHP component
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Start of generic CHP block
# ------------------------------------------------------------------------------


class GenericCHPBlock(SimpleBlock):
    """
    Block for the linear relation of nodes with type class:`.GenericCHP`.
    """

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _convert_to_sequence(self, m=None, node=None, attrs=None):
        """Set param constant over time if it is not passed time-dependent."""
        if not all(len(getattr(node, a)) == len(m.TIMESTEPS) for a in attrs):
            for a in attrs:
                seq = sequence([getattr(node, a)[0] for t in m.TIMESTEPS])
                setattr(node, a, seq)
        return node

    def _calculate_alphas(self, node=None, attrs=None):
        """
        Calculate alpha coefficients.

        A system of linear equations is created from passed capacities and
        efficiencies and solved to calculate both coefficients.
        """
        alpha1, alpha2 = [], []

        attrs = [node.P_min_woDH, node.Eta_el_min_woDH,
                 node.P_max_woDH, node.Eta_el_max_woDH]
        max_length = max([len(a) for a in attrs])

        if all(len(a) == max_length for a in attrs):
            if max_length == 0:
                max_length += 1  # increment dimension for scalars from 0 to 1
            for i in range(0, max_length):
                A = np.array([[1, node.P_min_woDH[i]],
                              [1, node.P_max_woDH[i]]])
                b = np.array([node.P_min_woDH[i] / node.Eta_el_min_woDH[i],
                              node.P_max_woDH[i] / node.Eta_el_max_woDH[i]])
                x = np.linalg.solve(A, b)
                alpha1.append(x[0])
                alpha2.append(x[1])
        else:
            error_message = ('Attributes to calculate alphas ' +
                             'must be of same dimension.')
            raise ValueError(error_message)

        return alpha1, alpha2

    def _create(self, group=None):
        """
        Create constraints for GenericCHPBlock.

        Parameters
        ----------
        group : list
            List containing storage objects.
            e.g. groups=[storage1, storage2,..]
        """
        m = self.parent_block()

        if group is None:
            return None

        for n in group:

            # assign in and outflows
            FH = {n: [i for i in n.inputs]}
            FQ = {n: [o for o in n.outputs if o is n.heat_bus]}
            FP = {n: [o for o in n.outputs if o is n.electrical_bus]}

            # convert scalar attributes into sequences
            attrs = ['P_max_woDH', 'P_min_woDH', 'Eta_el_max_woDH',
                     'Eta_el_min_woDH', 'Q_CW_min', 'Beta']
            n = self._convert_to_sequence(m, n, attrs)

            # calculate alpha coefficients
            n.alpha1 = self._calculate_alphas(n, attrs)[0]
            n.alpha2 = self._calculate_alphas(n, attrs)[1]

        self.GENERICCHPS = Set(initialize=[n for n in group])

        # @TODO:
        #   0. does it make sense to set flow attrs subsequently since they are created at first?
        #   yes, in the base class!
        #   1. set P_max, P_min, Q_min as bounds properly or use attributes
        #      instead or create flows internally in constructor and pass params
        #   2. declare Qmin, etc. as params over time and align equations
        #   3. if these are flow attributes, these can be accessed via
        #      FQ[0].attribute_name
        # update flows by heat_bus={bla: {attr1: 1, attr2: 'foo'}}

        # variables
        self.H_F = Var(self.GENERICCHPS, m.TIMESTEPS, within=NonNegativeReals)
        self.H_L_FG = Var(self.GENERICCHPS, m.TIMESTEPS,
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
            expr += - m.flow[FH[n][0], n, t]
            return expr == 0
        self.h_flow_connection = Constraint(self.GENERICCHPS, m.TIMESTEPS,
                                            rule=_h_flow_connection_rule)

        def _q_flow_connection_rule(block, n, t):
            """Link heat flow to component outflow."""
            expr = 0
            expr += self.Q[n, t]
            expr += - m.flow[n, FQ[n][0], t]
            return expr == 0
        self.q_flow_connection = Constraint(self.GENERICCHPS, m.TIMESTEPS,
                                            rule=_q_flow_connection_rule)

        def _p_flow_connection_rule(block, n, t):
            """Link power flow to component outflow."""
            expr = 0
            expr += self.P[n, t]
            expr += - m.flow[n, FP[n][0], t]
            return expr == 0
        self.p_flow_connection = Constraint(self.GENERICCHPS, m.TIMESTEPS,
                                            rule=_p_flow_connection_rule)

        def _H_F_1_rule(block, n, t):
            """Set P_woDH depending on H_F."""
            expr = 0
            expr += - self.H_F[n, t]
            expr += n.alpha1[t] * self.Y[n, t]
            expr += n.alpha2[t] * self.P_woDH[n, t]
            return expr == 0
        self.H_F_1 = Constraint(self.GENERICCHPS, m.TIMESTEPS,
                                rule=_H_F_1_rule)

        def _H_F_2_rule(block, n, t):
            """Determine relation between H_F, P and Q."""
            expr = 0
            expr += - self.H_F[n, t]
            expr += n.alpha1[t] * self.Y[n, t]
            expr += n.alpha2[t] * (self.P[n, t] + n.Beta[t] * self.Q[n, t])
            return expr == 0
        self.H_F_2 = Constraint(self.GENERICCHPS, m.TIMESTEPS,
                                rule=_H_F_2_rule)

        def _H_F_3_rule(block, n, t):
            """Set upper value of operating range via H_F."""
            expr = 0
            expr += self.H_F[n, t]
            expr += - self.Y[n, t] * (n.P_max_woDH[t] / n.Eta_el_max_woDH[t])
            return expr <= 0
        self.H_F_3 = Constraint(self.GENERICCHPS, m.TIMESTEPS,
                                rule=_H_F_3_rule)

        def _H_F_4_rule(block, n, t):
            """Set lower value of operating range via H_F."""
            expr = 0
            expr += self.H_F[n, t]
            expr += - self.Y[n, t] * (n.P_min_woDH[t] / n.Eta_el_min_woDH[t])
            return expr >= 0
        self.H_F_4 = Constraint(self.GENERICCHPS, m.TIMESTEPS,
                                rule=_H_F_4_rule)

        def _P_restriction_rule(block, n, t):
            """Restrict P depending on fuel and heat flow."""
            expr = 0
            expr += self.P[n, t] + self.Q[n, t] + self.H_L_FG[n, t]
            expr += n.Q_CW_min[t] * self.Y[n, t]
            expr += - self.H_F[n, t]
            return expr <= 0
        self.P_restriction = Constraint(self.GENERICCHPS, m.TIMESTEPS,
                                        rule=_P_restriction_rule)

    def _objective_expression(self):
        """Objective expression for generic CHPs with no investment.

        Note: This adds only fixed costs as variable costs are already
        added in the Block :class:`Flow`.
        """
        if not hasattr(self, 'GENERICCHPS'):
            return 0

        fixed_costs = 0

        # m = self.parent_block()
        #
        # for n in self.GENERICCHPS:
        #     if n.fixed_costs is not None:
        #         P_max = max([n.P_max_woDH[t] for t in m.TIMESTEPS])
        #         fixed_costs += P_max * n.fixed_costs
        #         #fixed_costs += n.P_max_woDH * n.fixed_costs
        #
        # self.fixed_costs = Expression(expr=fixed_costs)

        return fixed_costs


def custom_grouping(node):
    if isinstance(node, GenericStorage) and isinstance(node.investment,
                                                       Investment):
        return GenericInvestmentStorageBlock
    if isinstance(node, GenericStorage) and not isinstance(node.investment,
                                                           Investment):
        return GenericStorageBlock
    if isinstance(node, GenericCHP):
        return GenericCHPBlock
