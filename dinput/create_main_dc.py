#!/usr/bin/python
# -*- coding: utf-8

import logging
from types import *


def dict_from_parameter_dc(parameter_dc, main_dc):
    'Moves all data from parameter_dc to main_dc.'
    logging.debug('Moving data from parameter_dc to main_dc')

    # extract from parameter_dc for later use in main_dc
    tmp_p_set = parameter_dc['presetting']['name_data_set']
    tmp_e_system = parameter_dc['energy_system']['name_set']

    parameter_dc.pop('energy_system', None)
    main_dc['parameter'] = {}
    del_ls = ['changed_by', 'id', 'lastmodified', 'name', 'name_set', 'source',
        'region', 'description']

    # Create parameter-branch
    for key in list(parameter_dc['parameter'].keys()):
        if 'parameter' in key:
            nkey = key.replace('parameter_', '')
            main_dc['parameter'][nkey] = parameter_dc['parameter'][key]
            for a in list(main_dc['parameter'][nkey].keys()):
                for b in list(main_dc['parameter'][nkey][a].keys()):
                    if b in del_ls:
                        main_dc['parameter'][nkey][a].pop(b, None)
                    elif type(main_dc['parameter'][nkey][a][b]) is DictType:
                        for c in list(main_dc['parameter'][nkey][a][b].keys()):
                            if c in del_ls:
                                main_dc['parameter'][nkey][a][b].pop(c, None)
    main_dc['parameter'].pop('regions', None)

    # Create simulation branch
    main_dc['simulation'] = dict(parameter_dc['input']['input_simtype'])
    main_dc['simulation'].update(dict(parameter_dc['input']['input_general']))
    main_dc['simulation'].update(parameter_dc['simulation'])
    for key in list(main_dc['simulation'].keys()):
        if key in del_ls:
            main_dc['simulation'].pop(key, None)

    # Remove branches from parameter_dc
    parameter_dc.pop('parameter', None)
    parameter_dc.pop('energy_system', None)
    parameter_dc.pop('presetting', None)
    parameter_dc.pop('simulation', None)
    parameter_dc.pop('plot', None)
    parameter_dc.pop('lists', None)
    parameter_dc.pop('input', None)

    # Create info branch
    main_dc['info'] = parameter_dc
    main_dc['info']['sim_year'] = main_dc['simulation'].pop('sim_year', None)
    main_dc['info']['presetting_set'] = tmp_p_set
    main_dc['info']['energy_system'] = tmp_e_system
    del parameter_dc

    repair_transmission_branch(main_dc, del_ls)


def dict_from_basic_dc(basic_dc, main_dc):
    'Moves all data from basic_dc to main_dc.'
    logging.debug('Moving data from basic_dc to main_dc')

    # Create check branch
    if 'check' in basic_dc:
        main_dc['check'].update(basic_dc.pop('check', None))

    main_dc['simulation']['initpath'] = basic_dc['initpath']


def dict_from_data_dc(data_dc, main_dc):
    'Moves all data from basic_dc to main_dc.'
    logging.debug('Moving data from data_dc to main_dc')
    # Adds presetting and cap to the parameter branch.
    for key in list(main_dc['parameter'].keys()):
        for r in list(main_dc['parameter'][key].keys()):
            for t in list(main_dc['parameter'][key][r]):
                if t in list(data_dc['cap'].keys()):
                    for r in list(data_dc['cap'][t].keys()):
                        main_dc['parameter'][key][r][t]['capacity_limit'] = (
                            data_dc['cap'][t][r])
                if t in list(data_dc['presetting'].keys()):
                    for r in list(data_dc['presetting'][t].keys()):
                        (main_dc['parameter'][key][r][t]['installed_capacity']
                            ) = data_dc['presetting'][t][r]
    data_dc.pop('cap', None)
    data_dc.pop('presetting', None)

    # Creates timeseries branch
    main_dc['timeseries'] = {}
    main_dc['timeseries']['demand'] = {}
    main_dc['timeseries']['feedin'] = {}
    if main_dc['switch']['read_demand_data']:
        if 'demand_elec' in list(data_dc.keys()):
            main_dc['timeseries']['demand'].update(data_dc['demand_elec'])
        if 'demand_heat' in list(data_dc.keys()):
            for r in list(data_dc['demand_heat'].keys()):
                main_dc['timeseries']['demand'][r].update(
                    data_dc['demand_heat'][r])
    if main_dc['switch']['read_demand_data']:
        if 're' in list(data_dc.keys()):
            main_dc['timeseries']['feedin'].update(data_dc['re'])


def restructure_component_parameter(main_dc):
    '''
    The parameter of all components are now in one branch.
    To distinguish the types a field "type" and a field "out" are added
    '''
    type_ls = ['storages4biogas', 'storages4elec', 'transformer4gas',
        're', 'transformer4heat', 'transformer4chp', 'transformer4elec',
        'storages4gas']
    main_dc['parameter']['component'] = {}
    for t in type_ls:
        for r in list(main_dc['parameter'][t].keys()):
            if main_dc['parameter'][t][r]:
                if r not in main_dc['parameter']['component']:
                    main_dc['parameter']['component'][r] = {}
                main_dc['parameter']['component'][r].update(
                    main_dc['parameter'][t][r])
                for c in list(main_dc['parameter'][t][r].keys()):
                    if t is not 're':
                        [ctype, out] = t.split('4')
                        main_dc['parameter']['component'][r][c]['out'] = out
                    else:
                        ctype = 're'
                    main_dc['parameter']['component'][r][c]['type'] = ctype
                    if ctype == 'storages':
                        main_dc['parameter']['component'][r][c]['medium'] = (
                            main_dc['parameter']['component'][r][c].pop('out'))
        main_dc['parameter'].pop(t)


def repair_transmission_branch(main_dc, del_ls):
    'Purges an obsolete branch.'
    for r in list(main_dc['parameter']['transmission'].keys()):
        main_dc['parameter']['transmission'][r].update(
            main_dc['parameter']['transmission'][r].pop(
                'parameter_transmission_type'))
        for key in list(main_dc['parameter']['transmission'][r].keys()):
            if key in del_ls:
                main_dc['parameter']['transmission'][r].pop(key, None)


def create(basic_dc, parameter_dc, data_dc, main_dc):
    'Creates main_dc and moves the data from the existing dicts to main_dc.'

    dict_from_parameter_dc(parameter_dc, main_dc)
    dict_from_basic_dc(basic_dc, main_dc)
    dict_from_data_dc(data_dc, main_dc)
    restructure_component_parameter(main_dc)