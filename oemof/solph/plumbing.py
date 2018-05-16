# -*- coding: utf-8 -*-

"""Plumbing stuff.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/solph/plumbing.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

import operator
from collections import abc, UserList
from itertools import repeat
from numpy import array
from copy import deepcopy


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
    >>> sequence(2)
    2

    >>> x = sequence(10)
    >>> x[0]
    10

    >>> x[10]
    10
    >>> print(x)
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    >>> a = sequence(3)
    >>> a + sequence(5)
    8
    >>> a[2] = 4
    >>> a + sequence(5)
    [8, 8, 9]
    >>> a * sequence(2)
    [6, 6, 8]
    >>> b = sequence([1, 2, 3])
    >>> c = sequence([4, 5, 6])
    >>> b + c
    [5, 7, 9]
    """
    if (isinstance(sequence_or_scalar, abc.Iterable) and not
            isinstance(sequence_or_scalar, str)):
        return _Sequence(sequence_or_scalar)
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
    >>> [s[i] for i in range(5)]
    [23, 42, 42, 42, 42]
    >>> sl = _Sequence([1, 2, 3])
    >>> sl[2]
    3
    """
    def __init__(self, *args, **kwargs):
        self.default = kwargs.get('default')
        self.real_list = False
        if 'default' not in kwargs:
            self.real_list = True
            self.default_changed = True
            self.highest_index = len(args) - 1
        else:
            self.default_changed = False
            self.highest_index = -1
        super(_Sequence, self).__init__(*args)

    def __getitem__(self, key):
        if self.real_list:
            return super(_Sequence, self).__getitem__(key)
        self.highest_index = max(self.highest_index, key)
        if not self.default_changed:
            return self.default
        try:
            return self.data[key]
        except IndexError:
            self.data.extend([self.default] * (key - len(self.data) + 1))
            return self.data[key]

    def __setitem__(self, key, value):
        if self.real_list:
            return super(_Sequence, self).__setitem__(key, value)
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
        if self.highest_index < 0:
            return str(self.default)
        return str([i for i in self])

    def __len__(self):
        return max(len(self.data), self.highest_index + 1)

    def __iter__(self):
        if self.default_changed:
            return super(_Sequence, self).__iter__()
        else:
            return repeat(self.default)

    def __operate_sequences(self, other, op: operator):
        if not (self.default_changed or other.default_changed):
            return _Sequence(default=op(self.default, other.default))
        if not (self.real_list or other.real_list):
            length = max(len(self), len(other))
            new = deepcopy(self)
            new.data = list(op(
                array([self[i] for i in range(length)]),
                array([other[i] for i in range(length)])
            ))
            new.default = op(self.default, other.default)
            return new
        # At least one sequence contains a real list:
        length = max(len(self), len(other))
        new = deepcopy(self)
        try:
            new.data = list(op(
                array([self[i] for i in range(length)]),
                array([other[i] for i in range(length)])
            ))
        except IndexError:
            raise IndexError(
                'Sequences contain data with different lengths')
        new.real_list = True
        new.default = None
        return new

    def __add__(self, other):
        if not isinstance(other, _Sequence):
            return super(_Sequence, self).__add__(other)
        # If other is Sequence:
        op = operator.add
        return self.__operate_sequences(other, op)

    def __sub__(self, other):
        if not isinstance(other, _Sequence):
            return super(_Sequence, self).__add__(other)
        # If other is Sequence:
        op = operator.sub
        return self.__operate_sequences(other, op)

    def __mul__(self, other):
        if not isinstance(other, _Sequence):
            return super(_Sequence, self).__add__(other)
        # If other is Sequence:
        op = operator.mul
        return self.__operate_sequences(other, op)

    def __truediv__(self, other):
        if not isinstance(other, _Sequence):
            return super(_Sequence, self).__add__(other)
        # If other is Sequence:
        op = operator.truediv
        return self.__operate_sequences(other, op)

