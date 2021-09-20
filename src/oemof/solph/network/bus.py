# -*- coding: utf-8 -*-

"""
solph version of oemof.network.bus

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler

SPDX-License-Identifier: MIT

"""

from oemof.network import network as on

from oemof.solph import blocks


class Bus(on.Bus):
    """A balance object. Every node has to be connected to Bus.

    The sum of all inputs of a Bus object must equal the sum of all outputs
    within one time step.

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.bus.Bus`

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.balanced = kwargs.get("balanced", True)

    def constraint_group(self):
        if self.balanced:
            return blocks.Bus
        else:
            return None
