# -*- coding: utf-8 -*-
"""
The module contains different objective expression terms.

@author: Simon Hilpert (simon.hilpert@fh-flensburg.de)
"""
import numpy as np
import logging

def add_opex_var(model, objs=None, uids=None, ref='output'):
    """ Variable operation expenditure term for linear objective function

    If reference of opex is `output`:

    .. math:: \\sum_e \\sum_t W(e,O(e),t) \\cdot c_{var}(e)

    If reference of opex is `input`:

    .. math:: \\sum_e \\sum_t W(I(e),e,t) \\cdot c_{var}(e)

    Parameters:
    ------------
    model : OptimizationModel() instance
    objs : objects for which term should be set
    uids : corresponding uids
    ref : reference side on which opex are based on
        (e.g. powerplant MWhth -> input or MWhel -> output)

    """
    if uids is None:
        uids = [obj.uid for obj in objs]


    opex_var = {obj.uid: obj.opex_var for obj in objs}
    # outputs for cost objs
    if ref == 'output':
        expr = sum(model.w[e, model.O[e][0], t] * opex_var[e]
                   for e in uids
                   for t in model.timesteps)
    elif ref == 'input':
        expr = sum(model.w[model.I[e], e, t] * opex_var[e]
                   for e in uids
                   for t in model.timesteps)

    return(expr)

def add_input_costs(model, objs=None, uids=None):
    """ Adds costs for usage of input (fuel, elec, etc. ) if not included in
    opex

    .. math:: \\sum_e \\sum_t W(I(e), e, t) \\cdot c_{input}(e)

    Parameters:
    ------------

    model : OptimizationModel() instance
    objs : objects for which term should be set
    uids : corresponding uids
    """
    if uids is None:
        uids = [obj.uid for obj in objs]


    input_costs = {obj.uid: obj.inputs[0].price for obj in objs}
    # outputs for cost objs

    expr = -sum(model.w[model.I[e], e, t] * input_costs[e]
                for e in uids for t in model.timesteps)

    return(expr)

def add_opex_fix(model, objs=None, uids=None, ref=None):
    """ Fixed operation expenditure term for linear objective function

    If reference is `output` (e.g. powerplants):

    .. math:: \\sum_e out_{max}(e) \\cdot c_{fix}(e)

    If reference is `capacity` (e.g. storages):

    .. math:: \\sum_e cap_{max}(e) \\cdot c_{fix}(e)

    If investment:

    .. math:: \\sum_e (out_{max}(e) + ADDOUT(e)) \\cdot c_{fix}(e)

    .. math:: \\sum_e (out_{max}(e) + ADDCAP(e)) \\cdot c_{fix}(e)

    Parameters
    ------------

    model : OptimizationModel() instance
    objs : objects for which term should be set
    uids : corresponding uids
    ref : string
        string to check if capex is referred to capacity (storage) or output
        (e.g. powerplant)

    """
    if uids is None:
        uids = [obj.uid for obj in objs]

    uids_inv = set([obj.uid for obj in objs
                   if obj.model_param['investment'] == True])
    uids = set(uids) - uids_inv

    opex_fix = {obj.uid: obj.opex_fix for obj in objs}

    if ref == 'output':
        # installed electrical/thermal output: {'pp_chp': 30000,...}
        out_max = {obj.uid: obj.out_max for obj in objs}
        out_max = {k: sum(filter(None, v.values()))
                                 for k, v in out_max.items()}
        expr = 0
        expr += sum(out_max[e] * opex_fix[e] for e in uids)
        expr += sum((out_max[e] + model.add_out[e]) * opex_fix[e]
                    for e in uids_inv)
    elif ref == 'capacity':
        cap_max = {obj.uid: obj.cap_max for obj in objs}
        expr = 0
        expr += sum(cap_max[e] * opex_fix[e] for e in uids)
        expr += sum((cap_max[e] + model.add_cap[e]) * opex_fix[e]
                       for e in uids_inv)
    else:
        print('No reference defined. Please specificy in `add_opex()`!')
    return(expr)


def add_output_revenues(model, objs=None, uids=None):
    """ revenue term for linear objective function

    .. math:: \\sum_e \\sum_t W(e,O(e),t) \\cdot r_{out}(e,t)

    Parameters
    ------------

    model : OptimizationModel() instance
    objs : objects for which term should be set
    uids : corresponding uids
    """
    if uids is None:
        uids = [obj.uid for obj in objs]

    # why do we need revenues? price=0, so we just leave this code here..
    # @ CORD: the idea is that if price is constant over time-horizon,
    # a vector (array) is created
    #  if price is already a vector (array) this vector is taken
    revenues = {}
    for e in objs:
        if isinstance(e.outputs[0].price, (float, int, np.integer)):
            price = [e.outputs[0].price] * len(model.timesteps)
            revenues[e.uid] = price
        else:
            revenues[e.uid] = e.outputs[0].price

    # outputs for revemue objs (powerplant output e.g. electricty creates
    # revenues in objective function)
    O = {obj.uid: obj.outputs[0].uid for obj in objs}

    # create expression term
    expr = -sum(model.w[e, O[e], t] * revenues[e][t]
                for e in uids for t in model.timesteps)
    return(expr)

def add_curtailment_costs(model, objs=[], uids=None):
    """ Cost term for dispatchable sources in linear objective.

    .. math:: \\sum_e \\sum_ t CURTAIL(e,t) \\cdot c_{curt}(e)

    Parameters
    ------------

    model : OptimizationModel() instance
    objs : objects for which term should be set
    uids : corresponding uids
    """

    if objs:
        if uids is None:
            uids = [obj.uid for obj in objs]
        # get dispatch expenditure for renewable energies with dispatch
        c_curtail = {obj.uid: obj.dispatch_ex for obj in objs}
        expr = sum(model.curtailment_var[e, t] * c_curtail[e]
                   for e in uids for t in model.timesteps)
    else:
        expr = 0
        logging.info('No dispatch source objects defined. ' +
                     'No action for objective taken.')
    return(expr)

def add_capex(model, objs, uids=None, ref=None):
    """ Add capital expenditure to linear objective.

    If reference is `output` (e.g. powerplants):

    .. math:: \\sum_e ADDOUT(e) \\cdot crf(e) \\cdot c_{inv}(e)

    If reference is `capacity` (e.g. storages):

    .. math:: \\sum_e ADDCAP(e) \\cdot crf(e) \\cdot c_{inv}(e)

    Parameters
    ------------

    model : OptimizationModel() instance
    objs : objects for which term should be set
    uids : corresponding uids
    ref : string
        string to check if capex is referred to capacity (storage) or output
        (e.g. powerplant)

    """

    if uids is None:
        uids = [obj.uid for obj in objs]

    c_inv = {obj.uid: obj.capex for obj in objs}
    crf = {obj.uid: obj.crf for obj in objs}

    if ref == 'output':
        expr = sum(model.add_out[e] * crf[e] * c_inv[e] for e in uids)
        return(expr)
    elif ref == 'capacity':
        expr = sum(model.add_cap[e] * crf[e] * c_inv[e] for e in uids)
        return(expr)
    else:
        print('No reference defined. Please specificy in `add_capex()`')


def add_startup_costs(model, objs=None, uids=None):
    """ Adds startup costs for components to objective expression

    .. math:: \\sum_{e} \\sum_{t} Z_{start}(e,t) \\cdot c_{start}(e)

    Parameters
    ------------

    model : OptimizationModel() instance
    objs : objects for which term should be set
    uids : corresponding uids
    """
    if uids is None:
        uids = [obj.uid for obj in objs]

    c_start = {obj.uid: obj.start_costs for obj in objs}
    z_start = getattr(model, objs[0].lower_name+'_start_var')
    expr = sum(z_start[e, t] * c_start[e]
               for e in uids for t in model.timesteps)
    return(expr)

def add_shutdown_costs(model, objs=None, uids=None):
    """ Adds shutdown costs for components to objective expression

    .. math:: \\sum_{e} \\sum_t Z_{stop}(e,t) \\cdot c_{stop}(e)

    Parameters
    ------------

    model : OptimizationModel() instance
    objs : objects for which term should be set
    uids : corresponding uids
    """

    if uids is None:
        uids = [obj.uid for obj in objs]

    c_stop = {obj.uid: obj.stop_costs for obj in objs}
    z_stop = getattr(model, objs[0].lower_name+'_stop_var')
    expr = sum(z_stop[e, t] * c_stop[e]
               for e in uids for t in model.timesteps)
    return(expr)

def add_ramping_costs(model, objs=None, uids=None):
    """ Add gradient costs for components to linear objective expression.

    .. math::  \\sum_e \\sum_t GRADPOS(e,t) \\cdot c_{ramp}(e)

    Parameters
    ------------

    model : OptimizationModel() instance
    objs : objects for which term should be set
    uids : corresponding uids
    """
    if uids is None:
        uids = [obj.uid for obj in objs]


    c_ramp = {obj.uid: obj.ramp_costs for obj in objs}
    grad_pos = getattr(model, objs[0].lower_name+'_grad_pos_var' )
    expr = sum(grad_pos[e, t] * c_ramp[e]
               for e in uids for t in model.timesteps)
    return(expr)

def add_excess_slack_costs(model, uids=None):
    """ Artificial cost term for excess slack variables.

    .. math:: \\sum_e \\sum_t EXCESS(e,t) \\cdot c_{excess}(e)

    Parameters:
    ------------

    uids : unique ids of bus objects
    """
    if uids is None:
        uids = model.uids['excess']
    c_excess = {b.uid:b.excess_costs for b in model.bus_objs}
    expr = sum(model.excess_slack[e, t] * c_excess[e]
               for e in uids for t in model.timesteps)
    return(expr)


def add_shortage_slack_costs(model, uids=None):
    """ Artificial cost term for shortage slack variables.

    .. math:: \\sum_e \\sum_t SHORTAGE(e,t) \\cdot c_{shortage}(e)

    Parameters:
    ------------

    uids : unique ids of bus objects

    """
    if uids is None:
        uids = model.uids['shortage']
    c_shortage = {b.uid: b.shortage_costs for b in model.bus_objs}
    expr = sum(model.shortage_slack[e, t] * c_shortage[e]
               for e in uids for t in model.timesteps)
    return(expr)


