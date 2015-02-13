from oemof.entities.producer.powerplant import Powerplant

class PhotovoltaicPowerplant:

    def __init__(self, entity_id, position, production, nominal_power, sun_curve):
        super(self).__init__(self, entity_id, position, production, nominal_power)
        self.sun_curve = sun_curve