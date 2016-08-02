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

#%% plot fundamental and polynomial prices

df_raw[['price_volatility', 'duals']].plot()
plt.show()

df_raw[['price_volatility', 'duals']][0:24 * 7 * 8].plot()
plt.show()

df_raw[['price_volatility', 'duals']].describe()


# %% polynom fitting: residual load

#
## get imports and exports
#cc = 'DE'
#powerline_cols = [col for col in df_raw.columns
#                  if 'powerline' in col]
#powerlines = df_raw[powerline_cols]
#
#exports = powerlines[
#    [col for col in powerlines.columns
#     if cc + '_' in col]].sum(axis=1)
#df_raw['exports'] = exports
#
#imports = powerlines[
#    [col for col in powerlines.columns
#     if '_' + cc + '_' in col]].sum(axis=1)
#df_raw['imports'] = imports
#
## prepare dataframe for fit
#residual_load = df_raw['DE_load'] + df_raw['AT_load'] + df_raw['LU_load'] - \
#                df_raw['DE_wind'] - df_raw['AT_wind'] - df_raw['LU_wind'] - \
#                df_raw['DE_solar'] - df_raw['AT_solar'] - df_raw['LU_solar']
#
## real prices
#price_real = pd.read_csv('price_eex_day_ahead_2014.csv')
#price_real.index = df_raw.index
#
#df = pd.concat([residual_load, price_real, df_raw['duals']], axis=1)
#df.columns = ['res_load', 'price_real', 'price_model']
#
## fit polynom of 3rd degree to price_real(res_load)
#z = np.polyfit(df['res_load'], df['price_real'], 3)
#p = np.poly1d(z)
#df['price_polynom_res_load'] = p(df['res_load'])
#
## fit polynom of 3rd degree to price_residuals(price_model)
#df['price_residuals'] = df['price_real'] - df['price_model']
#z = np.polyfit(df['price_model'], df['price_residuals'], 3)
#p = np.poly1d(z)
#df['price_polynom_residuals'] = p(df['price_model'])
#
## fit polynom of 3rd degree to price_residuals(res_load)
#z = np.polyfit(df['res_load'], df['price_residuals'], 3)
#p = np.poly1d(z)
#df['price_model_residuals_res_load'] = df['price_model'] + p(df['res_load'])
#
## residuals of real-model
#df['price_residuals'].plot.hist(bins=50, title='price_real - price_model')
#df.plot.scatter(x='price_model', y='price_real')
#df.plot.scatter(x='res_load', y='price_real')
#df.plot.scatter(x='res_load', y='price_residuals')
#plt.plot(df['res_load'],
#         (
#          z[0] * df['res_load'] ** 3 +
#          z[1] * df['res_load'] ** 2 +
#          z[2] * df['res_load'] ** 1 +
#          z[3]
#          ), color='red')
#plt.show()
#
## show correlations
#print(
#    df[['price_real', 'price_model', 'price_polynom_res_load',
#        'price_model_residuals_res_load', 'price_polynom_residuals']].corr()
#)
#
## means
#print(
#    df[['price_real', 'price_model', 'price_polynom_res_load',
#        'price_model_residuals_res_load', 'price_polynom_residuals']].mean()
#)
#
## save and plot results
#df[['price_real', 'price_model', 'price_polynom_res_load',
#    'price_model_residuals_res_load']]\
#    ['2014-01 01':'2014-12 01'].plot(subplots=True, drawstyle='steps',
#                                     sharey=True)
#plt.show()


## %% detect local minima and maxima
#
#df_peaks = df[['price_real', 'price_model']]['2014-01 01':'2014-02 01']
#
#order_max = 2
#order_min = 2
#
## detection
## np.greater_equal für tableaus
#real_maxima = argrelextrema(df_peaks['price_real'].values, np.greater,
#                            order=order_max)
#real_maxima = [i for i in real_maxima[0]]
#
#real_minima = argrelextrema(df_peaks['price_real'].values, np.less,
#                            order=order_min)
#real_minima = [i for i in real_minima[0]]
#
#model_maxima = argrelextrema(df_peaks['price_model'].values, np.greater,
#                             order=order_max)
#model_maxima = [i for i in model_maxima[0]]
#
#model_minima = argrelextrema(df_peaks['price_model'].values, np.less,
#                             order=order_min)
#model_minima = [i for i in model_minima[0]]
#
## get residuals for maxima
#max_residuals = pd.DataFrame()
#max_residuals['residuals'] = df_peaks.iloc[model_maxima]['price_real'] - \
#    df_peaks.iloc[model_maxima]['price_model']
#
#param_max = scipy.stats.norm.fit(max_residuals)
#numbers_max = scipy.stats.norm.rvs(size=len(max_residuals),
#                                   loc=param_max[0],
#                                   scale=param_max[1])
#
#
## get residuals for minima
#min_residuals = pd.DataFrame()
#min_residuals['residuals'] = df_peaks.iloc[model_minima]['price_real'] - \
#    df_peaks.iloc[model_minima]['price_model']
#param_min = scipy.stats.norm.fit(min_residuals)
#numbers_min = scipy.stats.norm.rvs(size=len(min_residuals),
#                                   loc=param_min[0],
#                                   scale=param_min[1])
#
## scale prices
#df_peaks['price_scaled'] = df_peaks['price_model']
#df_peaks.ix[model_maxima, 'price_scaled'] += 20
#df_peaks.ix[model_minima, 'price_scaled'] -= 20
#
## plotting
#fig, axes = plt.subplots(nrows=2, sharey=True, sharex=True)
#
#df_peaks[['price_real']].plot(drawstyle='steps', color='r', ax=axes[0],
#                              title='Detected Maxima')
#df_peaks[['price_model']].plot(drawstyle='steps',
#                               markevery=[i for i in model_maxima],
#                               marker='o',
#                               color='b',
#                               ax=axes[0])
#
#df_peaks[['price_real']].plot(drawstyle='steps', color='r', ax=axes[1],
#                              title='Detected Minima')
#df_peaks[['price_model']].plot(drawstyle='steps',
#                               markevery=[i for i in model_minima],
#                               marker='o',
#                               color='b',
#                               ax=axes[1])
#plt.show()

## %% find tableaus using an own approach
#
## data
#df_peaks = df[['price_real', 'price_model']]['2014-02 01':'2014-02 14']
#
#positions = np.where(
#    (df_peaks['price_model'] == df_peaks['price_model'].shift(1)))
#
## plotting
#fig, axes = plt.subplots(nrows=2, sharey=True, sharex=True)
#fig.suptitle('Detected Tableaus', fontsize=16)
#
#df_peaks[['price_real']].plot(drawstyle='steps',
#                              color='r',
#                              ax=axes[0])
#
#df_peaks[['price_model']].plot(drawstyle='steps',
#                               markevery=[i for i in positions],
#                               marker='s',
#                               color='b',
#                               ax=axes[1])
#
#plt.show()

## %% create distribution-fitted volatility
#
## Sample
#data = df['price_residuals']
#
## Distributions to check
#dist_names = ['gausshyper', 'norm', 'gamma', 'hypsecant']
#
#for dist_name in dist_names:
#
#    # Fit distribution to the data
#    dist = getattr(scipy.stats, dist_name)
#    param = dist.fit(data)
#
#    # Plot the histogram
#    plt.hist(data, bins=100, normed=True, alpha=0.8, color='g')
#
#    # Plot and save the PDF in a PDF file
#    xmin, xmax = plt.xlim()
#    x = np.linspace(xmin, xmax, 100)
#    p = dist.pdf(x, *param[:-2], loc=param[-2], scale=param[-1])
#    plt.plot(x, p, 'k', linewidth=2)
#    title = 'Distribution: ' + dist_name + \
#            ' / Fit results: mu = %.2f,  std = %.2f' % (param[0], param[1])
#    plt.title(title)
#    plt.savefig('results/fit_' + dist_name + '.pdf')
#    plt.close()
#
#    print(dist_name, ': ', ' mu: ', param[0], ' std: ', param[1])


## %% QQ Plots and random numbers
#
## Sample
#data = df['price_residuals']
#
## Distributions to check
#dist_names = ['norm', 'hypsecant']
#
#for dist_name in dist_names:
#
#    # Fit distribution to the data
#    dist = getattr(scipy.stats, dist_name)
#    param = dist.fit(data)
#
#    scipy.stats.probplot(data, dist=dist_name, plot=plt)
#    plt.title('Probability Plot (' + dist_name + ')')
#    plt.savefig('results/qq_' + dist_name + '.pdf')
#    plt.close()
#
#
## %% mean and standard deviation of the fitted distribution
#
#df['random_hyper'] = scipy.stats.hypsecant.rvs(size=8760, loc=1.86383591071,
#                                               scale=5.41544622678)
#
#df['random_norm'] = scipy.stats.norm.rvs(size=8760, loc=1.78602,
#                                         scale=11.18743)
#
#df['price_model_volatility_norm'] = df['price_model'] + \
#                                    df['random_norm']
#
#df['price_model_volatility_hyper'] = df['price_model'] + \
#                                     df['random_hyper']
## plot
#df[['price_real', 'price_model',
#    'price_model_volatility_norm',
#    'price_model_volatility_hyper']]['2014-01':'2014-03'].plot(kind='line',
#                                                         subplots=True,
#                                                         sharex=True,
#                                                         sharey=True,
#                                                         drawstyle='steps')
#
#plt.show()

## %% spread analysis
#
## data
#df_spread = pd.DataFrame()
#
#df_spread['price_real'] = df['price_real']
#
#df_spread['spread_3h'] = df['price_real'].resample('3h').max() - \
#    df['price_real'].resample('3h').min()
#
#df_spread['spread_6h'] = df['price_real'].resample('6h').max() - \
#    df['price_real'].resample('6h').min()
#
#df_spread['spread_12h'] = df['price_real'].resample('12h').max() - \
#    df['price_real'].resample('12h').min()
#
#df_spread['spread_24h'] = df['price_real'].resample('24h').max() - \
#    df['price_real'].resample('24h').min()
#
#df_spread['spread_48h'] = df['price_real'].resample('48h').max() - \
#    df['price_real'].resample('48h').min()
#
#df_spread['spread_96h'] = df['price_real'].resample('96h').max() - \
#    df['price_real'].resample('96h').min()
#
#df_spread['spread_192h'] = df['price_real'].resample('192h').max() - \
#    df['price_real'].resample('192h').min()
#
#fig, axes = plt.subplots(nrows=7, sharey=True)
#fig.suptitle('Spread nach Zeitintervall', fontsize=16)
#
#df_spread[['spread_3h']].dropna().plot(kind='line', drawstyle='steps',
#                                       ax=axes[0])
#df_spread[['spread_6h']].dropna().plot(kind='line', drawstyle='steps',
#                                       ax=axes[1])
#df_spread[['spread_12h']].dropna().plot(kind='line', drawstyle='steps',
#                                        ax=axes[2])
#df_spread[['spread_24h']].dropna().plot(kind='line', drawstyle='steps',
#                                        ax=axes[3])
#df_spread[['spread_48h']].dropna().plot(kind='line', drawstyle='steps',
#                                        ax=axes[4])
#df_spread[['spread_96h']].dropna().plot(kind='line', drawstyle='steps',
#                                        ax=axes[5])
#df_spread[['spread_192h']].dropna().plot(kind='line', drawstyle='steps',
#                                         ax=axes[6])
#
#plt.show()
#
