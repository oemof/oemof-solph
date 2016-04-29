# -*- coding: utf-8 -*-
"""
Module contains variable definitions and constraint to bound variables (e.g.
for investement).

@author: Simon Hilpert (simon.hilpert@fh-flensburg.de)
"""

import pyomo.environ as po
import numpy as np
import logging


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
                         bounds=(0, 1))


def add_continuous(model, edges):
    """ Adds all variables corresponding to the edges of the bi-partite
    graph for all timesteps.

    The function uses the pyomo class `Var()` to create the optimization
    variables. As index-sets the provided edges of the graph
    (in general all edges) and the defined timesteps are used.
    The following variables are created: Variables for all the edges
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

    .. math:: w_{e, o_{e,1}}(t) \\leq \\overline{W}_{e, o_{e,1}} \\qquad \
    \\forall e, \\forall t

    With investment:

    .. math::  w_{e, o_{e,1}}(t) \\leq \\overline{W}_{e, o_{e,1}} + \
    \\overline{w}^{add}_{o_e}, \\qquad \\forall e, \\forall t

    If side is `input`:

    .. math:: w_{i_{e}, e}(t) \\leq \\overline{W}_{i_{e}, e} \\qquad \
    \\forall e, \\forall t

    With :math:`e  \\in \mathcal{E}` and :math:`\mathcal{E}` beeing
    the set of unique ids for all entities grouped inside the
    attribute `block.objs`.


    Parameters
    ----------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data
        Constraints are added as attributes to the `model`
    block : SimpleBlock()
    side : string
       Side of component for which the bounds are set ('input' or 'output')

    """
    logging.debug("Set bounds for {0}.".format(block))
    if block.objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                          which bounds should be set.")
    if block.uids is None:
        block.uids = [e.uids for e in block.objs]

    # set variable bounds (out_max = in_max * efficiency):
    # m.in_max = {'pp_coal': 51794.8717948718, ... }
    # m.out_max = {'pp_coal': 20200, ... }
    ub_in = {}
    ub_out = {}
    out_max = {}
    exist_ub_out = False
    for e in block.objs:
        if side == 'output':
            output_uids = [o.uid for o in e.outputs[:]]
            # ** Time depended bound
            if e.ub_out:
                ub_out[e.uid] = dict(zip(output_uids, e.ub_out))
                out_max[e.uid] = dict(zip(output_uids, e.out_max))
                if e.out_max < np.array(e.ub_out).max():
                    logging.error('The maximal value of ub_out should not be' +
                                  ' greater than out_max ({}).'.format(e.uid))
                exist_ub_out = True
            # ** Constant bound
            else:
                # If ub_out (time depended bound9 does not exist, create a list
                # with the same value. Use out_max for the upper bound of the
                # variable.
                ub_out[e.uid] = dict(zip(
                    output_uids,
                    [[x] * len(model.timesteps) for x in e.out_max]))
                out_max[e.uid] = dict(zip(output_uids, e.out_max))
        if side == 'input' and e.in_max is not None:
            input_uids = [i.uid for i in e.inputs[:]]
            ub_in[e.uid] = dict(zip(
                input_uids,
                [[x] * len(model.timesteps) for x in e.in_max]))

    # *** No investment - set upper bound to maximal output***
    if not block.optimization_options.get('investment', False):
        # edges for simple transformers ([('coal', 'pp_coal'),...])
        ee = model.edges(block.objs)
        for (e1, e2) in ee:
            for t in model.timesteps:
                # transformer output <= model.out_max
                if e1 in block.uids and side == 'output':
                    model.w[e1, e2, t].setub(ub_out[e1][e2][t])
                # transformer input <= model.in_max
                if e2 in ub_in and side == 'input':
                    try:
                        model.w[e1, e2, t].setub(ub_in[e2][e1][t])
                    except:
                        logging.warning("No upper bound for input (%s,%s)",
                                        e1, e2)
                        pass

    # *** Investment - set upper bound to overall output and add constraint***
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
                rhs = ub_out[e][model.O[e][0]][t] + block.add_out[e]
                return(lhs <= rhs)

            # constraint for additional capacity
            def add_output_rule_time_depended_bound(block, e, t):
                lhs = model.w[e, model.O[e][0], t]
                rhs = ub_out[e][model.O[e][0]][t] * (
                    1 + block.add_out[e] / out_max[e][model.O[e][0]])
                return(lhs <= rhs)

            if exist_ub_out:
                block.output_bound = po.Constraint(
                        block.indexset,
                        rule=add_output_rule_time_depended_bound)
            else:
                block.output_bound = po.Constraint(
                        block.indexset, rule=add_output_rule)

        # TODO: Implement upper bound constraint for investment models
        elif side == 'input':
            error_mesg = "Setting upper bounds on inputs of components is "
            error_mesg += "not possible for investment models"
            for e in block.objs:
                if e.in_max is not None:
                    for in_max in e.in_max:
                        if in_max is not None and in_max != float("inf"):
                            raise ValueError(error_mesg)


def set_storage_cap_bounds(model, block):
    """ Alters/sets upper and lower bounds for variables that represent the
    absolut state of charge e.g. filling level of a storage component.

    For investment  models upper and lower bounds will be modeled via
    additional constraints. The mathematical description for the
    constraint is as follows:

     .. math:: \\underline{L}_e \\leq l_e(t) \\leq \\overline{L}_e, \
    \\qquad \\forall e, \\forall t

    If investment:

    .. math:: l_e(t)  \\leq \\overline{L}_e + \\overline{l}^{add}_e, \
    \\qquad \\forall e, \\forall t

    With :math:`e  \\in \mathcal{E}` and :math:`\mathcal{E}` beeing
    the set of unique ids for all entities grouped inside the
    attribute `block.objs`.

    Additionally :math:`\mathcal{E} \subset \mathcal{E}_{S}`.

    Parameters
    ----------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data
        Bounds are altered at model attributes (variables) of `model`
    block : SimpleBlock()
         block to group all objects corresponding to one oemof base class
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
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data.
    block : SimpleBlock()
         block to group all objects corresponding to one oemof base class
    outagetype : string
        String indicates how to model outages of component. If outages is
        scalar 'period' yield one timeblock where component is off,
        while 'random_days' will sample random days over the timehorizon
        where component will forced to be offline.
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
                if t <= len(model.timesteps)-1:
                    model.w[model.I[e][0], e, t] = 0
                    model.w[model.I[e][0], e, t].fix()
    if side == 'output' and timesteps[e]:
        for e in block.uids:
            for t in timesteps[e]:
                if t <= len(model.timesteps)-1:
                    model.w[e, model.O[e][0], t] = 0
                    model.w[e, model.O[e][0], t].fix()
    else:
        pass


def set_fixed_sink_value(model, block):
    """ Setting a value und fixes the variable of input.

    The mathematical formulation is as follows:

    .. math:: w_{i_e, e}(t) = V_e(t), \\qquad \\forall e, \\forall t

    With :math:`e  \\in \mathcal{E}` and :math:`\mathcal{E}` beeing
    the set of unique ids for all entities grouped inside the
    attribute `block.objs`.

    Additionally :math:`\mathcal{E} \subset \mathcal{E}_{I}`.

    Parameters
    ----------
    model :OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data
        Attributes are altered of the `model`
    block : SimpleBlock()
         block to group all objects corresponding to one oemof base class

    """

    val = {obj.uid: obj.val for obj in block.objs}
    ee = model.edges(block.objs)
    for (e1, e2) in ee:
        for t in model.timesteps:
            # set variable value
            model.w[(e1, e2), t] = val[e2][t]
            # fix variable value for optimization problem
            model.w[(e1, e2), t].fix()
