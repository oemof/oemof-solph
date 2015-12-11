# -*- coding: utf-8 -*-

"""
Example application that uses pypower for load flow simulation.
pypo stands for an abbreviation for pypower
Mainly developed by Christian Fleischer and Clemens Wingenbach
"""
from oemof.core.network.entities.buses import BusPypo
from oemof.core.network.entities.components.transports import BranchPypo
from oemof.core.network.entities.components.sources import GenPypo
from oemof.core import energy_system as es

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
g_el1 = GenPypo(uid = "generator1", outputs = [b_el2], PG = 30, QG = 0, qmax = 62.5,
                qmin = -15, VG = 1, mbase = 100, gen_status = 1, pmax = 60,
                pmin = 0)
g_el2 = GenPypo(uid = "generator2", outputs = [b_el3], PG = 0, QG = 0, qmax = 0,
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

entities = busses + generators + branches

simulation = es.Simulation(method='pypower')
energysystem = es.EnergySystem(entities=entities, simulation=simulation)
energysystem.plot_as_graph(labels=True)
# if resultsfile already exists it will be appended
results = energysystem.simulate_loadflow(resultsfile="example_results.txt")
