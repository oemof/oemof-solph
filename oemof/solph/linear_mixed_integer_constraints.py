# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 11:31:11 2015

@author: simon
"""
import pyomo.environ as po


def set_bounds(model, objs=None, uids=None, side="output"):
    """ Set upper/lower bounds on all output variables via constraints

    The bounds are set with constraints using the binary status variable `y`
    of components. The bounds are only set for the ouput of variables.
    E.g. p_max constraints for transformers in milp problems
    can be set with this function.
    If you want to model e.g. p_max-constraints via the input side of a
    component (i.e. fuel) use milp_in_max_bound()
    Parameters
    ------------

    model : pyomo.ConcreteModel()
        A pyomo-object to be solved containing all Variables, Constraints, Data
        Bounds are altered at model attributes (variables) of `model`
    objs : array like
        list of component objects for which the bounds will be
        altered
    uids : array like
        list of component uids corresponding to the objects

    Returns
    -------

    There is no return value. The upper and lower bounds of the variables are
    set with constraints in the optimization model object `model` of type
    pyomo.ConcreteModel()

    """
    if objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                         which bounds should be set.")
    if uids is None:
        uids = [e.uids for e in objs]

    if side == "output":
        out_max = {obj.uid: obj.out_max for obj in objs}

        # set upper bounds
        def ub_rule(model, e, t):
            return(model.w[e, model.O[e][0], t] <=
                       getattr(model, "status_"+objs[0].lower_name)[e, t]
                        * out_max[e][model.O[e][0]])
        setattr(model, objs[0].lower_name+"_maximum_output",
                po.Constraint(uids, model.timesteps, rule=ub_rule))

        out_min = {obj.uid: obj.out_min for obj in objs}
        # set lower bounds
        def lb_rule(model, e, t):
            lhs = getattr(model,objs[0].lower_name+'_status_var')[e, t] * \
                      out_min[e][model.O[e][0]]
            rhs = model.w[e, model.O[e][0], t]
            return(lhs <= rhs)
        setattr(model, objs[0].lower_name+"_minimum_output",
                po.Constraint(uids, model.timesteps, rule=lb_rule))

    if side == "input":
        in_max = {obj.uid: obj.in_max for obj in objs}

        # set upper bounds
        def ub_rule(model, e, t):
            return(model.w[model.I[e], e, t] <=
                       getattr(model, "status_"+objs[0].lower_name)[e, t]
                        * in_max[e][model.I[e]])
        setattr(model, objs[0].lower_name+"_maximum_input",
                po.Constraint(uids, model.timesteps, rule=ub_rule))

        in_min = {obj.uid: obj.in_min for obj in objs}
        # set lower bounds
        def lb_rule(model, e, t):
            lhs = getattr(model,objs[0].lower_name+'_status_var')[e, t] * \
                      in_min[e][model.I[e]]
            rhs = model.w[model.I[e], e, t]
            return(lhs <= rhs)
        setattr(model, objs[0].lower_name+"_minimum_input",
                po.Constraint(uids, model.timesteps, rule=lb_rule))

def add_output_gradient_constraints(model, objs=None, uids=None,
                                    grad_direc="both"):
    """ Creates constraints to model the output gradient

    Parameter
    ------------
    model : pyomo.ConcreteModel()
        A pyomo-object to be solved containing all Variables, Constraints, Data

    objs : array like
        list of component objects for which the bounds will be
        altered
    uids : array linke
        list of component uids corresponding to the objects
    grad_direc : string
         direction of gradient ("both", "positive", "negative")
    Returns
    -------


    References
    ----------
    .. [1] M. Steck (2012): "Entwicklung und Bewertung von Algorithmen zur
       Einsatzplanerstelleung virtueller Kraftwerke", PhD-Thesis,
       TU Munich, p.38

    """
    if objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                          which bounds should be set.")
    if uids is None:
        uids = [e.uids for e in objs]

    out_min = {obj.uid: obj.out_min for obj in objs}
    grad_pos = {obj.uid: obj.grad_pos for obj in objs}

    y = getattr(model, objs[0].lower_name+'_status_var')

    # TODO: Define correct boundary conditions for t-1 of time
    def grad_pos_rule(model, e, t):
        if t > 1:
            return(model.w[e, model.O[e][0], t] - model.w[e, model.O[e][0], t-1] <=  \
               grad_pos[e] + out_min[e][model.O[e][0]] * (1 -y[e, t]))
        else:
            return(po.Constraint.Skip)

    grad_neg = {obj.uid: obj.grad_neg for obj in objs}
    # TODO: Define correct boundary conditions for t-1 of time horizon
    def grad_neg_rule(model, e, t):
        if t > 1:
            lhs = model.w[e, model.O[e][0], t-1] - model.w[e, model.O[e][0], t]
            rhs =  grad_neg[e] + \
                   out_min[e][model.O[e][0]] * (1 -y[e, t-1])
            return(lhs <=  rhs)

        else:
            return(po.Constraint.Skip)

    # positive gradient
    if grad_direc == "positive" or grad_direc == "both":
        setattr(model, objs[0].lower_name+"_milp_gradient_pos",
                po.Constraint(uids, model.timesteps, rule=grad_pos_rule))
    # negative gradient
    if grad_direc == "negative" or grad_direc == "both":
        setattr(model, objs[0].lower_name+"_milp_gradient_neg",
                po.Constraint(uids, model.timesteps, rule=grad_neg_rule))


def add_startup_constraints(model, objs=None, uids=None):
    """ Creates constraints to model the start up of a component

    Parameter
    ------------
    model : pyomo.ConcreteModel()
        A pyomo-object to be solved containing all Variables, Constraints, Data
    objs : array like
        list of component objects for which the bounds will be
        altered
    uids : array like
        list of component uids corresponding to the objects

    Returns
    -------

    References
    ----------
    .. [1] M. Steck (2012): "Entwicklung und Bewertung von Algorithmen zur
       Einsatzplanerstelleung virtueller Kraftwerke", PhD-Thesis,
       TU Munich, p.38
    """

    if objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                          which constraints should be set.")
    if uids is None:
        uids = [e.uids for e in objs]

    # create binary start-up variables for objects
    setattr(model, objs[0].lower_name+'_start_var',
            po.Var(uids, model.timesteps, within=po.Binary))

    def start_up_rule(model, e, t):
        if t >= 1:
            try:
                lhs = getattr(model,objs[0].lower_name+'_status_var')[e, t] - \
                       getattr(model,objs[0].lower_name+'_status_var')[e, t-1]
                rhs = getattr(model, objs[0].lower_name+'_start_var')[e, t]
                return(lhs <= rhs)
            except:
                raise AttributeError('Constructing startup constraints for' +
                                     ' component with uid: %s went wrong', e)

        else:
            # TODO: Define correct boundary conditions
            return(po.Constraint.Skip)
    setattr(model, objs[0].lower_name+"_start_up",
            po.Constraint(uids, model.timesteps, rule=start_up_rule))


def add_shutdown_constraints(model, objs=None, uids=None):
    """ Creates constraints to model the shut down of a component

    Parameter
    ------------
    model : pyomo.ConcreteModel()
        A pyomo-object to be solved containing all Variables, Constraints, Data
    objs : array like
        list of component objects for which the bounds will be
        altered
    uids : array like
        list of component uids corresponding to the objects

    Returns
    -------

    References
    ----------
    .. [1] M. Steck (2012): "Entwicklung und Bewertung von Algorithmen zur
       Einsatzplanerstelleung virtueller Kraftwerke", PhD-Thesis,
       TU Munich, p.38
    """

    if objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                          which constraints should be set.")
    if uids is None:
        uids = [e.uids for e in objs]

    # create binary start-up variables for objects
    setattr(model, objs[0].lower_name+'_stop_var',
            po.Var(uids, model.timesteps, within=po.Binary))

    def shutdown_rule(model, e, t):
        if t > 1:
            lhs = getattr(model,objs[0].lower_name+'_status_var')[e, t-1] - \
                  getattr(model,objs[0].lower_name+'_status_var')[e, t] - \
                  getattr(model, objs[0].lower_name+'_stop_var')[e, t]
            rhs = 0
            return(lhs <= rhs)
        else:
            # TODO: Define correct boundary conditions
            return(po.Constraint.Skip)
    setattr(model, objs[0].lower_name+"_shut_down",
            po.Constraint(uids, model.timesteps, rule=shutdown_rule))
