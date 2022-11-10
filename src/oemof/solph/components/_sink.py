# -*- coding: utf-8 -*-

"""
solph version of oemof.network.Sink

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler

SPDX-License-Identifier: MIT

"""

from oemof.network import network as on

from oemof.solph._helpers import check_node_object_for_missing_attribute


class Sink(on.Sink):
    """A component which is designed for one input flow.

    Parameters
    ----------
    label : str
        String holding the label of the Sink object.
        The label of each object must be unique.

    Examples
    --------
    Defining a Sink:

    >>> from oemof import solph
    >>> bel = solph.buses.Bus(label='electricity')

    >>> electricity_export = solph.components.Sink(
    ...    label='el_export',
    ...    inputs={bel: solph.flows.Flow()})

    >>> type(electricity_export)
    <class 'oemof.solph.components._sink.Sink'>

    >>> str(electricity_export.inputs())
    ['electricity']

    Notes
    -----
    It is theoretically possible to use the Sink object with multiple outputs.
    However, we strongly recommend using multiple Sink objects instead.
    """
    def __init__(self, label=None, inputs=None, **kwargs):
        if inputs is None:
            inputs = {}

        super().__init__(label=label, inputs=inputs, **kwargs)
        check_node_object_for_missing_attribute(self, "inputs")

    def constraint_group(self):
        pass
