from entities.producer.base_producer import Producer


class Powerplant(Producer):

    def __init__(self, entity_id, position, production, nominal_power):
        super(self).__init__(entity_id, position, production)
        self.nominal_power = nominal_power