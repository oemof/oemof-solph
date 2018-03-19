# -*- coding: utf-8 -

"""Basic tests.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/basic_tests.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable

from nose.tools import ok_, eq_
import pandas as pd

from oemof import energy_system as es
from oemof.network import Entity
from oemof.network import Bus, Transformer
from oemof.network import Bus as NewBus, Node, temporarily_modifies_registry
from oemof.groupings import Grouping, Nodes, Flows, FlowsWithNodes as FWNs


class EnergySystem_Tests:

    @classmethod
    def setUpClass(self):
        self.timeindex = pd.date_range('1/1/2012', periods=5, freq='H')

        #timesteps=range(len(time_index)))

    def setup(self):
        self.es = es.EnergySystem()
        Node.registry = self.es

    def test_entity_registration(self):
        bus = Bus(label='bus-uid', type='bus-type')
        eq_(self.es.nodes[0], bus)
        bus2 = Bus(label='bus-uid2', type='bus-type')
        Transformer(label='pp_gas', inputs=[bus], outputs=[bus2])
        ok_(isinstance(self.es.nodes[2], Transformer))
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

    @temporarily_modifies_registry
    def test_defining_multiple_groupings_with_one_function(self):
        def assign_to_multiple_groups_in_one_go(n):
            g1 = n.label[-1]
            g2 = n.label[0:3]
            return [g1, g2]

        ES = es.EnergySystem(groupings=[assign_to_multiple_groups_in_one_go])
        Node.registry = ES
        nodes = [ Node(label=("Foo: " if i % 2 == 0 else "Bar: ") +
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
                     sorted([e.label for e in ES.groups[group]])))

    def test_grouping_filter_parameter(self):
        g1 = Grouping( key=lambda e: "The Special One",
                       filter=lambda e: "special" in str(e))
        g2 = Nodes( key=lambda e: "A Subset",
                    filter=lambda e: "subset" in str(e))
        ES = es.EnergySystem(groupings=[g1, g2])
        special = Node(label="special")
        subset = set(Node(label="subset: {}".format(i)) for i in range(10))
        others = set(Node(label="other: {}".format(i)) for i in range(10))
        ES.add(special, *subset)
        ES.add(*others)
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
        special = Node(label="object")
        ES.add(special)
        eq_(ES.groups["group"], set((2, 4)))

    def test_non_callable_group_keys(self):
        collect_everything = Nodes(key="everything")
        g1 = Grouping( key="The Special One",
                       filter=lambda e: "special" in e.label)
        g2 = Nodes(key="A Subset", filter=lambda e: "subset" in e.label)
        ES = es.EnergySystem(groupings=[g1, g2, collect_everything])
        special = Node(label="special")
        subset = set(Node(label="subset: {}".format(i)) for i in range(2))
        others = set(Node(label="other: {}".format(i)) for i in range(2))
        everything = subset.union(others)
        everything.add(special)
        ES.add(*everything)
        eq_(ES.groups["The Special One"], special)
        eq_(ES.groups["A Subset"], subset)
        eq_(ES.groups["everything"], everything)

    @temporarily_modifies_registry
    def test_constant_group_keys(self):
        """ Callable keys passed in as `constant_key` should not be called.

        The `constant_key` parameter can be used to specify callable group keys
        without having to worry about `Grouping`s trying to call them. This
        test makes sure that the parameter is handled correctly.
        """
        everything = lambda: "everything"
        collect_everything = Nodes(constant_key=everything)
        ES = es.EnergySystem(groupings=[collect_everything])
        Node.registry = ES
        node = Node(label="A Node")
        ok_("everything" not in ES.groups)
        ok_(everything in ES.groups)
        eq_(ES.groups[everything], set([node]))

    @temporarily_modifies_registry
    def test_Flows(self):
        key = object()
        ES = es.EnergySystem(groupings=[Flows(key)])
        Node.registry = ES
        flows = (object(), object())
        bus = NewBus(label="A Bus")
        node = Node(label="A Node",
                    inputs={bus: flows[0]}, outputs={bus: flows[1]})
        eq_(ES.groups[key], set(flows))

    @temporarily_modifies_registry
    def test_FlowsWithNodes(self):
        key = object()
        ES = es.EnergySystem(groupings=[FWNs(key)])
        Node.registry = ES
        flows = (object(), object())
        bus = NewBus(label="A Bus")
        node = Node(label="A Node",
                    inputs={bus: flows[0]}, outputs={bus: flows[1]})
        eq_(ES.groups[key], set(((bus, node, flows[0]),
                                 (node, bus, flows[1]))))

