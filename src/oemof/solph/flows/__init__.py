# -*- coding: utf-8 -*-

"""
This module is designed to hold flows with their classes and
associated individual constraints (blocks) and groupings.
Currently, the design of the `Flow`s is that there is only one
class but object are different based on parameters.
This is subject to change in the future.

Note that only mature code is imported,
experimental code should be included in oemof.experimental.

SPDX-FileCopyrightText: oemof association (oemof e.V.)

SPDX-License-Identifier: MIT
"""

from ._flow import Flow

__all__ = [
    "Flow",
]
