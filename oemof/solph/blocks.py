# -*- coding: utf-8 -*-
"""

"""
from pyomo.core import (Var, NonNegativeReals, Set, Constraint, BuildAction,
                        Expression)
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


class InvestmentStorage(SimpleBlock):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """
        """
        m = self.parent_block()
        if group is None:
            return None

        self.INVESTSTORAGES = Set(initialize=[n for n in group])

        self.INITIAL_CAPACITY = Set(initialize=[
            n for n in group if n.initial_capacity is not None])

        # The capacity is set as a non-negative variable, therefore it makes no
        # sense to create an additional constraint if the lower bound is zero
        # for all time steps.
        self.MIN_INVESTSTORAGES = Set(
            initialize=[n for n in group if sum(
                [n.capacity_min[t] for t in m.TIMESTEPS]) > 0])

        # Set capacity variable
        self.capacity = Var(self.INVESTSTORAGES, m.TIMESTEPS,
                            within=NonNegativeReals)

        # Set invest storage variable
        def _storage_investvar_bound_rule(block, n):
            """ Returns bounds for invest_flow variable
            """
            return 0, n.investment.maximum
        self.invest_storage = Var(self.INVESTSTORAGES, within=NonNegativeReals,
                                  bounds=_storage_investvar_bound_rule)

        # Set capacity of last timestep to fixed value of initial_capacity
        self.t_end = len(m.TIMESTEPS) - 1

        def _initial_capacity_invest_rule(block, n):
            """
            """
            return (self.capacity[n, self.t_end] == n.initial_capacity *
                    self.invest_storage[n])
        self.initial_capacity_invest = Constraint(
            self.INITIAL_CAPACITY, rule=_initial_capacity_invest_rule)

        # ToDo Connection between invest_flow of input and invest_storage
        def _storage_capacity_input_invest_rule(block, n):
            """ Returns the storage balance for every storage n in timestep t
            """
            return (m.InvestmentFlow.invest_flow[m.INPUTS[n], n] ==
                    self.invest_storage[n] * n.nominal_input_capacity_ratio)
        self.storage_capacity_input_invest = Constraint(
            self.INVESTSTORAGES, rule=_storage_capacity_input_invest_rule)

        # Connection between invest_flow of output and invest_storage
        def _storage_capacity_output_invest_rule(block, n):
            """ Returns the storage balance for every storage n in timestep t
            """
            return (m.InvestmentFlow.invest_flow[n, m.OUTPUTS[n]] ==
                    self.invest_storage[n] * n.nominal_output_capacity_ratio)
        self.storage_capacity_output_invest = Constraint(
            self.INVESTSTORAGES, rule=_storage_capacity_output_invest_rule)

        # Set the upper bound of the storage capacity
        def _max_capacity_invest_rule(block, n, t):
            """
            """
            expr = (self.capacity[n, t] <= (n.capacity_max[t] *
                                            self.invest_storage[n]))
            return expr
        self.max_capacity_invest = Constraint(
            self.INVESTSTORAGES, m.TIMESTEPS, rule=_max_capacity_invest_rule)

        # Set the lower bound of the storage capacity if the attribute exists
        def _min_investstorage_rule(block, n, t):
            """
            """
            expr = (self.capacity[n, t] <= (n.capacity_min[t] *
                                            self.invest_storage[n]))
            return expr
        self.min_investstorage = Constraint(
            self.MIN_INVESTSTORAGES, m.TIMESTEPS, rule=_min_investstorage_rule)

        # ToDo: objective functions

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
        ############################ SETS #####################################
        # set for all flows with an global limit on the flow over time
        self.SUMMED_MAX_FLOWS = Set(initialize=[(g[0], g[1])
                                    for g in group
                                        if g[2].summed_max is not None])

        self.SUMMED_MIN_FLOWS = Set(initialize=[(g[0], g[1])
                                    for g in group
                                        if g[2].summed_min is not None])

        ########################### CONSTRAINTS ###############################

        # constraint to bound the sum of a flow over all timesteps with maxim.
        self.summed_max = Constraint(self.SUMMED_MAX_FLOWS, noruleinit=True)
        def _flow_summed_max_rule(model):
            for i, o in self.SUMMED_MAX_FLOWS:
                lhs = sum(m.flow[i, o, t] * m.timeincrement
                          for t in m.TIMESTEPS)
                rhs = (m.flows[i, o].summed_max *
                       m.flows[i, o].nominal_value)
                self.summed_max.add((i, o), lhs <= rhs)
        self.summed_max_build = BuildAction(rule=_flow_summed_max_rule)

        # constraint to bound the sum of a flow over all timesteps with minim.
        self.summed_min = Constraint(self.SUMMED_MIN_FLOWS, noruleinit=True)
        def _flow_summed_min_rule(model):
            """ Rule for build action
            """
            for i, o in self.SUMMED_MIN_FLOWS:
                lhs = sum(m.flow[i, o, t] * m.timeincrement
                          for t in m.TIMESTEPS)
                rhs = (m.flows[i, o].summed_min *
                       m.flows[i, o].nominal_value)
                self.summed_min.add((i, o), lhs >= rhs)
        self.summed_min_build = BuildAction(rule=_flow_summed_min_rule)


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
                   m.flows[i,o].nominal_value is not None):
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
        ############################ SETS #####################################
        self.FLOWS = Set(initialize=[(g[0], g[1]) for g in group])

        self.FIXEDFLOWS = Set(
            initialize=[(g[0], g[1]) for g in group if g[2].fixed])

        self.SUMMED_MAX_FLOWS = Set(
            initialize=[(g[0], g[1])
            for g in group if g[2].summed_max is not None])

        self.SUMMED_MIN_FLOWS = Set(
            initialize=[(g[0], g[1])
                        for g in group if g[2].summed_min is not None])

        self.MAX_FLOWS = Set(
            initialize=[(g[0], g[1])
                        for g in group if len(g[2].max) != 0])

        self.MIN_FLOWS = Set(
            initialize=[(g[0], g[1])
                        for g in group if len(g[2].min) != 0])

        ########################### VARIABLES ##################################
        def _investvar_bound_rule(block, i, o):
            """ Returns bounds for invest_flow variable
            """
            return 0, m.flows[i, o].investment.maximum
        # create variable bounded for flows with investement attribute
        self.flow = Var(self.FLOWS, within=NonNegativeReals,
                        bounds=_investvar_bound_rule)

        ########################### CONSTRAINTS ###############################
        def _investflow_bound_rule(block, i, o, t):
            """ Returns constraint to bound flow variable if flow investment
            """
            return (m.flow[i, o, t] == (self.invest_flow[i, o] *
                                        m.flows[i, o].actual_value[t]))
        # create constraint to bound flow variable
        self.bounds = Constraint(self.FIXEDFLOWS, m.TIMESTEPS,
                                 rule=_investflow_bound_rule)

        def _max_investflow_rule(block, i, o, t):
            """
            """
            expr = (m.flow[i, o, t] <= (m.flows[i, o].max[t] *
                                        self.flow[i, o]))
            return expr
        self.max = Constraint(self.MAX_FLOWS, m.TIMESTEPS,
                              rule=_max_investflow_rule)

        def _min_investflow_rule(block, i, o, t):
            """
            """
            expr = (m.flow[i, o, t] >= (m.flows[i, o].min[t] *
                                        self.flow[i, o]))
            return expr
        self.min = Constraint(self.MIN_FLOWS, m.TIMESTEPS,
                              rule=_min_investflow_rule)

        def _summed_max_investflow_rule(block, i, o):
            """
            """
            expr = (sum(m.flow[i, o, t] * m.timeincrement
                        for t in m.TIMESTEPS) <=
                m.flows[i, o].summed_max * self.flow[i, o])
            return expr
        self.summed_max = Constraint(self.SUMMED_MAX_FLOWS,
                                     rule=_summed_max_investflow_rule)

        def _summed_min_investflow_rule(block, i, o):
            """
            """
            expr = (sum(m.flow[i, o, t] * m.timeincrement
                        for t in m.TIMESTEPS) >=
                m.flows[i, o].summed_min * self.flow[i, o])
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
           for t in m.TIMESTEPS:
               # variable costs of flows
               if m.flows[i, o].variable_costs[0] is not None:
                   variable_costs += (m.flow[i, o, t] * m.timeincrement *
                                      m.flows[i, o].variable_costs[t])
           # fixed costs
           if m.flows[i, o].fixed_costs is not None:
                fixed_costs += (self.flow[i, o] *
                                m.flows[i, o].fixed_costs)
           # investment costs
           if m.flows[i, o].investment.epc is not None:
               investment_costs += (self.flow[i, o] *
                                    m.flows[i, o].investment.epc)
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
            List of oemof bus (b) object for which the busbalance is created
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
                        block.balance.add((n,t), expr)
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
