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

    # create data container for scalars and sequences
    container = {'scalars': pd.Series(),
                 'sequences': pd.DataFrame(index=es.timeindex)}

    # create dict with keys (n1, n2) for flows
    results = {(k, v): container for k, v in dict.fromkeys(om.flows)}

    # get unique keys (n1, n1) for nodes
    nodes_source = {(k1, k1): container for k1, k2 in results.keys()
                    if issubclass(type(k1), Node)}

    nodes_target = {(k2, k2): container for k1, k2 in results.keys()
                    if issubclass(type(k2), Node)}

    nodes_source.update(nodes_target)

    # add them to the results
    results.update(nodes_source)

    # print(dir(om.Storage))
    # print(type(om.Storage))
    # print(om.Storage.block_data_objects)
    print('Data (constraints):')


    # # get block of param/variable?
    # components = {v.index()[0]: v.value for v in om.component_data_objects(Var)
    #               if (v.index()[0], v.index()[1]) not in results.keys()}
    # print(components)


    # 1. get all component keys/labels that are not sources, sinks, flows, lts
    # 2. walk through component_data_objects and get data for these keys


        #print(str(v), v.value)
        #print(dir(v))
        #print(v.index()[0])
        #blocks.append(str(v.index()[0]))
        #blocks.append(str(v.parent_block()))

    # get all variables (including their block)
    block_vars = []
    for var in om.component_data_objects(Var):
        block_vars.append(str(var.parent_component()))
    block_vars = list(set(block_vars))

    print(block_vars)

    # get individual indices of specific block

    # get values for single components from block e.g. Storage.capacity
    print(dir(om.Storage.capacity))

    # for scalars
    bla = {i: om.Storage.capacity[i].value for i in om.Storage.capacity._index}

    # dict keys as index value as column
    # -> appending to dataframe/series makes it generically
    #bla = sorted(bla.items())

    print(bla)

    # walk over results[(n, n)] and get all values in bla if key contained

    # TODO: add data blockwise from pyomo model

    # # add data
    # for source, target in om.flows:
    #
    #     # flows
    #     data = [om.flow[source, target, t].value for t in om.TIMESTEPS]
    #     results[(source, target)]['sequences']['value'] = data
    #
    #     # storages
    #     if isinstance(source, Storage):
    #         results[(source, source)] = \
    #             {'sequences': pd.DataFrame(index=es.timeindex)}
    #         if source.investment is None:
    #             data = [om.Storage.capacity[source, t].value
    #                     for t in om.TIMESTEPS]
    #         else:
    #             data = [om.InvestmentStorage.capacity[source, t].value
    #                     for t in om.TIMESTEPS]
    #         results[(source, source)]['sequences']['soc'] = data
    #
    #     # investment
    #     if isinstance(om.flows[source, target].investment, Investment):
    #         results[(source, target)] = \
    #             {'scalars': pd.Series()}
    #         results[(source, target)]['scalars']['investment'] = \
    #             om.InvestmentFlow.invest[source, target].value
    #         if isinstance(source, Storage):
    #             results[(source, source)].update({'scalars': pd.Series()})
    #             results[(source, source)]['scalars']['investment'] = \
    #                 om.InvestmentStorage.invest[source].value

    return results
