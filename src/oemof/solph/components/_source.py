# -*- coding: utf-8 -*-

"""
solph version of oemof.network.Source

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler

SPDX-License-Identifier: MIT

"""

from oemof.network import network as on

from oemof.solph._helpers import check_node_object_for_missing_attribute


class Source(on.Source):
    """A node object which is designed for one output flow.

    Parameters
    ----------
    label : str
        String holding the label of the Source object.
        The label of each object must be unique.

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

    >>> str(pv_plant.outputs()])
    ['electricity']

    Notes
    -----
    It is theoretically possible to use the Source object with multiple outputs.
    However, we strongly recommend using multiple Source objects instead.
    """

    def __init__(self, label=None, outputs=None):
        if outputs is None:
            outputs = {}

        super().__init__(label=label, outputs=outputs)
        check_node_object_for_missing_attribute(self, "outputs")

    def constraint_group(self):
        pass
