# -*- coding: utf-8 -*-

"""
A Node that is not meant to have any outflows

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: Johannes Kochems

SPDX-License-Identifier: MIT

"""

from oemof.solph._node import Node


class Sink(Node):
    """A component which is designed for one input flow.

    Parameters
    ----------
    label : str or tuple
        String holding the label of the Sink object.
        The label of each object must be unique.
    inputs: dict
        A dictionary mapping input nodes to corresponding inflows
        (i.e. input values).

    Examples
    --------
    Defining a Sink:

    >>> from oemof import solph
    >>> bel = solph.buses.Bus(label='electricity')

    >>> electricity_export = solph.components.Sink(
    ...    label='el_export',
    ...    inputs={bel: solph.flows.Flow()})

    """

    def __init__(
        self, label=None, *, inputs, parent_node=None, custom_properties=None
    ):
        if inputs is None:
            inputs = {}
        if custom_properties is None:
            custom_properties = {}

        super().__init__(
            label=label,
            inputs=inputs,
            parent_node=parent_node,
            custom_properties=custom_properties,
        )
