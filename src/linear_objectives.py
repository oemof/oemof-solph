# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 11:34:27 2015

@author: simon
"""
import pyomo.environ as po

def objective_cost_min(model, cost_objs=None, revenue_objs=None):
    """Function that creates the objective function of the optimization
    model.

    Parameters
    ----------
    model : pyomo.ConcreteModel
    cost_objects : oemof objects that are related with costs in the objective
    revenue_objs: oemof objects that are related with revenues in the objective

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

    # operational expenditure
    model.opex_var = {obj.uid: obj.opex_var for obj in cost_objs}
    model.opex_fix = {obj.uid: obj.opex_fix for obj in cost_objs}
    model.input_costs = {obj.uid: obj.inputs[0].price for obj in cost_objs}

    # installed electrical/thermal capacity: {'pp_chp': 30000,...}
    model.cap_installed = {obj.uid: obj.out_max for obj in cost_objs}
    model.cap_installed = {k: sum(filter(None, v.values()))
                           for k, v in model.cap_installed.items()}

    # why do we need revenues? price=0, so we just leave this code here..
    # @ CORD: the idea is that if price is constant over time-horizon,
    # a vector (array) is created
    #  if price is already a vector (array) this vector is taken
    model.output_revenues = {}
    for obj in revenue_objs:
        if isinstance(obj.outputs[0].price, (float, int)):
            price = [obj.outputs[0].price] * len(model.timesteps)
            model.output_revenues[obj.uid] = price
        else:
            model.output_revenues[obj.uid] = obj.outputs[0].price

    # get dispatch expenditure for renewable energies with dispatch
    model.dispatch_ex = {obj.uid: obj.dispatch_ex
                         for obj in model.dispatch_source_objs}

    # objective function
    def obj_rule(model):
        expr = 0

        # variable opex including resource consumption
        expr += sum(model.w[I[e], e, t] *
                    (model.input_costs[e] + model.opex_var[e])
                    for e in cost_uids for t in model.timesteps)

        # fixed opex of components
        expr += sum(model.cap_installed[e] * (model.opex_fix[e])
                    for e in cost_uids)

        # revenues from outputs of components
        expr += - sum(model.w[e, O[e], t] * model.output_revenues[e][t]
                      for e in revenue_uids for t in model.timesteps)

        # dispatch costs
        if model.dispatch_source_objs:
            expr += sum(model.dispatch[e, t] * model.dispatch_ex[e]
                        for e in model.dispatch_source_uids
                        for t in model.timesteps)

        # add additional capacity & capex for investment models
        if(model.invest is True):
            model.capex = {obj.uid: obj.capex for obj in cost_objs}
            model.crf = {obj.uid: obj.crf for obj in cost_objs}

            expr += sum(model.add_cap[I[e], e] * model.crf[e] *
                        (model.capex[e] + model.opex_fix[e])
                        for e in model.cost_uids)
            expr += sum(model.soc_add[e] * model.crf[e] *
                        (model.capex[e] + model.opex_fix[e])
                        for e in model.simple_storage_uids)

        # artificial costs for excess or shortage
        if model.slack["excess"] is True:
            expr += sum(model.excess_slack[e, t] * 3000
                        for e in model.bus_uids for t in model.timesteps)
        if model.slack["shortage"] is True:
            expr += sum(model.shortage_slack[e, t] * 3000
                        for e in model.bus_uids for t in model.timesteps)
        return(expr)
    model.objective = po.Objective(rule=obj_rule)


