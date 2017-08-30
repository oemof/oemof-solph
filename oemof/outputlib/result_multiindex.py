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

    # # create data container for scalars and sequences
    # container = {'scalars': pd.Series(),
    #              'sequences': pd.DataFrame(index=es.timeindex)}
    #
    # # add it to a result dict with keys (n1, n2) for flows
    # results = {(k, v): container for k, v in dict.fromkeys(om.flows)}
    #
    # # get unique keys (n1, n1) for nodes
    # nodes_source = {(k1, k1): container for k1, k2 in results.keys()
    #                 if issubclass(type(k1), Node)}
    # nodes_target = {(k2, k2): container for k1, k2 in results.keys()
    #                 if issubclass(type(k2), Node)}
    # nodes_source.update(nodes_target)
    #
    # # add them to the result dict
    # results.update(nodes_source)

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
    #df.drop('tuple', axis=1, inplace=True)
    #isinstance(obj, tuple)
    #df['is_tuple'] = df['variable_index'].apply(lambda x: isinstance(x, tuple))
    #df['tup'] = df['tuple'].apply(lambda x: tuple(i for i in x if isinstance(i, tuple)))

    def my_fun(v):
        for i in v:
            if isinstance(i, tuple):
                return i
            elif issubclass(type(i), Node):
                return (i,)
            else:
                pass

    df['tup'] = df['tuple'].map(my_fun)

    print(df.head())
    df.to_csv('bla.csv')

    # from here on split the dataframe component-wise into frames/series
    # which are saved within the result-dict
    # idea: some apply/map function solution combined with grouping per
    #       component that creates a generic structure? in any case vectorized.
    #       the function could also integrate the whole dict creation, etc.

    #return results
