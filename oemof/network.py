from weakref import WeakKeyDictionary as WKD, WeakSet as WS
"""
This package (along with its subpackages) contains the classes used to model
energy systems. An energy system is modelled as a graph/network of entities
with very specific constraints on which types of entities are allowed to be
connected.

"""


class _Edges():
    """ Internal utility class keeping track of known edges.

    As this is currently quite dirty and hackish, it should be treated as an
    internal implementation detail with an unstable interface. Maye it can be
    converted to a fully fledged useful :python:`Edge` class later on, but for
    now it simply hides most of the dirty secrets of the :class:`Node` class.

    """
    _in_edges = WKD()
    _flows = WKD()
    def __getitem__(self, key):
        self._flows[key] = self._flows.get(key, WS())
        return self._flows.get[key]
    def __setitem__(self, key, value):
        source, target = key
        self._in_edges[target] = self._in_edges.get(target, WS())
        self._in_edges[target].add(source)
        self._flows[source] = self._flows.get(source, WKD())
        self._flows[source][target] = value

    def __call__(self, *keys):
        result = self._flows
        for k in keys:
            print(k)
            result = result[k]
        return result


flow = _Edges()


