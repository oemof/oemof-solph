# -*- coding: utf-8 -*-
"""
This module hold constraints, expressions, submodels etc that are generic
and can be used inside different blocks to create element inside the model.

"""
from pyomo.environ import (Constraint, SOSConstraint, Var, Set,
                           NonNegativeReals)

def sos_costs(block, nodes=None, sos_type=2):
    """ Creates SOSconstraint for investment costs of investment components.

    Parameters
    -----------
    block : pyomo.core.SimpleBlock()
        A block inside the solph optimization model
    nodes : list
       list of the nodes

    """
    if nodes is None:
        raise ValueError("No nodes provided for sos_costs!")

    block.SOS_Nodes = Set(ordered=True, initialize=nodes)
    # variable to be used in objective expression
    block.SOS_costs = Var(block.SOS_Nodes)
    # create dicts for initialization
    cost_points = {}
    capacity_points = {}
    for n in block.SOS_Nodes:
        cost_points[n] = [i[1] for i in n.investment.ep_costs]
        capacity_points[n] = [i[0] for i in  n.investment.ep_costs]

    def _SOS_indices_init(block, n):
        """ Set for the points for each node
        """
        return [(n, p) for p in range(len(cost_points[n]))]
    block._SOS_indices = Set(block.SOS_Nodes, dimen=2, ordered=True,
                             initialize=_SOS_indices_init)

    # indices for sos2 variable
    def _ub_indices_init(block):
        """ Indices for set of sos2-variable
        """
        return [(n, p) for n in block.SOS_Nodes
                       for p in range(len(cost_points[n]))]
    block._ub_indices = Set(ordered=True, dimen=2, initialize=_ub_indices_init)
    block.sos_var = Var(block._ub_indices, within=NonNegativeReals)

    def _SOS_capacity_rule(model, n):
        """ Forces the variable `ìnvest` to a interpolated value between
        the points of the approximated nonlinear cost-size relationship
        """
        expr =  (block.invest[n] ==
                    sum(block.sos_var[n, p] * capacity_points[n][p]
                        for p in range(len(capacity_points[n])))
            )
        return expr
    block.sos_capacity_constr = Constraint(block.SOS_Nodes,
                                           rule=_SOS_capacity_rule)

    def _SOS_costs_rule(model, n):
        """ Calculates the nonlinear approximated investcost for each
        storage n
        """
        expr = (block.SOS_costs[n] ==
                     sum(block.sos_var[n, p] * cost_points[n][p]
                         for p in range(len(cost_points[n])))
            )
        return expr
    block.nl_costs_constr = Constraint(block.SOS_Nodes,
                                    rule=_SOS_costs_rule)
    def _SOS_var_rule(model, n):
        """ sos constraint that only one segment/point can be selected, i.e.
        two adjacent weights of points must equal 0 if sos=2 or
        """
        return (sum(block.sos_var[n, p]
                for p in range(len(cost_points[n]))) == 1)
    block.sos2_constr = Constraint(block.SOS_Nodes,
                                   rule=_SOS_var_rule)
    block.sos_set_constraint = SOSConstraint(block.SOS_Nodes,
                                             var=block.sos_var,
                                             index=block._SOS_indices,
                                             sos=sos_type)
    return block.SOS_costs