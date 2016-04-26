# -*- coding: utf-8 -*-
"""
The module contains linear mixed integer constraints.

@author: Simon Hilpert (simon.hilpert@fh-flensburg.de)
"""
import pyomo.environ as po
import pandas as pd

def set_bounds(model, block, side="output"):
    """ Set upper and lower bounds via constraints.

    The bounds are set with constraints using the binary status variable
    of the components. The mathematical formulation is as follows:

    If side is `output`:

    .. math::  w_{e, o_{e,1}}(t) \\leq \\overline{W}_{e, o_{e,1}} \\cdot y_e(t), \
    \\qquad \\forall e, \\forall t

    .. math::  w_{e, o_{e,1}}(t) \\geq \\underline{W}_{e, o_{e,1}} \\cdot y_e(t), \
    \\qquad \\forall e, \\forall t

    If side is `input`:

    .. math::  w_{i_e, e}(t) \\leq \\overline{W}_{i_e, e} \\cdot y_e(t), \
    \\qquad \\forall e, \\forall t

    .. math:: w_{i_e, e}(t) \\geq \\underline{W}_{i_e, e} \\cdot y_e(t), \
    \\qquad \\forall e, \\forall t


    Parameters
    ----------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data.
        Bounds are altered at model attributes (variables) of `model`
    block : SimpleBlock()
         block to group all constraints and variables etc., block corresponds
         to one oemof base class
    side : string
       string to select on which side the bounds should be set
       (`ìnput`, `output`)


    """
    if block.objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                         which bounds should be set.")
    if side == "output":
        out_max = {obj.uid: obj.out_max for obj in block.objs}

        # set upper bounds
        def output_ub_rule(block, e, t):
            lhs = model.w[e, model.O[e][0], t]
            rhs = block.y[e, t] * out_max[e][0]
            return(lhs <= rhs)
        block.maximum_output = po.Constraint(block.indexset,
                                             rule=output_ub_rule)

        out_min = {obj.uid: obj.out_min for obj in block.objs}
        # set lower bounds
        def output_lb_rule(block, e, t):
            lhs = block.y[e, t] * out_min[e][0]
            rhs = model.w[e, model.O[e][0], t]
            return(lhs <= rhs)
        block.minimum_output = po.Constraint(block.indexset,
                                             rule=output_lb_rule)

    if side == "input":
        in_max = {obj.uid: obj.in_max for obj in block.objs}

        # set upper bounds
        def input_ub_rule(block, e, t):
            lhs = model.w[model.I[e][0], e, t]
            rhs = block.y[e, t] * in_max[e][0]
            return(lhs <= rhs)
        block.maximum_input = po.Constraint(block.indexset, rule=input_ub_rule)

        in_min = {obj.uid: obj.in_min for obj in block.objs}
        # set lower bounds
        def input_lb_rule(block, e, t):
            lhs = block.y[e, t] * in_min[e][0]
            rhs = model.w[model.I[e][0], e, t]
            return(lhs <= rhs)
        block.minimum_input = po.Constraint(block.indexset, rule=input_lb_rule)

def add_variable_linear_eta_relation(model, block):
    """ Adds constraint for input-output relation for all
    units with variable efficiency grouped in `block.objs`.

    The mathematical formulation for the constraint is as follows:

    .. math:: w_{i_e, e}(t) = y_e(t) \\cdot c_1 + c_2 \\cdot w_{e, o_{e,1}}(t), \
    \\qquad \\forall e, \\forall t


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

    c = {obj.uid: obj.coeff for obj in block.objs}

    def variable_linear_eta_rule(block, e, t):
        lhs = model.w[model.I[e][0], e, t]
        rhs = block.y[e,t]*c[e][0] + c[e][1] * model.w[e, model.O[e][0], t]
        return(lhs == rhs)
    block.variable_linear_eta_relation = po.Constraint(block.indexset,
                                            rule=variable_linear_eta_rule,
                                            doc="INFLOW = Y*c1 + c2*OUTFLOW_1")

def add_output_gradient_constraints(model, block, grad_direc="both"):
    """ Creates constraints to model the output gradient for milp-models.

    If gradient direction is `positive`:

    .. math:: w_{e,o_{e,1}}(t) - w_{e,o_{e,1}}(t-1) \\leq \\overline{G}^{pos}_{e_{o,1}} + \
    \\underline{W}_{e, o_{e,1}} \\cdot (1 - y_e(t))

    If gradient direction is `negative`:

    .. math:: w_{e,o_{e,1}}(t-1) - w_{e,o_{e,1}}(t) \\leq \\overline{G}^{neg}_{e_{o,1}} + \
    \\underline{W}_{e, o_{e,1}} \\cdot (1 - y_{e}(t-1))


    Parameters
    ----------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data.
    block : SimpleBlock()
         block to group all constraints and variables etc., block corresponds
         to one oemof base class
    grad_direc : string
         direction of gradient ("both", "positive", "negative")

    References
    ----------
    .. [1] M. Steck (2012): "Entwicklung und Bewertung von Algorithmen zur
       Einsatzplanerstelleung virtueller Kraftwerke", PhD-Thesis,
       TU Munich, p.38
    """
    if block.objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                          which bounds should be set.")

    out_min = {obj.uid: obj.out_min for obj in block.objs}
    grad_pos = {obj.uid: obj.grad_pos for obj in block.objs}

    # TODO: Define correct boundary conditions for t-1 of time
    def grad_pos_rule(block, e, t):
        if t > 1:
            return(model.w[e, model.O[e][0], t] - \
               model.w[e, model.O[e][0], t-1] <=  \
               grad_pos[e] + out_min[e][0] * (1 -block.y[e, t]))
        else:
            return(po.Constraint.Skip)

    grad_neg = {obj.uid: obj.grad_neg for obj in block.objs}
    # TODO: Define correct boundary conditions for t-1 of time horizon
    def grad_neg_rule(block, e, t):
        if t > 1:
            lhs = model.w[e, model.O[e][0], t-1] - model.w[e, model.O[e][0], t]
            rhs =  grad_neg[e] + \
                   out_min[e][0] * (1 -block.y[e, t-1])
            return(lhs <=  rhs)

        else:
            return(po.Constraint.Skip)

    # positive gradient
    if grad_direc == "positive" or grad_direc == "both":
        block.milp_gradient_pos = po.Constraint(block.indexset,
                                                rule=grad_pos_rule)
    # negative gradient
    if grad_direc == "negative" or grad_direc == "both":
        block.milp_gradient_neg = po.Constraint(block.indexset,
                                                rule=grad_neg_rule)


def add_startup_constraints(model, block):
    """ Creates constraints to model the start up of a components.

    The mathematical formulation of constraint is as follows:

    .. math::  y_e(t) - y_e(t-1) \\leq z^{start}_e(t), \\qquad \
        \\forall e, \\forall t

    Parameters
    ----------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data.
    block : SimpleBlock()
        block to group all constraints and variables etc., block corresponds
        to one oemof base class

    """

    if block.objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                          which constraints should be set.")

    # create binary start-up variables for objects
    block.z_start = po.Var(block.uids, model.timesteps, within=po.Binary)

    def start_up_rule(model, e, t):
        if t >= 1:
            try:
                lhs = block.y[e, t] - block.y[e, t-1] - block.z_start[e, t]
                rhs = 0
                return(lhs <= rhs)
            except:
                raise AttributeError('Constructing startup constraints for' +
                                     ' component with uid: %s went wrong', e)
        else:
            # TODO: Define correct boundary conditions
            return(po.Constraint.Skip)
    block.start_up = po.Constraint(block.indexset, rule=start_up_rule)


def add_shutdown_constraints(model, block):
    """ Creates constraints to model the shut down of a component.

    The mathematical formulation for the constraint is as follows:

    .. math::  y_e(t-1) - y_e(t) \\leq z^{stop}_e(t), \\qquad \
    \\forall e, \\forall t


    Parameters
    ----------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data.
    block : SimpleBlock()
         block to group all constraints and variables etc., block corresponds
         to one oemof base class

    """

    if block.objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                          which constraints should be set.")

    # create binary start-up variables for objects
    block.z_stop = po.Var(block.uids, model.timesteps, within=po.Binary)

    def shutdown_rule(block, e, t):
        if t > 1:
            lhs = block.y[e, t-1] - block.y[e, t] - block.z_stop[e, t]
            rhs = 0
            return(lhs <= rhs)
        else:
            # TODO: Define correct boundary conditions
            return(po.Constraint.Skip)
    block.shut_down = po.Constraint(block.indexset, rule=shutdown_rule)

def add_minimum_downtime(model, block):
    """ Adds minimum downtime constraints for for components grouped inside
    `block.objs`.

    The mathematical formulation for constraints is as follows:

     .. math::  (y_e(t-1)-y_e(t)) \\cdot T^{min,off}_e \\leq T^{min,off}_e - \
     \\sum_{\\gamma=0}^{T^{min,off}_e-1} y_e(t+\\gamma)  \
     \\qquad \\forall e, \\forall t \\in [2, t_{max}-t_{min,off}]

    Extra constraints for last timesteps:

    .. math::  (y_e(t-1)-y_e(t)) \\cdot T^{min,off}_e \\leq T^{min,off}_e - \
     \\sum_{\\gamma=0}^{t_{max}-t} y_e(t+\\gamma)  \
     \\qquad \\forall e, \\forall t \\in [t_{max}-t_{min,off}, t_{max}]


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
                          'which minimum downtime constraints should be set.')

    t_min_off = {obj.uid: obj.t_min_off for obj in block.objs}
    t_max = len(model.timesteps)-1

    def minimum_downtime_rule(block, e, t):
        if t <= 1:
            return po.Constraint.Skip
        elif t >= t_max - t_min_off[e]:
            # Adaption for border sections with range(timesteps_max-t)
            lhs = (block.y[e, t-1] - block.y[e, t]) * t_min_off[e]
            rhs = t_min_off[e] - sum(block.y[e, t + p]
                                     for p in range(t_max - t))
            return(lhs <= rhs)
        else:
            lhs = (block.y[e, t-1] - block.y[e, t]) * t_min_off[e]
            rhs = t_min_off[e] - sum(block.y[e, t + p]
                                     for p in range(t_min_off[e]))
            return(lhs <= rhs)
    block.minimum_downtime = po.Constraint(block.indexset,
                                           rule=minimum_downtime_rule)


def add_minimum_uptime(model, block):
    """ Adds minimum uptime constraints for for components in `block`

    The mathematical formulation for constraints is as follows:

     .. math::  (y_e(t) - y_e(t-1)) \\cdot T^{min,on}_e \\leq  \
     \\sum_{\\gamma=0}^{T^{min,on}_e-1} y_e(t+\\gamma)  \
     \\qquad \\forall e, \\forall t \\in [2, t_{max}-t_{min,on}]

     Extra constraint for the last timesteps:

     .. math::  (y_e(t) - y_e(t-1)) \\cdot T^{min,on}_e \\leq  \
      \\sum_{\\gamma=0}^{t_{max}-t} y_e(t+\\gamma)  \
      \\qquad \\forall e, \\forall t \\in [t_{max}-t_{min,on}, t_{max}]


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
                          'which minimum uptime constraints should be set.')

    t_min_on = {obj.uid: obj.t_min_on for obj in block.objs}
    t_max = len(model.timesteps)-1

    def minimum_uptime_rule(block, e, t):
        if t <= 1:
            return po.Constraint.Skip
        elif t >= t_max - t_min_on[e]:
            # Adaption for border sections with range(timesteps_max-t)
            lhs = (block.y[e, t] - block.y[e, t-1]) * t_min_on[e]
            rhs = sum(block.y[e, t + p] for p in range(t_max - t))
            return(lhs <= rhs)
        else:
            lhs = (block.y[e, t] - block.y[e, t-1]) * t_min_on[e]
            rhs = sum(block.y[e, t + p] for p in range(t_min_on[e]))
            return(lhs <= rhs)
    block.minimum_uptime = po.Constraint(block.indexset,
                                          rule=minimum_uptime_rule)

def maximum_starts_per_period(model, block, period=24):
    """

    Parameters
    ----------
    model : OptimizationModel() instance
        An object to be solved containing all Variables, Constraints, Data.
        Bounds are altered at model attributes (variables) of `model`
    block : SimpleBlock()
         block to group all constraints and variables etc., block corresponds
         to one oemof base class
    period : array like
       length of period

    """
    if not hasattr(block, 'z_start'):
        raise ValueError("Can not add maximum starts per period. \
                         Please add startup constraints!")

    if block.objs is None:
        raise ValueError("No objects defined. Please specify objects for \
                         which bounds should be set.")

    df = pd.DataFrame()
    for t in model.timesteps:
        if t >= period:
            df[t-period] = range(t-period,t)

    max_starts = {obj.uid: obj.max_starts for obj in block.objs}

    def max_start_rule(block, e, t):
        if max_starts[e] >= len(model.timesteps):
            return po.Constraint.Skip
        elif (t <= len(model.timesteps)-period-1):

            return sum(block.z_start[e, d] for d in df[t]) <= max_starts[e]
        else:
            return po.Constraint.Skip
    block.max_starts = po.Constraint(block.indexset, rule=max_start_rule)
