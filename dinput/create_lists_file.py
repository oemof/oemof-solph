#!/usr/bin/python
# -*- coding: utf-8

'''
Author: Uwe Krien
Changes by:
'''

import logging
from . import basic_dinput_functions as rb
import dblib as db
from . import basic_dinput_functions as bf


def fetch_vertical_list(name_set, basic_dc, esys_dc, table,
        basic_name_set='default'):
    '''

    Parameters
    ----------

    Keyword arguments
    -----------------

    Returns
    -------

    '''
    str_list = []
    str_list.append("(name_set='%s' and active='t')" % basic_name_set)
    str_list.append("(name_set='%s' and active='f')" % name_set)
    str_list.append("(name_set='%s' and active='t')" % name_set)
    for i in range(len(str_list)):
        str_list[i] = db.fetch_columns(basic_dc,
            basic_dc['schema'],
            table,
            columns='name',
            where_string=str_list[i])['name']
    line_list = bf.remove_from_list(str_list[0], str_list[1])
    line_list.extend(str_list[2])
    seen = set()
    esys_dc[table] = (
        [x for x in line_list if x not in seen and not seen.add(x)])


def fetch_row_list(name_set, basic_dc, esys_dc, table):
    '''

    Parameters
    ----------

    Keyword arguments
    -----------------

    Returns
    -------

    '''
    data_row = db.fetch_row(basic_dc, basic_dc['schema'], table,
        where_column='name_set', where_condition=name_set)
    tmp_list = []
    for key in list(data_row.keys()):
        if data_row[key] is True:
            tmp_list.append(key)
    esys_dc[table] = tmp_list


def combine_lists(esys_dc, in_list):
    '''
    '''
    out_list = []
    for part in in_list:
        table = 'energy_system_' + part
        if table in esys_dc:
            out_list.extend(esys_dc[table])
    return list(out_list)


def add_list_collections(basic_dc, esys_dc):
    '''
    Combines same lists to new ones
    '''
    # list of all transformers
    list_transformer = []
    for key in basic_dc['transformer_keys']:
        list_transformer.extend(['transformer4' + key],)
    esys_dc['energy_system_transformer'] = combine_lists(
        esys_dc, list_transformer)

    # list of all storages
    list_storages = []
    for key in basic_dc['storage_keys']:
        list_storages.extend(['storages4' + key],)
    esys_dc['energy_system_storages'] = combine_lists(
        esys_dc, list_storages)

    # list of all components of the energy system
    esys_dc['energy_system_components'] = (esys_dc['energy_system_storages'] +
        esys_dc['energy_system_transformer'] + esys_dc['energy_system_re'])


def create_lists_resources(basic_dc, parameter_dc):
    '''
    Analyse all transformer for the needed resources.

    Uwe Krien (uwe.krien@rl-institut.de)

    Returns:
    parameter_dc['energy_system']['resources']
    '''
    tmp_ls = []
    for table_key in basic_dc['transformer_keys']:
        table_name = 'parameter_transformer4' + table_key
        t2r = db.fetch_columns(basic_dc, basic_dc['schema'], table_name,
            columns=['name', 'resources'], where_column='name_set',
            where_condition='default', orderby='id')
        for n in xrange(len(t2r['name'])):
            if t2r['name'][n] in list(
                    parameter_dc['energy_system']['energy_system_transformer4' +
                    table_key]):
                tmp_ls.extend([t2r['resources'][n], ])
    if 'none' in tmp_ls:
        tmp_ls.remove('none')
    parameter_dc['energy_system']['energy_system_resources'] = (
        bf.unique_list(tmp_ls))


def create_lists(basic_dc, parameter_dc):
    '''

    Parameters
    ----------

    Keyword arguments
    -----------------

    Returns
    -------

    '''
    #Reads energy system for the given scenario
    esys_dc = dict(db.fetch_row(basic_dc, basic_dc['schema'],
        basic_dc['energy_system_table'],
        where_column='name_set',
        where_condition=parameter_dc[basic_dc['energy_system_table']]))

    #Removes the non-content columns and creates table list
    table_list = bf.remove_from_list(list(esys_dc.keys()),
        basic_dc['remove_columns'])

    #Reads the list for all subtables and adds it to the parameter_dc
    for table in table_list:
        table_type = rb.check_table_structure(basic_dc, table)
        if table_type == 'vertical':
            fetch_vertical_list(esys_dc[table], basic_dc, esys_dc, table)
            logging.debug('{tab}: {lst}'.format(tab=table, lst=esys_dc[table]))
        elif table_type == 'row':
            fetch_row_list(esys_dc[table], basic_dc, esys_dc, table)
            logging.debug('{tab}: {lst}'.format(tab=table, lst=esys_dc[table]))
        else:
            logging.warning('Something is wrong in the energy_system structure')

    #Add collection lists
    add_list_collections(basic_dc, esys_dc)

    #Dock the sub-dictionary to the parameter_dc
    parameter_dc[basic_dc['energy_system_table']] = esys_dc
    create_lists_resources(basic_dc, parameter_dc)
    create_list_storages4biogas(parameter_dc)
    logging.debug('Lists of the energy system created')


def create_lists_resources2plant(basic_dc, parameter_dc):
    '''
    Creates a list for every resource that contains the power plants,
    which need this resource, sorted by the type (elec, heat, chp...).

    Returns:
    parameter_dc['lists']['resources2plant'][resource][type]
    (with type in ['elec', 'heat, 'chp',...])
    parameter_dc['lists']['resources2plant'][resource]['all']
    (for all types)
    '''
    parameter_dc['lists']['resources2plant'] = {}
    for i in list(parameter_dc['energy_system']['energy_system_resources']):
        parameter_dc['lists']['resources2plant'][i] = {}
        parameter_dc['lists']['resources2plant'][i]['all'] = []
        for table_key in basic_dc['transformer_keys']:
            table_p = "parameter_transformer4" + table_key
            table_e = "energy_system_transformer4" + table_key
            where_str = "resources='%s' and name_set='default'" % i
            comp_list = db.fetch_columns(basic_dc, basic_dc['schema'], table_p,
                columns='name', where_string=where_str)['name']
            parameter_dc['lists']['resources2plant'][i][table_key] = (
                bf.cut_lists(comp_list, parameter_dc['energy_system'][table_e]))
            parameter_dc['lists']['resources2plant'][i]['all'].extend((
                parameter_dc['lists']['resources2plant'][i][table_key]))


def create_lists_heat_classes(basic_dc, parameter_dc):
    '''
    Returns two list with heating transformers. One with domestic transformers
    and one with transformers for district heating.
    Moreover the efficiency4heat and the resource for each component from above.

    Uwe Krien (uwe.krien@rl-institut.de)

    Returns
    Lists of components for district or domestic heating:
        parameter_dc['lists']['district']
        parameter_dc['lists']['domestic']
    Dictionaries with the efficiency4heat and the ressource for each component.
        parameter_dc['lists']['eff4heat']
        parameter_dc['lists']['resource']
    '''
    # Defines the empty lists and dicts.
    parameter_dc['lists']['district'] = []
    parameter_dc['lists']['domestic'] = []
    parameter_dc['lists']['eff4heat'] = {}
    parameter_dc['lists']['resource'] = {}
    parameter_dc['lists']['thoi'] = []
    parameter_dc['lists']['thng'] = []
    parameter_dc['lists']['twcb'] = []

    # One region to get the parameters.
    reg0 = parameter_dc['energy_system']['energy_system_regions'][0]

    #Sorts the heat transformers to the different classes.
    for comp in basic_dc['heat_transformer_keys']:
        comp = 'transformer4' + comp
        for c in parameter_dc['energy_system']['energy_system_' + comp]:
            heat_class = (parameter_dc['parameter']['parameter_' + comp][reg0]
                [c]['heat_class'])
            parameter_dc['lists'][heat_class].extend([c, ])
            parameter_dc['lists']['eff4heat'][c] = (parameter_dc['parameter']
                ['parameter_' + comp][reg0][c]['efficiency4heat'])
            parameter_dc['lists']['resource'][c] = (parameter_dc['parameter']
                ['parameter_' + comp][reg0][c]['resources'])


def creat_list_chp_types(basic_dc, parameter_dc):
    '''
    Creates list for the different types of chp (variable and fixed ratio) and
    a list of virtuell transformers for variable chp plants.
    The virtuell transformer represents the electricity-only-mode of the chp
    plant and starts with a 'v' instead of a 't' (tcga -> vcga).
    The 'dict' translates between these names.

    Uwe Krien (uwe.krien@rl-institut.de)
    '''
    # Defines the empty lists and dicts.
    parameter_dc['lists'].setdefault('chp', {})
    parameter_dc['lists']['chp']['variable'] = []
    parameter_dc['lists']['chp']['virtuell'] = []
    parameter_dc['lists']['chp']['fixed'] = []
    parameter_dc['lists']['chp']['dict'] = {}

    # One region to get the parameters.
    reg0 = parameter_dc['energy_system']['energy_system_regions'][0]

    # Sorts the chp transformer to the different lists.
    for c in parameter_dc['energy_system']['energy_system_transformer4chp']:
        if (parameter_dc['parameter']['parameter_transformer4chp'][reg0][c]
                ['hp_ratio_type'] == 'variable'):
            parameter_dc['lists']['chp']['variable'].extend([c],)
            parameter_dc['lists']['chp']['dict'][c] = 'v' + c[1:]
            parameter_dc['lists']['chp']['virtuell'].extend(['v' + c[1:]],)
        elif (parameter_dc['parameter']['parameter_transformer4chp'][reg0][c]
                ['hp_ratio_type'] == 'fixed'):
            parameter_dc['lists']['chp']['fixed'].extend([c],)
        else:
            logging.error(
                'HP_ratio_type for {0} must be "fixed" or "variable"'.format(c))


def create_list_storages4biogas(param_dc):
    '''
    Adds a biogas storage to the energy_system if biogas (rbig) is present.
    '''

    if 'rbig' in param_dc['energy_system']['energy_system_resources']:
        param_dc['energy_system']['energy_system_storages4biogas'] = ['sbig']
        param_dc['energy_system']['energy_system_storages'].extend(['sbig'])
        param_dc['energy_system']['energy_system_components'].extend(['sbig'])
    else:
        param_dc['energy_system']['energy_system_storages4biogas'] = []


def create_list_all_elec_components(param_dc):
    ''
    param_dc['lists']['all_elec_components'] = (param_dc['energy_system']
        ['energy_system_re'] + param_dc['energy_system']
        ['energy_system_transformer4elec'] + param_dc['energy_system']
        ['energy_system_storages4elec'])


def create_post_lists(basic_dc, parameter_dc):
    '''
    Creates lists, that could not be created until all parameters are read.
    '''
    parameter_dc['lists'] = {}
    create_lists_resources2plant(basic_dc, parameter_dc)
    create_lists_heat_classes(basic_dc, parameter_dc)
    creat_list_chp_types(basic_dc, parameter_dc)
    create_list_all_elec_components(parameter_dc)
