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
from collections import abc

import pandas as pd
from ._plumbing import _FakeSequence
from ._processing import results as new_results
from .helpers import flatten


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
                else str(k) if k is not None else None
            ): v
            for k, v in result.items()
        }
    else:
        converted = {
            tuple(map(str, k)) if isinstance(k, tuple) else str(k): v
            for k, v in result.items()
        }
    return converted


def results(model, remove_last_time_point=False):
    return new_results(
        model=model,
        remove_last_time_point=remove_last_time_point,
    )


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
                    meta_res[k1][k2] = msg.format(
                        type(om.es.results[k1][0][k2])
                    )

    return meta_res


def __separate_attrs(
    system, exclude_attrs, get_flows=False, exclude_none=True
):
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
