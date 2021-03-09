# -*- coding: utf-8 -*-

"""Classes used to model energy supply systems within solph.

Classes are derived from oemof core network classes and adapted for specific
optimization tasks. An energy system is modelled as a graph/network of nodes
with very specific constraints on which types of nodes are allowed to be
connected.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler

SPDX-License-Identifier: MIT

"""

from warnings import warn

from oemof.tools import debugging


def check_node_object_for_missing_attribute(obj, attribute):
    if not getattr(obj, attribute):
        msg = (
            "Attribute <{0}> is missing in Node <{1}> of {2}.\n"
            "If this is intended and you know what you are doing you can"
            "disable the SuspiciousUsageWarning globally."
        )
        warn(
            msg.format(attribute, obj.label, type(obj)),
            debugging.SuspiciousUsageWarning,
        )
