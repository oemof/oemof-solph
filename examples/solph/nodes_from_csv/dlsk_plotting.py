# -*- coding: utf-8 -*-

import scipy
import scipy.stats
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


# global plotting options
plt.rcParams.update(plt.rcParamsDefault)
matplotlib.style.use('ggplot')
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['axes.facecolor'] = 'silver'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams.update({'font.size': 10})
plt.rcParams['image.cmap'] = 'Spectral'

# read file
file = ('results/'
        'scenario_nep_2035_2016-08-02 15:10:24.050450_DE.csv')

df_raw = pd.read_csv(file, parse_dates=[0], index_col=0, keep_date_col=True)
df_raw.head()
df_raw.columns

# %% plot fundamental and polynomial prices

df = df_raw[['price_volatility', 'duals']]

df.plot()
plt.show()

df[0:24 * 7 * 8].plot()
plt.show()

df[['price_volatility', 'duals']].describe()


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
plt.show()
