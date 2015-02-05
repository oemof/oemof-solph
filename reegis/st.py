#!/usr/bin/python
# -*- coding: utf-8

import database as db
import numpy as np


def get_st_feed_in(building_type, ref_state, load):
    '''
    Retrieves the solarthermal feed-in into the thermal storage in MWh/h
    of the specified building_type and state of refurbishment.
    '''

    column = building_type + '_' + ref_state + '_' + load
    col_1 = column + '_S'
    col_2 = column + '_SO'
    col_3 = column + '_SW'

    st_feed_in = db.retrieve_from_db_table(
        'wittenberg', 'trnsys_st_zeitreihen', [col_1, col_2, col_3],
        primary_key='id', order='yes')

    av_st_feed_in = np.sum(st_feed_in, axis=1) / 3 / 1000

    return av_st_feed_in


def trnsys_p_set():
    '''
    Returns a dictionary (st_p_set) with relevant parameters used in the
    TRNSYS simulation.
    '''
    st_p_set = {
        # Heating demand
        'heating_demand': {  # MWh/a
            'EFH': {
                'Neubau': 9.089,
                'Altbau_vor95': 12.618,
                'Altbau_vor82': 15.184,
                'Altbau_san': 9.089},
            'MFH': {
                'Neubau': 33.212,
                'Altbau_vor95': 46.106,
                'Altbau_vor82': 55.484,
                'Altbau_san': 33.212}},
        # WW demand
        'ww_demand': {  # MWh/a
            'EFH': 2.780,
            'MFH': 10.159},
        # Area
        'st_area': {  # m²
            'EFH': {
                'WW': 2.4,
                'HWW': 13.1},
            'MFH': {
                'WW': 10.6,
                'HWW': 49.7}},
        # Size of thermal storage
        'size_ts': {  # m³
            'EFH': {
                'WW': 0.240,
                'HWW': 0.775},
            'MFH': {
                'WW': 1.061,
                'HWW': 3.015}}
             }
    return st_p_set


def weighing_by_refurbishment(var, building_type, p_set):
    '''
    This definitions weighs a variable by the share of each refurbishment state.

    var -- dictionary with value of the variable to be weighed in this
           definition of each refurbishment state
    building_type -- 'EFH' or 'MFH'
    '''

    dict_share_ref = p_set['ref_state'][building_type]
    fac = p_set['share_new_buildings']

    p_set['share_new_buildings']
    weighed_var = (var['Neubau'] * fac * dict_share_ref['fully ref'] +
        var['Altbau_san'] * (1 - fac) * dict_share_ref['fully ref'] +
        var['Altbau_vor95'] * dict_share_ref['partially ref'] +
        var['Altbau_vor82'] * dict_share_ref['unrenovated'])

    return weighed_var


def st_feed_in(p_set, typ, annual_demand):

    # import parameterset used in TRNSYS
    st_p_set = trnsys_p_set()

    # Average heating demand [MWh/a]
    av_heating_demand = weighing_by_refurbishment(
        st_p_set['heating_demand'][typ], typ, p_set)

    # Total average demand (heating + warm water) [MWh/a]
    total_av_demand = st_p_set['ww_demand'][typ] + av_heating_demand

    # Number of households with solarthermal systems
    number_st = annual_demand / total_av_demand
    number_st_ww = p_set['st_share_ww_only'][typ] * number_st
    number_st_hww = number_st - number_st_ww

    # Hourly solarthermal potential [MWh/h]
    hourly_st_pot_ww_tmp = {}
    hourly_st_pot_hww_tmp = {}

    ref_state = ['Neubau', 'Altbau_san', 'Altbau_vor95', 'Altbau_vor82']
    for i in ref_state:
        hourly_st_pot_ww_tmp[i] = get_st_feed_in(typ, i, 'WW')
        hourly_st_pot_hww_tmp[i] = get_st_feed_in(typ, i, 'HWW')

    hourly_st_pot_ww = weighing_by_refurbishment(
        hourly_st_pot_ww_tmp, typ, p_set) * number_st_ww
    hourly_st_pot_hww = weighing_by_refurbishment(
        hourly_st_pot_hww_tmp, typ, p_set) * number_st_hww
    hourly_st_pot = hourly_st_pot_ww + hourly_st_pot_hww

    # Area [m²]
    area = (number_st_ww * st_p_set['st_area'][typ]['WW'] +
        number_st_hww * st_p_set['st_area'][typ]['HWW'])

    # Total size of thermal storages [m³]
    size_ts = (number_st_ww * st_p_set['size_ts'][typ]['WW'] +
        st_p_set['size_ts'][typ]['HWW'] * number_st_hww)

    return hourly_st_pot, area, size_ts


def get_hourly_st_pot(p_set, input_data, hourly_heat_demand,
    schema=None, save=None, save_to_table=None, save_to_column='st_pot'):
    '''
    Returns the hourly PV potential in MWh/h.
    Depending on which potential is wanted, either the total potential of the
    chosen district, the scaled potential (scaled to a maximum capacity of 1 MW)
    or the district's potential (installed capacity plus additional potential)
    is returned.
    Depending on the chosen use case the hourly potential is either retrieved
    from a file or database or calculated.
    '''

    ######## erstmal nicht die Option, eine Potenzialzeitreihe einzulesen,
    ######## da dann auch die Speichergröße und Fläche gegeben sein müssen,
    ######## die nur mit den TRNSYS Parametern berechnet werden können...
    ## retrieve hourly solarthermal potential from the database
    #if use_case == 'db':
        #if db.table_exists(table_name):
            #hourly_st_potential = db.retrieve_from_db_table(
                #schema, table_name, column_name, order='yes')
            #hourly_st_potential = np.reshape(
                #hourly_st_potential, (-1, ))
        #else:
            #print (('Table to retrieve the hourly pv potential from ' +
            #'does not exist.'))
    ## retrieve hourly st potential from file
    #elif use_case == 'file':
        #hourly_st_potential = \
            #db.read_profiles_from_file(filename, directory)[column_name]
        #hourly_st_potential = np.reshape(hourly_st_potential, (-1, ))
    ## calculate solarthermal potential
    #elif use_case == 'calc':
        #hourly_st_potential = st_feed_in(input_data)
    #else:
        #print (('Hourly solarthermal potential cannot be returned because ' +
        #'of invalid use case. The use case chosen was: %s' % use_case))

    # calculate hourly solarthermal potential [MWh/h] plus size of the
    # collector [m²] and the thermal storages [l] for single- and multy-family
    # houses
    hourly_st_potential = {}
    hourly_st_potential['EFH'], area_efh, size_ts_efh = st_feed_in(
        p_set, 'EFH', sum(hourly_heat_demand['ST EFH']))
    hourly_st_potential['MFH'], area_mfh, size_ts_mfh = st_feed_in(
        p_set, 'MFH', sum(hourly_heat_demand['ST MFH']))

    # drop keys in hourly_heat_demand dictionary
    hourly_heat_demand.pop('ST EFH', None)
    hourly_heat_demand.pop('ST MFH', None)

    # calculate total solarthermal potential [MWh/h] plus size of the
    # collector [m²] and the thermal storages [MWh] for single- and multy-family
    # houses
    area = area_efh + area_mfh
    input_data['cap ST Storage Thermal'] = \
        (size_ts_efh + size_ts_mfh) / 10 ** 3 * 1.163 * (90 - 25)
    input_data['Discharge rate ST Storage Thermal'] = \
        input_data['cap ST Storage Thermal']
    hourly_st_pot = hourly_st_potential['EFH'] + hourly_st_potential['MFH']

    # save results to db
    if save:
        if db.table_exists(save_to_table):
            # save
            db.save_results_to_db(
                schema, save_to_table, save_to_column, hourly_st_pot)
        else:
            # create output table and id column
            db.create_db_table(schema, save_to_table,
                save_to_column + ' real')
            stringi = '(1)'
            for i in range(2, 8761):
                stringi = stringi + ',(' + str(i) + ')'
            db.insert_data_into_db_table(schema, save_to_table, 'id', stringi)
            # save
            db.save_results_to_db(
                schema, save_to_table, save_to_column, hourly_st_pot)

    return hourly_st_pot, area