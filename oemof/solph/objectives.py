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
    """
    """

    # create a combine list of all cost-related components
    cost_objs = \
        self.objs['simple_chp'] + \
        self.objs['simple_transformer'] + \
        self.objs['simple_transport']

    revenue_objs = (
        self.objs['simple_chp'] +
        self.objs['simple_transformer'])

    # objective function
    #def obj_rule(self):
    expr = 0

    expr += objexpr.add_opex_var(self,
                                 objs=cost_objs+self.objs['simple_storage'])
    # fixed opex of components
    expr += objexpr.add_opex_fix(self, objs=cost_objs, ref='output')
    # fixed opex of storages
    expr += objexpr.add_opex_fix(self, objs=self.objs['simple_storage'],
                                 ref='capacity')

    # revenues from outputs of components
    expr += - objexpr.add_output_revenues(self, revenue_objs)

    # costs for dispatchable sources
    expr += objexpr.add_dispatch_source_costs(self,
                                         objs=self.objs['dispatch_source'])
    if self.milp is True:
        expr += objexpr.add_startup_costs(self,
                                          objs=self.objs['simple_transformer'])
        expr += objexpr.add_startup_costs(self,
                                          objs=self.objs['simple_chp'])
    # add capex for investment models
    if(self.invest is True):
        # capital expenditure for output objects
        objexpr.add_capex(self, objs=cost_objs, ref='output')
        # capital expenditure for storages
        objexpr.add_capex(self, objs=self.objs['simple_storage'],
                          ref='capacity')

    if self.slack["shortage"] is True:
        expr += objexpr.add_shortage_slack_costs(self)
    # artificial costs for excess or shortage
    if self.slack["excess"] is True:
        expr += objexpr.add_excess_slack_costs(self)

    self.objective = po.Objective(expr=expr)

def minimize_co2_emissions(self):
    """
    """
