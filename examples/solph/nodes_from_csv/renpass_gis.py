# -*- coding: utf-8 -*-

import logging
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime

from oemof.tools import logger
from oemof.solph import OperationalModel, EnergySystem, GROUPINGS
from oemof.solph import NodesFromCSV
from oemof.outputlib import ResultsDataFrame

def stopwatch():
    if not hasattr(stopwatch, "now"):
        stopwatch.now = datetime.now()
        return None
    last = stopwatch.now
    stopwatch.now = datetime.now()
    return str(stopwatch.now-last)[0:-4]

logger.define_logging()

# %% configuration

date_from = '2014-01-01 00:00:00'
date_to = '2014-12-31 23:00:00'

datetime_index = pd.date_range(date_from, date_to, freq='60min')

# global plotting options
matplotlib.style.use('ggplot')
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['axes.facecolor'] = 'silver'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams.update({'font.size': 18})

# %% model creation and solving

es = EnergySystem(groupings=GROUPINGS, time_idx=datetime_index)

nodes = NodesFromCSV(file_nodes_flows='status_quo_2014_aggr.csv',
                     file_nodes_flows_sequences='status_quo_2014_aggr_seq.csv',
                     delimiter=',')

stopwatch()
om = OperationalModel(es)
print("OM creation time: " + stopwatch())

om.receive_duals()

om.solve(solver='gurobi', solve_kwargs={'tee': True})
print("Optimization time: " + stopwatch())

logging.info('Done!')

logging.info('Check the results')


# %% output: data

myresults = ResultsDataFrame(energy_system=es)

DE_inputs = myresults.slice_unstacked(bus_label="DE_bus_el", type="input",
                                      date_from=date_from, date_to=date_to,
                                      formatted=True)
DE_inputs.rename(columns={'DE_storage_phs': 'DE_storage_phs_out'},
                 inplace=True)

DE_outputs = myresults.slice_unstacked(bus_label="DE_bus_el", type="output",
                                       date_from=date_from, date_to=date_to,
                                       formatted=True)

DE_outputs.rename(columns={'DE_storage_phs': 'DE_storage_phs_in'},
                  inplace=True)

DE_other = myresults.slice_unstacked(bus_label="DE_bus_el", type="other",
                                     date_from=date_from, date_to=date_to,
                                     formatted=True)

DE_overall = pd.concat([DE_inputs, DE_outputs], axis=1)


# %% output: plotting of prices

power_price_model = DE_other['duals']
power_price_real = pd.read_csv('day_ahead_price_2014_eex.csv')
power_price_real.set_index(power_price_model.index, drop=True, inplace=True)
power_price = pd.concat([power_price_model, power_price_real], axis=1)
power_price.rename(columns={'price_avg_real': 'reality',
                            'duals': 'model'},
                   inplace=True)
power_price = power_price[['reality', 'model']]
power_price.to_csv('power_price_comparison_aggr_2014.csv')

nrow = 4
fig, axes = plt.subplots(nrows=nrow, ncols=1)
power_price.plot(drawstyle='steps-post', ax=axes[0],
                 title='Hourly price', sharex=True)
power_price.resample('1D').mean().plot(drawstyle='steps-post', ax=axes[1],
                                       title='Daily mean', sharex=True)
power_price.resample('1W').mean().plot(drawstyle='steps-post', ax=axes[2],
                                       title='Weekly mean', sharex=True)
power_price.resample('1M').mean().plot(drawstyle='steps-post', ax=axes[3],
                                       title='Montly mean (base)',
                                       sharex=True)
for i in range(0, nrow):
    axes[i].set_ylabel('EUR/MWh')

# %% output: plotting of production

fig, axes = plt.subplots(nrows=1, ncols=2)
fig.suptitle('Model validation for 2014', fontsize=30)

# data from ENSTO-E in GWh
# https://www.quandl.com/data/ENTSOE/DE_PROD-Electricity-Production-Germany
entsoe_data = pd.read_csv('data_DE_2014_ENTSO-E.csv')
entsoe_data.index = pd.date_range(entsoe_data['Date'].iloc[0], periods=12,
                                  freq='M')
entsoe_data = entsoe_data[['solar', 'wind', 'uranium',
                           'lignite', 'hard_coal', 'gas', 'oil', 'mixed_fuels',
                           'biomass', 'hydro', 'pump', 'consumption',
                           'import', 'export']]

entsoe_plot = entsoe_data.resample('1A').sum().plot(kind='bar', stacked=False,
                                                    ax=axes[0])
entsoe_plot.set_ylabel('Energy in GWh')
entsoe_plot.set_xlabel('Date and Time')
entsoe_plot.set_title('ENTSO-E Data')

# data from model in MWh
model_data = DE_overall[
     ['DE_solar', 'DE_wind', 'DE_pp_uranium', 'DE_pp_lignite',
      'DE_pp_hard_coal', 'DE_pp_gas', 'DE_pp_oil', 'DE_pp_mixed_fuels',
      'DE_pp_biomass', 'DE_run_of_river',
      'DE_storage_phs_out', 'DE_load']]
powerline_cols = [col for col in DE_overall.columns if 'powerline' in col]
model_data = pd.concat([model_data, DE_overall[powerline_cols]], axis=1)
model_data = model_data/1000

# resampling and plot
model_data = model_data.resample('1A').sum()
model_plot = model_data.plot(kind='bar', stacked=False, ax=axes[1])
model_plot.set_ylabel('Energy in GWh')
model_plot.set_xlabel('Date and Time')
model_plot.set_title('Model Results')
