# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 15:26:53 2015

@author: caro
"""

import logging
#logging.getLogger().setLevel(logging.DEBUG)
#logging.getLogger().setLevel(logging.INFO)
logging.getLogger().setLevel(logging.WARNING)
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.geometry import Point
from oemof_base.oemof.tools import db
# from oemof_base.oemof.core import energy_regions
from oemof_base.oemof.core import energy_buildings as eb
from oemof.core.network.entities import Bus
from oemof.core.network.entities.components import sinks as sink
from oemof.tools import helpers

conn = db.connection()
year = 2013

geo = Polygon([(12.2, 52.2), (12.2, 51.6),
                     (13.2, 51.6), (13.2, 52.2)])

geo2 = Point(12.2, 52.2).buffer(1.0)



#reg = energy_regions.region(year, geo)
#reg.fetch_demand_series(conn)

#path = '/home/caro/rlihome/Git/oemof/src/'
#filename = 'example_data_entsoe.csv'

#profile_entsoe = pd.read_csv(path + "example_data_entsoe.csv", sep=",")
#year = 2010 # years from 2006 to 2011 do exist in the example data
# (and only for Germany), more countries are in old oemof's database
#
#reg3 = energy_regions.region(year, geo2)
#reg3.set_connection(conn)
#reg3.fetch_demand_series(method='scale_profile_csv',
#                         path='/home/caro/rlihome/Git/oemof/src/',
#                         filename='example_data_entsoe.csv',
#                         ann_el_demand=3000)

#reg4 = energy_regions.region(year, geo2)
#reg4.set_connection(conn)
#reg4.fetch_demand_series(method='scale_profile_db',
#                         conn=conn)
#

'''
annual electrical demand per household member for one-, two-, three- and
four-person household in kWh per year. source: BDEW2010
'''

# TODO: folgende beiden dictionaries funktionieren derzeit nur entweder oder,
# also entweder demand für alle 3 Sektoren vorgeben oder berechnen
# lassen, aber ist vielleicht auch sinnvoll so, oder?

ann_el_demand_per_sector = [
    {'ann_el_demand': None,
     'selp_type': 'h0'},
    {'ann_el_demand': None,
     'selp_type': 'g0'},
    {'ann_el_demand': None,
     'selp_type': 'i0'}]

#ann_el_demand_per_sector = [
#    {'ann_el_demand': 3000,
#     'selp_type': 'h0'},
#    {'ann_el_demand': 3000,
#     'selp_type': 'g0'},
#    {'ann_el_demand': 3000,
#     'selp_type': 'i0'}]


# Necessary data to calculate the ann_el_demand_per_sector if None

# Household sector data (h)
population = 40000

ann_el_demand_per_person = [
    {'ann_el_demand': 2050,
     'household_type': 'one'},
    {'ann_el_demand': 1720,
     'household_type': 'two'},
    {'ann_el_demand': 1350,
     'household_type': 'three'},
    {'ann_el_demand': 1235,
     'household_type': 'four'}]

household_structure = [
    {'household_members': 10000,
     'household_type': 'one'},
    {'household_members': 10000,
     'household_type': 'two'},
    {'household_members': 10000,
     'household_type': 'three'},
    {'household_members': 10000,
     'household_type': 'four'}]

household_members_all = 40000
# TODO: wäre cool, wenn diese Summe automatisch
# gebildet wird aus allen household_members in household_structure


# Service sector data (g)
comm_ann_el_demand_state = 500000
comm_number_of_employees_state = 80000
comm_number_of_employees_region = 10000


# Industry sector data (i)
# The industry sector corrsponds to sector C ("Verarbeitendes Gewerbe") with
# wz ("Wirtschaftszweig") = 1

ind_statistics_state = [
    {'ann_el_demand': 200000,
     'number_employees': 551280,
     'wz': 11},
    {'ann_el_demand': 300000,
     'number_employees': 949468,
     'wz': 12},
    {'ann_el_demand': 400000,
     'number_employees': 837733,
     'wz': 13},
    {'ann_el_demand': 500000,
     'number_employees': 1755617,
     'wz': 14}]

ind_number_of_employees_region = [
    {'wz_11': 22709},
    {'wz_12': 15856},
    {'wz_13': 18554},
    {'wz_14': 20976}]


bel = Bus(uid="bel",
          type="el",
          excess=True)

data = pd.read_csv("storage_optimization/storage_invest.csv", sep=",")
demand = sink.Simple(uid="demand", inputs=[bel])
helpers.call_demandlib(demand,
                       method='calculate_profile',
                       year=2010,
                       ann_el_demand_per_sector=ann_el_demand_per_sector)

# reg5 = energy_regions.region(year, geo2)
# reg5.set_connection(conn)
# reg5.fetch_demand_series(method='calculate_profile',
#                         conn=conn,
#                         ann_el_demand_per_sector=ann_el_demand_per_sector)

# reg6 = energy_regions.region(year, geo2)
# reg6.set_connection(conn)
# reg6.fetch_demand_series(method='calculate_profile',
#                         conn=conn,
#                         population=population,
#                         ann_el_demand_per_sector=ann_el_demand_per_sector,
#                         ann_el_demand_per_person=ann_el_demand_per_person,
#                         household_structure=household_structure,
#                         household_members_all=household_members_all,
#                         comm_ann_el_demand_state=comm_ann_el_demand_state,
#                         comm_number_of_employees_state=
#                         comm_number_of_employees_state,
#                         comm_number_of_employees_region=
#                         comm_number_of_employees_region)

#reg7 = energy_regions.region(year, geo2)
#reg7.set_connection(conn)
#reg7.fetch_demand_series(method='calculate_profile',
#                         conn=conn,
#                         ann_el_demand_per_sector=ann_el_demand_per_sector)

#                         comm_number_of_employees=20000,
#                         ind_number_of_employees=30000)


#print(reg5.demand.elec_demand)
#reg5.demand.elec_demand.plot()
#plt.show()

#reg2.fetch_demand_series(conn,
#            ann_el_demand=define_elec_buildings[0]['annual_elec_demand'],
#            selp_type=define_elec_buildings[0]['selp_type'],
#            profile=profile_entsoe,
#            year=year)


#print(reg.demand)

print('ok')







#time_df = region.create_basic_dataframe()
#
##    time_df = pd.DataFrame(
##            index=pd.date_range(pd.datetime(year, 1, 1, 0), periods=hoy,
##                                freq='H', tz=tz),
##            columns=['weekday', 'hour', 'date'])
#
#bdew = bdew_elec_slp(conn, time_df)
#print(bdew.slp_frame)
