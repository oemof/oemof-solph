# -*- coding: utf-8 -*-

"""
Private helper functions.

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
