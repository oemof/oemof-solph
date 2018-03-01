""" Tools to work with deserialize energy systems from datapackages.
"""

from itertools import chain, cycle, groupby, repeat
import collections.abc as cabc
import json
import re
import types

import datapackage
import pandas as pd

def deserialize_energy_system(cls, path):
    package = datapackage.Package(path)
    # This is necessary because before reading a resource for the first
    # time its `headers` attribute is `None`.
    for r in package.resources: r.read()
    empty = types.SimpleNamespace()
    empty.read = lambda *xs, **ks: ()
    empty.headers = ()
    parse = lambda s: (json.loads(s) if s else {})
    data = {}
    listify = lambda x, n=None: (x
                                 if type(x) is list
                                 else repeat(x)
                                      if not n
                                      else repeat(x, n))
    resource = lambda r: package.get_resource(r) or empty

    timeindices = {}
    def sequences(r):
        """ Parses the resource `r` as a sequence.
        """
        result = {
            name: [s[name]
                   for s in r.read(keyed=True)]
            for name in r.headers}
        timeindices[r.name] = result['timeindex']
        result = {
            name: pd.Series(result[name], index=timeindices[r.name])
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
                            'type': (data['hubs'].get(name, {})
                                                 .get('type', 'bus')),
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
                    data['buses'][bus]: types.SimpleNamespace(**flow)
                    for bus, flow in element['inputs'].items()},
                 'outputs': {
                    data['buses'][bus]: types.SimpleNamespace(**flow)
                    for bus, flow in element['outputs'].items()}},
                 element['parameters'])
            for name, element in data['elements'].items()}

    lst = ([idx for idx in timeindices.values()])
    if lst[1:] == lst[:-1]:
        # TODO: Get frequency from meta data or calulate...
        es = cls(timeindex=pd.DatetimeIndex(lst[0], freq='H'))
        es.add(*chain(data['components'].values(),
                      data['buses'].values()))
        return es

    else:
        raise ValueError("Timeindices in sequence resources differ!")


