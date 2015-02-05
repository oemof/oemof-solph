#!/usr/bin/python
# -*- coding: utf-8

#import logging


def extend_basic_dc(basic_dict):
    '''
    Definition of pahesmf parameters outside the normal database
    '''
    extend_dc = {}

    # Name of column in db, where the name of the set can be found
    extend_dc['scenario_col'] = 'name_set'

    # Name of columns without parameters for the simulation
    extend_dc['remove_columns'] = [
                    'id',
                    'name_set',
                    'description',
                    'lastmodified',
                    'changed_by']

    # Schema of db, where the parameter tables are found (dev)
    extend_dc['schema'] = 'pahesmf_dev_sim'

    # Schema of db, where the result tables are found (dev)
    extend_dc['res_schema'] = 'pahesmf_dev_res'

    # Schema of db, where the parameter tables are found (master)
    extend_dc['master_schema'] = 'pahesmf_sim'

    # Schema of db, where the result tables are found (master)
    extend_dc['master_res_schema'] = 'pahesmf_res'

    # List of branches that uses the "master" schema.
    extend_dc['list_of_masters_in_db'] = ['master', 'finn_stable']

    # Schema of db, where the data tables are found
    extend_dc['dat_schema'] = 'pahesmf_dat'

    # Name of the table, where the basic scenario is defined
    extend_dc['start_table'] = 'scenarios'

    # Name of the table, where the energy system is defined
    extend_dc['energy_system_table'] = 'energy_system'

    # Name of column, where the name of the region ca be found
    extend_dc['regions_table'] = 'regions'

    # Basic names of result tables (obsolete?)
    extend_dc['res_tables'] = ['power_gen', 'power_inst', 'storage_charge',
        'storage_discharge', 'storage_inst', 'trline_transfer',
        'trm_power', 'storage_soc']

    # Table name extensions for transformer
    extend_dc['transformer_keys'] = ['elec', 'chp', 'heat', 'gas']

    # Table name extensions for storages
    extend_dc['storage_keys'] = ['elec', 'heat', 'gas', 'biogas']

    # List of all key parts that are part of the component list
    extend_dc['type_components'] = ['storages', 're', 'transformer']

    # Table name extensions for heat producing transformer
    extend_dc['heat_transformer_keys'] = ['chp', 'heat']

    # Schema of data tables
    extend_dc['data_schema'] = 'pahesmf_dat'

    # platts abbrevations translation tables
    extend_dc['platts_translate'] = 'presettingfuel2platt'

    # Order of components for plots
    extend_dc['order'] = {}
    extend_dc['order']['generation'] = ['tnuc', 'tlcp', 'thcp', 'tcpp',
        'rpvo', 'rpvr', 'rowi', 'rwin', 'twpp', 'tocg', 'topp',
        'sbat', 'sphs', 'trmi', 'txxx', 'tbga', 'thoi', 'thng', 'twcb', 'tgcb',
        'tbgc', 'tbbc', 'vbbc', 'thcc', 'tgac', 'vgac', 'tdhp', 'thdh', 'tgbd',
        'tbmc', 'vbmc', 'tccg', 'thxx']
    extend_dc['order']['demand'] = ['lele', 'sphs', 'sbat', 'tptg', 'trme',
        'rele', 'eexc', 'thoi', 'thng', 'twcb', 'tgcb', 'dst0', 'hexc']

    return extend_dc