# -*- coding: utf-8 -*-
"""
Modules for providing convenient views for solph results.

Information about the possible usage is provided within the examples.
"""
import itertools
import pandas as pd


def keys_as_strings(results):
    """
    Convert the dictionary keys to strings.

    All tuple keys of the result object e.g. results[(pp1, bus1)] are converted
    into strings that represent the object labels e.g. results[('pp1','bus1')].
    """
    results = {tuple([str(e) for e in k]): v for k, v in results.items()}

    return results


def node_results(results, node):
    """
    Obtain results for a single node e.g. a Bus or Component.

    Either a node or its label string can be passed.
    Results are written into a dictionary which is keyed by 'scalars' and
    'sequences' holding respective data in a pandas Series and DataFrame.
    """
    # convert to keys if only a string is passed
    if type(node) is str:
        results = keys_as_strings(results)

    # check if also multiple nodes can be passed to slice for flows

    filtered = {}

    # create a series with tuples as index labels for scalars
    scalars = {k: v['scalars'] for k, v in results.items()
               if node in k and not (v['scalars'].empty)}
    filtered['scalars'] = pd.concat(scalars.values(), axis=0)

    # assign index values
    idx = {k: [c for c in v['scalars'].index] for k, v in results.items()
           if node in k and not (v['scalars'].empty)}
    idx = [tuple((k, m) for m in v) for k, v in idx.items()]
    idx = [i for sublist in idx for i in sublist]
    filtered['scalars'].index = idx
    filtered['scalars'].sort_index(axis=0, inplace=True)

    # create a dataframe with tuples as column labels for sequences
    sequences = {k: v['sequences'] for k, v in results.items()
                 if node in k and not (v['sequences'].empty)}
    filtered['sequences'] = pd.concat(sequences.values(), axis=1)

    # assign column names
    cols = {k: [c for c in v['sequences'].columns] for k, v in results.items()
            if node in k and not (v['sequences'].empty)}
    cols = [tuple((k, m) for m in v) for k, v in cols.items()]
    cols = [c for sublist in cols for c in sublist]
    filtered['sequences'].columns = cols
    filtered['sequences'].sort_index(axis=1, inplace=True)

    return filtered
