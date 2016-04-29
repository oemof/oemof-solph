# -*- coding: utf-8 -*-
"""
The module contains different objective expression terms.

@author: Simon Hilpert (simon.hilpert@fh-flensburg.de)
"""
import numpy as np
import logging
import pyomo.environ as po

def add_opex_var(model, block, ref='output', idx=0):
    """ Variable operation expenditure term for linear objective function.

    If reference of opex is `output`:

    .. math:: \\sum_e \\sum_t w_{e, o_{e,1}}(t) \\cdot C_{e, o_{e,1}}(t)

    If reference of opex is `input`:

    .. math:: \\sum_e \\sum_t w_{i_e,e}(t) \\cdot C_{i_e, e}(t)

    Parameters
    ----------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data.
    block : SimpleBlock()
         block to group all objects corresponding to one oemof base class
    ref : string
       Reference side on which opex are based on
        (e.g. powerplant MWhth -> input or MWhel -> output)
    idx : int
       Index to select output/input of list of inputs/ouputs if multiple i/o
       exist

    Returns
    -------
    Expression
    """
    if block.uids is None:
        block.uids = [obj.uid for obj in block.objs]

    opex_var = {obj.uid: obj.opex_var for obj in block.objs}
    # outputs for cost objs
    if ref == 'output':
        expr = sum(model.w[e, model.O[e][idx], t] * opex_var[e]
                   for e in block.uids
                   for t in model.timesteps)

    elif ref == 'input':
        expr = sum(model.w[model.I[e][idx], e, t] * opex_var[e]
                   for e in block.uids
                   for t in model.timesteps)
    return(expr)

def add_input_costs(model, block):
    """ Adds costs for usage of input (fuel, elec, etc. ) if not included in
    opex

    .. math:: \\sum_e \\sum_t w_{i_e, e}(t) \\cdot C_{i_e, e}(t)

    Parameters
    ----------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data.
    block : SimpleBlock()
         block to group all objects corresponding to one oemof base class

    Returns
    -------
    Expression
    """
    if block.uids is None:
        block.uids = [obj.uid for obj in block.objs]

    input_costs = {}
    for e in block.objs:
        if e.__dict__.get('input_costs', None) is not None:
            input_costs[e.uid] = e.input_costs
        else:
            input_costs[e.uid] = e.inputs[0].price
    # outputs for cost objs
    expr = sum(model.w[model.I[e][0], e, t] * input_costs[e]
               for e in block.uids for t in model.timesteps)

    return(expr)

def add_opex_fix(model, block, ref=None):
    """ Fixed operation expenditure term for linear objective function.

    Parameters
    ----------
    model : OptimizationModel() instance
    block : SimpleBlock()
         block to group all objects corresponding to one oemof base class
    ref : string
        string to check if capex is referred to capacity (storage) or output
        (e.g. powerplant)

    Returns
    -------
    Expression

    """
    if not block.objs:
        expr=0
        print('No objects defined for adding fixed opex to objective.' +
              'No action taken.')
        return(expr)
    else:
        if block.uids is None:
            block.uids = [obj.uid for obj in block.objs]
        uids_inv = set([obj.uid for obj in block.objs
                       if block.optimization_options.get('investment', False)])
        uids = set(block.uids) - uids_inv

        opex_fix = {obj.uid: obj.opex_fix for obj in block.objs}
        if ref == 'output':
            # installed electrical/thermal output: {'pp_chp': 30000,...}
            out_max = {obj.uid: obj.out_max for obj in block.objs}
            expr = 0
            expr += sum(out_max[e][0] * opex_fix[e] for e in uids)
            expr += sum((out_max[e][0] + block.add_out[e]) * opex_fix[e]
                        for e in uids_inv)
        elif ref == 'capacity':
            cap_max = {obj.uid: obj.cap_max for obj in block.objs}
            expr = 0
            expr += sum(cap_max[e] * opex_fix[e] for e in uids)
            expr += sum((cap_max[e] + block.add_cap[e]) * opex_fix[e]
                           for e in uids_inv)
        else:
            print('No reference defined. Please specificy in `add_opex()`!')
        return(expr)


def add_revenues(model, block, ref='output', idx=0):
    """ Revenue term for linear objective function.

    .. math:: \\sum_e \\sum_t w_{e, o_{e,1}}(t) \\cdot R_{e, o_{e,1}}(t)

    Parameters
    ----------
    model : OptimizationModel() instance
    block : SimpleBlock()
         block to group all objects corresponding to one oemof base class
    ref : string
       Reference side for revnues ('output' or 'input' Note: 'input' not
       defined)
    idx : integer
       Integer indicating which output from list to select
       if entity has multiple outputs

    Returns
    -------
    Expression
    """

    if block.uids is None:
        block.uids = [obj.uid for obj in block.objs]

    expr = 0
    if ref == 'output':
        #  if price is already a vector (array) this vector is taken
        output_price = {}
        for e in block.objs:
            if e.__dict__.get('output_price', None)[idx] is not None:
                if isinstance(e.output_price[idx], (float, int, np.integer,
                                               np.float)):
                    output_price[e.uid] = [e.output_price[idx]] * len(model.timesteps)
                else:
                    output_price[e.uid] = e.output_price[idx]
            elif isinstance(e.outputs[idx].price, (float, int, np.integer)):
                output_price[e.uid] = \
                    [e.outputs[idx].price] * len(model.timesteps)
            else:
                output_price[e.uid] = e.outputs[idx].price

        # create expression term
        expr += -sum(model.w[e, model.O[e][idx], t] * output_price[e][t]
                     for e in block.uids for t in model.timesteps)
    else:
        raise NotImplementedError("Referece side 'input' not implemented.")

    return(expr)

def add_curtailment_costs(model, block=None):
    """ Cost term for dispatchable sources in linear objective.

    .. math:: \\sum_e \\sum_ t w^{cut}_e(t) \\cdot C^{cut}_e


    Parameters
    ----------
    model : OptimizationModel() instance
    block : SimpleBlock()
         block to group all objects corresponding to one oemof base class

    Returns
    -------
    Expression
    """

    if not block.objs:
        expr = 0
        logging.warning('No objects for curtailment costs term in objective' +
        ' defined. No action taken.')
        return(expr)

    else:
        if block.uids is None:
            block.uids = [obj.uid for obj in block.objs]
        # get dispatch expenditure for renewable energies with dispatch
        c_curtail = {obj.uid: obj.curtail_costs for obj in block.objs}
        expr = sum(block.curtailment_var[e, t] * c_curtail[e]
                   for e in block.uids for t in model.timesteps)
    return(expr)

def add_capex(model, block, ref='output'):
    """ Add capital expenditure to linear objective.

    If reference is `output` (e.g. powerplants):


    If reference is `capacity` (e.g. storages):


    Parameters
    ----------
    model : OptimizationModel() instance
    block : SimpleBlock()
         block to group all objects corresponding to one oemof base class
    ref : string
        string to check if capex is referred to capacity (storage) or output
        (e.g. powerplant)

    Returns
    -------
    Expression
    """
    if not block.objs:
        expr = 0
        print('No objects for capex objective term defined. No action taken')
        return(expr)
    else:
        if block.uids is None:
            block.uids = [obj.uid for obj in block.objs]

        c_inv = {obj.uid: obj.capex for obj in block.objs}
        crf = {obj.uid: obj.crf for obj in block.objs}

        if ref == 'output':
            expr = sum(block.add_out[e] * crf[e] * c_inv[e]
                       for e in block.uids)
            return(expr)
        elif ref == 'capacity':
            expr = sum(block.add_cap[e] * crf[e] * c_inv[e]
                       for e in block.uids)
            return(expr)
        else:
            print('No reference defined. Please specificy in `add_capex()`')

def linearized_invest_costs(model, block, ref):
    """ This functionality add linearized costs with sos2-constraint.

    The capex attribute of objects in 'block.objs'- needs to be a list of tuples
    with interpolation points. Every first element is the absolut value of investment
    for the corresponding size of investment in the second element of the tuple.

    e.g.  capex = [(10, 20), (20, 15),..]


    Parameters
    ----------
    model : OptimizationModel() instance
    block : SimpleBlock()
         block to group all objects corresponding to one oemof base class
    ref : string
        string to check if capex is referred to capacity (storage) or output
        (e.g. powerplant)
    """
    if not block.objs:
        expr = 0
        print('No objects for capex objective term defined. No action taken')
        return(expr)

    else:

        invest_points = {obj.uid: [point[0] for point in obj.capex]
                         for obj in block.objs}
        size_points = {obj.uid:  [point[1] for point in obj.capex]
                       for obj in block.objs}
        if ref == 'output':
            variable = block.add_out
        elif ref == 'capacity':
            variable = block.add_cap

        def SOS_indices_init(block, e):
            return [ (e, i)  for i in range(len(invest_points[e]))]
        block.SOS_indices = po.Set(block.uids, dimen=2, ordered=True,
                                   initialize=SOS_indices_init)

        def ub_indices_init(block):
            return [(e, i) for e in block.uids
                           for i in range(len(invest_points[e]))]
        block.ub_indices = po.Set(ordered=True, dimen=2,
                                  initialize=ub_indices_init)

        block.interpolate = po.Var(block.ub_indices, within=po.NonNegativeReals,
                                   bounds=(0, 1))

        block.invest_costs = po.Var(block.uids, within=po.NonNegativeReals)
        ## storage costs (SOS2)
        def sos2_invest_rule(block, e):
            return (block.invest_costs[e] == sum(block.interpolate[e, i] *
                    invest_points[e][i]
                    for i in range(len(invest_points[e]))))
        block.linearized_invest_constr = po.Constraint(block.uids,
                                                    rule=sos2_invest_rule)

        # storage size (SOS2)
        def sos2_size_rule(model, e):
            return (variable[e] == sum(block.interpolate[e, i] *
                    size_points[e][i]
                    for i in range(len(size_points[e]))))
        block.add_cap_constraint = po.Constraint(block.uids,
                                                 rule=sos2_size_rule)
        # sos variable for storage
        def interpolate_rule(block, e):
            return (sum(block.interpolate[e, i]
                    for i in range(len(invest_points[e])))  - 1 == 0)
        block.interpolate_constraint = po.Constraint(block.uids,
                                                     rule=interpolate_rule)

        block.invest_sos_constraint = po.SOSConstraint(block.uids,
                                                       var=block.interpolate,
                                                       index=block.SOS_indices,
                                                       sos=2)

        expr = sum(block.invest_costs[e] for e in block.uids)

        return(expr)

def add_startup_costs(model, block):
    """ Adds startup costs for components to objective expression

    .. math:: \\sum_{e} \\sum_{t} z^{start}_e(t) \\cdot C^{start}_e

    Parameters
    ----------
    model : OptimizationModel() instance
    block : SimpleBlock()
         block to group all objects corresponding to one oemof base class

    Returns
    -------
    Expression
    """
    if block.objs is None:
        expr = 0
    else:
        if block.uids is None:
            block.uids = [obj.uid for obj in block.objs]

        c_start = {obj.uid: obj.start_costs for obj in block.objs}
        expr = sum(block.z_start[e, t] * c_start[e]
                   for e in block.uids for t in model.timesteps)
    return(expr)

def add_shutdown_costs(model, block):
    """ Adds shutdown costs for components to objective expression

    .. math:: \\sum_{e} \\sum_t z^{stop}_e(t) \\cdot C^{stop}_e

    Parameters
    ----------
    model : OptimizationModel() instance
    block : SimpleBlock()
         block to group all objects corresponding to one oemof base class

    Returns
    -------
    Expression
    """

    if block.uids is None:
        block.uids = [obj.uid for obj in block.objs]

    c_stop = {obj.uid: obj.stop_costs for obj in block.objs}
    expr = sum(block.z_stop[e, t] * c_stop[e]
               for e in block.uids for t in model.timesteps)
    return(expr)

def add_ramping_costs(model, block, grad_direc='positive'):
    """ Add gradient costs for components to linear objective expression.

    .. math::  \\sum_e \\sum_t g^{pos}_e(t) \\cdot C^{g,neg}_e

    .. math:: \\sum_e \\sum_t g^{neg}_e(t) \\cdot C^{g,pos}_e

    Parameters
    ----------
    model : OptimizationModel() instance
    block : SimpleBlock()
         block to group all objects corresponding to one oemof base class
    grad_direc : string
        direction of gradient for which the costs are added to the objective
        expression

    Returns
    -------
    Expression
    """
    if block.uids is None:
        block.uids = [obj.uid for obj in block. objs]

    c_ramp = {obj.uid: obj.ramp_costs.get(grad_direc, obj.ramp_costs)
              for obj in block.objs}
    if grad_direc == 'positive':
        expr = sum(block.grad_pos_var[e, t] * c_ramp[e]
                   for e in block.uids for t in model.timesteps)
    if grad_direc == 'negative' :
        expr = sum(block.grad_neg_var[e, t] * c_ramp[e]
                   for e in block.uids for t in model.timesteps)
    else:
        pass
    return(expr)

def add_excess_slack_costs(model, block=None):
    """ Artificial cost term for excess slack variables.

    .. math:: \\sum_e \\sum_t EXCESS_e(t) \\cdot C^{excess}_e


    Parameters
    ----------
    model : OptimizationModel() instance
    block : SimpleBlock()    block : SimpleBlock()
         block to group all objects corresponding to one oemof base class

    Returns
    -------
    Expression
    """
    c_excess = {e.uid:e.costs for e in block.objs}
    expr = sum(model.w[model.I[e][0], e,   t] * c_excess[e]
               for e in block.uids for t in model.timesteps)
    return(expr)


def add_shortage_slack_costs(model, block=None):
    """ Artificial cost term for shortage slack variables.

    .. math:: \\sum_e \\sum_t SHORTAGE_e(t) \\cdot C^{shortage}_e

    With :math:`e  \\in E` and :math:`E` beeing the set of unique ids for
    all entities grouped inside the attribute `block.objs`.

    Parameters
    ----------
    model : OptimizationModel() instance
    block : SimpleBlock()
         block to group all objects corresponding to one oemof base class

    Returns
    -------
    Expression
    """
    c_shortage = {e.uid: e.costs for e in block.objs}
    expr = sum(model.w[e, model.O[e][0], t] * c_shortage[e]
               for e in block.uids for t in model.timesteps)
    return(expr)


