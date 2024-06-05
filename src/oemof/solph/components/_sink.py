# -*- coding: utf-8 -*-

"""
solph version of oemof.network.Sink

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


class Sink(Node):
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


    Notes
    -----
    It is theoretically possible to use the Sink object with multiple inputs.
    However, we strongly recommend using multiple Sink objects instead.
    """

    def __init__(self, label=None, inputs=None, custom_attributes=None):
        if inputs is None:
            inputs = {}
        if custom_attributes is None:
            custom_attributes = {}

        if len(inputs) != 1:
            msg = (
                "A Sink is designed to have one input but you provided {0}."
                " If this is intended and you know what you are doing you can "
                "disable the SuspiciousUsageWarning globally."
            )
            warn(
                msg.format(len(inputs)),
                debugging.SuspiciousUsageWarning,
            )

        super().__init__(
            label=label, inputs=inputs, custom_properties=custom_attributes
        )

    def constraint_group(self):
        pass
