# -*- coding: utf-8 -*-
"""
Modules for providing convenient views for solph results.

Information about the possible usage is provided within the examples.
"""

from enum import Enum
from itertools import zip_longest
import pandas as pd

from oemof.network import Bus


def convert_keys_to_strings(results):
    """
    Convert the dictionary keys to strings.

    All tuple keys of the result object e.g. results[(pp1, bus1)] are converted
    into strings that represent the object labels e.g. results[('pp1','bus1')].
    """
    converted = {tuple([str(e) for e in k]): v for k, v in results.items()}

    return converted


def node(results, node):
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

    return filtered


class NodeOption(Enum):
    All = 0
    HasOutputs = 1
    HasInputs = 2
    HasOnlyOutputs = 3
    HasOnlyInputs = 4


def get_nodes(results, option=NodeOption.All, exclude_busses=False):
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
