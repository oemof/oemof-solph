from entities.consumer.base_consumer import Consumer


class City(Consumer):

    def __init__(self, entity_id, position, consumption):
        super(self).__init__(entity_id, position, consumption)