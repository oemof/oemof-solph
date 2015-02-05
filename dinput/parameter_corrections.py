#!/usr/bin/python
# -*- coding: utf-8

'''
Author: Uwe Krien (uwe.krien@rl-institut.de)
Changes by:
Responsibility: Uwe Krien (uwe.krien@rl-institut.de)
'''


def correct_timestep(parameter_dc):
    '''
    The time range of a year is from 1 to 8760 hours.
    Python works from 0 to 8759. This function corrects this difference.
    '''
    parameter_dc['simulation']['timestep_start'] = (
        parameter_dc['simulation']['timestep_start'] - 1)


def correct_parameters(parameter_dc):
    '''
    This function corrects parameters, that need to be corrected.
    '''
    correct_timestep(parameter_dc)


def adapt_transformer_list(basic_dc, p_dc):
    '''
    Remove heat_transformers from transformer_tables,
    if there are no heat_transformers present
    '''
    number_keys = len(basic_dc['transformer_keys'])
    if not (p_dc['energy_system']['energy_system_transformer4heat'] or
            p_dc['energy_system']['energy_system_transformer4chp']):
        basic_dc['existing_transf_keys'] = ([basic_dc['transformer_keys'][n]
            for n in list(range(number_keys)) if basic_dc['transformer_keys'][n]
            not in basic_dc['heat_transformer_keys']])