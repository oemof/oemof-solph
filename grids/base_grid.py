class Grid(object):
    def __init__(self, schema):
        self.schema = schema
        self.node_list = {}
        self.connection_list = {}

    def add_node(self, node_id, node_object):
        self.node_list.update({node_id: node_object})

    def add_connection(self, connection_id, connection_object):
        self.connection_list.update({connection_id, connection_object})

    def remove_node_by_id(self, node_id):
        self.connection_list.pop(node_id)

    def remove_connection_by_id(self, connection_id):
        self.connection_list.pop(connection_id)

    def get_connections_of_specific_node(self, node):
        for key, in self.connection_list:
            if (connection.node_from or connection.node_to) == node:
                pass


class Connection(object):

    def __init__(self, node_from, node_to):
        self.node_from = node_from
        self.node_to = node_to


class Node(Grid):
    def __init__(self):
        super(Node, self).__init__(self)
        self.entity_list = []