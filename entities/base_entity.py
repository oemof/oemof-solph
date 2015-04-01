from oemof.helper import Timeseries


class Entity(object):

    def __init__(self, entity_id, position=None):
        self.id = entity_id
        self.position = position
        self.parent = None
        self._values = {}

    def get_parent(self):
        """
        Used to retrieve the parent element.
        :return: The parent Node/Grid
        """
        return self.parent

    def set_parent(self, parent):
        """
        changes the currents parent-pointer
        :param parent: the new parent
        """
        self.parent = parent


    def __setitem__(self, key, item):
        """
        use the dictionary-like notation for getting and setting computevalues of an entity.

        eg: entity["WSS"] = TimeSeries().

        will set the WSS-Field to be a Timeseries-Object (a dict).

        entity["output"][i] = entity["WSS"][i] * 5.


        :param key: The name of the field.
        :param item: The new Value
        """
        self._values[key] = item

    def __getitem__(self, key):
        """
        Use the dictionary-like notation for getting and setting computevalues of an entity.

        entity["output"][i] = entity["WSS"][i] * 5.


        If this entity doesnt have this value, it will try to get the value from the parent.
        The search will go up the Graph to the root element. Of none of these elements has the key set,
        it will return None.
        :param key: The key
        :return: value if this or one of the ancestor-elements have this field. Otherwise None.
        """
        try:
            return self._values[key]
        except Exception:
            return self.parent[key]
