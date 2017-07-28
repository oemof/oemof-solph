from collections import UserDict, UserList
from itertools import groupby
from ..solph.network import Bus
from ..solph.network import Storage
from ..solph.options import Investment
import pandas as pd


def results_to_multiindex(es, om):
    """
    Returns a multi-indexed dataframe of the results of an optimization model.
    """

    # create empty dict with flow tuples as keys
    results = {(k, v):
               {'scalars': pd.DataFrame(),
                'sequences': pd.DataFrame(index=es.timeindex)}
               for k, v in dict.fromkeys(om.flows)}

    # add data
    for source, target in om.flows:

        # flows (sequences)
        data = [om.flow[source, target, t].value for t in om.TIMESTEPS]
        results[(source, target)]['sequences']['value'] = data

        # storages (sequences)
        if isinstance(source, Storage):
            results[(source, source)] = \
                {'sequences': pd.DataFrame(index=es.timeindex)}
            if source.investment is None:
                data = [om.Storage.capacity[source, t].value
                        for t in om.TIMESTEPS]
            else:
                data = [om.InvestmentStorage.capacity[source, t].value
                        for t in om.TIMESTEPS]
            results[(source, source)]['sequences']['soc'] = data

        # investment (scalars)
        if isinstance(om.flows[source, target].investment, Investment):
            results[(source, target)]['scalars']['investment'] = \
                om.InvestmentFlow.invest[source, target].value
            if isinstance(source, Storage):
                results[(source, source)]['scalars']['investment'] = \
                    om.InvestmentStorage.invest[source].value

        # # buses
        # if hasattr(om, 'dual'):
        #     if isinstance(source, Bus):


    return results
