# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 12:04:21 2015

@author: uwe
"""
import numpy as np
import logging
import pandas as pd
import os
from math import ceil as round_up
from datetime import time as settime


class electric_building():
    ''

    def __init__(self, bdew=None, **kwargs):
        # slp is of type bdew_elec_slp!
        self.elec_demand = (
            bdew.slp[kwargs['selp_type']] /
            bdew.slp[kwargs['selp_type']].sum(0) *
            kwargs['annual_elec_demand'])
        self.type = kwargs['selp_type']
        self.annual_load = kwargs['annual_elec_demand']

    @property
    def load(self):
        return self.elec_demand


class HeatBuilding():
    ''
    def __init__(self, time_df, temp, **kwargs):
        self.datapath = os.path.join(os.path.dirname(__file__), 'data')
        self.year = time_df.index.year[1000]
        time_df['temp'] = (temp - 273)
        self.heat_demand = self.create_slp(time_df, **kwargs)
        self.type = kwargs['shlp_type']
        self.annual_load = kwargs['annual_heat_demand']

    def temp_geo_series(self, time_df):
        r'''
        A new temperature vector is generated containing a multy-day
        average temperature as needed in the load profile function.

        Notes
        -----
        Equation for the mathematical series of the average tempaerature [1]_:

        .. math::
            T=\frac{T_{t}+0.5\cdot T_{t-1}+0.25\cdot T_{t-2}+
                    0.125\cdot T_{t-3}}{1+0.5+0.25+0.125}

        with :math:`T_t` = Average temperature on the present day
             :math:`T_{t-1}` = Average temperature on the previous day ...

        References
        ----------
        .. [1] `BDEW <https://www.avacon.de/cps/rde/xbcr/avacon/15-06-30_Leitfaden_Abwicklung_SLP_Gas.pdf>`_, BDEW Documentation for heat profiles.
        '''
        tem = time_df['temp'].resample('D', how='mean').reindex(
            time_df.index).fillna(method="ffill")
        return (tem + 0.5 * np.roll(tem, 24) + 0.25 * np.roll(tem, 48) +
                0.125 * np.roll(tem, 72)) / 1.875

    def temp_interval(self, time_df):
        '''
        Appoints the corresponding temperature interval to each temperature in
        the temperature vector.
        '''
        temp = self.temp_geo_series(time_df)
        temp_dict = ({
            -20: 1, -19: 1, -18: 1, -17: 1, -16: 1, -15: 1, -14: 2,
            -13: 2, -12: 2, -11: 2, -10: 2, -9: 3, -8: 3, -7: 3, -6: 3, -5: 3,
            -4: 4, -3: 4, -2: 4, -1: 4, 0: 4, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5,
            6: 6, 7: 6, 8: 6, 9: 6, 10: 6, 11: 7, 12: 7, 13: 7, 14: 7, 15: 7,
            16: 8, 17: 8, 18: 8, 19: 8, 20: 8, 21: 9, 22: 9, 23: 9, 24: 9,
            25: 9, 26: 10, 27: 10, 28: 10, 29: 10, 30: 10, 31: 10, 32: 10,
            33: 10, 34: 10, 35: 10, 36: 10, 37: 10, 38: 10, 39: 10, 40: 10})
        temp_rounded = [round_up(i) for i in temp]
        temp_int = [temp_dict[i] for i in temp_rounded]
        return np.transpose(np.array(temp_int))

    def get_h_values(self, time_df, **kwargs):
        '''Determine the h-values'''
        file = os.path.join(self.datapath, 'shlp_hour_factors.csv')
        hour_factors = pd.read_csv(file, index_col=0)
        hour_factors = hour_factors.query(
            'building_class=={building_class} and shlp_type=="{shlp_type}"'
            .format(**kwargs))

        # Join the two DataFrames on the columns 'hour' and 'hour_of_the_day'
        # or ['hour' 'weekday'] and ['hour_of_the_day', 'weekday'] if it is
        # not a residential slp.
        residential = kwargs['building_class'] > 0

        left_cols = ['hour_of_day'] + (['weekday'] if not residential else [])
        right_cols = ['hour'] + (['weekday'] if not residential else [])

        SF_mat = pd.DataFrame.merge(
            hour_factors, time_df, left_on=left_cols, right_on=right_cols,
            how='outer', left_index=True).sort().drop(
            left_cols + right_cols, 1)

        # Determine the h values
        h = np.array(SF_mat)[np.array(range(0, 8760))[:], (
            self.temp_interval(time_df) - 1)[:]]
        return np.array(list(map(float, h[:])))

    def get_sigmoid_parameter(self, **kwargs):
        ''' Retrieve the sigmoid parameters from the database'''
        file = os.path.join(self.datapath, 'shlp_sigmoid_factors.csv')
        sigmoid = pd.read_csv(file, index_col=0)
        sigmoid = sigmoid.query(
            'building_class=={building_class} and '.format(**kwargs) +
            'shlp_type=="{shlp_type}" and '.format(**kwargs) +
            'wind_impact=={wind_class}'.format(**kwargs))

        A = float(sigmoid['parameter_a'])
        B = float(sigmoid['parameter_b'])
        C = float(sigmoid['parameter_c'])
        D = float(sigmoid['parameter_d']) if kwargs.get(
            'ww_incl', True) else 0
        return A, B, C, D

    def get_weekday_parameter(self, time_df, **kwargs):
        ''' Retrieve the weekdayparameter from the database'''
        file = os.path.join(self.datapath, 'shlp_weekday_factors.csv')
        F_df = pd.read_csv(file, index_col=0)

        F_df = (F_df.query('shlp_type=="{0}"'.format(
            kwargs['shlp_type'])))
        F_df.drop('shlp_type', axis=1, inplace=True)

        F_df['weekdays'] = F_df.index + 1

        return np.array(list(map(float, pd.DataFrame.merge(
            F_df, time_df, left_on='weekdays', right_on='weekday', how='outer',
            left_index=True).sort()['wochentagsfaktor'])))

    def create_slp(self, time_df, **kwargs):
        '''Calculation of the hourly heat demand using the bdew-equations'''
        time_df['weekday'].mask(time_df['weekday'] == 0, 7, True)
        SF = self.get_h_values(time_df, **kwargs)
        [A, B, C, D] = self.get_sigmoid_parameter(**kwargs)
        F = self.get_weekday_parameter(time_df, **kwargs)

        h = (A / (1 + (B / (time_df['temp'] - 40)) ** C) + D)
        KW = (kwargs['annual_heat_demand'] /
              (sum(h * F) / 24))
        return (KW * h * F * SF)

    @property
    def load(self):
        return self.heat_demand


class bdew_elec_slp():
    'Generate electrical standardized load profiles based on the BDEW method.'

    def __init__(self, conn, time_df, periods=None):
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
        self.slp_frame = self.all_load_profiles(conn, time_df)

    def all_load_profiles(self, conn, time_df):
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

        # Read standard load profile series from csv file

        selp_series = pd.read_csv('../oemof/demandlib/selp_series.csv')
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
        tmp_df = tmp_df.resample('H', how=how)

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
