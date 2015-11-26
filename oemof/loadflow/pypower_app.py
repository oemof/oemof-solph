# -*- coding: utf-8 -*-

"""
Example application that uses pypower for load flow simulation.
pypo stands for an abbreviation for pypower
Mainly developed by Christian Fleischer
"""
from network.entities import Bus
from network.entities.components import Transport
from numpy import array
from pypower.api import  runpf, printpf

# define a new bus class as child from Bus
class BusPypo(Bus):
    """
    some explanation on the class
    """

    def __init__(self, **kwargs):
        """
        here come information on the attributes and methods
        """
        super().__init__(**kwargs)
        # here you can add your own attribute which you need, like:#
        # Bus Data attributes
        self.bus_id = kwargs.get("bus_id", None)
        self.bus_type = kwargs.get("bus_type", None)
        self.PD = kwargs.get("PD", None)
        self.QD = kwargs.get("QD", None)
        self.GS = kwargs.get("GS", None)
        self.BS = kwargs.get("BS", None)
        self.bus_area = kwargs.get("bus_area", None)
        self.VM = kwargs.get("VM", None)
        self.VA = kwargs.get("VA", None)
        self.base_kv = kwargs.get("base_kv", None)
        self.zone = kwargs.get("zone", None)
        self.vmax = kwargs.get("vmax", None)
        self.vmin = kwargs.get("vmin", None)
        
        # Generator Data attributes
        #self.gen_bus = kwargs("gen_bus", None) #could possibly be replaced with bus_id
#        self.gen_bus = kwargs.get("gen_bus",None)
        self.PG = kwargs.get("PG", None)
        self.QG = kwargs.get("QG", None)
        self.qmax = kwargs.get("qmax", None)
        self.qmin = kwargs.get("qmin", None)
        self.VG = kwargs.get("VG", None)
        self.mbase = kwargs.get("mbase", None)
        self.gen_status = kwargs.get("gen_status", None)
        self.pmax = kwargs.get("pmax", None)
        self.pmin = kwargs.get("pmin", None)

    def __iter__(self):
        return iter(self.bus_id)
        
        
# define a new transport class for the grid
class CablePypo(Transport):
    """
    """

    def __init__(self, **kwargs):
        """
        here come information on the attributes and methods
        """
    
        super().__init__(**kwargs)
        # Branch Data attributes
        self.f_bus = kwargs.get('f_bus', None)
        self.t_bus = kwargs.get('t_bus', None)
        self.br_r = kwargs.get('br_r', None)
        self.br_x = kwargs.get('br_x', None)
        self.br_b = kwargs.get('br_b', None)
        self.rate_a = kwargs.get('rate_a', None)
        self.rate_b = kwargs.get('rate_b', None)
        self.rate_c = kwargs.get('rate_c', None)
        self.tap = kwargs.get('tap', None)
        self.shift = kwargs.get('shift', None)
        self.br_status = kwargs.get('br_status', None)

 
#  bus initialization
b_el1 = BusPypo(uid="b_el1", type="el", bus_id = 1, bus_type = 1, PD = 30, QD = 10, GS = 0, BS =0 , bus_area = 1, VM =1 , VA =0 , base_kv = 135, zone = 1, vmax = 1.05, vmin = 0.95 ) 
b_el2 = BusPypo(uid="b_el2", type="el", bus_id = 2, bus_type = 2, PD = 30, QD = 15, GS = 0, BS =0 , bus_area = 1, VM =1 , VA =0 , base_kv = 135, zone = 1, vmax =1.1 , vmin =0.95 ) 
b_el3 = BusPypo(uid="b_el3", type="el", bus_id = 3, bus_type = 3, PD = 0, QD = 0, GS = 0, BS = 0, bus_area = 1, VM = 1, VA = 0, base_kv = 135, zone = 1, vmax = 1.05, vmin = 0.95 ) 

busses = [b_el1, b_el2, b_el3]

# generator initialization
g_el1 = BusPypo(uid="generator1", bus_id = 2, PG =30, QG =0, qmax = 62.5, qmin = -15, VG = 1, mbase = 100, gen_status = 1, pmax = 60, pmin = 0 ) 
g_el2 = BusPypo(uid="generator2", bus_id = 3, PG = 0, QG =0, qmax = 0 , qmin = -15, VG = 1, mbase = 100, gen_status = 1, pmax = 0, pmin = 0 ) 

generators = [g_el1,g_el2]

# branch initialization
cable1 = CablePypo(uid="cable1", inputs=[b_el1], outputs=[b_el2], f_bus = 1, t_bus = 2, br_r = 0.02, br_x = 0.06, br_b = 0.03, rate_a = 130, rate_b = 130, rate_c = 130, tap = 0, shift = 0, br_status = 1)
cable2 = CablePypo(uid="cable2", inputs=[b_el2], outputs=[b_el3], f_bus = 1, t_bus = 3, br_r = 0.05, br_x = 0.19, br_b = 0.02, rate_a = 130, rate_b = 130, rate_c = 130, tap = 0, shift = 0, br_status = 1)
cable3 = CablePypo(uid="cable3", inputs=[b_el3], outputs=[b_el1], f_bus = 2, t_bus = 3, br_r = 0.06, br_x = 0.17, br_b = 0.02, rate_a = 65, rate_b = 65, rate_c = 65, tap = 0, shift = 0, br_status = 1)

branches = [cable1, cable2, cable3]
#make bus array 
my_bus_array = []
for bus in busses:
    my_bus_array.append([bus.bus_id, bus.bus_type, bus.PD, bus.QD, bus.GS, bus.BS, bus.bus_area, bus.VM, bus.VA, bus.base_kv, bus.zone, bus.vmax, bus.vmin])
#make generator array
my_gen_array = []
for gen in generators:
    my_gen_array.append([bus.bus_id, gen.PG, gen.QG, gen.qmax, gen.qmin, gen.VG, gen.mbase, gen.gen_status, gen.pmax, gen.pmin])
#make branch array
my_branch_array = []
for cables in branches:
    my_branch_array.append([cables.f_bus, cables.t_bus, cables.br_r, cables.br_x, cables.br_b, cables.rate_a, cables.rate_b, cables.rate_c, cables.tap, cables.shift, cables.br_status])

#print (my_branch_array)
#print (my_gen_array)
#print (my_bus_array)


#print (my_bus_array)
#create casefile     
def examplecase():
    """Power flow data for 3 bus, 2 generators.
   

    Based on data from ...
    """
    ppc = {"version": '1'}

    ##-----  Power Flow Data  -----##
    ## system MVA base
    ppc["baseMVA"] = 100.0  
    ppc["bus"] = array(my_bus_array)
    ppc ["gen"] = array(my_gen_array)  
    ppc["branch"] = array(my_branch_array)
    

    return ppc
    
ppc = examplecase()

results = runpf(ppc)
printpf(results)

# plot topology
#import networkx as nx
#g = nx.DiGraph()
#buses = [b_el1, b_el2, b_el3]
#components = [cable1, cable2, cable3]
#es = buses + components
#g.add_nodes_from(es)
#for e in es:
#    for e_in in e.inputs:
#        a, b = e_in, e
#        g.add_edge(a, b)
#graph_pos=nx.spectral_layout(g)
#nx.draw_networkx_nodes(g, graph_pos, buses, node_shape="o", node_color="r",
#                       node_size = 900)
#nx.draw_networkx_nodes(g, graph_pos, components, node_shape="s",
#                       node_color="b", node_size=300)
#nx.draw_networkx_edges(g, graph_pos)
#nx.draw_networkx_labels(g, graph_pos)

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
