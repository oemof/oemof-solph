# -*- coding: utf-8 -*-

"""
Application to use for grid course FL Dec 2015
"""
from oemof.core.network.entities.buses import BusPypo
from oemof.core.network.entities.components.transports import BranchPypo
from numpy import array
from pypower.api import runpf
import sqlalchemy
import pandas as pd

con = sqlalchemy.create_engine('postgresql://student:user123@localhost:5432/oemof')

sql = 'SELECT * FROM grids.opentgmod_bus_data WHERE base_kv = 380;'
bus_data =pd.read_sql_query(sql, con)

branch_data = pd.read_sql_table('opentgmod_branch_data', con, schema='grids')
branch_sub = [x&y for (x,y) in zip(list(branch_data.f_bus.isin(bus_data.bus_i)),
                                  list(branch_data.t_bus.isin(bus_data.bus_i)))]
branch_data = branch_data[branch_sub]

buses = {}
for index, row in bus_data.iterrows():
    buses[row['bus_i']] = BusPypo(uid= row['bus_i'])

branches = []
for index, row in branch_data.iterrows():
    branches.append(BranchPypo(uid= row['gid'],
                               inputs = [buses[row['f_bus']]],
                               outputs = [buses[row['t_bus']]]))

##bus initialization
#b_el1 = BusPypo(uid = "b_el1", type = "el", bus_id = 1, bus_type = 1, PD = 30,
#                QD = 10, GS = 0, BS =0 , bus_area = 1, VM =1 , VA = 0,
#                base_kv = 135, zone = 1, vmax = 1.05, vmin = 0.95)
#b_el2 = BusPypo(uid = "b_el2", type = "el", bus_id = 2, bus_type = 2, PD = 30,
#                QD = 15, GS = 0, BS =0 , bus_area = 1, VM =1 , VA = 0,
#                base_kv = 135, zone = 1, vmax =1.10, vmin = 0.95)
#b_el3 = BusPypo(uid = "b_el3", type = "el", bus_id = 3, bus_type = 3, PD = 0,
#                QD = 0, GS = 0, BS = 0, bus_area = 1, VM = 1, VA =  0,
#                base_kv = 135, zone = 1, vmax = 1.05, vmin = 0.95)
##bus list
#busses = [b_el1, b_el2, b_el3]
#
##generator and generators initialization
#g_el1 = BusPypo(uid = "generator1", bus_id = 2, PG = 30, QG = 0, qmax = 62.5,
#                qmin = -15, VG = 1, mbase = 100, gen_status = 1, pmax = 60,
#                pmin = 0)
#g_el2 = BusPypo(uid = "generator2", bus_id = 3, PG = 0, QG = 0, qmax = 0,
#                qmin = -15, VG = 1, mbase = 100, gen_status = 1, pmax = 0,
#                pmin = 0)
##generator list
#generators = [g_el1,g_el2]
#
##branch and branches initialization
#branch1 = BranchPypo(uid = "cable1", inputs = [b_el1], outputs = [b_el2],
#                     f_bus = 1, t_bus = 2, br_r = 0.02, br_x = 0.06,
#                     br_b = 0.03, rate_a = 130, rate_b = 130, rate_c = 130,
#                     tap = 0, shift = 0, br_status = 1)
#branch2 = BranchPypo(uid = "cable2", inputs = [b_el1], outputs = [b_el3],
#                     f_bus = 1, t_bus = 3, br_r = 0.05, br_x = 0.19,
#                     br_b = 0.02, rate_a = 130, rate_b = 130, rate_c = 130,
#                     tap = 0, shift = 0, br_status = 1)
#branch3 = BranchPypo(uid = "cable3", inputs = [b_el2], outputs = [b_el3],
#                     f_bus = 2, t_bus = 3, br_r = 0.06, br_x = 0.17,
#                     br_b = 0.02, rate_a = 65, rate_b = 65, rate_c = 65,
#                     tap = 0, shift = 0, br_status = 1)
##branch list
#branches = [branch1, branch2, branch3]
#
##make bus array from busses list
#my_bus_array = []
#for bus in busses:
#    my_bus_array.append([bus.bus_id, bus.bus_type, bus.PD, bus.QD, bus.GS,
#                         bus.BS, bus.bus_area, bus.VM, bus.VA, bus.base_kv,
#                         bus.zone, bus.vmax, bus.vmin])
##make generator array from generators list
#my_gen_array = []
#for gen in generators:
#    my_gen_array.append([bus.bus_id, gen.PG, gen.QG, gen.qmax, gen.qmin,
#                         gen.VG, gen.mbase, gen.gen_status, gen.pmax,
#                         gen.pmin])
##make branch array from branches list
#my_branch_array = []
#for branch in branches:
#    my_branch_array.append([branch.f_bus, branch.t_bus, branch.br_r,
#                            branch.br_x, branch.br_b, branch.rate_a,
#                            branch.rate_b, branch.rate_c, branch.tap,
#                            branch.shift, branch.br_status])
#
##create casefile
#def examplecase():
#    """create pypower case file "ppc". The examplecase contains 3 buses,
#    3 branches and 2 generators.
#
#    Minimum required information for ppc case file:
#    "version" -- defines version of ppc file, version 1 and version 2 available
#    "baseMVA" -- the power base value of the power system in MVA
#    "bus" -- arrays busses input data
#    "gen" -- arrays with generators input data
#    "branch" -- arrays with branches input data
#    """
#    ppc = {"version": '1'}
#
#    ##-----  Power Flow Data  -----##
#    ## system MVA base
#    ppc["baseMVA"] = 100.0
#    ppc["bus"] = array(my_bus_array)
#    ppc ["gen"] = array(my_gen_array)
#    ppc["branch"] = array(my_branch_array)
#
#    return ppc
#
##initialtes example case as ppc
#ppc = examplecase()
##prints out results of power flow optimization
#results = runpf(ppc)
#
#plot topology
import networkx as nx
g = nx.DiGraph()
buses = list(buses.values())
components = branches
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
