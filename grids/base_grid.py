"""

This base_grid.py module provides the base classes for constructing grids.
These grids can be used to model electrical grids, dispatch regions and their interconnections.
A grid is made of nodes and their connections.
Nodes hold the connected entities, like consumer and producer of a resource (energy, heat, ...)
Each node itself can contain a (sub-)grid, this way we are able to construct multilevel systems.

"""


from oemof.helper import Timeseries


class Grid(object):
    def __init__(self, grid_id, parent_element=None, schema=None):
        self.id = grid_id
        self.schema = schema
        self.child_list = {}
        self.inner_connection_list = {}
        self.parent = parent_element
        self.balance = Timeseries()     #Timeseries maybe boilerplate? #maybe rename it to "value"?


    def add_node(self,  node_object):
        """
        Adds a node-object to this grid.
        :param node_object: the node to be added.
        """
        self.child_list[node_object.id] = node_object

    def add_connection(self,  connection_object):
        """
        adds a connection to the grid. This connection has to be connected to 2 node within this grid.
        :param connection_object: the connection to be added.
        """
        self.inner_connection_list[connection_object.id] = connection_object

    def remove_node_by_id(self, node_id):
        """
        removes a node with the given id and all its connections.
        :param node_id: the id of the node to be removed.
        """

        for (k, v) in self.inner_connection_list.items():
            if v.node_to.id == node_id or v.node_from.id == node_id:
                self.inner_connection_list.pop(k)

        self.child_list.pop(node_id)

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
        :return: The parent Node/Grid
        """
        return self.parent


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
            for x in self.child_list:
                self.balance[timestep] += x.get_balance(timestep)
        return self.balance[timestep]


class Connection(object):

    def __init__(self, node_from, node_to, connection_id):
        self.node_from = node_from
        self.node_to = node_to
        self.id = connection_id


class Node(Grid):
    def __init__(self, node_id, parent, schema=None):
        super(Node, self).__init__(node_id, parent, schema)

    def remove_from_grid(self):
        self.parent.remove_node_by_id(self.id)