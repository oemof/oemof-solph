# -*- coding: utf-8 -*-

"""
Example application that uses pypower for load flow simulation.
pypo stands for an abbreviation for pypower
Mainly developed by Christian Fleischer
"""
from oemof.core.network.entities import Bus
from oemof.core.network.entities.components import Transport
from numpy import array
from pypower.api import runpf


class BusPypo(Bus):
    """ Create new pypower Bus class as child from oemof Bus used to define 
    busses and generators data
    """

    def __init__(self, **kwargs):
        """Assigned minimal required pypower input parameters of the bus and 
        generator as arguments 
        
        Keyword description of bus arguments:
        bus_id -- the bus number (also used as GEN_BUS parameter for generator)
        bus_type -- the bus type (1 = PQ, 2 = PV, 3 = ref, 4 = Isolated)
        PD -- the real power demand in MW
        QD -- the reactive power demand in MVAr
        GS -- the shunt conductance (demanded at V = 1.0 p.u.) in MW
        BS -- the shunt susceptance (injected at V = 1.0 p.u.) in MVAr
        bus_area -- area number (positive integer)
        VM -- the voltage magnitude in p.u.
        VA -- the voltage angle in degrees
        base_kv -- the base voltage in kV
        zone -- loss zone (positive integer)
        vmax -- the maximum allowed voltage magnitude in p.u.
        vmin -- the minimum allowed voltage magnitude in p.u.        
        
        Keyword generator arguments:
        PG --  the real power output in MW
        QG --  the reactive power output in MVAr
        qmax -- the maximum reactive power output in MVAr
        qmin -- the minimum reactive power output in MVAr
        VG -- the voltage magitude setpoint in p.u.
        mbase -- the total MVA base of the maschine, defaults to base MVA
        gen_status -- machine status,
                        > 0 = machine in-service
                        ≤ 0 = machine out-of-service
        pmax -- the maximum real power output in MW
        pmin -- the minimum real power output in MW
        """
        
        super().__init__(**kwargs)
        # Bus Data parameters
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
        
        # Generator Data parameters
#       gen_bus -- bus_id used instead (bus_id already created)
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
        
        
class BranchPypo(Transport):
    """Create new pypower Branch class as child from oemof Transport class 
    used to define branch data
    """

    def __init__(self, **kwargs):
        """Assigned minimal required pypower input parameters of the branch 
        arguments 
        
        Keyword description of branch arguments:
        f_bus -- "from" bus number
        t_bus -- "to" bus number
        br_r -- the line resistance in p.u. 
        br_x -- the line reactance in p.u.
        br_b -- the line charging susceptance in p.u.
        rate_a -- the line long term MVA  rating in MVA
        rate_b -- the line short term MVA rating in MVA
        rate_c -- the line emergency MVA rating on MVA
        tap -- the transformer tap ratio
        shift -- the transformer phase shift
        br_status -- branch status, 1= in service, 0 = out of service
        """
        super().__init__(**kwargs)
        # Branch Data Data parameters
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

 
#bus initialization
b_el1 = BusPypo(uid = "b_el1", type = "el", bus_id = 1, bus_type = 1, PD = 30,
                QD = 10, GS = 0, BS =0 , bus_area = 1, VM =1 , VA = 0,
                base_kv = 135, zone = 1, vmax = 1.05, vmin = 0.95)
b_el2 = BusPypo(uid = "b_el2", type = "el", bus_id = 2, bus_type = 2, PD = 30,
                QD = 15, GS = 0, BS =0 , bus_area = 1, VM =1 , VA = 0,
                base_kv = 135, zone = 1, vmax =1.10, vmin = 0.95)
b_el3 = BusPypo(uid = "b_el3", type = "el", bus_id = 3, bus_type = 3, PD = 0,
                QD = 0, GS = 0, BS = 0, bus_area = 1, VM = 1, VA =  0,
                base_kv = 135, zone = 1, vmax = 1.05, vmin = 0.95)
#bus list
busses = [b_el1, b_el2, b_el3]

#generator and generators initialization
g_el1 = BusPypo(uid = "generator1", bus_id = 2, PG = 30, QG = 0, qmax = 62.5,
                qmin = -15, VG = 1, mbase = 100, gen_status = 1, pmax = 60,
                pmin = 0)
g_el2 = BusPypo(uid = "generator2", bus_id = 3, PG = 0, QG = 0, qmax = 0,
                qmin = -15, VG = 1, mbase = 100, gen_status = 1, pmax = 0,
                pmin = 0)
#generator list                
generators = [g_el1,g_el2]

#branch and branches initialization
branch1 = BranchPypo(uid = "cable1", inputs = [b_el1], outputs = [b_el2],
                     f_bus = 1, t_bus = 2, br_r = 0.02, br_x = 0.06,
                     br_b = 0.03, rate_a = 130, rate_b = 130, rate_c = 130,
                     tap = 0, shift = 0, br_status = 1)
branch2 = BranchPypo(uid = "cable2", inputs = [b_el1], outputs = [b_el3],
                     f_bus = 1, t_bus = 3, br_r = 0.05, br_x = 0.19,
                     br_b = 0.02, rate_a = 130, rate_b = 130, rate_c = 130,
                     tap = 0, shift = 0, br_status = 1)
branch3 = BranchPypo(uid = "cable3", inputs = [b_el2], outputs = [b_el3],
                     f_bus = 2, t_bus = 3, br_r = 0.06, br_x = 0.17,
                     br_b = 0.02, rate_a = 65, rate_b = 65, rate_c = 65,
                     tap = 0, shift = 0, br_status = 1)
#branch list
branches = [branch1, branch2, branch3]

#make bus array from busses list
my_bus_array = []
for bus in busses:
    my_bus_array.append([bus.bus_id, bus.bus_type, bus.PD, bus.QD, bus.GS,
                         bus.BS, bus.bus_area, bus.VM, bus.VA, bus.base_kv,
                         bus.zone, bus.vmax, bus.vmin])
#make generator array from generators list
my_gen_array = []
for gen in generators:
    my_gen_array.append([bus.bus_id, gen.PG, gen.QG, gen.qmax, gen.qmin,
                         gen.VG, gen.mbase, gen.gen_status, gen.pmax,
                         gen.pmin])
#make branch array from branches list
my_branch_array = []
for branch in branches:
    my_branch_array.append([branch.f_bus, branch.t_bus, branch.br_r,
                            branch.br_x, branch.br_b, branch.rate_a,
                            branch.rate_b, branch.rate_c, branch.tap,
                            branch.shift, branch.br_status])

#create casefile
def examplecase():
    """create pypower case file "ppc". The examplecase contains 3 buses,
    3 branches and 2 generators.
    
    Minimum required information for ppc case file:
    "version" -- defines version of ppc file, version 1 and version 2 available
    "baseMVA" -- the power base value of the power system in MVA
    "bus" -- arrays busses input data
    "gen" -- arrays with generators input data
    "branch" -- arrays with branches input data
    """
    ppc = {"version": '1'}

    ##-----  Power Flow Data  -----##
    ## system MVA base
    ppc["baseMVA"] = 100.0
    ppc["bus"] = array(my_bus_array)
    ppc ["gen"] = array(my_gen_array)
    ppc["branch"] = array(my_branch_array)

    return ppc

#initialtes example case as ppc
ppc = examplecase()
#prints out results of power flow optimization
results = runpf(ppc)

#plot topology
import networkx as nx
g = nx.DiGraph()
buses = [b_el1, b_el2, b_el3]
components = [branch1, branch2, branch3]
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
