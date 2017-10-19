# -*- coding: utf-8 -*-

import pyomo.environ as po


def emission_limit(om, flows=None, limit=None):
    """
    Parameters
    ----------
    om : OperationModel
        Model to which constraints are added.
    flows : dict
        Dictionary holding the flows that should be considered in constraint.
        Keys are (source, target) objects of the Flow.
    limit : numeric
        Absolute emission limit.

    Note
    ----
    Flow objects required an emission attribute!

    """

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
