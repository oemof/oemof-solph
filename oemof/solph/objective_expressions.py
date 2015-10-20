# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 11:34:27 2015

@author: simon
"""
import numpy as np

def add_opex_var(model, objs=None, uids=None):
    """ variable operation expenditure term for linear objective function

    """
    if uids is None:
        uids = [obj.uid for obj in objs]

    opex_var = {obj.uid: obj.opex_var for obj in objs}
    # outputs for cost objs
    O = {obj.uid: obj.outputs[0].uid for obj in objs}

    expr = sum(model.w[e, O[e], t] * opex_var[e]
               for e in uids
               for t in model.timesteps)

    return(expr)

def add_opex_fix(model, objs=None, uids=None, ref=None):
    """ Fixed operation expenditure term for linear objective function

    Parameters
    ------------
    ref : string
        string to check if capex is referred to capacity (storage) or output
        (e.g. powerplant)

    """
    if uids is None:
        uids = [obj.uid for obj in objs]

    opex_fix = {obj.uid: obj.opex_fix for obj in objs}

    if ref == 'output':
        # installed electrical/thermal output: {'pp_chp': 30000,...}
        out_max = {obj.uid: obj.out_max for obj in objs}
        out_max = {k: sum(filter(None, v.values()))
                                 for k, v in out_max.items()}
        if model.invest is False:
            expr = sum(out_max[e] * opex_fix[e] for e in uids)
        else:
            expr = sum((out_max[e] + model.add_out[e]) * opex_fix[e]
                        for e in uids)
    elif ref == 'capacity':
        cap_max = {obj.uid: obj.cap_max for obj in objs}
        if model.invest is False:
            expr = sum(cap_max[e] * opex_fix[e] for e in uids)
        else:
            expr = sum((cap_max[e] + model.add_cap[e]) * opex_fix[e]
                       for e in uids)
    else:
        print('No reference defined. Please specificy in `add_opex()`!')
    return(expr)


def add_output_revenues(model, objs=None, uids=None):
    """ revenue term for linear objective function


    """
    if uids is None:
        uids = [obj.uid for obj in objs]

    # why do we need revenues? price=0, so we just leave this code here..
    # @ CORD: the idea is that if price is constant over time-horizon,
    # a vector (array) is created
    #  if price is already a vector (array) this vector is taken
    model.output_revenues = {}
    for e in objs:
        if isinstance(e.outputs[0].price, (float, int, np.integer)):
            price = [e.outputs[0].price] * len(model.timesteps)
            model.output_revenues[e.uid] = price
        else:
            model.output_revenues[e.uid] = e.outputs[0].price

    # outputs for revemue objs (powerplant output e.g. electricty creates
    # revenues in objective function)
    O = {obj.uid: obj.outputs[0].uid for obj in objs}

    # create expression term
    expr = sum(model.w[e, O[e], t] * model.output_revenues[e][t]
               for e in uids for t in model.timesteps)
    return(expr)

def add_dispatch_source_costs(model, objs=[], uids=None):
    """ cost term for dispatchable sources in linear objective

    """
    if objs:
        if uids is None:
            uids = [obj.uid for obj in objs]
        # get dispatch expenditure for renewable energies with dispatch
        model.dispatch_ex = {obj.uid: obj.dispatch_ex for obj in objs}

        expr = sum(model.dispatch[e, t] * model.dispatch_ex[e]
                   for e in uids for t in model.timesteps)
    else:
        print('Warning: No dispatch source objects defined.  \
              No action for objective take.')

    return(expr)

def add_capex(model, objs, uids=None, ref=None):
    """ add capital expenditure to objective

    Parameters
    ------------
    ref : string
        string to check if capex is referred to capacity (storage) or output
        (e.g. powerplant)

    """

    if uids is None:
        uids = [obj.uid for obj in objs]

    capex = {obj.uid: obj.capex for obj in objs}
    crf = {obj.uid: obj.crf for obj in objs}

    if ref == 'output':
        expr = sum(model.add_out[e] * crf[e] * capex[e] for e in uids)
    if ref == 'capacity':
        expr = sum(model.add_cap[e] * crf[e] * capex[e] for e in uids)
    else:
        print('No reference defined. Please specificy in `add_capex()`')
    return(expr)

def add_startup_costs(model, objs=None, uids=None):
    """ Adds startup costs for components to objective expression

    .. math:: \\sum_{e,t} su(e,t) \\cdot su_costs(e)
    """
    if uids is None:
        uids = [obj.uid for obj in objs]

    start_costs = {obj.uid: obj.start_costs for obj in objs}
    expr = sum(getattr(model, "start_"+objs[0].lower_name)[e, t] *
               start_costs[e] for e in uids for t in model.timesteps)
    return(expr)

def add_excess_slack_costs(model, uids=None):
    """ artificial cost term for excess slack variables

    """
    if uids is None:
        uids = model.bus_uids

    expr = sum(model.excess_slack[e, t] * 3000
               for e in uids for t in model.timesteps)
    return(expr)


def add_shortage_slack_costs(model, uids=None):
    """ artificial cost term for shortage slack variables

    """
    if uids is None:
        uids = model.bus_uids

    expr = sum(model.shortage_slack[e, t] * 3000
                for e in uids for t in model.timesteps)
    return(expr)


