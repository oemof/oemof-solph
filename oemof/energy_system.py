# -*- coding: utf-8 -*-

"""Basic EnergySystem class

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted by
the contributors recorded in the version control history of the file, available
from its original location oemof/oemof/energy_system.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

from functools import partial
import collections.abc as cabc
import logging
import os
import re

import pandas as pd
import dill as pickle

from oemof.groupings import DEFAULT as BY_UID, Grouping, Nodes
from oemof.network import Bus, Component

NOT_AVAILABLE = object()
try:
    import datapackage

    from itertools import chain, cycle, groupby, repeat
    import json
    import re
    import types
except ImportError as e:
    datapackage = NOT_AVAILABLE


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
    def __init__(self, **kwargs):
        for attribute in ['entities']:
            setattr(self, attribute, kwargs.get(attribute, []))

        self._groups = {}
        self._groupings = ([BY_UID] +
                           [g if isinstance(g, Grouping) else Nodes(g)
                            for g in kwargs.get('groupings', [])])
        for e in self.entities:
            for g in self._groupings:
                g(e, self.groups)
        self.results = kwargs.get('results')
        self.timeindex = kwargs.get('timeindex',
                                    pd.date_range(start=pd.to_datetime('today'),
                                                  periods=1, freq='H'))

    @staticmethod
    def _regroup(entity, groups, groupings):
        for g in groupings:
            g(entity, groups)
        return groups

    if not datapackage is NOT_AVAILABLE:
        @classmethod
        def from_datapackage(cls, path):
            package = datapackage.Package(path)
            # This is necessary because before reading a resource for the first
            # time its `headers` attribute ist `None`.
            for r in package.resources: r.read()
            empty = types.SimpleNamespace()
            empty.read = lambda *xs, **ks: ()
            empty.headers = ()
            parse = lambda s: (json.loads(re.sub(
                r'([{,] *)([^,:"{} ]*) *:',
                r'\1"\2":',
                s)) if s else {})
            data = {}
            listify = lambda x, n=None: (x
                                         if type(x) is list
                                         else repeat(x)
                                              if not n
                                              else repeat(x, n))
            resource = lambda r: package.get_resource(r) or empty

            timeindex = None
            def sequences(r):
                """ Parses the resource `r` as a sequence.
                """
                result = {
                    name: [s[name]
                           for s in r.read(keyed=True)]
                    for name in r.headers}
                timeindex=result['timeindex']
                result = {
                    name: pd.Series(result[name], index=timeindex)
                    for name in result
                    if name != 'timeindex'}
                return result

            for r in package.resources:
                if all(re.match(r'^data/sequences/.*$', p)
                       for p in listify(r.descriptor['path'], 1)):
                    data.update({r.name: sequences(r)})

            data.update(
                    {name: {r['name']: {key: r[key] for key in r}
                            for r in resource(name).read(keyed=True)}
                     for name in ('hubs', 'components')})

            data['elements'] = {e['name']:
                {'name': e['name'],
                 'inputs': {source: edges[i, source]
                            for i, source in enumerate(inputs)},
                 'outputs': {target: edges[i, target]
                             for i, target in enumerate(outputs, len(inputs))},
                 'parameters': dict(chain(
                        parse(e.get('node_parameters', "{}")).items(),
                        data['components'].get(e['name'], {}).items())),
                 'type': e['type']}
                for e in resource('elements').read(keyed=True)
                for inputs, outputs in (
                  ([p.strip() for p in e['predecessors'].split(',') if p],
                   [s.strip() for s in e['successors'].split(',') if s]),)
                for triples in (chain(
                    *(zip(enumerate(chain(inputs, outputs)),
                          repeat(parameter),
                          listify(value))
                      for parameter, value in
                          parse(e.get('edge_parameters', "{}")).items())),)
                for edges in (
                    {group: {parameter: value
                             for _, parameter, value in grouped_triples
                             if value is not None}
                     for group, grouped_triples in groupby(
                        sorted(triples),
                        key=lambda triple: triple[0])
                    },)}

            def resolve_foreign_keys(source):
                """ Check whether any key in `source` is a FK and follow it.

                The `source` dictionary is checked for whether any of
                its keys is a foreign key. A key is considered a
                foreign key if:

                  - the value it points to is a string,
                  - it is the name of a resource,
                  - the value it points to is itself a top level key in
                    the named resource.

                If the above is the case, the foreign key itself is
                deleted, the value it pointed to becomes the new key in
                it's place and the value the key points to in the named
                resource becomes the new value.
                Foreign keys are resolved deeply, i.e. if `source`
                contains nested dictionaries, foreign keys found on
                arbitrary levels are resolved.
                """
                for key in source:
                    if (isinstance(source[key], str) and
                        key in data and
                        source[key] in data[key]):

                        source_value = source[key]
                        target_value = data[key][source_value]
                        del source[key]
                        key = source_value
                        source[source_value] = target_value

                    if isinstance(source[key], cabc.MutableMapping):
                        resolve_foreign_keys(source[key])

                return source

            resolve_foreign_keys(data['elements'])
            bus_names = set(chain(*(e[io].keys()
                                    for e in data['elements'].values()
                                    for io in ['inputs', 'outputs'])))
            data['buses'] = {name: {'name': name,
                                    'type': 'bus',
                                    'parameters': data['hubs'].get(name, {})}
                             for name in bus_names}

            def create(cls, init, attributes):
                """ Creates an instance of `cls` and sets `attributes`.
                """
                instance = cls(**init)
                for k, v in attributes.items():
                    setattr(instance, k, v)
                return instance

            data['buses'] = {name: create(Bus, {'label': name},
                                          bus['parameters'])
                             for name, bus in data['buses'].items()}

            data['components'] = {
                    name: create(Component,
                        {'label': name,
                         'inputs': {
                            data['buses'][bus]: flow
                            for bus, flow in element['inputs'].items()},
                         'outputs': {
                            data['buses'][bus]: flow
                            for bus, flow in element['outputs'].items()}},
                         element['parameters'])
                    for name, element in data['elements'].items()}

            es = cls(timeindex=timeindex)
            es.add(*chain(data['components'].values(), data['buses'].values()))

            return es


    def _add(self, entity):
        self.entities.append(entity)
        self._groups = partial(self._regroup, entity, self.groups,
                               self._groupings)

    def add(self, *nodes):
        """ Add :class:`nodes <oemof.network.Node>` to this energy system.
        """
        for n in nodes:
            self._add(n)

    @property
    def groups(self):
        while callable(self._groups):
            self._groups = self._groups()
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

        self.__dict__ = pickle.load(open(os.path.join(dpath, filename), "rb"))
        msg = ('Attributes restored from: {0}'.format(os.path.join(
            dpath, filename)))
        logging.debug(msg)
        return msg
