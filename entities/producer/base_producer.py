from entities.base_entity import Entity


class Producer(Entity):

    def __init__(self, entity_id, production):
        self._id = entity_id
        self._production = production

    def get_production(self):
        return self._production

    def set_production(self, production):
        self._production = production


