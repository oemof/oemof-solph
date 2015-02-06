__author__ = 'stfn'
"""
graph.py
Author: steffen Peleikis

This module contains the Graph-ADT.

Graphs can be used to implement grids.
"""

class Graph(object):
    """
    Implements Graphs made of Vertices and Edges.
        Inherit from here to implement special graphs like grids.
    """
    def __init__(self):
        """
        Empty constructor. Creates an empty graph.
        """
        self.vertList = {}
        self.numVertices = 0

    def create_vertex(self, id, type):
        """
        creates a new vertex and adds it to the graph.
        :param id: the vertex id.
        :param type: the vertex-type
        :return: the new vertex
        """
        self.numVertices += 1
        newVertex = Vertex(id, type)
        self.vertList[id] = newVertex
        return newVertex

    def add_vertex(self, vertex):
        """
        adds an existing vertex to the graph.
        :param vertex: the vertex to be added.
        """
        self.numVertices += 1
        self.vertList[vertex.id] = vertex


    def get_vertex(self, id):
        """
        finds a vertex with the given id in the graph.
        :param id: the id to find.
        :return: the found vertex.
        """
        if id in self.vertList:
            return self.vertList[id]
        else:
            return None

    def __contains__(self, id):
        """
        checks if the vertex with the given id exists within the graph.
        :param id: the id to check.
        :return: true if found, false if not.
        """
        return id in self.vertList



    def add_edge(self, f, t, edge=None):
        """
        adds an edge between to vertices.
        if a vertex does not exist in the graph yet, it will be added.
        :param f: the first vertex to connect the edge to.
        :param t: the second vertex to connect the edge to.
        :param edge: the edge-object to add. None if just an abstract connection with no further information
            will be added.
        """
        if f not in self.vertList:
            nv = self.add_vertex(f)
        if t not in self.vertList:
            nv = self.add_vertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], edge)

    def get_vertices(self):
        """
        get all vertices of this graph.
        :return: list of vertices.
        """
        return self.vertList.values()

    def __iter__(self):
        """
        iterator.
        :return: next element.
        """
        return iter(self.vertList.values())


class Vertex(object):
    """
    Implements a Vertex that can be added to a graph.
    """
    def __init__(self, id, type):
        """
        default constructor of a vertex
        :param id: vertex id
        :param type: vertex type
        """
        self.id = id
        self.connectedTo = {}
        self.type = type

    def add_neighbor(self, vertex, edge=Edge()):
        """
        adds an edge between this vertex and the vertex provided.
        :param vertex: the vertex to add a connection to.
        :param edge: the edge object. adds abstract edge if no edge provided.
        :return:
        """

        self.connectedTo[vertex] = edge;

    def __str__(self):
        """
        to-string overload
        :return: the string
        """
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def get_connections(self):
        """
        get all vertices connected to this vertex.
        :return: list of vertices
        """
        return self.connectedTo.keys()

    def get_id(self):
        """
        get the own vertex-id.
        :return: the vertex id
        """
        return self.id

    def get_edge(self, vertex):
        """
        get an edge bewteen this vertex and the vertex provided.
        :param vertex: the vertex the get the edge to.
        :return: the edge.
        """
        return self.connectedTo[vertex]

    def get_type(self):
        """
        gets the type of this vertex.
        :return: type.
        """
        return self.type

    def set_type(self, type):
        """
        sets the type of this vertex.
        :param type: the type.
        """
        self.type = type


class Edge(object):
    """
    defines and edge between to vertices.
    inherit from here to implement further functionality.
    """
    def __init__(self):
        """
        base constructor for an empty egde.
        """
        self._weight = 0;

    def __init__(self, weight):
        """
        constructor for basic adges with weight.
        :param weight: the weight of this edge.
        """
        self._weight = weight