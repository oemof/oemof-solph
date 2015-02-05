#!/usr/bin/python
# -*- coding: utf-8

import dblib as db
import logging


#def creates_or_completes_info_table(main_dt):
#    ''
#    print main_dt.keys()
#    exist_col_ls = db.fetch_column_names(
#        main_dt['basic'], main_dt['basic']['res_schema'], 'info')
#    info_col_ls = list(main_dt['lp']['info']['data'].keys())
#    print info_col_ls
#    print [x for x in list(exist_col_ls) if x not in set(info_col_ls)]


def db_definitions():
    ''
    db_dc = {}
    db_dc['investment'] = {'column_type': 'boolean'}
    db_dc['re_share'] = {'column_type': 'varchar(10)'}
    db_dc['opt_target'] = {'column_type': 'varchar(20)'}
    db_dc['solver'] = {'column_type': 'varchar(20)'}
    return db_dc


def creates_or_completes_info_table(main_dt, column_ls):
    ''
    schema = main_dt['basic']['res_schema']
    table = 'info'
    db_dc = db_definitions()
    db_string = ''
    for col in column_ls:
        if not db.exists_column(main_dt['basic'], schema, table, col):
            db_string += 'ALTER TABLE {0}.{1} ADD COLUMN {2} {3};'.format(
                schema, table, col, db_dc[col]['column_type'])
            logging.debug('Column {0} adde in "info table".'.format(col))
    if db_string:
        db.execute_write_db(main_dt['basic'], db_string)
    else:
        logging.warning(
            'Tried to add a column to the "info table" but all columns exist.')
