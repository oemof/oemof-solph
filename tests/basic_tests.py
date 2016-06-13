try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable

from nose.tools import ok_, eq_

import pandas as pd
import logging

from oemof.core.network.entities.components import transformers as transformer
from oemof.core import energy_system as es
from oemof.core.network import Entity
from oemof.core.network.entities import Bus, Component


class EnergySystem_Tests:

    @classmethod
    def setUpClass(self):
        time_index = pd.date_range('1/1/2012', periods=5, freq='H')

        self.simulation = es.Simulation(timesteps=range(len(time_index)))

    def setup(self):
        self.es = es.EnergySystem()

    def test_entity_registration(self):
        eq_(Entity.registry, self.es)
        bus = Bus(uid='bus-uid', type='bus-type')
        eq_(self.es.entities[0], bus)
        bus2 = Bus(uid='bus-uid2', type='bus-type')
        transformer.Simple(uid='pp_gas', inputs=[bus], outputs=[bus2])
        ok_(isinstance(self.es.entities[2], transformer.Simple))
        self.es.simulation = self.simulation
        ok_(len(self.es.simulation.timesteps) == 5)

    def test_entity_grouping_on_construction(self):
        bus = Bus(uid="test bus")
        ES = es.EnergySystem(entities=[bus])
        ok_(ES.groups[bus.uid] is bus)

    def test_that_nodes_is_a_proper_alias_for_entities(self):
        b1, b2 = Bus(uid="B1"), Bus(uid="B2")
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

        ungrouped = [ Entity(uid="Not in 'Group': {}".format(i))
                      for i in range(10)]
        grouped = [ Entity(uid="In 'Group': {}".format(i))
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
            return es.MultipleGroups(g1, g2)

        ES = es.EnergySystem(groupings=[assign_to_multiple_groups_in_one_go])
        entities = [ Entity(uid=("Foo: " if i % 2 == 0 else "Bar: ") +
                                 "{}".format(i) +
                                ("A" if i < 5 else "B"))
                     for i in range(10)]
        for group in ["Foo", "Bar", "A", "B"]:
            eq_(len(ES.groups[group]), 5)

    def test_grouping_filter_parameter(self):
        g1 = es.GroupingBase( key=lambda e: "The Special One",
                              filter=lambda e: "special" in e.uid)
        g2 = es.Grouping( key=lambda e: "A Subset",
                          filter=lambda e: "subset" in e.uid)
        ES = es.EnergySystem(groupings=[g1, g2])
        special = Entity(uid="special")
        subset = set(Entity(uid="subset: {}".format(i)) for i in range(10))
        others = set(Entity(uid="other: {}".format(i)) for i in range(10))
        eq_(ES.groups["The Special One"], special)
        eq_(ES.groups["A Subset"], subset)

