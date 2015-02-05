#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Author: Uwe Krien (uwe.krien@rl-institut.de)
Changes by:
Responsibility: Uwe Krien (uwe.krien@rl-institut.de)
'''

import logging
import dblib as db


def read_demand_region_period(basic_dc, schema, table, region, year, where_str):
    '''
    Returns a demand series for a specific region and a specific year as a
    numpy-array. The columns must be named in the form: 'region_year'
    (e.g: deu_2010, fra_2009). The region must be specified in the iso-3 code.
    The where string might be used to restrict the demand to specific hours.

    This function is pretty basic and could be used for all series in future.

    Uwe Krien (uwe.krien@rl-institut.de)

    returns
        demand series : numpy-array
    '''
    col = region + '_' + str(year)
    logging.debug('Read demand for: %s' % col)
    return db.fetch_columns(basic_dc, schema, table, columns=col,
        as_np=True, orderby='hoy', where_string=where_str)[col]


def read_demand_from_db(basic_dc, p_dc, demand_dc):
    '''
    [Description]

    Uwe Krien (uwe.krien@rl-institut.de)

    Parameters

    Keyword arguments

    Returns
    '''
    start_hoy = p_dc['simulation']['timestep_start']
    end_hoy = p_dc['simulation']['timestep_end']
    where_str = "hoy>%s and hoy<=%s" % (start_hoy, end_hoy)
    for reg in p_dc['energy_system']['energy_system_regions']:
        demand_dc['demand_elec'].setdefault(reg, {})
        demand_dc['demand_elec'][reg]['lele'] = read_demand_region_period(
            basic_dc,
            p_dc['input']['input_demand']['input_demand_elec']['demand_schema'],
            p_dc['input']['input_demand']['input_demand_elec']['demand_table'],
            reg, p_dc['input']['data_year'], where_str)
        demand_dc['demand_elec_total_all'] = (sum(
            demand_dc['demand_elec'][reg]['lele']) + (
                demand_dc['demand_elec_total_all']))
    return demand_dc


def scale_demand(basic_dc, p_dc, demand_dc):
    '''
    [Description]

    Uwe Krien (uwe.krien@rl-institut.de)

    Parameters

    Keyword arguments

    Returns
    '''
    start_hoy = p_dc['simulation']['timestep_start']
    end_hoy = p_dc['simulation']['timestep_end']
    where_str = "hoy>%s and hoy<=%s" % (start_hoy, end_hoy)
    basic_demand = read_demand_region_period(basic_dc,
        p_dc['input']['input_demand']['input_demand_elec']['demand_schema'],
        p_dc['input']['input_demand']['input_demand_elec']['demand_table'],
        p_dc['input']['input_demand']['input_demand_elec']['scale_region'],
        p_dc['input']['input_demand']['input_demand_elec']['year'],
        where_str)
    basic_demand_year = sum(read_demand_region_period(basic_dc,
        p_dc['input']['input_demand']['input_demand_elec']['demand_schema'],
        p_dc['input']['input_demand']['input_demand_elec']['demand_table'],
        p_dc['input']['input_demand']['input_demand_elec']['scale_region'],
        p_dc['input']['input_demand']['input_demand_elec']['year'], "hoy>0"))
    for reg in p_dc['energy_system']['energy_system_regions']:
        where_str = "name_set='%s' and region='%s'" % (
            p_dc['input']['input_demand']['input_demand_elec']['scale_set'],
            reg)
        col = str(p_dc['input']['input_demand']['input_demand_elec']['year'])
        yearly_demand = db.fetch_columns(basic_dc,
            p_dc['input']['input_demand']['input_demand_elec']['scale_schema'],
            p_dc['input']['input_demand']['input_demand_elec']['scale_table'],
            columns=col,
            where_string=where_str)[col]
        factor = yearly_demand[0] / basic_demand_year
        demand_dc['demand_elec'].setdefault(reg, {})
        demand_dc['demand_elec'][reg]['lele'] = basic_demand * factor
        demand_dc['demand_elec_total_all'] = (sum(
            demand_dc['demand_elec'][reg]['lele']) + (
            demand_dc['demand_elec_total_all']))
    return demand_dc


def read_demand_heat(basic_dc, parameter_dc, demand_dc):
    '''
    Reads the heat demand
    '''
    #Create list with the names of the heat load columns
    demand_dc['demand_heat'] = {}
    col_list = []
    year = parameter_dc['input']['data_year']
    for reg in parameter_dc['energy_system']['energy_system_regions']:
        if parameter_dc['lists']['domestic']:
            for comp in parameter_dc['lists']['domestic']:
                col_list.extend([(comp + '_' + reg + '_' + year), ])
        if parameter_dc['lists']['district']:
            col_list.extend([('dst0_' + reg + '_' + year), ])

    # Creates where string to read only the requested hours
    start_hoy = parameter_dc['simulation']['timestep_start']
    end_hoy = parameter_dc['simulation']['timestep_end']
    where_str = "hoy>%s and hoy<=%s" % (start_hoy, end_hoy)

    # fetch the columns of the col list
    tmp_dc = db.fetch_columns(basic_dc, (parameter_dc['input']['input_demand']
        ['input_demand_heat']['schema_demand_heat']), (parameter_dc['input']
        ['input_demand']['input_demand_heat']['table_demand_heat']),
        columns=col_list, as_np=True, orderby='hoy', where_string=where_str)

    # Put the arrays into the demand dictionary (demand_dc)
    for reg in parameter_dc['energy_system']['energy_system_regions']:
        demand_dc['demand_heat'][reg] = {}
        if parameter_dc['lists']['domestic']:
            for comp in parameter_dc['lists']['domestic']:
                tmp_str = comp + '_' + reg + '_' + year
                demand_dc['demand_heat'][reg][comp] = tmp_dc[tmp_str]
        if parameter_dc['lists']['district']:
            tmp_str = 'dst0_' + reg + '_' + year
            demand_dc['demand_heat'][reg]['dst0'] = tmp_dc[tmp_str]
    return demand_dc


def read_demand_elec(basic_dc, parameter_dc, demand_dc):
    '''
    [Description]

    Uwe Krien (uwe.krien@rl-institut.de)

    Parameters

    Keyword arguments

    Returns
    '''
    demand_dc['demand_elec'] = {}
    demand_dc['demand_elec_total_all'] = 0
    method = (parameter_dc['input']['input_demand']['input_demand_elec']
        ['demand_method'])
    if method == 'read':
        demand_dc = read_demand_from_db(basic_dc, parameter_dc, demand_dc)
    elif method == 'scale':
        demand_dc = scale_demand(basic_dc, parameter_dc, demand_dc)
    return demand_dc


def read_demand_data(basic_dc, parameter_dc):
    '''
    [Description]

    Uwe Krien (uwe.krien@rl-institut.de)

    Parameters

    Keyword arguments

    Returns
    '''
    demand_dc = {}
    demand_dc = read_demand_elec(basic_dc, parameter_dc, demand_dc)
    if (parameter_dc['energy_system']['energy_system_transformer4heat'] or
            parameter_dc['energy_system']['energy_system_transformer4chp']):
        demand_dc = read_demand_heat(basic_dc, parameter_dc, demand_dc)
    return demand_dc