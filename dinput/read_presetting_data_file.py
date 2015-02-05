#!/usr/bin/python
# -*- coding: utf-8 -*-


'''
Author: Finn Grohmann
E-mail: finn.grohmann@ri-institut.de
Changes by: Uwe Krien (uwe.krien@rl-institut.de)
Responsibility: Finn Grohmann, Guido Plessmann
'''

import logging
import dblib as db
#from ..basic import checker_fkts as cfcn


def read_presetting_and_cap_data(basic_dc, parameter_dc):
    '''
    Reads presetting and cap data from the data schema.

    by Uwe Krien (uwe.krien@rl-institut.de)
    Responsibility: Guido Plessmann

    Parameters
        basic_dc : basic parameters : dictionary
        parameter_dc : parameters : dictionary

    Returns
        dictionary with data : dictionary
        keys:
            ['presetting'][component][region]
            ['cap'][component][region]
    '''
    presetting_dc = {}
    presetting_dc['presetting'] = {}
    presetting_dc['cap'] = {}
    for c in parameter_dc['energy_system']['energy_system_components']:
        presetting_dc['presetting'][c] = {}
        presetting_dc['cap'][c] = {}
        for r in parameter_dc['energy_system']['energy_system_regions']:
            # Trys to read presetting and cap data
            where_str = ("presetting_set=" +
                "'{0}' AND component='{1}' AND region='{2}'".format(
                parameter_dc['presetting']['name_data_set'], c, r))
            tmp_val = db.fetch_columns(basic_dc, basic_dc['dat_schema'],
                'presetting', ['eoo_year'],
                where_string=where_str)
            if parameter_dc['input']['input_general']['sim_year']:
                if not ((tmp_val['eoo_year'] == []) or (tmp_val['eoo_year']
                    == [None])):
                    tmp_val = {}
                    for d in ['presetted_summed_power', 'cap']:
                        sel_str = '''select sum({4}) from
                            pahesmf_dat.presetting where presetting_set = '{0}'
                            and eoo_year >= {1} and region = '{2}'
                            and component = '{3}';'''.format(
                                parameter_dc['presetting']['name_data_set'],
                                parameter_dc['input']['input_general']
                                ['sim_year'], r, c, d)
                        tmp_val[d] = db.execute_read_db(basic_dc, sel_str)[0]
                else:
                    tmp_val = db.fetch_columns(basic_dc, basic_dc['dat_schema'],
                    'presetting', ['presetted_summed_power', 'cap'],
                    where_string=where_str)
            else:
                tmp_val = db.fetch_columns(basic_dc, basic_dc['dat_schema'],
                    'presetting', ['presetted_summed_power', 'cap'],
                    where_string=where_str)

            # Set presetting to zero if not set.
            if not tmp_val['presetted_summed_power']:
                logging.warning('Missing presetting value for' +
                    ' "{0}" in "{1}" is set to zero.'.format(c, r))
                presetting_dc['presetting'][c][r] = 0
            else:
                presetting_dc['presetting'][c][r] = (
                    tmp_val['presetted_summed_power'][0])

            # Set cap to empty list if not set or investment=False
            if not tmp_val['cap'] or tmp_val['cap'] == [None] or not (
                parameter_dc['input']['input_simtype']['investment']):
                presetting_dc['cap'][c][r] = []
            else:
                presetting_dc['cap'][c][r] = tmp_val['cap'][0]
    return presetting_dc