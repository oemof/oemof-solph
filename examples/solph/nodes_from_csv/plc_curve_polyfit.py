# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from numpy import arange
from arch import arch_model

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
file = ('results/'
        'results_dispatch_prices_DE_2016-07-21 17:10:21.901285nep_2014_aggr'
        '.csv')

df_raw = pd.read_csv(file)
df_raw.head()
df_raw.columns

## %% create price volatility
#
#df_raw = df_raw[['eex_day_ahead_2014', 'power_price_model']]
#
#
#def price_volatility(price, factor):
#
#    price **= factor
#
#    if price >= 100.:
#        print('real: ', price)
#        price = 100
#        print('scaled: ', price)
#
#    return price
#
#df_raw['price_scaled'] = df_raw['power_price_model'].apply(price_volatility,
#                                                           args=[1.275])
#
## adjust scaled prices by mean value difference
#diff = df_raw['price_scaled'].mean() - df_raw['power_price_model'].mean()
#df_raw['price_scaled'] -= diff
#
#df_raw[:].plot(subplots=True, sharey=True)
#
#plt.show()


# %% polynom fitting

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
df_polyfit['price_polynom'] = p(df_polyfit['res_load'])

df_polyfit['residuals'] = df_polyfit['price_real'] - \
                          df_polyfit['price_model']

# %% plotting

#df_polyfit.plot(kind='scatter', x='res_load', y='price_real')

#df_polyfit.plot(kind='scatter',
#                x='price_real', y='price_model')

#df_polyfit[:][['price_real', 'price_model']].plot(linewidth=1.2, subplots=True,
#                                                  drawstyle='steps',
#                                                  color=['grey', 'r', 'b'],
#                                                  ylim=[-100, 100])

#residuals = pd.DataFrame()
#residuals = pd.concat([df_polyfit['residuals'][0:2190],
#                       df_polyfit['residuals'][2190:4380],
#                       df_polyfit['residuals'][4380:6570],
#                       df_polyfit['residuals'][6570:8760]], axis=1)
#residuals.plot.hist(bins=100, subplots=True, legend=None)
#residuals.columns=['Q1', 'Q2', 'Q3', 'Q4']
#
#residuals.std()

# create normal distributed random time series
# with mean and standard deviation of sample
mu, sigma = 0, df_polyfit['residuals'].std()

distribution = np.random.normal(mu, sigma, 8760)

df_polyfit['random_norm'] = pd.DataFrame(distribution)

df_polyfit['random_norm'].plot.hist(bins=100, title='Price Deviation')

plt.show()

df_polyfit['price_model_volatility'] = df_polyfit['price_model'] + \
                           df_polyfit['random_norm']

df_polyfit[0:24 * 31][['price_real', 'price_model',
                       'price_model_volatility']].plot(linewidth=1.2,
                                                       subplots=True,
                                                       drawstyle='steps',
                                                       ylim=[-100, 100])

plt.show()