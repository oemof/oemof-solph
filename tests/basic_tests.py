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

    def test_entity_registration(self):
        ensys = es.EnergySystem()
        eq_(Entity.registry, ensys)
        bus = Bus(uid='bus-uid', type='bus-type')
        eq_(ensys.entities[0], bus)
        bus2 = Bus(uid='bus-uid2', type='bus-type')
        transformer.Simple(uid='pp_gas', inputs=[bus], outputs=[bus2])
        ok_(isinstance(ensys.entities[4], transformer.Simple))
        ensys.simulation = self.simulation
        ok_(len(ensys.simulation.timesteps) == 5)

    def test_entity_grouping_on_construction(self):
        bus = Bus(uid="test bus")
        ES = es.EnergySystem(entities=[bus])
        ok_(ES.groups[bus.uid] is bus)

