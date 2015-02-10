from entities.producer.powerplant import Powerplant


class WindPowerplant(Powerplant):

    def __init__(self, entity_id, position, production, nominal_power, model_name):
        super(self).__init__(entity_id, position, production, nominal_power)
        self.model_name = model_name
        self.wind_curve = None

    def recalculate_production(self, time):
        if self.wind_curve is None:
            return "No windcurve defined"
        else:
            pass


