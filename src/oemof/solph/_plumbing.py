# -*- coding: utf-8 -*-

"""Helpers to fit scalar values into sequences.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: henhuy

SPDX-License-Identifier: MIT

"""

import warnings
from collections import UserDict
from collections import abc

import numpy as np


def sequence(iterable_or_scalar, length=None):
    """Casts iterable_or_scalar to an object that allows element access.

    Technically, it checks if an object is iterable or scalar and returns a
    numpy array if the object is an iterable or the length is given, or a
    _FakeSequence if the length cannot be infered.
    This way, we can (possibly) define a sequence of unknown length if needed.

    Parameters
    ----------
    iterable_or_scalar : iterable or None or int or float

    Examples
    --------
    >>> y = sequence([1,2,3,4,5,6,7,8,9,10,11])
    >>> y[0]
    np.int64(1)

    >>> y[10]
    np.int64(11)

    >>> import pandas as pd
    >>> s1 = sequence(pd.Series([1,5,9]))
    >>> s1[2]
    np.int64(9)

    >>> x = sequence(10)
    >>> x[0]
    10

    >>> x[10]
    10

    """
    if iterable_or_scalar is None:
        return None
    if isinstance(iterable_or_scalar, _FakeSequence):
        if length is not None:
            return np.full(shape=length, fill_value=iterable_or_scalar.value)
        else:
            return iterable_or_scalar

    if len(np.shape(iterable_or_scalar)) > 1:
        d = len(np.shape(iterable_or_scalar))
        raise ValueError(
            f"Dimension too high ({d} > 1) for {iterable_or_scalar}\n"
            "The dimension of a number is 0, of a list 1, of a table 2 and so "
            "on.\nPlease notice that a table with one column is still a table "
            "with 2 dimensions and not a Series."
        )
    if isinstance(iterable_or_scalar, abc.Iterable):
        if length and length is not len(iterable_or_scalar):
            raise ValueError(
                f"Length mismatch: Cannot create sequence of length {length}"
                + " from input {iterable_or_scalar}."
            )
        else:
            return np.array(iterable_or_scalar)
    else:
        return _FakeSequence(value=iterable_or_scalar)


def valid_sequence(sequence, length: int) -> bool:
    """
    Checks if an object has the given length

    This is needed as we have `_FakeSequence` which is assumed to have every
    possible length, thus `__len__` is not defined for it.
    """
    if sequence is None:
        return False
    elif isinstance(sequence, _FakeSequence):
        return True  # a _FakeSequence has every length
    else:
        if len(sequence) == length:
            return True
        # --- BEGIN: To be removed for versions >= v0.6 ---
        elif len(sequence) > length:
            warnings.warn(
                "Sequence longer than needed"
                f" ({sequence.size} items instead of {length})."
                " This will be treated as an error in the future.",
                FutureWarning,
            )
            return True
        # --- END ---
        else:
            raise ValueError(f"Lentgh of {sequence} should be {length}.")


class SequenceDict(UserDict):
    """Convert each value to a `sequence` upon insertion.

    A drop-in replacement class for `dict`s, that calls `sequence` on
    values before they are inserted and stores the result.

    """

    def __setitem__(self, key, value):
        self.data[key] = sequence(value)


class Apply:
    """Apply `converter` to values assigned to this attribute.

    Whenever a `value` is assigned to an attribute that uses this
    descriptor, what's actually stored is the result of
    `converter(value)`, e.g.:

    >>> class Inverter:
    ...     inverted = Apply(lambda x: -x)
    ...
    >>> one = Inverter()
    >>> one.inverted = 1
    >>> one.inverted
    -1

    """

    unset = object()

    def __init__(self, converter, default=unset):
        self.converter = converter
        self.default = default

        self.data = {}
        self.name = None

    def __get__(self, obj, objtype=None):
        if (id(obj) not in self.data) and (self.default is self.unset):
            raise AttributeError(
                f"attribute '{self.name}' of '{objtype.__name__}'"
                " object accessed before being assigned a value"
            )
        return self.data.get(id(obj), self.default)

    def __set__(self, obj, value):
        self.data[id(obj)] = self.converter(value)

    def __set_name__(self, owner, name):
        self.name = name


class _FakeSequence:
    """Emulates a numpy.array which length is not known in advance.

    Parameters
    ----------
    value : scalar
    length : integer


    Examples
    --------
    >>> s = _FakeSequence(value=42)
    >>> s
    [42, 42, ..., 42]
    >>> # undefined lenght, access always works
    >>> s[1337]
    42
    """

    def __init__(self, value):
        self._value = value

    def __getitem__(self, i):
        if isinstance(i, slice):
            start = (i.start if i.start is not None else 0)
            step = (i.step if i.step is not None else 1)
            stop = (i.stop if i.stop is not None else -1)
            if start < stop:
                length = (stop - start) // step
                return np.full(length, self._value)
            else:
                raise IndexError(
                    "_FakeSequence has every length. Thus, slicing only works"
                    + " if it allows infering the target length."
                )
        else:
            return self._value

    def __repr__(self):
        return f"[{self._value}, {self._value}, ..., {self._value}]"

    def __float__(self):
        return self._value

    def max(self):
        return self._value

    def min(self):
        return self._value

    def all(self):
        return bool(self.value)

    def any(self):
        return bool(self.value)

    def __bool__(self):
        return bool(self.value)

    def __abs__(self):
        return _FakeSequence(abs(self.value))

    def __and__(self, other):
        return sequence(self.value & other)

    __rand__ = __and__

    def __or__(self, other):
        return sequence(self.value | other)

    __ror__ = __or__

    def __eq__(self, other):
        return sequence(self.value == other)

    def __lt__(self, other):
        return sequence(self.value < other)

    def __le__(self, other):
        return sequence(self.value <= other)

    def __gt__(self, other):
        return sequence(self.value > other)

    def __ge__(self, other):
        return sequence(self.value >= other)

    def __add__(self, other):
        return sequence(self.value + other)

    __radd__ = __add__

    def __sub__(self, other):
        return sequence(self.value - other)

    def __rsub__(self, other):
        return sequence(other - self.value)

    def __mul__(self, other):
        return sequence(self.value * other)

    __rmul__ = __mul__

    def __truediv__(self, other):
        return sequence(self.value / other)

    def __rtruediv__(self, other):
        return sequence(other / self.value)

    @property
    def value(self):
        return self._value
