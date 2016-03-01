# -*- coding: utf-8 -*-
"""

"""
import pandas as pd
from oemof.demandlib import energy_buildings as eb
from oemof.tools import helpers
from oemof.demandlib import bdew_heatprofile as bdew_heat

# read example temperature series
temperature = pd.read_csv("example_data.csv")["temperature"]

# get german holidays
holidays = helpers.get_german_holidays(2010, ['Germany', 'SH'])


# Define default building
efh = eb.Building()
# calculate heat load based on bdew profiles
efh.heat_load = efh.hourly_heat_demand(datapath="../../oemof/demandlib/data",
                                       year=2010, holiday=holidays,
                                       temperature=temperature,
                                       shlp_type='EFH',
                                       building_class=10,
                                       wind_class=1,
                                       annual_heat_demand=10000,
                                       function=bdew_heat.create_bdew_profile)

# Plot demand of building
ax = efh.heat_load.plot()
ax.set_xlabel("Hour of the year")
ax.set_ylabel("Heat demand in MW)
