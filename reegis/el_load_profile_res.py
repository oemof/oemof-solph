#!/usr/bin/python
# -*- coding: utf-8

'''
This package serves the readout of an hourly residential electricity load
profile from a file or database for later use in the model. If no electricity
load profile exists it can be generated using the standardised load profiles
of the BDEW. In that case the annual electricity load is calculated using an
average demand per person (based on a statistic from the BDEW) and retrieving
the number of inhabitants in the specified region from the database.

use_case:
    'db' -- residential electricity load profile is retrieved from database
            further parameters needed:
                schema -- name of database schema
                table_name -- name of database table
                column name -- name of column in database table

    'file' -- residential electricity load profile is retrieved from a file
              further parameters needed:
                  filename -- name of data file with filename extension
                      (e.g. 'test.txt')
                  directory -- path to file
                  column_name -- heading of data column

    'slp_generation' -- residential electricity load profile is generated
                        using standardised load profiles from the BDEW
'''

import numpy as np
import database as db


def annual_el_demand_res(district):
    '''
    Calculates the annual electricity demand of residential houses based on
    an average annual demand and the number of inhabitants.
    '''
    # average demand per person
    ratio = {1: 0.37, 2: 0.36, 3: 0.18, 4: 0.09}
    demand = {1: 2050, 2: 1720, 3: 1350, 4: 1235}
    demand_per_person = (ratio[1] * demand[1] + ratio[2] * demand[2] +
        ratio[3] * demand[3] + ratio[4] * demand[4])
    # number of inhabitants
    conn = db.open_db_connection()
    cur = conn.cursor()
    cur.execute('''
        select sum(o.einwohner)
        from wittenberg.orte_landkreis_wittenberg as o,
            wittenberg.gemeinden as g
        where st_contains(g.the_geom, o.the_geom)
            and g.stadtname=%(str)s
    ''', {'str': district})
    inhabitants = cur.fetchone()
    cur.close()
    conn.close()

    return (float(inhabitants[0]) * demand_per_person / 1000)


def generate_load_profile(annual_el_demand):
    '''
    Calculates the hourly electricity load profile in MWh/h of a region.
    '''
    # generate load profiles
    slp = np.reshape(db.retrieve_from_db_table(
        'wittenberg', 'slp_strom', 'h_0_d', order='yes'), (-1, ))
    hourly_el_demand = slp / 1000 * annual_el_demand

    return hourly_el_demand


def get_hourly_el_load_profile(input_data, use_case,
    schema=None, table_name=None, column_name=None,
    filename=None, directory=None, save=None,
    save_to_table=None, save_to_column='res_el_load',
    annual_demand=None):
    '''
    Returns the hourly electricity load in MWh/h of a region. Depending on the
    chosen use case the electricity load profile is either retrieved from a
    file or database or generated using the standardised load profiles of the
    BDEW.
    '''
    # retrieve el load profile from the database
    if use_case == 'db':
        if db.table_exists(table_name):
            hourly_el_demand = db.retrieve_from_db_table(
                schema, table_name, column_name, order='yes')
            hourly_el_demand = np.reshape(hourly_el_demand, (-1, ))
        else:
            print (('Table to retrieve the residential elec. load profile ' +
            'does not exist.'))
    # retrieve el load profile from file
    elif use_case == 'file':
        hourly_el_demand = \
            db.read_profiles_from_file(filename, directory)[column_name]
        hourly_el_demand = np.reshape(hourly_el_demand, (-1, ))
    # calculate el load profile
    elif use_case == 'slp_generation':
        if not annual_demand:
            # calculate annual el demand
            annual_demand = \
                annual_el_demand_res(input_data['district'])
        # generate load profile
        hourly_el_demand = \
            generate_load_profile(annual_demand)
    else:
        print (('Electricity load profile cannot be generated because of ' +
        'invalid use case. The use case chosen was: %s' % use_case))

    # save results to db
    if save:
        if db.table_exists(save_to_table):
            db.save_results_to_db(
                schema, save_to_table, save_to_column, hourly_el_demand)
        else:
            # create output table and id column
            db.create_db_table(schema, save_to_table,
                save_to_column + ' real')
            stringi = '(1)'
            for i in range(2, 8761):
                stringi = stringi + ',(' + str(i) + ')'
            db.insert_data_into_db_table(schema, save_to_table, 'id', stringi)
            db.save_results_to_db(
                schema, save_to_table, save_to_column, hourly_el_demand)

    return hourly_el_demand