# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm


# global plotting options
plt.rcParams.update(plt.rcParamsDefault)
matplotlib.style.use('ggplot')
plt.rcParams['lines.linewidth'] = 2.5
plt.rcParams['axes.facecolor'] = 'silver'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams.update({'font.size': 10})
plt.rcParams['image.cmap'] = 'Blues'

# read file
file = ('results/'
'scenario_nep_2025_2016-08-05 09:41:23.723491_DE.csv')

df_raw = pd.read_csv(file, parse_dates=[0], index_col=0, keep_date_col=True)
df_raw.head()
df_raw.columns


# %% plot fundamental and regression prices (1 year)

df = df_raw[['duals']]

price_real = pd.read_csv('price_eex_day_ahead_2014.csv')
price_real.index = df_raw.index

df = pd.concat([price_real, df], axis=1)
df.columns = ['price_real', 'price_model']

df.plot(drawstyle='steps')
plt.xlabel('Zeit in h')
plt.ylabel('Preis in EUR/MWh')
plt.show()

# %% plot fundamental and regression prices (8 weeks)

df = df_raw[['duals']]

price_real = pd.read_csv('price_eex_day_ahead_2014.csv')
price_real.index = df_raw.index

df = pd.concat([price_real, df], axis=1)
df.columns = ['price_real', 'price_model']

df[(24 * 7)*8:(24 * 7)*16].plot(drawstyle='steps')
plt.xlabel('Zeit in h')
plt.ylabel('Preis in EUR/MWh')
plt.show()

# %% polynom fitting: residual load

# prepare dataframe for fit
residual_load = df_raw['DE_load'] + df_raw['AT_load'] + df_raw['LU_load'] - \
                df_raw['DE_wind'] - df_raw['AT_wind'] - df_raw['LU_wind'] - \
                df_raw['DE_solar'] - df_raw['AT_solar'] - df_raw['LU_solar']

# real prices
price_real = pd.read_csv('price_eex_day_ahead_2014.csv')
price_real.index = df_raw.index

df = pd.concat([residual_load, price_real, df_raw['duals']], axis=1)
df.columns = ['res_load', 'price_real', 'price_model']

# fit polynom of 3rd degree to price_real(res_load)
z = np.polyfit(df['res_load'], df['price_real'], 3)
p = np.poly1d(z)
df['price_polynom_res_load'] = p(df['res_load'])

df.plot.scatter(x='res_load', y='price_real')
plt.plot(df['res_load'],
         (
          z[0] * df['res_load'] ** 3 +
          z[1] * df['res_load'] ** 2 +
          z[2] * df['res_load'] ** 1 +
          z[3]
          ), color='red')
plt.xlabel('Residuallast in MW')
plt.ylabel('Day-Ahead Preis in EUR/MWh')
plt.show()


# %% dispatch plot (balance doesn't fit since DE/LU/AT are one bidding area)

# country code
cc = 'DE'

# get fossil and renewable power plants
fuels = ['run_of_river', 'biomass', 'solar', 'wind', 'uranium', 'lignite',
         'hard_coal', 'gas', 'mixed_fuels', 'oil', 'load', 'excess',
         'shortage']

dispatch = pd.DataFrame()

for f in fuels:
    cols = [c for c in df_raw.columns if f in c and cc in c]
    dispatch[f] = df_raw[cols].sum(axis=1)

dispatch.index = df_raw.index

# get imports and exports and aggregate columns
cols = [c for c in df_raw.columns if 'powerline' in c and cc in c]
powerlines = df_raw[cols]

exports = powerlines[[c for c in powerlines.columns
                      if c.startswith(cc + '_')]]

imports = powerlines[[c for c in powerlines.columns
                      if '_' + cc + '_' in c]]

dispatch['imports'] = imports.sum(axis=1)
dispatch['exports'] = exports.sum(axis=1)

# get imports and exports and aggregate columns
phs_in = df_raw[[c for c in df_raw.columns if 'phs_in' in c and cc in c]]
phs_out = df_raw[[c for c in df_raw.columns if 'phs_out' in c and cc in c]]
phs_level = df_raw[[c for c in df_raw.columns if 'phs_level' in c and cc in c]]

dispatch['phs_in'] = phs_in.sum(axis=1)
dispatch['phs_out'] = phs_out.sum(axis=1)
dispatch['phs_level'] = phs_level.sum(axis=1)

# MW to GW
dispatch = dispatch.divide(1000)

# translation
dispatch_de = dispatch[
    ['run_of_river', 'biomass', 'solar', 'wind', 'uranium', 'lignite',
     'hard_coal', 'gas', 'oil', 'mixed_fuels', 'phs_out', 'load', 'imports',
     'exports']]

# dict with new column names
en_de = {'run_of_river': 'Laufwasser',
         'biomass': 'Biomasse',
         'solar': 'Solar',
         'wind': 'Wind',
         'uranium': 'Kernenergie',
         'lignite': 'Braunkohle',
         'hard_coal': 'Steinkohle',
         'gas': 'Gas',
         'mixed_fuels': 'Sonstiges',
         'oil': 'Öl',
         'phs_out': 'Pumpspeicher',
         'imports': 'Import',
         'exports': 'Export',
         'load': 'Last'}
dispatch_de = dispatch_de.rename(columns=en_de)

# area plot. gute woche: '2014-01-21':'2014-01-27'
dispatch_de[['Biomasse', 'Laufwasser', 'Kernenergie', 'Braunkohle',
             'Steinkohle', 'Gas', 'Öl', 'Sonstiges', 'Solar', 'Wind',
             'Pumpspeicher', 'Import']][0:24*7] \
             .plot(kind='area', stacked=True, linewidth=0, legend='reverse',
                   cmap=cm.get_cmap('Spectral'))
plt.xlabel('Datum')
plt.ylabel('Leistung in  GW')
plt.ylim(0, max(dispatch_de.sum(axis=1)) * 0.65)
plt.show()

# %% duration curves for power plants
curves = pd.concat(
    [dispatch_de[col].sort_values(ascending=False).reset_index(drop=True)
     for col in dispatch_de], axis=1)
curves[['Kernenergie', 'Braunkohle', 'Steinkohle', 'Gas', 'Öl',
        'Sonstiges', 'Solar', 'Wind', 'Pumpspeicher',
        'Import', 'Export']].plot(cmap=cm.get_cmap('Spectral'))
plt.xlabel('Stunden des Jahres')
plt.ylabel('Leistung in GW')
plt.show()

# %% duration curves for power plants ordered by load (stacked)
curves_stacked = dispatch_de
curves_stacked = curves_stacked.sort_values(by=['Last'], ascending=False)
curves_stacked.reset_index(drop=True, inplace=True)

curves_stacked[['Biomasse', 'Laufwasser', 'Kernenergie', 'Braunkohle',
                'Steinkohle', 'Gas', 'Öl', 'Sonstiges', 'Solar', 'Wind',
                'Pumpspeicher',
                'Import']].plot(kind='area', stacked=True,
                                legend='reverse',
                                cmap=cm.get_cmap('Spectral'))
plt.xlabel('Stunden des Jahres geordnet nach der Last')
plt.ylabel('Leistung in GW')
plt.show()

# %% duration curves for all powerlines
pls = pd.concat(
    [powerlines[col].sort_values(ascending=False).reset_index(drop=True)
     for col in powerlines], axis=1)
pls.plot(legend='reverse', cmap=cm.get_cmap('Spectral'))
plt.xlabel('Stunden des Jahres')
plt.ylabel('Leistung in GW')
plt.show()

# %% duraction curve for one cable e.g. NordLink cable
cable = df_raw[['DE_NO_powerline', 'NO_DE_powerline']]
cable = pd.concat(
    [cable[col].sort_values(ascending=False).reset_index(drop=True)
     for col in cable], axis=1)
cable = cable.rename(columns={'DE_NO_powerline': 'DE-NO',
                              'NO_DE_powerline': 'NO-DE'})
cable.plot(legend='reverse', cmap=cm.get_cmap('Spectral'))
plt.xlabel('Stunden des Jahres')
plt.ylabel('Leistung in GW')
plt.ylim(0, max(cable.sum(axis=1)) * 1.2)
plt.show()

# %% duraction curve for prices
power_price_real = pd.read_csv('price_eex_day_ahead_2014.csv')
power_price_real.set_index(df_raw.index, drop=True, inplace=True)
power_price = pd.concat([power_price_real,
                         df_raw[['duals']]], axis=1)
power_price = pd.concat(
    [power_price[col].sort_values(ascending=False).reset_index(drop=True)
     for col in power_price], axis=1)
power_price.plot(legend='reverse', cmap=cm.get_cmap('Spectral'))
plt.xlabel('Stunden des Jahres')
plt.ylabel('Preis in EUR/MWh')
plt.show()

# %% scaling

df = df_raw[['duals']]
df['duals_x_1_5'] = df['duals'] + \
    (df['duals'].subtract(df['duals'].mean())) * 1.5
df['duals_x_2'] = df['duals'] + \
    (df['duals'].subtract(df['duals'].mean())) * 2
df['duals_x_2'] = df['duals'] + \
    (df['duals'].subtract(df['duals'].mean())) * 3

df[0:24*31].plot(drawstyle='steps')
plt.show()

# %% boxplot for prices: monthly

df = df_raw[['duals']]
df['dates'] = df.index
df['month'] = df.index.month

df_box = df.pivot(index='dates', columns='month', values='duals')

bp = df_box.boxplot(showfliers=False, showmeans=True, return_type='dict')
plt.xlabel('Monat', fontsize=20)
plt.ylabel('Preis in EUR/MWh', fontsize=22)
plt.tick_params(axis='y', labelsize=14)
plt.tick_params(axis='x', labelsize=14)
plt.legend('')

[[item.set_linewidth(2) for item in bp['boxes']]]
[[item.set_linewidth(2) for item in bp['fliers']]]
[[item.set_linewidth(2) for item in bp['medians']]]
[[item.set_linewidth(2) for item in bp['means']]]
[[item.set_linewidth(2) for item in bp['whiskers']]]
[[item.set_linewidth(2) for item in bp['caps']]]

[[item.set_color('k') for item in bp['boxes']]]
[[item.set_color('k') for item in bp['fliers']]]
[[item.set_color('k') for item in bp['medians']]]
[[item.set_color('k') for item in bp['whiskers']]]
[[item.set_color('k') for item in bp['caps']]]

[[item.set_markerfacecolor('k') for item in bp['means']]]

plt.show()
