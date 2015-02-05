#!/usr/bin/python
# -*- coding: utf-8

'''
This package serves the readout of an hourly commercial heat load
profile from a file or database for later use in the model. If no heat
load profile exists it can be generated using the standardised load profiles
of the BDW. In that case the annual heat load needs to be handed over
as an input parameter.

use_case:
    'db' -- commercial heat load profile is retrieved from database
            further parameters needed:
                schema -- name of database schema
                table_name -- name of database table
                column name -- name of column in database table

    'file' -- commercial heat load profile is retrieved from a file
              further parameters needed:
                  filename -- name of data file with filename extension
                      (e.g. 'test.txt')
                  directory -- path to file
                  column_name -- heading of data column

    'slp_generation' -- commercial heat load profile is generated
                        using standardised load profiles from the BDW
                        further parameters needed:
                          annual_heat_load -- commercial annual heat load
                                              [MWh/year]
'''

import numpy as np
import database as db
import shlp_bdew


def get_hourly_heat_load_profile(input_data, use_case,
    schema=None, table_name=None, column_name=None,
    filename=None, directory=None, save=None, annual_demand=None,
    save_to_table=None, save_to_column='com_heat_load'):
    '''
    Returns the hourly heat load in MWh/h of a region. Depending on the
    chosen use case the heat load profile is either retrieved from a
    file or database or generated using the standardised load profiles of the
    BDEW.
    '''
    # retrieve heat load profile from the database
    if use_case == 'db':
        if db.table_exists(table_name):
            hourly_heat_demand = db.retrieve_from_db_table(
                schema, table_name, column_name, order='yes')
            hourly_heat_demand = np.reshape(hourly_heat_demand, (-1, ))
        else:
            print (('Table to retrieve the commercial heat load profile ' +
            'does not exist.'))
    # retrieve heat load profile from file
    elif use_case == 'file':
        hourly_heat_demand = \
            db.read_profiles_from_file(filename, directory)[column_name]
        hourly_heat_demand = np.reshape(hourly_heat_demand, (-1, ))
    # calculate heat load profile
    elif use_case == 'slp_generation':
        # generate load profile
        annual_heat_demand = {}
        annual_heat_demand['GHD'] = annual_demand
        res_hourly_heat_demand, com_hourly_heat_demand = \
            shlp_bdew.generate_load_profile(
                input_data, annual_heat_demand)
        hourly_heat_demand = com_hourly_heat_demand
    else:
        print (('Heat load profile cannot be generated because of ' +
        'invalid use case. The use case chosen was: %s' % use_case))

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