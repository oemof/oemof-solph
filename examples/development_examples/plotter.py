# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 15:49:36 2015

@author: cord
"""

import matplotlib.pyplot as plt

from oemof.core.network.entities import Bus

def plot_dispatch(bus_to_plot, timesteps, data, storage, demand):
    # plotting: later as multiple pdf with pie-charts and topology?
    import numpy as np
    import matplotlib as mpl
    import matplotlib.cm as cm

    # data preparation
    x = np.arange(len(timesteps))
    y = []
    labels = []
    for c in data:
        if bus_to_plot in c.results['out']:
            y.append(c.results['out'][bus_to_plot])
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
    ax.step(x, demand.results['in'][demand.inputs[0].uid],
            c="black", lw=2)

    # storage soc (capacity at every timestep)
#        ax.step(x, sto_simple.results['cap'], c='green', lw=2.4)

    # plot storage input
    ax.step(x, (np.asarray(
        storage.results['in'][storage.inputs[0].uid])
        + np.asarray(
            demand.results['in'][demand.inputs[0].uid])),
        c='red', ls='-', lw=1)

    ax.legend(proxy, labels)
    ax.grid()

    ax.set_xlabel('Timesteps in h')
    ax.set_ylabel('Power in kW')
    ax.set_title('Dispatch')

def print_results(bus_to_print, data, demand, transformers, storage,
                  energysystem):
    import numpy as np

    # demand results
    print('sum elec demand: ',
          np.asarray(demand.results['in'][bus_to_print]).sum())

    # production results
    sum_production = np.array([])
    for c in data:
        print(c)
        res = np.asarray(c.results['out'][bus_to_print])
        sum_production = np.append(sum_production, res)
        print('sum: ', res.sum())
        print('maximum value: ', res.max())

    # only non renewable production results
    transf = np.array([])
    for t in transformers:
        res = np.asarray(t.results['out'][bus_to_print])
        transf = np.append(transf, res)
        print('sum non renewable: ', transf.sum())

    # storage state and capacity
    storage_soc = np.asarray(storage.results['cap'])
    print('sum storage content: ', storage_soc.sum())
    print('storage capacity: ', storage_soc.max())

    # storage load
    storage_load = np.asarray(
        storage.results['in'][storage.inputs[0].uid])
    print('sum storage load: ', storage_load.sum())
    print('maximum storage load: ', storage_load.max())

    # excess
    excess = list()
    for t in energysystem.simulation.timesteps:
        excess.append(
          getattr(energysystem.optimization_model,
                  str(Bus)).excess_slack['bel', t].value)

    print('sum excess: ', np.asarray(excess).sum())

    # autarky degree
    print('autarky degree: ', (sum_production.sum()  # production
                               - transf.sum()  # minus non renewable prod.
                               - np.asarray(excess).sum() # minus excess
                               - storage_load.sum()) /  # minus stor. load
                               np.asarray(demand.results['in']
                                          [bus_to_print]).sum())  #  in
                                          # proportion to the demand