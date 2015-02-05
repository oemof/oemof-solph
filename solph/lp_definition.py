#!/usr/bin/python
# -*- coding: utf-8 -*-

r"""
**List of lp-variables**


*Electrical power*

:py:func:`power_gen <solph.lp_definition.power_gen_lp_vars>`
    Electrical power generation of all electrical and chp transformer

:py:func:`power_inst <solph.lp_definition.power_gen_lp_vars>`
    Installed capacity of electrical power plants
        * if investment = TRUE

:py:func:`excess <solph.lp_definition.pwr_excess_lp_vars>`
    Power excess due to must-run power generation

:py:func:`ramping_power <solph.lp_definition.power_gen_lp_vars>`
    Ramping power....
        * if ramping_costs defined

:py:func:`excess <solph.lp_definition.heat_excess_lp_vars>`
    Heat excess due to must-run heat generation
        * if heat demand present


*Heat*

:py:func:`heat_gen <solph.lp_definition.heat_gen_lp_vars>`
    Heat generation of all heat and chp transformer
        * if heat demand present

:py:func:`heat_inst <solph.lp_definition.power_gen_lp_vars>`
    Installed capacity of heat and chp plants
        * if investment = TRUE
        * if heat demand present


*Storages*

:py:func:`elec_storage_soc <solph.lp_definition.storage_lp_vars>`
    blubb..
        * if electrical storage present

:py:func:`elec_storage_charge <solph.lp_definition.storage_lp_vars>`
    blubb..
        * if electrical storage present

:py:func:`elec_storage_discharge <solph.lp_definition.storage_lp_vars>`
    blubb..
        * if electrical storage present

:py:func:`elec_storage_inst <solph.lp_definition.storage_lp_vars>`
    blubb..
        * if electrical storage present
        * if investment = TRUE

:py:func:`biogas_storage_soc <solph.lp_definition.biogas_storage_lp_vars>`
    blubb..
        * if resource biogas is present

:py:func:`biogas_storage_inst <solph.lp_definition.biogas_storage_lp_vars>`
    blubb..
        * if resource biogas is present
        * if investment = TRUE


*Transmission lines*

:py:func:`trm_power <solph.lp_definition.trm_sys_lp_vars>`
    blubb..
        * if electrical transmission system present

:py:func:`trline_transfer <solph.lp_definition.trm_sys_lp_vars>`
    blubb..
        * if electrical transmission system present

:py:func:`trm_inst <solph.lp_definition.trm_sys_lp_vars>`
    blubb..
        * if electrical transmission system present
        * if investment = TRUE

_______________________________________________________________________________
"""

import pulp
from . import basic_functions as bm


def power_gen_lp_vars(main_dc):
    '''
    Returns a dictionary containing LP Variables for the electricity sector
    '''
    # LP-Variables for the power output of electricity producing transformers
    main_dc['lp']['power_gen'] = {}
    main_dc['lp']['power_gen']['data'] = pulp.LpVariable.dicts('Feedin_elec', (
        main_dc['energy_system']['transformer']['elec'] +
        main_dc['energy_system']['transformer']['chp'] +
        main_dc['energy_system']['re'] +
        main_dc['energy_system']['chp']['virtuell'],
        bm.get_timesteps(main_dc),
        main_dc['energy_system']['regions']), 0)
    main_dc['lp']['power_gen']['is_series'] = True
    main_dc['lp']['power_gen']['with_regions'] = True

    # LP-Variables for the installed power of electricity producing
    # transformers.
    if main_dc['simulation']['investment'] is True:
        main_dc['lp']['power_inst'] = {}
        main_dc['lp']['power_inst']['data'] = pulp.LpVariable.dicts(
            'InstPower',
            ((main_dc['energy_system']['transformer']['elec']
                + main_dc['energy_system']['re']),
                main_dc['energy_system']['regions']), 0)
        main_dc['lp']['power_inst']['is_series'] = False
        main_dc['lp']['power_inst']['with_regions'] = True

    #ramping

    #ramping costs > 0?
    counter_ramp = 0
    for r in main_dc['energy_system']['regions']:
        for i in main_dc['energy_system']['re']:
            counter_ramp += main_dc['parameter'][
                'component'][r][i]['ramping_costs']
    for r in main_dc['energy_system']['regions']:
        for i in main_dc['energy_system']['transformer']['elec']:
            counter_ramp += main_dc['parameter'][
                'component'][r][i]['ramping_costs']

    if counter_ramp > 0:  # Will only create lp-variables if ramping costs
        main_dc['lp']['ramping_power'] = {}
        main_dc['lp']['ramping_power']['data'] = \
            pulp.LpVariable.dicts('ramping_power', (
            (main_dc['energy_system']['transformer']['elec'] +
            main_dc['energy_system']['re']),
            list(bm.get_timesteps(main_dc)),
            main_dc['energy_system']['regions']))
        main_dc['lp']['ramping_power']['is_series'] = True
        main_dc['lp']['ramping_power']['with_regions'] = True


def pwr_excess_lp_vars(main_dc):
    '''
    Returns a dictionary containing LP Variable for the power excess
    '''
    # LP-Variables for the power excess
    main_dc['lp']['excess'] = {}
    main_dc['lp']['excess']['data'] = pulp.LpVariable.dicts('Excess_elec', (
        ['eexc'], bm.get_timesteps(main_dc),
        main_dc['energy_system']['regions']), 0)
    main_dc['lp']['excess']['is_series'] = True
    main_dc['lp']['excess']['with_regions'] = True


def heat_excess_lp_vars(main_dc):
    '''
    Returns a dictionary containing LP Variable for the power excess
    '''
    # LP-Variables for the power excess
    main_dc['lp']['heat_excess'] = {}
    main_dc['lp']['heat_excess']['data'] = pulp.LpVariable.dicts('Excess_elec',
        (['hexc'], bm.get_timesteps(main_dc),
        main_dc['energy_system']['regions']), 0)
    main_dc['lp']['heat_excess']['is_series'] = True
    main_dc['lp']['heat_excess']['with_regions'] = True


def heat_gen_lp_vars(main_dc):
    '''
    Uwe Krien (uwe.krien@rl-institut.de)

    Returns a dictionary containing LP Variables for the heating sector
    '''
    # LP-Variables for the heat output of heat producing transformers
    main_dc['lp']['heat_gen'] = {}
    main_dc['lp']['heat_gen']['data'] = pulp.LpVariable.dicts('Feedin_heat', (
        main_dc['energy_system']['transformer']['heat'] +
        main_dc['energy_system']['transformer']['chp'],
        bm.get_timesteps(main_dc),
        main_dc['energy_system']['regions']), 0)
    main_dc['lp']['heat_gen']['is_series'] = True
    main_dc['lp']['heat_gen']['with_regions'] = True

    # LP-Variables for the installed power of heat producing transformers
    if main_dc['simulation']['investment'] is True:
        # Remove domestic heating systems from the list.
        # Domestic heating systems do allways have the right capacity to
        # satisfy the domestic heat demand. Additional device like heating rods
        # for domestic systems are not(!) removed.
        heat_ls = ([x for x in list(
            main_dc['energy_system']['transformer']['heat'] +
            main_dc['energy_system']['transformer']['chp'])
            if x not in set(
                main_dc['energy_system']['hc']['domestic'])])
        main_dc['lp']['heat_inst'] = {}
        main_dc['lp']['heat_inst']['data'] = pulp.LpVariable.dicts(
            'InstHeat',
            ((heat_ls + main_dc['energy_system']['transformer']['chp']),
             main_dc['energy_system']['regions']), 0)
        main_dc['lp']['heat_inst']['is_series'] = False
        main_dc['lp']['heat_inst']['with_regions'] = True


def gas_gen_lp_vars(main_dc):
    '''
    Guido Plessmann (guido.plessmann@rl-institut.de)

    Returns a dictionary containing LP Variables for the gas sector
    '''
    # LP-Variables for the gas output of gas producing transformers
    main_dc['lp']['gas_gen'] = {}
    main_dc['lp']['gas_gen']['data'] = pulp.LpVariable.dicts('Feedin_gas', (
        main_dc['energy_system']['transformer'].get('gas', []),
        bm.get_timesteps(main_dc),
        main_dc['energy_system']['regions']), 0)
    main_dc['lp']['gas_gen']['is_series'] = True
    main_dc['lp']['gas_gen']['with_regions'] = True

    # LP-Variables for the installed power of gas producing transformers
    if main_dc['simulation']['investment'] is True:
        main_dc['lp']['gas_inst'] = {}
        main_dc['lp']['gas_inst']['data'] = pulp.LpVariable.dicts('InstGas',
            (main_dc['energy_system']['transformer'].get('gas', []),
            main_dc['energy_system']['regions']),
            0)
        main_dc['lp']['gas_inst']['is_series'] = False
        main_dc['lp']['gas_inst']['with_regions'] = True


def storage_lp_vars(main_dc, storage_type):
    '''
    Returns a dictionary containing storage LP Variables
    '''
    # Extract of lists for shorter calls
    storages = main_dc['energy_system']['storages'][storage_type]
    timesteps = main_dc['timesteps']
    regions = main_dc['energy_system']['regions']

    m = storage_type

    # LP variables creation
    main_dc['lp'][m + '_storage_soc'] = {}
    main_dc['lp'][m + '_storage_charge'] = {}
    main_dc['lp'][m + '_storage_discharge'] = {}
    main_dc['lp'][m + '_storage_soc']['data'] = pulp.LpVariable.dicts(
        m + '_Storage state', (storages, timesteps, regions), 0)
    main_dc['lp'][m + '_storage_soc']['is_series'] = True
    main_dc['lp'][m + '_storage_soc']['with_regions'] = True
    main_dc['lp'][m + '_storage_charge']['data'] = pulp.LpVariable.dicts(
        m + ' Storage charge', (storages, timesteps, regions), 0)
    main_dc['lp'][m + '_storage_charge']['is_series'] = True
    main_dc['lp'][m + '_storage_charge']['with_regions'] = True
    main_dc['lp'][m + '_storage_discharge']['data'] = pulp.LpVariable.dicts(
        m + ' Storage discharge', (storages, timesteps, regions), 0)
    main_dc['lp'][m + '_storage_discharge']['is_series'] = True
    main_dc['lp'][m + '_storage_discharge']['with_regions'] = True
    if main_dc['simulation']['investment'] is True:
        main_dc['lp'][m + '_storage_inst'] = {}
        main_dc['lp'][m + '_storage_inst']['data'] = pulp.LpVariable.dicts(
            m + ' InstPower_stor', (storages, regions), 0)
        main_dc['lp'][m + '_storage_inst']['is_series'] = False
        main_dc['lp'][m + '_storage_inst']['with_regions'] = True


def biogas_storage_lp_vars(main_dc):
    '''
    Returns a dictionary containing gas storage LP Variables
    '''
    # Extract of lists for shorter calls
    timesteps = bm.get_timesteps(main_dc)
    regions = main_dc['energy_system']['regions']
    storages = ['sbig']

    # LP variables creation
    main_dc['lp']['biogas_storage_soc'] = {}
    main_dc['lp']['biogas_storage_soc']['data'] = pulp.LpVariable.dicts(
        'Biogas storage state', (storages, timesteps, regions), 0)
    main_dc['lp']['biogas_storage_soc']['is_series'] = True
    main_dc['lp']['biogas_storage_soc']['with_regions'] = True

    if main_dc['simulation']['investment'] is True:
        main_dc['lp']['biogas_storage_inst'] = {}
        main_dc['lp']['biogas_storage_inst']['data'] = pulp.LpVariable.dicts(
            'InstPower_biogas_stor', (storages, regions), 0)
        main_dc['lp']['biogas_storage_inst']['is_series'] = False
        main_dc['lp']['biogas_storage_inst']['with_regions'] = True


def trm_sys_lp_vars(main_dc):
    '''
    Returns a dictionary containing transmission system LP Variables
    '''
    # Extract of lists for shorter calls
    timesteps = bm.get_timesteps(main_dc)
    lines = main_dc['energy_system']['transmission']
    regions = main_dc['energy_system']['regions']

    # LP variables creation
    main_dc['lp']['trline_transfer'] = {}
    main_dc['lp']['trm_power'] = {}
    main_dc['lp']['trline_transfer']['data'] = {}
    main_dc['lp']['trline_transfer']['data']['neg'] = pulp.LpVariable.dicts(
        'Transmission line power neg', (lines, timesteps), 0)
    main_dc['lp']['trline_transfer']['data']['pos'] = pulp.LpVariable.dicts(
        'Transmission line power pos', (lines, timesteps), 0)
    main_dc['lp']['trline_transfer']['is_series'] = True
    main_dc['lp']['trline_transfer']['with_regions'] = False
    main_dc['lp']['trm_power']['data'] = pulp.LpVariable.dicts('Transmission',
        (regions, timesteps), None)
    main_dc['lp']['trm_power']['is_series'] = True
    main_dc['lp']['trm_power']['with_regions'] = False

    # installed grid power
    main_dc['lp']['trm_inst'] = {}
    main_dc['lp']['trm_inst']['is_series'] = False
    main_dc['lp']['trm_inst']['with_regions'] = False
    main_dc['lp']['trm_inst']['data'] = pulp.LpVariable.dicts(
    'Transmission_inst', (lines), None)


def resources_lp_vars(main_dc):
    '''
    Returns a dictionary containing resources LP Variables
    '''
    # Extract of lists for shorter calls
    timesteps = bm.get_timesteps(main_dc)
    regions = main_dc['energy_system']['regions']
    #ptg = main_dc['energy_system']['energy_system_transformer4gas']
    #ren_share = main_dc['input']['input_general']['re_share']
    gas_pp = ([x for x in (main_dc['energy_system']
        ['transformer']['elec']) if x in ['tocg', 'tccg']])

    # LP variables creation
    main_dc['lp']['fossil_resources'] = {}
    main_dc['lp']['fossil_resources']['is_series'] = True
    main_dc['lp']['fossil_resources']['with_regions'] = True
    main_dc['lp']['fossil_resources']['data'] = pulp.LpVariable.dicts(
        'Resource_act_', ((list(main_dc['energy_system']['resources'].keys())),
            timesteps, regions), 0)

    if main_dc['check']['extend_nat_gas_bus']:
        main_dc['lp']['splitted_gas_flow'] = {}
        main_dc['lp']['splitted_gas_flow']['is_series'] = True
        main_dc['lp']['splitted_gas_flow']['with_regions'] = True
        if gas_pp:
            main_dc['lp']['splitted_gas_flow']['data'] = (
                pulp.LpVariable.dicts(
                'Splitted_fos_gas', (gas_pp, timesteps, regions), 0))


def ptg_lp_vars(main_dc):
    '''Creates LP variables for power to gas: Input power and installed
    capacity of ptg plants. '''

    # Extract of lists for shorter calls
    timesteps = bm.get_timesteps(main_dc)
    regions = main_dc['energy_system']['regions']
    r0 = main_dc['parameter']['component'].keys()[0]
    gas_consumer_list = []

    # creates list of gas power plants
    for c in main_dc['parameter']['component'][r0].keys():
        if main_dc['parameter']['component'][r0][c]['type'] == 'transformer':
            if (main_dc['parameter']['component'][r0][c]['out'] == 'elec' and
                main_dc['parameter']['component'][r0][c]['resources'] ==
                    'rnga'):
                gas_consumer_list.append(c)

    # synthetic gas flows
    if 'tptg' in (main_dc['energy_system']
            ['transformer']['gas']):
        main_dc['lp']['sng_resources'] = {}
        main_dc['lp']['sng_resources']['is_series'] = True
        main_dc['lp']['sng_resources']['with_regions'] = True
        main_dc['lp']['sng_resources']['data'] = (
                pulp.LpVariable.dicts('Resource_act_tocg_sng',
                (gas_consumer_list, timesteps, regions), 0))


def info_lp_vars(main_dc):
    '''
    Create a key in the lp_vars/ results_dcionary containing meta info about
    the simulation in order to write this into the data base'''

    main_dc['lp']['info'] = {}
    main_dc['lp']['info']['is_series'] = False
    main_dc['lp']['info']['with_regions'] = False
    main_dc['lp']['info']['data'] = {}


def create_lp_vars_dc(main_dc):
    '''
    Returns a dictionary containing all LP Variables
    '''
    main_dc['lp'] = {}
    info_lp_vars(main_dc)
    power_gen_lp_vars(main_dc)
    resources_lp_vars(main_dc)
    pwr_excess_lp_vars(main_dc)

    if main_dc['check']['heat']:
        heat_gen_lp_vars(main_dc)
        heat_excess_lp_vars(main_dc)

    if 'elec' in main_dc['energy_system']['storages']:
        storage_lp_vars(main_dc, 'elec')

    if 'heat' in main_dc['energy_system']['storages']:
        storage_lp_vars(main_dc, 'heat')

    if main_dc['energy_system']['transmission']:
        trm_sys_lp_vars(main_dc)

    # Condition is only valid if ptg is the only component in transformer4gas
    if 'gas' in main_dc['energy_system']['transformer']:
        ptg_lp_vars(main_dc)
        gas_gen_lp_vars(main_dc)

    if 'gas' in main_dc['energy_system']['storages']:
        storage_lp_vars(main_dc, 'gas')

    if main_dc['check']['biogas']:
        biogas_storage_lp_vars(main_dc)
