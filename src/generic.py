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


def generic_variables(model, edges, timesteps, var_name="w"):
    """ variables creates all variables corresponding to the edges indexed
    by t in timesteps, (e1,e2) in all_edges
    if invest flag is set to true, an additional variable indexed by
    (e1,e2) in all_edges is created.
    """
    # variable for all edges
    model.w = po.Var(edges, timesteps, within=po.NonNegativeReals)

    # additional variable for investment models
    if model.invest is True:
        model.add_cap = po.Var(edges, within=po.NonNegativeReals)

    # dispatch variables for dispatchable sources
    objs = [e for e in model.entities
            if isinstance(e, cp.sources.DispatchSource)]
    if objs:
        uids = [e.uid for e in objs]
        model.dispatch = po.Var(uids, timesteps,
                                within=po.NonNegativeReals)
    # storage state of charge variables
    objs = [e for e in model.entities
            if isinstance(e, cp.transformers.Storage)]
    if objs:
        uids = [e.uid for e in objs]

        soc_max = {obj.uid: obj.soc_max for obj in objs}
        soc_min = {obj.uid: obj.soc_min for obj in objs}

        def soc_bound_rule(model, e, t):
            return(soc_min[e], soc_max[e])
        model.soc = po.Var(uids, timesteps, bounds=soc_bound_rule)

        if model.invest is True:
            model.soc_add = po.Var(uids, within=po.NonNegativeReals)
            model.soc_max = po.Param(uids, initialize=soc_max)


def generic_io_constraints(model, objs=None, uids=None,
                           timesteps=None):
    """ creates constraint for input output relation as
    input * efficiency = output
    param objs: list of component objects for which the constraint will be
    build
    """
    if objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                         which the constraints should be build")
    if uids is None:
        uids = [e.uids for e in objs]

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
    """
    """
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
    """
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

    if model.invest is False:
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
    """
    """
    O = {obj.uid: [o.uid for o in obj.outputs[:]] for obj in objs}
    out_max = {obj.uid: obj.out_max for obj in objs}

    # constraint for additional capacity
    def rule(model, e, t):
        expr = model.w[e, O[e][0], t] - out_max[e][O[e][0]] - \
            model.add_cap[e, O[e][0]]
        return(expr <= 0)
    setattr(model, "generic_w_ub_" + objs[0].lower_name,
            po.Constraint(uids, timesteps, rule=rule))


def generic_soc_ub_invest(model, objs=None, uids=None, timesteps=None):

    # constraint for additional capacity in investment models
    def rule(model, e, t):
        return(model.soc[e, t] <= model.soc_max[e] + model.soc_add[e])
    setattr(model, "generic_soc_ub_invest_"+objs[0].lower_name,
            po.Constraint(uids, timesteps, rule=rule))


def generic_limit(model, objs=None, uids=None, timesteps=None):
    """generic limit constraints.

    Parameters
    ----------
    model : pyomo.ConcreteModel

    Returns
    -------
    model : pyomo.ConcreteModel
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
    """
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
    """
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


def generic_dispatch_source(model, objs, uids, timesteps):
    """
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
