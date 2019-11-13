# -*- coding: utf-8 -*-

"""Plumbing stuff.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/solph/plumbing.py

SPDX-License-Identifier: MIT
"""

from collections import abc, UserList
from itertools import repeat


def sequence(sequence_or_scalar):
    """ Tests if an object is sequence (except string) or scalar and returns
    a the original sequence if object is a sequence and a 'emulated' sequence
    object of class _Sequence if object is a scalar or string.

    Parameters
    ----------
    sequence_or_scalar : array-like, None, int, float

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
    if (isinstance(sequence_or_scalar, abc.Iterable) and not
            isinstance(sequence_or_scalar, str)):
        return sequence_or_scalar
    else:
        return _Sequence(default=sequence_or_scalar)


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
