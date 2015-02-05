#!/usr/bin/python
# -*- coding: utf-8

'''
Author: Uwe Krien (uwe.krien@rl-institut.de)
Changes by:
Responsibility: Uwe Krien (uwe.krien@rl-institut.de)
'''

import dblib as system
from . import create_lists_file as clf
from . import read_parameter_tables_file as rpt
from . import parameter_corrections as cor
from . import read_re_data_file as rre
from .read_demand_data_file import *
from .read_presetting_data_file import *
from .parameter_py_file import *
from . import create_main_dc as maindc


def read_basic_dc(overwrite=True, failsafe=False):
    '''
    Reads the basic parameters from two files and writes them into a dictionary
    One file is related to your computer, the other is placed in this package.

    by Uwe Krien (uwe.krien@rl-institut.de)

    Returns:
        basic_dc : dictionary
    '''
    system_dc = system.get_basic_dc()
    basic_dc = system_dc.pop('basic', None)
    basic_dc.update(extend_basic_dc(basic_dc))
    basic_dc['overwrite'] = overwrite
    basic_dc['failsafe'] = failsafe
    return basic_dc


def parameter_from_db(var, main_dc, overwrite=True, failsafe=False):
    '''
    Reads all parameters from the database.

    by Uwe Krien (uwe.krien@rl-institut.de)

    Parameters
        basic_dc : basic parameters : dictionary
        var : name or id of the chosen scenario : str/int

    Returns
        dictionary with all parameters : dictionary
    '''
    logging.info('Reading parameters from DB...')
    basic_dc = read_basic_dc(overwrite=True, failsafe=False)
    var_type = system.check_parameter(var)
    parameter_dc = dict(db.fetch_row(basic_dc, basic_dc['schema'],
                                     basic_dc['start_table'], var_type, var))
    clf.create_lists(basic_dc, parameter_dc)
    rpt.read_parameter_tables(basic_dc, parameter_dc)
    cor. correct_parameters(parameter_dc)
    cor. adapt_transformer_list(basic_dc, parameter_dc)
    clf.create_post_lists(basic_dc, parameter_dc)
    data_dc = read_data(basic_dc, parameter_dc, main_dc)
    maindc.create(basic_dc, parameter_dc, data_dc, main_dc)


def read_data(basic_dc, parameter_dc, main_dc):
    '''
    Reads all data sets from the database.

    by Uwe Krien (uwe.krien@rl-institut.de)

    Parameters
        basic_dc : basic parameters : dictionary
        parameter_dc : parameters : dictionary

    Returns
        dictionary with data : dictionary
        keys:
            ['demand_elec'][region][timestep] : time series with hourly
                electrical demand per region
            ['demand_elec_total_all'] : yearly demand over all regions
    '''
    data_dc = {}
    if main_dc['switch']['read_demand_data']:
        data_dc.update(read_demand_data(basic_dc, parameter_dc))
    data_dc.update(read_presetting_and_cap_data(basic_dc, parameter_dc))
    if main_dc['switch']['read_re_data']:
        data_dc.update(rre.read_re_data(basic_dc, parameter_dc, data_dc))
    return data_dc
