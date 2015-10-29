#!/usr/bin/python3
# -*- coding: utf-8

import matplotlib.pyplot as plt
import logging
import pandas as pd
import numpy as np

# logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.INFO)
# logging.getLogger().setLevel(logging.WARNING)
from oemof.tools import db
from oemof_pg import tools
from oemof_pg import powerplants as db_pps
from oemof.core import energy_system as es
from oemof.solph import postprocessing
from oemof.core.network.entities import Bus
from oemof.core.network.entities.components import sinks as sink
from oemof.core.network.entities.components import sources as source
from oemof.core.network.entities.components import transformers as transformer
from oemof.core.network.entities.components import transports as transport
from oemof.solph.optimization_model import OptimizationModel

import warnings
warnings.simplefilter(action="ignore", category=RuntimeWarning)

# Plant and site parameter
site = {'module_name': 'Yingli_YL210__2008__E__',
        'azimuth': 0,
        'tilt': 0,
        'albedo': 0.2,
        'hoy': 8760,
        'h_hub': 135,
        'd_rotor': 127,
        'wka_model': 'ENERCON E 126 7500',
        'h_hub_dc': {
            1: 135,
            2: 78,
            3: 98,
            4: 138,
            0: 135},
        'd_rotor_dc': {
            1: 127,
            2: 82,
            3: 82,
            4: 82,
            0: 127},
        'wka_model_dc': {
            1: 'ENERCON E 126 7500',
            2: 'ENERCON E 82 3000',
            3: 'ENERCON E 82 2300',
            4: 'ENERCON E 82 2300',
            0: 'ENERCON E 126 7500'},
        }


define_elec_buildings = [
    {'annual_elec_demand': 2000,
     'selp_type': 'h0'},
    {'annual_elec_demand': 2000,
     'selp_type': 'g0'},
    {'annual_elec_demand': 2000,
     'selp_type': 'i0'}]

define_heat_buildings = [
    {'building_class': 11,
     'wind_class': 0,
     'annual_heat_demand': 5000,
     'shlp_type': 'efh'},
    {'building_class': 5,
     'wind_class': 1,
     'annual_heat_demand': 5000,
     'shlp_type': 'mfh'},
    {'selp_type': 'g0',
     'building_class': 0,
     'wind_class': 1,
     'annual_heat_demand': 3000,
     'shlp_type': 'ghd'}]

# emission factors in t/MWh
co2_emissions = {}
co2_emissions['lignite'] = 0.111 * 3.6
co2_emissions['hard_coal'] = 0.0917 * 3.6
co2_emissions['natural_gas'] = 0.0556 * 3.6
co2_emissions['oil'] = 0.0750 * 3.6

eta_elec = {}
eta_elec['lignite'] = 0.35
eta_elec['hard_coal'] = 0.39
eta_elec['natural_gas'] = 0.45
eta_elec['oil'] = 0.40

opex_var = {}
opex_var['lignite'] = 22
opex_var['hard_coal'] = 25
opex_var['natural_gas'] = 22
opex_var['oil'] = 22
opex_var['solar_power'] = 1
opex_var['wind_power'] = 1

capex = {}
capex['lignite'] = 22
capex['hard_coal'] = 25
capex['natural_gas'] = 22
capex['oil'] = 22
capex['solar_power'] = 1
capex['wind_power'] = 1

de_en = {
    'Braunkohle': 'lignite',
    'Steinkohle': 'hard_coal',
    'Erdgas': 'natural_gas',
    'Öl': 'oil',
    'Solarstrom': 'solar_power',
    'Windkraft': 'wind_power',
    'Biomasse': 'biomass',
    'Wasserkraft': 'hydro_power',
    'Gas': 'methan'}

en_de = {
    'lignite': 'Braunkohle',
    'hard_coal': 'Steinkohle',
    'natural_gas': 'Erdgas',
    'oil': 'Öl'}

opex_fix = {}

resource_busses = {
    'global': ['hard_coal', 'lignite', 'oil'],
    'local': ['natural_gas']}


translator = lambda x: de_en[x]


def get_pp_data_from_type(row):
    row['eta'] = eta_elec.get(row['type'], np.nan)
    row['capex'] = capex.get(row['type'], 0)
    row['opex_fix'] = opex_fix.get(row['type'], 0)
    row['opex_var'] = opex_var.get(row['type'], 0)
    row['co2_var'] = co2_emissions.get(row['type'], 0)
    row['uid'] = row['type']
    return row


def get_feedin():
    'Dummy function until real function exists.'
    feedin_df = pd.DataFrame()
    feedin_df['wind_power'] = np.random.rand(8760) / 2.3 * 1000
    feedin_df['solar_power'] = np.random.rand(8760) / 4.5 * 1000
    return feedin_df


def get_demand():
    'Dummy function until real function exists.'
    demand_df = pd.DataFrame()
    demand_df['el'] = np.random.rand(8760) * 10
    return demand_df


def create_bus(region, pp, global_busses):
    r'''
    Maybe it is more stable to ask for the type of the bus object instead of
    checking the uid.
    '''
    if '_'.join(['b', 'glob', pp[1].type]) not in global_busses:
        uid = '_'.join(['b', region.code, pp[1].type])
        if uid not in region.busses:
            logging.debug('Creating bus {0}.'.format(uid))
            region.busses[uid] = (
                Bus(uid=uid, type=pp[1].type, price=60, sum_out_limit=10e10))
            bus_reg = region.code
        else:
            logging.debug('Local bus {0} exists. Nothing done.'.format(
                '_'.join(['b', region.code, pp[1].type])))
            bus_reg = region.code
    else:
        logging.debug('Global bus {0} exists. Nothing done.'.format(
            '_'.join(['b', 'glob', pp[1].type])))
        bus_reg = 'glob'
    return bus_reg


def create_solph_objects(region, pp, esystem, feedin):
    # Dispatch Sources
    if pp[1].type in ['wind_power', 'solar_power']:
        # renewables get their data from time_series dataframe
        # Hier fände ich eine Typ noch gut (Wind, PV...)
        logging.debug('Create dispatch source {0} for {1}.'.format(
            '_'.join(['DispSrc', region.code, str(len(region.renew_pps))]),
            pp[1].type))
        region.renew_pps.append(source.DispatchSource(
            uid='_'.join(['DispSrc', region.code, str(len(region.renew_pps))]),
            outputs=[region.busses['_'.join(['b', region.code, 'el'])]],
            val=feedin[pp[1].type],
            out_max={'_'.join(['b', region.code, 'el']): float(pp[1].cap)}))

    elif pp[1].type in ['lignite', 'natural_gas', 'hard_coal']:
        logging.debug('Create SimpleTransformer for ' + pp[1].type)
        bus_reg = create_bus(region, pp, esystem.global_busses)
        if bus_reg == region.code:
            resource_bus = region.busses['_'.join(['b', bus_reg, pp[1].type])]
        elif bus_reg == 'glob':
            resource_bus = esystem.global_busses['_'.join(['b', bus_reg,
                                                           pp[1].type])]

        # Hier fände ich eine Typ noch gut (lignite, natural_gas,...)
        logging.debug('Create transformer {0} for {1}.'.format(
            '_'.join(['TransSimp', region.code, str(len(region.conv_pps))]),
            pp[1].type))
        region.conv_pps.append(transformer.Simple(
            uid='_'.join(['TransSimp', region.code,
                          str(len(region.conv_pps))]),
            inputs=[resource_bus],
            outputs=[region.busses['_'.join(['b', region.code, 'el'])]],
            in_max={'_'.join(['b', bus_reg, pp[1].type]): None},
            out_max={'_'.join(['b', region.code, 'el']): float(pp[1].cap)},
            eta=[eta_elec[pp[1].type]]))
    else:
        logging.warning(
            "Power plant type {0} is not connected to solph type.".format(
                pp[1].type))


year = 2010
overwrite = False
overwrite = True
conn = db.connection()

# Create an energy system
TwoRegExample = es.EnergySystem()

# Add regions to the energy system
TwoRegExample.add_region(es.EnergyRegion(
    year=year, geom=tools.get_polygon_from_nuts(conn, 'DEE0E'),
    name='Landkreis Wittenberg'))

TwoRegExample.add_region(es.EnergyRegion(
    year=year, geom=tools.get_polygon_from_nuts(conn, 'DEE01'),
    name='Stadt Dessau-Roßlau'))

# Create global busses
uid = "b_glob_hard_coal"
TwoRegExample.global_busses[uid] = Bus(uid=uid, type="coal", price=60,
                                       sum_out_limit=10e10)
uid = "b_glob_lignite"
TwoRegExample.global_busses[uid] = Bus(uid=uid, type="coal", price=60,
                                       sum_out_limit=10e10)

# Create entity objects for each region
for region in TwoRegExample.regions.values():
    logging.info('Processing region: {0} ({1})'.format(
        region.name, region.code))
    # Get feedin time series
    feedin = get_feedin()

    # Get demand time series and create busses. One bus for each demand series.
    demand = get_demand()
    for demandtype in demand.keys():
        uid = '_'.join([region.code, demandtype])
        region.busses['b_' + uid] = Bus(uid='b_' + uid, type=demandtype,
                                        price=60, sum_out_limit=10e10)
        region.sinks.append(sink.Simple(uid='Sink_' + uid,
                                        inputs=[region.busses['b_' + uid]],
                                        val=demand[demandtype]))

    # Get power plants from database
    pps_df = (
        pd.concat([db_pps.get_bnetza_pps(conn, region.geom),
                   db_pps.get_energymap_pps(conn, region.geom)],
                  ignore_index=True))
    pps_df.loc[len(pps_df)] = 10 ** 6, np.nan, 'natural_gas'
#    pps_df = pps_df.apply(get_pp_data_from_type, axis=1)
    for pp in pps_df.iterrows():
        create_solph_objects(region, pp, TwoRegExample, feedin)

# Connect the electrical bus of region StaDes und LanWit.
TwoRegExample.connect('StaDes', 'LanWit', 'el', in_max=10000, out_max=9000,
                      eta=0.9, classtype='simple')

# ****************************************************************************
# At this point the TwoRegExample of the class EnergySystem is defined.
# Still missing a simulation object that contains all the hard coded
# informations below (solver, excess=True,...).
# ****************************************************************************


# ****************************************************************************
# The next step is to create a list of all entities and create an Optimization
# Model. This could be part of the solph package.
# ****************************************************************************

entities = []
components = []

for bus in TwoRegExample.global_busses.values():
    entities.append(bus)

for connection in TwoRegExample.connections.values():
    entities.append(connection)
    components.append(connection)

for region in TwoRegExample.regions.values():
    for bus in region.busses.values():
        entities.append(bus)
    for pp in region.conv_pps:
        entities.append(pp)
        components.append(pp)
    for pp in region.renew_pps:
        entities.append(pp)
        components.append(pp)

timesteps = [t for t in range(8760)]

om = OptimizationModel(entities=entities, timesteps=timesteps,
                       options={'invest': False, 'slack': {
                           'excess': True, 'shortage': True}})

om.solve(solver='gurobi', debug=True, tee=False, duals=True)

postprocessing.results_to_objects(om)

df = pd.DataFrame()
for c in components:
    for k in c.results["out"].keys():
        df[c.uid] = c.results["out"][k]

#for t in transmissions:
#    for k in t.results["out"].keys():
#        df[t.uid] = t.results["out"][k]
#for c in components:
#    for k in c.results["in"].keys():
#        df[c.uid] = c.results["in"][k]
#
#for c in components:
#    c.calc_emissions()
#    df[c.uid] = c.emissions

print(df.keys())

df.plot()
plt.show()


def plot_dispatch(bus_to_plot):
        # plotting: later as multiple pdf with pie-charts and topology?
        import numpy as np
        import matplotlib as mpl
        import matplotlib.cm as cm

        plot_data = components

        # data preparation
        x = np.arange(len(timesteps))
        y = []
        labels = []
        for c in plot_data:
            if bus_to_plot in c.results['out']:
                y.append(c.results['out'][bus_to_plot])
                labels.append(c.uid)


        # plotting
        fig, ax = plt.subplots()
        sp = ax.stackplot(x, y,
                          colors=cm.rainbow(np.linspace(0, 1, len(plot_data))))
        proxy = [mpl.patches.Rectangle((0, 0), 0, 0,
                                       facecolor=
                                       pol.get_facecolor()[0]) for pol in sp]
        ax.legend(proxy, labels)
        ax.grid()
        ax.set_xlabel('Timesteps in h')
        ax.set_ylabel('Power in MW')
        ax.set_title('Dispatch')

plot_dispatch('bus_LanWit_electrical')
plt.show()
# write results to data frame for excel export

#    print(region.power_plants['re'].type.unique())
#    print(region.power_plants['re'].subtype.unique())
#    print(region.power_plants['fossil'].type.unique())
#    print(region.power_plants['fossil'].subtype.unique())
#    print(region.feedin.keys())
#print(feedin)
#print('busse', busses.keys())
#print('transformer', transformers.keys())
#print('')
#print(demand.keys())
