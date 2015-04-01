"""

This base_grid.py module provides the base classes for constructing grids.
These grids can be used to model electrical grids, dispatch regions and their interconnections.
A grid is made of nodes and their connections.
Nodes hold the connected entities, like consumer and producer of a resource (energy, heat, ...)
Each node itself can contain a (sub-)grid, this way we are able to construct multilevel systems.

"""


from oemof.helper import Timeseries


class Grid(object):
    def __init__(self, node_id, position=None):
        self.id = node_id
        self.entity_list = {}
        self.position = position

        self.node_list = {}
        self.inner_connection_list = {}
        self.parent = None
        self.balance = Timeseries()     #Timeseries maybe boilerplate? #maybe rename it to "value"?
        self._values = {}

    def set_position(self, position):
        self.position = position

    def add_node(self,  node_object):
        """
        Adds a node-object to this Node.
        :param node_object: the node to be added.
        """
        node_object.set_parent(self)
        self.node_list[node_object.id] = node_object

    def remove_node_by_id(self, node_id):
        """
        removes a node with the given id and all its connections.
        :param node_id: the id of the node to be removed.
        """

        for (k, v) in self.inner_connection_list.items():
            if v.node_to.id == node_id or v.node_from.id == node_id:
                self.inner_connection_list.pop(k)

        self.node_list.pop(node_id)

    def add_connection(self,  connection_object):
        """
        adds a connection to the node. This connection has to be connected to 2 node within this grid.
        :param connection_object: the connection to be added.
        """
        self.inner_connection_list[connection_object.id] = connection_object

    def remove_connection_by_id(self, connection_id):
        """
        removes a connection with the given id.
        :param connection_id: the id of the connection to be removed.
        """
        self.inner_connection_list.pop(connection_id)

    def get_connections_of_specific_node(self, node):
        """
        returns all connections from and to a given node.
        :param node: the node, you want to get the connections of.
        :return: list of connections.
        """

        return {k: v for k, v in self.inner_connection_list.items()
                if v.node_from == node or v.node_to == node}

    def get_parent(self):
        """
        Used to retrieve the parent element.
        :return: The parent Node
        """
        return self.parent

    def set_parent(self, parent):
        """
        changes the currents parent-pointer
        :param parent: the new parent
        """
        self.parent = parent

    def remove_from_parent(self):
        """
        removes itself from the parent element
        :return:
        """
        self.parent.remove_node_by_id(self.id)
        self.parent = None

    def add_entity(self, entity_object):
        """
        adds an entity to this node.
        :param entity_object:  the entity to add.
        """
        entity_object.set_parent(self)
        self.entity_list[entity_object.id] = entity_object

    def get_own_entities(self):
        """
        get all entities connected to this entity.
        TODO: is it smarter to return a copy of the list instead of the original object=.
        :return: entity-List.
        """
        return self.entity_list

    def get_all_entities(self):
        """
        get all entities connected to this node and all its ancestors.
        :return: entity-List.
        """

        entities = dict(self.entity_list)

        for (id, node) in self.node_list.items():
            entities.update(node.get_all_entities())

        return entities

    def get_balance(self, timestep, force_recalculation=False):
        """
        gets the "balance" of a given grid/node for the given timestep. The balance is the product (positive value) or the
        consumption (negative value) of this element.
        If this Element has child elements, its balance is the sum of its children balances.
        Once this calculation has been done, it will be buffered inside this element.
        :param timestep: the timestep you need the balance for.
        :param force_recalculation: set to True, if you want all buffered calculations to be redone.
        :return: the balance value
        """

        if force_recalculation is True:
            self.balance[timestep] = None

        if self.balance[timestep] is None:
            for x in self.node_list:
                self.balance[timestep] += x.get_balance(timestep)
        return self.balance[timestep]

    def __setitem__(self, key, item):
        """
        use the dictionary-like notation for setting computevalues of a Node.

        eg: node["oilprice"] = TimeSeries().

        will set the WSS-Field to be a Timeseries-Object (a dict).

        node["cost"][i] = node["oilprice"][i] * node["output"][i].


        :param key: The name of the field.
        :param item: The new Value
        """
        self._values[key] = item

    def __getitem__(self, key):
        """
        Use the dictionary-like notation for getting and setting compute values of a Node.

        node["cost"][i] = node["oilprice"][i] * node["output"][i].

        If this node doesnt have this value, it will try to get the value from the parent.
        The search will go up the Graph to the root element. Of none of these elements has the key set,
        it will return None.
        :param key: The key
        :return: value if this or one of the ancestor-elements have this field. Otherwise None.
        """
        try:
            return self._values[key]
        except LookupError:
            try:
                return self.parent[key]
            except LookupError:
                return None


class Connection(object):
    """
    Connection object, which holds references for the two nodes that are connected
    :param node_from: Node from where the connection starts
    :param node_to: Node to where the connection ends
    :param connection_id: unique id for each connection
    """
    def __init__(self, node_from, node_to, connection_id):
        self.node_from = node_from
        self.node_to = node_to
        self.id = connection_id