import psycopg2 as psy
import psycopg2.extras as psyex
import json
import operator


class DBError(Exception):
    'error'
    def __init__(self, value):
        'init'
        self.value = value

    def __str__(self):
        'self'
        return repr(self.value)


def get_component_list(takeSubs):
    'Returns list of dictionarys from component table with given name'
    cur = connect_database().cursor(cursor_factory=psyex.DictCursor)
    try:
        if takeSubs:
            cur.execute('SELECT c_data, id FROM mobility.add_field')
        else:
            cur.execute('SELECT c_data, id FROM mobility.component')
    except:
        raise DBError('Could not select c_data from mobility.component-table')

    rows = cur.fetchall()
    n = len(rows)
    list_of_dicts = []
    for i in range(n):
        com_dict = json.loads(rows[i][0])
        com_dict['id'] = str(rows[i][1])
        list_of_dicts.append(com_dict)
    return list_of_dicts


def get_component_by_ID(com_id, takeSubs):
    'Returns list of dictionarys from component table with given name'
    cur = connect_database().cursor(cursor_factory=psyex.DictCursor)
    try:
        if takeSubs:
            cur.execute('''SELECT c_data FROM mobility.add_field WHERE id=%s''',
                (com_id,))
        else:
            cur.execute('''SELECT c_data FROM mobility.component WHERE id=%s''',
                (com_id,))
    except:
        raise DBError('Could not select component #' + str(com_id) +
            ' from subs-table')
    rows = cur.fetchall()
    if rows == []:
        raise DBError('Could not select component #' + str(com_id) +
            ' from subs-table')
    return json.loads(rows[0][0])


def get_pattern_list(takeSubs=None, takeID=1):
    '''Returns dictionary containing amount of patterns (count), pattern_types
    and pattern_fields (as dictionary)'''
    cur = connect_database().cursor(cursor_factory=psyex.DictCursor)
    try:
        if takeSubs is None:
            cur.execute('''SELECT c_type, fields, id FROM
            mobility.component_pattern''')
        else:
            cur.execute('''SELECT c_type, fields, id FROM
            mobility.component_pattern WHERE sub=%s''', (takeSubs,))
    except:
        print "Couldn't select table!"
    patterns = cur.fetchall()
    pattern_types = map(operator.itemgetter(0), patterns)
    pattern_fields = []
    n = len(patterns)
    for i in range(n):
        pat_dict = json.loads(patterns[i][1])
        if takeID:
            pat_dict['id'] = str(patterns[i][2])
        pattern_fields.append(pat_dict)
    return {'count': len(pattern_types), 'pattern_types': pattern_types,
            'pattern_fields': pattern_fields}


def add_component(com_type, com_dict, isSub):
    'Adds values as JSON-object into component-table'
    conn = connect_database()
    cur = conn.cursor(cursor_factory=psyex.DictCursor)
    json_str = json.dumps(com_dict)
    try:
        if isSub:
            cur.execute('''INSERT INTO mobility.add_field (c_type, c_data)
            VALUES (%s,%s);''', (com_type, json_str))
        else:
            cur.execute('''INSERT INTO mobility.component (c_type, c_data)
            VALUES (%s,%s);''', (com_type, json_str))
    except psy.ProgrammingError as pe:
        raise DBError(pe.args[0])
    conn.commit()


def add_pattern(com_type, com_dict, isSub):
    'Adds values as JSON-object into component-table'
    conn = connect_database()
    cur = conn.cursor(cursor_factory=psyex.DictCursor)
    json_str = json.dumps(com_dict)
    try:
        cur.execute('''INSERT INTO mobility.component_pattern
        (c_type, fields, sub) VALUES (%s,%s,%s);''',
        (com_type, json_str, isSub))
    except psy.ProgrammingError as pe:
        raise DBError(pe.args[0])
    conn.commit()


def insert(scheme, table, value_dict):
    'Inserts dict_values into given keys in scheme.table'
    conn = connect_database()
    cur = conn.cursor(cursor_factory=psyex.DictCursor)
    fields = ', '.join(list(value_dict.keys()))
    values = ', '.join(['%%(%s)s' % x for x in value_dict])
    query = '''INSERT INTO %s.%s (%s) VALUES (%s);''' % (scheme, table,
        fields, values)
    try:
        cur.execute(query, value_dict)
    except:
        print "Couldn't insert into table!"
    conn.commit()


def connect_database():
    'Connects to 192.168.10.25-Server as postgres-user (to be changed)'
    try:
        conn = psy.connect('''host='192.168.10.25' dbname='postgres'
        user='postgres' password='.titdbui2013' ''')
    except:
        print "I am unable to connect to the database."

    return conn