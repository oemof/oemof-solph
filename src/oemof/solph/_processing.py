# -*- coding: utf-8 -*-

"""Compatibility wrapper of solph.Results for providing solph results in the
structure of the output of old processing.results(model).

SPDX-FileCopyrightText: Patrik Schönfeldt <patrik.schoenfeldt@dlr.de>

SPDX-License-Identifier: MIT
"""

import pandas as pd

from ._models import Model
from ._results import Results


def results(
    model: Model,
    remove_last_time_point: bool = False,
    scalars: list[str] | None = None,
    sequences: list[str] | None = None,
):
    """Create a nested result dictionary from the result DataFrame

    The results from Pyomo from the Results object are
    transferred into a nested dictionary of pandas objects.
    The first level key of that dictionary is a node
    (denoting the respective flow or component).

    The second level keys are "sequences" and "scalars":

    * A pd.DataFrame holds all results that are time-dependent, i.e. given as
      a sequence and can be indexed with the energy system's timeindex.
    * A pd.Series holds all scalar values which are applicable for timestep 0
      (i.e. investments).

    Models with more than one time for investments are not supported.

    Examples
    --------
    * *Standard model*: `results[idx]['scalars']`
      and flows `results[n, n]['sequences']`.

    Parameters
    ----------
    model : oemof.solph.Model
        A solved oemof.solph model.
    remove_last_time_point : bool
        The last time point of all TIMEPOINT variables is removed to get the
        same length as the TIMESTEP (interval) variables without getting
        nan-values. By default, the last time point is removed if it has not
        been defined by the user in the EnergySystem but inferred. If all
        time points have been defined explicitly by the user the last time
        point will not be removed by default. In that case all interval
        variables will get one row with nan-values to have the same index
        for all variables.
    """

    meta_result_keys = ["Solution", "Problem", "Solver"]

    if scalars is None:
        scalars = ["invest", "total"]
    if sequences is None:
        sequences = ["flow", "storage_content", "storage_losses"]

    sorting = {
        scalar_data: "scalars" for scalar_data in scalars
    } | {
        sequence_data: "sequences" for sequence_data in sequences
    }

    result_dict = {}
    result_object = Results(model)

    for result_key in result_object.keys():
        if result_key not in meta_result_keys:
            index = result_object[result_key].columns
            for item in index:
                if isinstance(index, pd.MultiIndex):
                    node_tuple = item
                else:
                    node_tuple = (item, None)
                if item not in result_dict:
                    result_dict[node_tuple] = {"scalars": {}, "sequences": {}}

                result_dict[node_tuple][sorting[result_key]][result_key] = (
                    result_object[result_key][item]
                )

    return result_dict
