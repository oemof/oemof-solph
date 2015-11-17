# -*- coding: utf-8 -*-
"""
This module contains predefined objectives that can be used to model
energysystems.

@author: Simon Hilpert (simon.hilpert@fh-flensburg.de)
"""
try:
    import objective_expressions as objexpr
except:
    from . import objective_expressions as objexpr

import pyomo.environ as po
import oemof.solph as solph

def minimize_cost(self, c_blocks=(), r_blocks=()):
    """ Builds objective function that minimises the total costs.

    Costs included are:
                        opex_var,
                        opex_fix,
                        curtailment_costs (dispatch sources),
                        annulised capex (investment components)

    Parameters:
    ------------
    self : pyomo model instance
    c_blocks : pyomo blocks containing components that are included in
               cost terms of objective function
    r_blocks : pyomo blocks containing components that are included in revenue
               terms of objective function
    """
    expr = 0
    c_blocks = ('simple_transformer', 'simple_chp', 'fixed_source',
                'simple_storage', 'simple_transport', 'dispatch_source')
    r_blocks = ('simple_transformer', 'simple_chp', 'simple_extraction_chp')

    blocks = [block for block in self.block_data_objects(active=True)
              if not isinstance(block,
                                solph.optimization_model.OptimizationModel)]

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
            # input costs
            if 'input_costs' in block.model_param.get('objective'):
                expr += objexpr.add_input_costs(self, block)
            # fix costs
            expr += objexpr.add_opex_fix(self, block, ref=ref)
            # investment costs
            if block.model_param.get('investment', False) == True:
                expr += objexpr.add_capex(self, block, ref=ref)
            # revenues
        if block.name in r_blocks:
            expr += objexpr.add_revenues(self, block, ref='output')

    # costs for dispatchable sources
    if hasattr(self, 'dispatch_source'):
        expr += objexpr.add_curtailment_costs(self, self.dispatch_source)

    if self.bus.shortage_uids:
        expr += objexpr.add_shortage_slack_costs(self, block)
    # artificial costs for excess or shortage
    if self.bus.excess_uids:
        expr += objexpr.add_excess_slack_costs(self, block)

    self.objective = po.Objective(expr=expr)

def uc_minimize_costs(self, c_block=(), r_block=()):
    """ Unit commitment min. cost objective

    Costs that are included:
       For objects in c_blocks:
                          opex_var,
                          input costs (e.g. fuel),
                          startup costs (only milp models),
                          shutdown costs (only milp models)
                          ramp costs
       For objects in r_blocks:
                          output revenues
       Other:
          excess, slack costs for additional slack variables per bus (if exist)

    Parameters:
    ------------
    self : pyomo model instance
    c_blocks : pyomo blocks containing components that are included in
               cost terms of objective function
    r_blocks : pyomo blocks containing components that are included in revenue
               terms of objective function

    """
    c_blocks = ('simple_transformer', 'simple_chp', 'simple_extraction_chp')
    r_blocks = ('simple_transformer', 'simple_chp', 'simple_extraction_chp')

    blocks = [block for block in self.block_data_objects(active=True)
              if not isinstance(block,
                                solph.optimization_model.OptimizationModel)]
    expr = 0
    for block in blocks:
        if block.name in c_blocks:
            # variable costs
            expr += objexpr.add_opex_var(self, block, ref='output')
            # input costs
            expr += objexpr.add_input_costs(self, block)
            # startup costs
            if 'startup' in block.model_param.get('milp_constr', ()):
                expr += objexpr.add_startup_costs(self, block)
            # shutdown costs
            if 'shutdown' in block.model_param.get('milp_constr', ()):
                expr += objexpr.add_shutdown_costs(self, block)
            # ramp costs
            if 'ramping' in block.model_param.get('linear_constr', ()):
                expr += objexpr.add_ramping_costs(self, block)
        if block.name in r_blocks:
            expr += objexpr.add_revenues(self, block, ref='output')

    if self.uids['shortage']:
        expr += objexpr.add_shortage_slack_costs(self)
    # artificial costs for excess or shortage
    if self.uids['excess']:
        expr += objexpr.add_excess_slack_costs(self)


    self.objective = po.Objective(expr=expr)

