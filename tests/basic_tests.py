try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable

from nose.tools import ok_, eq_

import pandas as pd
import logging

# from oemof.core.network.entities.components import transformers as transformer
from oemof import energy_system as es
from oemof.network import Entity
from oemof.network import Bus, Transformer
from oemof.network import Bus as NewBus, Node
from oemof.groupings import Grouping, Nodes, Flows, FlowsWithNodes as FWNs


class EnergySystem_Tests:

    @classmethod
    def setUpClass(self):
        self.timeindex = pd.date_range('1/1/2012', periods=5, freq='H')

        #timesteps=range(len(time_index)))

    def setup(self):
        self.es = es.EnergySystem()

    def test_entity_registration(self):
        eq_(Entity.registry, self.es)
        bus = Bus(label='bus-uid', type='bus-type')
        eq_(self.es.entities[0], bus)
        bus2 = Bus(label='bus-uid2', type='bus-type')
        Transformer(label='pp_gas', inputs=[bus], outputs=[bus2])
        ok_(isinstance(self.es.entities[2], Transformer))
        self.es.timeindex = self.timeindex
        ok_(len(self.es.timeindex) == 5)

    def test_entity_grouping_on_construction(self):
        bus = Bus(label="test bus")
        ES = es.EnergySystem(entities=[bus])
        ok_(ES.groups[bus.label] is bus)

    def test_that_nodes_is_a_proper_alias_for_entities(self):
        b1, b2 = Bus(label="B1"), Bus(label="B2")
        eq_(self.es.nodes, [b1, b2])
        empty = []
        self.es.nodes = empty
        ok_(self.es.entities is empty)

    def test_that_None_is_not_a_valid_group(self):
        def by_uid(n):
            if "Not in 'Group'" in n.uid:
                return None
            else:
                return "Group"
        ES = es.EnergySystem(groupings=[by_uid])

        ungrouped = [Entity(uid="Not in 'Group': {}".format(i))
                     for i in range(10)]
        grouped = [Entity(uid="In 'Group': {}".format(i))
                   for i in range(10)]
        ok_(None not in ES.groups)
        for g in ES.groups.values():
            for e in ungrouped:
                if isinstance(g, Iterable) and not isinstance(g, str):
                    ok_(e not in g)
            for e in grouped:
                if isinstance(g, Iterable) and not isinstance(g, str):
                    ok_(e in g)

    def test_defining_multiple_groupings_with_one_function(self):
        def assign_to_multiple_groups_in_one_go(n):
            g1 = n.uid[-1]
            g2 = n.uid[0:3]
            return [g1, g2]

        ES = es.EnergySystem(groupings=[assign_to_multiple_groups_in_one_go])
        entities = [ Entity(uid=("Foo: " if i % 2 == 0 else "Bar: ") +
                                 "{}".format(i) +
                                ("A" if i < 5 else "B"))
                     for i in range(10)]
        for group in ["Foo", "Bar", "A", "B"]:
            eq_(len(ES.groups[group]), 5,
                ("\n  Failed testing length of group '{}'." +
                 "\n  Expected: 5" +
                 "\n  Got     : {}" +
                 "\n  Group   : {}" ).format(
                     group, len(ES.groups[group]),
                     sorted([e.uid for e in ES.groups[group]])))

    def test_grouping_filter_parameter(self):
        g1 = Grouping( key=lambda e: "The Special One",
                       filter=lambda e: "special" in e.uid)
        g2 = Nodes( key=lambda e: "A Subset",
                    filter=lambda e: "subset" in e.uid)
        ES = es.EnergySystem(groupings=[g1, g2])
        special = Entity(uid="special")
        subset = set(Entity(uid="subset: {}".format(i)) for i in range(10))
        others = set(Entity(uid="other: {}".format(i)) for i in range(10))
        eq_(ES.groups["The Special One"], special)
        eq_(ES.groups["A Subset"], subset)

    def test_proper_filtering(self):
        """ `Grouping.filter` should not be "all or nothing".

        There was a bug where, if `Grouping.filter` returned `False` only for
        some elements of `Grouping.value(e)`, those elements where actually
        retained.
        This test makes sure that the bug doesn't resurface again.
        """
        g = Nodes( key="group", value=lambda _: set((1, 2, 3, 4)),
                   filter=lambda x: x % 2 == 0)
        ES = es.EnergySystem(groupings=[g])
        special = Entity(uid="object")
        eq_(ES.groups["group"], set((2, 4)))

    def test_non_callable_group_keys(self):
        collect_everything = Nodes(key="everything")
        g1 = Grouping( key="The Special One",
                       filter=lambda e: "special" in e.uid)
        g2 = Nodes(key="A Subset", filter=lambda e: "subset" in e.uid)
        ES = es.EnergySystem(groupings=[g1, g2, collect_everything])
        special = Entity(uid="special")
        subset = set(Entity(uid="subset: {}".format(i)) for i in range(2))
        others = set(Entity(uid="other: {}".format(i)) for i in range(2))
        everything = subset.union(others)
        everything.add(special)
        eq_(ES.groups["The Special One"], special)
        eq_(ES.groups["A Subset"], subset)
        eq_(ES.groups["everything"], everything)

    def test_constant_group_keys(self):
        """ Callable keys passed in as `constant_key` should not be called.

        The `constant_key` parameter can be used to specify callable group keys
        without having to worry about `Grouping`s trying to call them. This
        test makes sure that the parameter is handled correctly.
        """
        everything = lambda: "everything"
        collect_everything = Nodes(constant_key=everything)
        ES = es.EnergySystem(groupings=[collect_everything])
        node = Node(label="A Node")
        ok_("everything" not in ES.groups)
        ok_(everything in ES.groups)
        eq_(ES.groups[everything], set([node]))

    def test_Flows(self):
        key = object()
        ES = es.EnergySystem(groupings=[Flows(key)])
        flows = (object(), object())
        bus = NewBus(label="A Bus")
        node = Node(label="A Node",
                    inputs={bus: flows[0]}, outputs={bus: flows[1]})
        eq_(ES.groups[key], set(flows))

    def test_FlowsWithNodes(self):
        key = object()
        ES = es.EnergySystem(groupings=[FWNs(key)])
        flows = (object(), object())
        bus = NewBus(label="A Bus")
        node = Node(label="A Node",
                    inputs={bus: flows[0]}, outputs={bus: flows[1]})
        eq_(ES.groups[key], set(((bus, node, flows[0]),
                                 (node, bus, flows[1]))))

