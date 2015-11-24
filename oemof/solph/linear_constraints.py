# -*- coding: utf-8 -*-
"""
The linear_contraints module contains the pyomo constraints wrapped in
functions. These functions are used by the '_assembler- methods
of the OptimizationModel()-class.

The module frequently uses the dictionaries I and O for the construction of
constraints. I and O contain all components' uids as dictionary keys and the
relevant input input/output uids as dictionary items.

*Illustrative Example*:

    Consider the following example of a chp-powerplant modeled with 4 entities
    (3 busses, 1 component) and their unique ids being stored in a list
    called `uids`:

    >>> uids = ['bus_el', 'bus_th', 'bus_coal','pp_coal']
    >>> I = {'pp_coal': 'bus_coal'}
    >>> O = {'pp_coal': ['bus_el', 'bus_th']}
    >>> print(I['pp_coal'])
    'bus_el'


In mathematical notation I, O can be seen as indexed index sets The
elements of the sets are the uids of all components (index: `e`). The the
inputs/outputs uids are the elements of the accessed set by the
component index `e`. Generally the index `e` is the index for the uids-sets
containing the uids of objects for which the constraints are build.
For all mathematical constraints the following definitions hold:

    Inputs:
    :math:`I(e) = \\text{Input-uids of entity } e`

    Outputs:
    :math:`O(e) = \\text{Output-uids of entity } e`

    Entities:
    :math:`e \\in E = \\{uids\\},`

    Timesteps:
    :math:`t \\in T = \\{timesteps\\}`


Simon Hilpert (simon.hilpert@fh-flensburg.de)
"""

import pyomo.environ as po

def add_bus_balance(model, block=None, balance_type='=='):
    """ Adds constraint for the input-ouput balance of bus objects

    .. math:: \\sum_{i \\in I(e)} W(i, e, t) = \\sum_{o \\in O(e)} \
    W(e, o, t), \\qquad \\forall t

    Parameters
    -----------
    model : OptimizationModel() instance
    block : SimpleBlock()
    balance_type : type of constraint ("==" or ">=" )

    Returns
    ----------
    The constraints are added as an attribute to the optimization model
    object `model` of type OptimizationModel()
    """
    if not block.objs or block.objs is None:
        raise ValueError('Failed to create busbalance. No busobjects defined!')

    if balance_type == '>=':
        upper = float('+inf')
    if balance_type == '==':
        upper = 0;

    uids = []
    I = {}
    O = {}
    for b in block.objs:
        if b.balanced == True:
            uids.append(b.uid)
            I[b.uid] = [i.uid for i in b.inputs]
            O[b.uid] = [o.uid for o in b.outputs]

    # component inputs/outputs are negative/positive in the bus balance
    def bus_balance_rule(block, e, t):
        lhs = 0
        lhs += sum(model.w[i, e, t] for i in I[e])
        rhs = sum(model.w[e, o, t] for o in O[e])
        if e in block.excess_uids:
            rhs += block.excess_slack[e, t]
        if e in block.shortage_uids:
            lhs += block.shortage_slack[e, t]
        return(0, lhs - rhs, upper)
    block.balance = po.Constraint(uids, model.timesteps, rule=bus_balance_rule)



def add_simple_io_relation(model, block, idx=0):
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
    block : pyomo.SimpleBlock()

    Returns
    -------
    The constraints are added as a
    attribute to the optimization model object `model` of type
    OptimizationModel()

    """
    if not block.objs or block.objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                         which the constraints should be build")

    eta = {obj.uid: obj.eta for obj in block.objs}

    # constraint for simple transformers: input * efficiency = output
    def io_rule(block, e, t):
        lhs = model.w[model.I[e], e, t] * eta[e][idx] - \
            model.w[e, model.O[e][idx], t]
        return(lhs == 0)
    block.io_relation = po.Constraint(block.indexset, rule=io_rule,
                                      doc="Input * Efficiency = Output")

def add_simple_chp_relation(model, block):
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
    block : SimpleBlock

    Returns
    -------
    The constraints are added as a
    attribute to the optimization model object `model` of type
    OptimizationModel()

    """
    if not block.objs or block.objs is None:
        raise ValueError('No objects defined. Please specify objects for \
                          which backpressure chp constraints should be set.')
    #TODO:
    #  - add possibility of multiple output busses (e.g. for heat and power)
    # efficiencies for simple chps

    eta = {obj.uid: obj.eta for obj in block.objs}

    # additional constraint for power to heat ratio of simple chp comp:
    # P/eta_el = Q/eta_th
    def simple_chp_rule(block, e, t):
        lhs = model.w[e, model.O[e][0], t] / eta[e][0]
        lhs += -model.w[e, model.O[e][1], t] / eta[e][1]
        return(lhs == 0)
    block.pth_relation = po.Constraint(block.indexset, rule=simple_chp_rule,
                                      doc="P/eta_el - Q/eta_th = 0")

def add_simple_extraction_chp_relation(model, block):
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
    block : SimpleBlock()

    Returns:
    --------

    """
    if not block.objs or block.objs is None:
        raise ValueError('No objects defined. Please specify objects for' +
                          'which extraction chp constraints should be set.')

    out_max = {}
    beta = {}
    sigma = {}
    eta_el_cond = {}
    for e in block.objs:
        out_max[e.uid] = e.out_max
        beta[e.uid] = e.beta
        sigma[e.uid] = e.sigma
        eta_el_cond[e.uid] = e.eta_el_cond

    def equivalent_output_rule(block, e, t):
        lhs = model.w[model.I[e], e, t]
        rhs = (model.w[e, model.O[e][0], t] +
              beta[e] * model.w[e, model.O[e][1], t]) / eta_el_cond[e]
        return(lhs == rhs)
    block.equivalent_output = po.Constraint(block.indexset,
                                            rule=equivalent_output_rule,
                                            doc='H = (P + Q*beta)/eta_el_cond')
    def power_heat_rule(block, e, t):
        lhs = model.w[e, model.O[e][0], t]
        rhs = sigma[e] *  model.w[e, model.O[e][1], t]
        return(lhs <= rhs)
    block.pth_relation = po.Constraint(block.indexset, rule=power_heat_rule,
                                       doc="P <= sigma * Q")

def add_global_output_limit(model, block=None):
    """ Adds constraint to set limit for variables as sum over the total
    timehorizon

    .. math:: \sum_{t} \sum_{o \\in O(e)} W(e, o, t) \
    \\leq sumlimit_{out}(e), \\qquad \\forall e

    Parameters
    ------------
    model : OptimizationModel() instance
       An object to be solved containing all Variables, Constraints, Data
       Constraints are added as attribtes to the `model`
    objs : objects
    uids : unique ids

    Returns
    -------
    The constraints are added as attributes
    to the optimization model object `model` of type OptimizationModel()
    """
    if not block.objs or block.objs is None:
        raise ValueError('Failed to create outputlimit. ' +
                         'No objects defined!')

    limit = {obj.uid: obj.sum_out_limit for obj in block.objs}

    # outputs: {'rcoal': ['coal'], 'rgas': ['gas'],...}
    O = {obj.uid: [o.uid for o in obj.outputs[:]] for obj in block.objs}

    # set upper bounds: sum(yearly commodity output) <= yearly_limit
    def output_limit_rule(block, e):
        lhs = sum(model.w[e, o, t] for t in model.timesteps for o in O[e]) -\
              limit[e]
        # if bus is defined but has not outputs Constraint is skipped
        # TODO: should be logged as well?
        if isinstance(lhs, (int, float)) or limit[e] == float('inf'):
            return(po.Constraint.Skip)
        else:
            return(lhs <= 0)
    block.global_limit = po.Constraint(block.uids, rule=output_limit_rule,
                                       doc="Sum of output <= global_limit")

def add_fixed_source(model, block):
    """ Adds fixed source

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
    block : SimpleBlock()

    Returns
    -------
    The constraints will be added as attributes to
    the optimization model object `model` of type OptimizationModel().
    """
    if not block.objs or block.objs is None:
        raise ValueError('No objects defined. Please specify objects for' +
                          'which fixed source constriants should be created.')
    # normed value of renewable source (0 <= value <=1)
    val = {}
    out_max = {}
    for e in block.objs:
         out_max[e.uid] = e.out_max
         val[e.uid] = e.val

    # normed value of renewable source (0 <= value <=1)
    val = {obj.uid: obj.val for obj in block.objs}

    if not block.optimization_options.get('investment', False):
        # maximal ouput of renewable source (in general installed capacity)
        out_max = {obj.uid: obj.out_max for obj in block.objs}
        # edges for renewables ([('wind_on', 'b_el'), ...)
        ee = model.edges(block.objs)
        # fixed values for every timestep
        for (e1, e2) in ee:
            for t in model.timesteps:
                # set value of variable
                model.w[e1, e2, t] = val[e1][t] * out_max[e1][0]
                # fix variable value ("set variable to parameter" )
                model.w[e1, e2, t].fix()
    else:
        # set maximum of additional output
        add_out_limit = {obj.uid: obj.add_out_limit for obj in block.objs}
        # loop over all uids (storages) set the upper bound
        for e in block.uids:
            block.add_out[e].setub(add_out_limit[e])

        def invest_rule(block, e, t):
            lhs = model.w[e, model.O[e][0], t]
            rhs = (out_max[e][model.O[e][0]] + model.add_out[e]) * val[e][t]
            return(lhs == rhs)
        block.invest = po.Constraint(block.indexset, rule=invest_rule)

def add_dispatch_source(model, block):
    """ Creates dispatchable source models by setting bounds and
       adding constraints

    First the maximum value for the output of the source will be set. Then a
    constraint is defined that determines the dispatch of the source. This
    dispatch can be used in the objective function to add cost for dispatch
    of sources.

    The mathemathical formulation of the constraint is as follows:

    .. math:: CURTAIL(e,t) = val_{norm}(e,t) \\cdot out_{max}(e) - \
    W(e,O(e),t),  \\qquad \\forall e, \\forall t

    Parameters
    ------------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data
        Constraints are added as attributes to the `model` and bounds are
        altered for attributes of `model`
    block : SimpleBlock()

    Returns
    -------
    The constraints will be added as attributes of
    the optimization model object `model` of class OptimizationModel().
    """
    if not block.objs or block.objs is None:
        raise ValueError('No objects defined. Please specify objects for' +
                          'which dispatch source constaints should be set.')
    # create dispatch var
    block.curtailment_var = po.Var(block.indexset, within=po.NonNegativeReals)

    # normed value of renewable source (0 <= value <=1)
    val = {}
    out_max = {}
    for e in block.objs:
         out_max[e.uid] = e.out_max
         val[e.uid] = e.val

    ee = model.edges(block.objs)
    # fixed values for every timestep
    for (e1, e2) in ee:
        for t in model.timesteps:
            # set upper bound of variable
            model.w[e1, e2, t].setub(val[e1][t] * out_max[e1][0])

    def curtailment_source_rule(block, e, t):
        lhs = block.curtailment_var[e, t]
        rhs = val[e][t] * out_max[e][model.O[e][0]] - \
           model.w[e, model.O[e][0], t]
        return(lhs == rhs)
    block.curtailment = po.Constraint(block.indexset,
                                      rule=curtailment_source_rule)

def add_storage_balance(model, block):
    """ Constraint to update the storage level in every timestep
        depending on charge and discharge operations and storage losses.

    .. math:: STORLEV(e,t) = STORLEV(e,t-1) \\cdot (1 - CAPLOSS)(e) \
    - \\frac{P_{discharge}(e,t)}{\\eta_{discharge}(e)} \
    + P_{charge}(e,t) \\cdot \\eta_{charge}(e) \
    \\qquad \\forall e, \\forall t

    .. math:: STORLEV = \\text{Storage level}
    .. math:: CAPLOSS = \\text{Self discharge rate}
    .. math:: P_{discharge} = \\text{Discharge power - in systems with \
        hourly timesteps equivalent to the discharge energy}
    .. math:: P_{charge} = \\text{Charge power - in systems with \
        hourly timesteps equivalent to the charge energy}
    .. math:: \\eta_{discharge} = \\text{Discharge efficiency factor}
    .. math:: \\eta_{charge} = \\text{Charge efficiency factor}

    Parameters
    -------------


    Returns
    ----------

    """
    if not block.objs or block.objs is None:
        raise ValueError('No objects defined. Please specify objects for' +
                          'which storage balanece constraint should be set.')
    # constraint for storage energy balance
    cap_initial = {}
    cap_loss = {}
    eta_in = {}
    eta_out = {}

    for e in block.objs:
        cap_initial[e.uid] = e.cap_initial
        cap_loss[e.uid] = e.cap_loss
        eta_in[e.uid] = e.eta_in
        eta_out[e.uid] = e.eta_out

    # set cap of last timesteps to fixed value of cap_initial
    t_last = len(model.timesteps)-1
    for e in block.uids:
      block.cap[e, t_last] = cap_initial[e]
      block.cap[e, t_last].fix()

    def storage_balance_rule(block, e, t):
        # TODO:
        #   - include time increment
        expr = 0
        if(t == 0):
            expr += block.cap[e, t] - cap_initial[e]
            expr += - model.w[model.I[e], e, t] * eta_in[e]
            expr += + model.w[e, model.O[e][0], t] / eta_out[e]
        else:
            expr += block.cap[e, t]
            expr += - block.cap[e, t-1] * (1 - cap_loss[e])
            expr += - model.w[model.I[e], e, t] * eta_in[e]
            expr += + model.w[e, model.O[e][0], t] / eta_out[e]
        return(expr, 0)
    block.balance = po.Constraint(block.indexset, rule=storage_balance_rule)


def add_storage_charge_discharge_limits(model, block):
    """
    Constraints that limit the discharge and charge power by the c-rate

    .. math:: P_{discharge}(e, t) \\leq (CAP_{max}(e) + ADDCAP(e)) \
        \\cdot c_{out}(e)
        \\qquad \\forall e, \\forall t
    .. math:: P_{charge}(e, t) \\leq (CAP_{max}(e) + ADDCAP(e)) \
        \\cdot c_{in}(e)
        \\qquad \\forall e, \\forall t

    .. math:: P_{discharge} = \\text{Discharge power - in systems with \
        hourly timesteps equivalent to the discharge energy}
    .. math:: P_{charge} = \\text{Charge power - in systems with \
        hourly timesteps equivalent to the charge energy}
    .. math:: CAP_{max} = \\text{Installed capacity of energy storage}
    .. math:: ADDCAP = \\text{Additionally installed capacity \
        of energy storage in investment models}
    .. math:: c_{out} = \\text{C factor for discharging, here defined as ratio
        of ouput power and maximum capacity}
    .. math:: c_{in} = \\text{C factor for charging, here defined as ratio
        of input power and maximum capacity}

    """

    c_rate_out = {obj.uid: obj.c_rate_out for obj in block.objs}
    c_rate_in = {obj.uid: obj.c_rate_in for obj in block.objs}
    cap_max = {obj.uid: obj.cap_max for obj in block.objs}

    def storage_discharge_limit_rule(block, e, t):
        expr = 0
        expr += model.w[e, model.O[e][0], t]
        expr += -(cap_max[e] + block.add_cap[e]) \
            * c_rate_out[e]
        return(expr <= 0)
    block.discharge_limit_invest = po.Constraint(block.uids,
                                                 model.timesteps,
                                                 rule=
                                                 storage_discharge_limit_rule)

    def storage_charge_limit_rule(block, e, t):
        expr = 0
        expr += model.w[e, model.I[e], t]
        expr += -(cap_max[e] + block.add_cap[e]) \
            * c_rate_in[e]
        return(expr <= 0)
    block.charge_limit_invest = po.Constraint(block.uids,
                                              model.timesteps,
                                              rule=storage_charge_limit_rule)


def add_output_gradient_calc(model, block, grad_direc='both'):
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
    block : SimpleBlock()

    grad_direc: string
        string defining the direction of the gradient constraint.
        ('positive', negative', 'both')

    Returns
    -------
    The constraints will be added as attributes of
    the optimization model object `model` of class OptimizationModel().
    """
    if not block.objs or block.objs is None:
        raise ValueError('No objects defined. Please specify objects for' +
                          'which output gradient constraints should be set.')

    def grad_pos_calc_rule(block, e, t):
        if t > 0:
            lhs = model.w[e, model.O[e][0], t] - model.w[e,model.O[e][0], t-1]
            rhs = block.grad_pos_var[e, t]
            return(lhs <= rhs)
        else:
            return(po.Constraint.Skip)

    def grad_neg_calc_rule(block, e, t):
        if t > 0:
            lhs = model.w[e, model.O[e][0], t-1] - model.w[e,model.O[e][0], t]
            rhs = block.grad_neg_var[e, t]
            return(lhs <= rhs)
        else:
            return(po.Constraint.Skip)

    def grad_pos_bound_rule(block, e, t):
        return((0, grad_pos[e]))

    def grad_neg_bound_rule(block, e, t):
        return((0, grad_neg[e]))

    # negative gradient
    if grad_direc == 'positive' or grad_direc == "both":
        # create variable
        grad_pos = {obj.uid: obj.grad_pos for obj in block.objs}
        block.grad_pos_var = po.Var(block.indexset, within=po.NonNegativeReals,
                                    bounds=grad_pos_bound_rule)
        # set constraint
        block.grad_pos_calc = po.Constraint(block.indexset,
                                            rule=grad_pos_calc_rule)

    # positive gradient
    if grad_direc == 'negative' or grad_direc == "both":
        # create variable
        grad_neg = {obj.uid: obj.grad_neg for obj in block.objs}
        block.grad_neg_var = po.Var(block.indexset, within=po.NonNegativeReals,
                                    bounds=grad_neg_bound_rule)
        # set constraint
        block.grad_neg_calc = po.Constraint(block.indexset,
                                            rule=grad_neg_calc_rule)
