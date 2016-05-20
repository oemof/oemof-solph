# -*- coding: utf-8 -*-
"""

"""
from pyomo.core import Var, Binary, NonNegativeReals, Set, Constraint, BuildAction
from pyomo.core.base.block import SimpleBlock


class Investment(SimpleBlock):
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
        m = self.parent_block()
        # pyomo set with investment flows as list of tuples
        self.INVESTFLOWS = Set(initialize=[(str(g[0]), str(g[1]))
                                           for g in group])

        def _invest_bound_rule(block, i, o):
            """ Returns bounds for invest_flow variable
            """
            return (0, m.flows[i, o].investment.maximum)
        # create variable bounded for flows with investement attribute
        self.invest_flow = Var(self.INVESTFLOWS, within=NonNegativeReals,
                               bounds=_invest_bound_rule)

        def _invest_bounds(block, i, o, t):
            """ Returns constraint to bound flow variable if flow investment
            """
            return m.flow[i,o,t] <= self.invest_flow[i,o]
        # create constraint to bound flow variable
        self.invest_bounds = Constraint(self.INVESTFLOWS, m.TIMESTEPS,
                                        rule=_invest_bounds)


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
        m = self.parent_block()
        self.NODES = Set(initialize=[str(n) for n in group])
        self.INDEXSET = self.NODES * m.TIMESTEPS
        self.constraint = Constraint(self.INDEXSET, noruleinit=True)

        def _busbalance_rule(block):
            for t in m.TIMESTEPS:
                for n in block.NODES:
                    lhs = sum(m.flow[i, n, t] * m.timeincrement
                              for i in m.INPUTS[n])
                    rhs = sum(m.flow[n, o, t] * m.timeincrement
                              for o in m.OUTPUTS[n])
                    expr = (lhs == rhs)
                    # no inflows no outflows yield: 0 == 0 which is True
                    if expr is not True:
                        block.constraint.add((n,t), expr)
        self.constraintCon = BuildAction(rule=_busbalance_rule)




# TODO: Implement this as a block
#        self.flowlimits =  pyomo.Constraint(self.FLOWS,
#                                            rule=self._summend_flowlimit_rule)
#    @staticmethod
#    def _summend_flowlimit_rule(self, o, i):
#        """
#        """
#        return (
#            sum(self.flow[o, i, t] * self.time_increment
#                for t in self.TIMESTEPS) <= self.flows[o, i].summed
#        )

#
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
        m = self.parent_block()

        self.NODES = Set(initialize=[str(n) for n in group])
        self.constraint = Constraint(self.NODES, noruleinit=True)

        conversion_factors = {
            (str(n), str(k)): n.conversion_factors[k]
             for n in group for k in n.conversion_factors}

        def _input_output_relation(block):
            for t in m.TIMESTEPS:
                for n in block.NODES:
                    for o in m.OUTPUTS[n]:
                        lhs = m.flow[m.INPUTS[n], n, t] * \
                                conversion_factors[(n, o)][t]
                        rhs = m.flow[n, o, t]
                        block.constraint.add((n, o, t), (lhs == rhs))
        self.constraintCon = BuildAction(rule=_input_output_relation)



# This is just for no for test puposes
class MinimumOutflow(SimpleBlock):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """
        """
        m = self.parent_block()
        self.NODES = Set(initialize=[str(n) for n in group])
        # create status variable
        self.status = Var(self.NODES, m.TIMESTEPS, within=Binary)
        # create "empty" constraint
        self.minimum_outflow = Constraint(self.NODES, noruleinit=True)

    def _build(self):
        """
        """
        m = self.parent_block()

        def _minimum_outflow(block):
            for t in m.TIMESTEPS:
                for n in block.NODES:
                    for o in m.OUTPUTS[n]:
                        lhs = m.flow[n, o, t]
                        rhs = self.status[n, t] * \
                            m.es.groups[n].outputs[m.es.groups[o]].min[t]
                        block.minimum_outflow.add((n, o, t), (lhs >= rhs))
        self.constraintCon = BuildAction(rule=_minimum_outflow)
