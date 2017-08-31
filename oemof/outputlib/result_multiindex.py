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

    # get all pyomo variables including their block
    block_vars = []
    for bv in om.component_data_objects(Var):
        block_vars.append(bv.parent_component())
    block_vars = list(set(block_vars))

    # write them into a dict with tuples as keys
    dc = {(str(bv).split('.')[0], str(bv).split('.')[-1], i): bv[i].value
          for bv in block_vars for i in getattr(bv, '_index')}

    # use this to create a pandas dataframe
    df = pd.DataFrame(list(dc.items()), columns=['pyomo_tuple', 'value'])
    df['variable_name'] = df['pyomo_tuple'].str[1]

    def get_tuple(v):
        for i in v:
            if isinstance(i, tuple):
                return i
            elif issubclass(type(i), Node):
                return (i,)
            else:
                pass

    df['oemof_tuple'] = df['pyomo_tuple'].map(get_tuple)

    def get_timestep(v):
        if all(issubclass(type(x), Node) for x in v):
            return 0
        else:
            return v[-1]

    df['timestep'] = df['oemof_tuple'].map(get_timestep)

    def remove_timestep(v):
        if all(issubclass(type(x), Node) for x in v):
            return v
        else:
            return v[:-1]

    df['oemof_tuple'] = df['oemof_tuple'].map(remove_timestep)

    df.sort_values(['oemof_tuple', 'timestep'], ascending=[True, True],
                   inplace=True)

    results = {k: v[['timestep', 'variable_name', 'value']]
               for k, v in df.groupby('oemof_tuple')}

    my_dc = {}
    for k, v in results.items():
        results[k].set_index('timestep', inplace=True)
        results[k] = results[k].pivot(columns='variable_name', values='value')
        results[k].index = es.timeindex
        scalars = results[k].loc[:, results[k].isnull().any()].dropna().iloc[0]
        sequences = results[k].loc[:, ~(results[k].isnull().any())]
        my_dc[k] = {'scalars': scalars, 'sequences': sequences}

    return my_dc
