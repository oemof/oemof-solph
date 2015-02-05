#!/usr/bin/python  # lint:ok
# -*- coding: utf-8

import logging
import numpy as np
import dblib as db


def read_results(var, main_dc):
    '''
    Reading results
    '''
    # Creates new dict.branch and adds the info table from the database
    main_dc.setdefault('res', {})
    read_info_table(var, main_dc)
    info = main_dc['res']['info']

    # Finds the result tables, which are connected to the given scenario
    where_str = "table_schema = '{0}' and table_name LIKE '{1}\_\_%'".format(
        main_dc['basic']['res_schema'],
        info['energy_system'].lower())
    res_tables = db.fetch_columns(main_dc['basic'], 'information_schema',
        'tables', columns='table_name', where_string=where_str)['table_name']

    # Extract the keys from the names of the result tables.
    res_keys = []
    for table in res_tables:
        res_keys.append(table.replace("{0}__".format(
            info['energy_system'].lower()), ""))

    # Creates an info section and adds information about table_names
    main_dc['res'].setdefault('info', {})
    main_dc['res']['info'].setdefault('keys', {})
    main_dc['res']['info'].setdefault('tables', res_tables)

    #for types in list(main_dc['res']table_type'].keys()):
    for key, table in zip(res_keys, res_tables):
        col_ls = db.fetch_column_names(main_dc['basic'],
            main_dc['basic']['res_schema'], table)

        # if a column 'region' is exists an extra level is added
        # to the dictionary
        if 'region' in col_ls:
            with_reg = True
        else:
            with_reg = False

        # if a column 'timestep' is exists the results are sorted
        # by this column
        if 'timestep' in col_ls:
            orderby = 'timestep'
            table_with_timesteps = table
        else:
            orderby = None

        # Remove columns that contain meta data
        col_ls = db.remove_from_list(col_ls, ['id', 'timestep', 'region'])

        #Saves the list of the components in the info section
        main_dc['res']['info']['keys'][key] = col_ls

        # Saves the regions in the info table.
        main_dc['res']['info']['regions'] = list(info['regions'])

        # Reads the tables
        if with_reg:
            main_dc['res'].setdefault(key, {})
            for region in main_dc['res']['info']['regions']:
                where_string = '''{0} = '{1}' and {2} = {3}'''.format('region',
                    region, 'id', info['id'])
                main_dc['res'][key][region] = db.fetch_columns(main_dc['basic'],
                    main_dc['basic']['res_schema'], table, columns=col_ls,
                    as_np=True, orderby=orderby, where_string=where_string)
        else:
            main_dc['res'][key] = db.fetch_columns(main_dc['basic'],
                main_dc['basic']['res_schema'], table, columns=col_ls,
                as_np=True, orderby=orderby)

    # Adds information about the timeseries to the info section
    timeseries = db.fetch_columns(main_dc['basic'],
        main_dc['basic']['res_schema'],
        table_with_timesteps, columns='timestep', unique=True, as_np=True,
        orderby='timestep')['timestep']
    main_dc['res']['info']['timesteps'] = len(timeseries)
    main_dc['res']['info']['timestart'] = timeseries.min()
    main_dc['res']['info']['timeend'] = timeseries.max()
    main_dc['res']['info']['timeseries'] = timeseries


def read_info_table(var, main_dc):
    '''
    Reads the info table from the result schema.
    '''
    main_dc['res'].setdefault('info', {})
    var_type = db.check_parameter(var)
    main_dc['res']['info'] = dict(db.fetch_row(main_dc['basic'],
        main_dc['basic']['res_schema'], 'info', var_type, var))


def get_next_level_key(dictionary):
    '''
    Returns a list of keys for the next level of the dictionary.
    This functions works, if the dictionary has the same keys in the next level
    for all keys in the present level. Otherwise the result will be random.
    '''
    return list(dictionary[list(dictionary.keys())[0]].keys())


def devide_vector(vector, keep_sign=False):
    '''
    Devides a vector with positive and negative values into two vectors.
    One vector will contain the positive values and one the negative ones.

    By default the values in both vectors are positve.
    Set the value 'keep_sign=True' to keep the negative values negative.

    Returns the postive and the negative sector
    '''
    positive_vector = np.zeros(len(vector))
    positive_vector[vector > 0] = vector[vector > 0]

    negative_vector = np.zeros(len(vector))
    negative_vector[vector < 0] = vector[vector < 0]

    if not keep_sign:
        negative_vector = negative_vector * (-1)

    return positive_vector, negative_vector


def read_results_generation_demand(var, main_dc):
    '''
    Reads the results an order them by type and generation/demand.
    see: restructure_results_generation_demand()
    '''
    read_results(var, main_dc)
    main_dc['res'] = restructure_results_generation_demand(main_dc)


def restructure_results_generation_demand(main_dc):
    '''
    Restructure the dictionary.

    Returns a dictionary with two keys (generation, demand) for every
    energy type (elec, heat).
    '''

    logging.info('Restructure results into generation/demand and heat/elec')
    result_dc = {}
    result_dc.setdefault('elec', {})
    result_dc.setdefault('heat', {})
    result_dc.setdefault('info', {})

    # Definition of the connection sets
    def_dc = {}
    def_dc.setdefault('elec', {})
    def_dc.setdefault('heat', {})
    demand_dc = {}
    demand_dc.setdefault('demand', {})
    def_dc['elec']['generation'] = ['elec_storage_discharge', 'power_gen', ]
    def_dc['elec']['demand'] = ['elec_storage_charge', 'ptg_power_in',
                                'demand', 'excess']
    def_dc['heat']['generation'] = ['heat_gen', 'heat_storage_discharge']
    def_dc['heat']['demand'] = ['demand', 'heat_storage_charge', 'heat_excess']
    demand_dc['demand']['heat'] = ['twcb', 'dst0', 'thoi', 'thng']
    demand_dc['demand']['elec'] = ['lele']
    # installed = ['power_inst', 'ptg_power_inst', 'gas_storage_inst',
    #              'storage_inst', 'trm_inst']

    # Restructures the different tables to the sections as defined above.
    for energy_type in list(def_dc.keys()):
        result_dc['info'].setdefault(energy_type, {})
        for u_type in list(def_dc[energy_type].keys()):
            result_dc[energy_type][u_type] = {}
            result_dc['info'][energy_type].setdefault(u_type, {})
            for key in def_dc[energy_type][u_type]:
                if key in list(main_dc['res'].keys()):
                    comps = main_dc['res']['info']['keys'][key]
                    if key == 'demand':
                        comps = list(set(comps).intersection(set(
                            demand_dc['demand'][energy_type])))
                    for c in comps:
                        result_dc[energy_type][u_type][c] = {}
                        for reg in main_dc['res']['info']['regions']:
                            result_dc[energy_type][u_type][c][reg] = (
                                main_dc['res'][key][reg][c])

    # Save the energy types to the info branch.
    # So far only ['elec'] or ['elec', 'heat'] are possible.
    result_dc['info']['energy_types'] = ['elec']
    if result_dc['heat']['generation']:
        result_dc['info']['energy_types'].append('heat')

    # Devides transmission power into transmission export and import.
    if 'trm_power' in main_dc['res']:

        # So far there are only transmission lines for the power sector
        energy_type = 'elec'

        # Creates the new keys for the new vector set.
        result_dc[energy_type]['generation']['trmi'] = {}
        result_dc[energy_type]['demand']['trme'] = {}

        # Devides the vector for every region.
        for r in main_dc['res']['info']['regions']:
            [pos, neg] = devide_vector(main_dc['res']['trm_power'][r])
            result_dc[energy_type]['generation']['trmi'][r] = neg
            result_dc[energy_type]['demand']['trme'][r] = pos

    # Adds the electrical resource to the demand branch
    energy_type = 'elec'
    for reg in main_dc['res']['info']['regions']:
        if 'rele' in main_dc['res']['fossil_resources'][reg]:
            result_dc[energy_type]['demand'].setdefault('rele', {})
            result_dc[energy_type]['demand']['rele'][reg] = (
                main_dc['res']['fossil_resources'][reg]['rele'])

    # Copys the info branch of the res_data dictionary to the new dictionary.
    for energy_type in result_dc['info']['energy_types']:
        for u_type in list(result_dc['info'][energy_type].keys()):
            result_dc['info'][energy_type][u_type] = (
                list(result_dc[energy_type][u_type].keys()))
    for key in list(main_dc['res']['info'].keys()):
        if key not in result_dc['info']:
            result_dc['info'][key] = main_dc['res']['info'][key]
    return result_dc


def restructure_results_for_balance(main_dc, res_data):
    '''
    Restructure the dictionary for print balances and annual sums of generation
    and demand.

    Returns a dictionary with a few keys (generation, demand, trm_power,
    charge, discharge, gas) for every energy type (elec, heat).
    '''

    logging.info('Restructure results for plotting!')
    result_dc = {}
    result_dc.setdefault('elec', {})
    result_dc.setdefault('heat', {})
    result_dc.setdefault('info', {})

    # Definition of the connection sets
    def_dc = {}
    def_dc.setdefault('elec', {})
    def_dc.setdefault('heat', {})
    def_dc['elec']['generation'] = ['power_gen']
    def_dc['elec']['demand'] = ['demand_elec', 'excess']
    def_dc['elec']['discharge'] = ['storage_discharge',
                                   'gas_storage_discharge']
    def_dc['elec']['charge'] = ['storage_charge', 'gas_storage_charge']
    def_dc['elec']['gas'] = ['splitted_gas_flow']
    def_dc['elec']['trm_power'] = ['trm_power']
    def_dc['heat']['generation'] = ['heat_gen']
    def_dc['heat']['demand'] = ['demand_heat']

    # Restructures the different tables to the sections as defined above.
    for energy_type in list(def_dc.keys()):
        result_dc['info'].setdefault(energy_type, {})
        for u_type in list(def_dc[energy_type].keys()):
            result_dc[energy_type][u_type] = {}
            result_dc['info'][energy_type].setdefault(u_type, {})
            for key in def_dc[energy_type][u_type]:
                if key in list(res_data.keys()):
                    # special handling of trm_power data
                    if u_type is 'trm_power':
                            for reg in main_dc['res']['info']['regions']:
                                result_dc[energy_type][u_type][reg] = (
                                    res_data[key][reg])
                    # standard procedure for all other data
                    else:
                        comps = main_dc['res']['info']['keys'][key]
                        for c in comps:
                            result_dc[energy_type][u_type][c] = {}
                            for reg in main_dc['res']['info']['regions']:
                                result_dc[energy_type][u_type][c][reg] = (
                                    res_data[key][reg][c])

    # Adds the electrical resource to the demand branch
    energy_type = 'elec'
    for reg in main_dc['res']['info']['regions']:
        if 'rele' in main_dc['res']['fossil_resources'][reg]:
            result_dc[energy_type]['demand'].setdefault('rele', {})
            result_dc[energy_type]['demand']['rele'][reg] = (
                main_dc['res']['fossil_resources'][reg]['rele'])

    # Save the energy types to the info branch.
    # So far only ['elec'] or ['elec', 'heat'] are possible.
    result_dc['info']['energy_types'] = ['elec']
    if result_dc['heat']['generation']:
        result_dc['info']['energy_types'].append('heat')

    # Copys the info branch of the res_data dictionary to the new dictionary.
    for energy_type in result_dc['info']['energy_types']:
        for u_type in list(result_dc['info'][energy_type].keys()):
            result_dc['info'][energy_type][u_type] = (
                list(result_dc[energy_type][u_type].keys()))
    result_dc['info'].update(main_dc['res']['info'])

    return result_dc
