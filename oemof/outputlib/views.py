# -*- coding: utf-8 -*-
"""
Modules for providing convenient views for solph results.

Information about the possible usage is provided within the examples.
"""

from enum import Enum
from itertools import zip_longest
import pandas as pd
from collections import namedtuple

from oemof.network import Bus


# NodeFlow contains oemof.network.Flow or oemof.network.Node component and
# related FlowType (see below):
NodeFlow = namedtuple('NodeFlow', ['component', 'type'])


class FlowType(str, Enum):
    """
    Gives information on flow type
    """
    Single = 'single'
    Input = 'input'
    Output = 'output'


def convert_keys_to_strings(results):
    """
    Convert the dictionary keys to strings.

    All tuple keys of the result object e.g. results[(pp1, bus1)] are converted
    into strings that represent the object labels e.g. results[('pp1','bus1')].
    """
    converted = {tuple([str(e) for e in k]): v for k, v in results.items()}

    return converted


def node(results, node, get_flows=False):
    """
    Obtain results for a single node e.g. a Bus or Component.

    Either a node or its label string can be passed.
    Results are written into a dictionary which is keyed by 'scalars' and
    'sequences' holding respective data in a pandas Series and DataFrame.
    """
    # convert to keys if only a string is passed
    if type(node) is str:
        results = convert_keys_to_strings(results)

    filtered = {}

    # create a series with tuples as index labels for scalars
    scalars = {k: v['scalars'] for k, v in results.items()
               if node in k and not v['scalars'].empty}
    if scalars:
        # aggregate data
        filtered['scalars'] = pd.concat(scalars.values(), axis=0)
        # assign index values
        idx = {k: [c for c in v['scalars'].index]
               for k, v in results.items()
               if node in k and not v['scalars'].empty}
        idx = [tuple((k, m) for m in v) for k, v in idx.items()]
        idx = [i for sublist in idx for i in sublist]
        filtered['scalars'].index = idx
        filtered['scalars'].sort_index(axis=0, inplace=True)

    # create a dataframe with tuples as column labels for sequences
    sequences = {k: v['sequences'] for k, v in results.items()
                 if node in k and not v['sequences'].empty}
    if sequences:
        # aggregate data
        filtered['sequences'] = pd.concat(sequences.values(), axis=1)
        # assign column names
        cols = {k: [c for c in v['sequences'].columns]
                for k, v in results.items()
                if node in k and not v['sequences'].empty}
        cols = [tuple((k, m) for m in v) for k, v in cols.items()]
        cols = [c for sublist in cols for c in sublist]
        filtered['sequences'].columns = cols
        filtered['sequences'].sort_index(axis=1, inplace=True)

    if get_flows:
        filtered['flows'] = flows(results, node)

    return filtered


def flows(results, current_node, flow_type=None):
    nodes_list = [
        k
        for k, v in results.items()
        if current_node in k and not v['sequences'].empty
    ]
    flow_dict = {}
    for nodes in nodes_list:
        flow = __get_flow_component(nodes, current_node)
        if flow_type is None:
            flow_dict[nodes] = flow
        elif flow.type == flow_type:
            flow_dict[nodes] = flow.component
    return flow_dict


class NodeOption(Enum):
    All = 0
    HasOutputs = 1
    HasInputs = 2
    HasOnlyOutputs = 3
    HasOnlyInputs = 4


def filter_nodes(results, option=NodeOption.All, exclude_busses=False):
    """
    Get set of nodes from results-dict for given node option

    See NodeOption for all options. This function filters nodes from results
    for special needs.

    Parameters
    ----------
    results: dict
    option: NodeOption
    exclude_busses: bool
        If set all bus nodes are excluded from resulting node set

    Returns
    -------
    :obj:'set' of Node
    """
    node_from, node_to = map(
        lambda x: set(x) - {None},
        zip_longest(*list(results))
    )
    if option == NodeOption.All:
        nodes = node_from.union(node_to)
    elif option == NodeOption.HasOutputs:
        nodes = node_from
    elif option == NodeOption.HasInputs:
        nodes = node_to
    elif option == NodeOption.HasOnlyOutputs:
        nodes = node_from - node_to
    elif option == NodeOption.HasOnlyInputs:
        nodes = node_to - node_from
    else:
        raise ValueError('Invalid node option "' + str(option) + '"')

    if exclude_busses:
        return {n for n in nodes if not isinstance(n, Bus)}
    else:
        return nodes


def get_node_by_name(results, *names):
    """
    Searches results for nodes

    Names are looked up in nodes from results and either returned single node
    (in case only one name is given) or as list of nodes. If name is not found,
    None is returned.
    """
    nodes = filter_nodes(results)
    if len(names) == 1:
        return next(filter(lambda x: str(x) == names[0], nodes), None)
    else:
        node_names = {str(n): n for n in nodes}
        return [node_names.get(n, None) for n in names]


def __get_flow_component(nodes, current_node):
    """
    Returns input or output flow of node-tuple if two-dimensional
    tuple is given, otherwise node itself s returned. Additionally, flow type
    of result is returned.
    """
    if nodes[1] is None:
        return NodeFlow(nodes[0], FlowType.Single)
    elif nodes[0] == current_node:
        return NodeFlow(current_node.outputs[nodes[1]], FlowType.Output)
    else:
        return NodeFlow(current_node.inputs[nodes[0]], FlowType.Input)
