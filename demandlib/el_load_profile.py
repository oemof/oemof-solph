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
import matplotlib.pyplot as plt
import logging
import pandas as pd
from datetime import time as settime
from oemof.dblib import read_data_pg as rdb


def all_bdew_load_profiles(main_dt, time_df, slp_type=None, periods=None):
    '''
    Calculates the hourly electricity load profile in MWh/h of a region.
    '''
    if slp_type is None:
        slp_type = ['h0', 'g0', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'l0', 'l1',
                    'l2']
    if periods is None:
        periods = {
            'summer1': [5, 15, 9, 14],  # summer: 15.05. to 14.09
            'transition1': [3, 21, 5, 14],  # transition1 :21.03. to 14.05
            'transition2': [9, 15, 10, 31],  # transition2 :15.09. to 31.10
            'winter1': [1, 1, 3, 20],  # winter1:  01.01. to 20.03
            'winter2': [11, 1, 12, 31],  # winter2: 01.11. to 31.12
            }

    # Write values from the data base to a DataFrame
    # The dates are not real dates but helpers to calculate the mean values
    tmp_df = pd.DataFrame(rdb.fetch_columns(
        main_dt['basic'], 'demand', 'selp_series',
        columns=['period', 'weekday'] + slp_type, as_np=True, orderby='id',
        close=True), index=pd.date_range(pd.datetime(2007, 1, 1, 0),
                                         periods=2016, freq='15Min'))

    # Convert decimal values to floats
    tmp_df[slp_type] = tmp_df[slp_type].astype(float)

    # Create a new DataFrame to collect the results
    new_df = time_df.copy()

    # Create an empty column for all slp types and calculate the hourly mean
    how = {'period': 'last', 'weekday': 'last'}
    for typ in slp_type:
        new_df[typ] = 0
        how[typ] = 'mean'
    tmp_df = tmp_df.resample('H', how=how)

    # Inner join the slps on the time_df to the slp's for a whole year
    tmp_df['hour_of_day'] = tmp_df.index.hour + 1
    left_cols = ['hour_of_day', 'weekday']
    right_cols = ['hour', 'weekday']
    tmp_df = tmp_df.reset_index()
    tmp_df.pop('index')

    for p in periods.keys():
        a = pd.datetime(main_dt['year'], periods[p][0], periods[p][1], 0, 0)
        b = pd.datetime(main_dt['year'], periods[p][2], periods[p][3], 23, 59)
        new_df.update(pd.DataFrame.merge(
            tmp_df[tmp_df['period'] == p[:-1]], time_df[a:b],
            left_on=left_cols, right_on=right_cols,
            how='inner', left_index=True).sort().drop(['hour_of_day'], 1))

    # Add the slp for the industrial group
    new_df['i0'] = simple_industrial_heat_profile(time_df)
    return new_df


def simple_industrial_heat_profile(df):
    ''

    # TODO: Remove the hard coded values
    am = settime(7, 0, 0)
    pm = settime(23, 30, 0)

    df['ind'] = 0

    # Day(am to pm), night (pm to am), week day (week), weekend day (weekend)
    week = [1, 2, 3, 4, 5]
    weekend = [0, 6, 7]

    df['ind'].mask(df['weekday'].between_time(am, pm).isin(week), 0.8, True)
    df['ind'].mask(df['weekday'].between_time(pm, am).isin(week), 0.6, True)
    df['ind'].mask(df['weekday'].between_time(am, pm).isin(weekend), 0.9, True)
    df['ind'].mask(df['weekday'].between_time(pm, am).isin(weekend), 0.7, True)

    if df['ind'].isnull().any(axis=0):
        logging.error('NAN value found in industrial load profile')
    return df.pop('ind')


def create_slp(main_dt, year, reg, slp_df, parameter):
    ''
    # Normalize the slp and multiply it with the annual demand
    main_dt['timeseries']['demand'][reg]['elec_demand'][
        parameter['selp_type']] = (
            slp_df[parameter['selp_type']]
            / slp_df[parameter['selp_type']].sum(0)
            * parameter['annual_elec_demand'])

    # Add the calculated load profile to the summery column
    main_dt['timeseries']['demand'][reg]['elec_demand']['all'] += main_dt[
        'timeseries']['demand'][reg]['elec_demand'][parameter['selp_type']]


def generate_elec_load_profile(main_dt, time_df, reg, year):
    '''
    This function calculates the hourly heat demand of the different
    residential and commercial types as a function of the maximum heat demand,
    the wind and building class and the given temperature profile.
    '''
    # Set holidays (weekday=0) to sundays (weekday=7).
    time_df['weekday'].mask(time_df['weekday'] == 0, 7, True)

    # Create DataFrame with the index of time_df and one column ('all')
    main_dt['timeseries']['demand'][reg]['elec_demand'] = time_df.drop(
        list(time_df.keys()), 1)
    main_dt['timeseries']['demand'][reg]['elec_demand']['all'] = 0

    # generate a DateFrame with all  slp-Types
    slp_df = all_bdew_load_profiles(main_dt, time_df)

    # Calculate the load profile for all groups from the slp's.
    for group in main_dt['parameter']['building'][reg].keys():
        create_slp(main_dt, year, reg, slp_df,
                   main_dt['parameter']['building'][reg][group])
