# -*- coding: utf-8 -*-
"""
The linear_contraints module contains the coded pyomo constraint that
are used by the '*_assembler' methods of OptimizationModel()-class

The module frequently uses the dictionaries I and O for the construction of
constraints. I,E contain all uids of components as the keys of the dict and
the input/output uids as items of the dict corresponding to the key.

In mathematical notation I,O can be seen as indexed index sets The
elements of the sets are the uids of all components (index: `e`). The the
inputs/outputs uids are the elements of the accessed set by the
component index `e`.
Generally the index `e` is the index for the uids-sets containing the uids
of objects for which the constraints are build.

Simon Hilpert (simon.hilpert@fh-flensburg.de)
"""

import pyomo.environ as po

def add_bus_balance(model, objs=None, uids=None, balance_type="=="):
    """ Adds constraint for the input-ouput balance of bus objects

    .. math:: \\sum_{i \\in I(e)} W(i, e, t) = \\sum_{o \\in O(e)} \
    W(e, o, t), \\qquad \\forall t

    Parameters
    -----------
    model : OptimizationModel() instance
    objs : bus objects for which the constraints are created
    uids : unique ids of bus object in `objs` (math. index 'e')
    balance_type : type of constraint ("==" or ">=" )

    Returns
    ----------
    The constraints are added to as a attribute to the optimization model
    object `model` of type OptimizationModel()
    """
    if balance_type == ">=":
        upper = float('+inf')
    if balance_type == "==":
        upper = 0;

    I = {b.uid: [i.uid for i in b.inputs] for b in objs}
    O = {b.uid: [o.uid for o in b.outputs] for b in objs}

    # component inputs/outputs are negative/positive in the bus balance
    def bus_balance_rule(model, e, t):
        lhs = 0
        lhs += sum(model.w[i, e, t] for i in I[e])
        rhs = sum(model.w[e, o, t] for o in O[e])
        if e in model.uids["excess"]:
            rhs += model.excess_slack[e, t]
        if e in model.uids["shortage"]:
            lhs += model.shortage_slack[e, t]
        return(0, lhs - rhs, upper)
    setattr(model, objs[0].lower_name+"_balance",
            po.Constraint(uids, model.timesteps, rule=bus_balance_rule))


def add_simple_io_relation(model, objs=None, uids=None):
    """ Adds constraint for input-output relation as simple function
    The function uses the `pyomo.Constraint()` class to build the constraint
    with the following relation.

    .. math:: W(I(e), e, t) \cdot \\eta(e) = W(e, O(e), t), \
    \\qquad \\forall e, \\forall t

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
    with the following relation:

    .. math:: \\frac{W_1(e,O_1(e),t)}{\\eta_1(e,t)} = \
    \\frac{W_2(e,O_2(e), t)}{\\eta_2(e,t)}, \
    \\qquad \\forall e, \\forall t

    The constraint is indexed with all unique ids 'e' of objects and
    timesteps 't'.

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

def add_simple_extraction_chp_relation(model, objs=None, uids=None):
    """ Adds constraint for power to heat relation and equivalent output
    for a simple extraction combined heat an power units. The constraints
    represent the PQ-region of the extraction unit.

    The function uses the `pyomo.Constraint()` class to build the constraint
    with the following relation:

    Power/Heat ratio:

    .. math:: W(e,O_1(e),t) = W(e, O_2(e), t) \\cdot \\sigma(e), \
    \\qquad \\forall e, \\forall t

    .. math:: \\sigma = \\text{Power to heat ratio}

    Equivalent power:

    .. math:: W(I(e),e,t) = \\frac{(W(e,O_1(e),t) + \\beta(e) \\cdot \
    W(e, O_2(e), t))}{\\eta_1(e)}

    .. math:: \\beta = \\text{Power loss index}

    The constraint is indexed with all unique ids 'e' of objects and
    timesteps 't'.

    Parameters
    ------------
    model : OptimizationModel() instance
    objs : array like
    uids : array like
    """

    if uids is None:
        uids = [e.uid for e in objs]

    out_max = {}
    beta = {}
    sigma = {}
    eta = {}
    for e in objs:
        out_max[e.uid] = e.out_max
        beta[e.uid] = e.beta
        sigma[e.uid] = e.sigma
        eta[e.uid] = e.eta

    def equivalent_output_rule(model, e, t):
        lhs = model.w[model.I[e], e, t]
        rhs = (model.w[e, model.O[e][0], t] +
              beta[e] * model.w[e, model.O[e][1], t]) / eta[e][0]
        return(lhs == rhs)
    setattr(model, objs[0].lower_name+'_equivalent_output',
            po.Constraint(uids, model.timesteps, rule=equivalent_output_rule))

    def power_heat_rule(model, e, t):
        lhs = model.w[e, model.O[e][1], t]
        rhs = model.w[e, model.O[e][0], t] / sigma[e]
        return(lhs <= rhs)
    setattr(model, objs[0].lower_name+ '_pth',
            po.Constraint(uids, model.timesteps, rule=power_heat_rule))

def add_bus_output_limit(model, objs=None, uids=None):
    """ Adds constraint to set limit for variables as sum over the total
    timehorizon

    .. math:: \sum_{t} \sum_{o \\in O(e)} W(e, o, t) \
    \\leq sumlimit_{out}(e), \\qquad \\forall e

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
        if isinstance(lhs, (int, float)) or limit[e] == float('inf'):
            return(po.Constraint.Skip)
        else:
            return(lhs <= 0)
    setattr(model,objs[0].lower_name+"_limit",
            po.Constraint(uids, rule=output_limit_rule))

def add_fixed_source(model, objs, uids,):
    """ Add fixed source

     .. math::  W(e,O(e),t) = val_{norm}(e,t) \\cdot out_{max}(e), \
     \\qquad \\forall e, \\forall t

    If investment for component:
    .. math::  W(e, O(e), t) \\leq (out_{max}(e) + ADDOUT(e) \
    \cdot val_{norm}(e,t), \\qquad \\forall e, \\forall t

    .. math:: ADDOUT(e)  \\leq addout_{max}(e), \\qquad \\forall e


    Parameters
    ------------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data
        Constraints are added as attributes to the `model`
    objs : array like
        list of component objects for which the constraints will be created.
    uids : array like
        list of component uids corresponding to the objects.

    Returns
    -------
    The constraints will be added as attributes to
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

    if objs[0].model_param['investment'] ==  False:
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

def add_dispatch_source(model, objs=None, uids=None):
    """ Creates dispatchable source models by setting bounds and
       adding constraints

    First the maximum value for the output of the source will be set. Then a
    constraint is defined that determines the dispatch of the source. This
    dispatch can be used in the objective function to add cost for dispatch
    of sources.

    The mathemathical fomulation for the constraint is as follows:

    .. math:: CURTAIL(e,t) = val_{norm}(e,t) \\cdot out_{max}(e) - \
    W(e,O(e),t),  \\qquad \\forall e, \\forall t

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
    if uids is None:
        uids = [e.uid for e in objs]

    # create dispatch var
    model.curtailment_var = po.Var(uids, model.timesteps,
                                   within=po.NonNegativeReals)

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

    def curtailment_source_rule(model, e, t):
        lhs = model.curtailment_var[e, t]
        rhs = val[e][t] * out_max[e][model.O[e][0]] - \
           model.w[e, model.O[e][0], t]
        return(lhs == rhs)
    setattr(model, objs[0].lower_name+"_calc",
            po.Constraint(uids, model.timesteps, rule=curtailment_source_rule))

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
            expr += + model.w[model.I[e], e, t] * eta_in[e]
            expr += - model.w[e, model.O[e][0], t] / eta_out[e]
        else:
            expr += model.cap[e, t]
            expr += - model.cap[e, t-1] * (1 - cap_loss[e])
            expr += + model.w[model.I[e], e, t] * eta_in[e]
            expr += - model.w[e, model.O[e][0], t] / eta_out[e]
        return(expr, 0)
    setattr(model, objs[0].lower_name+"_balance",
            po.Constraint(uids, model.timesteps, rule=storage_balance_rule))


def add_output_gradient_calc(model, objs=None, uids=None, grad_direc='both'):
    """ Add constraint to calculate the gradient between two timesteps
    (positive and negative)

    Positive gradient:

    .. math::  W(e,O(e),t) - W(e,O(e),t-1) \\leq GRADPOS(e,t)\
    \\qquad \\forall e, \\forall t / t=1

    .. math:: GRADPOS(e,t) \\leq gradpos_{max}(e), \\qquad \\forall e, \\forall t

    Negative gradient:

        .. math::  W(e,O(e),t-1) - W(e,O(e),t) \\leq GRADNEG(e,t)\
    \\qquad \\forall e, \\forall t / t=1

    .. math:: GRADNEG(e,t) \\leq gradneg_{max}(e), \\qquad \\forall e, \\forall t

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
    grad_direc: string
        string defining the direction of the gradient constraint.
        ('positive', negative', 'both')

    Returns
    -------
    The constraints will be added as attributes of
    the optimization model object `model` of class OptimizationModel().
    """

    def grad_pos_calc_rule(model, e, t):
        if t > 0:
            lhs = model.w[e, model.O[e][0], t] - model.w[e,model.O[e][0], t-1]
            rhs = var_pos[e, t]
            return(lhs <= rhs)
        else:
            return(po.Constraint.Skip)

    def grad_neg_calc_rule(model, e, t):
        if t > 0:
            lhs = model.w[e, model.O[e][0], t-1] - model.w[e,model.O[e][0], t]
            rhs = var_neg[e, t]
            return(lhs <= rhs)
        else:
            return(po.Constraint.Skip)

    def grad_pos_bound_rule(model, e, t):
        return((0, grad_pos[e]))

    def grad_neg_bound_rule(model, e, t):
        return((0, grad_neg[e]))

    # negative gradient
    if grad_direc == 'positive' or grad_direc == "both":
        # create variable
        grad_pos = {obj.uid: obj.grad_pos for obj in objs}
        setattr(model, objs[0].lower_name+'_grad_pos_var',
                po.Var(uids, model.timesteps, within=po.NonNegativeReals,
                       bounds=grad_pos_bound_rule))

        var_pos = getattr(model,  objs[0].lower_name+'_grad_pos_var')
        # set constraint
        setattr(model, objs[0].lower_name+"_grad_pos_calc",
                po.Constraint(uids, model.timesteps, rule=grad_pos_calc_rule))

    # positive gradient
    if grad_direc == 'negative' or grad_direc == "both":
        # create variable
        grad_neg = {obj.uid: obj.grad_neg for obj in objs}
        setattr(model,  objs[0].lower_name+'_grad_neg_var',
                po.Var(uids, model.timesteps, within=po.NonNegativeReals,
                       bounds=grad_neg_bound_rule))
        var_neg = getattr(model,  objs[0].lower_name+'_grad_neg_var')
        # set constraint
        setattr(model, objs[0].lower_name+"_grad_neg_calc",
                po.Constraint(uids, model.timesteps, rule=grad_neg_calc_rule))
