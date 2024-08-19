# -*- coding: utf-8 -*-

"""Helpers to fit scalar values into sequences.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: henhuy

SPDX-License-Identifier: MIT

"""

from collections import abc
from itertools import repeat

import numpy as np


def sequence(iterable_or_scalar):
    """Checks if an object is iterable (except string) or scalar and returns
    the original sequence if object is an iterable and an 'emulated'
    sequence object of class _Sequence if object is a scalar or string.

    Parameters
    ----------
    iterable_or_scalar : iterable or None or int or float

    Examples
    --------
    >>> y = sequence([1,2,3,4,5,6,7,8,9,10,11])
    >>> y[0]
    1

    >>> y[10]
    11

    >>> import pandas as pd
    >>> s1 = sequence(pd.Series([1,5,9]))
    >>> s1[2]
    9

    >>> x = sequence(10)
    >>> x[0]
    10

    >>> x[10]
    10

    """
    if isinstance(iterable_or_scalar, str):
        return iterable_or_scalar
    elif isinstance(iterable_or_scalar, abc.Iterable):
        return np.array(iterable_or_scalar)
    else:
        return _FakeSequence(value=iterable_or_scalar)


class _FakeSequence:
    """Emulates a list whose length is not known in advance.

    Parameters
    ----------
    value : scalar
    length : integer


    Examples
    --------
    >>> s = _FakeSequence(value=42, length=5)
    >>> s
    [42, 42, 42, 42, 42]
    >>> s = _FakeSequence(value=42)
    >>> # undefined lenght, access still works
    >>> s[1337]
    42
    """

    def __init__(self, value, length=None):
        self._value = value
        self._length = length

    @property
    def size(self):
        return self._length

    @size.setter
    def size(self, value):
        self._length = value

    def __getitem__(self, _):
        return self._value

    def __repr__(self):
        if self._length is not None:
            return str([i for i in self])
        else:
            return f"[{self._value}, {self._value}, ..., {self._value}]"

    def __len__(self):
        return self._length

    def __iter__(self):
        return repeat(self._value, self._length)

    def max(self):
        return self._value

    def min(self):
        return self._value

    def sum(self):
        if self._length is None:
            return np.inf
        else:
            return self._length * self._value

    def to_numpy(self, length=None):
        if length is not None:
            return np.full(length, self._value)
        else:
            return np.full(len(self), self._value)

    @property
    def value(self):
        return self._value
