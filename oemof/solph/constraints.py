# -*- coding: utf-8 -*-

import pyomo.environ as po


def emission_limit(om, flows=None, limit=None):
    """
    Parameters
    ----------
    om : oemof.solph.Model
        Model to which constraints are added.
    flows : dict
        Dictionary holding the flows that should be considered in constraint.
        Keys are (source, target) objects of the Flow. If no dictionary is given
        all flows containing the 'emission' attribute will be used.
    limit : numeric
        Absolute emission limit.

    Note
    ----
    Flow objects required an emission attribute!

    """

    if flows is None:
        flows = {}
        for (i, o) in om.flows:
            if hasattr(om.flows[i, o], 'emission'):
                flows[(i, o)] = om.flows[i, o]

    else:
        for (i, o) in flows:
            if not hasattr(flows[i, o], 'emission'):
                raise ValueError(('Flow with source: {0} and target: {1} '
                                 'has no attribute emission.').format(i.label,
                                                                      o.label))

    def emission_rule(m):
        """
        """
        return (sum(m.flow[i, o, t] * flows[i, o].emission
                for (i, o) in flows
                for t in m.TIMESTEPS) <= limit)

    om.emission_limit = po.Constraint(rule=emission_rule)

    return om


def connect_investment_variables(om, invest):

    iset = set(n for n in range(len(invest) - 1))

    def connect_invest_rule(m, n):
        return invest[n][0] * invest[n][1] == invest[n+1][0] * invest[n+1][1]

    om.invest_connect_cnstr = po.Constraint(iset, rule=connect_invest_rule)

    return om
