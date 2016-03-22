#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
# logging.getLogger().setLevel(logging.DEBUG)
# logging.getLogger().setLevel(logging.INFO)
logging.getLogger().setLevel(logging.WARNING)

from oemof.core.network.entities import Bus
from oemof.core.network.entities.components import sinks as sink
from oemof.demandlib import demand as dm

year = 2013

###########################################################################
# Parameters to calculate the profile
###########################################################################

# TODO:
# Both following parameter dictionaries work either or. You can know the
# annual electric demand or let it calculate for every of the three sectors
# each

ann_el_demand_per_sector = {
    'h0': 3000,
    'g0': 3000,
    'i0': 3000}

ann_el_demand_per_sector_2 = {
    'h0': None,
    'g0': None,
    'i0': None}

ann_el_demand_per_sector_3 = {
    'h0': None,
    'g0': 3000,
    'i0': 3000}

# Following data has to be provided if sectoral annual demand is specified as
# None which corresponds to unknown demand

# Household sector data (h)
# annual electrical demand per household member for one-, two-, three- and
# four-person household in kWh per year. source: BDEW2010

population = 40000

ann_el_demand_per_person = {
    'one': 2050,
    'two': 1720,
    'three': 1350,
    'four': 1235}

number_household_members = {
    'one': 10000,
    'two': 10000,
    'three': 10000,
    'four': 10000}

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
demand.val = dm.electrical_demand(method='calculate_profile',
                                  year=year,
                                  ann_el_demand_per_sector=
                                  ann_el_demand_per_sector) \
                                  .elec_demand

# Example 2: Calculate profile with unknown annual electric demand per sector
#
demand_2 = sink.Simple(uid="demand_2", inputs=[bel])
demand_2.val = dm.electrical_demand(method='calculate_profile',
                                    year=year,
                                    ann_el_demand_per_sector=
                                        ann_el_demand_per_sector_2,
                                    ann_el_demand_per_person=
                                        ann_el_demand_per_person,
                                    number_household_members=
                                        number_household_members,
                                    household_members_all=
                                        household_members_all,
                                    population=
                                        population,
                                    comm_ann_el_demand_state=
                                        comm_ann_el_demand_state,
                                    comm_number_of_employees_state=
                                        comm_number_of_employees_state,
                                    comm_number_of_employees_region=
                                        comm_number_of_employees_region) \
                                    .elec_demand

demand_3 = sink.Simple(uid="demand_3", inputs=[bel])
demand_3.val = dm.electrical_demand(method='calculate_profile',
                                    year=year,
                                    ann_el_demand_per_sector=
                                        ann_el_demand_per_sector_3,
                                    ann_el_demand_per_person=
                                        ann_el_demand_per_person,
                                    number_household_members=
                                        number_household_members,
                                    household_members_all=
                                        household_members_all,
                                    population=
                                        population) \
                                    .elec_demand

print(demand.val)
print(demand_2.val)
print(demand_3.val)
