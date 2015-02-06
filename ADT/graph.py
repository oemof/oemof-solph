"""
graph.py.
Author: steffen Peleikis.

This module contains the Graph-ADT.

L{Graphs<Graph>} can be used to implement grids.
They are made of L{vertices<Vertex>} and L{edges<Edge>}.
"""


class Edge(object):
    """
    defines and edge between to L{vertices<Vertex>}.
    inherit from here to implement further functionality.
    """
    def __init__(self, weight=0):
        """
        base constructor for an empty edge.
        """
        self._weight = weight


class Graph(object):
    """
    Implements Graphs made of L{Vertices<ADT.Vertex>} and L{Edges<Edge>}.
    Inherit from here to implement special graphs like grids.
    """
    def __init__(self):
        """
        Empty constructor. Creates an empty graph.
        """
        self.vertice_list = {}
        self.num_vertices = 0

    def create_vertex(self, vertex_id, vertex_type):
        """
        creates a new L{Vertex} and adds it to the graph.
        :param vertex_id: the vertex id.
        :param vertex_type: the vertex-type.
        :return: the new L{Vertex}.
        """
        self.num_vertices += 1
        new_vertex = Vertex(vertex_id, vertex_type)
        self.vertice_list[vertex_id] = new_vertex
        return new_vertex

    def add_vertex(self, vertex):
        """
        adds an existing L{Vertex} to the graph.
        :param vertex: the L{Vertex} to be added.
        """
        self.num_vertices += 1
        self.vertice_list[vertex.id] = vertex

    def get_vertex(self, vertex_id):
        """
        finds a L{Vertex} with the given id in the graph.
        :param vertex_id: the L{Vertex} id to find.
        :return: the found L{Vertex}.
        """
        if vertex_id in self.vertice_list:
            return self.vertice_list[vertex_id]
        else:
            return None

    def __contains__(self, vertex_id):
        """
        checks if the L{Vertex} with the given id exists within the graph.
        :param vertex_id: the id to check.
        :return: true if found, false if not.
        """
        return vertex_id in self.vertice_list

    def add_edge(self, source_vertex, target_vertex, edge=Edge()):
        """
        adds an L{Edge} between to L{vertices<Vertex>}.
        if a L{Vertex} does not exist in the graph yet, it will be added.
        :param source_vertex: the first L{Vertex} to connect the L{Edge} to.
        :param target_vertex: the second v to connect the L{Edge} to.
        :param edge: the L{Edge}-object to add. None if just an abstract connection with no further information
        will be added.
        """
        if source_vertex not in self.vertice_list:
            self.add_vertex(source_vertex)
        if target_vertex not in self.vertice_list:
            self.add_vertex(target_vertex)
        self.vertice_list[source_vertex].addNeighbor(self.vertice_list[target_vertex], edge)

    def get_vertices(self):
        """
        get all L{vertices<Vertex>} of this graph.
        :return: list of L{vertices<Vertex>}.
        """
        return self.vertice_list.values()

    def __iter__(self):
        """
        iterator.
        :return: next element.
        """
        return iter(self.vertice_list.values())


class Vertex(object):
    """
    Implements a Vertex that can be added to a L{Graph}.
    """
    def __init__(self, vertex_id, vertex_type):
        """
        default constructor of a vertex.
        :param vertex_id: vertex id.
        :param vertex_type: vertex type.
        """
        self.id = vertex_id
        self.connected_to = {}
        self.type = vertex_type

    def add_neighbor(self, vertex, edge=Edge()):
        """
        adds an L{Edge} between this vertex and the vertex provided.
        :param vertex: the vertex to add a connection to.
        :param edge: the L{Edge} object. adds abstract L{Edge} if no edge provided.
        """

        self.connected_to[vertex] = edge

    def __str__(self):
        """
        to-string overload.
        :return: the string.
        """
        return str(self.id) + ' connected_to: ' + str([x.id for x in self.connected_to])

    def get_connections(self):
        """
        get all vertices connected to this vertex.
        :return: list of vertices.
        """
        return self.connected_to.keys()

    def get_id(self):
        """
        get the own vertex-id.
        :return: the vertex id.
        """
        return self.id

    def get_edge(self, vertex):
        """
        get an L{Edge} between this vertex and the vertex provided.
        :param vertex: the vertex the get the L{Edge} to.
        :return: the edge.
        """
        return self.connected_to[vertex]

    def get_type(self):
        """
        gets the type of this vertex.
        :return: type.
        """
        return self.type

    def set_type(self, vertex_type):
        """
        sets the type of this vertex.
        :param vertex_type: the type.
        """
        self.type = vertex_type


