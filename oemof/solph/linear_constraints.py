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
    bus_coal


In mathematical notation I, O can be seen as indexed index sets The
elements of the sets are the uids of all components (index: `e`). The the
inputs/outputs uids are the elements of the accessed set by the
component index `e`. Generally the index `e` is the index for the uids-sets
containing the uids of objects for which the constraints are build.
For all mathematical constraints the following definitions hold:

    Inputs:
    :math:`\mathcal{I}_e = \\text{Input-uids of entity } e \\in \mathcal{E}`

    Outputs:
    :math:`\mathcal{O}_e = \\text{All output-uids of entity } e \\in \mathcal{E}`


Simon Hilpert (simon.hilpert@fh-flensburg.de)
"""

import inspect
import logging
import pyomo.environ as po
from pandas import Series as pdSeries
from . import pyomo_fastbuild as pofast


def add_bus_balance(model, block=None):
    """ Adds constraint for the input-ouput balance of bus objects.

    The mathematical formulation for the balance is as follows:

    .. math:: \\sum_{i \\in \mathcal{I}_e} w_{i, e}(t) = \\sum_{o \\in O_e} \
    w_{e, o}(t), \\qquad \\forall e, \\forall t

    With :math:`e  \\in \mathcal{E}_B, t \in \mathcal{T}`

    Parameters
    ----------
    model : OptimizationModel() instance
    block : SimpleBlock()
        block to group all constraints and variables etc., block corresponds
        to one oemof base class

    """
    if not block.objs or block.objs is None:
        raise ValueError('Failed to create busbalance. No busobjects defined!')

    uids = []
    I = {}
    O = {}
    for b in block.objs:
        if b.balanced == True:
            uids.append(b.uid)
            I[b.uid] = [i.uid for i in b.inputs]
            O[b.uid] = [o.uid for o in b.outputs]

    block.balanced_uids = po.Set(initialize=uids)
    block.balanced_uids.construct()

    block.balanced_indexset = po.Set(initialize=block.balanced_uids*model.T)
    block.balanced_indexset.construct()

    if not model.energysystem.simulation.fast_build:
        # component inputs/outputs are negative/positive in the bus balance
        def bus_balance_rule(block, e, t):
            lhs = 0
            lhs = sum(model.w[i, e, t] for i in I[e])
            rhs = sum(model.w[e, o, t] for o in O[e])
            return(lhs == rhs)
        block.balance = po.Constraint(block.balanced_indexset,
                                      rule=bus_balance_rule)

    if model.energysystem.simulation.fast_build:
        balance_dict = {}
        for t in model.timesteps:
            for e in uids:
                tuples = [(1, model.w[i, e, t]) for i in I[e]] + \
                         [(-1, model.w[e, o, t]) for o in O[e]]
                balance_dict[e, t] = [tuples, "==", 0.]
        pofast.l_constraint(block, 'balance', balance_dict,
                            block.balanced_indexset)


def add_simple_io_relation(model, block, idx=0):
    """ Adds constraints for input-output relation as simple function for
    all objects in `block.objs`.

    The mathematical formulation of the input-output relation of a simple
    transformer is as follows:

    .. math:: w_{i_e, e}(t) \cdot \\eta_{i,o_{e,n}} = w_{e, o_{e,n}}(t), \
    \\qquad \\forall e, \\forall t

    With :math:`e  \\in \mathcal{E}` and :math:`\mathcal{E}` beeing
    the set of unique ids for all entities grouped inside the
    attribute `block.objs`.

    Additionally :math:`\mathcal{E} \subset \{\mathcal{E}_{IO}, \mathcal{E}_{IOO}\}`.

    :math:`n` indicates the n-th output of component :math:`e` (arg: idx)


    Parameters
    ----------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data.
    block : SimpleBlock()
         block to group all constraints and variables etc., block corresponds
         to one oemof base class
    idx : integer
      Index to choose which output to select (from list of Outputs: O[e][idx])

    """
    if not block.objs or block.objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                         which the constraints should be build")

    eta = {obj.uid: obj.eta for obj in block.objs}

    for key, value in eta.items():
        try:
            len(value[0])
        except:
            eta[key] = [[x] * len(model.timesteps) for x in value]

    # constraint for simple transformers: input * efficiency = output
    def io_rule(block, e, t):
        lhs = model.w[model.I[e][0], e, t] * eta[e][idx][t] - \
            model.w[e, model.O[e][idx], t]
        return(lhs == 0)

    if not model.energysystem.simulation.fast_build:
        block.io_relation = po.Constraint(block.indexset, rule=io_rule,
                                          doc="INFLOW * efficiency = OUTFLOW_n")

    if model.energysystem.simulation.fast_build:
        io_relation_dict = {(e, t): [[(eta[e][idx],
                                      model.w[model.I[e][0], e, t]),
                                      (-1, model.w[e, model.O[e][idx], t])],
                                     "==", 0.]
                            for e,t in block.indexset}
        pofast.l_constraint(block, 'io_relation', io_relation_dict,
                            block.indexset)


def add_two_inputs_one_output_relation(model, block):
    r""" Adds constraint for the input-output relation of a post heating
    transformer with two input flows.

    Then the amount of all input flows multiplied with their efficiency will be
    the output flow. The efficiency of the each will be calculated so that the
    sum of the efficiency of both flows might be greater than one.

    The mathematical formulation for the constraint is as follows:

    .. math::
        w_{e,i_{e,1}}(t)\cdot\eta_{e,i_{e,1}}(t)+w_{e,i_{e,2}}(t)\cdot
        \eta_{e,i_{e,2}}(t)=w_{e,o_{e}},\qquad\forall e,\forall t\qquad\qquad

    .. math::
        w_{e,i_{e,1}}(t)=w_{e,i_{e,2}}(t)\cdot f(t),\quad\forall e,\forall t
        \qquad\\

    With :math:`e\in\mathcal{E}` and :math:`\mathcal{E}` beeing the
    set of unique ids for all entities grouped inside the
    attribute `block.objs`.

    Additionally: :math:`\mathcal{E} \subset \mathcal{E}_{IIO}`.

    Parameters
    ----------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data.
    block : SimpleBlock()
         block to group all constraints and variables etc., block corresponds
         to one oemof base class

    """
    if not block.objs or block.objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                         which the constraints should be build")

    eta = {obj.uid: obj.eta for obj in block.objs}
    f = {obj.uid: obj.f for obj in block.objs}

    # constraint for simple transformers: input * efficiency = output
    def io_rule(block, e, t):
        lhs = (model.w[model.I[e][0], e, t] * eta[e][0] +
               model.w[model.I[e][1], e, t] * eta[e][1] -
               model.w[e, model.O[e][0], t])
        return(lhs == 0)

    def two_inputs_rule(block, e, t):
        lhs = (model.w[model.I[e][1], e, t] * eta[e][1] * f[e][t] -
               model.w[model.I[e][0], e, t] * eta[e][0])
        return(lhs == 0)

    block.io_relation = po.Constraint(
        block.indexset, rule=io_rule,
        doc="INFLOW_1 * efficiency_1 +  INFLOW_2 * efficiency_2 = OUTFLOW")

    block.two_inputs_relation = po.Constraint(
        block.indexset, rule=two_inputs_rule,
        doc="INFLOW_1  =  INFLOW_2 * efficiency_2 * f")


def add_eta_total_chp_relation(model, block):
    """ Adds constraints for input-(output1,output2) relation as
    simple function for all objects in `block.objs`.

    The mathematical formulation of the input-output relation of a simple
    transformer is as follows:

    .. math:: w_{i_e, e}(t) \cdot \\eta^{total}_e = \
    w_{e, o_{e,1}}(t) + w_{e, o_{e,2}}(t), \\qquad \\forall e, \\forall t

    With :math:`e  \\in \mathcal{E}` and :math:`\mathcal{E}` beeing the
    set of unique ids for all entities grouped inside the
    attribute `block.objs`.

    Additionally: :math:`\mathcal{E} \subset \mathcal{E}_{IOO}`.

    Parameters
    ----------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data.
    block : SimpleBlock()
         block to group all constraints and variables etc., block corresponds
         to one oemof base class

    """
    if not block.objs or block.objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                         which the constraints should be build")

    eta_total = {obj.uid: obj.eta_total for obj in block.objs}
    # constraint for simple transformers: input * efficiency = output
    def ioo_rule(block, e, t):
        lhs = model.w[model.I[e][0], e, t] * eta_total[e]
        rhs = model.w[e, model.O[e][0], t] + model.w[e, model.O[e][1], t]
        return(lhs == rhs)
    block.ioo_relation = po.Constraint(block.indexset, rule=ioo_rule,
                             doc="INFLOW * efficiency = OUTFLOW_1 + OUTFLOW_2")


def add_simple_chp_relation(model, block):
    """ Adds constraint for output-output relation for all simple
    combined heat an power units in `block.objs`.

    The mathematical formulation for the constraint is as follows:

    .. math:: \\frac{w_{e, o_{e,1}}(t)}{\\eta_{e, o_{e,1}}(t)} = \
    \\frac{w_{e, o_{e,2}}(t)}{\\eta_{e, o_{e,2}}(t)}, \
    \\qquad \\forall e, \\forall t

    With :math:`e  \\in \mathcal{E}` and :math:`\mathcal{E}` beeing the
    set of unique ids for all entities grouped inside the
    attribute `block.objs`.

    Additionally: :math:`\mathcal{E} \subset \mathcal{E}_{IOO}`.

    Parameters
    ----------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data.
    block : SimpleBlock()
         block to group all constraints and variables etc., block corresponds
         to one oemof base class

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

    if not model.energysystem.simulation.fast_build:
        block.pth_relation = po.Constraint(block.indexset, rule=simple_chp_rule,
                                           doc="P/eta_el - Q/eta_th = 0")

    if model.energysystem.simulation.fast_build:
        pth_relation_dict = {(e, t): [
                                [(1/eta[e][0], model.w[e, model.O[e][0], t]),
                                 (-1/eta[e][1], model.w[e, model.O[e][1], t])],
                                "==", 0.]
                             for e,t in block.indexset}
        pofast.l_constraint(block, 'pth_relation', pth_relation_dict,
                            block.indexset)


def add_simple_extraction_chp_relation(model, block):
    """ Adds constraints for power to heat relation and equivalent output
    for a simple extraction combined heat an power units. The constraints
    represent the PQ-region of the extraction unit and are set for all
    objects in `block.objs`

    The mathematical formulation is as follows:

    For Power/Heat ratio:

    .. math:: w_{e,o_{e,1}}(t) = w_{e, o_{e,2}}(t) \\cdot \\sigma_{e}, \
    \\qquad \\forall e, \\forall t

    .. math:: \\sigma_{e} = \\text{Power to heat ratio of entity } e

    For euivalent power:

    .. math:: w_{i_e,e}(t) = \\frac{w_{e,o_{e,1}}(t) + \\beta_e \\cdot \
    w_{e, o_{e,2}}(t)}{\\eta_{i_e, o_{e,1}}}

    .. math:: \\beta_e = \\text{Power loss index of entity } e

    With :math:`e  \\in \mathcal{E}` and :math:`\mathcal{E}` beeing the
    set of unique ids for all entities grouped inside the
    attribute `block.objs`.

    Additionally: :math:`\mathcal{E} \subset \mathcal{E}_{IOO}`.



    Parameters
    ----------
    model : OptimizationModel() instance
           An object to be solved containing all Variables, Constraints, Data.
    block : SimpleBlock()
         block to group all constraints and variables etc., block corresponds
         to one oemof base class

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
        lhs = model.w[model.I[e][0], e, t]
        rhs = (model.w[e, model.O[e][0], t] +
              beta[e] * model.w[e, model.O[e][1], t]) / eta_el_cond[e]
        return(lhs == rhs)
    block.equivalent_output = po.Constraint(block.indexset,
                                            rule=equivalent_output_rule,
                                            doc='H = (P + Q*beta)/eta_el_cond')
    def power_heat_rule(block, e, t):
        lhs = model.w[e, model.O[e][0], t]
        rhs = sigma[e] *  model.w[e, model.O[e][1], t]
        return(lhs >= rhs)
    block.pth_relation = po.Constraint(block.indexset, rule=power_heat_rule,
                                       doc="P <= sigma * Q")

def add_global_output_limit(model, block=None):
    """ Adds constraints to set limit for variables as sum over the total
    timehorizon for all objects in `block.objs`

    The mathematical formulation is as follows:

    .. math:: \sum_{t \\in \mathcal{T}} \sum_{o \\in \mathcal{O}_e} w_{e, o}(t) \
    \\leq \overline{O}^{global}_e, \\qquad \\forall e \\in E

    With :math:`e  \\in \mathcal{E}` and :math:`\mathcal{E}` beeing the
    set of unique ids for all entities grouped inside the
    attribute `block.objs`.

    Additionally: :math:`\mathcal{E} \subset \{\mathcal{E}_{B},\mathcal{E}_{O}\}`.


    Parameters
    ----------
    model : OptimizationModel() instance
       An object to be solved containing all Variables, Constraints, Data.
    block : SimpleBlock()
         block to group all constraints and variables etc., block corresponds
         to one oemof base class

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
    """ Sets fixed source bounds and constraints for all objects in
    `block.objs`

    The mathematical formulation is as follows:

     .. math::  w_{e,o_e}(t) = V^{norm}_e(t) \\cdot \overline{W}_{e, o_e}, \
     \\qquad \\forall e, \\forall t

    For `investment` for component:

    .. math::  w_{e, o}(t) \\leq (\overline{W}_{e, o_e} + \overline{w}^{add}_{e_o}) \
    \cdot V^{norm}_e(t), \\qquad \\forall e, \\forall t

    .. math:: \overline{w}^{add}_{e_o}  \\leq \overline{W}^{add}_{e_o}, \
    \\qquad \\forall e

    With :math:`e  \\in \mathcal{E}` and :math:`\mathcal{E}` beeing the
    set of unique ids for all entities grouped inside the
    attribute `block.objs`.

    Additionally: :math:`\mathcal{E} \subset \mathcal{E}_{O}`.

    Parameters
    ----------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data.
    block : SimpleBlock()
        block to group all constraints and variables etc., block corresponds
        to one oemof base class

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
            rhs = (out_max[e][0] + block.add_out[e]) * val[e][t]
            return(lhs == rhs)
        block.invest = po.Constraint(block.indexset, rule=invest_rule)

def add_dispatch_source(model, block):
    """ Creates dispatchable source bounds/constraints.

    First the maximum value for the output of the source will be set. Then a
    constraint is defined that determines the dispatch of the source. This
    dispatch can be used in the objective function to add cost for dispatch
    of sources.

    The mathemathical formulation of the constraint is as follows:

    .. math:: w^{cut}_{e,o_e}(t) = V^{norm}_e(t) \\cdot \overline{W}_{e,o_e} - \
    w_{e,o_e}(t),  \\qquad \\forall e, \\forall t

    With :math:`e  \\in \mathcal{E}` and :math:`\mathcal{E}` beeing the
    set of unique ids for all entities grouped in the attribute `block.objs`.

    Additionally: :math:`\mathcal{E} \subset \mathcal{E}_{O}`.


    Parameters
    ----------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data.
    block : SimpleBlock()
         block to group all constraints and variables etc., block corresponds
         to one oemof base class

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
        rhs = val[e][t] * out_max[e][0] - \
           model.w[e, model.O[e][0], t]
        return(lhs == rhs)
    block.curtailment = po.Constraint(block.indexset,
                                      rule=curtailment_source_rule)


def add_storage_balance(model, block):
    """ Constraint to build the storage balance in every timestep

     The mathematical formulation of the constraint is as follows:

    .. math:: l_e(t) = l_e(t-1) \\cdot (1 - C^{loss}(e)) \
    - \\frac{w_{e,o_e}(t)}{\\eta^{out}_e} \
    + w_{i_e,e}(t) \\cdot \\eta^{in}_e  \\qquad \\forall e, \\forall t \\in [2, t_{max}]


    With :math:`e  \\in \mathcal{E}` and :math:`\mathcal{E}` beeing the
    set of unique ids for all entities grouped in the attribute `block.objs`.

    Additionally: :math:`\mathcal{E} \subset \mathcal{E}_{S}`.


    Parameters
    ----------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data.
    block : SimpleBlock()
         block to group all constraints and variables etc., block corresponds
         to one oemof base class
    """
    if not block.objs or block.objs is None:
        raise ValueError('No objects defined. Please specify objects for' +
                         'which storage balance constraint should be set.')
    # constraint for storage energy balance
    cap_initial = {}
    cap_loss = {}
    eta_in = {}
    eta_out = {}

    for e in block.objs:
        cap_initial[e.uid] = e.cap_initial
        cap_loss[e.uid] = e.cap_loss
        # if cap_loss is no list or Series, alter to list
        if not isinstance(cap_loss[e.uid], (list, pdSeries)):
            cap_loss[e.uid] = [cap_loss[e.uid]]*len(model.timesteps)
        eta_in[e.uid] = e.eta_in
        eta_out[e.uid] = e.eta_out

    # set cap of last timesteps to fixed value of cap_initial
    t_last = len(model.timesteps)-1
    for e in block.uids:
        if cap_initial[e] is not None:
            block.cap[e, t_last] = cap_initial[e]
            block.cap[e, t_last].fix()

    def storage_balance_rule(block, e, t):
        # TODO: include time increment
        expr = 0
        if(t == 0):
            t_last = len(model.timesteps)-1
            expr += block.cap[e, t]
            expr += - block.cap[e, t_last] * (1 - cap_loss[e][t])
            expr += - model.w[model.I[e][0], e, t] * eta_in[e]
            expr += + model.w[e, model.O[e][0], t] / eta_out[e]
        else:
            expr += block.cap[e, t]
            expr += - block.cap[e, t-1] * (1 - cap_loss[e][t])
            expr += - model.w[model.I[e][0], e, t] * eta_in[e]
            expr += + model.w[e, model.O[e][0], t] / eta_out[e]
        return(expr, 0)
    block.balance = po.Constraint(block.indexset, rule=storage_balance_rule)


def add_storage_charge_discharge_limits(model, block):
    """ Constraints that limit the discharge and charge power by the c-rate

    Constraints are for investment models only.

    The mathematical formulation for the constraints is as follows:

    Discharge:

    .. math:: w_{e, o_e}(t) \\leq (\overline{L}_e + \overline{l}^{add}_e) \
        \\cdot C^{rate}_{o_e}
        \\qquad \\forall e, \\forall t

    Charge:

    .. math:: w_{i_e, e}(t) \\leq (\overline{L}_e + \overline{l}^{add}_e) \
        \\cdot C^{rate}_{i_e}
        \\qquad \\forall e, \\forall t


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
        expr += model.w[model.I[e][0], e, t]
        expr += -(cap_max[e] + block.add_cap[e]) \
            * c_rate_in[e]
        return(expr <= 0)
    block.charge_limit_invest = po.Constraint(block.uids,
                                              model.timesteps,
                                              rule=storage_charge_limit_rule)


def add_output_gradient_calc(model, block, grad_direc='both', idx=0):
    """ Add constraint to calculate the gradient between two timesteps
    (positive and negative)

    The mathematical formulation for constraints are as follows:

    Positive gradient:

    .. math::  w_{e,o_{e,n}}(t) - w_{e, o_{e,n}}(t-1) \\leq g^{pos}_{e_o}(t)\
    \\qquad \\forall e, \\forall t / t=1

    .. math:: g^{pos}_{e_o}(t) \\leq \overline{G}^{pos}_{e_o}, \\qquad \\forall e, \\forall t

    Negative gradient:

        .. math::  w_{e,o_{e,n}}(t-1) - w_{e,o_{e,n}}(t) \\leq g^{neg}_{e_o}(t)\
    \\qquad \\forall e, \\forall t / t=1

    .. math:: g^{neg}_{e_o}(t) \\leq \overline{G}^{neg}_{e_o}, \\qquad \\forall e, \\forall t

    With :math:`e  \\in \mathcal{E}` and :math:`\mathcal{E}` beeing the
    set of unique ids for all entities grouped in the attribute `block.objs`.

    Additionally: :math:`\mathcal{E} \subset \mathcal{E}_{C}`.

    :math:`n` indicates the n-th output of component :math:`e` (arg: idx)

    Parameters
    ----------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data.
    block : SimpleBlock()
         block to group all constraints and variables etc., block corresponds
         to one oemof base class

    grad_direc: string
        string defining the direction of the gradient constraint.
        ('positive', negative', 'both')

    """
    if not block.objs or block.objs is None:
        raise ValueError('No objects defined. Please specify objects for' +
                          'which output gradient constraints should be set.')

    def grad_pos_calc_rule(block, e, t):
        if t > 0:
            lhs = model.w[e, model.O[e][idx], t] - model.w[e,model.O[e][idx], t-1]
            rhs = block.grad_pos_var[e, t]
            return(lhs <= rhs)
        else:
            return(po.Constraint.Skip)

    def grad_neg_calc_rule(block, e, t):
        if t > 0:
            lhs = model.w[e, model.O[e][idx], t-1] - model.w[e,model.O[e][idx], t]
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


