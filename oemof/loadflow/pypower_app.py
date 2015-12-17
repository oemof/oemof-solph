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
import pg8000

# TODO: con = sqlalchemy.create_engine('postgresql+pg8000://postgres:user123@localhost:5432/oemof')
con = sqlalchemy.create_engine('postgresql+pg8000://'+
                               'student:user123@localhost:5432/oemof')

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
         ST_X(geom) AS lon,
         ST_Y(geom) AS lat
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
         ST_X(ST_PointOnSurface(geom)) AS lon,
         ST_Y(ST_PointOnSurface(geom)) AS lat
         FROM grids.opentgmod_branch_data;'''
branch_data = pd.read_sql_query(sql, con)

#For conventional nearest neighbour:
sql = """SELECT
         DISTINCT ON (pp.pp_nr) pp.pp_nr AS pp_nr,
         bus.bus_i AS bus_id,
         ST_Distance_Sphere(pp.geom, bus.geom)/1000 AS dist_in_km,
         pp.pinst AS pinst,
         ST_X(pp.geom) AS lon,
         ST_Y(pp.geom) AS lat
         FROM
         grids.opentgmod_bus_data AS bus,
         grids.register_conventional_power_plants AS pp
         WHERE bus.base_kv = 380 AND pinst IS NOT NULL
         ORDER BY  pp_nr, dist_in_km;"""
gen_data = pd.read_sql_query(sql, con)

# for population data:
sql = """SELECT
         b.bus_i AS bus_id,
         c.population AS population
         FROM
         grids.geo_district a,
         grids.opentgmod_bus_data b,
         grids.district_population c
         WHERE
         cntr_id ='DE'
         AND
         ST_Intersects(b.geom,a.geom)
         AND
         a.region_key = c.region_key
         AND b.base_kv = 380
         Order by bus_id;"""
pop_data = pd.read_sql_query(sql, con)

# choose only branches for existing buses
branch_sub = [x & y for (x, y) in
              zip(list(branch_data.f_bus.isin(bus_data.bus_i)),
                  list(branch_data.t_bus.isin(bus_data.bus_i)))]
branch_data = branch_data[branch_sub]

# get population per bus for demand
populations = {}
total_population = pop_data.sum().population
for index, row in pop_data.iterrows():
    populations[row['bus_id']] = row['population']

# Choose total deman in MWh/h
demand = 183e3

# initailize positions for plotting
positions = {}

# intitialize buses
buses = {}

# choose ref buses, the rest will be initialized as PQ-bus
ref_buses = ["8205", "3227", "4075", "1978", "3285", "7766", "7847", "7879"]
for index, row in bus_data.iterrows():
    bus_id = row['bus_i']
    bus_pd = 0
    if bus_id in populations.keys():
        bus_pd = demand * populations[bus_id] / total_population
    bus_type = 1
    if bus_id in ref_buses:
        bus_type = 3
    bus_temp = BusPypo(uid=bus_id, type="el",
                       bus_id=int(bus_id),
                       bus_type=bus_type,
                       PD=bus_pd, QD=0,
                       GS = 0, BS =0 , bus_area = 1, VM =1 , VA = 0,
                       base_kv = 380, zone = 1, vmax = 1.1, vmin = 0.9)
    buses[bus_temp.uid] = bus_temp
    positions[bus_temp] = [row['lon'], row['lat']]

# intitialize branches
branches = {}
for index, row in branch_data.iterrows():
    branch_rate = row["rate_a"]
    branch_temp = BranchPypo(uid=row['gid'],
                             inputs=[buses[row['f_bus']]],
                             outputs=[buses[row['t_bus']]],
                             f_bus=buses[row['f_bus']].bus_id,
                             t_bus=buses[row['t_bus']].bus_id,
                             br_r = row["br_r"], br_x = row['br_x'],
                             br_b = row['br_b'],
                             rate_a = branch_rate,
                             rate_b = branch_rate,
                             rate_c = branch_rate,
                             tap = 0, shift = 0, br_status = 1)
    branches[branch_temp.uid] = branch_temp
    positions[branch_temp] = [row['lon'], row['lat']]

# intitialize generators
generators = {}
buses_with_generators = []
for index, row in gen_data.iterrows():
    gen_temp = GenPypo(uid = row["pp_nr"], outputs = [buses[row["bus_id"]]],
                        PG = 0.8*int(row["pinst"]),
                        QG = 0, qmax = row["pinst"],
                        qmin = -row["pinst"],
                        VG = 1, mbase = 100, gen_status = 1,
                        pmax = row["pinst"], pmin = 0)
    generators[gen_temp.uid] = gen_temp
    positions[gen_temp] = [row['lon'], row['lat']]
    buses_with_generators.append(row["bus_id"])

for bus in list(buses.values()):
    if bus.uid not in buses_with_generators:
        power_temp = bus.PD
        gen_temp = GenPypo(uid = bus.uid, outputs = [bus],
                        PG = power_temp,
                        QG = 0, qmax = power_temp,
                        qmin = -power_temp,
                        VG = 1, mbase = 100, gen_status = 1,
                        pmax = power_temp, pmin = 0)
        generators[gen_temp.uid] = gen_temp
        positions[gen_temp] = positions[bus]



# make entity list
entities = list(buses.values())+list(branches.values()) + list(generators.values())

# choose simulation parameter
simulation = es.Simulation(method='pypower')
energysystem = es.EnergySystem(entities=entities, simulation=simulation)

# plot entities as graph
g = energysystem.plot_as_graph(labels=False, positions=positions)

# simulate loadflow
# if resultsfile already exists an error will be raised
# it will be overwritten if the argument overwrite is True
# without the resultsfile argument the output will be in the console
results = energysystem.simulate_loadflow(max_iterations=20,
                                         resultsfile="app_results.txt",
                                         overwrite=True)
