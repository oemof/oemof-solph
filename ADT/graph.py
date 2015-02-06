__author__ = 'stfn'


class Graph(object):
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def add_vertex(self, key):
        self.numVertices += 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def get_vertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList

    def add_edge(self, f, t, edge=None):
        if f not in self.vertList:
            nv = self.add_vertex(f)
        if t not in self.vertList:
            nv = self.add_vertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], edge)

    def get_vertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())



class Vertex(object):
    def __init__(self, key, type):
        self.id = key
        self.connectedTo = {}
        self.type = type

    def add_neighbor(self, nbr, edge=None):
        self.connectedTo[nbr] = edge

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def get_connections(self):
        return self.connectedTo.keys()

    def get_id(self):
        return self.id

    def get_edge(self, nbr):
        return self.connectedTo[nbr]

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

class Edge(object):

    def __init__(self):
        self._weight = 0;

    def __init__(self, weight):
        self._weight = weight