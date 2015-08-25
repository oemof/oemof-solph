# -*- coding: utf-8 -*-

"""
Example application that uses pypower for load flow simulation.
pypo stands for an abbreviation for pypower
Mainly developed by Christian Fleischer
"""
from network.entities import Bus
from network.entities.components import Transport

# define a new bus class as child from Bus
class BusPypo(Bus):
    """
    some explanation on the class
    """

    def __init__(self, **kwargs):
        """
        here come information on the attributes and methods, e.g.:
        :param voltage_level: voltage level of the bus
        """
        super().__init__(**kwargs)
        # here you can add your own attribute which you need, like:
        self.voltage_level = kwargs.get("voltage_level", None)


# define a new transport class for the grid
class CablePypo(Transport):
    """
    """

    def __init__(self, **kwargs):
        """
        :param maximal_current: maximal (thermal) current of the cable
        """
        super().__init__(**kwargs)
        self.maximal_current = kwargs.get('maximal_current', None)


# electricity bus initialization
b_el1 = BusPypo(uid="b_el1", type="el", voltage_level=220000)
b_el2 = Bus(uid="b_el2", type="el", voltage_level=220000)
b_el3 = Bus(uid="b_el3", type="el", voltage_level=220000)

# transport initialization
cable1 = CablePypo(uid="cable1", inputs=[b_el1], outputs=[b_el2],
                   maimal_current=1000)
cable2 = CablePypo(uid="cable2", inputs=[b_el2], outputs=[b_el3],
                   maimal_current=1000)
cable3 = CablePypo(uid="cable3", inputs=[b_el3], outputs=[b_el1],
                   maimal_current=1000)

# plot topology
import networkx as nx
g = nx.DiGraph()
buses = [b_el1, b_el2, b_el3]
components = [cable1, cable2, cable3]
es = buses + components
g.add_nodes_from(es)
for e in es:
    for e_in in e.inputs:
        a, b = e_in, e
        g.add_edge(a, b)
graph_pos=nx.spectral_layout(g)
nx.draw_networkx_nodes(g, graph_pos, buses, node_shape="o", node_color="r",
                       node_size = 900)
nx.draw_networkx_nodes(g, graph_pos, components, node_shape="s",
                       node_color="b", node_size=300)
nx.draw_networkx_edges(g, graph_pos)
nx.draw_networkx_labels(g, graph_pos)
