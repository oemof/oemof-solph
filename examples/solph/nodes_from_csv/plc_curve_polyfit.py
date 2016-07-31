# -*- coding: utf-8 -*-

import scipy
import scipy.stats
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from scipy.signal import argrelextrema


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
        'scenario_nep_2014_2016-07-29 12:10:39.331957_DE.csv')

df_raw = pd.read_csv(file, parse_dates=[0], index_col=0, keep_date_col=True)
df_raw.head()
df_raw.columns


# %% polynom fitting

# prepare dataframe for fit
residual_load = df_raw['DE_load'] + df_raw['AT_load'] + df_raw['LU_load'] - \
                df_raw['DE_wind'] - df_raw['AT_wind'] - df_raw['LU_wind'] - \
                df_raw['DE_solar'] - df_raw['AT_solar'] - df_raw['LU_solar']

price_real = pd.read_csv('price_eex_day_ahead_2014.csv')
price_real.index = df_raw.index

df = pd.concat([residual_load, price_real, df_raw['duals']], axis=1)
df.columns = ['res_load', 'price_real', 'price_model']

# fit polynom of 3rd degree
z = np.polyfit(df['res_load'], df['price_real'], 3)
p = np.poly1d(z)

# save and plot results
df['price_polynom'] = p(df['res_load'])

df['residuals'] = df['price_real'] - \
                  df['price_model']

# %% detect local minima and maxima

df_peaks = df[['price_real', 'price_model']]['2014-01 01':'2014-02 01']

# detection
order = 5


# np.greater_equal für tableaus
real_maxima = argrelextrema(df_peaks['price_real'].values, np.greater,
                            order=order)
real_maxima = [i for i in real_maxima[0]]

real_minima = argrelextrema(df_peaks['price_real'].values, np.less_equal,
                            order=order)
real_minima = [i for i in real_minima[0]]

model_maxima = argrelextrema(df_peaks['price_model'].values, np.greater,
                             order=order)
model_maxima = [i for i in model_maxima[0]]

model_minima = argrelextrema(df_peaks['price_model'].values, np.less_equal,
                             order=order)
model_minima = [i for i in model_minima[0]]

# get residuals for maxima
max_residuals = pd.DataFrame()
max_residuals['residuals'] = df_peaks.iloc[model_maxima]['price_real'] - \
    df_peaks.iloc[model_maxima]['price_model']

param_max = scipy.stats.norm.fit(max_residuals)
numbers_max = scipy.stats.norm.rvs(size=len(max_residuals),
                                   loc=param_max[0],
                                   scale=param_max[1])


# get residuals for minima
min_residuals = pd.DataFrame()
min_residuals['residuals'] = df_peaks.iloc[model_minima]['price_real'] - \
    df_peaks.iloc[model_minima]['price_model']
param_min = scipy.stats.norm.fit(min_residuals)
numbers_min = scipy.stats.norm.rvs(size=len(min_residuals),
                                   loc=param_min[0],
                                   scale=param_min[1])

# scale prices
df_peaks['price_scaled'] = df_peaks['price_model']
df_peaks.ix[model_maxima, 'price_scaled'] *= 1.2
df_peaks.ix[model_minima, 'price_scaled'] *= 0.8

# plotting
fig, axes = plt.subplots(nrows=3, sharey=True, sharex=True)

df_peaks[['price_real']].plot(drawstyle='steps', color='r', ax=axes[0],
                              title='Detected Maxima')
df_peaks[['price_model']].plot(drawstyle='steps',
                               markevery=[i for i in model_maxima],
                               marker='o',
                               color='b',
                               ax=axes[0])

df_peaks[['price_real']].plot(drawstyle='steps', color='r', ax=axes[1],
                              title='Detected Minima')
df_peaks[['price_model']].plot(drawstyle='steps',
                               markevery=[i for i in model_minima],
                               marker='o',
                               color='b',
                               ax=axes[1])

df_peaks[['price_real']].plot(drawstyle='steps', color='r', ax=axes[2],
                              title='Manipulated Data')
#df_peaks[['price_model']].plot(drawstyle='steps', color='b', ax=axes[2])
df_peaks[['price_scaled']].plot(drawstyle='steps',
                                    color='k', ax=axes[2])

plt.show()

# %% find tableaus using an own approach

# data
df_peaks = df[['price_real', 'price_model']]['2014-02 01':'2014-02 14']

positions = np.where(
    (df_peaks['price_model'] == df_peaks['price_model'].shift(1)))

# plotting
fig, axes = plt.subplots(nrows=2, sharey=True, sharex=True)
fig.suptitle('Maxima', fontsize=16)

df_peaks[['price_real']].plot(drawstyle='steps',
                              color='r',
                              ax=axes[0])

df_peaks[['price_model']].plot(drawstyle='steps',
                               markevery=[i for i in positions],
                               marker='s',
                               color='b',
                               ax=axes[0])

plt.show()

# %% create distribution-fitted volatility

# Sample
data = df['residuals']

# Distributions to check
dist_names = ['gausshyper', 'norm', 'gamma', 'hypsecant']

for dist_name in dist_names:

    # Fit distribution to the data
    dist = getattr(scipy.stats, dist_name)
    param = dist.fit(data)

    # Plot the histogram
    plt.hist(data, bins=100, normed=True, alpha=0.8, color='g')

    # Plot and save the PDF in a PDF file
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = dist.pdf(x, *param[:-2], loc=param[-2], scale=param[-1])
    plt.plot(x, p, 'k', linewidth=2)
    title = 'Distribution: ' + dist_name + \
            ' / Fit results: mu = %.2f,  std = %.2f' % (param[0], param[1])
    plt.title(title)
    plt.savefig('results/fit_' + dist_name + '.pdf')
    plt.close()

    print(dist_name, ': ', ' mu: ', param[0], ' std: ', param[1])


# %% QQ Plots and random numbers

# Sample
data = df['residuals']

# Distributions to check
dist_names = ['norm', 'hypsecant']

for dist_name in dist_names:

    # Fit distribution to the data
    dist = getattr(scipy.stats, dist_name)
    param = dist.fit(data)

    scipy.stats.probplot(data, dist=dist_name, plot=plt)
    plt.title('Probability Plot (' + dist_name + ')')
    plt.savefig('results/qq_' + dist_name + '.pdf')
    plt.close()


# %% mean and standard deviation of the fitted distribution

df['random_hyper'] = scipy.stats.hypsecant.rvs(size=8760, loc=1.86383591071,
                                               scale=5.41544622678)

df['random_norm'] = scipy.stats.norm.rvs(size=8760, loc=1.78602,
                                         scale=11.18743)

df['price_model_volatility_norm'] = df['price_model'] + \
                                    df['random_norm']

df['price_model_volatility_hyper'] = df['price_model'] + \
                                     df['random_hyper']
# plot
df[['price_real', 'price_model',
    'price_model_volatility_norm',
    'price_model_volatility_hyper']]['2014-01':'2014-03'].plot(kind='line',
                                                         subplots=True,
                                                         sharex=True,
                                                         sharey=True,
                                                         drawstyle='steps')

plt.show()

# %% real vs. model

df[['price_real', 'price_model']]['2014-01':'2014-01'].plot(kind='line',
                                                         subplots=False,
                                                         sharex=True,
                                                         sharey=True,
                                                         drawstyle='steps',
                                                         linewidth=1.6)

plt.show()


# %% spread analysis

# data
df_spread = pd.DataFrame()

df_spread['price_real'] = df['price_real']

df_spread['spread_3h'] = df['price_real'].resample('3h').max() - \
    df['price_real'].resample('3h').min()

df_spread['spread_6h'] = df['price_real'].resample('6h').max() - \
    df['price_real'].resample('6h').min()

df_spread['spread_12h'] = df['price_real'].resample('12h').max() - \
    df['price_real'].resample('12h').min()

df_spread['spread_24h'] = df['price_real'].resample('24h').max() - \
    df['price_real'].resample('24h').min()

df_spread['spread_48h'] = df['price_real'].resample('48h').max() - \
    df['price_real'].resample('48h').min()

df_spread['spread_96h'] = df['price_real'].resample('96h').max() - \
    df['price_real'].resample('96h').min()

df_spread['spread_192h'] = df['price_real'].resample('192h').max() - \
    df['price_real'].resample('192h').min()

fig, axes = plt.subplots(nrows=7, sharey=True)
fig.suptitle('Spread nach Zeitintervall', fontsize=16)

df_spread[['spread_3h']].dropna().plot(kind='line', drawstyle='steps',
                                       ax=axes[0])
df_spread[['spread_6h']].dropna().plot(kind='line', drawstyle='steps',
                                       ax=axes[1])
df_spread[['spread_12h']].dropna().plot(kind='line', drawstyle='steps',
                                        ax=axes[2])
df_spread[['spread_24h']].dropna().plot(kind='line', drawstyle='steps',
                                        ax=axes[3])
df_spread[['spread_48h']].dropna().plot(kind='line', drawstyle='steps',
                                        ax=axes[4])
df_spread[['spread_96h']].dropna().plot(kind='line', drawstyle='steps',
                                        ax=axes[5])
df_spread[['spread_192h']].dropna().plot(kind='line', drawstyle='steps',
                                         ax=axes[6])

plt.show()

