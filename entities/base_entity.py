

class Entity(object):

    def __init__(self, entity_id):
        self._id = entity_id

    def get_entity_id(self):
        return self._id

    def set_entity_id(self, entity_id):
        self._id = entity_id