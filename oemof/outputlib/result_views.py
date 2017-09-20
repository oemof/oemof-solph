# -*- coding: utf-8 -*-
"""
Modules for providing convenient views for solph results.

Information about the possible usage is provided within the examples.
"""

import pandas as pd


def node_results(results, node):
    """
    Obtain results for a single node e.g. a Bus or Component.

    Results are written into a dictionary which is keyed by 'scalars' and
    'sequences' holding respective data in a pandas Series and DataFrame.
    """
    filtered = {}

    # create a series with tuples as index labels for scalars
    scalars = {k: v['scalars'] for k, v in results.items()
               if node in k and not (v['scalars'].empty)}
    tuples = [str(tup) for tup in scalars.keys()]
    filtered['scalars'] = pd.concat(scalars.values(), axis=0)
    filtered['scalars'].index = zip(tuples, filtered['scalars'].index)
    filtered['scalars'].sort_index(axis=0, inplace=True)

    # create a dataframe with tuples as column labels for sequences
    sequences = {k: v['sequences'] for k, v in results.items()
                 if node in k and not (v['sequences'].empty)}
    tuples = [str(tup) for tup in sequences.keys()]
    filtered['sequences'] = pd.concat(sequences.values(), axis=1)
    filtered['sequences'].columns = zip(tuples, filtered['sequences'].columns)
    filtered['sequences'].sort_index(axis=1, inplace=True)

    return filtered
