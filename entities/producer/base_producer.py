from oemof.entities.base_entity import Entity


class Producer(Entity):

    def __init__(self, entity_id, position, production):
        super(self).__init__(entity_id, position)
        self.production = production
