"""
This module contains the base-entity-class.
inherit from this class to build more complex entities, like powerplants and consumers.

At the moment, the (output-)calculations for each entity happen within the feedinlib.
It may be a good idea, to implement the "_apply_model()"-Code directly in the inherited entities.


"""

class Entity(object):
    """
    This class should be the parent class of all you entity-implementations, like powerplants.
    This class is designed for entities "living" inside a graph structure: the grid.
    Every entity has a parent-node to which it belongs and a space for user-defined data, like windspeed- or
    output-timeseries, dimensions etc.
    All these fields can be accessed via the dictionary-notation:
    h = entity["hub_height"]
    entity["output"] = entity["wss"] * entity["eex_day_ahead"]
    These fields will be used at entity creation and will be filled with all the data, tha is provided in the DB or csv.
    If you try to read from a field, that doesnt exit inside the entity, it will ask it's parent node for this value.
    This will go up the hierarchy until the value is found. Using this technique, we can define different energy prices
    for different nodes, for example, end every entity inside this grid will automatically access the correct price data.
    If you write to a field, that does not exist, it will be created.

    Use these fields inside your _apply_model function and inside the solver, read entity-specific data and write to it.
    This way, we will be able to track our data over the whole simulation and output any field we want afterwards.
    """
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
