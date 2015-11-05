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


def minimize_cost(self):
    """ Builds objective function that minimises the total costs.


    """

    # create a combine list of all cost-related components
    cost_objs = \
        self.objs['simple_chp'] + \
        self.objs['simple_transformer'] + \
        self.objs['simple_extraction_chp'] + \
        self.objs['fixed_source']

    revenue_objs = (
        self.objs['simple_chp'] +
        self.objs['simple_transformer'])

    # objective function
    # def obj_rule(self):
    expr = 0

    expr += objexpr.add_opex_var(self, objs=cost_objs, ref='output')
    expr += objexpr.add_opex_var(self, objs=self.objs['simple_storage'],
                                 ref='output')
    expr += objexpr.add_opex_var(self, objs=self.objs['simple_storage'],
                                 ref='input')
    # fixed opex of components
    expr += objexpr.add_opex_fix(self, objs=cost_objs, ref='output')
    # fixed opex of storages
    expr += objexpr.add_opex_fix(self, objs=self.objs['simple_storage'],
                                 ref='capacity')

    # revenues from outputs of components
    expr += objexpr.add_output_revenues(self, revenue_objs)

    # costs for dispatchable sources
    expr += objexpr.add_dispatch_source_costs(self,
                                         objs=self.objs['dispatch_source'])

    # add capex for investment components
    objs_inv = [e for e in cost_objs if e.model_param['investment'] == True]
    # capital expenditure for output objects
    expr += objexpr.add_capex(self, objs=objs_inv, ref='output')
    # capital expenditure for storages
    objs_inv = [e for e in self.objs['simple_storage']
                if e.model_param['investment'] == True]
    expr += objexpr.add_capex(self, objs=objs_inv,
                              ref='capacity')

    if self.uids['shortage']:
        expr += objexpr.add_shortage_slack_costs(self)
    # artificial costs for excess or shortage
    if self.uids['excess']:
        expr += objexpr.add_excess_slack_costs(self)

    self.objective = po.Objective(expr=expr)
