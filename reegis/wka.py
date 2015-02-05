#!/usr/bin/python
# -*- coding: utf-8

'''
This package conducts all calculations necessary to calculate the power output
of a wind turbine and the total hourly wind energy potential of an area.

Keyword arguments:
    wind_area - possible area for wind parks in km² (retrieved from database)
    h_hub - hub height in m of chosen wind turbine
    d_rotor - rotor diameter in m of chosen wind turbine
    h_windmast - meters above ground of TRY wind measurement
    z_0 - surface roughness in m
    type_wka - wind turbine type
    v_wind, p_data, T_data - wind speed in m/s, air pressure in hPa and
                             air temperature in °C respectively, retrieved
                             from TRY
    h_data_amsl - meters above sea level of TRY station
'''

import numpy as np
from scipy.interpolate import interp1d
import database as db
import ee_potential_district


def rho_hub(h_hub, h_base_amsl, h_data_amsl, T_data, p_data):
    '''
    Calculates the density of air in kg/m³ at hub height. (temperature in °C,
        height in m, pressure in hPa)
    Assumptions:
        Temperature gradient of -6.5 K/km
        Density gradient of -1/8 hPa/m
    '''
    T_hub = (T_data + 273.15) - 0.0065 * (h_hub + h_base_amsl - h_data_amsl)
    return (p_data - (h_hub + h_base_amsl - h_data_amsl) *
        1 / 8) / (2.8706 * T_hub)


def v_wind_hub(h_hub, h_windmast, v_winddata, z_0):
    '''
    Calculates the wind speed in m/s at hub height.
    h_windmast is the hight in which the wind velocity is measured.
    (height in m, velocity in m/s)
    '''
    return (v_winddata * np.log(h_hub / z_0) /
        np.log(h_windmast / z_0))


def cp_values(cp_data, v_wind):
    '''
    Interpolates the cp value as a function of the wind velocity between data
    obtained from the power curve of the specified wind turbine type.
    '''
    v_wind[v_wind > np.max(cp_data[:, 0])] = np.max(cp_data[:, 0])
    return interp1d(cp_data[:, 0], cp_data[:, 1])(v_wind)


def number_wka_sqkm(d_rotor):
    '''
    Calculates the possible number of wind power stations per km² (Hau, 2008).
    According to Hau the distance between two turbines should be 8 - 10 rotor
    diameters in the prevailing wind direction and 3 - 5 rotor diameters
    perpendicular to the prevailing wind direction. (diameter in m)
    '''
    dist_wd = 8  # prevailing wind direction
    dist_pwd = 4  # perpendicular to prevailing wind direction
    return 1 / (dist_wd * dist_pwd * (float(d_rotor) / 1000) ** 2)


def number_wka_district(d_rotor, area):
    '''
    Returns the possible number of wind turbines in a district.
    '''
    return round(area * number_wka_sqkm(d_rotor))


def turbine_power_output(h_hub, d_rotor, h_windmast, z_0, cp_data, v_wind,
    p_data, T_data, h_data_amsl):
    '''
    Calculates the power output in W of one wind turbine.
    '''
    # mamsl (meters above sea level) of the base of the wind turbine are set
    # to mamsl of the weather station
    # (height in m, diameter in m, power in W, density in kg/m³, temp. in °C,
    # pressure in hPa, velocity in m/s)
    h_base_amsl = h_data_amsl

    P_wka = ((rho_hub(h_hub, h_base_amsl, h_data_amsl, T_data,
    p_data) / 2) * (((d_rotor / 2) ** 2) * np.pi) *
    np.power(v_wind_hub(h_hub, h_windmast, v_wind, z_0), 3) *
    cp_values(cp_data, v_wind_hub(h_hub, h_windmast, v_wind, z_0)))

    return P_wka


def scaled_power_output(input_data):
    '''
    Calculates the hourly wind potential in MWh/h of a region scaled to a
    maximum capacity of 1 MW.
    '''
    # variable definition
    district = input_data['district']
    h_hub = input_data['h_hub']
    d_rotor = input_data['d_rotor']
    h_windmast = input_data['h_windmast']
    z_0 = input_data['z_0']
    type_wka = input_data['type_wka']
    cp_data = db.wka_cp_values(type_wka)
    try_data = db.get_try_data(district)
    v_wind = try_data[:, 8]
    p_data = try_data[:, 10]
    T_data = try_data[:, 9]
    h_data_amsl = try_data[0, 20]
    # calculation of power output
    P_wka = turbine_power_output(h_hub, d_rotor, h_windmast, z_0, cp_data,
        v_wind, p_data, T_data, h_data_amsl)
    hourly_wind_pot = P_wka / (10 ** 6)
    scaled_wind_pot = hourly_wind_pot / max(hourly_wind_pot)
    return scaled_wind_pot


def total_power_output(input_data):
    '''
    Calculates the hourly wind potential in MWh/h of a region.
    '''
    scaled_wind_pot = scaled_power_output(input_data)
    area = db.wind_area(input_data['district'])
    number_wka = number_wka_district(input_data['d_rotor'], area)
    P_max_wka = db.P_max_wka(input_data['type_wka']) / (10 ** 3)
    hourly_wind_pot = number_wka * P_max_wka * scaled_wind_pot
    return hourly_wind_pot, number_wka


def get_hourly_wind_pot(input_data, p_set, potential, use_case,
    schema=None, table_name=None, column_name=None,
    filename=None, directory=None, save=None,
    save_to_table=None, save_to_column='wind_pot',
    share_pot_used=1):
    '''
    Returns the hourly wind potential in MWh/h.
    Depending on which potential is wanted, either the total potential of the
    chosen district, the scaled potential (scaled to a maximum capacity of 1 MW)
    or the district's potential (installed capacity plus additional potential)
    is returned.
    Depending on the chosen use case the hourly potential is either retrieved
    from a file or database or calculated.
    '''
    # Returns the total hourly potential of the chosen area
    if potential == 'total':
        hourly_wind_potential, number_wka = total_power_output(input_data)

    # Returns the hourly potential of the chosen area scaled to the capacity of
    # 1 MW
    elif potential == 'scaled' or potential == 'district':
        # retrieve hourly wind potential from the database
        if use_case == 'db':
            if db.table_exists(table_name):
                hourly_wind_potential = db.retrieve_from_db_table(
                    schema, table_name, column_name, order='yes')
                hourly_wind_potential = np.reshape(
                    hourly_wind_potential, (-1, ))
                # scale
                hourly_wind_potential = \
                    hourly_wind_potential / max(hourly_wind_potential)
            else:
                print (('Table to retrieve the hourly wind potential from ' +
                'does not exist.'))
        # retrieve hourly wind potential from file
        elif use_case == 'file':
            hourly_wind_potential = \
                db.read_profiles_from_file(filename, directory)[column_name]
            hourly_wind_potential = np.reshape(hourly_wind_potential, (-1, ))
            # scale
            hourly_wind_potential = \
                hourly_wind_potential / max(hourly_wind_potential)
        # calculate scaled hourly wind potential
        elif use_case == 'calc':
            hourly_wind_potential = scaled_power_output(input_data)
        else:
            print (('Hourly wind potential cannot be returned because of ' +
            'invalid use case. The use case chosen was: %s' % use_case))
        number_wka = None
    # calculate scaled hourly wind potential considering different wind turbine
    # types
    elif potential == 'scaled_mixed':
        hourly_wind_potential = mixed_wind_feedin(
            p_set['cap_wind_current'][p_set['index']] /
            p_set['cap_wind'][p_set['index']])
        hourly_wind_potential = np.reshape(hourly_wind_potential, (-1, ))
        number_wka = None
    # Error message
    else:
        print (('Hourly wind potential cannot be returned because of ' +
        'invalid "potential" input. The "potential" chosen was: %s'
        % potential))

    # Returns the hourly potential of the chosen district in Wittenberg
    if potential == 'district':
        hourly_wind_potential = ee_potential_district.wind_potential(
            input_data['district'], hourly_wind_potential, share_pot_used)

    # save results to db
    if save:
        if db.table_exists(save_to_table):
            db.save_results_to_db(
                schema, save_to_table, save_to_column, hourly_wind_potential)
        else:
            # create output table and id column
            db.create_db_table(schema, save_to_table,
                save_to_column + ' real')
            stringi = '(1)'
            for i in range(2, 8761):
                stringi = stringi + ',(' + str(i) + ')'
            db.insert_data_into_db_table(schema, save_to_table, 'id', stringi)
            db.save_results_to_db(
                schema, save_to_table, save_to_column, hourly_wind_potential)

    return hourly_wind_potential, number_wka


def mixed_wind_feedin(share_current):
    '''
    Returns an hourly wind feed-in profile for a mix of currently built
    wind turbines and wind turbines build in the future.
    '''
    # retrieve profile for current-state
    hourly_wind_pot_current = share_current * \
        db.retrieve_from_db_table('wittenberg',
            'scaled_wind_feedin', 'mix_ist', primary_key='hoy')
    # retrieve profile for future
    hourly_wind_pot_future = (1 - share_current) * \
        db.retrieve_from_db_table('wittenberg',
            'scaled_wind_feedin', 'mix_zukunft', primary_key='hoy')
    return hourly_wind_pot_current + hourly_wind_pot_future


def mixed_wind_feedin_av_cap(share_current):
    '''
    Returns the average size of the windturbines considered for the mixed
    wind feed-in profile.
    '''
    # dictionary with share of current and future state of each
    # wind turbine type considered
    wka_types = {'E-70': {'share_current': 0.6,
                          'share_future': 0.25},
                'E-40': {'share_current': 0.3,
                         'share_future': 0.0},
                'E-82 E2': {'share_current': 0.1,
                            'share_future': 0.25},
                'E-82 E3': {'share_current': 0.0,
                            'share_future': 0.25},
                'E101': {'share_current': 0.0,
                         'share_future': 0.25}}
    # average capacity
    av_cap_current = 0
    av_cap_future = 0
    for i in list(wka_types.keys()):
        wka_types[i]['cap'] = db.P_max_wka(i) / 1000  # cap in MW
        av_cap_current += wka_types[i]['cap'] * wka_types[i]['share_current']
        av_cap_future += wka_types[i]['cap'] * wka_types[i]['share_future']
    return share_current * av_cap_current + (1 - share_current) * av_cap_future