#!/usr/bin/python
# -*- coding: utf-8

'''
Author: Uwe Krien (uwe.krien@rl-institut.de)
Changes by: Uwe Krien (uwe.krien@rl-institut.de)
Responsibility: Uwe Krien (uwe.krien@rl-institut.de)
'''

import dblib as db
import logging
import psycopg2

## Definition of the column names for typical columns
## Changes here might cause errors, writing data to existing tables
#id_col = 'id'  # column for the scenario-id in the result tables
#timestep_col = 'timestep'  # column for the timestep
#region_col = 'region'  # column for the name of the region


def del_one_set_in_one_table(main_dc, table, scenario_id):
    '''
    Delets all results with a given id inside a given table

    Example
    -------
    del_one_set_in_one_table('test_power_gen', 10)
    '''
    scenario_id = float(scenario_id)
    db_string = 'delete from %s.%s where id=%s;' % (
        main_dc['basic']['res_schema'], table, scenario_id)
    try:
        db.execute_write_db(main_dc['basic'], db_string)
    except (psycopg2.ProgrammingError) as e:
        logging.debug(e)


def del_set_and_it_subsets_in_one_table(main_dc, table, scenario_id):
    '''
    Delets all results with a given id and all possible sub ids
    inside a given table

    Example
    -------
    del_set_and_it_subsets_in_one_table('info', 10)
    '''
    for i in range(1, 10):
        tmp_id = scenario_id + i / 10.
        del_one_set_in_one_table(main_dc, table, tmp_id)
    del_one_set_in_one_table(main_dc, table, scenario_id)


def del_one_set_in_all_tables(main_dc, scenario_id, res_tables, e_system=None):
    '''
    Delets all results with a given id inside all result-tables defined on top.
    The name of the energy system comes from the scenario table.
    Use the optional variable e_system if the name of energy system, where you
    want to delete the results differs from one in the actual scenario
    definition.

    Example
    -------
    del_one_set_in_all_tables(10)
    or
    del_one_set_in_all_tables(10, 'test')
    '''
    if e_system is None:
        name_scenario = db.fetch_value(main_dc['basic'],
            main_dc['basic']['schema'],
            'scenarios', 'energy_system', where_column='id',
            where_condition=int(scenario_id))
    else:
        name_scenario = e_system
    for table in res_tables:
        table = name_scenario + '__' + table
        del_one_set_in_one_table(main_dc, table, scenario_id)


def del_all_subsets_in_all_tables(main_dc, scenario_id, res_tables,
        e_system=None):
    '''
    Delets all results with all possible sub ids of the given id inside all
    result-tables defined on top. The results with the main id are kept!
    The name of the energy system comes from the scenario table.
    Use the optional variable e_system if the name of energy system, where you
    want to delete the results differs from one in the actual scenario
    definition.

    Example
    -------
    del_all_subsets_in_all_tables(10)
    or
    del_all_subsets_in_all_tables(10, 'test')
    '''
    for i in range(1, 10):
        tmp_id = scenario_id + i / 10.
        del_one_set_in_all_tables(main_dc, tmp_id, res_tables,
            e_system=e_system)


def del_set_and_subsets_in_all_tables(main_dc, scenario_id, res_tables,
        e_system=None):
    '''
    Delets all results with all possible sub ids of the given id inside all
    result-tables defined on top. The results with the main id are also deleted!
    The name of the energy system comes from the scenario table.
    Use the optional variable e_system if the name of energy system, where you
    want to delete the results differs from one in the actual scenario
    definition.

    Example
    -------
    del_set_and_subsets_in_all_tables(10)
    or
    del_set_and_subsets_in_all_tables(10, 'test')
    '''
    del_one_set_in_all_tables(main_dc, scenario_id, res_tables,
        e_system=e_system)
    del_all_subsets_in_all_tables(main_dc, scenario_id, res_tables,
        e_system=e_system)


def check_subscenario(dic, schema, esy_tbname, where_column, where_condition):
    ''
    value = list([where_condition, ])
    for n in range(1, 10):
        lastvalue = value
        cond = where_condition + n / 10.
        value = db.fetch_row(dic, schema, esy_tbname, where_column='id',
            where_condition=cond)
        if value is None:
            return lastvalue[0]
    return value[0]


def smart_remove_results(main_dc, res_tables, overwrite):
    ''
    esys_name = (db.fetch_columns(main_dc['basic'],
        main_dc['basic']['res_schema'], 'info',
        'energy_system', where_column='id',
        where_condition=int(main_dc['info']['id'])
        )['energy_system'])[0].replace(" ", "_")
    subset = db.fetch_columns(main_dc['basic'],
        main_dc['basic']['res_schema'], 'info',
        columns='id', where_string="id>%s and id<%s" % (
        main_dc['info']['id'], (main_dc['info']['id'] + 1)), as_np=True)['id']
    res_tables.remove('info')
    if overwrite:
        if subset.any():
            del_set_and_subsets_in_all_tables(main_dc, main_dc['info']['id'],
                res_tables, e_system=esys_name)
            del_set_and_it_subsets_in_one_table(main_dc, 'info',
                main_dc['info']['id'])
        else:
            del_one_set_in_all_tables(main_dc, main_dc['info']['id'],
                res_tables, e_system=esys_name)
            del_one_set_in_one_table(main_dc, 'info', main_dc['info']['id'])
    else:
        if subset.any():
            new_id = float(subset.max()) + 0.1
            if new_id > (float(main_dc['info']['id']) + 0.9):
                new_id = float(main_dc['info']['id']) + 0.9
                logging.error('Too many subscenarios for id: %s' % (
                    main_dc['info']['id']))
                del_one_set_in_all_tables(main_dc, new_id, res_tables,
                    e_system=esys_name)
                del_one_set_in_one_table(main_dc, 'info', new_id)
        else:
            new_id = float(main_dc['info']['id']) + 0.1
        stringdb = ''
        for table in res_tables:
            table = main_dc['res_schema'] + '.' + esys_name + '__' + table
            stringdb = stringdb + 'update %s set id=%s where id=%s;' % (
                table, new_id, main_dc['info']['id'])
        table = main_dc['res_schema'] + '.' + 'info'
        stringdb = stringdb + 'update %s set id=%s where id=%s;' % (table,
            new_id, main_dc['info']['id'])
        try:
            db.execute_write_db(main_dc, stringdb)
            logging.warning('Created subset %s to save existing results.'
                % new_id)
        except (psycopg2.ProgrammingError) as e:
            logging.warning(e)