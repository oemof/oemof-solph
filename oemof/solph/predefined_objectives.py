# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 21:01:48 2015

@author: simon
"""
try:
    import objective_expressions as objexpr
except:
    from . import objective_expressions as objexpr

import pyomo.environ as po
import oemof.solph as solph

def minimize_cost(self):
    """ Builds objective function that minimises the total costs.


    """
    expr = 0
    c_blocks = ('simple_transformer', 'simple_chp', 'fixed_source',
                'simple_storage', 'simple_transport', 'dispatch_source')
    r_blocks = ('simple_transformer', 'simple_chp', 'simple_extraction_chp')

    blocks = [block for block in self.block_data_objects(active=True)
              if not isinstance(block, solph.optimization_model.OptimizationModel)]

    for block in blocks:
        if block.name in c_blocks:
            if block.name == 'simple_storage':
                ref = 'capacity'
                expr += objexpr.add_opex_var(self, self.simple_storage,
                                             ref='input')
            else:
                ref = 'output'
            # variable costs
            expr += objexpr.add_opex_var(self, block, ref='output')
            # fix costs
            expr += objexpr.add_opex_fix(self, block, ref=ref)
            # investment costs
            if block.model_param.get('investement', False) == True:
                expr += objexpr.add_capex(self, block, ref=ref)
        # revenues
        if block.name in r_blocks:
            expr += objexpr.add_revenues(self, block, ref='output')

    # costs for dispatchable sources
    if hasattr(self, 'dispatch_source'):
        expr += objexpr.add_curtailment_costs(self, self.dispatch_source)

    if self.uids['shortage']:
        expr += objexpr.add_shortage_slack_costs(self)
    # artificial costs for excess or shortage
    if self.uids['excess']:
        expr += objexpr.add_excess_slack_costs(self)

    self.objective = po.Objective(expr=expr)
