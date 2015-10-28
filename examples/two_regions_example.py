#!/usr/bin/python3
# -*- coding: utf-8

import matplotlib.pyplot as plt
import logging
import pandas as pd
import numpy as np

logging.getLogger().setLevel(logging.DEBUG)
#logging.getLogger().setLevel(logging.INFO)
#logging.getLogger().setLevel(logging.WARNING)
from oemof.tools import config
from oemof.tools import db
from oemof_pg import tools
from oemof_pg import powerplants as db_pps
from oemof.core import energy_regions as reg
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
    demand_df['elec'] = np.random.rand(8760) * 10
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
            Bus(uid=uid, type=pp[1].type, price=60, sum_out_limit=10e10)
            bus_reg = region.code
        else:
            logging.debug('Local bus {0} exists. Nothing done.'.format(
                '_'.join(['b', region.code, pp[1].type])))
            bus_reg = region.code
    else:
        logging.debug('Global bus {0} exists. Nothing done.'.format(
            '_'.join(['b', 'glob', pp[1].type])))
        bus_reg = 'glob'
    return region, bus_reg


def create_solph_objects(region, pp, esystem, feedin):
    # Dispatch Sources
    print('Create:', pp[1].type)
    if pp[1].type in ['wind_power', 'solar_power']:
        # renewables get their data from time_series dataframe
        # Hier fände ich eine Typ noch gut (Wind, PV...)
        region.renew_pps.append(source.DispatchSource(
            uid='_'.join(['DispSrc', region.code, str(len(region.renew_pps))]),
            outputs=[region.busses['_'.join(['b', region.code, 'elec'])]],
            val=feedin[pp[1].type],
            out_max={'_'.join(['b', region.code, 'elec']): pp[1].cap}))

    elif pp[1].type in ['lignite', 'natural_gas', 'hard_coal']:
        print('FOSSIL', pp[1].type)
        [region, bus_reg] = create_bus(region, pp, esystem.global_busses)
        print(region.busses)
        print(bus_reg)
        if bus_reg == region.code:
            resource_bus = region.busses['_'.join(['b', bus_reg, pp[1].type])]
        elif bus_reg == 'glob':
            resource_bus = esystem.global_busses['_'.join(['b', bus_reg,
                                                           pp[1].type])]
        print(resource_bus)
        # Hier fände ich eine Typ noch gut (lignite, natural_gas,...)

        region.conv_pps.append(transformer.Simple(
            uid='_'.join(['TransSimp', region.code,
                          str(len(region.conv_pps))]),
            inputs=resource_bus,
            outputs=region.busses['_'.join(['b', region.code, 'elec'])],
            in_max={'_'.join(['b', region.code, pp[1].type]): None},
            out_max={'_'.join(['b', region.code, 'elec']): pp[1].cap},
            eta=[eta_elec[pp[1].type]]))
    else:
        logging.warning("Power plant type unknown")


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
    print('Region: {0} ({1})'.format(region.name, region.code))
    # Get feedin time series
    feedin = get_feedin()

    # Get demand time series and create busses. One bus for each demand series.
    demand = get_demand()
    for bustype in demand.keys():
        uid = '_'.join(['b', region.code, bustype])
    region.busses[uid] = Bus(uid=uid, type=bustype, price=60,
                             sum_out_limit=10e10)

    # Get power plants from database
    pps_df = (
        pd.concat([db_pps.get_bnetza_pps(conn, region.geom),
                   db_pps.get_energymap_pps(conn, region.geom)],
                  ignore_index=True))
    pps_df.loc[len(pps_df)] = 10 ** 6, np.nan, 'natural_gas'
#    pps_df = pps_df.apply(get_pp_data_from_type, axis=1)
    for pp in pps_df.iterrows():
        create_solph_objects(region, pp, TwoRegExample, feedin)

exit(0)
regions = [lk_wtb, std_dr]
busses = {}
demand = {}
feedin = {}
transformers = {}
transmission = {}



for region in regions:
    if overwrite:
        region.fetch_weather_raster(conn)
        region.fetch_ee_feedin(
            conn, store='hf5', dpath=config.get('oemof', 'OutPath'), **site)
        region.fetch_demand_series(conn)
        region.fetch_fossil_power_plants(conn)
        region.dump()
    else:
        try:
            region.restore()
        except:
            region.fetch_weather_raster(conn)
            region.fetch_ee_feedin(conn, **site)
            region.fetch_demand_series(conn)
            region.fetch_fossil_power_plants(conn)
            region.dump()

    remove_ls = ['wood_hs_0', 'gas_hs_0', 'oil_hs_0',
                 'thbm_lk_wtb_2013', 'st_pot']
    for key in region.demand.keys():
        if key in remove_ls:
            region.demand.drop([key], 1, inplace=True)
    region.feedin = region.feedin / 10 ** 9

#    region.demand['district_0'] = region.demand['district_0'] * 0
#    region.demand.plot()
#    region.feedin.plot()
#    plt.show()
    # region2solph
    # Create busses for all demand series
    # Connect demand series as sinks to its bus
    for key in region.demand.keys():
        if key == 'electrical':
            bus_type = 'el'
        else:
            bus_type = 'th'
        uid = '_'.join([region.code, key])

        busses[uid] = Bus(uid='_'.join(['bus', uid]), type=bus_type)
        demand[uid] = sink.Simple(uid='_'.join(['demand', uid]),
                                  inputs=[busses[uid]],
                                  val=region.demand[key])

    # Connect all feedin series to the electrical bus
    bus_type = 'electrical'
    for key in region.feedin.keys():
        uid = '_'.join([region.code, key])

        feedin[uid] = source.DispatchSource(
            uid=uid,
            outputs=[busses['_'.join([region.code, bus_type])]],
            val=region.feedin[key],
            out_max={busses['_'.join([region.code, bus_type])].uid: 1})

    # Create a bus for all resources needed
    # Global busses are created only once.
    for resource in region.power_plants['fossil'].type.unique():
        if de_en[resource] in resource_busses['local']:
            uid = '_'.join([region.code, de_en[resource]])
            busses[uid] = Bus(uid='_'.join(['bus', uid]), type=de_en[
                resource])
        elif de_en[resource] in resource_busses['global']:
            busses[de_en[resource]] = busses.get(de_en[resource], Bus(
                uid='_'.join(['bus', de_en[resource]]),
                type=de_en[resource]))

    # Connect all transformer to its resource bus.
    for pp in region.power_plants['fossil'].iterrows():
        # Check if the input bus is global or local
        if de_en[pp[1].type] in resource_busses['global']:
            in_bus = de_en[pp[1].type]
        elif de_en[pp[1].type] in resource_busses['lokal']:
            in_bus = '_'.join([region.code, de_en[pp[1].type]])
        else:
            logging.error(
                "Can't decide wether your resource is global or local.")
        bid = '_'.join([region.code, de_en[pp[1].type], str(pp[0])])
        transformers[bid] = transformer.Simple(
            uid='_'.join(['transf', bid]),
            inputs=[busses[in_bus]],
            outputs=[busses['_'.join([region.code, bus_type])]],
            in_max={'bus_' + in_bus: None},
            out_max={
                '_'.join(['bus', region.code, bus_type]): pp[1].p_kw_peak},
            eta=[eta_elec[de_en[pp[1].type]]],
            opex_var=opex_var[de_en[pp[1].type]],
            co2_var=co2_emissions[de_en[pp[1].type]])

    # Add one chp-power plant and its resource bus (if missing) by hand
    uid = '_'.join([region.code, 'natural_gas'])
    busses[uid] = busses.get(
        uid, Bus(uid='bus_' + uid, type="natural_gas"))

    transformers[uid + '_a0'] = transformer.CHP(
        uid='transf_' + uid,
        inputs=[busses[uid]],
        outputs=[busses[region.code + '_electrical'],
                 busses[region.code + '_district_0']],
        in_max={'bus_' + uid: 100000},
        out_max={'bus_' + region.code + '_electrical': 3000000,
                 'bus_' + region.code + '_district_0': None},
        eta=[0.4, 0.3],
        co2_var=co2_emissions['natural_gas'])

# transport
transmission['LanWit_StaDes_electrical'] = transport.Simple(
    uid='LanWit_StaDes_electrical',
    inputs=[busses['LanWit_electrical']],
    outputs=[busses['StaDes_electrical']],
    in_max={'bus_LanWit_electrical': 10000},
    out_max={'bus_StaDes_electrical': 9000},
    eta=[0.9])

transmission['StaDes_LanWit_electrical'] = transport.Simple(
    uid='StaDes_LanWit_electrical',
    inputs=[busses['StaDes_electrical']],
    outputs=[busses['LanWit_electrical']],
    in_max={'bus_StaDes_electrical': 10000},
    out_max={'bus_LanWit_electrical': 8000},
    eta=[0.8])

entities = []
components = []
for key in busses.keys():
    entities.append(busses[key])
for key in demand.keys():
    entities.append(demand[key])
for key in feedin.keys():
    entities.append(feedin[key])
    components.append(feedin[key])
for key in transformers.keys():
    entities.append(transformers[key])
    components.append(transformers[key])
for key in transmission.keys():
    entities.append(transmission[key])
    components.append(transmission[key])

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
