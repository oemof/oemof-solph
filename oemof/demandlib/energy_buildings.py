# -*- coding: utf-8 -*-
"""

"""
import logging
import pandas as pd
from datetime import time as settime
import os

class Building():
    """
    """

    def __init__(self, **kwargs):
        """
        """
        self.annual_heat_demand = kwargs.get('annual_heat_demand')

    def hourly_heat_demand(self, fun=None, **kwargs):
        """
        Calculate hourly heat demand

        Parameters
        ----------

        self : building object
        fun : python function
           function to use for heat demand calculation
        kwargs : additional arguments
           arguments to use in fun
        """
        if not kwargs.get("annual_heat_demand"):
            try:
                kwargs["annual_heat_demand"] = self.annual_heat_demand
            except:
                raise ValueError("Missing annual heat demand!")

        hourly_heat_demand = fun(**kwargs)

        return hourly_heat_demand


class bdew_elec_slp():
    'Generate electrical standardized load profiles based on the BDEW method.'

    def __init__(self, time_df, periods=None):
        if periods is None:
            self.periods = {
                'summer1': [5, 15, 9, 14],  # summer: 15.05. to 14.09
                'transition1': [3, 21, 5, 14],  # transition1 :21.03. to 14.05
                'transition2': [9, 15, 10, 31],  # transition2 :15.09. to 31.10
                'winter1': [1, 1, 3, 20],  # winter1:  01.01. to 20.03
                'winter2': [11, 1, 12, 31],  # winter2: 01.11. to 31.12
                }
        else:
            self.periods = periods
        self._year = time_df.index.year[1000]
        self.slp_frame = self.all_load_profiles(time_df)

    def all_load_profiles(self, time_df):
        slp_types = ['h0', 'g0', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'l0',
                     'l1', 'l2']
        new_df = self.create_bdew_load_profiles(time_df, slp_types)

        # Add the slp for the industrial group
        new_df['i0'] = self.simple_industrial_heat_profile(time_df)

        new_df.drop(['hour', 'weekday'], 1, inplace=True)
        # TODO: Gleichmäßig normalisieren der i0-Lastgang hat höhere
        # Jahressumme als die anderen.
        return new_df

    def create_bdew_load_profiles(self, time_df, slp_types):
        '''
        Calculates the hourly electricity load profile in MWh/h of a region.
        '''

        # define file path of slp csv data
        self.datapath = os.path.join(os.path.dirname(__file__), 'bdew_data')
        file_path = os.path.join(self.datapath, 'selp_series.csv')

        # Read standard load profile series from csv file
        selp_series = pd.read_csv(file_path)
        tmp_df = selp_series

        index = pd.date_range(
                pd.datetime(2007, 1, 1, 0), periods=2016, freq='15Min')
                # columns=['period', 'weekday'] + slp_types)

        tmp_df.set_index(index, inplace=True)

        # All holidays(0) are set to sunday(7)
        time_df.weekday = time_df.weekday.replace(0, 7)
        new_df = time_df.copy()

        # Create an empty column for all slp types and calculate the hourly
        # mean.
        how = {'period': 'last', 'weekday': 'last'}
        for slp_type in slp_types:
            tmp_df[slp_type] = tmp_df[slp_type].astype(float)
            new_df[slp_type] = 0
            how[slp_type] = 'mean'
        tmp_df = tmp_df.groupby(pd.TimeGrouper(freq='H')).agg(how)

        # Inner join the slps on the time_df to the slp's for a whole year
        tmp_df['hour_of_day'] = tmp_df.index.hour + 1
        left_cols = ['hour_of_day', 'weekday']
        right_cols = ['hour', 'weekday']
        tmp_df = tmp_df.reset_index()
        tmp_df.pop('index')

        for p in self.periods.keys():
            a = pd.datetime(self._year, self.periods[p][0],
                            self.periods[p][1], 0, 0)
            b = pd.datetime(self._year, self.periods[p][2],
                            self.periods[p][3], 23, 59)
            new_df.update(pd.DataFrame.merge(
                tmp_df[tmp_df['period'] == p[:-1]], time_df[a:b],
                left_on=left_cols, right_on=right_cols,
                how='inner', left_index=True).sort_index().drop(['hour_of_day'], 1))

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
        return self.slp_frame

    @property
    def year(self):
        return self._year
