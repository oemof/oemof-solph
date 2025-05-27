# -*- coding: utf-8 -*-

"""Compatibility wrapper of solph.Results for providing solph results in the
structure of the output of old processing.results(model).

SPDX-FileCopyrightText: Patrik Schönfeldt <patrik.schoenfeldt@dlr.de>

SPDX-License-Identifier: MIT
"""

import pandas as pd
import warnings

from oemof.tools import debugging

from ._models import Model
from ._results import Results


def results(
    model: Model,
    remove_last_time_point: bool = False,
    scalar_data: list[str] | None = None,
    sequence_data: list[str] | None = None,
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
    In these models, investments are sequential data,
    but with a second time imdex. As this is a compatibility layer,
    we did not add support for this new feature.
    Instead, use of the Results object is advised.

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
    scalar_data :  list[str]
        List of variables to be treated as scalar data (see above).
    sequence_data: list[str]
        List of variables to be treated as sequential data (see above).
    """

    meta_result_keys = ["Solution", "Problem", "Solver"]

    if scalar_data is None:
        scalar_data = ["invest", "total"]
    if sequence_data is None:
        sequence_data = ["flow", "storage_content", "storage_losses"]

    result_dict = {}
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", category=debugging.ExperimentalFeatureWarning
        )
        result_object = Results(model)

    timeindex = model.es.timeindex

    if remove_last_time_point:
        timeindex = timeindex[:-1]

    def _handle_scalar(data):
        return data.iloc[0]

    def _handle_sequence(data):
        return data

    for result_key in result_object.keys():
        if result_key not in meta_result_keys:
            if result_key in scalar_data:
                result_type = "scalars"
                data_handler = _handle_scalar
            elif result_key in sequence_data:
                result_type = "sequences"
                data_handler = _handle_sequence
            else:
                warnings.warn(f"Unhandled data: {result_key}")
                continue

            index = result_object[result_key].columns
            for item in index:
                if isinstance(index, pd.MultiIndex):
                    node_tuple = item
                else:
                    node_tuple = (item, None)
                if node_tuple not in result_dict:
                    result_dict[node_tuple] = {
                        "scalars": pd.Series(),
                        "sequences": pd.DataFrame(index=timeindex),
                    }

                data = result_object[result_key][item]
                result_dict[node_tuple][result_type][result_key] = (
                    data_handler(data)
                )

    return result_dict
