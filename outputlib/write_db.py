#!/usr/bin/python
# -*- coding: utf-8

'''
Author: Caroline Möller (caro.moeller@rl-institut.de)
Changes by: Uwe Krien (uwe.krien@rl-institut.de)
Responsibility: Uwe Krien (uwe.krien@rl-institut.de)
'''

import dblib as db
import logging
import pulp as pulp
import numpy as np

# Definition of the column names for typical columns
# Changes here might cause errors, writing data to existing tables
id_col = 'id'  # column for the scenario-id in the result tables
timestep_col = 'timestep'  # column for the timestep
region_col = 'region'  # column for the name of the region


def add_column(table, i, col_type, db_string):
    '''
    [Description]

    [Autor]

    Parameters

    Keyword arguments

    Returns
    '''
    tmp_string = 'ALTER TABLE %s ADD COLUMN "%s" %s;' % (table, i, col_type)
    return db_string + tmp_string


def create_table(dic, schema, esy_tbname, colnames, is_series, with_regions,
        results):
    '''
    Creates a results table in a postgres database.
    This function can create results tables with single and series values.
    Table type is defined by the logical value 'is_series'.
    '''

    table = schema + '.' + esy_tbname

    # create table
    if is_series:
        db_string = 'CREATE TABLE %s (%s numeric, %s numeric);' % (
            table, id_col, timestep_col)
    elif not is_series and with_regions:
        db_string = 'CREATE TABLE %s (%s numeric, %s varchar);' % (
            table, id_col, region_col)
    else:
        db_string = 'CREATE TABLE %s (%s numeric);' % (table, id_col)

    type_dc = {
        "<type 'str'>": 'varchar',
        "<type 'int'>": 'integer',
        "<type 'float'>": 'real',
        "<type 'dict'>": 'real',
        "<type 'datetime.datetime'>": 'timestamp',
        "<class 'pulp.pulp.LpVariable'>": 'real'
        }
    # add columns (components)
    for i in colnames:
        col_type = type_dc[str(type(results[i]))]
        db_string = add_column(table, i, col_type, db_string)

    # add column 'region' if series-table
    if is_series and with_regions:
        db_string = add_column(table, region_col, 'varchar', db_string)

    db.execute_write_db(dic, db_string)


def create_insert_string(table, sql_data, columns):
    '''
    [Description]

    [Autor]

    Parameters

    Keyword arguments

    Returns
    '''
    cols = str(tuple(columns)).replace("'", "\"")
    return ('INSERT INTO %s %s VALUES %s ; ' % (table, cols, tuple(sql_data)))


def write_series_with_regions(scenario_id, timesteps, colnames, data,
        stringdb, table, regionnames, timestep_start):
    '''
    [Description]

    [Autor]

    Parameters

    Keyword arguments

    Returns
    '''
    for r in regionnames:
        for t in timesteps:
            hoy = t + timestep_start + 1
            sql_data = [scenario_id, hoy, r]
            col_data = [id_col, timestep_col, region_col]
            for i in colnames:
                col_data.append(i)
                if type(data[i][t][r]) is (
                    pulp.pulp.LpVariable):
                    sql_data.append(data[i][t][r].varValue)
                elif type(data[i][t][r]) is float:
                    sql_data.append(data[i][t][r])
                elif type(data[i][t][r]) is np.float64:
                    sql_data.append(data[i][t][r])
                else:
                    logging.warning(
                        'Unknown data type: {0}. Try to write it'.format(
                            type(data[i][t][r])))
                    sql_data.append(data[i][t][r])
            stringdb = stringdb + (
                create_insert_string(table, sql_data, col_data))
    return stringdb


def write_series_without_regions(scenario_id, timesteps, colnames, data,
        stringdb, table, timestep_start):
    '''
    [Description]

    [Autor]

    Parameters

    Keyword arguments

    Returns
    '''
    for t in timesteps:
        hoy = t + timestep_start + 1
        sql_data = [scenario_id, hoy]
        col_data = [id_col, timestep_col]
        for i in colnames:
            col_data.append(i)
            if type(data[i][t]) is pulp.pulp.LpVariable:
                sql_data.append(data[i][t].varValue)
            elif type(data[i][t]) is float:
                sql_data.append(data[i][t])
            else:
                logging.warning('Unknown data type. Try to write it')
                sql_data.append(data[i][t])
        stringdb = stringdb + (
            create_insert_string(table, sql_data, col_data))
    return stringdb


def write_rows_with_regions(scenario_id, colnames, data, stringdb, table,
        regionnames):
    '''
    [Description]

    [Autor]

    Parameters

    Keyword arguments

    Returns
    '''
    for r in regionnames:
        sql_data = [scenario_id, r]
        col_data = [id_col, region_col]
        for i in colnames:
            col_data.append(i)
            if type(data[i][r]) is pulp.pulp.LpVariable:
                sql_data.append(data[i][r].varValue)
            elif type(data[i][r]) is float:
                sql_data.append(data[i][r])
            else:
                logging.warning('Unknown data type. Try to write it')
                sql_data.append(data[i][r])
        stringdb = stringdb + (
            create_insert_string(table, sql_data, col_data))
    return stringdb


def write_rows_without_regions(scenario_id, colnames, data, stringdb, table):
    '''
    [Description]

    [Autor]

    Parameters

    Keyword arguments

    Returns
    '''
    sql_data = [scenario_id]
    col_data = [id_col]
    for i in colnames:
        col_data.append(i)
        if type(data[i]) is pulp.pulp.LpVariable:
            sql_data.append(data[i].varValue)
        elif type(data[i]) in [float, int, str, bool]:
            sql_data.append(data[i])
        elif data[i] is None and table.split('.')[1] == 'info':
            sql_data.append(str(data[i]))
        else:
            logging.warning('Unknown data type: %s. Try to write it1' % (
                type(data[i])))
            sql_data.append(data[i])
    stringdb = stringdb + (
        create_insert_string(table, sql_data, col_data))
    return stringdb


def write_results(dic, schema, esy_tbname, timesteps, colnames, regionnames,
        is_series, scenario_id, data, with_regions, timestep_start):
    '''
    Writes data to existing tables in a postgres database.
    This function can write into tables for single and series results values.
    Table type is defined by the logical value 'is_series'.
    '''

    table = schema + '.' + esy_tbname
    stringdb = ''
    logging.debug('%s' % (esy_tbname))
    logging.debug('%s' % (str(colnames)))
    if is_series:
        if with_regions:
            stringdb = write_series_with_regions(scenario_id, timesteps,
                colnames, data, stringdb, table, regionnames, timestep_start)
            logging.debug('%s' % (str(regionnames)))
        else:
            stringdb = write_series_without_regions(scenario_id, timesteps,
                colnames, data, stringdb, table, timestep_start)
    else:
        if with_regions:
            stringdb = write_rows_with_regions(scenario_id, colnames, data,
                stringdb, table, regionnames)
            logging.debug('%s' % (str(regionnames)))
        else:
            stringdb = write_rows_without_regions(scenario_id, colnames, data,
                stringdb, table)
    if stringdb.find('None') > 0 and esy_tbname != 'info':
        logging.error(stringdb)
        logging.error(
            "'None' string found in the database string on position {0}"
            .format(stringdb.find('None')))
        stringdb = stringdb.replace('None', str(0))
    db.execute_write_db(dic, stringdb)
    return