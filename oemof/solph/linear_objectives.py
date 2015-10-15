# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 11:34:27 2015

@author: simon
"""
import pyomo.environ as po
import numpy as np

def objective_cost_min(model, cost_objs=None, revenue_objs=None):
    """Function that creates the objective function of the optimization
    model.

    Parameters
    ----------
    model : pyomo.ConcreteModel
    cost_objects : oemof objects that are related with costs in the objective
    revenue_objs : oemof objects that are related with revenues in
    the objective

    Returns
    -------
    m : pyomo.ConcreteModel
    """

    cost_uids = {obj.uid for obj in cost_objs}
    revenue_uids = {obj.uid for obj in revenue_objs}

    # inputs for cost objs (powerplant input e.g. gas -> creates
    # cost in objective function)
    I = {obj.uid: obj.inputs[0].uid for obj in cost_objs}
    # outputs for revemue objs (powerplant output e.g. electricty creates
    # revenues in objective function)
    O = {obj.uid: obj.outputs[0].uid for obj in revenue_objs}

    def sum_opex_var(model):
        """ variable operation expenditure term for linear objective function

        """
        model.opex_var = {obj.uid: obj.opex_var for obj in cost_objs}
        model.input_costs = {obj.uid: obj.inputs[0].price for obj in cost_objs}

        expr = sum(model.w[I[e], e, t] *
            (model.input_costs[e] + model.opex_var[e])
            for e in cost_uids for t in model.timesteps)
        return(expr)

    def sum_opex_fix(model):
        """ fixed operation expenditure term for linear objective function

        """
        model.opex_fix = {obj.uid: obj.opex_fix for obj in cost_objs}
        # installed electrical/thermal capacity: {'pp_chp': 30000,...}
        model.cap_installed = {obj.uid: obj.out_max for obj in cost_objs}
        model.cap_installed = {k: sum(filter(None, v.values()))
                               for k, v in model.cap_installed.items()}
        # create expression term
        expr = sum(model.cap_installed[e] * (model.opex_fix[e])
                    for e in cost_uids)
        return(expr)

    def sum_output_revenues(model):
        """ revenue term for linear objective function


        """
        # why do we need revenues? price=0, so we just leave this code here..
        # @ CORD: the idea is that if price is constant over time-horizon,
        # a vector (array) is created
        #  if price is already a vector (array) this vector is taken
        model.output_revenues = {}
        for obj in revenue_objs:
            if isinstance(obj.outputs[0].price, (float, int, np.integer)):
                price = [obj.outputs[0].price] * len(model.timesteps)
                model.output_revenues[obj.uid] = price
            else:
                model.output_revenues[obj.uid] = obj.outputs[0].price

        # create expression term
        expr = sum(model.w[e, O[e], t] * model.output_revenues[e][t]
                   for e in revenue_uids for t in model.timesteps)
        return(expr)

    def sum_dispatch_source_costs(model):
        """ cost termn for dispatchable sources in linear objective

        """
        # get dispatch expenditure for renewable energies with dispatch
        model.dispatch_ex = {obj.uid: obj.dispatch_ex
                             for obj in model.objs['dispatch_source']}
        expr = sum(model.dispatch[e, t] * model.dispatch_ex[e]
                   for e in model.uids['dispatch_source']
                   for t in model.timesteps)
        return(expr)

    def sum_excess_slack_costs(model):
        """ artificial cost term for excess slack variables
    
        """
        expr = sum(model.excess_slack[e, t] * 3000
                   for e in model.bus_uids for t in model.timesteps)
        return(expr)


    def sum_shortage_slack_costs(model):
        """ artificial cost term for shortage slack variables

        """
        expr = sum(model.shortage_slack[e, t] * 3000
                    for e in model.bus_uids for t in model.timesteps)
        return(expr)


    # objective function
    def obj_rule(model):
        expr = 0

        # variable opex including resource consumption
        expr += sum_opex_var(model)

        # fixed opex of components
        expr += sum_opex_fix(model)

        # revenues from outputs of components
        expr += - sum_output_revenues(model)

        if model.objs['dispatch_source']:
            # disptach cost for sources
            expr += sum_dispatch_source_costs(model)

        # add additional capacity & capex for investment models
        if(model.invest is True):
            model.capex = {obj.uid: obj.capex for obj in cost_objs}
            model.crf = {obj.uid: obj.crf for obj in cost_objs}

            expr += sum(model.add_cap[e] * model.crf[e] *
                        (model.capex[e] + model.opex_fix[e])
                        for e in cost_uids)
            expr += sum(model.soc_add[e] * model.crf[e] *
                        (model.capex[e] + model.opex_fix[e])
                        for e in model.uids['simple_storage'])

        if model.slack["shortage"] is True:
            expr += sum_shortage_slack_costs(model)
        # artificial costs for excess or shortage
        if model.slack["excess"] is True:
            expr += sum_excess_slack_costs(model)

        return(expr)
    model.objective = po.Objective(rule=obj_rule)
