# -*- coding: utf-8 -*-

"""Basic EnergySystem class

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/energy_system.py

SPDX-License-Identifier: MIT
"""

from collections import deque
from pickle import UnpicklingError
import logging
import os

import blinker
import dill as pickle

from oemof.groupings import DEFAULT as BY_UID, Grouping, Nodes
from oemof.network import Bus


class EnergySystem:
    r"""Defining an energy supply system to use oemof's solver libraries.

    Note
    ----
    The list of regions is not necessary to use the energy system with solph.

    Parameters
    ----------
    entities : list of :class:`Entity <oemof.core.network.Entity>`, optional
        A list containing the already existing :class:`Entities
        <oemof.core.network.Entity>` that should be part of the energy system.
        Stored in the :attr:`entities` attribute.
        Defaults to `[]` if not supplied.
    timeindex : pandas.datetimeindex
        Define the time range and increment for the energy system.
    groupings : list
        The elements of this list are used to construct :class:`Groupings
        <oemof.core.energy_system.Grouping>` or they are used directly if they
        are instances of :class:`Grouping <oemof.core.energy_system.Grouping>`.
        These groupings are then used to aggregate the entities added to this
        energy system into :attr:`groups`.
        By default, there'll always be one group for each :attr:`uid
        <oemof.core.network.Entity.uid>` containing exactly the entity with the
        given :attr:`uid <oemof.core.network.Entity.uid>`.
        See the :ref:`examples <energy-system-examples>` for more information.

    Attributes
    ----------
    entities : list of :class:`Entity <oemof.core.network.Entity>`
        A list containing the :class:`Entities <oemof.core.network.Entity>`
        that comprise the energy system. If this :class:`EnergySystem` is
        set as the :attr:`registry <oemof.core.network.Entity.registry>`
        attribute, which is done automatically on :class:`EnergySystem`
        construction, newly created :class:`Entities
        <oemof.core.network.Entity>` are automatically added to this list on
        construction.
    groups : dict
    results : dictionary
        A dictionary holding the results produced by the energy system.
        Is `None` while no results are produced.
        Currently only set after a call to :meth:`optimize` after which it
        holds the return value of :meth:`om.results()
        <oemof.solph.optimization_model.OptimizationModel.results>`.
        See the documentation of that method for a detailed description of the
        structure of the results dictionary.
    timeindex : pandas.index, optional
        Define the time range and increment for the energy system. This is an
        optional attribute but might be import for other functions/methods that
        use the EnergySystem class as an input parameter.


    .. _energy-system-examples:
    Examples
    --------

    Regardles of additional groupings, :class:`entities
    <oemof.core.network.Entity>` will always be grouped by their :attr:`uid
    <oemof.core.network.Entity.uid>`:

    >>> from oemof.network import Entity
    >>> from oemof.network import Bus, Sink
    >>> es = EnergySystem()
    >>> bus = Bus(label='electricity')
    >>> es.add(bus)
    >>> bus is es.groups['electricity']
    True

    For simple user defined groupings, you can just supply a function that
    computes a key from an :class:`entity <oemof.core.network.Entity>` and the
    resulting groups will be sets of :class:`entities
    <oemof.core.network.Entity>` stored under the returned keys, like in this
    example, where :class:`entities <oemof.core.network.Entity>` are grouped by
    their `type`:

    >>> es = EnergySystem(groupings=[type])
    >>> buses = set(Bus(label="Bus {}".format(i)) for i in range(9))
    >>> es.add(*buses)
    >>> components = set(Sink(label="Component {}".format(i))
    ...                   for i in range(9))
    >>> es.add(*components)
    >>> buses == es.groups[Bus]
    True
    >>> components == es.groups[Sink]
    True

    """

    signals = {}
    """A dictionary of blinker_ signals emitted by energy systems.

    Currently only one signal is supported. This signal is emitted whenever a
    `Node <oemof.network.Node>` is `add`ed to an energy system. The signal's
    `sender` is set to the `node <oemof.network.Node>` that got added to the
    energy system so that `nodes <oemof.network.Node>` have an easy way to only
    receive signals for when they themselves get added to an energy system.

    .. _blinker: https://pythonhosted.org/blinker/
    """

    def __init__(self, **kwargs):
        self._first_ungrouped_node_index_ = 0
        self._groups = {}
        self._groupings = ([BY_UID] +
                           [g if isinstance(g, Grouping) else Nodes(g)
                            for g in kwargs.get('groupings', [])])
        self.entities = []

        self.results = kwargs.get('results')

        self.timeindex = kwargs.get('timeindex')

        self.temporal = kwargs.get('temporal')

        self.add(*kwargs.get('entities', ()))

    def add(self, *nodes):
        """Add :class:`nodes <oemof.network.Node>` to this energy system."""
        self.nodes.extend(nodes)
        for n in nodes:
            self.signals[type(self).add].send(n, EnergySystem=self)
    signals[add] = blinker.signal(add)

    @property
    def groups(self):
        gs = self._groups
        deque(
            (
                g(n, gs)
                for g in self._groupings
                for n in self.nodes[self._first_ungrouped_node_index_ :]
            ),
            maxlen=0,
        )
        self._first_ungrouped_node_index_ = len(self.nodes)
        return self._groups

    @property
    def nodes(self):
        return self.entities

    @nodes.setter
    def nodes(self, value):
        self.entities = value

    def flows(self):
        return {(source, target): source.outputs[target]
                for source in self.nodes
                for target in source.outputs}

    def dump(self, dpath=None, filename=None):
        r""" Dump an EnergySystem instance.
        """
        if dpath is None:
            bpath = os.path.join(os.path.expanduser("~"), '.oemof')
            if not os.path.isdir(bpath):
                os.mkdir(bpath)
            dpath = os.path.join(bpath, 'dumps')
            if not os.path.isdir(dpath):
                os.mkdir(dpath)

        if filename is None:
            filename = 'es_dump.oemof'

        pickle.dump(self.__dict__, open(os.path.join(dpath, filename), 'wb'))

        msg = ('Attributes dumped to: {0}'.format(os.path.join(
            dpath, filename)))
        logging.debug(msg)
        return msg

    def restore(self, dpath=None, filename=None):
        r""" Restore an EnergySystem instance.
        """
        logging.info(
            "Restoring attributes will overwrite existing attributes.")
        if dpath is None:
            dpath = os.path.join(os.path.expanduser("~"), '.oemof', 'dumps')

        if filename is None:
            filename = 'es_dump.oemof'

        try:
            self.__dict__ = pickle.load(
                    open(os.path.join(dpath, filename), "rb"))
        except UnpicklingError as e:
            if str(e) == "state is not a dictionary":
                raise UnpicklingError(
                        "\n  "
                        "Seems like you're trying to load an energy system "
                        "dumped with an older\n  "
                        "oemof version. Unfortunetaly we made changes which "
                        "broke this from\n  "
                        "v0.2.2 (more specifically commit `bec669b`) to its "
                        "successor.\n  "
                        "If you really need this functionality, please file "
                        "a bug entitled\n\n    "
                        '"Pickle customization removal breaks '
                        '`EnergySystem.restore`"\n\n  '
                        "at\n\n    "
                        "https://github.com/oemof/oemof/issues\n\n  "
                        "or comment on it if it already exists.")
            raise e

        msg = ('Attributes restored from: {0}'.format(os.path.join(
            dpath, filename)))
        logging.debug(msg)
        return msg
