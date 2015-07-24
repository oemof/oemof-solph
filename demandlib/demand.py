#!/usr/bin/python
# -*- coding: utf-8

'''Create demand series for heat and electricity'''

import logging
import pandas as pd
from . import holiday
from . import shlp_bdew as heat
from . import el_load_profile as elec


def create_basic_dataframe(year, region):
    '''Create a basic hourly dataframe for the given year.'''

    # Create a temporary DataFrame to calculate the heat demand
    time_df = pd.DataFrame(
        index=pd.date_range(
            pd.datetime(year, 1, 1, 0), periods=8760, freq='H'),
        columns=['weekday', 'hour', 'date'])
    holidays = holiday.get_german_holidays(
        year, place=holiday.fetch_admin_from_latlon(coord=region['centroid']))

    # Add a column 'hour of the day to the DataFrame
    time_df['hour'] = time_df.index.hour + 1
    time_df['weekday'] = time_df.index.weekday + 1
    time_df['date'] = time_df.index.date

    # Set weekday to Holiday (0) for all holidays
    time_df['weekday'].mask(pd.to_datetime(time_df['date']).isin(
        pd.to_datetime(list(holidays.keys()))), 0, True)

    return time_df


def generate_heat_load_profiles(main_dt):
    '''Generate a load profile for the given year with hourly values'''
    logging.debug('Generate standard load profiles according to BDEW.')
    for reg in list(main_dt['parameter']['building'].keys()):
        time_df = create_basic_dataframe(main_dt['year'], main_dt[reg])
        heat.generate_bdew_load_profile(main_dt, time_df, reg, main_dt['year'])


def generate_elec_load_profiles(main_dt):
    ''
    for reg in list(main_dt['parameter']['building'].keys()):
        time_df = create_basic_dataframe(main_dt['year'], main_dt[reg])
        elec.generate_elec_load_profile(main_dt, time_df, reg, main_dt['year'])
