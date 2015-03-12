#!/usr/bin/python
# -*- coding: utf-8

import sys
import os
import psycopg2
import psycopg2.extras
import numpy as np


def get_db_dict():
    r"""Reads the basic db-information from a local init file. The file has be
    in: '[$HOME].python_local/init_local.py'.

    Returns
    -------
    dictionary
        Dictionary with the keys: ip, port, db, user, password.

    Examples
    --------
    .. code:: python

        #!/usr/bin/python
        # -*- coding: utf-8


        def pg_db():
            local_dict = {
                'ip': 'localhost_or_ip',
                'port': '5432',
                'db': 'name_of_db',
                'user': 'username',
                'password': 'password'}
            return local_dict
    """
    initpath = os.path.join(os.environ['HOME'], '.python_local')
    sys.path.append(initpath)
    import init_local as init
    return init.pg_db()


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
    values = cur.fetchall()
    for i in range(len(values)):
        values[i] = values[i][0]
    close_db(cur, conn)
    return values


def fetch_column_names(dic, schema, table):
    '''
    Returns all column names from a given table
    and writes it into a dictionary
    '''
    conn = connect2db(dic)
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    dict_cur.execute('''
        SELECT * FROM %s.%s LIMIT 1;
        ''' % (schema, table))
    values = dict_cur.fetchone()
    close_db(dict_cur, conn)
    return list(values.keys())


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