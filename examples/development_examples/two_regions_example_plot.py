#!/usr/bin/python3
# -*- coding: utf-8

import logging
import matplotlib.pyplot as plt

from oemof.outputlib import to_pandas as tpd
from oemof.tools import logger
from oemof.core import energy_system as es


# The following dictionaries are a workaround due to issue #26
rename = {
    "(val, ('sink', 'Landkreis Wittenberg', 'elec'))": "elec demand",
    "(val, ('sto_simple', 'Landkreis Wittenberg', 'elec'))": "battery",
    "(val, ('transport', 'bus', 'Stadt Dessau-Rosslau', 'elec', 'bus', 'Landkreis Wittenberg', 'elec'))": "to Dessau",
    "(val, ('FixedSrc', 'Landkreis Wittenberg', 'pv_pwr'))": "pv power",
    "(val, ('FixedSrc', 'Landkreis Wittenberg', 'wind_pwr'))": "wind power",
    "(val, ('transformer', 'Landkreis Wittenberg', 'natural_gas'))": "gas power plant",
    "(val, ('transport', 'bus', 'Landkreis Wittenberg', 'elec', 'bus', 'Stadt Dessau-Rosslau', 'elec'))": "to Wittenberg",
    "(val, ('sink', 'Stadt Dessau-Rosslau', 'elec'))": "elec demand",
    "(val, ('sto_simple', 'Stadt Dessau-Rosslau', 'elec'))": "battery",
    "(val, ('FixedSrc', 'Stadt Dessau-Rosslau', 'pv_pwr'))": "pv power",
    "(val, ('FixedSrc', 'Stadt Dessau-Rosslau', 'wind_pwr'))": "wind power",
    "(val, ('transformer', 'Stadt Dessau-Rosslau', 'lignite'))": "lignite power plant",
    "(val, ('transformer', 'Stadt Dessau-Rosslau', 'natural_gas'))": "gas power plant",
    }

# Define a color set for the plots.
cdict = {}

cdict["('FixedSrc', 'Landkreis Wittenberg', 'wind_pwr')"] = '#4536bb'
cdict["('FixedSrc', 'Landkreis Wittenberg', 'pv_pwr')"] = '#ffcc00'
cdict["('FixedSrc', 'Stadt Dessau-Rosslau', 'wind_pwr')"] = '#4536bb'
cdict["('FixedSrc', 'Stadt Dessau-Rosslau', 'pv_pwr')"] = '#ffcc00'

cdict["('transport', 'bus', 'Landkreis Wittenberg', 'elec', 'bus', 'Stadt Dessau-Rosslau', 'elec')"] = '#643780'
cdict["('transport', 'bus', 'Stadt Dessau-Rosslau', 'elec', 'bus', 'Landkreis Wittenberg', 'elec')"] = '#643780'

cdict["('transformer', 'Landkreis Wittenberg', 'natural_gas')"] = '#7c7c7c'
cdict["('transformer', 'Stadt Dessau-Rosslau', 'natural_gas')"] = '#7c7c7c'
cdict["('transformer', 'Landkreis Wittenberg', 'lignite')"] = '#000000'
cdict["('transformer', 'Stadt Dessau-Rosslau', 'lignite')"] = '#000000'

cdict["('sto_simple', 'Landkreis Wittenberg', 'elec')"] = '#ff5e5e'
cdict["('sto_simple', 'Stadt Dessau-Rosslau', 'elec')"] = '#ff5e5e'

cdict["('sink', 'Landkreis Wittenberg', 'elec')"] = '#0cce1e'
cdict["('sink', 'Stadt Dessau-Rosslau', 'elec')"] = '#0cce1e'


# Define the oemof default logger
logger.define_logging()

# Create an energy system
TwoRegExample = es.EnergySystem()

# Restoring a dumped EnergySystem
logging.info(TwoRegExample.restore())

esplot = tpd.DataFramePlot(energy_system=TwoRegExample)

fig = plt.figure(figsize=(24, 14))
plt.rc('legend', **{'fontsize': 19})
plt.rcParams.update({'font.size': 14})
plt.style.use('ggplot')

n = 1

# Loop over the regions to plot them.
for region in TwoRegExample.regions:
    uid = str(('bus', region.name, 'elec'))

    esplot.ax = fig.add_subplot(2, 1, n)
    n += 1
    handles, labels = esplot.io_plot(
        uid, cdict,
        date_from="2010-06-01 00:00:00",
        date_to="2010-06-8 00:00:00",
        line_kwa={'linewidth': 4})

    new_labels = []
    for lab in labels:
        new_labels.append(rename.get(str(lab), lab))

    esplot.ax.set_ylabel('Power in MW')
    esplot.ax.set_xlabel('')
    esplot.ax.set_title(region.name)

    esplot.set_datetime_ticks(tick_distance=24, date_format='%d-%m-%Y')
    esplot.outside_legend(handles=handles, labels=new_labels)

plt.show()
