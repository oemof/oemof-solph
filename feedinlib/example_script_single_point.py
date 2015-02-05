#!/usr/bin/python
# -*- coding: utf-8

import sys
from os import path
import matplotlib.pyplot as plt
import pv_feedin_file as pv

# imports init_local from .python_local (for database connection settings)
import init_local as init_db

# get basic db dict
DIC = init_db.pg_db()

# retrieve pv system params and region definition
param, region = pv.param_definition()

# examplary coords pairs (RLI)
coords = {'lon': 13.532892,
        'lat': 52.457429}

# expand region dict
region['longitude'] = coords['lon']
region['latitude'] = coords['lat']

# calculate annual feedin time series for a single pv system
ts = pv.pv_timeseries(param, region, DIC, param['year'])

# do some output stuff
print('Full load hours: ' + str(sum(ts)) + ' h')
#plt.plot(ts)
#plt.show()

