# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 18:41:08 2015

@author: simon
"""

import pyomo.environ as po
import logging

try:
    from oemof.core.network.entities import components as cp
    from oemof.core.network.entities import Component
except:
    from .network.entities import components as cp

def add_binary(model, objs=None, uids=None):
    """ Creates all variables status variables (binary) for `objs`

    The function uses the pyomo class `Var()` to create the status variables of
    components. E.g. if a transformer is switched on/off -> y=1/0
    As index-sets the provided unique ids of the objects and the defined
    timesteps are used.

    Parameters
    ------------

    model : pyomo.ConcreteModel()
        A pyomo-object to be solved containing all Variables, Constraints, Data
        Variables are added as attributes to the `model`
    objs : array_like (list)
        all components for which the status variable is created
    uids : unique ids of `ojbs`

    Returns
    --------

    There is no return value. The variables are added as a
    attribute to the optimization model object `model` of type
    pyomo.ConcreteModel()


    """
    # check
    if objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                          which the status variable should be created.")
    if uids is None:
        uids = [e.uids for e in objs]

    # add binary variables to model
    setattr(model, "status_"+objs[0].lower_name,
            po.Var(uids, model.timesteps, within=po.Binary))

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

    Returns
    --------
    The variables are added as a attribute to the optimization model object
    `model` of type OptimizationModel()


    """
    # variable for all edges
    model.w = po.Var(edges, model.timesteps, within=po.NonNegativeReals)


    # additional variable for investment models
    if model.invest is True:
        objs = [e for e in model.entities if isinstance(e, Component)]
        uids = [e.uid for e in objs]
        model.add_out = po.Var(uids, within=po.NonNegativeReals)

    # storage state of charge variables
    objs = [e for e in model.entities
            if isinstance(e, cp.transformers.Storage)]
    # if storages exist, create pyomo variables
    if objs:
        uids = [e.uid for e in objs]

        model.cap = po.Var(uids, model.timesteps, within=po.NonNegativeReals)

        # create additional variable for investment models
        if model.invest is True:
            model.add_cap = po.Var(uids, within=po.NonNegativeReals)


def set_bounds(model, objs=None, uids=None, side='output'):
    """ Sets bounds for variables that represent the weight
    of the edges of the graph if investment models are calculated.

    For investment  models upper and lower bounds will be modeled via
    additional constraints of type pyomo.Constraint(). The mathematical
    description for the constraint is as follows

    .. math::  w(e, O_1[e], t) \\leq out_{max}(e,O_1[e]) + \
    add\\_cap(e,O_1[e]), \\qquad \\forall e \\in uids, \\forall t \\in T

        .. math:: w(e_1, e_2, t) \\leq ub_w(e_1, e_2), \\qquad \
    \\forall (e_1, e_2) \\in \\vec{E}, \\forall t \\in T
    .. math:: w(e_1, e_2, t) \\geq lb_w(e_1, e_2), \\qquad \
    \\forall (e_1, e_2) \\in \\vec{E}, \\forall t \\in T

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
    side : side of component for which the bounds are set('input' or 'output')

    Returns
    -------
    The constraints are added as attributes
    to the optimization model object `model` of type OptimizationModel()
    """

    if objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                          which bounds should be set.")
    if uids is None:
        uids = [e.uids for e in objs]

    # set variable bounds (out_max = in_max * efficiency):
    # m.in_max = {'pp_coal': 51794.8717948718, ... }
    # m.out_max = {'pp_coal': 20200, ... }
    in_max = {}
    out_max = {}
    for e in objs:
        in_max[e.uid] = e.in_max
        out_max[e.uid] = e.out_max

    if model.invest is False:
        # edges for simple transformers ([('coal', 'pp_coal'),...])
        ee = model.edges(objs)
        for (e1, e2) in ee:
            for t in model.timesteps:
                # transformer output <= model.out_max
                if e1 in uids and side == 'output':
                    model.w[e1, e2, t].setub(out_max[e1][e2])
                # transformer input <= model.in_max
                if e2 in uids and side == 'input':
                    try:
                        model.w[e1, e2, t].setub(in_max[e2][e1])
                    except:
                        logging.warning("No upper bound for input (%s,%s)",
                                        e1, e2)
                        pass

    else:
        if side == 'output':
            # set maximum of addiational storage capacity
            add_out_limit = {obj.uid: obj.add_out_limit for obj in objs}
            # loop over all uids (storages) set the upper bound
            for e in uids:
                model.add_out[e].setub(add_out_limit[e])

            # constraint for additional capacity
            def add_output_rule(model, e, t):
                lhs = model.w[e, model.O[e][0], t]
                rhs = out_max[e][model.O[e][0]] + model.add_out[e]
                return(lhs <= rhs)
            setattr(model, objs[0].lower_name+"_output_bound",
                    po.Constraint(uids, model.timesteps, rule=add_output_rule))

        # TODO: Implement upper bound constraint for investment models
        if side == 'input':
            raise ValueError('Setting upper bounds on inputs of components' +
                              ' not possible for investment models')



def set_storage_cap_bounds(model, objs=None, uids=None):
    """ Alters/sets upper and lower bounds for variables that represent the
    state of charge e.g. filling level of a storage component.

    For investment  models upper and lower bounds will be modeled via
    additional constraints of type pyomo.Constraint(). The mathematical
    description for the constraint is as follows:

    .. math:: cap(e, t) \\leq cap_{max}(e) + cap_{add}(e), \
    \\qquad \\forall e \\in uids, \\forall t \\in T

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

    # extract values for storages m.cap_max = {'storge': 120.5, ... }
    cap_max = {obj.uid: obj.cap_max for obj in objs}
    cap_min = {obj.uid: obj.cap_min for obj in objs}

    if model.invest is False:
        # loop over all uids (storages) and timesteps to set the upper bound
        for e in uids:
            for t in model.timesteps:
                model.cap[e, t].setub(cap_max[e])
                model.cap[e, t].setlb(cap_min[e])
    else:
        # set maximum of additional storage capacity
        add_cap_limit = {obj.uid: obj.add_cap_limit for obj in objs}
        # loop over all uids (storages) set the upper bound
        for e in uids:
            model.add_cap[e].setub(add_cap_limit[e])

        # constraint for additional capacity in investment models
        def add_cap_rule(model, e, t):
            lhs = model.cap[e, t]
            rhs = cap_max[e] + model.add_cap[e]
            return(lhs <= rhs)
        setattr(model,objs[0].lower_name+"_cap_bound",
                po.Constraint(uids, model.timesteps, rule=add_cap_rule))

def set_fixed_sink_value(model, objs=None, uids=None):
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

    Returns
    -------

    The variables as attributes to
    the optimization model object `model` of type OptimizationModel() will
    be altered.
    """

    val = {obj.uid: obj.val for obj in objs}
    ee = model.edges(objs)
    for (e1, e2) in ee:
        for t in model.timesteps:
            # set variable value
            model.w[(e1, e2), t] = val[e2][t]
            # fix variable value for optimization problem
            model.w[(e1, e2), t].fix()
