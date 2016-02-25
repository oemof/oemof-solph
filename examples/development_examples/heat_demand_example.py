# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 14:51:34 2016

@author: uwe
"""
import numpy as np
from matplotlib import pyplot as plt
from oemof.demandlib import energy_buildings as eb
from oemof.tools import helpers
from oemof import db

conn = db.connection()

# Erstellung eines Temperaturvektors
periods = 8760
temperature = np.ones(periods) * 263 + (
    np.random.rand(periods) * 40).round(0)

# Hilsfunktionen für die Standortbestimmung für die Feiertage
print(helpers.abbreviation_of_state('Schleswig-Holstein'))
print(helpers.fetch_admin_from_coord_osm((7.4, 55)))

# Bestimmung der Feiertage über Standort oder Ortsangabe
try:
    feiertage = helpers.get_german_holidays(
        2010, helpers.fetch_admin_from_coord_osm(7.4, 55))
except:
    feiertage = helpers.get_german_holidays(2010, ['Germany', 'SH'])

# Jetzt kannst Du mit oder ohne Feiertage arbeiten. Den UNterschied siehst Du
# in der "weekday"-Spalte (0=Feiertag, 1=Montag, 7=Sonntag). Bei der Berechnung
# werden Feiertag und Sonntag gleich behandelt, aber das lässt sich auch
# ändern.
time_df = helpers.create_basic_dataframe(2010)
print(time_df[:5])
time_df = helpers.create_basic_dataframe(2010, holidays=feiertage)
print(time_df[:5])

# Mögliche shlp-Typen sind:
# shlp = standardized heat load profile
# GMF, GPD, GHD, GWA, GGB, EFH, GKO, MFH, GBD, GBA, GMK, GBH, GGA, GHA

# Windklassen gibt es nur 2: windiger Standort 1, sonst 0

# Baualtersklassen 1-11, da finde ich gerade die Erklärung nicht zu

# Define default building
default_efh = eb.HeatBuilding(conn, time_df, temperature, shlp_type='EFH',
                               building_class=1, wind_class=0,
                               annual_heat_demand=150)

# Plot demand of building
default_efh.load.plot()
plt.show()
