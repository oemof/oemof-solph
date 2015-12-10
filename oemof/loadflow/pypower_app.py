# -*- coding: utf-8 -*-

"""
Application to use for grid course FL Dec 2015
"""
from oemof.core.network.entities.buses import BusPypo
from oemof.core.network.entities.components.transports import BranchPypo
from oemof.core.network.entities.components.sources import GenPypo
from oemof.core import energy_system as es
import sqlalchemy
import pandas as pd


con = sqlalchemy.create_engine('postgresql://student:user123@localhost:5432/oemof')

sql = '''SELECT gid,
         bus_i,
         bus_type,
         pd ,
         qd ,
         bus_area,
         vm ,
         va ,
         base_kv ,
         zone,
         ST_X(geom) AS lat,
         ST_Y(geom) AS lon
         FROM grids.opentgmod_bus_data
         WHERE base_kv = 380;'''
bus_data = pd.read_sql_query(sql, con)

sql = '''SELECT gid,
         f_bus,
         t_bus,
         br_r,
         br_x,
         br_b,
         rate_a,
         tap,
         shift,
         br_status,
         link_type,
         ST_X(ST_PointOnSurface(geom)) AS lat,
         ST_Y(ST_PointOnSurface(geom)) AS lon
         FROM grids.opentgmod_branch_data;'''
branch_data = pd.read_sql_query(sql, con)


branch_sub = [x&y for (x,y) in zip(list(branch_data.f_bus.isin(bus_data.bus_i)),
                                  list(branch_data.t_bus.isin(bus_data.bus_i)))]
branch_data = branch_data[branch_sub]

buses = {}
positions = {}

for index, row in bus_data.iterrows():
    bus_temp = BusPypo(uid=row['bus_i'], type="el",
                       bus_id=int(row['bus_i']), bus_type=int(row["bus_type"]),
                       PD = int(row["pd"]), QD = int(row["qd"]),
                       GS = 0, BS =0 , bus_area = 1, VM =1 , VA = 0,
                       base_kv = 380, zone = 1, vmax = 1.05, vmin = 0.95)
    buses[bus_temp.uid] = bus_temp
    positions[bus_temp] = [row['lat'], row['lon']]

branches = {}
for index, row in branch_data.iterrows():
    branch_temp = BranchPypo(uid=row['gid'],
                             inputs=[buses[row['f_bus']]],
                             outputs=[buses[row['t_bus']]],
                             f_bus=buses[row['f_bus']].bus_id,
                             t_bus=buses[row['t_bus']].bus_id,
                             br_r = 0.02, br_x = 0.06,
                             br_b = 0.03, rate_a = 130, rate_b = 130, rate_c = 130,
                             tap = 0, shift = 0, br_status = 1)
    branches[branch_temp.uid] = branch_temp
    positions[branch_temp] = [row['lat'], row['lon']]

def create_dummy_gen(bus):
    dummy_gen = GenPypo(uid = "generator1", outputs = [bus],
                        PG = 30, QG = 0, qmax = 62.5,
                        qmin = -15, VG = 1, mbase = 100, gen_status = 1, pmax = 60,
                        pmin = 0)
    return dummy_gen

generators = []
for bus in list(buses.values()):
    gen_temp = create_dummy_gen(bus)
    generators.append(gen_temp)
    positions[gen_temp] = positions[bus]

entities = list(buses.values())+list(branches.values()) + generators

simulation = es.Simulation(method='pypower')
energysystem = es.EnergySystem(entities=entities, simulation=simulation)
energysystem.plot_as_graph(labels=False, positions=positions)
results = energysystem.simulate_loadflow()

