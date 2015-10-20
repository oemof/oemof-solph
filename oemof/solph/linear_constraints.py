# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 10:27:00 2015

@author: simon
"""

import pyomo.environ as po
try:
    from oemof.core.network.entities import components as cp
except:
    from .network.entities import components as cp


def add_bus_balance(model, objs=None, uids=None):
    """ Adds constraint for the input-ouput balance of bus objects

    .. math:: \\sum_{i \\in I[e]} w(i, e, t) \\geq \\sum_{o \\in O[e]} w(e, o, t), \\\ \
    \\qquad \\text{with:}
    .. math:: I = \\text{all inputs of bus } e
    .. math:: O = \\text{all outputs of bus } e

    Parameters
    -----------
    model : OptimizationModel() instance
    objs : objects for which the constraints are created (object type `bus`)
    uids : unique ids of bus object in `objs`


    Returns
    ----------
    The constraints are added as a
    attribute to the optimization model object `model` of type
    OptimizationModel()
    """

    I = {b.uid: [i.uid for i in b.inputs] for b in objs}
    O = {b.uid: [o.uid for o in b.outputs] for b in objs}

    # constraint for bus balance:
    # component inputs/outputs are negative/positive in the bus balance
    def bus_balance_rule(model, e, t):
        lhs = 0
        lhs += sum(model.w[i, e, t] for i in I[e])
        rhs = sum(model.w[e, o, t] for o in O[e])
        if model.slack["excess"] is True:
            rhs += model.excess_slack[e, t]
        if model.slack["shortage"] is True:
            lhs += model.shortage_slack[e, t]
        return(lhs >= rhs)
    setattr(model, objs[0].lower_name+"_balance",
            po.Constraint(uids, model.timesteps, rule=bus_balance_rule))


def add_simple_io_relation(model, objs=None, uids=None):
    """ Adds constraint for input-output relation as simple function
    The function uses the `pyomo.Constraint()` class to build the constraint
    with the following relation.

    .. math:: w(I[e], e, t) \cdot \\eta[e] = w(e, O[e], t), \
    \\qquad \\forall e \\in uids, \\forall t \\in T

    The constraint is indexed with all unique ids of objects and timesteps.

    Parameters
    ------------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data
        Constraints are added as attributes to the `model`
    objs : array like
        list of component objects for which the constraint will be
        build
    uids : array like
        list of component uids corresponding to the objects

    Returns
    -------
    The constraints are added as a
    attribute to the optimization model object `model` of type
    OptimizationModel()

    """
    if objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                         which the constraints should be build")
    if uids is None:
        uids = [e.uids for e in objs]

    #TODO:
    eta = {obj.uid: obj.eta for obj in objs}

    # constraint for simple transformers: input * efficiency = output
    def io_rule(model, e, t):
        lhs = model.w[model.I[e], e, t] * eta[e][0] - \
            model.w[e, model.O[e][0], t]
        return(lhs == 0)
    setattr(model, objs[0].lower_name+"_io_relation",
            po.Constraint(uids, model.timesteps, rule=io_rule,
                          doc="Input * Efficiency = Output"))

def add_simple_chp_relation(model, objs=None, uids=None):
    """ Adds constraint for input-output relation for a simple
    representation of combined heat an power units.

    The function uses the `pyomo.Constraint()` class to build the constraint
    with the following relation

    .. math:: \\frac{w_1(e,O_1[e],t)}{eta_1(e,t)} = \
    \\frac{w_2(e,O_2[e], t)}{eta_2(e,t)} \
    \\forall e \\in uids \\forall t \\in T

    The constraint is indexed with all unique ids of objects and timesteps.

    Parameters
    ------------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data
        Constraints are added as attributes to the `model`
    objs : array like
        list of component objects for which the constraint will be
        build
    uids : array like
        list of component uids corresponding to the objects

    Returns
    -------
    The constraints are added as a
    attribute to the optimization model object `model` of type
    OptimizationModel()

    """
    #TODO:
    #  - add possibility of multiple output busses (e.g. for heat and power)
    # efficiencies for simple chps
    eta = {obj.uid: obj.eta for obj in objs}

    # additional constraint for power to heat ratio of simple chp comp:
    # P/eta_el = Q/eta_th
    def simple_chp_rule(model, e, t):
        lhs = model.w[e, model.O[e][0], t] / eta[e][0]
        lhs += -model.w[e, model.O[e][1], t] / eta[e][1]
        return(lhs == 0)
    setattr(model, objs[0].lower_name+"_gc",
            po.Constraint(uids, model.timesteps, rule=simple_chp_rule,
                          doc="P/eta_el - Q/eta_th = 0"))

def add_bus_output_limit(model, objs=None, uids=None):
    """ Adds constraint to set limit for variables as sum over the total
    timehorizon

    .. math:: \sum_{t \\in T} \sum_{o \\in O[e]} w(e, o, t) \\leq limit[e], \
    \\qquad \\forall e \\in uids

    Parameters
    ------------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data
       Constraints are added as attribtes to the `model`
    objs : array like
        list of component objects for which the constraints will be created
    uids : array like
        list of component uids corresponding to the objects

    Returns
    -------
    The constraints are added as attributes
    to the optimization model object `model` of type OptimizationModel()
    """

    limit = {obj.uid: obj.sum_out_limit for obj in objs}

    # outputs: {'rcoal': ['coal'], 'rgas': ['gas'],...}
    O = {obj.uid: [o.uid for o in obj.outputs[:]] for obj in objs}

    # set upper bounds: sum(yearly commodity output) <= yearly_limit
    def output_limit_rule(model, e):
        lhs = sum(model.w[e, o, t] for t in model.timesteps for o in O[e]) -\
            limit[e]
        # if bus is defined but has not outputs Constraint is skipped
        # (should be logged as well)
        if isinstance(lhs, (int, float)):
            return(po.Constraint.Skip())
        else:
            return(lhs <= 0)
    setattr(model,objs[0].lower_name+"_limit_gc",
            po.Constraint(uids, rule=output_limit_rule))

def add_fixed_source(model, objs, uids, val=None, out_max=None):
    """ Adds fixed source with investment models by adding constraints

    The mathemathical fomulation for the constraint is as follows:

    *Definition:*
    .. math:: O : \\text{Array with indices for all outputs of objs (index set)}
    .. math::  w(e, O[e], t) \\leq (out_{max}(e) + add\\_cap(e, O[e]) ) \
    \cdot val[e], \\qquad \\forall e \\in uids, \\forall t \\in T

    Parameters
    ------------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data
        Constraints are added as attributes to the `model`
    objs : array like
        list of component objects for which the constraints will be created.
    uids : array like
        list of component uids corresponding to the objects.
    val : dict()
        dict with objs uids as keys and normed values of source (0<=val<=1)
        as items
    out_max : dict

    Returns
    -------
    There is no return value. The constraints will be added as attributes to
    the optimization model object `model` of typeOptimizationModel().
    """
    # normed value of renewable source (0 <= value <=1)
    val = {}
    out_max = {}
    for e in objs:
         out_max[e.uid] = e.out_max
         val[e.uid] = e.val

    # normed value of renewable source (0 <= value <=1)
    val = {obj.uid: obj.val for obj in objs}
    if model.invest is False:

        # maximal ouput of renewable source (in general installed capacity)
        out_max = {obj.uid: obj.out_max for obj in objs}
        # edges for renewables ([('wind_on', 'b_el'), ...)
        ee = model.edges(objs)
        # fixed values for every timestep
        for (e1, e2) in ee:
            for t in model.timesteps:
                # set value of variable
                model.w[e1, e2, t] = val[e1][t] * out_max[e1][e2]
                # fix variable value ("set variable to parameter" )
                model.w[e1, e2, t].fix()
    else:
        # set maximum of additional output
        add_out_limit = {obj.uid: obj.add_out_limit for obj in objs}
        # loop over all uids (storages) set the upper bound
        for e in uids:
            model.add_out[e].setub(add_out_limit[e])

        def invest_rule(model, e, t):
            lhs = model.w[e, model.O[e][0], t]
            rhs = (out_max[e][model.O[e][0]] + model.add_out[e]) * val[e][t]
            return(lhs == rhs)
        setattr(model, objs[0].lower_name+"_invest",
                po.Constraint(uids, model.timesteps, rule=invest_rule))

def add_dispatch_source(model, objs=None, uids=None, val=None, out_max=None):
    """ Creates dispatchable source models by setting bounds and
       adding constraints

    First the maximum value for the output of the source will be set. Then a
    constraint is defined that determines the dispatch of the source. This
    dispatch can be used in the objective function to add cost for dispatch
    of sources.

    The mathemathical fomulation for the constraint is as follows:
    # TODO: write mathematical eq.

    .. math:: MISSING!

    Parameters
    ------------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data
        Constraints are added as attributes to the `model` and bounds are
        altered for attributes of `model`
    objs : array like
        list of component objects for which the constraints will be created.
    uids : array like
        list of component uids corresponding to the objects.

    Returns
    -------
    The constraints will be added as attributes of
    the optimization model object `model` of class OptimizationModel().
    """

    # normed value of renewable source (0 <= value <=1)
    val = {}
    out_max = {}
    for e in objs:
         out_max[e.uid] = e.out_max
         val[e.uid] = e.val

    ee = model.edges(objs)
    # fixed values for every timestep
    for (e1, e2) in ee:
        for t in model.timesteps:
            # set upper bound of variable
            model.w[e1, e2, t].setub(val[e1][t] * out_max[e1][e2])

    def dispatch_rule(model, e, t):
        lhs = model.dispatch[e, t]
        rhs = val[e][t] * out_max[e][model.O[e][0]] - \
           model.w[e, model.O[e][0], t]
        return(lhs == rhs)
    setattr(model, objs[0].lower_name+"_calc",
            po.Constraint(uids, model.timesteps, rule=dispatch_rule))

def add_storage_balance(model, objs=None, uids=None):
    """ Creates constraint for storage balance

    Parameters
    -------------


    Returns
    ----------

    """
    # constraint for storage energy balance
    cap_initial = {}
    cap_loss = {}
    eta_in = {}
    eta_out = {}

    for e in objs:
        cap_initial[e.uid] = e.cap_initial
        cap_loss[e.uid] = e.cap_loss
        eta_in[e.uid] = e.eta_in
        eta_out[e.uid] = e.eta_out

    # set cap of last timesteps to fixed value of cap_initial
    t_last = len(model.timesteps)-1
    for e in uids:
      model.cap[e, t_last] = cap_initial[e]
      model.cap[e, t_last].fix()

    def storage_balance_rule(model, e, t):
        # TODO:
        #   - include time increment
        expr = 0
        if(t == 0):
            expr += model.cap[e, t] - cap_initial[e]
            expr += - model.w[model.I[e], e, t] * eta_in[e]
            expr += + model.w[e, model.O[e][0], t] / eta_out[e]
        else:
            expr += model.cap[e, t]
            expr += - model.cap[e, t-1] * (1 - cap_loss[e])
            expr += - model.w[model.I[e], e, t] * eta_in[e]
            expr += + model.w[e, model.O[e][0], t] / eta_out[e]
        return(expr, 0)
    setattr(model, objs[0].lower_name+"_balance",
            po.Constraint(uids, model.timesteps, rule=storage_balance_rule))