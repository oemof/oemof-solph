from collections import UserDict, UserList
from itertools import groupby
from ..solph.network import Storage
from ..solph.options import Investment
import numpy as np
import pandas as pd
import itertools


def results_to_multiindex(es, om):
    """
    Returns a multi-indexed dataframe of the results of an optimization model.
    """

    # create dataframe
    tuples = [(l, s, n) for l, s in om.flows for n in es.timeindex]
    levels = ['source', 'target', 'datetime']
    df = pd.DataFrame(tuples, columns=levels)

    # add columns
    df['value'] = [om.flow[i, o, t].value
                   for i, o in om.flows for t in om.TIMESTEPS]
    df['value2'] = [om.flow[i, o, t].value + 2
                    for i, o in om.flows for t in om.TIMESTEPS]

    # set multi-index
    df.set_index(levels, inplace=True)
    df.sort_index(inplace=True)

    return print(df)
