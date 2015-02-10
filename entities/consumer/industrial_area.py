from entities.consumer.base_consumer import Consumer


class IndustrialArea(Consumer):

    def __init__(self, entity_id, position, consumption):
        super(IndustrialArea, self).__init__(entity_id, position)