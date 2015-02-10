from entities.base_entity import Entity


class Producer(Entity):

    def __init__(self, entity_id, position, production):
        super(self).__init__(entity_id, position)
        self._production = production

    def get_production(self):
        return self._production

    def set_production(self, production):
        self._production = production