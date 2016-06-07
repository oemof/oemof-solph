# -*- coding: utf-8 -*-
"""

"""
from pyomo.core import (Var, Set, Constraint, BuildAction, Expression,
                        NonNegativeReals, Binary)
from pyomo.core.base.block import SimpleBlock


class Storage(SimpleBlock):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """

        Parameters
        ----------
        group : list
            List containing storage objects e.g. groups=[storage1, storage2,..]
        """
        m = self.parent_block()

        if group is None:
            return None

        self.STORAGES = Set(initialize=[n for n in group])

        def _storage_capacity_bound_rule(block, n, t):
            """ Returns bounds for capacity variable of storage n in timestep t
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
            """ Returns the storage balance for every storage n in timestep t
            """
            expr = 0
            expr += block.capacity[n, t]
            expr += - block.capacity[n, m.previous_timesteps[t]] * (
                1 - n.capacity_loss[t])
            expr += (- m.flow[m.INPUTS[n], n, t] *
                     n.inflow_conversion_factor[t]) * m.timeincrement
            expr += (m.flow[n, m.OUTPUTS[n], t] /
                     n.outflow_conversion_factor[t]) * m.timeincrement
            return expr == 0
        self.balance = Constraint(self.STORAGES, m.TIMESTEPS,
                                  rule=_storage_balance_rule)

    def _objective_expression(self):
        """
        """
        if not hasattr(self, 'STORAGES'):
            return 0

        fixed_costs = 0

        for n in self.STORAGES:
            if n.fixed_costs is not None:
                fixed_costs += n.nominal_capacity * n.fixed_costs

        self.fixed_costs = Expression(expr=fixed_costs)

        return fixed_costs


class InvestmentStorage(SimpleBlock):
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

    capacity
        Load of the storage for every time step

    invest
        Nominal capacity of the storage


    **The following constraints are build:**

    Storage balance

    .. math:: l_n(t) = l_n(t_{previous}) \\cdot (1 - C^{loss}(n)) \
    - \\frac{w_{n, o_n}(t)}{\\eta^{out}_n} \
    + w_{i_n, n}(t) \\cdot \\eta^{in}_n

    With
    :math:`\\textrm{~}\\; \\forall n \\in \\textrm{INVESTSTORAGES} \\textrm{,}
    \\; \\forall t \\in \\textrm{TIMESTEPS}`.

    Minimal capacity

    .. math:: l_n(t) <= c_{invest} \cdot c_{min}(t)

    With
    :math:`\\textrm{~}\\; \\forall n \\in \\textrm{MIN\_INVESTSTORAGES} \\textrm{,}
    \\; \\forall t \\in \\textrm{TIMESTEPS}`.

    etc.

    **The following parts of the objective function are created:**

    etc.
    """
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
            """ Returns bounds for invest_flow variable
            """
            return 0, n.investment.maximum
        self.invest = Var(self.INVESTSTORAGES, within=NonNegativeReals,
                          bounds=_storage_investvar_bound_rule)

        # ######################### CONSTRAINTS ###############################
        def _storage_balance_rule(block, n, t):
            """ Returns the storage balance for every storage n in timestep t.
            """
            expr = 0
            expr += block.capacity[n, t]
            expr += - block.capacity[n, m.previous_timesteps[t]] * (
                1 - n.capacity_loss[t])
            expr += (- m.flow[m.INPUTS[n], n, t] *
                     n.inflow_conversion_factor[t]) * m.timeincrement
            expr += (m.flow[n, m.OUTPUTS[n], t] /
                     n.outflow_conversion_factor[t]) * m.timeincrement
            return expr == 0
        self.balance = Constraint(self.INVESTSTORAGES, m.TIMESTEPS,
                                  rule=_storage_balance_rule)

        def _initial_capacity_invest_rule(block, n):
            """Set capacity of last timestep to fixed value of initial_capacity.
            """
            expr = (self.capacity[n, self.t_end] == (n.initial_capacity *
                                                     self.invest[n]))
            return expr
        self.t_end = len(m.TIMESTEPS) - 1
        self.initial_capacity_invest = Constraint(
            self.INITIAL_CAPACITY, rule=_initial_capacity_invest_rule)

        def _storage_capacity_input_invest_rule(block, n):
            """ Connection between invest_flow of input and invest
            """
            expr = (m.InvestmentFlow.invest[m.INPUTS[n], n] ==
                    self.invest[n] * n.nominal_input_capacity_ratio)
            return expr
        self.storage_capacity_input_invest = Constraint(
            self.INVESTSTORAGES, rule=_storage_capacity_input_invest_rule)

        def _storage_capacity_output_invest_rule(block, n):
            """ Connection between invest_flow of output and invest
            """
            expr = (m.InvestmentFlow.invest[n, m.OUTPUTS[n]] ==
                    self.invest[n] * n.nominal_output_capacity_ratio)
            return expr
        self.storage_capacity_output_invest = Constraint(
            self.INVESTSTORAGES, rule=_storage_capacity_output_invest_rule)

        def _max_capacity_invest_rule(block, n, t):
            """Set the upper bound of the storage capacity
            """
            expr = (self.capacity[n, t] <= (n.capacity_max[t] *
                                            self.invest[n]))
            return expr
        self.max_capacity_invest = Constraint(
            self.INVESTSTORAGES, m.TIMESTEPS, rule=_max_capacity_invest_rule)

        def _min_investstorage_rule(block, n, t):
            """Set the lower bound of the storage capacity
            """
            expr = (self.capacity[n, t] <= (n.capacity_min[t] *
                                            self.invest[n]))
            return expr
        # Set the lower bound of the storage capacity if the attribute exists
        self.min_investstorage = Constraint(
            self.MIN_INVESTSTORAGES, m.TIMESTEPS, rule=_min_investstorage_rule)

    def _objective_expression(self):
        """
        """
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


class Flow(SimpleBlock):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """

        Parameters
        ----------
        group : list
            List containing tuples containing flow (f) objects and the
            associated source (s) and target (t)
            of flow e.g. groups=[(s1, t1, f1), (s2, t2, f2),..]


        """
        if group is None:
            return None

        m = self.parent_block()

        # ########################## SETS #####################################
        # set for all flows with an global limit on the flow over time
        self.SUMMED_MAX_FLOWS = Set(initialize=[
            (g[0], g[1]) for g in group if g[2].summed_max is not None])

        self.SUMMED_MIN_FLOWS = Set(initialize=[
            (g[0], g[1]) for g in group if g[2].summed_min is not None])

        self.NEGATIVE_GRADIENT_FLOWS = Set(
            initialize=[(g[0], g[1]) for g in group
                        if g[2].negative_gradient[0] is not None])

        self.POSITIVE_GRADIENT_FLOWS = Set(
            initialize=[(g[0], g[1]) for g in group
                        if g[2].positive_gradient[0] is not None])

        # ######################### Variables  ################################
        # set upper bound of gradient variable
        for i, o, f in group:
            if m.flows[i, o].positive_gradient[0] is not None:
                for t in m.TIMESTEPS:
                    m.positive_flow_gradient[i, o, t].setub(
                        f.positive_gradient[t] * f.nominal_value)
            if m.flows[i, o].negative_gradient[0] is not None:
                for t in m.TIMESTEPS:
                    m.negative_flow_gradient[i, o, t].setub(
                        f.negative_gradient[t] * f.nominal_value)

        # ######################### CONSTRAINTS ###############################

        def _flow_summed_max_rule(model):
            """constraint to bound the sum of a flow over all timesteps with
             maxim"""
            for inp, out in self.SUMMED_MAX_FLOWS:
                lhs = sum(m.flow[inp, out, ts] * m.timeincrement
                          for ts in m.TIMESTEPS)
                rhs = (m.flows[inp, out].summed_max *
                       m.flows[inp, out].nominal_value)
                self.summed_max.add((inp, out), lhs <= rhs)
        self.summed_max = Constraint(self.SUMMED_MAX_FLOWS, noruleinit=True)
        self.summed_max_build = BuildAction(rule=_flow_summed_max_rule)

        def _flow_summed_min_rule(model):
            """ Rule for build action. Constraint to bound the sum of a flow
            over all timesteps with minim.
            """
            for inp, out in self.SUMMED_MIN_FLOWS:
                lhs = sum(m.flow[inp, out, ts] * m.timeincrement
                          for ts in m.TIMESTEPS)
                rhs = (m.flows[inp, out].summed_min *
                       m.flows[inp, out].nominal_value)
                self.summed_min.add((inp, out), lhs >= rhs)
        self.summed_min = Constraint(self.SUMMED_MIN_FLOWS, noruleinit=True)
        self.summed_min_build = BuildAction(rule=_flow_summed_min_rule)

        def _positive_gradient_flow_rule(model):
            """constraint for positive gradient
            """
            for inp, out in self.POSITIVE_GRADIENT_FLOWS:
                for ts in m.TIMESTEPS:
                    if ts > 0:
                        lhs = m.flow[inp, out, ts] - m.flow[inp, out, ts-1]
                        rhs = m.positive_flow_gradient[inp, out, ts]
                        self.positive_gradient_constr.add((inp, out, ts),
                                                          lhs <= rhs)
                    else:
                        pass  # return(Constraint.Skip)
        self.positive_gradient_constr = Constraint(group, noruleinit=True)
        self.positive_gradient_build = BuildAction(
            rule=_positive_gradient_flow_rule)

        def _negative_gradient_flow_rule(model):
            """constraint for negative gradient
            """
            for inp, out in self.NEGATIVE_GRADIENT_FLOWS:
                for ts in m.TIMESTEPS:
                    if ts > 0:
                        lhs = m.flow[i, o, t] - m.flow[inp, out, ts-1]
                        rhs = m.positive_flow_gradient[inp, out, ts]
                        self.negative_gradient_constr.add((inp, out, ts),
                                                          lhs <= rhs)
                    else:
                        pass  # return(Constraint.Skip)

        self.negative_gradient_constr = Constraint(group, noruleinit=True)
        self.negative_gradient_build = BuildAction(
            rule=_negative_gradient_flow_rule)

    def _objective_expression(self):
        """
        """
        m = self.parent_block()

        variable_costs = 0
        fixed_costs = 0

        for i, o in m.FLOWS:
            for t in m.TIMESTEPS:
                # add variable costs
                if m.flows[i, o].variable_costs[0] is not None:
                    variable_costs += (m.flow[i, o, t] * m.timeincrement *
                                       m.flows[i, o].variable_costs[t])
            # add fixed costs if nominal_value is not None
            if (m.flows[i, o].fixed_costs and
                    m.flows[i, o].nominal_value is not None):
                fixed_costs += (m.flows[i, o].nominal_value *
                                m.flows[i, o].fixed_costs)

        # add the costs expression to the block
        self.fixed_costs = Expression(expr=fixed_costs)
        self.variable_costs = Expression(expr=variable_costs)

        return fixed_costs + variable_costs


class InvestmentFlow(SimpleBlock):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """

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
        self.FLOWS = Set(initialize=[(g[0], g[1]) for g in group])

        self.FIXEDFLOWS = Set(
            initialize=[(g[0], g[1]) for g in group if g[2].fixed])

        self.SUMMED_MAX_FLOWS = Set(initialize=[
            (g[0], g[1]) for g in group if g[2].summed_max is not None])

        self.SUMMED_MIN_FLOWS = Set(initialize=[
            (g[0], g[1]) for g in group if g[2].summed_min is not None])

        self.MAX_FLOWS = Set(initialize=[
            (g[0], g[1]) for g in group if len(g[2].max) != 0])

        self.MIN_FLOWS = Set(initialize=[
            (g[0], g[1]) for g in group if len(g[2].min) != 0])

        # ######################### VARIABLES #################################
        def _investvar_bound_rule(block, i, o):
            """ Returns bounds for invest_flow variable
            """
            return 0, m.flows[i, o].investment.maximum
        # create variable bounded for flows with investement attribute
        self.invest = Var(self.FLOWS, within=NonNegativeReals,
                          bounds=_investvar_bound_rule)

        # ######################### CONSTRAINTS ###############################

        # TODO: Add gradient constraints

        def _investflow_bound_rule(block, i, o, t):
            """ Returns constraint to bound flow variable if flow investment
            """
            return (m.flow[i, o, t] == (self.invest[i, o] *
                                        m.flows[i, o].actual_value[t]))
        self.bounds = Constraint(self.FIXEDFLOWS, m.TIMESTEPS,
                                 rule=_investflow_bound_rule)

        def _max_investflow_rule(block, i, o, t):
            """
            """
            expr = (m.flow[i, o, t] <= (m.flows[i, o].max[t] *
                                        self.invest[i, o]))
            return expr
        self.max = Constraint(self.MAX_FLOWS, m.TIMESTEPS,
                              rule=_max_investflow_rule)

        def _min_investflow_rule(block, i, o, t):
            """
            """
            expr = (m.flow[i, o, t] >= (m.flows[i, o].min[t] *
                                        self.invest[i, o]))
            return expr
        self.min = Constraint(self.MIN_FLOWS, m.TIMESTEPS,
                              rule=_min_investflow_rule)

        def _summed_max_investflow_rule(block, i, o):
            """
            """
            expr = (sum(m.flow[i, o, t] * m.timeincrement
                        for t in m.TIMESTEPS) <=
                    m.flows[i, o].summed_max * self.invest[i, o])
            return expr
        self.summed_max = Constraint(self.SUMMED_MAX_FLOWS,
                                     rule=_summed_max_investflow_rule)

        def _summed_min_investflow_rule(block, i, o):
            """
            """
            expr = (sum(m.flow[i, o, t] * m.timeincrement
                        for t in m.TIMESTEPS) >=
                    m.flows[i, o].summed_min * self.invest[i, o])
            return expr
        self.summed_min = Constraint(self.SUMMED_MIN_FLOWS,
                                     rule=_summed_min_investflow_rule)

    def _objective_expression(self):
        """
        """
        m = self.parent_block()
        fixed_costs = 0
        variable_costs = 0
        investment_costs = 0

        for i, o in self.FLOWS:
            # fixed costs
            if m.flows[i, o].fixed_costs is not None:
                fixed_costs += (self.invest[i, o] *
                                m.flows[i, o].fixed_costs)
            # investment costs
            if m.flows[i, o].investment.ep_costs is not None:
                investment_costs += (self.invest[i, o] *
                                     m.flows[i, o].investment.ep_costs)
            else:
                raise ValueError("Missing value for investment costs!")

        self.investment_costs = Expression(expr=investment_costs)
        self.fixed_costs = Expression(expr=fixed_costs)
        self.variable_costs = Expression(expr=variable_costs)

        return fixed_costs + variable_costs + investment_costs


class Bus(SimpleBlock):
    """ Creates emtpy pyomo constraint for bus balance. Construct the
    constraints with _create method.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """ Creates the linear constraints for the BusBalance block.

        Parameters
        ----------
        group : list
            List of oemof bus (b) object for which the bus balance is created
            e.g. group = [b1, b2, b3, .....]
        """
        if group is None:
            return None

        m = self.parent_block()

        self.balance = Constraint(group, noruleinit=True)

        def _busbalance_rule(block):
            for t in m.TIMESTEPS:
                for n in group:
                    lhs = sum(m.flow[i, n, t] * m.timeincrement
                              for i in n.inputs)
                    rhs = sum(m.flow[n, o, t] * m.timeincrement
                              for o in n.outputs)
                    expr = (lhs == rhs)
                    # no inflows no outflows yield: 0 == 0 which is True
                    if expr is not True:
                        block.balance.add((n, t), expr)
        self.balance_build = BuildAction(rule=_busbalance_rule)


class LinearTransformer(SimpleBlock):
    """ Creates pyomo emtpy constraint for linear relation of 1:n flows.
    Construct the constraints with _create method.

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """ Creates the linear constraint for the LinearRelation block.

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

        self.relation = Constraint(group, noruleinit=True)

        def _input_output_relation(block):
            for t in m.TIMESTEPS:
                for n in group:
                    for o in n.outputs:
                        lhs = m.flow[m.INPUTS[n], n, t] * \
                            n.conversion_factors[o][t]
                        rhs = m.flow[n, o, t]
                        block.relation.add((n, o, t), (lhs == rhs))
        self.relation_build = BuildAction(rule=_input_output_relation)


class Discrete(SimpleBlock):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """ Creates the linear constraint for the LinearRelation block.

        Parameters
        ----------
        group : list
            List of oemof.solph.DiscreteFlow objects for which
            the constraints are build.
        """
        if group is None:
            return None

        m = self.parent_block()
        # ########################## SETS #####################################

        self.FLOWS = Set(initialize=[(g[0], g[1]) for g in group])

        self.MIN_FLOWS = Set(initialize=[(g[0], g[1]) for g in group
                                         if g[2].min[0] != 0])

        self.STARTCOSTFLOWS = Set(initialize=[(g[0], g[1]) for g in group
                                  if g[2].discrete.start_costs is not None])

        # ################### VARIABLES AND CONSTRAINTS #######################
        self.status = Var(self.FLOWS, m.TIMESTEPS, within=Binary)

        def _minimum_flow_rule(block, i, o, t):
            expr = (self.status[i, o, t] *
                    m.flows[i, o].min[t] * m.flows[i, o].nominal_value >=
                    m.flow[i, o, t])
            return expr
        self.minimum_flow = Constraint(self.MIN_FLOWS, m.TIMESTEPS,
                                       rule=_minimum_flow_rule)

        def _maximum_flow_rule(block, i, o, t):
            expr = (self.status[i, o, t] *
                    m.flows[i, o].max[t] * m.flows[i, o].nominal_value <=
                    m.flow[i, o, t])
            return expr
        self.maximum_flow = Constraint(self.MIN_FLOWS, m.TIMESTEPS,
                                       rule=_maximum_flow_rule)

        # TODO: Add gradient constraints for discrete block / flows
        # TODO: Add objective expression for discrete block / flows
