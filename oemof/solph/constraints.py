# -*- coding: utf-8 -*-
"""

"""
from pyomo.core import Var, Binary, Set, Constraint, BuildAction
from pyomo.core.base.block import SimpleBlock


class BusBalance(SimpleBlock):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def _create(self, nodes=None):
        """
        """
        m = self.parent_block()
        self.NODES = Set(initialize=[str(n) for n in nodes])
        self.INDEXSET = self.NODES * m.TIMESTEPS
        self.constraint = Constraint(self.INDEXSET, noruleinit=True)

        def _busbalance_rule(block):
            for t in m.TIMESTEPS:
                for n in block.NODES:
                    lhs = sum(m.flow[i, n, t] * m.time_increment
                              for i in m.INPUTS[n])
                    rhs = sum(m.flow[n, o, t] * m.time_increment
                              for o in m.OUTPUTS[n])
                    expr = (lhs == rhs)
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
    """ Creates pyomo contraint for linear relation of 1:n flows
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, nodes=None):
        m = self.parent_block()

        self.NODES = Set(initialize=[str(n) for n in nodes])
        self.constraint = Constraint(self.NODES, noruleinit=True)

        conversion_factors = {
            (str(n), str(k)): n.conversion_factors[k]
             for n in nodes for k in n.conversion_factors}

        def _input_output_relation(block):
            for t in m.TIMESTEPS:
                for n in block.NODES:
                    for o in m.OUTPUTS[n]:
                        lhs = m.flow[m.INPUTS[n], n, t]   * conversion_factors[(n, o)][t]
                        rhs = m.flow[n, o, t]
                        block.constraint.add((n, o, t), (lhs == rhs))
        self.constraintCon = BuildAction(rule=_input_output_relation)


def outflowcosts(m, nodes):
    """
    """
    NODES = [str(n) for n in nodes]

    expr = sum(m.flow[n, o, t] *
               m.flows[n, o].variable_costs[t]
        for n in NODES
        for o in m.OUTPUTS[n]
        for t in m.TIMESTEPS
    )

    return expr




class MinimumOutflow(SimpleBlock):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, nodes=None):
        """
        """
        m = self.parent_block()

        self.NODES = Set(initialize=[str(n) for n in nodes])

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
                        rhs = self.status[n, t] * m.es.groups[n].outputs[m.es.groups[o]].min[t]

                        block.minimum_outflow.add((n, o, t), (lhs >= rhs))

        self.constraintCon = BuildAction(rule=_minimum_outflow)
