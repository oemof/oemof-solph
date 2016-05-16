# -*- coding: utf-8 -*-
"""

"""
from pyomo.core import Set, Constraint
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

        #@staticmethod
        def _busbalance_rule(block, n, t):
            lhs = sum(m.flow[i, n, t] * m.time_increment for i in m.INPUTS[n])
            rhs = sum(m.flow[n, o, t] * m.time_increment for o in m.OUTPUTS[n])
            return (lhs == rhs)

        self.NODES = Set(initialize=[str(n) for n in nodes])
        self.INDEXSET = self.NODES * m.TIMESTEPS
        self.constraint = Constraint(self.INDEXSET,
                                     rule=_busbalance_rule)

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
#class LinearRelation(Block):
#    """
#    """
#    def __init__(self, *args, **kwargs):
#        super().__init__()
#        self.parent = self.parent_block()
#        self.nodes = kwargs.get('nodes')
#
#        self.conversion_factors = {k:n.conversion_factor[k]
#                                   for n in self.nodes
#                                   for k in n.conversion_factor.keys()}
#        self._create()
#    def _create(self):
#
#        # block subset of nodes with str of node
#        self.NODES = Set(initialize=[str(n) for n in self.nodes])
#        #
#        self.constraint = Constraint(self.NODES, self.parent.TIMESTEPS,
#                                     rule=self._input_output_relation)
#
#    def _input_output_relation(self, n, t):
#
#        i, o = self.parent.FLOWS[n]
#        lhs = self.parent.flow[i, o, t] * conversion_factor[i,o][t]
#
#        rhs = self.parent.flow[n, self.parent.OUTPUTS[n][idx], t]
#
#        return lhs == rhs

