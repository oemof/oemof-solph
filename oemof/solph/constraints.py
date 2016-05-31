# -*- coding: utf-8 -*-
"""

"""
import pyomo.environ as pyomo
from pyomo.core import Var, Binary, NonNegativeReals, Set, Constraint, BuildAction
from pyomo.core.base.block import SimpleBlock


class StorageBalance(SimpleBlock):
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

        # dictionaries to use in the _storage_capacity_bound_rule
        ub_capacity = {}
        lb_capacity = {}
        capacity_loss = {}
        inflow_conversion = {}
        outflow_conversion = {}
        # fill dictionaries with storage objects attributes from group list
        for t in m.TIMESTEPS:
            for n in group:
                ub_capacity[n, t] = n.nominal_capacity * n.capacity_max[t]
                lb_capacity[n, t] = n.nominal_capacity * n.capacity_min[t]
                capacity_loss[n, t] = n.capacity_loss[t]
                inflow_conversion[n, t] = n.inflow_conversion_factor[t]
                outflow_conversion[n, t] = n.outflow_conversion_factor[t]

        # ToDo Minimal capacity bound (lb_capacity)
        def _storage_capacity_bound_rule(block, n, t):
            """ Returns bound for capacity variable of storage n in timestep t
            """
            return 0, ub_capacity[n, t]
        self.capacity = Var(self.STORAGES, m.TIMESTEPS,
                            bounds=_storage_capacity_bound_rule)

        # set capacity of last timestep to fixed value of initial_capacity
        self.t_end = len(m.TIMESTEPS) - 1
        for n in group:
            if n.initial_capacity is not None:
                self.capacity[n, self.t_end] = (n.initial_capacity *
                                                n.nominal_capacity)
                self.capacity[n, self.t_end].fix()

        def _storage_balance_rule(block, n, t):
            """ Returns the storage balance for every storage n in timestep t
            """
            # TODO: include time increment
            expr = 0
            expr += block.capacity[n, t]
            expr += - block.capacity[n, m.previous_timestep[t]] * (
                1 - capacity_loss[n, t])
            expr += - m.flow[m.INPUTS[n], n, t] * inflow_conversion[n, t]
            expr += + m.flow[n, m.OUTPUTS[n], t] / outflow_conversion[n, t]
            return expr, 0
        self.storage_balance = Constraint(self.STORAGES, m.TIMESTEPS,
                                          rule=_storage_balance_rule)


class InvestmentStorageBalance(SimpleBlock):
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
                            within=pyomo.NonNegativeReals)

        # Set invest storage variable
        def _storage_investvar_bound_rule(block, n):
            """ Returns bounds for invest_flow variable
            """
            return 0, n.investment.maximum
        self.invest_storage = Var(self.INVESTSTORAGES, within=NonNegativeReals,
                                  bounds=_storage_investvar_bound_rule)

        # Set capacity of last timestep to fixed value of initial_capacity
        self.t_end = len(m.TIMESTEPS) - 1

        def _initial_capacity_invest_rule(block, n, t):
            """
            """
            return (self.capacity[n, self.t_end] == n.initial_capacity *
                    self.invest_storage[n])
        self.initial_capacity_invest = Constraint(
            self.INITIAL_CAPACITY, m.TIMESTEPS,
            rule=_initial_capacity_invest_rule)

        # ToDo Connection between invest_flow of input and invest_storage
        # def _storage_capacity_input_invest_rule(block, n):
        #     """ Returns the storage balance for every storage n in timestep t
        #     """
        #     return (m.InvestmentFlow.invest_flow[m.INPUTS[n], n] <=
        #             self.invest_storage[n])
        # self.storage_capacity_input_invest = Constraint(
        #     self.INVESTSTORAGES, rule=_storage_capacity_input_invest_rule)

        # Connection between invest_flow of output and invest_storage
        def _storage_capacity_output_invest_rule(block, n):
            """ Returns the storage balance for every storage n in timestep t
            """
            return (m.InvestmentFlow.invest_flow[n, m.OUTPUTS[n]] <=
                    self.invest_storage[n])
        self.storage_capacity_input_invest = Constraint(
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
        # pyomo set with investment flows as list of tuples
        self.INVESTFLOWS = Set(initialize=[(g[0], g[1]) for g in group])

        self.FIXEDFLOWS = Set(
            initialize=[(g[0], g[1]) for g in group if g[2].fixed])

        self.SUMMED_MAX_INVESTFLOWS = Set(
            initialize=[(g[0], g[1])
            for g in group if g[2].summed_max is not None])

        self.SUMMED_MIN_INVESTFLOWS = Set(
            initialize=[(g[0], g[1])
                        for g in group if g[2].summed_min is not None])

        self.MAX_INVESTFLOWS = Set(
            initialize=[(g[0], g[1])
                        for g in group if len(g[2].max) != 0])

        self.MIN_INVESTFLOWS = Set(
            initialize=[(g[0], g[1])
                        for g in group if len(g[2].min) != 0])

        ########################### VARIABLES ##################################
        def _investvar_bound_rule(block, i, o):
            """ Returns bounds for invest_flow variable
            """
            return 0, m.flows[i, o].investment.maximum
        # create variable bounded for flows with investement attribute
        self.invest_flow = Var(self.INVESTFLOWS, within=NonNegativeReals,
                               bounds=_investvar_bound_rule)

        ########################### CONSTRAINTS ###############################
        def _investflow_bound_rule(block, i, o, t):
            """ Returns constraint to bound flow variable if flow investment
            """
            return (m.flow[i, o, t] == (self.invest_flow[i, o] *
                                        m.flows[i, o].actual_value[t]))
        # create constraint to bound flow variable
        self.invest_bounds = Constraint(self.FIXEDFLOWS, m.TIMESTEPS,
                                        rule=_investflow_bound_rule)

        def _max_investflow_rule(block, i, o, t):
            """
            """
            expr = (m.flow[i, o, t] <= (m.flows[i, o].max[t] *
                                        self.invest_flow[i, o]))
            return expr
        self.max_investflow = Constraint(self.MAX_INVESTFLOWS, m.TIMESTEPS,
                                         rule=_max_investflow_rule)

        def _min_investflow_rule(block, i, o, t):
            """
            """
            expr = (m.flow[i, o, t] >= (m.flows[i, o].min[t] *
                                        self.invest_flow[i, o]))
            return expr
        self.min_investflow = Constraint(self.MIN_INVESTFLOWS, m.TIMESTEPS,
                                         rule=_min_investflow_rule)

        def _summed_max_investflow_rule(block, i, o):
            """
            """
            expr = (sum(m.flow[i, o, t] for t in m.TIMESTEPS) <=
                    m.flows[i, o].summed_max * self.invest_flow[i, o])
            return expr
        self.summed_max_investflow = Constraint(
            self.SUMMED_MAX_INVESTFLOWS, rule=_summed_max_investflow_rule)

        def _summed_min_investflow_rule(block, i, o):
            """
            """
            expr = (sum(m.flow[i, o, t] for t in m.TIMESTEPS) >=
                    m.flows[i, o].summed_min * self.invest_flow[i, o])
            return expr
        self.summed_min_investflow = Constraint(
            self.SUMMED_MIN_INVESTFLOWS, rule=_summed_min_investflow_rule)


    def _objective_expression(self):
        """
        """
        m = self.parent_block()
        expr = 0
        for i, o in self.INVESTFLOWS:
           if m.flows[i, o].fixed_costs is not None:
                expr += self.invest_flow[i, o] * m.flows[i, o].fixed_costs
           if m.flows[i, o].investment.epc is not None:
               expr += self.invest_flow[i, o] * m.flows[i, o].investment.epc
           else:
               raise ValueError("Missing value for investment costs")
        return expr


class BusBalance(SimpleBlock):
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

        self.constraint = Constraint(group, noruleinit=True)

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
                        block.constraint.add((n,t), expr)
        self.constraintCon = BuildAction(rule=_busbalance_rule)


class LinearRelation(SimpleBlock):
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

        self.constraint = Constraint(group, noruleinit=True)

        def _input_output_relation(block):
            for t in m.TIMESTEPS:
                for n in group:
                    for o in m.OUTPUTS[n]:
                        lhs = m.flow[m.INPUTS[n], n, t] * n.conversion_factors[o][t]
                        rhs = m.flow[n, o, t]
                        block.constraint.add((n, o, t), (lhs == rhs))
        self.constraintCon = BuildAction(rule=_input_output_relation)



def VariableCosts(m, group=None):
    """
    """
    if group is None:
        return 0

    VARIABLECOST_FLOWS = [(g[0], g[1]) for g in group]

    expr = sum(m.flow[i, o, t] * m.flows[i, o].variable_costs[t]
               for i, o in VARIABLECOST_FLOWS
               for t in m.TIMESTEPS)

    return expr

