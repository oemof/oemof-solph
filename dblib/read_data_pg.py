#!/usr/bin/python
# -*- coding: utf-8

'''
Author: Uwe Krien (uwe.krien@rl-institut.de)
Changes by:
Responsibility: Uwe Krien (uwe.krien@rl-institut.de)
'''

import psycopg2
import psycopg2.extras
import numpy as np
from . import basic_pg as pg


def execute_read_db(dic, db_string):
    '''
    Executes a sql-string and returns a tuple with the return values from the db

    Uwe Krien (uwe.krien@rl-institut.de)
    '''
    conn = pg.connect2db(dic)
    cur = conn.cursor()
    cur.execute(db_string)
    values = cur.fetchall()
    pg.close_db(cur, conn)
    return values


def fetch_row(dic, schema, table_name, where_column=None, where_condition=None,
        where_string=None):
    '''
    Fetch one row from a given table and write it into a dictionary, where the
    dictionary keys are the names of the columns.

    Uwe Krien (uwe.krien@rl-institut.de)
    '''
    exec_str = 'select * from %s.%s' % (schema, table_name)
    if where_column is not None:
        exec_str = exec_str + (" where %s='%s';" % (
            where_column, where_condition))
    elif where_string is not None:
        exec_str = exec_str + (" where %s;" % where_string)
    else:
        exec_str = exec_str + ';'
    conn = pg.connect2db(dic)
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    dict_cur.execute(exec_str)
    value_dict = dict_cur.fetchone()
    pg.close_db(dict_cur, conn)
    return value_dict


def fetch_columns(dic, schema, table, columns=None, unique=False, as_np=False,
        orderby=None, is_tuple=False, where_column=None, where_condition=None,
        where_string=None):
    '''
    Fetches one or more columns from a given table with various options.

    Uwe Krien (uwe.krien@rl-institut.de)

    Parameters

    Keyword arguments

    Returns
    '''
    if columns is None:
        columns = pg.fetch_column_names(dic, schema, table)
    table_dict = {}
    if type(columns) is str:
        columns = ((columns,))
    conn = pg.connect2db(dic)
    cur = conn.cursor()
    for col in columns:
        exec_str = 'select "%s" from %s.%s' % (col, schema, table)
        if where_column is not None:
            exec_str = exec_str + (" where %s='%s'" % (
                where_column, where_condition))
        if where_string is not None:
            exec_str = exec_str + (' where %s' % where_string)
        if orderby is None:
            exec_str = exec_str + (' order by "%s";' % col)
        else:
            exec_str = exec_str + (' order by %s;' % orderby)
        cur.execute(exec_str)
        values = cur.fetchall()
        if not is_tuple:
            for i in range(len(values)):
                values[i] = values[i][0]
        if unique:
            seen = set()
            values = [x for x in values if x not in seen and not seen.add(x)]
        if as_np:
            col_dict = np.asarray((values))
            table_dict[col] = col_dict.transpose()
        else:
            table_dict[col] = values
    pg.close_db(cur, conn)
    return table_dict


def fetch_columns_np(dic, schema, table, columns=None, unique=False,
    orderby=None):
    '''
    Dummy function to fetch_column directly as np_array. You should use
    fetch_columns with parameter as_np=True instead.
    '''
    return fetch_columns(dic, schema, table, columns, unique, as_np=True,
        orderby=orderby)