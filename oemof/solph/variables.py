# -*- coding: utf-8 -*-
"""
Module contains variable definitions and constraint to bound variables (e.g.
for investement).

@author: Simon Hilpert (simon.hilpert@fh-flensburg.de)
"""

import pyomo.environ as po
import numpy as np
import logging

try:
    from oemof.core.network.entities import components as cp
except:
    from .network.entities import components as cp

def add_binary(model, block, relaxed=False):
    """ Creates all status variables (binary) for `block.objs`

    Status variable indicates if a unit is turned on or off.
    E.g. if a transformer is switched on/off -> y=1/0

    Parameters
    ----------
    model : pyomo.ConcreteModel()
        A pyomo-object to be solved containing all Variables, Constraints, Data
        Variables are added as attributes to the `model`
    objs : array_like (list)
        all components for which the status variable is created
    relaxed : boolean
       If True "binary" variables will be created as continuous variables with
       bounds of 0 and 1.

    """
    # check
    if block.objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                          which the status variable should be created.")
    # add binary variables to model
    if not relaxed:
        block.y = po.Var(block.indexset, within=po.Binary)
    if relaxed:
        block.y = po.Var(block.indexset, within=po.NonNegativeReals,
                         bounds=(0,1))

def add_continuous(model, edges):
    """ Adds all variables corresponding to the edges of the bi-partite
    graph for all timesteps.

    The function uses the pyomo class `Var()` to create the optimization
    variables. As index-sets the provided edges of the graph
    (in general all edges) and the defined timesteps are used.
    If an invest model is used an additional optimization variable indexed by
    the edges is created to handle "flexible" upper bounds of the edge variable
    by using an additional constraint.
    The following variables are created: Variables for all the edges, variables
    for the state of charge of storages.
    (If specific components such as disptach sources and storages exist.)

    Parameters
    ----------
    model : OptimizationModel() instance
        A object to be solved containing all Variables, Constraints, Data
        Variables are added as attributes to the `model`
    edges : array_like (list)
        `edges` will be a list containing tuples representing the directed
        edges of the graph by using unique ids of components and buses.
        e.g. [('coal', 'pp_coal'), ('pp_coal', 'b_el'),...]

    Returns
    -------
    The variables are added as a attribute to the optimization model object
    `model`.
    """
    # variable for all edges
    model.w = po.Var(edges, model.timesteps, within=po.NonNegativeReals)



def set_bounds(model, block, side='output'):
    """ Sets bounds for variables that represent the weight
    of the edges of the graph if investment models are calculated.

    For investment  models upper and lower bounds will be modeled via
    additional constraints. The mathematical description for the
    constraint is as follows:

    If side is `output`

    .. math:: W(e, O_1(e)), t) \\leq out_{max}(e, t), \\qquad \
    \\forall e, \\forall t

    With investment:

    .. math::  W(e, O_1(e), t) \\leq out_{max}(e, t) + \
    ADDCAP(e,O_1[e]), \\qquad \\forall e, \\forall t

    If side is `input`:

    .. math:: W(I(e), e, t) \\leq in_{max}(e, t), \\qquad \
    \\forall e, \\forall t

    With :math:`e  \\in E` and :math:`E` beeing the set of unique ids for
    all entities grouped inside the attribute `block.objs`.

    :math:`O_1(e)` beeing the set of all first outputs of
    entitiy (component) :math:`e`.

    :math:`I(e)` beeing the set of all inputs of entitiy (component) :math:`e`.

    Parameters
    ----------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data
        Constraints are added as attributes to the `model`
    block : SimpleBlock()
    side : string
       Side of component for which the bounds are set ('input' or 'output')

    """

    if block.objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                          which bounds should be set.")
    if block.uids is None:
        block.uids = [e.uids for e in block.objs]

    # set variable bounds (out_max = in_max * efficiency):
    # m.in_max = {'pp_coal': 51794.8717948718, ... }
    # m.out_max = {'pp_coal': 20200, ... }
    in_max = {}
    out_max = {}
    for e in block.objs:
        if side == 'output':
            output_uids = [o.uid for o in e.outputs[:]]
            out_max[e.uid] = dict(zip(output_uids, e.out_max))
        if side == 'input':
            input_uids = [i.uid for i in e.inputs[:]]
            in_max[e.uid] = dict(zip(input_uids, e.in_max))


    if not block.optimization_options.get('investment', False):
        # edges for simple transformers ([('coal', 'pp_coal'),...])
        ee = model.edges(block.objs)
        for (e1, e2) in ee:
            for t in model.timesteps:
                # transformer output <= model.out_max
                if e1 in block.uids and side == 'output':
                    model.w[e1, e2, t].setub(out_max[e1][e2])
                # transformer input <= model.in_max
                if e2 in block.uids and side == 'input':
                    try:
                        model.w[e1, e2, t].setub(in_max[e2][e1])
                    except:
                        logging.warning("No upper bound for input (%s,%s)",
                                        e1, e2)
                        pass

    else:
        if side == 'output':
            # set maximum of addiational storage capacity
            add_out_limit = {obj.uid: obj.add_out_limit for obj in block.objs}
            # loop over all uids (storages) set the upper bound
            for e in block.uids:
                block.add_out[e].setub(add_out_limit[e])

            # constraint for additional capacity
            def add_output_rule(block, e, t):
                lhs = model.w[e, model.O[e][0], t]
                rhs = out_max[e][model.O[e][0]] + block.add_out[e]
                return(lhs <= rhs)
            block.output_bound = po.Constraint(block.indexset,
                                               rule=add_output_rule)

        # TODO: Implement upper bound constraint for investment models
        if side == 'input':
            raise ValueError('Setting upper bounds on inputs of components' +
                              ' not possible for investment models')



def set_storage_cap_bounds(model, block):
    """ Alters/sets upper and lower bounds for variables that represent the
    absolut state of charge e.g. filling level of a storage component.

    For investment  models upper and lower bounds will be modeled via
    additional constraints. The mathematical description for the
    constraint is as follows:

     .. math:: cap_{min}(e) \\leq CAP(e, t) \\leq cap_{max}(e), \
    \\qquad \\forall e, \\forall t

    If investment:

    .. math:: CAP(e, t) \\leq cap_{max}(e) + ADDCAP(e), \
    \\qquad \\forall e, \\forall t

    With :math:`e  \\in E` and :math:`E` beeing the set of unique ids for
    all entities grouped inside the attribute `block.objs`.


    Parameters
    ----------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data
        Bounds are altered at model attributes (variables) of `model`
    block : SimpleBlock()
    """


    if block.objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                         which bounds should be set.")
    if block.uids is None:
        block.uids = [e.uids for e in block.objs]

    # extract values for storages m.cap_max = {'storge': 120.5, ... }
    cap_max = {obj.uid: obj.cap_max for obj in block.objs}
    cap_min = {obj.uid: obj.cap_min for obj in block.objs}

    if not block.optimization_options.get('investment', False):
        # loop over all uids (storages) and timesteps to set the upper bound
        for e in block.uids:
            for t in model.timesteps:
                block.cap[e, t].setub(cap_max[e])
                block.cap[e, t].setlb(cap_min[e])
    else:
        # set maximum of additional storage capacity
        add_cap_limit = {obj.uid: obj.add_cap_limit for obj in block.objs}
        # loop over all uids (storages) set the upper bound
        for e in block.uids:
            block.add_cap[e].setub(add_cap_limit[e])

        # constraint for additional capacity in investment models
        def add_cap_rule(block, e, t):
            lhs = block.cap[e, t]
            rhs = cap_max[e] + block.add_cap[e]
            return(lhs <= rhs)
        block.cap_bound = po.Constraint(block.indexset,
                                        rule=add_cap_rule)

def set_outages(model, block, outagetype='period', side='output'):
    """ Fixes component input/output to zeros for modeling outages.


    Parameters
    ----------
    model :OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data.
    block : SimpeBlock()
    outagetype : string
        Type to model outages of component if outages is scalar.
       'period' yield one timeblock where component is off,
       while 'random_days' will sample random days over the timehorizon
       where component is off
    side : string
       Side of component to fix to zero: 'output', 'input'.

    """
    outages = {obj.uid: obj.outages for obj in block.objs}
    timesteps = {}
    for e in outages.keys():
       if isinstance(outages[e], (float, np.float)) \
          and outages[e] <= 1 and outages[e] >= 0:
            time_off = int(len(model.timesteps) * outages[e])
            if outagetype == 'period':
                start = np.random.randint(0, len(model.timesteps)-time_off+1)
                end = start + time_off
                timesteps[e] = [t for t in range(start, end)]
            if outagetype == 'random_days':
                timesteps[e] = np.random.randint(0, len(model.timesteps))
       elif len(outages[e]) >= 1:
           timesteps[e] = outages[e]
       else:
           timesteps[e] = []

    if side == 'input' and timesteps[e]:
        for e in block.uids:
            for t in timesteps[e]:
                model.w[model.I[e], e, t] = 0
                model.w[model.I[e], e, t].fix()
    if side == 'output' and timesteps[e]:
        for e in block.uids:
            for t in timesteps[e]:
                model.w[e, model.O[e][0], t] = 0
                model.w[e, model.O[e][0], t].fix()
    else:
      pass

def set_fixed_sink_value(model, block):
    """ Setting a value und fixes the variable of input.

    The mathematical formulation is as follows:

    .. math:: W(I(e), e,t) = val(e,t), \\qquad \\forall e, \\forall t

    With :math:`e  \\in E` and :math:`E` beeing the set of unique ids for
    all entities grouped inside the attribute `block.objs`.

    :math:`I(e)` beeing the set of all inputs of entitiy (component) :math:`e`.

    Parameters
    ----------
    model :OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data
        Attributes are altered of the `model`
    block : SimpeBlock()

    """

    val = {obj.uid: obj.val for obj in block.objs}
    ee = model.edges(block.objs)
    for (e1, e2) in ee:
        for t in model.timesteps:
            # set variable value
            model.w[(e1, e2), t] = val[e2][t]
            # fix variable value for optimization problem
            model.w[(e1, e2), t].fix()
