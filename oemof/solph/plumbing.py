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


def node_param_dict(node_timestep_set=None, attribute=None):
    """Create double indexed attribute dictionary for nodes.

    This is used to initialize (mutable) parameters over a two-dimensional
    set of nodes and timesteps. See `custom.GenericCAESBlock2` for usage.
    A node attribute name is passed in order to get its value for the
    respective node within a list comprehension and initialize it over
    all timesteps within the two-dimensional set.

    Note that the attribute must be subscriptable in order to deal with scalars
    and sequences similarly and thus must be converted to a subscriptable data
    type i.e. here a `solph_sequence`.

    Parameters
    ----------
    node_timestep_set: set with tuples of nodes and timesteps (n, t)
    attribute: string with node attribute name

    Examples
    --------
    >>> my_set =  [(n1, 1), (n1, 2), ... , (n2, 1), (n2, 2)] # doctest: +SKIP
    >>> my_attribute = 'cmp_P_inst' # doctest: +SKIP
    >>> node_param_dict(my_set, my_attribute) # doctest: +SKIP
    {(n, 1): 20, (n1, 2): 20, ... , (n2, 1): 47, (n2, 2): 11}
    """
    node_param_dict = {((node, timestep)):
                       sequence(getattr(node, attribute))[timestep]
                       for (node, timestep) in node_timestep_set}
    return node_param_dict


def flow_param_dict(flow_timestep_set=None, flows=None,
                    attribute=None, attribute_default=None):
    """Create double indexed attribute dictionary for flows.

    This is used to initialize (mutable) parameters over a three-dimensional
    set of two flows and respective timesteps and works similarly as
    `node_param_dict`.

    Parameters
    ----------
    flow_timestep_set: set with tuples of flow nodes and timesteps (n1, n2, t)
    flows: flow object container of `EnergySystem` class
    attribute: string with node attribute name
    attribute_default: default value for attribute if not set

    Examples
    --------
    >>> my_set = [(n1, n2, 1), (n1, n2, 2), ... , (n3, n4, 1), (n3, n4, 2)] # doctest: +SKIP
    >>> my_attribute = 'nominal_value' # doctest: +SKIP
    >>> flow_param_dict(my_set, es.flows, my_attribute) # doctest: +SKIP
    {(n1, n2, 1): 20, (n1, n2, 2): 20, ... , (n3, n4, 1): 47, (n3, n4, 2): 11}
    """
    flow_param_dict = {
        (n1, n2, t): (
            sequence(getattr(flows[n1, n2], attribute))[t] if
            getattr(flows[n1, n2], attribute) else
            sequence(attribute_default)[t]
        )
        for n1, n2, t in flow_timestep_set
    }

    return flow_param_dict
