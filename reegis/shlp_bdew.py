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
'''

import numpy as np
from math import ceil as round_up
import database as db


def temp_geo_series(temp):
    '''
    A new temperature vector is generated containing a multy-day
    average temperature as needed in the load profile function.
    '''
    daily_average_temp = np.zeros((365,))
    for i in range(365):
        daily_average_temp[i] = (sum(temp[i * 24: (i + 1) * 24]) / 24)
    temp_geo = np.zeros((365,))
    temp_geo[0] = ((daily_average_temp[0] + 0.5 *
        daily_average_temp[364] + 0.25 * daily_average_temp[363] + 0.125 *
        daily_average_temp[362]) / 1.875)
    temp_geo[1] = ((daily_average_temp[1] + 0.5 * daily_average_temp[0] +
        0.25 * daily_average_temp[364] + 0.125 * daily_average_temp[363]) /
        1.875)
    temp_geo[2] = ((daily_average_temp[2] + 0.5 * daily_average_temp[1] +
        0.25 * daily_average_temp[0] + 0.125 * daily_average_temp[364]) /
        1.875)
    for i in range(3, 365):
        temp_geo[i] = ((daily_average_temp[i] + 0.5 *
        daily_average_temp[i - 1] + 0.25 * daily_average_temp[i - 2] + 0.125 *
        daily_average_temp[i - 3]) / 1.875)
        temp_geo_series = np.zeros((8760,))
    for i in range(365):
        temp_geo_series[i * 24: (i + 1) * 24] = temp_geo[i]
    return temp_geo_series


def temp_interval(temp):
    '''
    Appoints the corresponding temperature interval to each temperature in the
    temperature vector.
    '''
    temp_dict = ({-20: 1, -19: 1, -18: 1, -17: 1, -16: 1, -15: 1, -14: 2,
        -13: 2, -12: 2, -11: 2, -10: 2, -9: 3, -8: 3, -7: 3, -6: 3, -5: 3,
        -4: 4, -3: 4, -2: 4, -1: 4, 0: 4, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 6,
        7: 6, 8: 6, 9: 6, 10: 6, 11: 7, 12: 7, 13: 7, 14: 7, 15: 7, 16: 8,
        17: 8, 18: 8, 19: 8, 20: 8, 21: 9, 22: 9, 23: 9, 24: 9, 25: 9, 26: 10,
        27: 10, 28: 10, 29: 10, 30: 10, 31: 10, 32: 10, 33: 10, 34: 10, 35: 10,
        36: 10, 37: 10, 38: 10, 39: 10, 40: 10})
    temp_rounded = [round_up(i) for i in temp]
    temp_int = [temp_dict[i] for i in temp_rounded]
    return np.transpose(np.array(temp_int))


def res_slp(cur, res_type, temp, temp_int, building_class, wind_class,
    annual_heat_demand, ww_incl='yes'):
    '''
    Returns a vector SF_vec containing the applicable hour factors, as well as
    the sigmoid parameters A, B, C and D and the weekday parameter F of
    single- or multi-family houses.
    '''
    # hours_vec, SF_mat
    cur.execute('''
        select l.id, l.tagesstunden, r.temp_intervall_1, r.temp_intervall_2,
            r.temp_intervall_3, r.temp_intervall_4, r.temp_intervall_5,
            r.temp_intervall_6, r.temp_intervall_7, r.temp_intervall_8,
            r.temp_intervall_9,r.temp_intervall_10
        from wittenberg.stunden_tage as l
            left join wittenberg.hour_factors as r
                on l.tagesstunden=r.hour_of_day
        where r.building_class=%(int)s and r.type=%(str)s
        order by l.id
    ''', {'int': building_class, 'str': res_type})
    data_array = np.asarray(cur.fetchall())
    hours_vec = np.array(list(map(int, data_array[:, 0])))
    SF_mat = (np.transpose(np.array([data_array[:, 2], data_array[:, 3],
        data_array[:, 4], data_array[:, 5], data_array[:, 6], data_array[:, 7],
        data_array[:, 8], data_array[:, 9], data_array[:, 10],
        data_array[:, 11]])))
    SF_vec = SF_mat[(hours_vec - 1)[:], (temp_int - 1)[:]]
    # sigmoid parameters A, B, C, D
    if ww_incl == 'yes':
        # returns the sigmoid parameters for the generation of a heat load
        # profile where warm water demand is included
        cur.execute('''
           select parameter_a, parameter_b, parameter_c, parameter_d
           from wittenberg.sigmoid_parameters
           where building_class=%(int)s and wind_impact=%(int_2)s
           and type=%(str)s
       ''', {'int': building_class, 'int_2': wind_class, 'str': res_type})
        data_array = np.asarray(cur.fetchall())
        A = float(data_array[0, 0])
        B = float(data_array[0, 1])
        C = float(data_array[0, 2])
        D = float(data_array[0, 3])
    else:
        # returns the sigmoid parameters for the generation of a heat load
        # profile where warm water demand is not included
        cur.execute('''
        select parameter_a, parameter_b, parameter_c
        from wittenberg.sigmoid_parameters
        where building_class=%(int)s and wind_impact=%(int_2)s and type=%(str)s
        ''', {'int': building_class, 'int_2': wind_class, 'str': res_type})
        data_array = np.asarray(cur.fetchall())
        A = float(data_array[0, 0])
        B = float(data_array[0, 1])
        C = float(data_array[0, 2])
        D = 0
    # weekday parameter F
    cur.execute('''
        select r.wochentagsfaktor
        from wittenberg.stunden_tage as l
            left join wittenberg.wochentagsfaktoren as r
                on l.wochentag = r.wochentag
        where typ = %(str)s
    ''', {'str': res_type})
    data_array = np.asarray(cur.fetchall())
    F = np.array(list(map(float, data_array[:, 0])))
    # calculation of hourly heat demand
    SF = np.array(list(map(float, SF_vec[:])))
    h = (A / (1 + (B / (temp - 40)) ** C) + D)
    KW = annual_heat_demand / (sum(h * F) / 24)
    hourly_heat_demand = KW * h * F * SF
    return hourly_heat_demand


def com_slp(cur, com_type, temp, temp_int, wind_class,
    annual_heat_demand):
    '''
    Returns a vector SF_vec containing the applicable hour factors, as well as
    the sigmoid parameters A, B, C and D and the weekday parameter F of
    the specified commercial business.
    '''
    # hours_vec, SF_mat
    cur.execute('''
        select l.id, l.tagesstunden, r.temp_intervall_1, r.temp_intervall_2,
            r.temp_intervall_3, r.temp_intervall_4, r.temp_intervall_5,
            r.temp_intervall_6, r.temp_intervall_7,r.temp_intervall_8,
            r.temp_intervall_9,r.temp_intervall_10
        from wittenberg.stunden_tage as l
            left join wittenberg.hour_factors as r
                on l.tagesstunden=r.hour_of_day and l.wochentag=r.weekday
        where r.type=%(str)s
        order by l.id
    ''', {'str': com_type})
    data_array = np.asarray(cur.fetchall())
    hours_vec = np.array(list(map(int, data_array[:, 0])))
    SF_mat = (np.transpose(np.array([data_array[:, 2], data_array[:, 3],
        data_array[:, 4], data_array[:, 5], data_array[:, 6], data_array[:, 7],
        data_array[:, 8], data_array[:, 9], data_array[:, 10],
        data_array[:, 11]])))
    SF_vec = SF_mat[(hours_vec - 1)[:], (temp_int - 1)[:]]
    # sigmoid parameters A, B, C, D
    cur.execute('''
        select parameter_a, parameter_b, parameter_c, parameter_d
        from wittenberg.sigmoid_parameters
        where type=%(str)s and wind_impact=%(int)s
    ''', {'str': com_type, 'int': wind_class})
    data_array = np.asarray(cur.fetchall())
    A = float(data_array[0, 0])
    B = float(data_array[0, 1])
    C = float(data_array[0, 2])
    D = float(data_array[0, 3])
    # weekday parameter F
    cur.execute('''
        select r.wochentagsfaktor
        from wittenberg.stunden_tage as l
        left join wittenberg.wochentagsfaktoren as r
        on l.wochentag = r.wochentag
        where typ = %(str)s
    ''', {'str': com_type})
    data_array = np.asarray(cur.fetchall())
    F = np.array(list(map(float, data_array[:, 0])))
    # calculation of hourly heat demand
    SF = np.array(list(map(float, SF_vec[:])))
    h = (A / (1 + (B / (temp - 40)) ** C) + D)
    KW = annual_heat_demand / (sum(h * F) / 24)
    hourly_heat_demand = KW * h * F * SF
    return hourly_heat_demand


def generate_load_profile(input_data, annual_heat_demand, ww_incl='yes',
    hourly_temp=None):
    '''
    This function calculates the hourly heat demand of the different
    residential and commercial types as a function of the maximum heat demand,
    the wind and building class and the given temperature profile.
    '''
    district = input_data['district']
    building_class = str(input_data['building_class'])
    wind_class = str(input_data['wind_class'])

    if hourly_temp is None:
        hourly_temp = db.get_try_data(district)[:, 9]

    # appoint temperature interval
    temp = temp_geo_series(hourly_temp)
    temp_int = temp_interval(temp)

    # generate load profiles
    hourly_heat_demand = {}
    res_hourly_heat_demand = np.zeros((8760, ))
    com_hourly_heat_demand = np.zeros((8760, ))
    conn = db.open_db_connection()
    cur = conn.cursor()

    for i in list(annual_heat_demand.keys()):
        if i == 'EFH' or i == 'MFH':
            if not ww_incl == 'yes':
                hourly_heat_demand[i] = res_slp(
                    cur, i, temp, temp_int, building_class, wind_class,
                    annual_heat_demand[i], ww_incl='no')
                res_hourly_heat_demand += hourly_heat_demand[i]
            else:
                hourly_heat_demand[i] = res_slp(
                    cur, i, temp, temp_int, building_class, wind_class,
                    annual_heat_demand[i])
                res_hourly_heat_demand += hourly_heat_demand[i]
        else:
            hourly_heat_demand[i] = com_slp(
                cur, i, temp, temp_int, wind_class, annual_heat_demand[i])
            com_hourly_heat_demand += hourly_heat_demand[i]

    cur.close()
    conn.close()

    return res_hourly_heat_demand, com_hourly_heat_demand