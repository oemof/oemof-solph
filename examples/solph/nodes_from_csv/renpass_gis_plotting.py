# -*- coding: utf-8 -*-

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

from datetime import datetime
from matplotlib import cm
from Quandl import Quandl

# %% configuration

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

# %% plotting

# dateiauswahl basierend auf unique substring(s), die übergeben werden
# im standardfall läuft die schleife dann nur 1x durch

scenario_name = 'blablubb'
folder = 'results/'
unique_substring = '2016-07-28 09:27'

for file in os.listdir(folder):
    if unique_substring in file:
        cc = ''.join([c for c in file if c.isupper()])

        model_data = pd.read_csv(folder + file, parse_dates=[0], index_col=0,
                                 keep_date_col=True)

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
        model_data.rename(columns=lambda x: x.replace(cc + '_', ''),
                          inplace=True)
        model_data = model_data/1000
        model_data_hourly = model_data
        model_data = model_data.resample('1A').sum()

        # exclude AT, LU and DE as the pps are connected to the german bus
        # and the naming doesn't match
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
        entsoe_data = entsoe_data[['load', 'solar', 'wind', 'uranium',
                                   'lignite', 'hard_coal', 'gas', 'oil',
                                   'mixed_fuels', 'biomass', 'run_of_river',
                                   'pumped_hydro', 'import_export',
                                   'other_fossil', 'other_hydro',
                                   'generation_not_clearly']]
        entsoe_data.index = pd.date_range(entsoe_data.index[0], periods=12,
                                          freq='M')
        entsoe_data = entsoe_data.resample('1A').sum()

        # plotting
        fig, axes = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True)
        fig.suptitle('Annual production (' + cc + ')' + ' for ' + scenario_name,
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
                    scenario_name + '_' +
                    str(datetime.now()) +
                    '.pdf', orientation='landscape')
        plt.close()

        print('Land' + cc)

        # plotting of prices for Germany
        if cc == 'DE':
            model_data = pd.read_csv(folder + file, parse_dates=[0],
                                     index_col=0, keep_date_col=True)
            power_price_model = model_data['duals']
            power_price_real = pd.read_csv('price_eex_day_ahead_2014.csv')
            power_price_real.set_index(power_price_model.index, drop=True,
                                       inplace=True)
            power_price = pd.concat([power_price_model, power_price_real],
                                    axis=1)
            power_price.rename(columns={'price_eur_mwh': 'eex_day_ahead_2014',
                                        'duals': 'power_price_model'},
                               inplace=True)

            # plot
            power_price = power_price[['eex_day_ahead_2014',
                                       'power_price_model']]
            nrow = 4
            fig, axes = plt.subplots(nrows=nrow, ncols=1)
            fig.suptitle('Power prices (' + cc + ')' + ' for ' + scenario_name,
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
                        scenario_name + '_' +
                        str(datetime.now()) +
                        '.pdf', orientation='landscape')
            plt.close()
