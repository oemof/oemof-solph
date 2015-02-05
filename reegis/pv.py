#!/usr/bin/python
# -*- coding: utf-8

'''
This package uses the Suncalc algorithm to calculate the power output
of a photo voltaic module and further calculates the total hourly pv energy
potential of an area.

Keyword arguments:
    i_dif_hrz - diffuse irradiation on a horizontal surface in W/m²
    i_dir_hrz - direct irradiation on a horizontal surface in W/m²
    geo_b - location latitude
    geo_l - location longitude
    a_module - azimuth angle of the module (default 0.(south))
    h_module - slope angle of the module (default 30.)
    Y=None - year for the calculation of the sun angles (default last year)
    albedo - reflection of the ground around the module (default 0.2)
    h_limit - min height of the sun to start the calculation (default 4.)
    roof_area - ground-plan area of all buildings in m² retrieved from database
    PR - performance ratio of pv collector
    mob_fac - mobilisation factor
              represents the percentage of roofs that are actually used for
              the installation of pv collectors
    E_F - percentage of roofs suitable for the use of PV
'''

#       Suncalc algorithm
#
#       Copyright (c) 2013 iaktueller.de
#       Author: Franz Scheerer <scheerer.software@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
# aus de.wikipedia.org
# Siehe auch Formel (31) in
# http://www.igep.tu-bs.de/lehre/skripten/moderne_physik_dynamik/dynamik.pdf

import time
import numpy as np
import database as db
import ee_potential_district


def tage(Y, M, T):
    '''
    Days since 0.0.0000 (Gregorian Calender).
    '''
    ym = Y - 1
    rm = 365 * ym + ym / 4 - ym / 100 + ym / 400
    mon = np.asarray([0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334])
    rm = rm + mon[M - 1]
    #if M > 2 and Y % 4 == 0 and ((Y % 100 != 0) or (Y % 400 == 0)):
        #rm = rm + 1
    return rm + T


def julian_date(Y, M, T, gmt):
    '''
    Determines the julian date.
    '''
    return (gmt - 6) / 24.0 + tage(Y, M, T) - tage(2006, 8, 6) + 2453953.75


def n(Y, M, T, gmt):
    '''
    Days since 1.1.2000, 12.00 TT.
    '''
    return julian_date(Y, M, T, gmt) - 2451545


def L(Y, M, T, gmt):
    '''
    Determines the mean ecliptic longitude.
    '''
    return 280.460 + n(Y, M, T, gmt) * 0.9856474


def g(Y, M, T, gmt):
    '''
    Determines the mean anomaly.
    '''
    return 357.528 + n(Y, M, T, gmt) * 0.9856003


def lmb(Y, M, T, gmt):
    '''
    Determines the ecliptic longitude.
    '''
    gg = g(Y, M, T, gmt) * (np.pi / 180.0)
    return L(Y, M, T, gmt) + 1.915 * np.sin(gg) + 0.02 * np.sin(2 * gg)


def delta(Y, M, T, gmt):
    '''
    Determines the declination of the earth.
    '''
    lx = lmb(Y, M, T, gmt) * (np.pi / 180.0)
    eps = (23.439 + 0.0000004 * n(Y, M, T, gmt)) * (np.pi / 180.0)
    return np.arcsin(np.sin(lx) * np.sin(eps))


def alpha(Y, M, T, gmt):
    '''
    Dertermines the right ascension.
    '''
    lx = lmb(Y, M, T, gmt) * (np.pi / 180.0)
    eps = (23.439 + 0.0000004 * n(Y, M, T, gmt)) * (np.pi / 180.0)
    return np.arctan2(np.sin(lx) * np.cos(eps), np.cos(lx))


def sidereal_time(Y, M, T, gmt):
    '''
    Dertermines the sidereal time.
    '''
    T0 = n(Y, M, T, 0) / 36525.0
    return (np.pi / 12.0) * (6.697376 + 2400.05134 * T0 + 1.002738 * gmt)


def a(b, lg, Y, M, T, gmt):
    '''
    Determines the azimuth angle of the sun position.
    '''
    b = b * np.pi / (180.0)
    tau = lg * np.pi / 180.0 + sidereal_time(Y, M, T, gmt) - alpha(Y, M, T, 0)
    td = np.tan(delta(Y, M, T, gmt))
    y = np.sin(tau)
    x = np.cos(tau) * np.sin(b) - td * np.cos(b)
    return (180.0 / np.pi) * np.arctan2(y, x)


def h(b, lg, Y, M, T, gmt):
    '''
    Determines the height angle of the sun position.
    '''
    b = b * np.pi / (180.0)
    tau = lg * np.pi / 180.0 + sidereal_time(Y, M, T, gmt) - alpha(Y, M, T, 0)
    d = delta(Y, M, T, gmt)
    tmp1 = np.sin(b) * np.sin(d)
    tmp2 = np.cos(tau) * np.cos(b) * np.cos(d)
    return (180.0 / np.pi) * np.arcsin(tmp1 + tmp2)


def timevector(Y):
    '''
    Creates timevectors for the given year. (Dimension: hours of the year)
    '''
    tmp_m = []
    tmp_tm = []
    tmp_gmt = []
    mon = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if Y % 4 == 0 and (Y % 100 > 0 or Y % 400 == 0):
        mon[1] = 29
    for m in range(12):
        for tm in range(mon[m]):
            for minx in range(24):
                gmt = minx
                tmp_m.append(((m + 1)))
                tmp_tm.append(((tm + 1)))
                tmp_gmt.append(((gmt + 1)))
    return np.asarray(tmp_m), np.asarray(tmp_tm), np.asarray(tmp_gmt)


def position_sun(b, lg, Y, m=None, tm=None, gmt=None):
    '''
    Determines the position of the sun.
    '''
    if m is None or tm is None or gmt is None:
        m, tm, gmt = timevector(Y)
    tmp_h = h(b, lg, Y, m, tm, gmt) / 180.0 * np.pi
    tmp_a = a(b, lg, Y, m, tm, gmt) / 180.0 * np.pi
    return tmp_h, tmp_a


def incident_angle(a_module, h_module, geo_b, geo_l, Y):
    '''
    Determines the incident angle of the sun's irradiation on a tilted surface.
    '''
    h_sun, a_sun = position_sun(geo_b, geo_l, Y)
    a_module = a_module / 180.0 * np.pi
    h_module = h_module / 180.0 * np.pi
    teta_sun = (np.arccos(-1 * np.cos(h_sun) * np.sin(h_module) *
        np.cos(a_sun - a_module) + np.sin(h_sun) *
        np.cos(h_module)) / np.pi * 180.0)
    teta_sun[teta_sun > 90.0] = 90.0
    return teta_sun, h_sun / np.pi * 180.0, a_sun / np.pi * 180.0


def irr_direct_tld_surf(i_dir_hrz, h_sun, teta, h_limit):
    '''
    Calculates the direct irradiation on a tilted surface knowing the direct
    irradiation on a horizontal surface.
    '''
    i_dir_tld = np.zeros(np.size(i_dir_hrz))
    i_dir_tld[h_sun > h_limit] = (
        i_dir_hrz[h_sun > h_limit] *
        (np.cos(teta[h_sun > h_limit] / 180.0 * np.pi) /
        np.sin(h_sun[h_sun > h_limit] / 180.0 * np.pi)))
    return i_dir_tld


def diffuse_sky_tld_klucher(i_dif_hrz, i_dir_hrz, a_sun, theta, h_module):
    '''
    Calculates the diffuse irradiation on a tilted surface knowing the
    diffuse irradiation on a horizontal surface using the model of Klucher.
    [Quasching, Volker : Regenerative Energiesysteme]
    '''
    i_glob_hrz = i_dif_hrz + i_dir_hrz
    F = np.zeros(np.size(i_dif_hrz))
    F[i_glob_hrz != 0.] = 1 - np.power((i_dif_hrz[i_glob_hrz != 0.] /
        i_glob_hrz[i_glob_hrz != 0.]), 2)
    I_dif_sky_tld = (i_dif_hrz * 0.5 *
        (1 + np.cos(h_module / 180. * np.pi)) *
        (1 + F * np.power(np.sin((h_module / 2.) / 180. * np.pi), 3.)) *
        (1 + F * np.power(np.cos(theta / 180. * np.pi), 2.) *
        np.power(np.cos(a_sun / 180. * np.pi), 3)))
    return I_dif_sky_tld


def diffuse_reflection_tld(i_dif_hrz, i_dir_hrz, h_module, albedo):
    '''
    Calculates the diffuse irradiation on a tilted surface reflected
    from the ground.
    '''
    i_glob_hrz = i_dif_hrz + i_dir_hrz
    i_dif_tld_refl = (i_glob_hrz * albedo * 0.5 *
        (1 - np.cos(h_module / 180. * np.pi)))
    return i_dif_tld_refl


def irr_global_tld_surf(i_dif_hrz, i_dir_hrz, geo_b, geo_l,
        a_module=0., h_module=30, Y=None, albedo=0.2, h_limit=4):
    '''
    Calculates the global irratdiation on a tilted surface by knowing the
    diffuse and direct irradiation on a horizontal surface
    and the coordinates (latitude and longitude) of the location.
    '''
    if not Y:
        Y = time.localtime().tm_year - 1
    teta, h_sun, a_sun = incident_angle(a_module, h_module, geo_b, geo_l, Y)
    try:
        i_dir_hrz + h_sun
    except ValueError:
        print(("Days in " + str(Y) + ": " + str(np.size(h_sun) / 24)))
        print(("Days in weather data: " + str(np.size(i_dir_hrz) / 24)))
        errorstring = ("Vector dimensions do not agree. You might have " +
            "selected a leap year with 366 days but the weather data only " +
            "has 365 days (8760) hours. See output above")
        raise ValueError(errorstring)
    i_dir_t = irr_direct_tld_surf(i_dir_hrz, h_sun, teta, h_limit)
    i_dif_sky_t = diffuse_sky_tld_klucher(i_dif_hrz, i_dir_hrz, a_sun,
        teta, h_module)
    i_dif_refl_t = diffuse_reflection_tld(
        i_dif_hrz, i_dir_hrz, h_module, albedo)
    return (i_dir_t + i_dif_sky_t + i_dif_refl_t)


def scaled_power_output(input_data):
    '''
    Calculates the hourly pv potential in MWh/h of a region scaled to 1 MW.
    '''
    # variable definition
    district = input_data['district']
    PR = input_data['PR']
    eta = input_data['eta PV']
    a_module = input_data['a_module']
    h_module = input_data['h_module']
    Year = input_data['Year']
    albedo = input_data['albedo']
    h_limit = input_data['h_limit [m]']
    try_data = db.get_try_data(district)
    i_dif_hrz = try_data[:, 15]
    i_dir_hrz = try_data[:, 14]
    geo_b, geo_l = db.long_lat(district)
    # calculation of power output
    if not Year:
        Year = time.localtime().tm_year - 1
    i_glob_tld = irr_global_tld_surf(i_dif_hrz, i_dir_hrz, geo_b, geo_l,
        a_module, h_module, Year, albedo, h_limit)
    pv_pot = (i_glob_tld * PR * eta) / (10 ** 6)
    scaled_pv_pot = pv_pot / max(pv_pot)
    return scaled_pv_pot


def pv_total_area(input_data, pv_cap=None):
    '''
    Calculates the pv area in m².
    '''
    # if capacity is given
    if pv_cap:
        pv_area = pv_cap * 1000 / input_data['eta PV']
    # if capacity is not given, calculate potential area
    else:
        district = input_data['district']
        mob_fac = input_data['mob_fac']
        E_F = input_data['E_F']
        building_area = db.building_area(district)
        pv_area = building_area * E_F * mob_fac
    return pv_area


def total_power_output(input_data, pv_cap=None):
    '''
    Calculates the hourly pv potential in MWh/h of a region.
    pv_cap in MW
    pv_area in m²
    '''
    scaled_pv_pot = scaled_power_output(input_data)
    pv_area = pv_total_area(input_data)
    if not pv_cap:
        pv_cap = input_data['eta PV'] * pv_area / 1000
    hourly_pv_pot = pv_cap * scaled_pv_pot
    return pv_area, hourly_pv_pot


def get_hourly_pv_pot(input_data, potential, use_case,
    schema=None, table_name=None, column_name=None,
    filename=None, directory=None, save=None,
    save_to_table=None, save_to_column='pv_pot',
    share_pot_used=1):
    '''
    Returns the hourly PV potential in MWh/h.
    Depending on which potential is wanted, either the total potential of the
    chosen district, the scaled potential (scaled to a maximum capacity of 1 MW)
    or the district's potential (installed capacity plus additional potential)
    is returned.
    Depending on the chosen use case the hourly potential is either retrieved
    from a file or database or calculated.
    '''
    # Returns the total hourly potential of the chosen area
    if potential == 'total':
        pv_area, hourly_pv_potential = total_power_output(input_data)

    # Returns the hourly potential of the chosen area scaled to the capacity of
    # 1 MW
    elif potential == 'scaled' or potential == 'district':
        # retrieve hourly pv potential from the database
        if use_case == 'db':
            if db.table_exists(table_name):
                hourly_pv_potential = db.retrieve_from_db_table(
                    schema, table_name, column_name, order='yes')
                hourly_pv_potential = np.reshape(
                    hourly_pv_potential, (-1, ))
                # scale
                hourly_pv_potential = \
                    hourly_pv_potential / max(hourly_pv_potential)
            else:
                print (('Table to retrieve the hourly pv potential from ' +
                'does not exist.'))
        # retrieve hourly pv potential from file
        elif use_case == 'file':
            hourly_pv_potential = \
                db.read_profiles_from_file(filename, directory)[column_name]
            hourly_pv_potential = np.reshape(hourly_pv_potential, (-1, ))
            # scale
            hourly_pv_potential = \
                hourly_pv_potential / max(hourly_pv_potential)
        elif use_case == 'calc':
            hourly_pv_potential = scaled_power_output(input_data)
        else:
            print (('Hourly pv potential cannot be returned because of ' +
            'invalid use case. The use case chosen was: %s' % use_case))
        pv_area = None
    elif potential == 'scaled_mixed':
        hourly_pv_potential = mixed_pv_feedin()
        hourly_pv_potential = np.reshape(hourly_pv_potential, (-1, ))
        pv_area = None
    # Error message
    else:
        print (('Hourly pv potential cannot be returned because of ' +
        'invalid "potential" input. The "potential" chosen was: %s'
        % potential))

    # Returns the hourly potential of the chosen district in Wittenberg
    if potential == 'district':
        hourly_pv_potential = ee_potential_district.pv_potential(
            input_data, hourly_pv_potential, share_pot_used)

    # save results to db
    if save:
        if db.table_exists(save_to_table):
            db.save_results_to_db(
                schema, save_to_table, save_to_column, hourly_pv_potential)
        else:
            # create output table and id column
            db.create_db_table(schema, save_to_table,
                save_to_column + ' real')
            stringi = '(1)'
            for i in range(2, 8761):
                stringi = stringi + ',(' + str(i) + ')'
            db.insert_data_into_db_table(schema, save_to_table, 'id', stringi)
            db.save_results_to_db(
                schema, save_to_table, save_to_column, hourly_pv_potential)

    return hourly_pv_potential, pv_area


def mixed_pv_feedin():
    '''
    Returns an hourly pv feed-in profile for different orientations of
    pv modules.
    '''
    # dictionary with share of each orientation of the pv modules
    orientation = {'East_30deg': 0.05,
        'SouthEast_30deg': 0.2,
        'South_25deg': 0.5 / 3,
        'South_30deg': 0.5 / 3,
        'South_35deg': 0.5 / 3,
        'SouthWest_30deg': 0.2,
        'West_30deg': 0.05}

    # retrieve profiles from db
    hourly_pv_pot = np.zeros((8760, 1))
    for i in list(orientation.keys()):
        hourly_pv_pot += orientation[i] * db.retrieve_from_db_table(
            'wittenberg', 'scaled_pv_feedin', i, primary_key='hoy')

    return hourly_pv_pot