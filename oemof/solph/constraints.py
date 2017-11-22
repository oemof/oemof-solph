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


def equate_variables(om, var1, var2, factor1=1, name=None):
    """

    Parameters
    ----------
    name
    factor1
    var1 : po.Var
        First variable, to be set to equal with Var2 and multiplied with
        factor1.
    var2 : po.Var
        Second variable, to be set equal to (Var1 * factor1).
    factor1 : float
        Factor to define the proportion between the variables.
    name : str
        Optional name for the equation e.g. in the LP file. By default the
        name is: equate + string representation of var1 and var2.
    om : oemof.solph.Model
        Model to which constraints are added.

    Returns
    -------
    om.solph.Model

    """
    if name is None:
        name = '_'.join(["equate", str(var1), str(var2)])

    def connect_invest_rule(m):
        return var1 * factor1 == var2
    setattr(om, name, po.Constraint(rule=connect_invest_rule))

    return om
