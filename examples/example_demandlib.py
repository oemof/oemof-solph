# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 15:26:53 2015

@author: caro
"""

import logging
# logging.getLogger().setLevel(logging.DEBUG)
# logging.getLogger().setLevel(logging.INFO)
logging.getLogger().setLevel(logging.WARNING)

from oemof.core.network.entities import Bus
from oemof.core.network.entities.components import sinks as sink
from oemof.tools import helpers

year = 2013

###########################################################################
# Parameters to calculate the profile
###########################################################################

# TODO:
# Both following parameter dictionaries work either or. You can know the
# annual electric demand or let it calculate for every of the three sectors
# each

ann_el_demand_per_sector = [
    {'ann_el_demand': 3000,
     'selp_type': 'h0'},
    {'ann_el_demand': 3000,
     'selp_type': 'g0'},
    {'ann_el_demand': 3000,
     'selp_type': 'i0'}]

ann_el_demand_per_sector_2 = [
    {'ann_el_demand': None,
     'selp_type': 'h0'},
    {'ann_el_demand': None,
     'selp_type': 'g0'},
    {'ann_el_demand': None,
     'selp_type': 'i0'}]

# Necessary data if annual electric demand for every sector needs to be
# calculated (ann_el_demand_per_sector is None)

# Household sector data (h)
# annual electrical demand per household member for one-, two-, three- and
# four-person household in kWh per year. source: BDEW2010

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
# TODO:
# would be cool to let this sum up automatically from all
#  household_members in household_structure


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

# ############################################################################
# Create demand object and relevant bus
# ############################################################################

# Example 1: Calculate profile with annual electric demand per sector is known

bel = Bus(uid="bel",
          type="el",
          excess=True)

demand = sink.Simple(uid="demand", inputs=[bel])
helpers.call_demandlib(demand,
                       method='calculate_profile',
                       year=2010,
                       ann_el_demand_per_sector=ann_el_demand_per_sector)

# Example 2: Calculate profile with unknown annual electric demand per sector

demand_2 = sink.Simple(uid="demand_2", inputs=[bel])
helpers.call_demandlib(
    demand_2,
    method='calculate_profile',
    year=2010,
    ann_el_demand_per_sector=ann_el_demand_per_sector_2,
    ann_el_demand_per_person=ann_el_demand_per_person,
    household_structure=household_structure,
    household_members_all=household_members_all,
    population=population,
    comm_ann_el_demand_state=comm_ann_el_demand_state,
    comm_number_of_employees_state=comm_number_of_employees_state,
    comm_number_of_employees_region=comm_number_of_employees_region)

print(demand.val)
print(demand_2.val)
