#!/usr/bin/python3
# -*- coding: utf-8

import logging
import pandas as pd
import matplotlib.pyplot as plt
from oemof.outputlib import devplots
from oemof.tools import logger
from oemof.core import energy_system as es

# Define a color set for the plots.
color_def = {}

color_def['FixedSrc'] = {}
color_def['FixedSrc']['wind_pwr'] = '#4536bb'
color_def['FixedSrc']['pv_pwr'] = '#ffcc00'

color_def['transport'] = {}
color_def['transport']['LandkreisWittenberg'] = '#643780'
color_def['transport']['StadtDessau-Rosslau'] = '#643780'

color_def['transformer'] = {}
color_def['transformer']['natural_gas'] = '#7c7c7c'
color_def['transformer']['lignite'] = '#000000'

color_def['sto_simple'] = {}
color_def['sto_simple']['elec'] = '#ff5e5e'

color_def['sink'] = {}
color_def['sink']['elec'] = '#0cce1e'

# Define the oemof default logger
logger.define_logging()

# Create an energy system
TwoRegExample = es.EnergySystem()

# Restoring a dumped EnergySystem
logging.info(TwoRegExample.restore())

# Plotting the regions in one plot or separated plots
combined_plot = True

# Create a nested dictionary of DataFrames for inputs and outputs of a bus.
plot = devplots.stackplot(es=TwoRegExample)
color_dc = {}

if combined_plot:
    fig = plot.create_fig()
    i = 0
    n = len(TwoRegExample.regions)

# Loop over the regions to plot them.
for region in TwoRegExample.regions:
    uid = str(('bus', region.name, 'elec'))
    plot.plot_dc = plot.create_io_df(uid)

    # *** This part is just necessary to define colors and column names
    # *** This part is optional.
    io_ls = ['in', 'out']
    rename = {}
    color_dc[region.name] = {}
    for io in io_ls:
        rename = {}
        color_dc[region.name][io] = []
        for column in plot.plot_dc[io].keys():
            # The following lines are necessary due to an oemof bug (issue #26)
            uid = column.replace('(', '').replace("'", "").replace(')', '')
            uid = tuple(uid.split(','))

            # Set nicer names for the columns (default: uid).
            maintype = uid[0]
            subtype = uid[2].replace(' ', '')
            col = uid[0] + uid[2]

            # Set a color set according to the dictionary above.
            color_dc[region.name][io].append(color_def[maintype][subtype])
            rename[column] = col

        # Rename the columns.
        plot.plot_dc[io].rename(columns=rename, inplace=True)
    # *** Eding the optional part.

    prange = pd.date_range(pd.datetime(2010, 6, 1, 0, 0),
                           periods=168, freq='H')

    # Normaly just one of the following blocks are necessary.
    if not combined_plot:
        logging.info('Plotting region {0} in separated plots.'.format(
            region.name))
        plot.full(prange, out_color=color_dc[region.name]['out'],
                  in_color=color_dc[region.name]['in'])

    if combined_plot:
        logging.info('Plotting region {0} in a combined plot.'.format(
            region.name))
        i += 1
        ax = fig.add_subplot(n, 1, i)
        plot.part(prange, ax, out_color=color_dc[region.name]['out'],
                  in_color=color_dc[region.name]['in'])
plt.show()
