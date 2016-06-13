""" All you need to create groups of stuff in your energy system.
"""
try:
    from collections.abc import ( Hashable, Iterable, Mapping,
                                  MutableMapping as MM)
except ImportError:
    from collections import ( Hashable, Iterable, Mapping,
                              MutableMapping as MM)
from itertools import filterfalse


class Grouping:
    """
    Used to aggregate :class:`entities <oemof.core.network.Entity>` in an
    :class:`energy system <oemof.core.energy_system.EnergySystem>` into
    :attr:`groups <oemof.core.energy_system.EnergySystem.groups>`.

    The way :class:`Groupings <Grouping>` work is that each :class:`Grouping`
    :obj:`g` of an energy system is called whenever an :class:`entity
    <oemof.core.network.Entity>` is added to the energy system (and for each
    :class:`entity <oemof.core.network.Entity>` already present, if the energy
    system is created with existing enties).
    The call :obj:`g(e, groups)`, where :obj:`e` is an :class:`entity
    <oemof.core.network.Entity>` and :attr:`groups
    <oemof.core.energy_system.EnergySystem.groups>` is a dictionary mapping
    group keys to groups, then uses the three functions :meth:`key
    <Grouping.key>`, :meth:`value <Grouping.value>` and :meth:`merge
    <Grouping.merge>` in the following way:

        - :meth:`key(e) <Grouping.key>` is called to obtain a key :obj:`k`
          under which the group should be stored,
        - :meth:`value(e) <Grouping.value>` is called to obtain a value
          :obj:`v` (the actual group) to store under :obj:`k`,
        - if you supplied a :func:`filter` argument, :obj:`v` is
          :func:`filtered <builtins.filter>` using that function,
        - otherwise, if there is not yet anything stored under
          :obj:`groups[k]`, :obj:`groups[k]` is set to :obj:`v`. Otherwise
          :meth:`merge <Grouping.merge>` is used to figure out how to merge
          :obj:`v` into the old value of :obj:`groups[k]`, i.e.
          :obj:`groups[k]` is set to :meth:`merge(v, groups[k])
          <Grouping.merge>`.

    Instead of trying to use this class directly, have a look at its
    subclasses, like :class:`Nodes`, which should cater for most use cases.

    Parameters
    ----------

    key: callable

        Extract a :meth:`key <Grouping.key>` for each :class:`entity
        <oemof.core.network.Entity>` of the :class:`energy system
        <oemof.core.energy_system.EnergySystem>`.

    value: callable, optional

        Overrides the default behaviour of :meth:`value <Grouping.value>`.

    filter: callable, optional

        If supplied, whatever is returned by :meth:`value` is :func:`filtered
        <builtins.filter>` through this. See :meth:`filter` for more details.

    merge: callable, optional

        Overrides the default behaviour of :meth:`merge <Grouping.merge>`.

    """

    def __init__(self, key, filter=None, **kwargs):
        self.key = key
        self.filter = filter
        for kw in ["value", "merge", "filter"]:
            if kw in kwargs:
                setattr(self, kw, kwargs[kw])

    def key(self, e):
        """ Obtain a key under which to store the group.

        You have to supply this method yourself using the :obj:`key` parameter
        when creating :class:`Grouping` instances.

        Called for every :class:`entity <oemof.core.network.Entity>` :obj:`e`
        of the energy system. Expected to return the key (i.e. a valid
        :class:`hashable`) under which the group :meth:`value(e)
        <Grouping.value>` will be stored. If it should be added to more than
        one group, return a :class:`list` (or any other :class:`non-hashable
        <Hashable>`, :class:`iterable`) containing the group keys.

        Return :obj:`None` if you don't want to store :obj:`e` in a group.
        """
        raise NotImplementedError(
                "There is no default implementation for `Groupings.key`.\n" +
                "Congratulations, you managed to execute supposedly " +
                "unreachable code.\n" +
                "Please let us know by filing a bug at:\n\n    " +
                "https://github.com/oemof/oemof/issues\n")

    def value(self, e):
        """ Generate the group obtained from :obj:`e`.

        This methd returns the actual group obtained from :obj:`e`. Like
        :meth:`key <Grouping.key>`, it is called for every :obj:`e` in the
        energy system. If there is no group stored under :meth:`key(e)
        <Grouping.key>`, :obj:`groups[key(e)]` is set to :meth:`value(e)
        <Grouping.value>`. Otherwise :meth:`merge(value(e), groups[key(e)])
        <Grouping.merge>` is called.

        The default returns the :class:`entity <oemof.core.network.Entity>`
        itself.
        """
        return e

    def merge(self, new, old):
        """ Merge a known :obj:`old` group with a :obj:`new` one.

        This method is called if there is already a value stored under
        :obj:`group[key(e)]`. In that case, :meth:`merge(value(e),
        group[key(e)]) <Grouping.merge>` is called and should return the new
        group to store under :meth:`key(e) <Grouping.key>`.

        The default behaviour is to raise an error.
        """
        raise ValueError( "\nGrouping \n  " +
                          "{}:{}\nand\n  {}:{}\ncollides.\n".format(
                                id(old), old, id(new), new) +
                          "Possibly duplicate uids/labels?")

    def filter(self, group):
        """
        :func:`Filter <builtins.filter>` the group returned by :meth:`value`
        before storing it.

        Should return a boolean value. If the :obj:`group` returned by
        :meth:`value` is :class:`iterable <collections.abc.Iterable>`, this
        function is used (via Python's :func:`builtin filter
        <builtins.filter>`) to select the values which should be retained in
        :obj:`group`. If :obj:`group` is not :class:`iterable
        <collections.abc.Iterable>`, it is simply called on :obj:`group` itself
        and the return value decides whether :obj:`group` is stored
        (:obj:`True`) or not (:obj:`False`).

        """
        raise NotImplementedError(
                "`Groupings.filter` called without being overridden.\n" +
                "Congratulations, you managed to execute supposedly " +
                "unreachable code.\n" +
                "Please let us know by filing a bug at:\n\n    " +
                "https://github.com/oemof/oemof/issues\n")


    def __call__(self, e, d):
        k = self.key(e)
        if k is None:
            return
        v = self.value(e)
        if isinstance(v, MM):
            for k in list(filterfalse(self.filter, v)):
                v.pop(k)
        elif isinstance(v, Mapping):
            v = type(v)((k, v[k]) for k in filter(self.filter, v))
        elif isinstance(v, Iterable):
            v = type(v)(filter(self.filter, v))
        else:
            v = (self.filter or (lambda x: x))(v)
        if not v:
            return
        for group in (k if ( isinstance(k, Iterable) and not
                             isinstance(k, Hashable))
                        else [k]):
            d[group] = ( self.merge(self.value(e), d[group])
                         if group in d else self.value(e))


class Nodes(Grouping):
    """
    Modifies :class:`Grouping` to group :class:`entities
    <oemof.core.network.Entity>` into :class:`sets <set>`.
    """
    def value(self, e):
        """
        Returns a :class:`set` containing only :obj:`e`, so groups are
        :class:`sets <set>` of :class:`entities <oemof.core.network.Entity>`.
        """
        return set((e,))

    def merge(self, new, old):
        """
        :meth:`Updates <set.update>` :obj:`old` to be the union of :obj:`old`
        and :obj:`new`.
        """
        old.update(new)
        return old


def _uid_or_str(node_or_entity):
    """ Helper function to support the transition from `Entitie`s to `Node`s.
    """
    return (node_or_entity.uid if hasattr(node_or_entity, "uid")
                               else str(node_or_entity))

DEFAULT = Grouping(_uid_or_str)
""" The default :class:`Grouping`.

This one is always present in an :class:`energy system
<oemof.core.energy_system.EnergySystem>`. It stores every :class:`entity
<oemof.core.network.Entity>` under its :attr:`uid
<oemof.core.network.Entity.uid>` and raises an error if another :class:`entity
<oemof.core.network.Entity>` with the same :attr:`uid
<oemof.core.network.Entity.uid>` get's added to the :class:`energy system
<oemof.core.energy_system.EnergySystem>`.
"""

