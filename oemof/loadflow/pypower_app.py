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

#For conventional nearest neoghbour:
#  SELECT g1.gid As gref_gid,
# g1.bus_i As gref_description,
# g2.pp_nr As gnn_gid,
# g2.bnetza_nr As gnn_description,
# ST_Distance_Sphere(g1.geom,ST_SetSRID(g2.geom, 4326))/1000 AS distance_in_km
#FROM grids.opentgmod_bus_data As g1,
# (SELECT * FROM grids.register_conventional_power_plants) As g2
#WHERE g1.gid = 100 and g1.gid <> g2.pp_nr
#ORDER BY ST_Distance_Sphere(g1.geom,ST_SetSRID(g2.geom, 4326))
#LIMIT 10;

#For renewable nearest neoghbour:
#SELECT g1.gid As gref_gid,
# g1.bus_i As gref_description,
# g2.gid As gnn_gid,
# g2.power_plant_id As gnn_description,
# ST_Distance_Sphere(g1.geom,ST_SetSRID(g2.geom, 4326))/1000 AS distance_in_km
#FROM grids.opentgmod_bus_data As g1,
# (SELECT * FROM grids.register_renewable_power_plants) As g2
#WHERE g1.gid = 100 and g1.gid <> g2.gid
#ORDER BY ST_Distance_Sphere(g1.geom, g2.geom)
#LIMIT 10;

# get bus and branch data from database
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

# choose only branches for existing buses
branch_sub = [x&y for (x,y) in zip(list(branch_data.f_bus.isin(bus_data.bus_i)),
                                  list(branch_data.t_bus.isin(bus_data.bus_i)))]
branch_data = branch_data[branch_sub]

# initailize positions for plotting
positions = {}

# intitialize buses
buses = {}

# choose ref buses, the rest will be initialized as PQ-bus
ref_buses = ["8205", "3227", "4075", "1978", "3285", "7766", "7847", "7879"]
for index, row in bus_data.iterrows():
    bus_type=1
    if row['bus_i'] in ref_buses:
        bus_type = 3
    bus_temp = BusPypo(uid=row['bus_i'], type="el",
                       bus_id=int(row['bus_i']),
                       bus_type=bus_type,
                       PD = 200, QD = 0,
                       GS = 0, BS =0 , bus_area = 1, VM =1 , VA = 0,
                       base_kv = 380, zone = 1, vmax = 1.1, vmin = 0.9)
    buses[bus_temp.uid] = bus_temp
    positions[bus_temp] = [row['lat'], row['lon']]

# intitialize branches
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

# function to initialize dummy generators
def create_dummy_gen(bus):
    dummy_gen = GenPypo(uid = "generator1", outputs = [bus],
                        PG = 200, QG = 0, qmax = 200,
                        qmin = -200, VG = 1, mbase = 100, gen_status = 1,
                        pmax = 200, pmin = 0)
    return dummy_gen

# intitialize generators
generators = []
for bus in list(buses.values()):
    gen_temp = create_dummy_gen(bus)
    generators.append(gen_temp)
    positions[gen_temp] = positions[bus]

# make entity list
entities = list(buses.values())+list(branches.values()) + generators

# choose simulation parameter
simulation = es.Simulation(method='pypower')
energysystem = es.EnergySystem(entities=entities, simulation=simulation)

# plot entities as graph
energysystem.plot_as_graph(labels=False, positions=positions)

# simulate loadflow
# if resultsfile already exists an error will be raised
results = energysystem.simulate_loadflow(max_iterations=20,
                                         resultsfile="app_results.txt")
