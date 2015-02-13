from oemof.entities.base_entity import Entity


class Consumer(Entity):

    def __init__(self, entity_id, position, consumption):
        super(Consumer, self).__init__(entity_id, position)
        self.consumption = consumption