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
        ok_(isinstance(self.es.entities[4], transformer.Simple))
        self.es.simulation = self.simulation
        ok_(len(self.es.simulation.timesteps) == 5)

    def test_entity_grouping_on_construction(self):
        bus = Bus(uid="test bus")
        ES = es.EnergySystem(entities=[bus])
        ok_(ES.groups[bus.uid] is bus)

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

