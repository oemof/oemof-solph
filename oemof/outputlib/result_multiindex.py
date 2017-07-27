from collections import UserDict, UserList
from itertools import groupby
from ..solph.network import Storage
from ..solph.options import Investment
import numpy as np
import pandas as pd


def results_to_multiindex(om):
    """ Returns a multi-indexed dataframe of the results of an optimization
    model.
    """
    df = pd.DataFrame(np.random.rand(3, 3))

    print(df)

    return df
