# -*- coding: utf-8 -*-
"""
Modules for providing a convenient data structure for solph results.

Information about the possible usage is provided within the examples.
"""

import pandas as pd
from oemof.network import Node
from pyomo.core.base.var import Var


def get_tuple(x):
    """
    Get oemof tuple within iterable or create it.

    Tuples from Pyomo are of type `(n, n, int)`, `(n, n)` and `(n, int)`.
    For single nodes `n` a tuple with one object `(n,)` is created.
    """
    for i in x:
        if isinstance(i, tuple):
            return i
        elif issubclass(type(i), Node):
            return (i,)
        else:
            pass


def get_timestep(x):
    """
    Get the timestep from oemof tuples.

    The timestep from tuples `(n, n, int)`, `(n, n)`, `(n, int)` and (n,)
    is fetched as the last element. For time-independent data (scalars)
    zero ist returned.
    """
    if all(issubclass(type(n), Node) for n in x):
        return 0
    else:
        return x[-1]


def remove_timestep(x):
    """
    Remove the timestep from oemof tuples.

    The timestep is removed from tuples of type `(n, n, int)` and `(n, int)`.
    """
    if all(issubclass(type(n), Node) for n in x):
        return x
    else:
        return x[:-1]


def results_to_df(es, om):
    """
    Create a result dataframe with all optimization data.

    Results from Pyomo are written into pandas DataFrame where separate columns
    are created for the variable index e.g. for tuples of the flows and
    components or the timesteps.
    """
    # get all pyomo variables including their block
    block_vars = []
    for bv in om.component_data_objects(Var):
        block_vars.append(bv.parent_component())
    block_vars = list(set(block_vars))

    # write them into a dict with tuples as keys
    var_dict = {(str(bv).split('.')[0], str(bv).split('.')[-1], i): bv[i].value
                for bv in block_vars for i in getattr(bv, '_index')}

    # use this to create a pandas dataframe
    df = pd.DataFrame(list(var_dict.items()), columns=['pyomo_tuple', 'value'])
    df['variable_name'] = df['pyomo_tuple'].str[1]

    # adapt the dataframe by separating tuple data into columns depending
    # on which dimension the variable/parameter has (scalar/sequence).
    # columns for the oemof tuple and timestep are created
    df['oemof_tuple'] = df['pyomo_tuple'].map(get_tuple)
    df['timestep'] = df['oemof_tuple'].map(get_timestep)
    df['oemof_tuple'] = df['oemof_tuple'].map(remove_timestep)

    # order the data by oemof tuple and timestep
    df = df.sort_values(['oemof_tuple', 'timestep'], ascending=[True, True])

    return df


def results_to_dict(es, om):
    """
    Create a result dictionary from the result DataFrame.

    Results from Pyomo are written into a dictionary of pandas objects where
    a Series holds all scalar values and a dataframe all sequences for nodes
    and flows.
    The dictionary is keyed by the nodes e.g. `results[(n,)]['scalars']`
    and flows e.g. `results[(n,n)]['sequences']`.
    """
    df = results_to_df(es, om)

    # create a dict of dataframes keyed by oemof tuples
    df_dict = {k: v[['timestep', 'variable_name', 'value']]
               for k, v in df.groupby('oemof_tuple')}

    # create final result dictionary by splitting up the dataframes in the
    # dataframe dict into a series for scalar data and dataframe for sequences
    results = {}
    for k, v in df_dict.items():
        df_dict[k].set_index('timestep', inplace=True)
        df_dict[k] = df_dict[k].pivot(columns='variable_name', values='value')
        df_dict[k].index = es.timeindex
        scalars = df_dict[k].loc[:, df_dict[k].isnull().any()].dropna().iloc[0]
        sequences = df_dict[k].loc[:, ~(df_dict[k].isnull().any())]
        results[k] = {'scalars': scalars, 'sequences': sequences}

    return results


def node_results(results, node):
    """
    Obtain results for a single node e.g. a Bus or Component.

    Results are written into a dictionary which is keyed by 'scalars' and
    'sequences' holding respective data in a pandas Series and DataFrame.
    """
    filtered = {}

    # create a DataFrame with tuples as column labels for sequences
    sequences = {k: v['sequences'] for k, v in results.items() if node in k}
    tuples = ['(%s)' % ', '.join([j.label for j in i])
              for i in sequences.keys()]
    filtered['sequences'] = pd.concat(sequences.values(), axis=1)
    filtered['sequences'].columns = zip(tuples, filtered['sequences'].columns)
    filtered['sequences'].sort_index(axis=1, inplace=True)

    # create a Series with tuples as index labels for scalars
    scalars = {k: v['scalars'] for k, v in results.items() if node in k}
    tuples = ['(%s)' % ', '.join([j.label for j in i])
              for i in scalars.keys()]
    filtered['scalars'] = pd.concat(scalars.values(), axis=0)
    filtered['scalars'].index = zip(tuples, filtered['scalars'].index)
    filtered['scalars'].sort_index(axis=0, inplace=True)

    return filtered
