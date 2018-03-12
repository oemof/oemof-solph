# -*- coding: utf-8 -*-

"""Modules for providing convenient views for solph results.

Information about the possible usage is provided within the examples.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/outputlib/views.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

import pandas as pd
from enum import Enum
from oemof.outputlib.processing import convert_keys_to_strings


def node(results, node, multiindex=False):
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

        if multiindex:
            idx = pd.MultiIndex.from_tuples(
                [tuple([row[0][0], row[0][1], row[1]])
                 for row in filtered['scalars'].index])
            idx.set_names(['from', 'to', 'type'], inplace=True)
            filtered['scalars'].index = idx

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

        if multiindex:
            idx = pd.MultiIndex.from_tuples(
                [tuple([col[0][0], col[0][1], col[1]])
                 for col in filtered['sequences'].columns])
            idx.set_names(['from', 'to', 'type'], inplace=True)
            filtered['sequences'].columns = idx

    return filtered


class NodeOption(str, Enum):
    All = 'all'
    HasOutputs = 'has_outputs'
    HasInputs = 'has_inputs'
    HasOnlyOutputs = 'has_only_outputs'
    HasOnlyInputs = 'has_only_inputs'


def filter_nodes(results, option=NodeOption.All, exclude_busses=False):
    """
    Get set of nodes from results-dict for given node option

    This function filters nodes from results for special needs. At the moment,
    following options are available:
        * NodeOption.All/'all':
            Returns all nodes
        * NodeOption.HasOutputs/'has_outputs':
            Returns nodes with an output flow (eg. Transformer, Source)
        * NodeOption.HasInputs/'has_inputs':
            Returns nodes with an input flow (eg. Transformer, Sink)
        * NodeOption.HasOnlyOutputs/'has_only_outputs':
            Returns nodes having only output flows (eg. Source)
        * NodeOption.HasOnlyInputs/'has_only_inputs':
            Returns nodes having only input flows (eg. Sink)
    Additionally, busses can be excluded setting 'exclude_busses' to True.

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
    node_from, node_to = map(lambda x: set(x) - {None}, zip(*results))
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
        return {n for n in nodes if not n.__class__.__name__ == 'Bus'}
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
