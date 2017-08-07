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


    # get block of param/variable?
    blocks = []
    for v in om.component_data_objects(Var):
        #print(str(v), v.value)

        #print(dir(v))

        print(str(v.index()))

        #blocks.append(str(v.parent_component()))
        #blocks.append(str(v.parent_block()))

    #print(blocks)

    # for obj in om.LinearTransformer.component_data_objects(ctype=Constraint, active=True, sort=True, descend_into=True):
    #     print(obj)
    #     print(dir(obj))
    #     #print(obj.cname())

    # print(om.LinearTransformer.component_data_objects)
    # print(om.Storage.component_data_objects)
    # for var in om.Storage.component_data_objects(ctype=po.Var, active=True,
    #                                              sort=True, descend_into=True):
    #     print(var)

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
