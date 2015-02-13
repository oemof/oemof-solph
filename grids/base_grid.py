from oemof.helper import Timeseries


class Grid(object):
    def __init__(self, grid_id, schema, parent_element):
        self.id = grid_id
        self.schema = schema
        self.child_list = {}
        self.inner_connection_list = {}
        self.parent = parent_element
        self.balance = Timeseries()     #Timeseries maybe boilerplate?

    def add_node(self, node_id, node_object):
        self.child_list.update({node_id: node_object})

    def add_connection(self, connection_id, connection_object):
        self.inner_connection_list.update({connection_id, connection_object})

    def remove_node_by_id(self, node_id):
        self.inner_connection_list.pop(node_id)

    def remove_connection_by_id(self, connection_id):
        self.inner_connection_list.pop(connection_id)

    def get_connections_of_specific_node(self, node):
        pass

    def get_balance(self, t, force=False):

        if force is True:
            self.balance[t] = None

        if self.balance[t] is None:
            for x in self.child_list:
                self.balance[t] += x.get_balance(t)
        return self.balance[t]


class Connection(object):

    def __init__(self, node_from, node_to, connection_id):
        self.node_from = node_from
        self.node_to = node_to
        self.id = connection_id


class Node(Grid):
    def __init__(self):
        super(Node, self).__init__(self)