# -*- coding: utf-8 -*-

"""Module to collect useful functions for economic calculation.
"""

__copyright__ = "oemof developer group"
__license__ = "GPLv3"

import pandas
from collections import namedtuple
from oemof.outputlib import views


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


LCOE = namedtuple('LCOE', ['invest', 'input_costs', 'output_costs'])


def calculate_lcoe(node, results, cost_results):
    invest = 0.0
    variable_input_costs = 0.0
    variable_output_costs = 0.0
    output = 0.0

    flow_types = views.get_flow_type(node, results)

    # Get total output of node:
    for output_nodes in flow_types['output']:
        invest += cost_results[output_nodes].get('invest', 0.0)
        variable_output_costs += cost_results[output_nodes].get(
            'variable_costs', 0.0)
        output += results[output_nodes]['sequences']['flow'].sum()
    if output == 0.0:
        return LCOE(0.0, 0.0, 0.0)

    # Get total input of node:
    for input_nodes in flow_types['input']:
        invest += cost_results[input_nodes].get('invest', 0.0)
        variable_input_costs += cost_results[input_nodes].get(
            'variable_costs', 0.0)

    # Get total invest of node:
    for single_nodes in flow_types['single']:
        invest += cost_results[single_nodes].get('invest', 0.0)

    return LCOE(
        *map(
            lambda x: x / output,
            [invest, variable_input_costs, variable_output_costs]
        )
    )
