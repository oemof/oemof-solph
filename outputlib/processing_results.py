#!/usr/bin/python
# -*- coding: utf-8

'''
Author: Caroline Möller (caro.moeller@rl-institut.de)
Changes by: Uwe Krien (uwe.krien@rl-institut.de)
Responsibility: Uwe Krien (uwe.krien@rl-institut.de)
'''


########################## write data into database ##################
import os
import logging
import datetime
from . import write_db as write_db
from . import remove_results_from_db as rm
from . import post_calculations_file as pcal
from . import db_utilities as dbu
import dblib as db


def create_info_columns_if_not_exist(main_dt):
    '''
    Checks for missing columns in the info table and logs an error.
    '''
    needed_cols = list(main_dt['lp']['info']['data'].keys())
    existing_cols = db.fetch_column_names(
        main_dt['basic'], main_dt['basic']['res_schema'], 'info')
    db.remove_from_list(needed_cols, existing_cols)
    if needed_cols:
        logging.warning('Missing columns in "info" table: {0}'.format(
            needed_cols))
        dbu.creates_or_completes_info_table(main_dt, needed_cols)


def create_res_tables_if_not_exist(main_dt, name_scenario, tbnames):
    '''
    [Description]

    [Autor]

    Parameters

    Keyword arguments

    Returns
    '''
    for table in tbnames:
        if table == 'info':
            esy_tbname = table
        else:
            esy_tbname = name_scenario + '__' + table
        if (db.exists_table(main_dt['basic'], main_dt['basic']['res_schema'],
                esy_tbname)):
            pass
        elif bool(list(main_dt['lp'][table]['data'].keys())):
            logging.info(('Creating table %s' % esy_tbname))
            write_db.create_table(main_dt['basic'],
                main_dt['basic']['res_schema'],
                esy_tbname, list(main_dt['lp'][table]['data'].keys()),
                main_dt['lp'][table]['is_series'],
                main_dt['lp'][table]['with_regions'],
                main_dt['lp'][table]['data'])
        else:
            logging.warning('Result table %s does not exits, ' % esy_tbname +
                'but has no data. Will not create it.')


def write_data2all_tables(main_dt, esy_tbnames, tbnames, overwrite=False):
    '''
    [Description]

    [Autor]

    Parameters

    Keyword arguments

    Returns
    '''
    for tb in range(len(esy_tbnames)):
        if (db.exists_table(main_dt['basic'], main_dt['basic']['res_schema'],
                esy_tbnames[tb])):
            logging.debug(('Writing table %s' % esy_tbnames[tb]))
            write_db.write_results(main_dt['basic'],
                main_dt['basic']['res_schema'],
                esy_tbnames[tb], main_dt['timesteps'],
                list(main_dt['lp'][tbnames[tb]]['data'].keys()),
                main_dt['energy_system']['regions'],
                main_dt['lp'][tbnames[tb]]['is_series'], main_dt['info']['id'],
                main_dt['lp'][tbnames[tb]]['data'],
                main_dt['lp'][tbnames[tb]]['with_regions'],
                main_dt['simulation']['timestep_start'])
        else:
            logging.warning('Table %s is not written' % esy_tbnames[tb])


def add_scenario_as_meta_info(main_dt):
    '''
    Adds values from the scenario definitions to the results info table.
    '''
    main_dt['lp']['info']['data'].update(main_dt['info'])
    main_dt['lp']['info']['data'].pop('id', None)
    if main_dt['lp']['info']['data']['sim_year'] is None:
        main_dt['lp']['info']['data']['sim_year'] = 'not_set'


def add_meta_info(main_dt):
    '''
    Adds different system and simulation parameter to results info table.
    '''
    # Adds the scenario definitions to the results info table
    add_scenario_as_meta_info(main_dt)

    # Some field names has to be changed to avoid confusion
    main_dt['lp']['info']['data']['last modification of input data'] = str(
        main_dt['lp']['info']['data'].pop('lastmodified'))
    main_dt['lp']['info']['data']['input data changed by'] = (
        main_dt['lp']['info']['data'].pop('changed_by'))

    # Adds more values
    main_dt['lp']['info']['data']['user_name'] = os.getenv('USER')
    main_dt['lp']['info']['data']['os_system'] = os.name
    main_dt['lp']['info']['data']['sim_end_time'] = str(
        datetime.datetime.now())

    # Adds the checker values
    main_dt['lp']['info']['data'].update(main_dt['check'])

    # Adds info for the energy_system
    main_dt['lp']['info']['data']['energy_system'] = (
        main_dt['info']['name_set'])
    region_db = str(
        main_dt['energy_system']['regions']).replace(']', '}').replace(
        '[', '{').replace('\'', '"')
    main_dt['lp']['info']['data']['regions'] = region_db

    # Adds simulation table to info
    main_dt['lp']['info']['data']['solver'] = main_dt['simulation']['solver']
    main_dt['lp']['info']['data']['re_share'] = (
        main_dt['simulation']['re_share'])
    main_dt['lp']['info']['data']['opt_target'] = (
        main_dt['simulation']['opt_target'])
    main_dt['lp']['info']['data']['investment'] = (
        main_dt['simulation']['investment'])


def remove_res_tables(main_dt):
    '''
    irrelevant internal data is removed from results variables
    '''
    remove_fields = []
    for i in remove_fields:
        del main_dt['lp'][i]


def check_if_results_exist(main_dt, overwrite):
    '''
    '''
    tester = db.fetch_columns(main_dt['basic'], main_dt['basic']['res_schema'],
        'info', columns='id', where_column='id',
        where_condition=main_dt['info']['id'])['id']
    if tester:
        tester = True
        if overwrite:
            logging.warning('System will overwrite existing results for ' +
                'scenario: %s.' % (main_dt['info']['id']))
        else:
            logging.warning('System will try to create subscenario to save ' +
                'the existing results of scenario %s.' % main_dt['info']['id'])
            logging.warning('This mode is unsecure and might cause data' +
                ' losses. Try to avoid this by using a new scenario.')
    else:
        tester = False
    return tester


def add_timeseries_to_results(main_dt):
    'Adds the timeseries of feedin and demand to the lp-branch.'
    r0 = list(main_dt['timeseries']['demand'].keys())[0]

    main_dt['lp']['demand'] = {}
    main_dt['lp']['demand']['is_series'] = True
    main_dt['lp']['demand']['with_regions'] = True
    main_dt['lp']['demand']['data'] = {}
    for c in list(main_dt['timeseries']['demand'][r0].keys()):
        main_dt['lp']['demand']['data'][c] = {}
        for t in main_dt['timesteps']:
            main_dt['lp']['demand']['data'][c][t] = {}
            for r in main_dt['energy_system']['regions']:
                main_dt['lp']['demand']['data'][c][t][r] = (
                    main_dt['timeseries']['demand'][r][c][t])


def write_all(main_dt, overwrite=False):
    '''
    [Description]

    [Autor]

    Parameters

    Keyword arguments

    Returns
    '''
    # create table names (with energy system)
    esy_tbnames = []
    name_scenario = main_dt['info']['name_set'].lower().replace(' ', '_')

    add_timeseries_to_results(main_dt)

    if 'sng_resources' in list(main_dt['lp'].keys()):
        remove_res_tables(main_dt)

    tbnames = list(main_dt['lp'].keys())

    for table in tbnames:
        if table == 'info':
            esy_tbnames.append(table)
        else:
            esy_tbnames.append(name_scenario + '__' + table)

    pcal.post_calculations(main_dt)

    add_meta_info(main_dt)

    create_res_tables_if_not_exist(main_dt, name_scenario, tbnames)

    create_info_columns_if_not_exist(main_dt)

    if check_if_results_exist(main_dt, overwrite):
        rm.smart_remove_results(main_dt, list(main_dt['lp'].keys()), overwrite)

    write_data2all_tables(main_dt, esy_tbnames, tbnames, overwrite=overwrite)
