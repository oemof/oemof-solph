""" Tools to deserialize energy systems from datapackages.

**WARNING**

This is work in progress and still pretty volatile, so use it at your own risk.
The datapackage format and conventions we use are still a bit in flux. This is
also why we don't have documentation or tests yet. Once things are stabilized a
bit more, the way in which we extend the datapackage spec will be documented
along with how to use the functions in this module.

"""

from decimal import Decimal
from itertools import chain, groupby, repeat
import collections.abc as cabc
import json
import re
import types

import datapackage
from datapackage import exceptions
import pandas as pd

from oemof.network import Bus, Component


def raisestatement(exception, message=""):
    if message:
        raise exception(message)
    else:
        raise exception()
    return "No one should ever see this."


class HSN(types.SimpleNamespace):
    """ A hashable variant of `types.Simplenamespace`.

    By making it hashable, we can use the instances as dictionary keys, which
    is necessary, as this is the default type for flows.
    """
    def __hash__(self):
        return id(self)


DEFAULT = object()
FLOW_TYPE = object()

def remap(attributes, translations, target_class):
    mro = getattr(target_class, "mro", lambda: [target_class])
    for c in mro():
        if c in translations:
            break
    return {translations.get(c, {}).get(k, k): v for k, v in attributes.items()}


def sequences(r, timeindices=None):
    """ Parses the resource `r` as a sequence.
    """
    result = {
        name: [float(s[name]) if isinstance(s[name], Decimal) else s[name]
               for s in r.read(keyed=True)]
        for name in r.headers}
    if timeindices is not None:
        timeindices[r.name] = result['timeindex']
    result = {
        name: result[name]
        for name in result
        if name != 'timeindex'}
    return result

def read_facade(facade, facades, create, typemap, data, objects,
                sequence_names,
                fks,
                resources):
    """ Parse the resource `r` as a facade.
    """
    # TODO: Generate better error messages, if keys which are assumed to be
    # present, e.g. because they are used as foreign keys or because our
    # way of reading data packages needs them, are missing.
    if 'name' in facade and facade['name'] in facades:
        return facades[facade['name']]
    for field, reference in fks.items():
        if reference["resource"] in sequence_names:
            # if referenc not found -> set field value to None
            facade[field] = data[reference["resource"]].get(facade[field])
        elif facade[field][reference['fields']] in objects:
            facade[field] = objects[facade[field][reference['fields']]]
        elif facade[field][reference['fields']] in facades:
            facade[field] = facades[facade[field][reference['fields']]]
        else:
            foreign_keys = {fk["fields"]: fk["reference"]
                for fk in (resources(reference["resource"])
                           .descriptor['schema']
                           .get("foreignKeys", ()))}
            facade[field] = read_facade(
                facade[field], facades, create, typemap, data, objects,
                sequence_names, foreign_keys, resources)
    # TODO: Do we really want to strip whitespace?
    mapping = typemap.get(facade.get('type').strip())
    if mapping is None:
        raise(ValueError("Typemap is missing a mapping for '{}'."
                         .format(facade.get('type', '<MISSING TYPE>'))))
    instance = create(mapping, facade, facade)
    facades[facade["name"]] = instance
    return instance


def deserialize_energy_system(cls, path,
                              typemap={},
                              attributemap={}):

    default_typemap = {'bus': Bus,
                       'hub': Bus,
                       DEFAULT: Component,
                       FLOW_TYPE: HSN}

    for k, v in default_typemap.items():
        typemap[k] = typemap.get(k, v)

    if attributemap.get(object) is None:
        attributemap[object] = {'name': 'label'}

    for k, v in attributemap.items():
        if v.get('name') is None:
            attributemap[k]['name'] = 'label'



    package = datapackage.Package(path)
    # This is necessary because before reading a resource for the first
    # time its `headers` attribute is `None`.
    for r in package.resources:
        try:
            r.read()
        except exceptions.CastError as e:
            raise exceptions.CastError(
                "Cast error occured in resource with name `{}`".format(r.name))

    empty = types.SimpleNamespace()
    empty.read = lambda *xs, **ks: ()
    empty.headers = ()
    parse = lambda s: (json.loads(s) if s else {})
    data = {}
    listify = lambda x, n=None: (x
                                 if isinstance(x, list)
                                 else repeat(x)
                                 if not n
                                 else repeat(x, n))
    resource = lambda r: package.get_resource(r) or empty

    timeindices = {}

    for r in package.resources:
        if all(re.match(r'^data/sequences/.*$', p)
               for p in listify(r.descriptor['path'], 1)):
            data.update({r.name: sequences(r, timeindices)})
    sequence_names = set(data.keys())

    data.update(
        {name: {r['name']: {key: r[key] for key in r}
                for r in resource(name).read(keyed=True)}
         for name in ('hubs', 'components')})

    data['elements'] = {
        e['name']: {
            'name': e['name'],
            'inputs': {source: edges[i, source]
                       for i, source in enumerate(inputs)},
            'outputs': {target: edges[i, target]
                        for i, target in enumerate(outputs, len(inputs))},
            'parameters': dict(chain(
                parse(e.get('node_parameters', "{}")).items(),
                data['components'].get(e['name'], {}).items())),
            'type': e['type']}
        for e in resource('elements').read(keyed=True)
        for inputs, outputs in
        (([p.strip() for p in e['predecessors'].split(',') if p],
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
             for group, grouped_triples in
             groupby(sorted(triples), key=lambda triple: triple[0])},)}

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

                source[key] = data[key][source[key]]

            if isinstance(source[key], cabc.MutableMapping):
                resolve_foreign_keys(source[key])

        return source

    resolve_foreign_keys(data['elements'])

    bus_names = set(chain(*(e[io].keys()
                            for e in data['elements'].values()
                            for io in ['inputs', 'outputs'])))
    data['buses'] = {name: {'name': name,
                            'type': (data['hubs']
                                     .get(name, {})
                                     .get('type', 'bus')),
                            'parameters': data['hubs'].get(name, {})}
                     for name in bus_names}

    objects = {}
    def create(cls, init, attributes):
        """ Creates an instance of `cls` and sets `attributes`.
        """
        init.update(attributes)
        instance = cls(**remap(init, attributemap, cls))
        for k, v in remap(attributes, attributemap, cls).items():
            if not hasattr(instance, k):
                setattr(instance, k, v)
            name = getattr(instance, "name", getattr(instance, "label", None))
            if name is not None:
                objects[name] = instance
        return instance

    data['buses'] = {
        name: create(mapping if mapping
                     else raisestatement(
                         ValueError,
                         "Typemap is missing a mapping for '{}'."
                         .format(bus.get('type', 'bus'))),
                     {'label': name},
                     bus['parameters'])
        for name, bus in sorted(data['buses'].items())
        for mapping in (typemap.get(bus.get('type', 'bus')),)}

    def resolve_object_references(source, f=None):
        """ Check whether any key in `source` is a reference to a `name`d object.
        """
        def find(n, d):
            found = []
            for resource in d:
                if n in d[resource]:
                    assert getattr(d[resource][n], "label", n) == n
                    found.append(d[resource][n])
                assert len(found) <= 1
            return found

        filtered = {r: data[r] for r in data if (not f) or f(r)}
        for key, name in source.items():
            found = find(key, filtered)
            if len(found) > 0:
                v = source[key]
                del source[key]
                key = found[0]
                source[key] = v
            if isinstance(name, str):
                found = find(name, filtered)
                if len(found) > 0:
                    source[key] = found[0]

            if isinstance(source[key], cabc.MutableMapping):
                resolve_object_references(source[key], f=f)

        return source

    data['components'] = {
        name: create(
            typemap[element.get('type', DEFAULT)],
            {'label': name,
             'inputs': {
                 data['buses'][bus]: flow(**remap(kwargs, attributemap, flow))
                 for bus, kwargs in sorted(element['inputs'].items())},
             'outputs': {
                 data['buses'][bus]: flow(**remap(kwargs, attributemap, flow))
                 for bus, kwargs in sorted(element['outputs'].items())}},
            resolve_object_references(element['parameters'],
                                      f=lambda r: r == 'buses'))
        for name, element in sorted(data['elements'].items())
        for flow in (typemap.get(FLOW_TYPE, HSN),)}

    facades = {}
    for r in package.resources:
        if all(re.match(r'^data/elements/.*$', p)
               for p in listify(r.descriptor['path'], 1)):
            r.read(keyed=True)
            foreign_keys = {fk["fields"]: fk["reference"]
                for fk in r.descriptor['schema'].get("foreignKeys", ())}
            for facade in r.read(keyed=True, relations=True):
                # convert decimal to float
                for f, v in facade.items():
                    if isinstance(v, Decimal):
                        facade[f] = float(v)

                read_facade(facade, facades, create, typemap, data, objects,
                            sequence_names,
                            foreign_keys,
                            resource)

    # TODO: Find concept how to deal with timeindices and clean up based on
    # concept
    lst = ([idx for idx in timeindices.values()])
    if lst[1:] == lst[:-1]:
        # look for temporal resource and if present, take as timeindex from it
        if package.get_resource('temporal'):
            temporal = pd.DataFrame.from_dict(
                package.get_resource('temporal').\
                    read(keyed=True)).set_index('timeindex').astype(float)
            # for correct freq setting of timeindex
            temporal.index = pd.DatetimeIndex(
                temporal.index.values, freq=temporal.index.inferred_freq,
                name='timeindex')
            timeindex = temporal.index

        # if no temporal provided as resource, take the first timeindex
        # from dict
        else:
            # if lst is not empty
            if lst:
                idx = pd.DatetimeIndex(lst[0])
                timeindex = pd.DatetimeIndex(idx.values,
                                             freq=idx.inferred_freq,
                                             name='timeindex')
                temporal = None
            # if for any reason lst of datetimeindices is empty
            # (i.e. no sequences) have been provided, set datetime to one time
            # step of today (same as in the EnergySystem __init__ if no
            # timeindex is passed)
            else:
                timeindex = pd.date_range(start=pd.to_datetime('today'),
                                          periods=1, freq='H')

        es = (cls(timeindex=timeindex, temporal=temporal)
              if lst
              else cls())

        es.add(*chain(data['components'].values(),
                      data['buses'].values(),
                      facades.values(),
                      chain(*[f.subnodes for f in facades.values()
                              if hasattr(f, 'subnodes')])))

        return es

    else:
        raise ValueError("Timeindices in resources differ!")
