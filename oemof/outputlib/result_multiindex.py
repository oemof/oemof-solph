from collections import UserDict, UserList
from itertools import groupby
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

    # add data for sequences
    for source, target in om.flows:

        # flows
        data = [om.flow[source, target, t].value for t in om.TIMESTEPS]
        results[(source, target)]['sequences']['value'] = data

        # storages
        if isinstance(source, Storage):
            if source.investment is None:
                data = [om.Storage.capacity[source, t].value
                        for t in om.TIMESTEPS]
            else:
                data = [om.InvestmentStorage.capacity[source, t].value
                        for t in om.TIMESTEPS]
            results[(source, source)] = data
            print('Hallo', results[(source, source)])
            #['sequences']['soc'] = data

    return results
