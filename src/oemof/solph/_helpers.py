# -*- coding: utf-8 -*-

"""
Private helper functions.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: David Fuhrländer
SPDX-FileCopyrightText: Johannes Röder

SPDX-License-Identifier: MIT

"""

from warnings import warn

from oemof.tools import debugging


def check_node_object_for_missing_attribute(obj, attribute):
    """Raises a predefined warning if object does not have attribute.

    Arguments
    ---------

    obj : python object
    attribute : (string) name of the attribute to test for

    """
    if not getattr(obj, attribute):
        warn_if_missing_attribute(obj, attribute)


def warn_if_missing_attribute(obj, attribute):
    """Raises warning if attribute is missing for given object"""
    msg = (
        "Attribute <{0}> is missing in Node <{1}> of {2}.\n"
        "If this is intended and you know what you are doing you can"
        "disable the SuspiciousUsageWarning globally."
    )
    warn(
        msg.format(attribute, obj.label, type(obj)),
        debugging.SuspiciousUsageWarning,
    )
