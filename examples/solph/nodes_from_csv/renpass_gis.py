# -*- coding: utf-8 -*-

import logging
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import cm
from datetime import datetime
from oemof.tools import logger
from oemof.solph import OperationalModel, EnergySystem, GROUPINGS
from oemof.solph import NodesFromCSV
from oemof.outputlib import ResultsDataFrame
from Quandl import Quandl


def stopwatch():
    if not hasattr(stopwatch, "now"):
        stopwatch.now = datetime.now()
        return None
    last = stopwatch.now
    stopwatch.now = datetime.now()
    return str(stopwatch.now-last)[0:-4]

logger.define_logging()


# %% configuration

nodes_flows = 'nep_2014_aggr.csv'
nodes_flows_sequences = 'nep_2014_aggr_seq.csv'

date_from = '2014-01-01 00:00:00'
date_to = '2014-12-31 23:00:00'

datetime_index = pd.date_range(date_from, date_to, freq='60min')


# %% model creation and solving

es = EnergySystem(groupings=GROUPINGS, time_idx=datetime_index)

nodes = NodesFromCSV(file_nodes_flows=nodes_flows,
                     file_nodes_flows_sequences=nodes_flows_sequences,
                     delimiter=',')

stopwatch()
om = OperationalModel(es)
print('OM creation time: ' + stopwatch())

om.receive_duals()

om.solve(solver='gurobi', solve_kwargs={'tee': True})
print('Optimization time: ' + stopwatch())

logging.info('Done!')

logging.info('Check the results')


# %% output: model data

results = ResultsDataFrame(energy_system=es)


# %% output: plotting of production (model vs. entso-e dataset)

# global plotting options
plt.rcParams.update(plt.rcParamsDefault)
matplotlib.style.use('ggplot')
plt.rcParams['lines.linewidth'] = 1.2
plt.rcParams['axes.facecolor'] = 'silver'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams.update({'font.size': 10})
plt.rcParams['image.cmap'] = 'Spectral'
#plt.rcParams.update({'legend.fontsize': 6})

# colormap for plots
cmap = cm.Blues

# country codes
country_codes = ['AT', 'BE', 'CH', 'CZ', 'DE', 'DK', 'FR', 'LU', 'NL', 'NO',
                 'PL', 'SE']

new_colnames = {
                'net_gen_nuclear': 'uranium',
                '-> of which lignite': 'lignite',
                '-> of which hard coal': 'hard_coal',
                '-> of which gas': 'gas',
                '-> of which oil': 'oil',
                '-> of which mixed fuels': 'mixed_fuels',
                '-> of_which_other_fossil_fuels': 'other_fossil',
                '-> of which wind': 'wind',
                '-> of which solar': 'solar',
                '-> of which biomass': 'biomass',
                '-> of_which_other_renewable': 'other_renewable',
                '-> of_which_renew': 'run_of_river',
                '-> of_which_other_hydro': 'other_hydro',
                'pump': 'pumped_hydro',
                'consumption': 'load',
                'exg_saldo': 'import_export',
                'net_gen_not_clearly': 'generation_not_clearly'
                }

# quandl data gets downloaded into dataframes in loop
# see: https://www.quandl.com/data/ENTSOE/ or ENTSO-E data portal
auth_tok = "QFsHqrY3BqG91_f1Utsj"

for cc in country_codes:

    inputs = results.slice_unstacked(bus_label=cc + '_bus_el', type='input',
                                     date_from=date_from, date_to=date_to,
                                     formatted=True)
    inputs.rename(columns={cc + '_storage_phs': cc + '_storage_phs_out'},
                  inplace=True)

    outputs = results.slice_unstacked(bus_label=cc + '_bus_el', type='output',
                                      date_from=date_from, date_to=date_to,
                                      formatted=True)

    outputs.rename(columns={cc + '_storage_phs': cc + '_storage_phs_in'},
                   inplace=True)

    other = results.slice_unstacked(bus_label=cc + '_bus_el', type='other',
                                    date_from=date_from, date_to=date_to,
                                    formatted=True)

    # data from model in MWh
    model_data = pd.concat([inputs, outputs], axis=1)

    powerline_cols = [col for col in model_data.columns
                      if 'powerline' in col]
    powerlines = model_data[powerline_cols]

    exports = powerlines[
        [col for col in powerlines.columns
         if cc + '_' in col]].sum(axis=1)
    exports = exports.to_frame()
    imports = powerlines[
        [col for col in powerlines.columns
         if '_' + cc + '_' in col]].sum(axis=1)
    imports = imports.to_frame()
    imports_exports = imports-exports
    imports_exports.columns = ['import_export']

    model_data = pd.concat([model_data, imports_exports], axis=1)
    model_data = model_data[
        [col for col in model_data.columns
         if 'powerline' not in col
         if 'shortage' not in col
         if 'excess' not in col]]
    model_data.rename(columns=lambda x: x.replace(cc + '_', ''), inplace=True)
    model_data = model_data/1000
    model_data_hourly = model_data
    model_data = model_data.resample('1A').sum()

    # exclude AT as its pps are connected to the german electricity bus
    if cc not in ['AT', 'LU', 'DE']:
        model_data = model_data[
             ['load', 'solar', 'wind', 'pp_uranium', 'pp_lignite',
              'pp_hard_coal', 'pp_gas', 'pp_oil', 'pp_mixed_fuels',
              'pp_biomass', 'run_of_river', 'storage_phs_out',
              'import_export']]

    # data from ENTSO-E in GWh
    idx = 'ENTSOE/' + cc + '_PROD'
    entsoe_data = Quandl.get(idx,
                             trim_start="2014-01-01",
                             trim_end="2014-12-31",
                             authtoken=auth_tok)
    entsoe_data.rename(columns=new_colnames, inplace=True)
    entsoe_data = entsoe_data[['load', 'solar', 'wind', 'uranium', 'lignite',
                               'hard_coal', 'gas', 'oil', 'mixed_fuels',
                               'biomass', 'run_of_river', 'pumped_hydro',
                               'import_export', 'other_fossil',
                               'other_hydro', 'generation_not_clearly']]
    entsoe_data.index = pd.date_range(entsoe_data.index[0], periods=12,
                                      freq='M')
    entsoe_data = entsoe_data.resample('1A').sum()

    # plotting
    fig, axes = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True)
    fig.suptitle('Annual production(' + cc + ')' + ' for ' + nodes_flows,
                 fontsize=16)

    model_plot = model_data.plot(kind='bar', stacked=False, ax=axes[0])
    model_plot.set_ylabel('Energy in GWh')
    model_plot.set_xlabel('Model Results')
    model_plot.set_xticklabels([])
    model_plot.legend(loc='upper right', ncol=1, fontsize=6)

    entsoe_plot = entsoe_data.plot(kind='bar', stacked=False, ax=axes[1])
    entsoe_plot.set_ylabel('Energy in GWh')
    entsoe_plot.set_xlabel('ENTSO-E Data for 2014')
    entsoe_plot.set_xticklabels([])
    entsoe_plot.legend(loc='upper right', ncol=1, fontsize=6)

    plt.savefig('results/results_balance_' + cc + '_' +
                nodes_flows.replace('.csv', '') + '_' +
                str(datetime.now()) +
                '.pdf', orientation='landscape')
    plt.close()

    # plotting of prices for Germany
    if cc is 'DE':
        power_price_model = other['duals']
        power_price_real = pd.read_csv('day_ahead_price_2014_eex.csv')
        power_price_real.set_index(power_price_model.index, drop=True,
                                   inplace=True)
        power_price = pd.concat([power_price_model, power_price_real], axis=1)
        power_price.rename(columns={'price_avg_real': 'eex_day_ahead_2014',
                                    'duals': 'power_price_model'},
                           inplace=True)

        # dispatch and prices in one file
        power_price = pd.concat([inputs, outputs, power_price], axis=1)
        power_price.to_csv('results/results_dispatch_prices_DE_' +
                           str(datetime.now()) + nodes_flows)

        # plot
        power_price = power_price[['eex_day_ahead_2014', 'power_price_model']]
        nrow = 4
        fig, axes = plt.subplots(nrows=nrow, ncols=1)
        fig.suptitle('Power prices (' + cc + ')' + ' for ' + nodes_flows,
                     fontsize=16)

        power_price.plot(drawstyle='steps-post', ax=axes[0],
                         title='Hourly price', sharex=True)
        power_price.resample('1D').mean().plot(drawstyle='steps-post',
                                               ax=axes[1],
                                               title='Daily mean',
                                               sharex=True)
        power_price.resample('1W').mean().plot(drawstyle='steps-post',
                                               ax=axes[2],
                                               title='Weekly mean',
                                               sharex=True)
        power_price.resample('1M').mean().plot(drawstyle='steps-post',
                                               ax=axes[3],
                                               title='Montly mean (base)',
                                               sharex=True)
        for i in range(0, nrow):
            axes[i].set_ylabel('EUR/MWh')
            axes[i].legend(loc='upper right', ncol=2, fontsize=6)

        plt.savefig('results/results_prices_' + cc + '_' +
                    nodes_flows.replace('.csv', '') + '_' +
                    str(datetime.now()) +
                    '.pdf', orientation='landscape')
        plt.close()

        # 15 minute value prices
        power_price = power_price[
            ['power_price_model', 'eex_day_ahead_2014']].resample(
                '15Min').bfill().to_csv(
                    'results/results_power_price_DE_15_min_' +
                    str(datetime.now()) + nodes_flows)

#    # dispatch
#    if cc not in ['AT', 'LU']:
#
#        model_data_hourly = model_data_hourly.resample('1M').sum()
#        model_data_hourly.loc[:, 'load'] *= -1
#        bar = model_data_hourly.plot(kind='bar', stacked=True)
#        bar.set_ylabel('Energy in GWh')
#        bar.set_xlabel('Month')
#        bar.set_xticklabels([i for i in range(1, 13)])
#        bar.legend(loc='center left', ncol=1, fontsize=5,
#                   bbox_to_anchor=(0.99, 0.5))
#        plt.savefig('results/results_dispatch_' + cc + '_' +
#                    nodes_flows.replace('.csv', '') + '_' +
#                    str(datetime.now()) +
#                    '.pdf', orientation='landscape')
#        plt.close()
#

#        nrow = 8
#        ncol = 2
#
#        dispatch = inputs.plot(kind='line', subplots=True, grid=True,
#                               sharex=False, sharey=False, legend=True,
#                               title='Dispatch (' + cc + ') for ' +
#                               nodes_flows.replace('.csv', '.pdf'),
#                               layout=(nrow, ncol))
#        for c in range(0, ncol):
#            for r in range(0, nrow):
#                dispatch[r, c].set_ylabel('MW')
#                dispatch[r, c].legend(loc='upper right')
#        plt.show()
