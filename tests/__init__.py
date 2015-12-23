from nose.tools import ok_, eq_

from oemof.core.energy_system import EnergySystem
from oemof.core.network import Entity
from oemof.core.network.entities import Bus


class EnergySystem_Tests:

    def test_entity_registration(self):
        ok_(Entity.registry is None)
        es = EnergySystem()
        eq_(Entity.registry, es)
        bus = Bus(uid='bus-uid', type='bus-type')
        eq_(es.entities[0], bus)

