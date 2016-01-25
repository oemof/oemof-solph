from nose.tools import ok_, eq_

import pandas as pd

from oemof.core.network.entities.components import transformers as transformer
from oemof.core import energy_system as es
from oemof.core.network import Entity
from oemof.core.network.entities import Bus


class EnergySystem_Tests:

    @classmethod
    def setUpClass(self):
        time_index = pd.date_range('1/1/2012', periods=5, freq='H')

        self.simulation = es.Simulation(
            timesteps=range(len(time_index)), solver='glpk')

    def test_entity_registration(self):
        ok_(Entity.registry is None)
        ensys = es.EnergySystem()
        eq_(Entity.registry, ensys)
        bus = Bus(uid='bus-uid', type='bus-type')
        eq_(ensys.entities[0], bus)
        bus2 = Bus(uid='bus-uid2', type='bus-type')
        transformer.Simple(uid='pp_gas', inputs=[bus], outputs=[bus2])
        ok_(isinstance(ensys.entities[2], transformer.Simple))
        ensys.simulation = self.simulation
        ok_(len(ensys.simulation.timesteps) == 5)
