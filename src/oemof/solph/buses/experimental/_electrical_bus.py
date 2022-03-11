# -*- coding: utf-8 -*-

"""
In-development electrical bus component.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Johannes Röder
SPDX-FileCopyrightText: jakob-wo
SPDX-FileCopyrightText: gplssm
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: Johannes Kochems

SPDX-License-Identifier: MIT

"""

from oemof.solph.buses._bus import Bus


class ElectricalBus(Bus):
    r"""An electrical bus object used for linear optimal power flow (lopf)

    Every (spatial) node has to be connected to a BusBlock.
    This BusBlock is used in combination with ElectricalLine objects
    for linear optimal power flow (lopf) calculations.

    Parameters
    ----------
    slack: boolean
        If True BusBlock is slack bus for electrical network
    v_max: numeric
        Maximum value of voltage angle at electrical bus
    v_min: numeric
        Mininum value of voltage angle at electrical bus

    Note: This component is experimental. Use it with care.

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :class:`.BusBlock`
    The objects are also used inside:
     * :class:`.ElectricalLine`

    """  # noqa: E501

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slack = kwargs.get("slack", False)
        self.v_max = kwargs.get("v_max", 1000)
        self.v_min = kwargs.get("v_min", -1000)
