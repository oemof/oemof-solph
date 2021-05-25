# -*- coding: utf-8 -*-

"""Plumbing stuff.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: henhuy

SPDX-License-Identifier: MIT

"""

from collections import UserList
from collections import abc
from itertools import repeat


def sequence(iterable_or_scalar):
    """ Tests if an object is iterable (except string) or scalar and returns
    a the original sequence if object is an iterable and a 'emulated' sequence
    object of class _Sequence if object is a scalar or string.

    Parameters
    ----------
    iterable_or_scalar : iterable or None or int or float

    Examples
    --------
    >>> sequence([1,2])
    [1, 2]

    >>> x = sequence(10)
    >>> x[0]
    10

    >>> x[10]
    10
    >>> print(x)
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

    """
    if (isinstance(iterable_or_scalar, abc.Iterable) and not
            isinstance(iterable_or_scalar, str)):
        return iterable_or_scalar
    else:
        return _Sequence(default=iterable_or_scalar)


class _Sequence(UserList):
    """ Emulates a list whose length is not known in advance.

    Parameters
    ----------
    source:
    default:


    Examples
    --------
    >>> s = _Sequence(default=42)
    >>> len(s)
    0
    >>> s[1]
    42
    >>> s[2]
    42
    >>> len(s)
    3
    >>> s
    [42, 42, 42]
    >>> s[8]
    42


    """
    def __init__(self, *args, **kwargs):
        self.default = kwargs["default"]
        self.default_changed = False
        self.highest_index = -1
        super().__init__(*args)

    def __getitem__(self, key):
        self.highest_index = max(self.highest_index, key)
        return self.default

    def __init_list(self):
        self.data = [self.default] * (self.highest_index + 1)

    def __repr__(self):
        return str([i for i in self])

    def __len__(self):
        return max(len(self.data), self.highest_index + 1)

    def __iter__(self):
        return repeat(self.default, self.highest_index + 1)
