
import pandas
from collections import namedtuple
from oemof.outputlib import views
from oemof.tools.economics import lcoe


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
    """
    Calculate costs for all node tuples in param_results

    Different costs can be calculated, by default DEFAULT_COSTS are calculated.
    Costs are calculated by multiplying node parameters from param_results
    dictionary with flows from results dictionary.

    Parameters
    ----------
    results: dict
        from `oemof.processing.results`
    param_results: dict
        from `oemof.processing.param_results`
    costs: list-of-Costs (optional)
        Costs to be calculated; by default DEFAULT_COSTS are calculated

    Returns
    -------
    dict:
        For each node tuple from param_results, calculated costs are returned
        as dict containing cost name as key and cost result as value.
    """
    def get_value(component, key):
        """
        Searches component for key

        Returns component[key.dimension][key.name] if given.
        If dimension is "sequences" pandas.Series is returned.

        Parameters
        ----------
        component: dict
            Parameters from param_results[nodes]
        key: AttributeKey
            AttributeKey with dimension and key name to search

        Returns
        -------
        value/pandas.Series:
            Returns component[key.dimension][key.name]. If dimension
            "sequences" is given, value is turned into pandas.Series first.
            If key is not found, None is returned.
        """
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


def calculate_lcoe(node, results, cost_results):
    """
    Returns LCOE for given node

    Calculates LCOE (see `oemof.tools.economics.lcoe`) from results and
    cost_results for given node.

    Parameters
    ----------
    node: Node
        Node to calculated LCOE for
    results: dict
        Results dict from `oemof.outputlib.processing.results`
    cost_results: dict
        Cost results dict from `oemof.tools.economics.cost_results`

    Returns
    -------
    collections.namedtuple:
        from oemof.tools.economics.LCOE
    """
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

    # Get total input of node:
    for input_nodes in flow_types['input']:
        invest += cost_results[input_nodes].get('invest', 0.0)
        variable_input_costs += cost_results[input_nodes].get(
            'variable_costs', 0.0)

    # Get total invest of node:
    for single_nodes in flow_types['single']:
        invest += cost_results[single_nodes].get('invest', 0.0)

    return lcoe(output, invest, variable_output_costs, variable_input_costs)