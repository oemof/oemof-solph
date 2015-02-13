from oemof.entities.producer.powerplant import Powerplant


class NuclearPowerplant(Powerplant):

    def __init__(self, entity_id, position, production, nominal_power):
        super(NuclearPowerplant, self).__init__(self, entity_id, position, production, nominal_power)

    def gib_nuke(self):
        return NuclearPowerplant()