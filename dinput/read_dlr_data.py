#!/usr/bin/python  # lint:ok
# -*- coding: utf-8

'''
Author: Uwe Krien (uwe.krien@rl-institut.de)
Changes by:
Responsibility: Uwe Krien (uwe.krien@rl-institut.de)
'''

import os
import logging
import time
import scipy.io
import numpy as np
import dblib as db


def define_pv_dlr_path(coord_x, coord_y, year, ownpath):
    lon_dlr = np.ceil(coord_x * 800 / 360 + 400)
    lat_dlr = np.ceil(coord_y * 800 / 360 + 200)
    filename = ('pv_feedin_' +
                str('%003.0f' % lat_dlr) + '_' +
                str('%003.0f' % lon_dlr) + '_' +
                str(year) + '.mat')
    path_to_file = os.path.join(
                ownpath,
                'pv_feedin',
                str('%003.0f' % lat_dlr),
                filename)
    return path_to_file


def define_wind_dlr_path(coord_x, coord_y, year, ownpath):
    lon_dlr = np.ceil(coord_x * 800 / 360 + 400)
    lat_dlr = np.ceil(coord_y * 800 / 360 + 200)
    filename = ('wind_feedin_E101_100m_' +
                str('%003.0f' % lat_dlr) + '_' +
                str('%003.0f' % lon_dlr) + '_' +
                str(year) + '.mat')
    path_to_file = os.path.join(
                ownpath,
                'wind_feedin_E101_100m',
                str('%003.0f' % lat_dlr),
                filename)
    return path_to_file


def read_mat_feedin_file(path_to_file, timezone, start_hoy, end_hoy):
    tmz = round(timezone)
    mat_feedin = scipy.io.loadmat(path_to_file)['feedin']
    mat_feedin = np.roll(mat_feedin, int(tmz))
    mat_feedin_cut = mat_feedin[start_hoy:end_hoy]
    return mat_feedin_cut


def read_all_feedin(coord_x, coord_y, year, tmz, basic_dc, start_hoy, end_hoy):
    dlr_data = {}
    dlr_data['rpvo'] = read_mat_feedin_file(
        define_pv_dlr_path(coord_x, coord_y, year,
        basic_dc['dlrpath']),
        tmz,
        start_hoy,
        end_hoy)
    dlr_data['rwin'] = read_mat_feedin_file(
        define_wind_dlr_path(coord_x, coord_y, year,
        basic_dc['dlrpath']),
        tmz,
        start_hoy,
        end_hoy)
    return dlr_data


def check_dlr_server_path(basic_dc):
    counter = 0
    if basic_dc['failsafe']:
        while not (os.path.isdir(basic_dc['dlrpath']) or counter == 10):
            print ((os.path.isdir(basic_dc['dlrpath']) or counter == 10))
            counter = counter + 1
            logging.warning('Cannot reach dlrpath. Try again in 30s (%s times).'
                % str(10 - counter))
            time.sleep(30)
    if not os.path.isdir(basic_dc['dlrpath']):
        raise IOError('The given dlrpath is not valid!')


def get_dlr_data(basic_dc, param_dc):
    '''
    This function returns a dictionary which contains DLR feedin time series of
    normalized pv an wind power
    Parameters
    ----------
    param_dict: Parameter dictionary [dictionary]

    Returns
    -------
    dlr_dict: Feedin time series [dictionary]
    '''
    check_dlr_server_path(basic_dc)
    start_hoy = param_dc['simulation']['timestep_start']
    end_hoy = param_dc['simulation']['timestep_end']
    dlr_dict = {r: read_all_feedin(
        param_dc['parameter']['parameter_regions'][r]['longitude'],
        param_dc['parameter']['parameter_regions'][r]['latitude'],
        param_dc['parameter']['parameter_regions'][r]['data_year'],
        param_dc['parameter']['parameter_regions'][r]['timezone'],
        basic_dc, start_hoy, end_hoy)
        for r in param_dc['energy_system']['energy_system_regions']}
    return dlr_dict


def fetch_dlr_data_db(basic_dc, region, start_hoy, end_hoy):
    dlr_dc = {}
    col = region + '_2005'
    where_str = "timestep >= '%s' and timestep <= '%s'" % (
                    start_hoy + 1, end_hoy)
    dlr_dc['rpvo'] = db.fetch_columns(basic_dc, basic_dc['dat_schema'],
            'feedin_pv_dlr', col,
            where_string=where_str, as_np=True, orderby='timestep')[col]
    dlr_dc['rwin'] = db.fetch_columns(basic_dc, basic_dc['dat_schema'],
            'feedin_wind_dlr', col,
            where_string=where_str, as_np=True, orderby='timestep')[col]
    return dlr_dc


def get_dlr_aggr_data(basic_dc, param_dc):
    '''Returns a dictionary in the same structure as returned by
    "get_dlr_data" but with aggregated feedin time series'''
    start_hoy = param_dc['simulation']['timestep_start']
    end_hoy = param_dc['simulation']['timestep_end']
    dlr_dict = {r: fetch_dlr_data_db(basic_dc, r, start_hoy, end_hoy)
        for r in param_dc['energy_system']['energy_system_regions']}
    return dlr_dict