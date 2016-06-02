""" All you need to create groups of stuff in your energy system.
"""
try:
    from collections.abc import Hashable, Iterable
except ImportError:
    from collections import Hashable, Iterable
from operator import attrgetter


def _value_error(s):
    """ Helper function to be able to `raise ValueError` as an expression.
    """
    raise ValueError(s)

class Grouping:
    """
    Used to aggregate :class:`entities <oemof.core.network.Entity>` in an
    :class:`energy system <oemof.core.energy_system.EnergySystem>` into
    :attr:`groups <oemof.core.energy_system.EnergySystem.groups>`.

    Parameters
    ----------

    key: callable
        Called for every :class:`entity <oemof.core.network.Entity>` `e` of the
        energy system with `e` as the sole argument. Should return the key of
        the group that `e` should be added to. If `e` should be added to more
        than one group, return a `list` (or any other non-hashable, iterable)
        containing the group keys.
        Return `None` if you don't want to store a group for a specific `e`.
    value: callable, optional
        A function that should return the actual group obtained from `e`. Like
        `key`, this is called for every `e` in the energy system, with `e` as
        the sole argument. If there is no group stored under `key(e)`,
        `value(e)` will be stored in `groups[key(e)]`. Otherwise
        `merge(value(e), groups[key(e)])` will be called.
        The default just wraps an entity in a list, so by default, groups are
        lists of :class:`entities <oemof.core.network.Entity>`.
    merge: callable, optional
        This function is called if `group[key(e)]` already exists. In that
        case, `merge(value(e), group[key(e)])` is called and should return the
        new group to store under `key(e)`.
        By default the list of :class:`entities <oemof.core.network.Entity>` is
        :meth:`extended <list.extend>` with `[e]`.

    """

    @staticmethod
    def create(argument):
        if isinstance(argument, Grouping):
            return argument
        if callable(argument):
            return Grouping(argument)
        raise NotImplementedError(
                "Can only create Groupings from Groupings and callables for now.\n" +
                "  Please add a comment to https://github.com/oemof/oemof/issues/60\n" +
                "  If you stumble upon this as this feature is currently being\n" +
                "  developed and any input on how you expect it to work would be\n" +
                "  appreciated")

    #: The default grouping, which is always present in addition to user
    #: defined ones. Stores every :class:`entity <oemof.core.network.Entity>`
    #: in a group of its own under its :attr:`uid
    #: <oemof.core.network.Entity.uid>` and raises an error if another
    #: :class:`entity <oemof.core.network.Entity>` with the same :attr:`uid
    #: <oemof.core.network.Entity.uid>` get's added to the energy system.
    UID = None
    def __init__(self, key, value=lambda e: [e],
                 merge=lambda new, old: old.extend(new) or old,
                 insert=None):
        if insert:
            self._insert = insert
            return
        def insert(e, d):
            k = key(e)
            if k is None:
                return
            for group in (k if ( isinstance(k, Iterable) and not
                                 isinstance(k, Hashable))
                            else [k]):
                d[group] = merge(value(e), d[group]) if group in d else value(e)

        self._insert = insert

    def __call__(self, e, d):
        self._insert(e, d)

Grouping.UID = Grouping(attrgetter('uid'), value=lambda e: e,
                        merge=lambda e, d: _value_error("Duplicate uid: %s" % e.uid))


