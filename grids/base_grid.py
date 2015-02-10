class Grid(object):
    def __init__(self):
        self.node_list = []

    def add_node(self, node):
        self.node_list.append(node)


class Connection(object):
    pass


class Node(Grid):
    def __init__(self):
        super(Node, self).__init__(self)