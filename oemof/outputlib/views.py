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


class FlowType(str, Enum):
    """
    Gives information on flow type
    """
    Single = 'single'
    Input = 'input'
    Output = 'output'


def get_flow_type(node, results):
    """
    Categorize results keys by flow type (Single, Input, Output)

    Parameters
    ----------
    node: Node
        Node of interest
    results: dict
        Results dict with tuple of nodes as key
        (i.e. results, param_results, cost_results)
    Returns
    -------
    dict: FlowType as key and tuple of nodes as value
    """
    flow_types = {ft: [] for ft in FlowType}
    for nodes in results:
        if (
                nodes[0] == node and
                (nodes[1] is None or nodes[1] == 'None')
        ):
            flow_types[FlowType.Single].append(nodes)
        elif nodes[1] == node:
            flow_types[FlowType.Input].append(nodes)
        elif nodes[0] == node:
            flow_types[FlowType.Output].append(nodes)
    return flow_types
