# -*- coding: utf-8 -*-
""" list:  Groupings needed on an energy system for it to work with solph.

If you want to use solph on an energy system, you need to create it with these
groupings specified like this:

    .. code-block: python

    from oemof.network import EnergySystem
    import solph

    energy_system = EnergySystem(groupings=solph.GROUPINGS)

"""

__copyright__ = "oemof developer group"
__license__ = "GPLv3"

from oemof.solph.network import Bus, Transformer
from oemof.solph import blocks
import oemof.groupings as groupings


def constraint_grouping(node):
    """Grouping function for constraints.

    This function can be passed in a list to :attr:`groupings` of
    :class:`oemof.solph.network.EnergySystem`.
    """
    # TODO: Refactor this for looser coupling between modules.
    # This code causes an unwanted tight coupling between the `groupings` and
    # `network` modules, resulting in having to do an import at runtime in the
    # init method of solph's `EnergySystem`. A better way would be to add a
    # method (maybe `constraints`, `constraint_group`, `constraint_type` or
    # something like that) to solph's node hirarchy, which gets overriden in
    # each subclass to return the appropriate value. Then we can just call the
    # method here.
    # This even gives other users/us the ability to customize/extend how
    # constraints are grouped by overriding the method in future subclasses.
    if isinstance(node, Bus) and node.balanced:
        return blocks.Bus
    if type(node) == Transformer:
        return blocks.Transformer


investment_flow_grouping = groupings.FlowsWithNodes(
    constant_key=blocks.InvestmentFlow,
    # stf: a tuple consisting of (source, target, flow), so stf[2] is the flow.
    filter=lambda stf: stf[2].investment is not None)

standard_flow_grouping = groupings.FlowsWithNodes(
    constant_key=blocks.Flow)

nonconvex_flow_grouping = groupings.FlowsWithNodes(
    constant_key=blocks.NonConvexFlow,
    filter=lambda stf: stf[2].nonconvex is not None)


GROUPINGS = [constraint_grouping, investment_flow_grouping,
             standard_flow_grouping, nonconvex_flow_grouping]
