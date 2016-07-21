# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

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

# read file
df_raw = pd.read_csv('results/results_dispatch_prices_DE_nep_2014_aggr.csv')
df_raw.head()
df_raw.columns


# prepare dataframe for fit
residual_load = df_raw['DE_load'] + df_raw['AT_load'] + df_raw['LU_load'] - \
                df_raw['DE_wind'] - df_raw['AT_wind'] - df_raw['LU_wind'] - \
                df_raw['DE_solar'] - df_raw['AT_solar'] - df_raw['LU_solar']
df_polyfit = pd.concat([residual_load, df_raw['eex_day_ahead_2014'],
                       df_raw['power_price_model']], axis=1)
df_polyfit.columns = ['res_load', 'price_real', 'price_model']

# fit polynom of 3rd degree
z = np.polyfit(df_polyfit['res_load'], df_polyfit['price_real'], 3)
p = np.poly1d(z)

# save and plot results
df_polyfit['price_regression'] = p(df_polyfit['res_load'])

line = df_polyfit[0:24*31][['price_real', 'price_regression',
    'price_model']].plot(linewidth=1.2, drawstyle='steps')

#scatter = df_polyfit.plot(kind='scatter', x='res_load', y='price_real')

plt.show()
