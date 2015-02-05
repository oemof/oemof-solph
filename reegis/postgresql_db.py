#!/usr/bin/python
# -*- coding: utf-8

import psycopg2
import psycopg2.extras
import numpy as np


def connect2db(dic):
    '''
    Open database connection using the values of a dictionary.
    The dictionary must contain at least the following values:
        ip: the ip of the database server
        db: the name of the database
        user: the name of the database user
        password: the password of the database user
        port: port for the database connection (default: 5432)
    '''
    dic.setdefault('port', 5432)
    conn = psycopg2.connect('''host=%s dbname=%s user=%s password=%s port=%s
    ''' % (dic['ip'], dic['db'], dic['user'], dic['password'], dic['port']))
    return conn


def close_db(cur, conn, commit=False):
    '''
    Close open database connection while "cur" and "conn" are connection objects
    Use "commit=True" if you want to write the changes to the database
    '''
    if commit:
        conn.commit()
    cur.close()
    conn.close()


def fetch_table_names(dic, schema):
    '''
    Returns all table names from a given schema
    '''
    conn = connect2db(dic)
    cur = conn.cursor()
    cur.execute('''
        select table_name from information_schema.tables
            where table_schema = '%s';''' % (schema))
    tables = cur.fetchall()
    close_db(cur, conn)
    return tables


def fetch_column(dic, schema, table, column, unique=False):
    '''
    Returns all values from a given column in a given table
    '''
    conn = connect2db(dic)
    cur = conn.cursor()
    cur.execute('''
        select %s from %s.%s;
        ''' % (column, dic['schema'], table))
    if unique:
        values = list({}.fromkeys(cur.fetchall()).keys())
    else:
        values = cur.fetchall()
    close_db(cur, conn)
    return values


def fetch_row(dic, schema, table_name, where_column=None, where_condition=None):
    '''
    Fetch one row from a given table and write it into a dictionary, where the
    dictionary keys are the names of the columns.
    '''
    conn = connect2db(dic)
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if where_column is None:
        dict_cur.execute('''
            select * from %s.%s;
            ''' % (schema, table_name))
    else:
        dict_cur.execute('''
            select * from %s.%s where %s='%s';
            ''' % (schema, table_name, where_column, where_condition))
    value_dict = dict_cur.fetchone()
    close_db(dict_cur, conn)
    return value_dict


def fetch_column_names(dic, schema, table_name):
    '''
    Returns all column names from a given a given table
    and write it into a dictionary
    '''
    conn = connect2db(dic)
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    dict_cur.execute('''
        select * from %s.%s;
        ''' % (schema, table_name))
    values = dict_cur.fetchone()
    close_db(dict_cur, conn)
    return list(values.keys())


def columns2array_dict(dic, schema, table):
    '''
    Writes all columns of a given table as np.arrays to a dictionary,
    where the names of the columns are the keys of the dictionary.
    '''
    conn = connect2db(dic)
    cur = conn.cursor()
    cur.execute('''select column_name from information_schema.columns
        where table_schema = '%s'
        and table_name   = '%s'
        ''' % (schema, table))
    columns = cur.fetchall()
    table_dict = {}
    for col in columns:
        cur.execute('''
            select "%s" from %s.%s;
            ''' % (col[0], schema, table))
        col_dict = np.asarray(cur.fetchall())
        table_dict[col[0]] = col_dict.transpose()[0]
    close_db(cur, conn)
    return table_dict


def exists_table(dic, schema, table_name):
    '''
    Checks if table exists and returns true or false
    '''
    conn = connect2db(dic)
    cur = conn.cursor()
    cur.execute('''
    select table_name from information_schema.tables where table_schema = '%s';
    ''' % schema)
    table_names = np.array(cur.fetchall())
    close_db(cur, conn)
    return table_name in table_names


def exists_column(dic, schema, table_name, column_name):
    '''
    Checks if table exists and returns true or false
    '''
    conn = connect2db(dic)
    cur = conn.cursor()
    cur.execute('''
    select column_name from information_schema.columns
    where table_schema = '%s'
    and table_name = '%s';
    ''' % (schema, table_name))
    column_names = np.array(cur.fetchall())
    close_db(cur, conn)
    return column_name in column_names


def add_column(db_dict, schema, table, column, col_type):
    '''
    Adds column to given table and returns true if the column has been created
    and false if the column already exists.
    '''
    if not exists_column(db_dict, schema, table, column):
        conn = connect2db(db_dict)
        cur = conn.cursor()
        cur.execute('''alter table %s.%s add column %s %s;
        ''' % (schema, table, column, col_type))
        close_db(cur, conn, commit=True)
        bool_var = True
    else:
        bool_var = False
    return bool_var


def write_comment(comment, db_dict, schema, table, column=None):
    '''
    Writes a comment to a given table or column
    if the name of the column is defined.
    '''
    conn = connect2db(db_dict)
    cur = conn.cursor()
    if column is None:
        cur.execute('''COMMENT ON TABLE %s.%s IS '%s';''' % (
            schema, table, comment))
    else:
        cur.execute('''COMMENT ON COLUMN %s.%s.%s IS '%s';''' % (
            schema, table, column, comment))
    close_db(cur, conn, commit=True)


def read_comment(db_dict, schema, table, column=None):
    '''
    Returns the comment of a given table or column
    if the name of the column is defined.
    '''
    conn = connect2db(db_dict)
    cur = conn.cursor()
    if column is None:
        cur.execute('''
        SELECT attrelid
        FROM pg_attribute
        WHERE attrelid = '%s.%s'::regclass;''' % (schema, table))
        id_tmp = cur.fetchone()[0]
        cur.execute('''select pg_catalog.obj_description(%s);''' % (id_tmp))
        comment = cur.fetchone()[0]
    else:
        cur.execute('''
        SELECT attrelid,attnum
        FROM pg_attribute
        WHERE attrelid = '%s.%s'::regclass
        and attname='%s';''' % (schema, table, column))
        id_tmp = cur.fetchall()[0]
        cur.execute('''select pg_catalog.col_description(%s,%s);
        ''' % (id_tmp[0], id_tmp[1]))
        comment = cur.fetchone()[0]
    close_db(cur, conn)
    return comment