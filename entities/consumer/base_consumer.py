from entities.base_entity import Entity


class Consumer(Entity):

    def __init__(self, entity_id, consumption):
        self._id = entity_id
        self._consumption = consumption

    def get_consumption(self):
        return self._consumption

    def set_consumption(self, consumption):
        self._consumption = consumption

