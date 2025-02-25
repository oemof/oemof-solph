# -*- coding: utf-8 -*-

"""Modules for providing a convenient data structure for solph results.

Information about the possible usage is provided within the examples.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: henhuy
SPDX-FileCopyrightText: Johannes Kochems
SPDX-FileCopyrightText: Patrik Schönfeldt <patrik.schoenfeldt@dlr.de>

SPDX-License-Identifier: MIT

"""

import numbers
import sys
from collections import abc, namedtuple
from itertools import groupby
from typing import Iterable, Optional

import numpy as np
import pandas as pd
from oemof.network.network import Entity, Node
from pyomo.core.base.piecewise import IndexedPiecewise
from pyomo.core.base.set import OrderedScalarSet
from pyomo.core.base.var import Var

from ._plumbing import _FakeSequence
from .helpers import flatten


def get_tuple(x):
    """Get oemof tuple within iterable or create it

    Tuples from Pyomo are of type `(n, n, int)`, `(n, n)` and `(n, int)`.
    For single nodes `n` a tuple with one object `(n,)` is created.
    """
    for i in x:
        if isinstance(i, tuple):
            return i
        elif issubclass(type(i), Entity):
            return (i,)

    # for standalone variables, x is used as identifying tuple
    if isinstance(x, tuple):
        return x


def get_timestep(x):
    """Get the timestep from oemof tuples

    The timestep from tuples `(n, n, int)`, `(n, n)`, `(n, int)` and (n,)
    is fetched as the last element. For time-independent data (scalars)
    zero ist returned.
    """
    if all(issubclass(type(n), Entity) for n in x):
        return 0
    else:
        return x[-1]


def remove_timestep(x):
    """Remove the timestep from oemof tuples

    The timestep is removed from tuples of type `(n, n, int)` and `(n, int)`.
    """
    if all(issubclass(type(n), Entity) for n in x):
        return x
    else:
        return x[:-1]


def create_dataframe(om):
    """Create a result DataFrame with all optimization data

    Results from Pyomo are written into one common pandas.DataFrame where
    separate columns are created for the variable index e.g. for tuples
    of the flows and components or the timesteps.
    """
    # get all pyomo variables including their block
    block_vars = list(
        set([bv.parent_component() for bv in om.component_data_objects(Var)])
    )
    var_dict = {}
    for bv in block_vars:
        # Drop the auxiliary variables introduced by pyomo's Piecewise
        parent_component = bv.parent_block().parent_component()
        if not isinstance(parent_component, IndexedPiecewise):
            try:
                idx_set = getattr(bv, "_index_set")
            except AttributeError:
                # To make it compatible with Pyomo < 6.4.1
                idx_set = getattr(bv, "_index")

            for i in idx_set:
                key = (str(bv).split(".")[0], str(bv).split(".")[-1], i)
                value = bv[i].value
                var_dict[key] = value

    # use this to create a pandas dataframe
    df = pd.DataFrame(list(var_dict.items()), columns=["pyomo_tuple", "value"])
    df["variable_name"] = df["pyomo_tuple"].str[1]

    # adapt the dataframe by separating tuple data into columns depending
    # on which dimension the variable/parameter has (scalar/sequence).
    # columns for the oemof tuple and timestep are created
    df["oemof_tuple"] = df["pyomo_tuple"].map(get_tuple)
    df = df[df["oemof_tuple"].map(lambda x: x is not None)]
    df["timestep"] = df["oemof_tuple"].map(get_timestep)
    df["oemof_tuple"] = df["oemof_tuple"].map(remove_timestep)

    # Use another call of remove timestep to get rid of period not needed
    df.loc[df["variable_name"] == "flow", "oemof_tuple"] = df.loc[
        df["variable_name"] == "flow", "oemof_tuple"
    ].map(remove_timestep)

    # order the data by oemof tuple and timestep
    df = df.sort_values(["oemof_tuple", "timestep"], ascending=[True, True])

    # drop empty decision variables
    df = df.dropna(subset=["value"])

    return df


def divide_scalars_sequences(df_dict, k):
    """Split results into scalars and sequences results

    Parameters
    ----------
    df_dict: dict
        dict of pd.DataFrames, keyed by oemof tuples
    k: tuple
        oemof tuple for results processing
    """
    try:
        condition = df_dict[k][:-1].isnull().any()
        scalars = df_dict[k].loc[:, condition].dropna().iloc[0]
        sequences = df_dict[k].loc[:, ~condition]
        return {"scalars": scalars, "sequences": sequences}
    except IndexError:
        error_message = (
            "Cannot access index on result data. "
            + "Did the optimization terminate"
            + " without errors?"
        )
        raise IndexError(error_message)


def set_result_index(df_dict, k, result_index):
    """Define index for results

    Parameters
    ----------
    df_dict: dict
        dict of pd.DataFrames, keyed by oemof tuples
    k: tuple
        oemof tuple for results processing
    result_index: pd.Index
        Index to use for results
    """
    try:
        df_dict[k].index = result_index
    except ValueError:
        try:
            df_dict[k] = df_dict[k][:-1]
            df_dict[k].index = result_index
        except ValueError as e:
            msg = (
                "\nFlow: {0}-{1}. This could be caused by NaN-values "
                "in your input data."
            )
            raise type(e)(str(e) + msg.format(k[0].label, k[1].label)).with_traceback(
                sys.exc_info()[2]
            )


def set_sequences_index(df, result_index):
    try:
        df.index = result_index
    except ValueError:
        try:
            df = df[:-1]
            df.index = result_index
        except ValueError:
            raise ValueError("Results extraction failed!")


def results(model, remove_last_time_point=False):
    """Create a nested result dictionary from the result DataFrame

    The already rearranged results from Pyomo from the result DataFrame are
    transferred into a nested dictionary of pandas objects.
    The first level key of that dictionary is a node (denoting the respective
    flow or component).

    The second level keys are "sequences" and "scalars" for a *standard model*:

    * A pd.DataFrame holds all results that are time-dependent, i.e. given as
      a sequence and can be indexed with the energy system's timeindex.
    * A pd.Series holds all scalar values which are applicable for timestep 0
      (i.e. investments).

    For a *multi-period model*, the second level key for "sequences" remains
    the same while instead of "scalars", the key "period_scalars" is used:

    * For sequences, see standard model.
    * Instead of a pd.Series, a pd.DataFrame holds scalar values indexed
      by periods. These hold investment-related variables.

    Examples
    --------
    * *Standard model*: `results[idx]['scalars']`
      and flows `results[n, n]['sequences']`.
    * *Multi-period model*: `results[idx]['period_scalars']`
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
    # Extraction steps that are the same for both model types
    df = create_dataframe(model)

    # create a dict of dataframes keyed by oemof tuples
    df_dict = {
        k if len(k) > 1 else (k[0], None): v[["timestep", "variable_name", "value"]]
        for k, v in df.groupby("oemof_tuple")
    }

    # Define index
    if model.es.timeindex is None:
        result_index = list(range(len(model.es.timeincrement) + 1))
    else:
        result_index = model.es.timeindex

    # create final result dictionary by splitting up the dataframes in the
    # dataframe dict into a series for scalar data and dataframe for sequences
    result = {}

    # Standard model results extraction
    if model.es.periods is None:
        result = _extract_standard_model_result(
            df_dict, result, result_index, remove_last_time_point
        )
        scalars_col = "scalars"

    # Results extraction for a multi-period model
    else:
        period_indexed = ["invest", "total", "old", "old_end", "old_exo"]

        result = _extract_multi_period_model_result(
            model,
            df_dict,
            period_indexed,
            result,
            result_index,
            remove_last_time_point,
        )
        scalars_col = "period_scalars"

    # add dual variables for bus constraints
    if model.dual is not None:
        grouped = groupby(sorted(model.BusBlock.balance.iterkeys()), lambda t: t[0])
        for bus, timestep in grouped:
            duals = [model.dual[model.BusBlock.balance[bus, t]] for _, t in timestep]
            if model.es.periods is None:
                df = pd.DataFrame({"duals": duals}, index=result_index[:-1])
            # TODO: Align with standard model
            else:
                df = pd.DataFrame({"duals": duals}, index=result_index)
            if (bus, None) not in result.keys():
                result[(bus, None)] = {
                    "sequences": df,
                    scalars_col: pd.Series(dtype=float),
                }
            else:
                result[(bus, None)]["sequences"]["duals"] = duals

    return result


def _extract_standard_model_result(
    df_dict, result, result_index, remove_last_time_point
):
    """Extract and return the results of a standard model

    * Optionally remove last time point or include it elsewise.
    * Set index to timeindex and pivot results such that values are displayed
      for the respective variables. Reindex with the energy system's timeindex.
    * Filter for columns with nan values to retrieve scalar variables. Split
      up the DataFrame into sequences and scalars and return it.

    Parameters
    ----------
    df_dict : dict
        dictionary of results DataFrames
    result : dict
        dictionary to store the results
    result_index : pd.DatetimeIndex
        timeindex to use for the results (derived from EnergySystem)
    remove_last_time_point : bool
        if True, remove the last time point

    Returns
    -------
    result : dict
        dictionary with results stored
    """
    if remove_last_time_point:
        # The values of intervals belong to the time at the beginning of the
        # interval.
        for k in df_dict:
            df_dict[k].set_index("timestep", inplace=True)
            df_dict[k] = df_dict[k].pivot(columns="variable_name", values="value")
            set_result_index(df_dict, k, result_index[:-1])
            result[k] = divide_scalars_sequences(df_dict, k)
    else:
        for k in df_dict:
            df_dict[k].set_index("timestep", inplace=True)
            df_dict[k] = df_dict[k].pivot(columns="variable_name", values="value")
            # Add empty row with nan at the end of the table by adding 1 to the
            # last value of the numeric index.
            df_dict[k].loc[df_dict[k].index[-1] + 1, :] = np.nan
            set_result_index(df_dict, k, result_index)
            result[k] = divide_scalars_sequences(df_dict, k)

    return result


def _extract_multi_period_model_result(
    model,
    df_dict,
    period_indexed=None,
    result=None,
    result_index=None,
    remove_last_time_point=False,
):
    """Extract and return the results of a multi-period model

    Difference to standard model is in the way, scalar values are extracted
    since they now depend on periods.

    Parameters
    ----------
    model : oemof.solph.models.Model
        The optimization model
    df_dict : dict
        dictionary of results DataFrames
    period_indexed : list
        list of variables that are indexed by periods
    result : dict
        dictionary to store the results
    result_index : pd.DatetimeIndex
        timeindex to use for the results (derived from EnergySystem)
    remove_last_time_point : bool
        if True, remove the last time point

    Returns
    -------
    result : dict
        dictionary with results stored
    """
    for k in df_dict:
        df_dict[k].set_index("timestep", inplace=True)
        df_dict[k] = df_dict[k].pivot(columns="variable_name", values="value")
        # Split data set
        period_cols = [col for col in df_dict[k].columns if col in period_indexed]
        # map periods to their start years for displaying period results
        d = {
            key: val + model.es.periods[0].min().year
            for key, val in enumerate(model.es.periods_years)
        }
        period_scalars = df_dict[k].loc[:, period_cols].dropna()
        sequences = df_dict[k].loc[
            :, [col for col in df_dict[k].columns if col not in period_cols]
        ]
        if remove_last_time_point:
            set_sequences_index(sequences, result_index[:-1])
        else:
            set_sequences_index(sequences, result_index)
        if period_scalars.empty:
            period_scalars = pd.DataFrame(index=d.values())
        try:
            period_scalars.rename(index=d, inplace=True)
            period_scalars.index.name = "period"
            result[k] = {
                "period_scalars": period_scalars,
                "sequences": sequences,
            }
        except IndexError:
            error_message = (
                "Some indices seem to be not matching.\n"
                "Cannot properly extract model results."
            )
            raise IndexError(error_message)

    return result


def convert_keys_to_strings(result, keep_none_type=False):
    """
    Convert the dictionary keys to strings.

    All (tuple) keys of the result object e.g. results[(pp1, bus1)] are
    converted into strings that represent the object labels
    e.g. results[('pp1','bus1')].
    """
    if keep_none_type:
        converted = {
            (
                tuple([str(e) if e is not None else None for e in k])
                if isinstance(k, tuple)
                else str(k)
                if k is not None
                else None
            ): v
            for k, v in result.items()
        }
    else:
        converted = {
            tuple(map(str, k)) if isinstance(k, tuple) else str(k): v
            for k, v in result.items()
        }
    return converted


def meta_results(om, undefined=False):
    """
    Fetch some metadata from the Solver. Feel free to add more keys.

    Valid keys of the resulting dictionary are: 'objective', 'problem',
    'solver'.

    om : oemof.solph.Model
        A solved Model.
    undefined : bool
        By default (False) only defined keys can be found in the dictionary.
        Set to True to get also the undefined keys.

    Returns
    -------
    dict
    """
    meta_res = {"objective": om.objective()}

    for k1 in ["Problem", "Solver"]:
        k1 = k1.lower()
        meta_res[k1] = {}
        for k2, v2 in om.es.results[k1][0].items():
            try:
                if str(om.es.results[k1][0][k2]) == "<undefined>":
                    if undefined:
                        meta_res[k1][k2] = str(om.es.results[k1][0][k2])
                else:
                    meta_res[k1][k2] = om.es.results[k1][0][k2]
            except TypeError:
                if undefined:
                    msg = "Cannot fetch meta results of type {0}"
                    meta_res[k1][k2] = msg.format(type(om.es.results[k1][0][k2]))

    return meta_res


def __separate_attrs(system, exclude_attrs, get_flows=False, exclude_none=True):
    """
    Create a dictionary with flow scalars and series.

    The dictionary is structured with flows as tuples and nested dictionaries
    holding the scalars and series e.g.
    {(node1, node2): {'scalars': {'attr1': scalar, 'attr2': 'text'},
    'sequences': {'attr1': iterable, 'attr2': iterable}}}

    system:
        A solved oemof.solph.Model or oemof.solph.Energysystem
    exclude_attrs: List[str]
        List of additional attributes which shall be excluded from
        parameter dict
    get_flows: bool
        Whether to include flow values or not
    exclude_none: bool
        If set, scalars and sequences containing None values are excluded

    Returns
    -------
    dict
    """

    def detect_scalars_and_sequences(com):
        scalars = {}
        sequences = {}

        default_exclusions = [
            "__",
            "_",
            "registry",
            "inputs",
            "outputs",
            "Label",
            "input",
            "output",
            "constraint_group",
        ]
        # Must be tuple in order to work with `str.startswith()`:
        exclusions = tuple(default_exclusions + exclude_attrs)
        attrs = [
            i
            for i in dir(com)
            if not (i.startswith(exclusions) or callable(getattr(com, i)))
        ]

        for a in attrs:
            attr_value = getattr(com, a)

            # Iterate trough investment and add scalars and sequences with
            # "investment" prefix to component data:
            if attr_value.__class__.__name__ == "Investment":
                invest_data = detect_scalars_and_sequences(attr_value)
                scalars.update(
                    {
                        "investment_" + str(k): v
                        for k, v in invest_data["scalars"].items()
                    }
                )
                sequences.update(
                    {
                        "investment_" + str(k): v
                        for k, v in invest_data["sequences"].items()
                    }
                )
                continue

            if isinstance(attr_value, str):
                scalars[a] = attr_value
                continue

            # If the label is a tuple it is iterable, therefore it should be
            # converted to a string. Otherwise, it will be a sequence.
            if a == "label":
                attr_value = str(attr_value)

            if isinstance(attr_value, abc.Iterable):
                sequences[a] = attr_value
            elif isinstance(attr_value, _FakeSequence):
                scalars[a] = attr_value.value
            else:
                scalars[a] = attr_value

        sequences = flatten(sequences)

        com_data = {
            "scalars": scalars,
            "sequences": sequences,
        }
        move_undetected_scalars(com_data)
        if exclude_none:
            remove_nones(com_data)

        com_data = {
            "scalars": pd.Series(com_data["scalars"]),
            "sequences": pd.DataFrame(com_data["sequences"]),
        }
        return com_data

    def move_undetected_scalars(com):
        for ckey, value in list(com["sequences"].items()):
            if isinstance(value, (str, numbers.Number)):
                com["scalars"][ckey] = value
                del com["sequences"][ckey]
            elif isinstance(value, _FakeSequence):
                com["scalars"][ckey] = value.value
                del com["sequences"][ckey]
            elif len(value) == 0:
                del com["sequences"][ckey]

    def remove_nones(com):
        for ckey, value in list(com["scalars"].items()):
            if value is None:
                del com["scalars"][ckey]
        for ckey, value in list(com["sequences"].items()):
            if len(value) == 0 or value[0] is None:
                del com["sequences"][ckey]

    # Check if system is es or om:
    if system.__class__.__name__ == "EnergySystem":
        components = system.flows() if get_flows else system.nodes
    else:
        components = system.flows if get_flows else system.es.nodes

    data = {}
    for com_key in components:
        component = components[com_key] if get_flows else com_key
        component_data = detect_scalars_and_sequences(component)
        comkey = com_key if get_flows else (com_key, None)
        data[comkey] = component_data
    return data


def parameter_as_dict(system, exclude_none=True, exclude_attrs=None):
    """
    Create a result dictionary containing node parameters.

    Results are written into a dictionary of pandas objects where
    a Series holds all scalar values and a dataframe all sequences for nodes
    and flows.
    The dictionary is keyed by flows (n, n) and nodes (n, None), e.g.
    `parameter[(n, n)]['sequences']` or `parameter[(n, n)]['scalars']`.

    Parameters
    ----------
    system: energy_system.EnergySystem
        A populated energy system.
    exclude_none: bool
        If True, all scalars and sequences containing None values are excluded
    exclude_attrs: Optional[List[str]]
        Optional list of additional attributes which shall be excluded from
        parameter dict

    Returns
    -------
    dict: Parameters for all nodes and flows
    """

    if exclude_attrs is None:
        exclude_attrs = []

    flow_data = __separate_attrs(
        system, exclude_attrs, get_flows=True, exclude_none=exclude_none
    )
    node_data = __separate_attrs(
        system, exclude_attrs, get_flows=False, exclude_none=exclude_none
    )

    flow_data.update(node_data)
    return flow_data


SolphResults = namedtuple(
    typename="SolphResults",
    field_names=["flows", "states", "invest", "other_timeindexed", "not_timeindexed"],
)


def _concat_and_pivot(
    dfs: Iterable[pd.DataFrame],
    index: list[str],
    columns: Optional[list[str]] = None,
):
    """Concatenate DataFrames and pivot the result."""
    if len(dfs) > 0:
        if columns is not None:
            return pd.concat(dfs).pivot(index=index, columns=columns, values="value")
        else:
            # We have only the value column
            return pd.concat(dfs).set_index(keys=index)
    else:
        # No DataFrames to concatenate, return an empty one
        return pd.DataFrame()


def is_component_index(idx: OrderedScalarSet) -> bool:
    return idx.dimen == 1 and isinstance(idx.first(), Node)


def is_flow_index(idx: OrderedScalarSet) -> bool:
    return idx.dimen == 2 and all(map(lambda x: isinstance(x, Node), idx.first()))


def process_results(om):
    """
    Get results from solved model.
    """
    # Lists of variable blocks
    _flow = []
    _state = []
    _invest = []

    _other_timeindexed = {}
    _not_timeindexed = []

    # Get variable blocks from solved model
    blocks = set([bv.parent_component() for bv in om.component_data_objects(Var)])

    for var_block in blocks:
        _idx, values = zip(*var_block.extract_values().items())
        indices = np.array(_idx)

        block = pd.DataFrame(
            index=range(len(indices)),
            data={"value": values, "variable": var_block.getname()},
        )

        match tuple(var_block.index_set().subsets()):
            case (om.FLOWS, om.TIMESTEPS):
                # This is the flow block
                block[["from", "to", "timesteps"]] = indices

                _flow.append(block)
            case (idx, om.TIMEPOINTS) if is_component_index(idx):
                # This is a block of component state variables at timepoints
                block[["component", "timepoints"]] = indices

                _state.append(block)
            case (idx, om.PERIODS) if is_component_index(idx) or is_flow_index(idx):
                # This block is period indexed, i.e. an invest block
                xs, ts = np.split(indices, [-1], axis=1)
                if idx.dimen == 1:
                    xs = np.reshape(xs, (len(xs),))
                elif idx.dimen == 2:
                    xs = np.array(map(tuple, xs))

                block[["component"]] = xs
                block[["periods"]] = ts

                _invest.append(block)
            case (
                *_,
                (om.TIMESTEPS | om.TIMEPOINTS | om.PERIODS) as t_idx,
            ):
                # These are some other time indexed variables
                # Split indices into generic identifier and time index
                xs, ts = np.split(indices, [-t_idx.dimen], axis=1)

                block["identifier"] = list(map(tuple, xs))

                t_idx_name = str(t_idx).lower()
                block[t_idx_name] = ts

                _other_timeindexed[t_idx_name].append(block)
            case _:
                # These are variables which are not time indexed
                block["identifier"] = indices

                _not_timeindexed.append(block)

    return SolphResults(
        flows=_concat_and_pivot(
            _flow,
            index="timesteps",
            columns=["from", "to"],
        ),
        states=_concat_and_pivot(
            _state,
            index="timepoints",
            columns=["component", "variable"],
        ),
        invest=_concat_and_pivot(
            _invest,
            index="periods",
            columns=["component", "variable"],
        ),
        other_timeindexed={
            index: _concat_and_pivot(
                _other_timeindexed[index],
                index=index,
                columns=["identifier", "variable"],
            )
            for index in _other_timeindexed
        },
        not_timeindexed=_concat_and_pivot(
            _not_timeindexed, index=["variable", "identifier"]
        ),
    )


def extract_results(timeindex: Optional[str], var_names: Optional[list[str]], om):
    # Get variable blocks from solved model
    blocks = set([bv.parent_component() for bv in om.component_data_objects(Var)])
    _resdfs = []
    for var_block in blocks:
        if not var_block.getname() in var_names:
            # this block is not in focus
            continue

        _idx, values = zip(*var_block.extract_values().items())
        indices = np.array(_idx)
        *_, t_idx = var_block.index_set().subsets()

        if not t_idx == getattr(om, timeindex):
            # not correct time index
            continue

        block = pd.DataFrame(
            index=range(len(indices)),
            data={"value": values, "variable": var_block.getname()},
        )

        # timeindex hinzufügen
        # sonstige identifier in block packen
        # in liste packen

    return _concat_and_pivot(_resdfs, ...)


extract_flows = partial(extract_results, index_structure=("flows", "timesteps"))
extract_states = partial(extract_results, index_structure=("compoment", "timepoints"))
