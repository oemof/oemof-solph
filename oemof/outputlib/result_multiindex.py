from collections import UserDict, UserList
from itertools import groupby
from ..solph.network import Storage
from ..solph.options import Investment
import numpy as np
import pandas as pd


def results_to_multiindex(es, om):
    """ Returns a multi-indexed dataframe of the results of an optimization
    model.
    """

    rows = []

    for i, o in om.flows:  # .items() ?

        row = dict()
        row['source'] = i
        row['target'] = o
        row['datetime'] = es.timeindex
        row['val'] = [om.flow[i, o, t].value for t in om.TIMESTEPS]

        rows.append(row)

    # split date and value lists to tuples
    tuples = [
        (item['source'], item['target'], date, val)
        for item in rows for date, val
        in zip(item['datetime'], item['val'])
    ]

    # print(rows)
    # print(tuples)

    # create MultiIndex DataFrame
    index = ['source', 'target', 'datetime']
    columns = index + ['val']
    df = pd.DataFrame(tuples, columns=columns)
    df.set_index(index, inplace=True)
    df.sort_index(inplace=True)

    print(df)

    return None
