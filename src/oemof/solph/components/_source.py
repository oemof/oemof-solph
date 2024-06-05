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

from warnings import warn

from oemof.network import Node
from oemof.tools import debugging


class Source(Node):
    """A component which is designed for one output flow.

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

    >>> pv_plant.label
    'pp_pv'

    >>> str(pv_plant.outputs[bel].output)
    'electricity'

    Notes
    -----
    It is theoretically possible to use the Source object with multiple
    outputs. However, we strongly recommend using multiple Source objects
    instead.
    """

    def __init__(self, label=None, outputs=None, custom_attributes=None):
        if outputs is None:
            outputs = {}
        if custom_attributes is None:
            custom_attributes = {}

        if len(outputs) != 1:
            msg = (
                "A Source is designed to have one output but you provided {0}."
                " If this is intended and you know what you are doing you can "
                "disable the SuspiciousUsageWarning globally."
            )
            warn(
                msg.format(len(outputs)),
                debugging.SuspiciousUsageWarning,
            )

        super().__init__(
            label=label, outputs=outputs, custom_properties=custom_attributes
        )

    def constraint_group(self):
        pass
