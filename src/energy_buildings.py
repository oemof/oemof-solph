# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 12:04:21 2015

@author: uwe
"""
from matplotlib import pyplot as plt
import db
import holiday
import logging
import pandas as pd
from datetime import time as settime


class electric_building():
    ''

    def __init__(self, bdew=None, **kwargs):
        # slp is of type bdew_elec_slp!
        self.__elec_demand__ = (
            bdew.slp[kwargs['selp_type']] /
            bdew.slp[kwargs['selp_type']].sum(0) *
            kwargs['annual_elec_demand'])

    @property
    def load(self):
        return self.__elec_demand__


class heat_building():
    ''
    pass


class bdew_elec_slp():
    'Generate electrical standardized load profiles based on the BDEW method.'

    def __init__(self, year, time_df, periods=None):
        if periods is None:
            self.__periods__ = {
                'summer1': [5, 15, 9, 14],  # summer: 15.05. to 14.09
                'transition1': [3, 21, 5, 14],  # transition1 :21.03. to 14.05
                'transition2': [9, 15, 10, 31],  # transition2 :15.09. to 31.10
                'winter1': [1, 1, 3, 20],  # winter1:  01.01. to 20.03
                'winter2': [11, 1, 12, 31],  # winter2: 01.11. to 31.12
                }
        else:
            self.__periods__ = periods

        self.__year__ = year
        self.__time_df__ = time_df
        self.__slp_frame__ = self.all_load_profiles()

    def all_load_profiles(self):
        slp_types = ['h0', 'g0', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'l0',
                     'l1', 'l2']
        new_df = self.create_bdew_load_profiles(slp_types)

        # Add the slp for the industrial group
        new_df['i0'] = self.simple_industrial_heat_profile(self.__time_df__)

        new_df.drop(['hour', 'weekday'], 1, inplace=True)
        # TODO: Gleichmäßig normalisieren der i0-Lastgang hat höhere
        # Jahressumme als die anderen.
        return new_df

    def create_bdew_load_profiles(self, slp_types):
        '''
        Calculates the hourly electricity load profile in MWh/h of a region.
        '''

        # Write values from the data base to a DataFrame
        # The dates are not real dates but helpers to calculate the mean values
        tmp_df = pd.read_sql_table(
            table_name='selp_series', con=db.db_engine(), schema='demand',
            columns=['period', 'weekday'] + slp_types)
        tmp_df.set_index(pd.date_range(pd.datetime(2007, 1, 1, 0),
                                       periods=2016, freq='15Min'),
                         inplace=True)

        # Create a new DataFrame to collect the results
        time_df = self.__time_df__

        # All holidays(0) are set to sunday(7)
        time_df.weekday = self.__time_df__.weekday.replace(0, 7)
        new_df = time_df.copy()

        # Create an empty column for all slp types and calculate the hourly
        # mean.
        how = {'period': 'last', 'weekday': 'last'}
        for slp_type in slp_types:
            new_df[slp_type] = 0
            how[slp_type] = 'mean'
        tmp_df = tmp_df.resample('H', how=how)

        # Inner join the slps on the time_df to the slp's for a whole year
        tmp_df['hour_of_day'] = tmp_df.index.hour + 1
        left_cols = ['hour_of_day', 'weekday']
        right_cols = ['hour', 'weekday']
        tmp_df = tmp_df.reset_index()
        tmp_df.pop('index')

        for p in self.__periods__.keys():
            a = pd.datetime(self.__year__, self.__periods__[p][0],
                            self.__periods__[p][1], 0, 0)
            b = pd.datetime(self.__year__, self.__periods__[p][2],
                            self.__periods__[p][3], 23, 59)
            new_df.update(pd.DataFrame.merge(
                tmp_df[tmp_df['period'] == p[:-1]], time_df[a:b],
                left_on=left_cols, right_on=right_cols,
                how='inner', left_index=True).sort().drop(['hour_of_day'], 1))

        return new_df

    def simple_industrial_heat_profile(self, df):
        ''

        # TODO: Remove the hard coded values
        am = settime(7, 0, 0)
        pm = settime(23, 30, 0)

        df['ind'] = 0

        # Day(am to pm), night (pm to am), week day (week),
        # weekend day (weekend)
        week = [1, 2, 3, 4, 5]
        weekend = [0, 6, 7]

        df['ind'].mask(df['weekday'].between_time(am, pm).isin(week), 0.8,
                       True)
        df['ind'].mask(df['weekday'].between_time(pm, am).isin(week), 0.6,
                       True)
        df['ind'].mask(df['weekday'].between_time(am, pm).isin(weekend), 0.9,
                       True)
        df['ind'].mask(df['weekday'].between_time(pm, am).isin(weekend), 0.7,
                       True)

        if df['ind'].isnull().any(axis=0):
            logging.error('NAN value found in industrial load profile')
        return df.pop('ind')

    @property
    def slp(self):
        return self.__slp_frame__


def create_basic_dataframe(year, place):
    '''This function is just for testing later on the dataframe is passed.'''

    # Create a temporary DataFrame to calculate the heat demand
    time_df = pd.DataFrame(
        index=pd.date_range(
            pd.datetime(year, 1, 1, 0), periods=8760, freq='H'),
        columns=['weekday', 'hour', 'date'])

    holidays = holiday.get_german_holidays(year, place)

    # Add a column 'hour of the day to the DataFrame
    time_df['hour'] = time_df.index.hour + 1
    time_df['weekday'] = time_df.index.weekday + 1
    time_df['date'] = time_df.index.date
    time_df['elec'] = 0
    time_df['heat'] = 0

    # Set weekday to Holiday (0) for all holidays
    time_df['weekday'].mask(pd.to_datetime(time_df['date']).isin(
        pd.to_datetime(list(holidays.keys()))), 0, True)
    return time_df


if __name__ == "__main__":
    year = 2007
    define_buildings = [
        {'annual_elec_demand': 2000,
         'selp_type': 'h0'},
        {'annual_elec_demand': 2000,
         'selp_type': 'g0'},
        {'annual_elec_demand': 3000,
         'selp_type': 'i0'}]

    time_df = create_basic_dataframe(year, ['Deutschland', 'ST'])

    a = bdew_elec_slp(year, time_df)

    buildings = []
    for building_def in define_buildings:
        buildings.append(electric_building(bdew=a, **building_def))

    for building in buildings:
        building.load.plot()
    plt.show()
