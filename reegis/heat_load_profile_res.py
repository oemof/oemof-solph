#!/usr/bin/python
# -*- coding: utf-8

'''
This package serves the readout of an hourly residential heat load profile
from a file or database for later use in the model. If no heat load profile
exists it can be generated using the standardised load profiles of the BDW.
In that case the annual heat load is calculated according to the Wärmeatlas
Baden-Württemberg.

use_case:
    'db' -- residential heat load profile is retrieved from database
            further parameters needed:
                schema -- name of database schema
                table_name -- name of database table
                column name -- name of column in database table

    'file' -- residential heat load profile is retrieved from a file
              further parameters needed:
                  filename -- name of data file with filename extension
                      (e.g. 'test.txt')
                  directory -- path to file
                  column_name -- heading of data column

    'slp_generation' -- residential heat load profile is generated following
                        the guidelines of the BDW
'''

import numpy as np
import database as db
import shlp_bdew


def annual_heat_demand_efh(district):
    '''
    Calculates the heat demand (heating and warm water) of single-family
    houses in the specified district in MWh/a according to the Wärmeatlas
    Baden-Württemberg.
    '''
    conn = db.open_db_connection()
    cur = conn.cursor()
    cur.execute('''
        select sum(a.waermeverbrauchsdichte_max *
            st_area(s.the_geom::geography) * 10^(-3))
        from wittenberg.gemeinden as gem, wittenberg.siedlungstypen_waerme as s
            left join wittenberg.siedlungstypen as a
                on s.siedlungstyp = a.siedlungstyp
        where st_contains ( gem.the_geom, s.the_geom ) = 't'
            and gem.stadtname = %(str)s
            and (s.siedlungstyp = 'ST1'
                or s.siedlungstyp = 'ST2'
                or s.siedlungstyp = 'ST3'
                or s.siedlungstyp = 'ST4'
                or s.siedlungstyp = 'ST0');
    ''', {'str': district})
    annual_heat_demand_efh = cur.fetchone()[0]
    cur.close()
    conn.close()

    return annual_heat_demand_efh


def annual_heat_demand_mfh(district):
    '''
    Calculates the heat demand (heating and warm water) of multy-family
    houses in the specified district in MWh/a according to the Wärmeatlas
    Baden-Württemberg.
    '''
    conn = db.open_db_connection()
    cur = conn.cursor()
    cur.execute('''
        select sum(a.waermeverbrauchsdichte_max *
            st_area(s.the_geom::geography) * 10^(-3))
        from wittenberg.gemeinden as gem, wittenberg.siedlungstypen_waerme as s
            left join wittenberg.siedlungstypen as a
                on s.siedlungstyp = a.siedlungstyp
        where st_contains ( gem.the_geom, s.the_geom ) = 't'
            and gem.stadtname = %(str)s
            and (s.siedlungstyp = 'ST5a'
                or s.siedlungstyp = 'ST5b'
                or s.siedlungstyp = 'ST6'
                or s.siedlungstyp = 'ST7'
                or s.siedlungstyp = 'ST9');
    ''', {'str': district})
    annual_heat_demand_mfh = cur.fetchone()[0]
    cur.close()
    conn.close()

    return annual_heat_demand_mfh


def get_hourly_heat_load_profile(input_data, use_case, res_type,
    schema=None, table_name=None, column_name=None,
    filename=None, directory=None, save=None,
    save_to_table=None, save_to_column='res_heat_load',
    annual_demand=None):
    '''
    Returns the hourly heat load in MWh/h of a region. Depending on the
    chosen use case the heat load profile is either retrieved from a file or
    database or generated using the standardised load profiles of the BDEW.
    '''
    # retrieve heat load profile from the database
    if use_case == 'db':
        print schema, table_name, column_name
        if db.table_exists(table_name):
            hourly_heat_demand = db.retrieve_from_db_table(
                schema, table_name, column_name, order='yes')
            hourly_heat_demand = np.reshape(hourly_heat_demand, (-1, ))
        else:
            print (('Table to retrieve the residential heat load profile ' +
            'does not exist.'))
    # retrieve heat load profile from file
    elif use_case == 'file':
        hourly_heat_demand = \
            db.read_profiles_from_file(filename, directory)[column_name]
        hourly_heat_demand = np.reshape(hourly_heat_demand, (-1, ))
    # calculate heat load profile
    elif use_case == 'slp_generation':
        if not annual_demand:
            # calculate annual heat demand
            annual_demand = {}
            annual_demand[res_type] = \
                annual_heat_demand_efh(input_data['district'])
        # generate load profile
        res_hourly_heat_demand, com_hourly_heat_demand = \
            shlp_bdew.generate_load_profile(input_data, annual_demand)
        hourly_heat_demand = res_hourly_heat_demand

    else:
        print (('Heat load profile cannot be generated because of invalid ' +
        'use case. The use case chosen was: %s' % use_case))

    # save results to db
    if save:
        if db.table_exists(save_to_table):
            db.save_results_to_db(
                schema, save_to_table, save_to_column, hourly_heat_demand)
        else:
            # create output table and id column
            db.create_db_table(schema, save_to_table,
                save_to_column + ' real')
            stringi = '(1)'
            for i in range(2, 8761):
                stringi = stringi + ',(' + str(i) + ')'
            db.insert_data_into_db_table(schema, save_to_table, 'id', stringi)
            db.save_results_to_db(
                schema, save_to_table, save_to_column, hourly_heat_demand)

    return hourly_heat_demand