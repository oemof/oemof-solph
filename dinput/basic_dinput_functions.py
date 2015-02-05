#!/usr/bin/python
# -*- coding: utf-8

import logging
import dblib as db


def remove_from_list(orig_list, remove_list):
    '''
    Removes the values inside the remove_list from the orig_list.
    '''
    for item in remove_list:
        if item in orig_list:
            try:
                orig_list.remove(item)
            except:
                logging.debug('Cannot remove %s from list %s' % (
                    item, orig_list))
    return orig_list


def unique_list(seq):
    '''
    Returns a unique list without preserving the order
    '''
    return list({}.fromkeys(seq).keys())


def cut_lists(list_a, list_b):
    '''
    Returns a list with the values of list_a AND list_b.
    '''
    return [x for x in list(list_a) if x in set(list_b)]


def check_table_structure(basic_dc, table):
    '''
    [Description]

    [Autor]

    Parameters

    Keyword arguments

    Returns
    '''
    number_lines = len(db.fetch_columns(basic_dc,
            basic_dc['schema'],
            table,
            columns='name_set',
            where_column='name_set',
            where_condition='default')['name_set'])
    if number_lines > 1:
        table_type = 'vertical'
    elif number_lines == 1:
        if db.exists_column(basic_dc, basic_dc['schema'], table, 'region'):
            table_type = 'vertical'
        else:
            table_type = 'row'
    else:
        logging.warning('Something is wrong in the db structure. Table: %s' % (
            table))
    return table_type


def get_parameter_arbitrary_subtable(basic_dc, param_dc, column, region, comp):
    '''returns parameter from arbitrary parameter_* sub table'''
    top_tables = remove_from_list(list(param_dc['parameter'].keys()),
        basic_dc['remove_columns'])
    for subtab in top_tables:
        try:
            param = param_dc['parameter'][subtab][region][comp][column]
        except:
            pass
        if 'param' in locals():
            return param
            break
    raise KeyError(column)