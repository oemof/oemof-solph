# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 10:27:00 2015

@author: simon
"""

import pyomo.environ as po
try:
    from network.entities import components as cp
except:
    from .network.entities import components as cp


def generic_bus_constraint(model, objs=None, uids=None, timesteps=None):
    """ creates constraint for the input-ouput balance of bus objects

    .. math:: \\sum_{i \\in I[e]} w(i, e, t) \\geq \\sum_{o \\in O[e]} w(e, o, t), \
    \\qquad with: \\quad I = all inputs of bus `e`, O = all outputs of bus `e`

    Parameter
    -----------
    model : OptimizationModel() instance
    objs : objects for which the constraints are created (object type `bus`)
    uids : unique ids of bus object in `objs`
    timesteps : array_like (list)
        will be a list with timesteps representing the time-horizon
        of the optimization problem.
        (e.g. `timesteps` =  [t for t in range(168)])

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
    def bus_rule(model, e, t):
        expr = 0
        expr += sum(model.w[i, e, t] for i in I[e])
        rhs = sum(model.w[e, o, t] for o in O[e])
        if model.slack["excess"] is True:
            rhs += model.excess_slack[e, t]
        if model.slack["shortage"] is True:
            expr += model.shortage_slack[e, t]
        return(expr >= rhs)
    model.bus = po.Constraint(uids, timesteps, rule=bus_rule)


def generic_variables(model, edges, timesteps, var_name="w"):
    """ Creates all variables corresponding to the edges of the bi-partite
    graph for all timesteps.

    The function uses the pyomo class `Var()` to create the optimization
    variables. As index-sets the provided edges of the graph
    (in general all edges) and the defined timesteps are used.
    If an invest model is used an additional optimization variable indexed by
    the edges is created to handle "flexible" upper bounds of the edge variable
    by using an additional constraint.
    The following variables are created: Variables for all the edges, variables
    for dispatchable sources, variables for the state of charge of storages.
    (If specific components such as disptach sources and storages exist.)

    Parameters
    ------------
    model : OptimizationModel() instance
        A object to be solved containing all Variables, Constraints, Data
        Variables are added as attributes to the `model`
    edges : array_like (list)
        `edges` will be a list containing tuples representing the directed
        edges of the graph by using unique ids of components and buses.
        e.g. [('coal', 'pp_coal'), ('pp_coal', 'b_el'),...]
    timesteps : array_like (list)
        will be a list with timesteps representing the time-horizon
        of the optimization problem.
        (e.g. `timesteps` =  [t for t in range(168)])

    Returns
    --------
    The variables are added as a attribute to the optimization model object
    `model` of type OptimizationModel()


    """
    # variable for all edges
    model.w = po.Var(edges, timesteps, within=po.NonNegativeReals)

    # additional variable for investment models
    if model.invest is True:
        model.add_cap = po.Var(edges, within=po.NonNegativeReals)

    # dispatch variables for dispatchable sources
    objs = [e for e in model.entities
            if isinstance(e, cp.sources.DispatchSource)]
    # if disptachable sources exist, create pyomo variables
    if objs:
        uids = [e.uid for e in objs]
        model.dispatch = po.Var(uids, timesteps,
                                within=po.NonNegativeReals)

    # storage state of charge variables
    objs = [e for e in model.entities
            if isinstance(e, cp.transformers.Storage)]
    # if storages exist, create pyomo variables
    if objs:
        uids = [e.uid for e in objs]

        model.soc = po.Var(uids, timesteps, within=po.NonNegativeReals)

        # create additional variable for investment models
        if model.invest is True:
            model.soc_add = po.Var(uids, within=po.NonNegativeReals)


def generic_io_constraints(model, objs=None, uids=None, timesteps=None):
    """ Creates constraint for input-output relation as simple function


    The function uses the `pyomo.Constraint()` class to build the constraint
    with the following relation

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
    timesteps : array_like (list)
        will be a list with timesteps representing the time-horizon
        of the optimization problem.
        (e.g. `timesteps` =  [t for t in range(168)])

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
    #  - add possibility of multiple input busses (e.g. for syn + nat. gas)
    I = {obj.uid: obj.inputs[0].uid for obj in objs}
    # set with output uids for every simple transformer
    O = {obj.uid: [o.uid for o in obj.outputs[:]] for obj in objs}
    eta = {obj.uid: obj.eta for obj in objs}

    # constraint for simple transformers: input * efficiency = output
    def io_rule(model, e, t):
        expr = model.w[I[e], e, t] * eta[e][0] - model.w[e, O[e][0], t]
        return(expr == 0)
    setattr(model, "generic_io_"+objs[0].lower_name,
            po.Constraint(uids, timesteps, rule=io_rule,
                          doc="Input * Efficiency = Output"))


def generic_chp_constraint(model, objs=None, uids=None, timesteps=None):
    """ Creates constraint for input-output relation for a simple
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
    uids : array linke
        list of component uids corresponding to the objects

    timesteps : array_like (list)
        will be a list with timesteps representing the time-horizon
        of the optimization problem.
        (e.g. `timesteps` =  [t for t in range(168)])

    Returns
    -------
    The constraints are added as a
    attribute to the optimization model object `model` of type
    OptimizationModel()

    """
    #TODO:
    #  - add possibility of multiple output busses (e.g. for heat and power)
    # set with output uids for every simple chp
    # {'pp_chp': ['b_th', 'b_el']}
    O = {obj.uid: [o.uid for o in obj.outputs[:]] for obj in objs}
    # efficiencies for simple chps
    eta = {obj.uid: obj.eta for obj in objs}

    # additional constraint for power to heat ratio of simple chp comp:
    # P/eta_el = Q/eta_th
    def rule(model, e, t):
        expr = model.w[e, O[e][0], t] / eta[e][0]
        expr += -model.w[e, O[e][1], t] / eta[e][1]
        return(expr == 0)
    setattr(model, "generic_"+objs[0].lower_name,
            po.Constraint(uids, timesteps, rule=rule,
                          doc="P/eta_el - Q/eta_th = 0"))


def generic_w_ub(model, objs=None, uids=None, timesteps=None):
    """ Alters/sets upper bounds for variables that represent the
    weight of the edges of the graph.

    .. math:: w(e_1, e_2, t) \\leq ub_w(e_1, e_2), \\qquad \
    \\forall (e_1, e_2) \\in \\vec{E}, \\forall t \\in T
    .. math:: w(e_1, e_2, t) \\geq lb_w(e_1, e_2), \\qquad \
    \\forall (e_1, e_2) \\in \\vec{E}, \\forall t \\in T

    Parameters
    ------------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data
        Bounds are altered at model attributes (variables) of `model`
    objs : array like
        list of component objects for which the bounds will be
        altered
    uids : array like
        list of component uids corresponding to the objects
    timesteps : array_like (list)
        will be a list with timesteps representing the time-horizon
        of the optimization problem.
        (e.g. `timesteps` =  [t for t in range(168)])

    Returns
    -------
    The upper and lower bounds of the variables are
    altered at attributes (variables) of the optimization model object 
    `model` of type OptimizationModel()

    """
    if objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                         which bounds should be set.")
    if uids is None:
        uids = [e.uids for e in objs]

    # set variable bounds (out_max = in_max * efficiency):
    # m.in_max = {'pp_coal': 51794.8717948718, ... }
    # m.out_max = {'pp_coal': 20200, ... }
    in_max = {obj.uid: obj.in_max for obj in objs}
    out_max = {obj.uid: obj.out_max for obj in objs}

    # edges for simple transformers ([('coal', 'pp_coal'),...])
    ee = model.edges(objs)
    for (e1, e2) in ee:
        for t in timesteps:
            # transformer output <= model.out_max
            if e1 in uids:
                model.w[e1, e2, t].setub(out_max[e1][e2])
            # transformer input <= model.in_max
            if e2 in uids:
                model.w[e1, e2, t].setub(in_max[e2][e1])


def generic_w_ub_invest(model, objs=None, uids=None, timesteps=None):
    """ Sets upper bounds for variables that represent the weight
    of the edges of the graph if investment models are calculated.

    For investment  models upper and lower bounds will be modeled via
    additional constraints of type pyomo.Constraint(). The mathematical
    description for the constraint is as follows

    .. math::  w(e, O_1[e], t) \\leq out_{max}(e,O_1[e]) + \
    add\\_cap(e,O_1[e]), \\qquad \\forall e \\in uids, \\forall t \\in T

    Parameters
    ------------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data
        Constraints are added as attributes to the `model`
    objs : array like
        list of component objects for which the bounds will be
        altered
    uids : array linke
        list of component uids corresponding to the objects
    timesteps : array_like (list)
        will be a list with timesteps representing the time-horizon
        of the optimization problem.
        (e.g. `timesteps` =  [t for t in range(168)])
    
    Returns
    -------
    The constraints are added as attributes
    to the optimization model object `model` of type OptimizationModel()
    """
    O = {obj.uid: [o.uid for o in obj.outputs[:]] for obj in objs}
    out_max = {obj.uid: obj.out_max for obj in objs}

    # constraint for additional capacity
    def rule(model, e, t):
        expr = 0
        expr += model.w[e, O[e][0], t]
        rhs = out_max[e][O[e][0]] + model.add_cap[e, O[e][0]]
        return(expr <= rhs)
    setattr(model, "generic_w_ub_" + objs[0].lower_name,
            po.Constraint(uids, timesteps, rule=rule))

def generic_soc_bounds(model, objs=None, uids=None, timesteps=None):
    """ Alters/sets upper and lower bounds for variables that represent the
    state of charge e.g. filling level of a storage component.

    Parameters
    ------------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data
        Bounds are altered at model attributes (variables) of `model`
    objs : array like
        list of component objects for which the bounds will be
        altered
    uids : array linke
        list of component uids corresponding to the objects
    timesteps : array_like (list)
        will be a list with timesteps representing the time-horizon
        of the optimization problem.
        (e.g. `timesteps` =  [t for t in range(168)])

    Returns
    -------
    The upper and lower bounds of the variables are
    altered in the optimization model object `model` of type
    OptimizationModel()

    """
    if objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                         which bounds should be set.")
    if uids is None:
        uids = [e.uids for e in objs]

    # extract values for storages m.soc_max = {'storge': 120.5, ... }
    soc_max = {obj.uid: obj.soc_max for obj in objs}
    soc_min = {obj.uid: obj.soc_min for obj in objs}

    # loop over all uids (storages) and timesteps to set the upper bound
    for e in uids:
        for t in timesteps:
            model.soc[e, t].setub(soc_max[e])
            model.soc[e, t].setlb(soc_min[e])

def generic_soc_ub_invest(model, objs=None, uids=None, timesteps=None):
    """ Sets upper and lower bounds for variables that represent the state
    of charge of storages if investment models are calculated.

    For investment  models upper and lower bounds will be modeled via
    additional constraints of type pyomo.Constraint(). The mathematical
    description for the constraint is as follows:

    .. math:: soc(e, t) \\leq soc_{max}(e) + soc\\_add(e), \
    \\qquad \\forall e \\in uids, \\forall t \\in T

    Parameters
    ------------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data
       Constraints are added as attribtes to the `model`
    objs : array like
        list of component objects for which the bounds will be
        altered e.g. constraints will be created
    uids : array linke
        list of component uids corresponding to the objects
    timesteps : array_like (list)
        will be a list with timesteps representing the time-horizon
        of the optimization problem.
        (e.g. `timesteps` =  [t for t in range(168)])

    Returns
    -------
    The constraints are added as attributes
    to the optimization model object `model` of type OptimizationModel()
    """
    # constraint for additional capacity in investment models
    def rule(model, e, t):
        return(model.soc[e, t] <= model.soc_max[e] + model.soc_add[e])
    setattr(model, "generic_soc_ub_invest_"+objs[0].lower_name,
            po.Constraint(uids, timesteps, rule=rule))



def generic_limit(model, objs=None, uids=None, timesteps=None):
    """ Creates constraint to set limit for variables as sum over the total
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
    uids : array linke
        list of component uids corresponding to the objects
    timesteps : array_like (list)
        will be a list with timesteps representing the time-horizon
        of the optimization problem.
        (e.g. `timesteps` =  [t for t in range(168)])

    Returns
    -------
    The constraints are added as attributes
    to the optimization model object `model` of type OptimizationModel()
    """

    limit = {obj.uid: obj.sum_out_limit for obj in objs}

    # outputs: {'rcoal': ['coal'], 'rgas': ['gas'],...}
    O = {obj.uid: [o.uid for o in obj.outputs[:]] for obj in objs}

    # set upper bounds: sum(yearly commodity output) <= yearly_limit
    def limit_rule(model, e):
        expr = sum(model.w[e, o, t] for t in timesteps for o in O[e]) -\
            limit[e]
        # if bus is defined but has not outputs Constraint is skipped
        # (should be logged as well)
        if isinstance(expr, (int, float)):
            return(po.Constraint.Skip)
        else:
            return(expr <= 0)
    setattr(model, "generic_limit_"+objs[0].lower_name,
            po.Constraint(uids, rule=limit_rule))


def generic_fixed_source(model, objs, uids, timesteps):
    """ Creates fixed source from standard edges variables by setting the value
    of variables and fixing variables to that value


    Parameters
    ------------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data
        Attributes are altered of the `model`
    objs : array like
        list of component objects for which the variables representing the
        output edges values will be set to a certain value and then fixed.
    uids : array like
        list of component uids corresponding to the objects
    timesteps : array_like (list)
        will be a list with timesteps representing the time-horizon
        of the optimization problem.
        (e.g. `timesteps` =  [t for t in range(168)])

    Returns
    -------
    The variables as attributes of
    the optimization model object `model` of type OptimizationModel() will
    be altered.
    """
    # normed value of renewable source (0 <= value <=1)
    val = {obj.uid: obj.val for obj in objs}
    # maximal ouput of renewable source (in general installed capacity)
    out_max = {obj.uid: obj.out_max for obj in objs}
    # edges for renewables ([('wind_on', 'b_el'), ...)
    ee = model.edges(objs)
    # fixed values for every timestep
    for (e1, e2) in ee:
        for t in timesteps:
            # set value of variable
            model.w[e1, e2, t] = val[e1][t] * out_max[e1][e2]
            # fix variable value ("set variable to parameter" )
            model.w[e1, e2, t].fix()


def generic_fixed_sink(model, objs, uids, timesteps):
    """ Creates fixed sink from standard edges / variables by setting the value
    of variables and fixing variables to that value.


    Parameters
    ------------

    model :OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data
       Attributes are altered of the `model`
    objs : array like
        list of component objects for which the variables representing the
        input edges values will be set to a certain value and then fixed.
    uids : array like
        list of component uids corresponding to the objects
    timesteps : array_like (list)
        will be a list with timesteps representing the time-horizon
        of the optimization problem.
        (e.g. `timesteps` =  [t for t in range(168)])

    Returns
    -------

    The variables as attributes to
    the optimization model object `model` of type OptimizationModel() will
    be altered.
    """

    val = {obj.uid: obj.val for obj in objs}
    ee = model.edges(objs)
    for (e1, e2) in ee:
        for t in timesteps:
            # set variable value
            model.w[(e1, e2), t] = val[e2][t]
            # fix variable value for optimization problem
            model.w[(e1, e2), t].fix()


def generic_fixed_source_invest(model, objs, uids, timesteps, val=None,
                                out_max=None):
    """ Creates fixed source with investment models by adding constraints

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

    timesteps : array_like (list)
        will be a list with timesteps representing the time-horizon
        of the optimization problem.
        (e.g. `timesteps` =  [t for t in range(168)])

    Returns
    -------
    There is no return value. The constraints will be added as attributes to
    the optimization model object `model` of typeOptimizationModel().
    """
    # outputs: {'pv': 'b_el', 'wind_off': 'b_el', ... }
    O = {obj.uid: obj.outputs[0].uid for obj in objs}
    # normed value of renewable source (0 <= value <=1)
    if val is None:
        val = {obj.uid: obj.val for obj in objs}
    # maximal ouput of renewable source (in general installed capacity)
    if out_max is None:
        out_max = {obj.uid: obj.out_max for obj in objs}

    def invest_rule(model, e, t):
        expr = model.w[e, O[e], t]
        rhs = (out_max[e] + model.add_cap[e, O[e]]) * val[e][t]
        return(expr <= rhs)
    setattr(model, "generic_invest_"+objs[0].lower_name,
            po.Constraint(uids, timesteps, rule=invest_rule))


def generic_dispatch_source(model, objs=None, uids=None, timesteps=None):
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
    timesteps : array_like (list)
        will be a list with timesteps representing the time-horizon
        of the optimization problem.
        (e.g. `timesteps` =  [t for t in range(168)])

    Returns
    -------
    There is no return value. The constraints will be added as attributes of
    the optimization model object `model` of type OptimizationModel().
    """
    # outputs: {'pv': 'b_el', 'wind_off': 'b_el', ... }
    O = {obj.uid: obj.outputs[0].uid for obj in objs}
    # normed value of renewable source (0 <= value <=1)
    val = {obj.uid: obj.val for obj in objs}
    # maximal ouput of renewable source (in general installed capacity)
    out_max = {obj.uid: obj.out_max for obj in objs}
    # create dispatch variables

    ee = model.edges(objs)
    # fixed values for every timestep
    for (e1, e2) in ee:
        for t in timesteps:
            # set upper bound of variable
            model.w[e1, e2, t].setub(val[e1][t] * out_max[e1][e2])

    def dispatch_rule(model, e, t):
        expr = model.dispatch[e, t]
        expr += - val[e][t] * out_max[e][O[e]] + model.w[e, O[e], t]
        return(expr, 0)
    setattr(model, "generic_constr_"+objs[0].lower_name,
            po.Constraint(uids, timesteps, rule=dispatch_rule))
