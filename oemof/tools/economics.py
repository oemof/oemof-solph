# -*- coding: utf-8 -*-

"""Module to collect useful functions for economic calculation.
"""

__copyright__ = "oemof developer group"
__license__ = "GPLv3"

import pandas
from collections import namedtuple


def annuity(capex, n, wacc):
    """Calculate the annuity.

    annuity = capex * (wacc * (1 + wacc) ** n) / ((1 + wacc) ** n - 1)

    Parameters
    ----------
    capex : float
        Capital expenditure (NPV of investment)
    n : int
        Number of years that the investment is used (economic lifetime)
    wacc : float
        Weighted average cost of capital

    Returns
    -------
    float : annuity

    """
    return capex * (wacc * (1 + wacc) ** n) / ((1 + wacc) ** n - 1)


Costs = namedtuple('Costs', ['name', 'flow_key', 'param_key'])
AttributeKey = namedtuple('CostKey', ['dimension', 'name'])
DEFAULT_COSTS = [
    Costs(
        'invest',
        AttributeKey('scalars', 'invest'),
        AttributeKey('scalars', 'investment_ep_costs')
    ),
    Costs(
        'variable_costs',
        AttributeKey('sequences', 'flow'),
        AttributeKey('sequences', 'variable_costs')
    ),
]


def cost_results(results, param_results, costs=DEFAULT_COSTS):
    def get_value(component, key):
        dimension = component.get(key.dimension)
        if dimension is None:
            return None
        value = dimension.get(key.name)
        if value is None:
            return None
        if key.dimension == 'sequences':
            if value[0] is None:
                return None
            value = pandas.Series(value.data)
            value.reset_index(drop=True, inplace=True)
        return value

    cost_data = {}
    for nodes, attributes in param_results.items():
        cost_data[nodes] = {}

        result = results.get(nodes)
        if result is None:
            continue

        for cost in costs:
            flow_value = get_value(result, cost.flow_key)
            if flow_value is None:
                continue
            param_value = get_value(attributes, cost.param_key)
            if param_value is None:
                continue
            cost_value = flow_value * param_value
            if isinstance(cost_value, pandas.Series):
                cost_value = cost_value.sum()
            cost_data[nodes][cost.name] = cost_value

    return cost_data
