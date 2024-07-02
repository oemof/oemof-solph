# -*- coding: utf-8 -*-

"""
solph version of oemof.network.Source

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: Johannes Kochems

SPDX-License-Identifier: MIT

"""
from oemof.network import Node


class Source(Node):
    """A component which is designed for one output flow.

    Parameters
    ----------
    label : str
        String holding the label of the Source object.
        The label of each object must be unique.
    outputs: dict
        A dictionary mapping input nodes to corresponding outflows
        (i.e. output values).

    Examples
    --------
    Defining a Source:

    >>> from oemof import solph
    >>> bel = solph.buses.Bus(label='electricity')

    >>> pv_plant = solph.components.Source(
    ...    label='pp_pv',
    ...    outputs={bel: solph.flows.Flow()})

    >>> type(pv_plant)
    <class 'oemof.solph.components._source.Source'>

    >>> pv_plant.label
    'pp_pv'

    >>> str(pv_plant.outputs[bel].output)
    'electricity'
    """

    def __init__(self, label=None, *, outputs, custom_attributes=None):
        if outputs is None:
            outputs = {}
        if custom_attributes is None:
            custom_attributes = {}

        super().__init__(
            label=label, outputs=outputs, custom_properties=custom_attributes
        )

    def constraint_group(self):
        pass
