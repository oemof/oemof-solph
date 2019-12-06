# -*- coding: utf-8 -*-

"""Module contains tools facilitating debugging

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/tools/economics.py

SPDX-License-Identifier: MIT
"""


class SuspiciousUsageWarning(UserWarning):
    """
    Warn the user about potentially dangerous usage.

    It is not necessarily wrong but could lead to an unwanted behaviour if you
    do not know what you are doing. If you know what you are doing you can
    easily switch off the warnings.

    Examples
    --------
    >>> import warnings
    >>> warnings.filterwarnings("ignore", category=SuspiciousUsageWarning)
    """
    pass
