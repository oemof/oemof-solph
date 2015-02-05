#!/usr/bin/python
# -*- coding: utf-8

import logging
from . import basic_functions as bm


def create_energy_system_branch(main_dt):
    'Creates the energy_system branch.'
    main_dt['energy_system'] = {}
    main_dt['energy_system']['all'] = {}
    main_dt['energy_system']['all']['components'] = []
    main_dt['energy_system']['regions'] = list(
        main_dt['parameter']['component'].keys())
    main_dt['energy_system']['transmission'] = list(
        main_dt['parameter']['transmission'].keys())
    r0 = main_dt['energy_system']['regions'][0]
    for c in list(main_dt['parameter']['component'][r0].keys()):
        ct = main_dt['parameter']['component'][r0][c]['type']
        if ct == 'transformer':
            if 'transformer' not in list(main_dt['energy_system'].keys()):
                main_dt['energy_system']['transformer'] = {}
            if 'transformer' not in list(
                    main_dt['energy_system']['all'].keys()):
                main_dt['energy_system']['all']['transformer'] = []
            main_dt['energy_system']['all']['transformer'].extend([c, ])
            cout = main_dt['parameter']['component'][r0][c]['out']
            if cout not in list(
                    main_dt['energy_system']['transformer'].keys()):
                main_dt['energy_system']['transformer'][cout] = []
            main_dt['energy_system']['transformer'][cout].extend([c, ])
        if ct == 'storages':
            if 'storages' not in list(main_dt['energy_system'].keys()):
                main_dt['energy_system']['storages'] = {}
            if 'storages' not in list(
                    main_dt['energy_system']['all'].keys()):
                main_dt['energy_system']['all']['storages'] = []
            main_dt['energy_system']['all']['storages'].extend([c, ])
            cout = main_dt['parameter']['component'][r0][c]['medium']
            if cout not in list(
                    main_dt['energy_system']['storages'].keys()):
                main_dt['energy_system']['storages'][cout] = []
            main_dt['energy_system']['storages'][cout].extend([c, ])
        if ct == 're':
            if 're' not in list(main_dt['energy_system'].keys()):
                main_dt['energy_system']['re'] = []
            main_dt['energy_system']['re'].extend([c, ])
        main_dt['energy_system']['all']['components'].extend([c, ])
    main_dt['energy_system']['all']['elec_comp'] = (
        main_dt['energy_system']['transformer'].get('elec', []) +
        main_dt['energy_system']['storages'].get('elec', []) +
        main_dt['energy_system'].get('re', []))
    main_dt['energy_system']['resources'] = {}
    for res in list(main_dt['parameter']['resources'][r0].keys()):
        main_dt['energy_system']['resources'][res] = {}


def create_lists_resources2plant(main_dt):
    '''
    Creates a list for every resource that contains the power plants,
    which need this resource, sorted by the type (elec, heat, chp...).

    Returns:
    main_dt['energy_system']['resources2plant'][resource][type]
    (with type in ['elec', 'heat, 'chp',...])
    main_dt['energy_system']['resources2plant'][resource]['all']
    (for all types)
    '''
    for i in list(main_dt['energy_system']['resources'].keys()):
        main_dt['energy_system']['resources'][i] = {}
        main_dt['energy_system']['resources'][i]['all'] = []
        r0 = main_dt['energy_system']['regions'][0]
        for key in list(main_dt['energy_system']['transformer']):
            main_dt['energy_system']['resources'][i][key] = []
            for t in main_dt['energy_system']['transformer'][key]:
                if main_dt['parameter']['component'][r0][t]['resources'] == i:
                    main_dt['energy_system']['resources'][i][key].extend([t],)
                    main_dt['energy_system']['resources'][i]['all'].extend(
                        [t],)


def create_lists_heat_classes(main_dt):
    '''
    Returns two list with heating transformers. One with domestic transformers
    and one with transformers for district heating.
    Moreover the efficiency4heat and the resource for each component from
    above.

    Uwe Krien (uwe.krien@rl-institut.de)

    Returns
    Lists of components for district or domestic heating:
        main_dt['energy_system']['district']
        main_dt['energy_system']['domestic']
    Dictionaries with the efficiency4heat and the ressource for each component.
        main_dt['energy_system']['eff4heat']
        main_dt['energy_system']['resource']
    '''
    # Define subtree of main_dt
    main_dt['energy_system'].setdefault('hc', {})

    # One region to get the parameters.
    r0 = main_dt['energy_system']['regions'][0]

    # Sorts the heat transformers to the different classes.
    c_list = (main_dt['energy_system']['transformer']['heat'] +
              main_dt['energy_system']['transformer']['chp'])
    for c in c_list:
        if main_dt['parameter']['component'][r0][c][
                'heat_class'] not in main_dt['energy_system']['hc']:
            main_dt['energy_system']['hc'].setdefault(
                main_dt['parameter']['component'][r0][c]['heat_class'], [])
        main_dt['energy_system']['hc'][main_dt['parameter']['component'][r0][c]
                                       ['heat_class']].extend([c, ])

    # Sorts all storages for heat to the associated heating system
    for c in main_dt['energy_system']['storages']['heat']:
        main_dt['energy_system'].setdefault('hstorage2system', {})
        main_dt['energy_system']['hstorage2system'][
            main_dt['parameter']['component'][r0][c]['heating_system']] = c


def create_list_chp_types(main_dt):
    '''
    Creates list for the different types of chp (variable and fixed ratio) and
    a list of virtuell transformers for variable chp plants.
    The virtuell transformer represents the electricity-only-mode of the chp
    plant and starts with a 'v' instead of a 't' (tcga -> vcga).
    The 'dict' translates between these names.

    Uwe Krien (uwe.krien@rl-institut.de)
    '''
    # Defines the empty lists and dicts.
    main_dt['energy_system'].setdefault('chp', {})
    main_dt['energy_system']['chp']['variable'] = []
    main_dt['energy_system']['chp']['virtuell'] = []
    main_dt['energy_system']['chp']['fixed'] = []
    main_dt['energy_system']['chp']['dict'] = {}

    # One region to get the parameters.
    r0 = main_dt['energy_system']['regions'][0]

    # Sorts the chp transformer to the different lists.
    for c in main_dt['energy_system']['transformer']['chp']:
        if (main_dt['parameter']['component'][r0][c]['hp_ratio_type'] ==
                'variable'):
            main_dt['energy_system']['chp']['variable'].extend([c],)
            main_dt['energy_system']['chp']['dict'][c] = 'v' + c[1:]
            main_dt['energy_system']['chp']['virtuell'].extend(['v' + c[1:]],)
        elif (main_dt['parameter']['component'][r0][c]['hp_ratio_type'] ==
                'fixed'):
            main_dt['energy_system']['chp']['fixed'].extend([c],)
        else:
            logging.error(
                'HP_ratio_type for {0} must be "fixed" or "variable"'.format(
                    c))


def create_list_storages4biogas(param_dc):
    '''
    Adds a biogas storage to the energy_system if biogas (rbig) is present.
    '''

    if 'rbig' in param_dc['energy_system']['energy_system_resources']:
        param_dc['energy_system']['storages']['biogas'] = ['sbig']
        param_dc['energy_system']['energy_system_storages'].extend(['sbig'])
        param_dc['energy_system']['energy_system_components'].extend(['sbig'])
    else:
        param_dc['energy_system']['energy_system_storages4biogas'] = []


def create_heat_parts(main_dt):
    '''
    Creates the branches for the heat part if present.
    '''
    main_dt['energy_system']['transformer'].setdefault('heat', [])
    main_dt['energy_system']['transformer'].setdefault('chp', [])
    for i in list(main_dt['energy_system']['resources'].keys()):
        main_dt['energy_system']['resources'][i].setdefault('heat', [])
        main_dt['energy_system']['resources'][i].setdefault('chp', [])
    create_lists_heat_classes(main_dt)
    create_list_chp_types(main_dt)


def calc_installed_cap_domestic_heat(main_dt):
    ''
    for c in main_dt['energy_system']['hc']['domestic']:
        for r in main_dt['energy_system']['regions']:
            main_dt['parameter']['component'][r][c]['installed_capacity'] = (
                max(main_dt['timeseries']['demand'][r][c]) /
                main_dt['simulation']['simultaneity_domestic_heat'])


def extend(main_dt):
    'Creates main_dt and moves the data from the existing dicts to main_dt.'
    logging.debug('Extending main_dt...')
    main_dt['timesteps'] = bm.get_timesteps(main_dt)
    create_energy_system_branch(main_dt)
    create_lists_resources2plant(main_dt)
    create_heat_parts(main_dt)
    calc_installed_cap_domestic_heat(main_dt)