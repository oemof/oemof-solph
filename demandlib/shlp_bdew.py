#!/usr/bin/python
# -*- coding: utf-8

'''
This package follows the guidelines for the generation of standardised load
profiles of the BDEW (Bundesverband der Energie- und Wasserwirtschaft) to
calculate the residential and commercial hourly heat demand (heating and warm
water) of a region.

Keyword arguments:
    temp - hourly outdoor temperature profile
    building_class - Classifies the ratio of old to new buildings from
                     1 to 10. For more information see 'Praxisinformation
                     P 2006/8 Gastransport/Betriebswirtschaft' page 42.
                     As default building_class is set to 11 which represents
                     the german average ratio of 75% old buildings to 25%
                     new buildings .
    wind_class - As default 'wind_class' is set to '0'. If the area to be
                 analyzed is a windy region, 'wind_class' can be set to '1'

http://www.eichsfeldwerke.de/_data/Praxisinformation_P2007_13.pdf
https://www.avacon.de/cps/rde/xbcr/avacon/Netze_Lieferanten_Netznutzung_Lastprofilverfahren_Leitfaden_SLP_Gas.pdf
'''
import logging
import pandas as pd
import numpy as np
from math import ceil as round_up
from oemof.dblib import read_data_pg as rdb


def get_try_region(main_dt, reg):
    '''
    Determines applicable Test Reference Year Region.
    '''
    sql_string = '''
    select try_code
    from wittenberg.try_dwd as dwd,
         {0} as vshape
    where st_contains(the_geom, st_centroid(vshape.geom));'''.format(
        main_dt[reg]['region_view'])
    return rdb.execute_read_db(main_dt['basic'], sql_string)[0][0]


def get_try_temperature(main_dt, reg):
    '''
    Returns the following data set for the given region.

    air_temp  Air temperature 2m above ground                          [°C]
    '''
    return rdb.fetch_columns(
        main_dt['basic'], 'wittenberg', 'try_2010_av_year', columns='air_temp',
        where_column='region', where_condition=get_try_region(main_dt, reg),
        as_np=True, orderby='id')['air_temp']


def temp_geo_series(temp, time_df):
    '''
    A new temperature vector is generated containing a multy-day
    average temperature as needed in the load profile function.

    Notes
    -----
    Equation for the mathematical series of the average tempaerature [1]_:

    .. math::
        T=\frac{T_{t}+0.5\cdot T_{t-1}+0.25\cdot T_{t-2}+0.125\cdot T_{t-3}}
                {1+0.5+0.25+0.125}$
    with :math:`T_t` = Average temperature on the present day
         :math:`T_{t-1}` = Average temperature on the previous day ...

    References
    ----------
    .. [1] `BDEW <https://www.avacon.de/cps/rde/xbcr/avacon/Netze_Lieferanten_Netznutzung_Lastprofilverfahren_Leitfaden_SLP_Gas.pdf>`_, BDEW Documentation for heat profiles.
    '''
    time_df['temp'] = temp
    tem = time_df['temp'].resample('D', how='mean').reindex(
        time_df.index).fillna(method="ffill")
    return (tem + 0.5 * np.roll(tem, 24) + 0.25 * np.roll(tem, 48) +
            0.125 * np.roll(tem, 72)) / 1.875


def temp_interval(temp):
    '''
    Appoints the corresponding temperature interval to each temperature in the
    temperature vector.
    '''
    temp_dict = ({
        -20: 1, -19: 1, -18: 1, -17: 1, -16: 1, -15: 1, -14: 2,
        -13: 2, -12: 2, -11: 2, -10: 2, -9: 3, -8: 3, -7: 3, -6: 3, -5: 3,
        -4: 4, -3: 4, -2: 4, -1: 4, 0: 4, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 6,
        7: 6, 8: 6, 9: 6, 10: 6, 11: 7, 12: 7, 13: 7, 14: 7, 15: 7, 16: 8,
        17: 8, 18: 8, 19: 8, 20: 8, 21: 9, 22: 9, 23: 9, 24: 9, 25: 9, 26: 10,
        27: 10, 28: 10, 29: 10, 30: 10, 31: 10, 32: 10, 33: 10, 34: 10, 35: 10,
        36: 10, 37: 10, 38: 10, 39: 10, 40: 10})
    temp_rounded = [round_up(i) for i in temp]
    temp_int = [temp_dict[i] for i in temp_rounded]
    return np.transpose(np.array(temp_int))


def get_h_values(main_dt, parameter, time_df, temp_int):
    '''Determine the h-values'''
    # Create the condition to retrieve the hour_factors from the database
    condition = (
        "building_class = {building_class} and type = upper('{shlp_type}')"
        ).format(**parameter)

    # Retrieve the hour factors and write them into a DataFrame
    hour_factors = pd.DataFrame.from_dict(rdb.fetch_columns(
        main_dt['basic'], 'demand', 'shlp_hour_factors', columns=[
            'hour_of_day', 'weekday']
        + ['temp_intervall_{0:02.0f}'.format(x) for x in range(1, 11)],
        as_np=True, orderby='id', where_string=condition))

    # Join the two DataFrames on the columns 'hour' and 'hour_of_the_day' or
    # ['hour' 'weekday'] and ['hour_of_the_day', 'weekday'] if it is not a
    # residential slp.
    residential = parameter['building_class'] > 0

    left_cols = ['hour_of_day'] + (['weekday'] if not residential else [])
    right_cols = ['hour'] + (['weekday'] if not residential else [])

    SF_mat = pd.DataFrame.merge(
        hour_factors, time_df, left_on=left_cols, right_on=right_cols,
        how='outer', left_index=True).sort().drop(left_cols + right_cols, 1)

    # Determine the h values
    h = np.array(SF_mat)[np.array(range(0, 8760))[:], (temp_int - 1)[:]]
    return np.array(list(map(float, h[:])))


def get_sigmoid_parameter(main_dt, parameter):
    ''' Retrieve the sigmoid parameters from the database'''

    condition = """building_class={building_class} and wind_impact={wind_class}
    and type=upper('{shlp_type}')""".format(**parameter)

    sigmoid = rdb.fetch_columns(
        main_dt['basic'], 'demand', 'shlp_sigmoid_parameters', columns=[
            'parameter_{0}'.format(x) for x in ['a', 'b', 'c', 'd']],
        as_np=True, where_string=condition)

    A = float(sigmoid['parameter_a'])
    B = float(sigmoid['parameter_b'])
    C = float(sigmoid['parameter_c'])
    D = float(sigmoid['parameter_d']) if parameter.get('ww_incl', True) else 0
    return A, B, C, D


def get_weekday_parameter(main_dt, parameter, time_df):
    ''' Retrieve the weekdayparameter from the database'''
    F_df = pd.DataFrame.from_dict(rdb.fetch_columns(
        main_dt['basic'], 'demand', 'shlp_wochentagsfaktoren',
        columns=['wochentagsfaktor'], as_np=True, where_column='typ',
        orderby='wochentag', where_condition=(parameter['shlp_type'].upper())))
    F_df['weekdays'] = F_df.index + 1

    return np.array(list(map(float, pd.DataFrame.merge(
        F_df, time_df, left_on='weekdays', right_on='weekday', how='outer',
        left_index=True).sort()['wochentagsfaktor'])))


def create_slp(main_dt, temp, temp_int, year, reg, time_df, parameter):
    '''Calculation of the hourly heat demand using the bdew-equations'''
    SF = get_h_values(main_dt, parameter, time_df, temp_int)
    [A, B, C, D] = get_sigmoid_parameter(main_dt, parameter)
    F = get_weekday_parameter(main_dt, parameter, time_df)

    h = (A / (1 + (B / (temp - 40)) ** C) + D)
    KW = (parameter['annual_heat_demand'] /
          (sum(h * F) / 24))
    main_dt['timeseries']['demand'][reg]['heat_demand'][
        parameter['shlp_type']] = (KW * h * F * SF)
    main_dt['timeseries']['demand'][reg]['heat_demand']['all'] += main_dt[
        'timeseries']['demand'][reg]['heat_demand'][parameter['shlp_type']]


def generate_bdew_load_profile(main_dt, time_df, reg, year):
    '''
    This function calculates the hourly heat demand of the different
    residential and commercial types as a function of the maximum heat demand,
    the wind and building class and the given temperature profile.
    '''
    # Set holidays (weekday=0) to sundays (weekday=7).
    time_df['weekday'].mask(time_df['weekday'] == 0, 7, True)
    hourly_temp = get_try_temperature(main_dt, reg)
    temp = temp_geo_series(hourly_temp, time_df)
    temp_int = temp_interval(temp)
    main_dt['timeseries']['demand'][reg]['heat_demand'] = time_df.drop(
        list(time_df.keys()), 1)
    main_dt['timeseries']['demand'][reg]['heat_demand']['all'] = 0
    for group in main_dt['parameter']['building'][reg].keys():
        create_slp(main_dt, temp, temp_int, year, reg, time_df,
                   main_dt['parameter']['building'][reg][group])
