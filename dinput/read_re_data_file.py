#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Author: Uwe Krien (uwe.krien@rl-institut.de)
Changes by:
Responsibility: Uwe Krien (uwe.krien@rl-institut.de)
'''

import logging
from . import read_dlr_data as dlr
import dblib as db


def read_re_data(basic_dc, parameter_dc, data_dc):
    '''
    Reads the data series of the renewable energy sources

    Uwe Krien (uwe.krien@rl-institut.de)

    Parameters

    Keyword arguments

    Returns
    '''
    logging.debug('Import re-data')
    re_dc = {}
    if parameter_dc['input']['input_re']['input_re_elec'] in ['default', 'dlr']:
        re_dc['re'] = dlr.get_dlr_data(basic_dc, parameter_dc)
    elif parameter_dc['input']['input_re']['input_re_elec'] in ['aggr']:
        re_dc['re'] = dlr.get_dlr_aggr_data(basic_dc, parameter_dc)
    elif parameter_dc['input']['input_re']['input_re_elec'] in ['db']:
        re_dc['re'] = read_re_from_db(basic_dc, parameter_dc, data_dc)
    return re_dc


def read_re_from_db(basic_dc, p_dc, d_dc):
    ''
    start_hoy = p_dc['simulation']['timestep_start']
    end_hoy = p_dc['simulation']['timestep_end']
    where_str = "hoy>%s and hoy<=%s" % (start_hoy, end_hoy)
    tmp_dc = {}
    for reg in p_dc['energy_system']['energy_system_regions']:
        tmp_dc[reg] = {}
        for c in p_dc['energy_system']['energy_system_re']:
            col = (c + '_' + reg + '_' + str(p_dc['input']['data_year']))
            tmp_dc[reg][c] = db.fetch_columns(basic_dc,
                p_dc['input']['input_re']['schema_re_elec'],
                p_dc['input']['input_re']['table_re_elec'], columns=col,
                as_np=True, orderby='hoy', where_string=where_str)[col]
    return tmp_dc