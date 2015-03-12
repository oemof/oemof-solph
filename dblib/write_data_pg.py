#!/usr/bin/python
# -*- coding: utf-8

from . import basic_pg as pg


def execute_write_db(dic, db_string, commit=True):
    '''
    '''
    conn = pg.connect2db(dic)
    cur = conn.cursor()
    cur.execute(db_string)
    pg.close_db(cur, conn, commit=commit)


def insert_value(dic, schema, table, column, value,
    where_column, where_condition, numeric=False):
    '''inserts one value at a specific place in DB, the where column should
    be given by a unique value, like id'''

    if numeric is True:
        db_string = 'update %s.%s SET %s = %s WHERE %s=%s; ' % (
            schema, table, column, value, where_column, where_condition)
    else:
        db_string = 'update %s.%s SET %s = %s WHERE %s="%s"; ' % (
            schema, table, column, value, where_column, where_condition)
    execute_write_db(dic, db_string, commit=True)