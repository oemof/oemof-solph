# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 15:49:36 2015

@author: cord
"""

import matplotlib.pyplot as plt
import pandas as pd
from oemof.outputlib import devplots
from oemof.core.network.entities import Bus


def plot_dispatch(bus_to_plot, results, timesteps, data, storage, demand):
    # plotting: later as multiple pdf with pie-charts and topology?
    import numpy as np
    import matplotlib as mpl
    import matplotlib.cm as cm

    # data preparation
    x = np.arange(len(timesteps))
    y = []
    labels = []
    for c in data:
        #if bus_to_plot in c.results['out']:
        y.append(results[c][bus_to_plot])
        labels.append(c.uid)

    # plot production
    fig, ax = plt.subplots()
    sp = ax.stackplot(x, y,
                      colors=('yellow', 'blue', 'grey', 'red'),
                      linewidth=0)

    proxy = [mpl.patches.Rectangle((0, 0), 0, 0,
                                   facecolor=
                                   pol.get_facecolor()[0]) for pol in sp]
    # plot demand
    ax.step(x, results[demand.inputs[0]][demand], c="black", lw=2)

    # storage soc (capacity at every timestep)
#        ax.step(x, sto_simple.results['cap'], c='green', lw=2.4)

    # plot storage input
    ax.step(x, (np.asarray(results[storage.inputs[0]][storage])
                + np.asarray(results[demand.inputs[0]][demand])),
            c='red', ls='-', lw=1)

    ax.legend(proxy, labels)
    ax.grid()

    ax.set_xlabel('Timesteps in h')
    ax.set_ylabel('Power in kW')
    ax.set_title('Dispatch')
    plt.show()


def use_devplot(energysystem, uid, prange):
    energysystem.year = 2010

    # Initialise the plot object with the energy system
    plot = devplots.stackplot(es=energysystem)

    # Prepare the time series to plot the balance around the electricity bus
    plot.plot_dc = plot.create_io_df(uid)

    # Plotting the bus balance with an own color set.
    c_in = ['#4536bb', '#ffcc00', '#7c7c7c', '#ff5e5e']
    c_out = ['#0cce1e', '#ff5e5e']
    plot.full(prange, in_color=c_in, out_color=c_out)
    plt.show()


def print_results(bus_to_print, data, demand, transformers, storage,
                  energysystem):
    import numpy as np
    results = energysystem.results
    # demand results
    print('sum elec demand: ',
          np.asarray(results[bus_to_print][demand]).sum())

    # production results
    sum_production = np.array([])
    for c in data:
        print(c.uid)
        res = np.asarray(results[c][bus_to_print])
        sum_production = np.append(sum_production, res)
        print('sum: ', res.sum())
        print('maximum value: ', res.max())

    # only non renewable production results
    transf = np.array([])
    for t in transformers:
        res = np.asarray(results[t][bus_to_print])
        transf = np.append(transf, res)
        print('sum non renewable: ', transf.sum())

    # storage state and capacity
    storage_soc = np.asarray(results[storage][storage])
    print('sum storage content: ', storage_soc.sum())
    print('storage capacity: ', storage_soc.max())

    # storage load
    storage_load = np.asarray(
        results[storage.inputs[0]][storage])
    print('sum storage load: ', storage_load.sum())
    print('maximum storage load: ', storage_load.max())

    # excess
    excess = results[bus_to_print]['excess']
    print('sum excess: ', np.asarray(excess).sum())

    # autarky degree
    print('autarky degree: ', (sum_production.sum()  # production
                               - transf.sum()  # minus non renewable prod.
                               - np.asarray(excess).sum() # minus excess
                               - storage_load.sum()) /  # minus stor. load
                               np.asarray(results[bus_to_print][demand]).sum())
                               #  in
                                          # proportion to the demand