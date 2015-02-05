#!/usr/bin/python
# -*- coding: utf-8

import numpy as np
import database as db
import plot_lists


def retrieve_data(schema, results_table, week=None, nod=None):
    '''
    Retrieve data from database.
    '''

    # open connection to the database
    conn = db.open_db_connection()
    cur = conn.cursor()

    # read the names of the columns of the solver output table
    cur.execute('''SELECT column_name FROM information_schema.columns
                WHERE table_name = '%s';''' % results_table)
    colnames = np.asarray(cur.fetchall())

    # read data for the given week (and the following) from the solver
    # output table
    table = schema + '.' + results_table
    sql_string = 'SELECT * FROM %s' % table
    if week:
        sql_string += (' ORDER BY id LIMIT %s OFFSET %s'
        % (nod * 24, (week - 1) * 168))
    cur.execute('%s' % sql_string)
    #cur.execute('''
                #SELECT * FROM %s ORDER BY id LIMIT %s OFFSET %s
                #''' % (table, number_of_days * 24, (week - 1) * 168))
    data = np.asarray(cur.fetchall())

    cur.close()
    conn.close()

    return colnames, data


def retrieve_in_data(schema, load_table, week, number_of_days):
    '''
    Retrieve data from database.
    '''

    # open connection to the database
    conn = db.open_db_connection()
    cur = conn.cursor()

    # read the names of the columns of the load and potential table
    cur.execute('''SELECT column_name FROM information_schema.columns
                WHERE table_name = '%s';''' % load_table)
    colnames_in = np.asarray(cur.fetchall())

    # read data for the given week (and the following) from the load and
    # potential table
    table = schema + '.' + load_table
    cur.execute('''
                SELECT * FROM %s ORDER BY id LIMIT %s OFFSET %s
                ''' % (table, number_of_days * 24, (week - 1) * 168))
    in_data = np.asarray(cur.fetchall())

    cur.close()
    conn.close()

    return colnames_in, in_data


def el_heating_exists(results_table):
    '''
    Checks, if any electrical heating systems are used in the model.
    '''
    # get list with all electrical heating systems used in the model
    el_heating_sys = plot_lists.get_list_el_heating(results_table)

    el_heating = False
    if len(el_heating_sys) > 0:
        el_heating = True

    return el_heating


def append_colname(colnames_orig, colname_entry):
    '''
    Appends a new column name to the column names vector.
    '''
    colnames = np.chararray((
        colnames_orig.shape[0] + 1, colnames_orig.shape[1]),
        itemsize=colnames_orig.itemsize)
    colnames[0: colnames_orig.shape[0]] = colnames_orig
    colnames[-1] = colname_entry
    return colnames


def append_fee_column(data_orig, colnames):
    '''
    Appends a column to the data matrix where pv and wind energy are summed up.
    '''
    # initialize data matrix
    data = np.ones((data_orig.shape[0], data_orig.shape[1] + 1))

    # write original data to data matrix and colnames vector
    data[:, 0: data_orig.shape[1]] = data_orig

    # add column with sum of wind and PV energy to data matrix
    pv_energy = ([i for i, x in enumerate(colnames) if x == 'PV'])
    wind_energy = ([i for i, x in enumerate(colnames) if x == 'Wind'])
    data[:, -1] = (data_orig[:, pv_energy] + data_orig[:, wind_energy])[:, 0]

    return data


def append_el_heating_column(data_orig, colnames, results_table):
    '''
    Appends a column to the data matrix where all electrical heating
    systems are summed up.
    '''

    # initialize data matrix
    data = np.ones((data_orig.shape[0], data_orig.shape[1] + 1))

    # write original data to data matrix
    data[:, 0: data_orig.shape[1]] = data_orig

    # get list with all electrical heating systems used in the model
    el_heating_sys = plot_lists.get_list_el_heating(results_table)

    # sum of electric heating
    data_el_heating = np.zeros((data_orig.shape[0], ))
    for el_heating in el_heating_sys:
        tmp = ([i for i, x in enumerate(colnames) if x == el_heating])
        data_el_heating += data_orig[:, tmp[0]]
    # add column with sum of el heating to data matrix
    data[:, -1] = data_el_heating

    return data


def get_stack(p_set):
    # summer data
    [colnames, data_summer] = retrieve_data(
        p_set['schema'], p_set['output_table'], p_set['week_summer'], 7)
    [colnames_in, in_data_summer] = retrieve_in_data(
        p_set['schema'], p_set['load_pot_table'], p_set['week_summer'], 7)
    # winter data
    [colnames, data_winter] = retrieve_data(
        p_set['schema'], p_set['output_table'], p_set['week_winter'], 7)
    [colnames_in, in_data_winter] = retrieve_in_data(
        p_set['schema'], p_set['load_pot_table'], p_set['week_winter'], 7)
    # add FEE column to data matrix
    data_summer = append_fee_column(data_summer, colnames)
    data_winter = append_fee_column(data_winter, colnames)
    colnames = append_colname(colnames, 'FEE')
    # add el heating column to data matrix (if exists)
    if el_heating_exists(p_set['output_table']) is True:
        data_summer = append_el_heating_column(
            data_summer, colnames, p_set['output_table'])
        data_winter = append_el_heating_column(
            data_winter, colnames, p_set['output_table'])
        colnames = append_colname(colnames, 'Sum el Heating')
    return (data_summer, data_winter, in_data_summer, in_data_winter,
        colnames, colnames_in)


def get_pie(p_set):
    # summer data
    [colnames, data] = retrieve_data(
        p_set['schema'], p_set['output_table'])
    # add FEE column to data matrix
    data = append_fee_column(data, colnames)
    colnames = append_colname(colnames, 'FEE')
    # add el heating column to data matrix (if exists)
    if el_heating_exists(p_set['output_table']) is True:
        data = append_el_heating_column(data, colnames, p_set['output_table'])
        colnames = append_colname(colnames, 'Sum el Heating')
    return data, colnames