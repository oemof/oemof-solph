# -*- coding: utf-8 -*-

"""Plumbing stuff.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/solph/plumbing.py

SPDX-License-Identifier: GPL-3.0-or-later
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
    >>> s[2]
    42
    >>> len(s)
    3
    >>> s[0] = 23
    >>> s
    [23, 42, 42]

    """
    def __init__(self, *args, **kwargs):
        self.default = kwargs["default"]
        self.default_changed = False
        self.highest_index = -1
        super().__init__(*args)

    def __getitem__(self, key):
        self.highest_index = max(self.highest_index, key)
        if not self.default_changed:
            return self.default
        try:
            return self.data[key]
        except IndexError:
            self.data.extend([self.default] * (key - len(self.data) + 1))
            return self.data[key]

    def __setitem__(self, key, value):
        if not self.default_changed:
            self.default_changed = True
            self.__init_list()
        try:
            self.data[key] = value
        except IndexError:
            self.data.extend([self.default] * (key - len(self.data) + 1))
            self.data[key] = value

    def __init_list(self):
        self.data = [self.default] * (self.highest_index + 1)

    def __repr__(self):
        if self.default_changed:
            return super(_Sequence, self).__repr__()
        return str([i for i in self])

    def __len__(self):
        return max(len(self.data), self.highest_index + 1)

    def __iter__(self):
        if self.default_changed:
            return super(_Sequence, self).__iter__()
        else:
            return repeat(self.default, self.highest_index + 1)
