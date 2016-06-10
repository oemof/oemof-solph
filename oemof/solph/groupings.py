# -*- coding: utf-8 -*-
""" list:  Groupings needed on an energy system for it to work with solph.

TODO: Maybe move this to the module docstring? It shoule be somewhere prominent
      so solph user's immediately see that they need to use :const:`GROUPINGS`
      when they want to create an energy system for use with solph.

If you want to use solph on an energy system, you need to create it with these
groupings specified like this:

    .. code-block: python

    from oemof.network import EnergySystem
    import solph

    energy_system = EnergySystem(groupings=solph.GROUPINGS)

"""
from itertools import chain
from oemof.core import energy_system as core_es
from .network import Bus, LinearTransformer, Storage
from .options import Investment
from . import blocks


def constraint_grouping(node):
    if isinstance(node, Bus) and node.balanced:
        return blocks.Bus
    if isinstance(node, LinearTransformer):
        return blocks.LinearTransformer
    if isinstance(node, Storage) and isinstance(node.investment, Investment):
        return blocks.InvestmentStorage
    if isinstance(node, Storage):
        return blocks.Storage


def investment_key(n):
    for f in n.outputs.values():
        if f.investment is not None:
            return blocks.InvestmentFlow


def investment_flows(n):
    return set(chain(((n, t, f) for (t, f) in n.outputs.items()
                      if f.investment is not None),
                     ((s, n, f) for (s, f) in n.inputs.items()
                      if f.investment is not None)))


def merge_investment_flows(n, group):
    return group.union(n)

investment_flow_grouping = core_es.Grouping(
    key=investment_key,
    value=investment_flows,
    merge=merge_investment_flows)


def standard_flow_key(n):
    for f in n.outputs.values():
        if f.investment is None:
            return blocks.Flow


def standard_flows(n):
    return [(n, t, f) for (t, f) in n.outputs.items()
            if f.investment is None]


def merge_standard_flows(n, group):
    group.extend(n)
    return group

standard_flow_grouping = core_es.Grouping(
    key=standard_flow_key,
    value=standard_flows,
    merge=merge_standard_flows)


def discrete_flow_key(n):
    for f in n.outputs.values():
        if f.discrete is not None:
            return blocks.Discrete


def discrete_flows(n):
    return [(n, t, f) for (t, f) in n.outputs.items()
            if f.discrete is not None]


def merge_discrete_flows(n, group):
    group.extend(n)
    return group

discrete_flow_grouping = core_es.Grouping(
    key=discrete_flow_key,
    value=discrete_flows,
    merge=merge_discrete_flows)

GROUPINGS = [constraint_grouping, investment_flow_grouping,
             standard_flow_grouping, discrete_flow_grouping]
