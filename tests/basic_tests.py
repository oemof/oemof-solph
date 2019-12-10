# -*- coding: utf-8 -

"""Basic tests.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/basic_tests.py

SPDX-License-Identifier: MIT
"""
try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable
from pprint import pformat

from nose.tools import ok_, eq_
import pandas as pd

from oemof import energy_system as es
from oemof.network import Bus, Transformer
from oemof.network import Bus as NewBus, Node, temporarily_modifies_registry
from oemof.groupings import Grouping, Nodes, Flows, FlowsWithNodes as FWNs


class TestsEnergySystem:

    @classmethod
    def setUpClass(cls):
        cls.timeindex = pd.date_range('1/1/2012', periods=5, freq='H')

    def setup(self):
        self.es = es.EnergySystem()
        Node.registry = self.es

    def test_entity_registration(self):
        bus = Bus(label='bus-uid', type='bus-type')
        eq_(self.es.nodes[0], bus)
        bus2 = Bus(label='bus-uid2', type='bus-type')
        eq_(self.es.nodes[1], bus2)
        t1 = Transformer(label='pp_gas', inputs=[bus], outputs=[bus2])
        ok_(t1 in self.es.nodes)
        self.es.timeindex = self.timeindex
        ok_(len(self.es.timeindex) == 5)

    def test_entity_grouping_on_construction(self):
        bus = Bus(label="test bus")
        ensys = es.EnergySystem(entities=[bus])
        ok_(ensys.groups[bus.label] is bus)

    def test_that_nodes_is_a_proper_alias_for_entities(self):
        b1, b2 = Bus(label="B1"), Bus(label="B2")
        eq_(self.es.nodes, [b1, b2])
        empty = []
        self.es.nodes = empty
        ok_(self.es.entities is empty)


    def test_that_none_is_not_a_valid_group(self):
        def by_uid(n):
            if "Not in 'Group'" in n.uid:
                return None
            else:
                return "Group"

        ensys = es.EnergySystem(groupings=[by_uid])

        ungrouped = [Entity(uid="Not in 'Group': {}".format(i))
                     for i in range(10)]
        grouped = [Entity(uid="In 'Group': {}".format(i))
                   for i in range(10)]
        ok_(None not in ensys.groups)
        for g in ensys.groups.values():
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

        ensy = es.EnergySystem(groupings=[assign_to_multiple_groups_in_one_go])
        Node.registry = ensy
        [Node(label=("Foo: " if i % 2 == 0 else "Bar: ") +
              "{}".format(i) + ("A" if i < 5 else "B")) for i in
         range(10)]
        for group in ["Foo", "Bar", "A", "B"]:
            eq_(len(ensy.groups[group]), 5,
                ("\n  Failed testing length of group '{}'." +
                 "\n  Expected: 5" +
                 "\n  Got     : {}" +
                 "\n  Group   : {}").format(
                    group, len(ensy.groups[group]),
                    sorted([e.label for e in ensy.groups[group]])))

    def test_grouping_filter_parameter(self):
        g1 = Grouping(key=lambda e: "The Special One",
                      filter=lambda e: "special" in str(e))
        g2 = Nodes(key=lambda e: "A Subset",
                   filter=lambda e: "subset" in str(e))
        ensys = es.EnergySystem(groupings=[g1, g2])
        special = Node(label="special")
        subset = set(Node(label="subset: {}".format(i)) for i in range(10))
        others = set(Node(label="other: {}".format(i)) for i in range(10))
        ensys.add(special, *subset)
        ensys.add(*others)
        eq_(ensys.groups["The Special One"], special)
        eq_(ensys.groups["A Subset"], subset)

    def test_proper_filtering(self):
        """ `Grouping.filter` should not be "all or nothing".

        There was a bug where, if `Grouping.filter` returned `False` only for
        some elements of `Grouping.value(e)`, those elements where actually
        retained.
        This test makes sure that the bug doesn't resurface again.
        """
        g = Nodes(key="group", value=lambda _: {1, 2, 3, 4},
                  filter=lambda x: x % 2 == 0)
        ensys = es.EnergySystem(groupings=[g])
        special = Node(label="object")
        ensys.add(special)
        eq_(ensys.groups["group"], {2, 4})

    def test_non_callable_group_keys(self):
        collect_everything = Nodes(key="everything")
        g1 = Grouping(key="The Special One",
                      filter=lambda e: "special" in e.label)
        g2 = Nodes(key="A Subset", filter=lambda e: "subset" in e.label)
        ensys = es.EnergySystem(groupings=[g1, g2, collect_everything])
        special = Node(label="special")
        subset = set(Node(label="subset: {}".format(i)) for i in range(2))
        others = set(Node(label="other: {}".format(i)) for i in range(2))
        everything = subset.union(others)
        everything.add(special)
        ensys.add(*everything)
        eq_(ensys.groups["The Special One"], special)
        eq_(ensys.groups["A Subset"], subset)
        eq_(ensys.groups["everything"], everything)

    def test_grouping_laziness(self):
        """ Energy system `groups` should be fully lazy.

        `Node`s added to an energy system should only be tested for and put
        into their respective groups right before the `groups` property of an
        energy system is accessed.
        """
        group = "Group"
        g = Nodes(key=group, filter=lambda n: getattr(n, "group", False))
        self.es = es.EnergySystem(groupings=[g])
        buses = [Bus("Grouped"), Bus("Ungrouped one"), Bus("Ungrouped two")]
        self.es.add(buses[0])
        buses[0].group = True
        self.es.add(*buses[1:])
        ok_(
            group in self.es.groups,
            "\nExpected to find\n\n  `{!r}`\n\nin `es.groups`.\nGot:\n\n  `{}`"
            .format(
                group,
                "\n   ".join(pformat(set(self.es.groups.keys())).split("\n")),
            ),
        )
        ok_(
            buses[0] in self.es.groups[group],
            "\nExpected\n\n  `{}`\n\nin `es.groups['{}']`:\n\n  `{}`"
            .format(
                "\n   ".join(pformat(buses[0]).split("\n")),
                group,
                "\n   ".join(pformat(self.es.groups[group]).split("\n"))
            ),
        )

    @temporarily_modifies_registry
    def test_constant_group_keys(self):
        """ Callable keys passed in as `constant_key` should not be called.

        The `constant_key` parameter can be used to specify callable group keys
        without having to worry about `Grouping`s trying to call them. This
        test makes sure that the parameter is handled correctly.
        """
        everything = lambda: "everything"
        collect_everything = Nodes(constant_key=everything)
        ensys = es.EnergySystem(groupings=[collect_everything])
        Node.registry = ensys
        node = Node(label="A Node")
        ok_("everything" not in ensys.groups)
        ok_(everything in ensys.groups)
        eq_(ensys.groups[everything], {node})

    @temporarily_modifies_registry
    def test_flows(self):
        key = object()
        ensys = es.EnergySystem(groupings=[Flows(key)])
        Node.registry = ensys
        flows = (object(), object())
        bus = NewBus(label="A Bus")
        Node(label="A Node", inputs={bus: flows[0]}, outputs={bus: flows[1]})
        eq_(ensys.groups[key], set(flows))

    @temporarily_modifies_registry
    def test_flows_with_nodes(self):
        key = object()
        ensys = es.EnergySystem(groupings=[FWNs(key)])
        Node.registry = ensys
        flows = (object(), object())
        bus = NewBus(label="A Bus")
        node = Node(label="A Node",
                    inputs={bus: flows[0]}, outputs={bus: flows[1]})
        eq_(ensys.groups[key], {(bus, node, flows[0]), (node, bus, flows[1])})

    def test_that_node_additions_are_signalled(self):
        """
        When a node gets `add`ed, a corresponding signal should be emitted.
        """
        node = Node(label="Node")

        def subscriber(sender, **kwargs):
            ok_(sender is node)
            ok_(kwargs['EnergySystem'] is self.es)
            subscriber.called = True

        subscriber.called = False

        es.EnergySystem.signals[es.EnergySystem.add].connect(
            subscriber, sender=node
        )
        self.es.add(node)
        ok_(
            subscriber.called,
            (
                "\nExpected `subscriber.called` to be `True`.\n"
                "Got {}.\n"
                "Probable reason: `subscriber` didn't get called."
            ).format(subscriber.called),
        )
