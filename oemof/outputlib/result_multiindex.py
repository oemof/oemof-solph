from collections import UserDict, UserList
from itertools import groupby
from ..solph.network import Bus
from ..solph.network import Storage
from ..solph.options import Investment
from oemof.network import Node
import pandas as pd
from pyomo.core.base.var import _VarData, Var
from pyomo.core.base.constraint import Constraint


def results_to_multiindex(es, om):
    """
    Returns a multi-indexed dataframe of the results of an optimization model.
    """

    # get all variables including their block
    block_vars = []
    for bv in om.component_data_objects(Var):
        block_vars.append(bv.parent_component())
    block_vars = list(set(block_vars))

    # write them into a dict with tuple keys (block_name, var_name, var_index)
    dc = {(str(bv).split('.')[0], str(bv).split('.')[-1], i): bv[i].value
          for bv in block_vars for i in getattr(bv, '_index')}

    # create a pandas dataframe
    df = pd.DataFrame(list(dc.items()), columns=['tuple', 'value'])
    df['block_name'] = df['tuple'].str[0]
    df['variable_name'] = df['tuple'].str[1]
    df['variable_index'] = df['tuple'].str[2]

    def get_tuple(v):
        for i in v:
            if isinstance(i, tuple):
                return i
            elif issubclass(type(i), Node):
                return (i,)
            else:
                pass

    df['tuples'] = df['tuple'].map(get_tuple)

    def get_timestep(v):
        if all(issubclass(type(x), Node) for x in v):
            return 0
        else:
            return v[-1]

    df['timestep'] = df['tuples'].map(get_timestep)

    def remove_timestep(v):
        if all(issubclass(type(x), Node) for x in v):
            return v
        else:
            return v[:-1]

    df['tuples'] = df['tuples'].map(remove_timestep)

    df.sort_values(['tuples', 'timestep'], ascending=[True, True],
                   inplace=True)

    #print(df.head())
    #df.to_csv('df.csv')

    dfs = {k: v[['timestep', 'variable_name', 'value']]
           for k, v in df.groupby('tuples')}

    for k, v in dfs.items():
        v.set_index('timestep', inplace=True)
        v = v.pivot(columns='variable_name', values='value')
        v.index = es.timeindex
        v.to_csv(str(k) + '.csv')
        print(k, v.head())

    #return results
