# -*- coding: utf-8 -*-

"""Exceptions to allow reusing of warnings.

SPDX-FileCopyrightText: Pierre-François Duc

SPDX-License-Identifier: MIT

"""


class FlowOptionWarning(UserWarning):
    pass


class WrongOptionCombinationError(ValueError):
    pass
