#!/usr/bin/python
# -*- coding: utf-8

# TESTAUFRUF ZUM ERSTELLEN DER PV-ZEITREIHEN

import sys
sys.path.append('/home/caro/rlihome/Git/pahesmf') # temporär: Einbinden meines
# lokalen pahesmf-Pfads, notwendig zur Erstellung von DIC
import src.dinput.read_pahesmf as din

from feedinlib.pv_feed import *

DIC = din.read_basic_dc()

print(DIC)

site = {'module_name': 'Advent_Solar_Ventura_210___2008_',
        'azimuth': 0,
        'tilt': 30,
        'parallelStrings': 1,
        'seriesModules': 1,
        'TZ': 0.5,
        'albedo': 0.2}

obj = PvFeed(DIC, site, '2010', '201')
#timeseries = obj.apply_model()

#Neue_Instanz=Neue_Klasse(1,2,3)