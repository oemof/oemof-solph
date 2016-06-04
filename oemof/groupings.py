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
        - if there is not yet anything stored under :obj:`groups[k]`,
          :obj:`groups[k]` is set to :obj:`v`. Otherwise :meth:`merge
          <Grouping.merge>` is used to figure out how to merge :obj:`v` into
          the old value of :obj:`groups[k]`, i.e. :obj:`groups[k]` is set to
          :meth:`merge(v, groups[k]) <Grouping.merge>`.


    Parameters
    ----------

    key: callable
    value: callable, optional
    merge: callable, optional

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
    def __init__(self, key, **kwargs):
        self.key = key
        for kw in ["value", "merge"]:
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
                "Please file a bug at:\n\n    " +
                "https://github.com/oemof/oemof/issues\n")

    def value(self, e):
        """ Generate the group obtained from :obj:`e`.

        This methd returns the actual group obtained from :obj:`e`. Like
        :meth:`key <Grouping.key>`, it is called for every :obj:`e` in the
        energy system. If there is no group stored under :meth:`key(e)
        <Grouping.key>`, :obj:`groups[key(e)]` is set to :meth:`value(e)
        <Grouping.value>`. Otherwise :meth:`merge(value(e), groups[key(e)])
        <Grouping.merge>` is called.

        The default just wraps an entity in a list, so by default, groups are
        lists of :class:`entities <oemof.core.network.Entity>`.
        """
        return [e]

    def merge(self, new, old):
        """ Merge a known :obj:`old` group with a :obj:`new` one.

        This method is called if there is already a value stored under
        :obj:`group[key(e)]`. In that case, :meth:`merge(value(e),
        group[key(e)]) <Grouping.merge>` is called and should return the new
        group to store under :meth:`key(e) <Grouping.key>`.

        By default the list of :class:`entities <oemof.core.network.Entity>` is
        :meth:`extended <list.extend>` with :obj:`[e]`.
        """
        old.extend(new)
        return old

    def __call__(self, e, d):
        k = self.key(e)
        if k is None:
            return
        for group in (k if ( isinstance(k, Iterable) and not
                             isinstance(k, Hashable))
                        else [k]):
            d[group] = ( self.merge(self.value(e), d[group])
                         if group in d else self.value(e))



Grouping.UID = Grouping(attrgetter('uid'), value=lambda e: e,
                        merge=lambda e, d: _value_error("Duplicate uid: %s" % e.uid))


