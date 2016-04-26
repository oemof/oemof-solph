#!/usr/bin/python3
# -*- coding: utf-8

import logging
import pandas as pd
import numpy as np

from oemof import db
from oemof.db import tools
from oemof.db import powerplants as db_pps
from oemof.db import feedin_pg
from oemof.tools import logger
from oemof.core import energy_system as es
from oemof.solph import predefined_objectives as predefined_objectives
from oemof.core.network.entities import Bus
from oemof.core.network.entities.components import sources as source
from oemof.core.network.entities.components import sinks as sink
from oemof.core.network.entities.components import transformers as transformer
from oemof.core.network.entities.components import transports as transport
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

# price for resource
price = {}
price['lignite'] = 60
price['hard_coal'] = 60
price['natural_gas'] = 60
price['oil'] = 60

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

resource_buses = {
    'global': ['hard_coal', 'lignite', 'oil'],
    'local': ['natural_gas']}


translator = lambda x: de_en[x]


def get_demand():
    'Dummy function until real function exists.'
    demand_df = pd.DataFrame()
    demand_df['elec'] = np.random.rand(8760) * 10 ** 11
    return demand_df


def entity_exists(esystem, uid):
    return len([obj for obj in esystem.entities if obj.uid == uid]) > 0


def create_entity_objects(esystem, region, pp, tclass, bclass):
    ''
    if entity_exists(esystem, ('bus', region.name, pp[1].type)):
        logging.debug('Bus {0} exists. Nothing done.'.format(
            ('bus', region.name, pp[1].type)))
        location = region.name
    elif entity_exists(esystem, ('bus', 'global', pp[1].type)):
        logging.debug('Bus {0} exists. Nothing done.'.format(
            ('bus', 'global', pp[1].type)))
        location = 'global'
    else:
        logging.debug('Creating Bus {0}.'.format(
            ('bus', region.name, pp[1].type)))
        bclass(uid=('bus', region.name, pp[1].type), type=pp[1].type,
               price=price[pp[1].type], regions=[region], excess=False)
        location = region.name
        source.Commodity(
            uid=('resource', region.name, pp[1].type),
            outputs=[obj for obj in esystem.entities if obj.uid == (
                'bus', location, pp[1].type)])

    tclass(
        uid=('transformer', region.name, pp[1].type),
        inputs=[obj for obj in esystem.entities if obj.uid == (
                'bus', location, pp[1].type)],
        outputs=[obj for obj in region.entities if obj.uid == (
                 'bus', region.name, 'elec')],
        in_max=[None],
        out_max=[float(pp[1].cap)],
        eta=[eta_elec[pp[1].type]],
        opex_var=opex_var[pp[1].type],
        regions=[region])

logger.define_logging()
year = 2010
time_index = pd.date_range('1/1/{0}'.format(year), periods=8760, freq='H')
overwrite = False
overwrite = True
conn = db.connection()

# Create a simulation object
simulation = es.Simulation(
    timesteps=range(len(time_index)), verbose=True, solver='glpk',
    objective_options={'function': predefined_objectives.minimize_cost})

# Create an energy system
TwoRegExample = es.EnergySystem(time_idx=time_index, simulation=simulation)

# Add regions to the energy system
TwoRegExample.regions.append(es.Region(
    geom=tools.get_polygon_from_nuts(conn, 'DEE0E'),
    name='Landkreis Wittenberg'))

TwoRegExample.regions.append(es.Region(
    geom=tools.get_polygon_from_nuts(conn, 'DEE01'),
    name='Stadt Dessau-Rosslau'))

# Create global buses
Bus(uid=('bus', 'global', 'coal'), type='coal', price=60, sum_out_limit=10e10,
    excess=False)
Bus(uid=('bus', 'global', 'lignite'), type='lignite', price=60,
    sum_out_limit=10e10, excess=False)

# Create entity objects for each region
for region in TwoRegExample.regions:
    logging.info('Processing region: {0} ({1})'.format(
        region.name, region.code))

    # Get demand time series and create buses. One bus for each demand series.
    demand = get_demand()
    for demandtype in demand.keys():
        Bus(uid=('bus', region.name, demandtype), type=demandtype, price=60,
            regions=[region], excess=False)
        sink.Simple(
            uid=('sink', region.name, demandtype),
            inputs=[obj for obj in TwoRegExample.entities
                    if obj.uid == ('bus', region.name, demandtype)],
            val=demand[demandtype],
            region=[region])

    # Create source object
    feedin_pg.Feedin().create_fixed_source(
        conn, region=region, year=TwoRegExample.time_idx.year[0],
        bustype='elec', **site)

    # Get power plants from database and write them into a DataFrame
    pps_df = db_pps.get_bnetza_pps(conn, region.geom)

    # Add aditional power plants to the DataFrame
    pps_df.loc[len(pps_df)] = 'natural_gas', np.nan, 10 ** 12

    # TODO: Summerize power plants of the same type
    for pwrp in pps_df.iterrows():
        create_entity_objects(TwoRegExample, region, pwrp,
                              tclass=transformer.Simple, bclass=Bus)

    # create storage transformer object for storage
#    transformer.Storage.optimization_options.update({'investment': True})
    bel = [obj for obj in TwoRegExample.entities
           if obj.uid == ('bus', region.name, demandtype)]
    transformer.Storage(uid=('sto_simple', region.name, 'elec'),
                        inputs=bel,
                        outputs=bel,
                        eta_in=1,
                        eta_out=0.8,
                        cap_loss=0.00,
                        opex_fix=35,
                        opex_var=0,
                        capex=1000,
                        cap_max=10 ** 12,
                        cap_initial=0,
                        c_rate_in=1/6,
                        c_rate_out=1/6)

# Connect the electrical bus of region StaDes und LanWit.
bus1 = [obj for obj in TwoRegExample.entities if obj.uid == (
    'bus', 'Landkreis Wittenberg', 'elec')][0]
bus2 = [obj for obj in TwoRegExample.entities if obj.uid == (
    'bus', 'Stadt Dessau-Rosslau', 'elec')][0]
TwoRegExample.connect(bus1, bus2, in_max=10 * 10 ** 12, out_max=0.9 * 10 ** 12,
                      eta=0.9, transport_class=transport.Simple)

pv_lk_wtb = ([obj for obj in TwoRegExample.entities if obj.uid == (
    'FixedSrc', 'Landkreis Wittenberg', 'pv_pwr')][0])

# Multiply PV with 25
pv_lk_wtb.val = pv_lk_wtb.val * 25

# Remove orphan buses
buses = [obj for obj in TwoRegExample.entities if isinstance(obj, Bus)]
for bus in buses:
    if len(bus.inputs) > 0 or len(bus.outputs) > 0:
        logging.debug('Bus {0} has connections.'.format(bus.type))
    else:
        logging.debug('Bus {0} has no connections and will be deleted.'.format(
            bus.type))
        TwoRegExample.entities.remove(bus)

TwoRegExample.simulation = es.Simulation(
    solver='gurobi', timesteps=[t for t in range(8760)],
    stream_solver_output=True, objective_options={
        'function': predefined_objectives.minimize_cost})

for entity in TwoRegExample.entities:
    entity.uid = str(entity.uid)

# Optimize the energy system
TwoRegExample.optimize()

logging.info(TwoRegExample.dump())
