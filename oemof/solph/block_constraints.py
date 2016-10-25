# -*- coding: utf-8 -*-
"""
This module hold constraints, expressions, submodels etc that are generic
and can be used inside different blocks to create element inside the model.

"""
from pyomo.environ import (Constraint, SOSConstraint, Var, Set,
                           NonNegativeReals)

def sos2_costs(block, group):
    """ Creates SOSconstraint for investment costs of investment components.

    Parameters
    -----------
    block : pyomo.core.SimpleBlock()
        A block inside the solph optimization model
    group : list
       group of the block (see: :py:mod:`~oemof.solph.blocks` module)

    """
    block.NL_INVESTSTORAGES = Set(ordered=True,
                                  initialize=[n for n in group
                                  if isinstance(n.investment.ep_costs, list)])
    # variable to be used in objective expression
    block.nl_investcosts = Var(block.NL_INVESTSTORAGES)
    # create dicts for initialization
    cost_points = {}
    capacity_points = {}
    for n in block.NL_INVESTSTORAGES:
        cost_points[n] = [i[0] for i in n.investment.ep_costs]
        capacity_points[n] = [i[1] for i in  n.investment.ep_costs]

    def SOS_indices_init(block, n):
        """ Set for the points for each storage
        """
        return [(n, p) for p in range(len(cost_points[n]))]
    block.SOS_indices = Set(block.NL_INVESTSTORAGES, dimen=2, ordered=True,
                           initialize=SOS_indices_init)

    # indices for sos2 variable
    def ub_indices_init(block):
        """ Indices for set of sos2-variable
        """
        return [(n, p) for n in block.NL_INVESTSTORAGES
                       for p in range(len(cost_points[n]))]
    block.ub_indices = Set(ordered=True, dimen=2, initialize=ub_indices_init)
    block.sos2_var = Var(block.ub_indices, within=NonNegativeReals)

    def _nl_capacity_rule(model, n):
        """ Forces the variable `ìnvest` to a interpolated value between
        the points of the approximated nonlinear cost-size relationship
        """
        expr =  (block.invest[n] ==
                    sum(block.sos2_var[n, p] * capacity_points[n][p]
                        for p in range(len(capacity_points[n])))
            )
        return expr
    block.nl_capacity_constr = Constraint(block.NL_INVESTSTORAGES,
                                         rule=_nl_capacity_rule)

    def _nl_costs_rule(model, n):
        """ Calculates the nonlinear approximated investcost for each
        storage n
        """
        expr = (block.nl_investcosts[n] ==
                     sum(block.sos2_var[n, p] * cost_points[n][p]
                         for p in range(len(cost_points[n])))
            )
        return expr
    block.nl_costs_constr = Constraint(block.NL_INVESTSTORAGES,
                                    rule=_nl_costs_rule)
    def _sos2_var_rule(model, n):
        """ sos2 constraint that only one segment can be selected, i.e.
        two adjacent weights of points must equal 0
        """
        return (sum(block.sos2_var[n, p]
                for p in range(len(cost_points[n]))) == 1)
    block.sos2_constr = Constraint(block.NL_INVESTSTORAGES,
                                 rule=_sos2_var_rule)
    block.sos_set_constraint = SOSConstraint(block.NL_INVESTSTORAGES,
                                            var=block.sos2_var,
                                            index=block.SOS_indices, sos=2)
    return block.nl_investcosts