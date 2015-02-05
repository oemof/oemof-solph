##!/usr/bin/python    # lint:ok
# -*- coding: utf-8 -*-

'''
Author: Uwe Krien (uwe.krien@rl-institut.de)
Changes by:
Responsibility: Uwe Krien (uwe.krien@rl-institut.de)
'''

import logging
import dblib as db
from . import basic_dinput_functions as bf
from . import basic_dinput_functions as rb


def save_fetch_row(basic_dc, inner_dc, table, name_set, name, region):
    '''
    Reads a data row for the given name_set (and the given region, if given)
    for an object given be the "name" parameter.
    If nothing is found for the given name_set, the default name_set is used.
    If nothing is found for the given region, the default region is used.
    If nothing is found a logging error is raised.

    Uwe Krien (uwe.krien@rl-institut.de)

    Returns
        Data row from the database : dictionary
    '''
    set_s = "name_set='%s'" % name_set
    setd_s = "name_set='default'"
    and_s = " and "
    name_s = "name='%s'" % name
    reg_s = "region='%s'" % region
    regd_s = "region='default'"
    where_str = set_s + and_s + name_s
    if region:
        where_str = where_str + and_s + reg_s
        inner_dc[name] = db.fetch_row(basic_dc, basic_dc['schema'], table,
            where_string=where_str)
    if not inner_dc[name] and region:
        tmp_str = where_str.replace(reg_s, regd_s)
        inner_dc[name] = db.fetch_row(basic_dc, basic_dc['schema'], table,
            where_string=tmp_str)
    if not region:
        inner_dc[name] = db.fetch_row(basic_dc, basic_dc['schema'], table,
            where_string=where_str)
    if not inner_dc[name]:
        where_str = where_str.replace(set_s, setd_s)
        inner_dc[name] = db.fetch_row(basic_dc, basic_dc['schema'], table,
            where_string=where_str)
    if not inner_dc[name] and region:
        where_str = where_str.replace(reg_s, regd_s)
        inner_dc[name] = db.fetch_row(basic_dc, basic_dc['schema'], table,
            where_string=where_str)
    if not inner_dc[name]:
        logging.error('No Data found in table %s. Constraint: %s' % (
            table, where_str))
    else:
        inner_dc[name] = dict(inner_dc[name])
    return inner_dc


def read_inner_table(basic_dc, table, esys_dc, name_set, region=None):
    if table.split('_')[0] == 'parameter':
        list_name = basic_dc['energy_system_table'] + '_' + table.split('_')[1]
        names = esys_dc[list_name]
    else:
        names = db.fetch_columns(basic_dc, basic_dc['schema'], table,
            columns='name', unique=True, where_column='name_set',
            where_condition=name_set)['name']
    inner_dc = {l: {} for l in names}
    for name in names:
        save_fetch_row(basic_dc, inner_dc, table, name_set, name, region)
    return inner_dc


def read_vertical_table(basic_dc, sub_dc, table, esys_dc):
    name_set = sub_dc[table]
    sub_dc[table] = {}
    columns = db.fetch_column_names(basic_dc, basic_dc['schema'], table)
    if 'region' in columns:
        for region in list(esys_dc['energy_system_regions']):
            sub_dc[table][region] = read_inner_table(basic_dc, table, esys_dc,
                name_set, region=region)
    else:
        sub_dc[table] = read_inner_table(basic_dc, table, esys_dc, name_set)
    sub_ls = bf.remove_from_list(columns, basic_dc['remove_columns'])
    return (sub_dc[table], sub_ls)


def read_row_table(basic_dc, sub_dc, table):
    sub_dc[table] = db.fetch_row(
        basic_dc, basic_dc['schema'],
        table,
        where_column='name_set',
        where_condition=sub_dc[table])
    sub_ls = bf.remove_from_list(list(sub_dc[table].keys()),
        basic_dc['remove_columns'])
    return (sub_dc[table], sub_ls)


def read_subtable(basic_dc, sub_dc, table, esys_dc):
    '''
    Description

    Autor

    Parameters

    Keyword arguments

    Returns
    '''
    table_type = rb.check_table_structure(basic_dc, table)
    if table_type == 'vertical':
        return read_vertical_table(basic_dc, sub_dc, table, esys_dc)
    elif table_type == 'row':
        return read_row_table(basic_dc, sub_dc, table)
    else:
        logging.warning('Something is wrong in the database structure')


def read_parameter_tables(basic_dc, para_dc):

    '''
    [Description]

    [Autor]

    Parameters

    Keyword arguments

    Returns
    '''
    schema_tables = db.fetch_table_names(basic_dc, basic_dc['schema'])
    schema_tables.remove(basic_dc['energy_system_table'])
    esys_dc = para_dc[basic_dc['energy_system_table']]
    tables = bf.cut_lists(list(para_dc.keys()), schema_tables)
    for table in tables:
        logging.debug('Reading parameter table: %s' % table)
        tmp_dc, tmp_ls = read_subtable(basic_dc, para_dc, table, esys_dc)
        subtables = [x for x in tmp_ls if x in set(schema_tables)]
        para_dc[table] = dict(tmp_dc)
        for subtable in subtables:
            subtmp_dc, tmp_ls = read_subtable(basic_dc, tmp_dc, subtable,
                esys_dc)
            subsubtables = [x for x in tmp_ls if x in set(schema_tables)]
            para_dc[table][subtable] = subtmp_dc
            if subsubtables:
                key_list = []
                for key in list(subtmp_dc.keys()):
                    if type(subtmp_dc[key]) is dict:
                        key_list.append(key)
            for subsubtable in subsubtables:
                if key_list:
                    for key in key_list:
                        subsubtmp_dc, tmp_ls = read_subtable(
                            basic_dc, subtmp_dc[key], subsubtable, esys_dc)
                        para_dc[table][subtable][key][subsubtable] = (
                            subsubtmp_dc)
                elif subtmp_dc:
                    subsubtmp_dc, tmp_ls = read_subtable(
                        basic_dc, subtmp_dc, subsubtable, esys_dc)
                    para_dc[table][subtable][subsubtable] = subsubtmp_dc
                elif not subtmp_dc:
                    tmp_ls = []
                if [x for x in tmp_ls if x in set(schema_tables)]:
                    logging.warning('Too many levels in database')
    logging.debug('Parameter set is read')
