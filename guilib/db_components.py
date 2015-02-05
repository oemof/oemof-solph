import psycopg2 as psy
import psycopg2.extras as psyex
import json
import operator


class DBError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def get_component_list(takeSubs):
    # Returns list of dictionarys from component table
    # with given name
    cur = connect_database().cursor(cursor_factory=psyex.DictCursor)
    try:
        if takeSubs:
            cur.execute('''SELECT data, id FROM onehour.subs''')
        else:
            cur.execute('''SELECT c.data, c.id, s.data
            FROM onehour.component AS c
            LEFT JOIN onehour.component_subs AS cs ON c.id=cs.component_id
            LEFT JOIN onehour.subs AS s ON cs.sub_id=s.id''')
    except:
        raise DBError('Could not select c_data from onehour.component-table')

    rows = cur.fetchall()
    n = len(rows)
    list_of_dicts = []
    for i in range(n):
        com_dict = json.loads(rows[i][0])
        com_dict['id'] = str(rows[i][1])
        if not takeSubs:
            if not rows[i][2] is None:
                com_dict = dict(com_dict.items() +
                    json.loads(rows[i][2]).items())
        list_of_dicts.append(com_dict)
    return list_of_dicts


def get_component_by_ID(com_id, takeSubs):
    # Returns list of dictionarys from component table
    # with given name
    cur = connect_database().cursor(cursor_factory=psyex.DictCursor)
    try:
        if takeSubs:
            cur.execute('''SELECT data FROM onehour.subs WHERE id=%s''',
                (com_id,))
        else:
            cur.execute('''SELECT data FROM onehour.component WHERE id=%s''',
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
    # Returns dictionary containing amount of patterns (count), pattern_types
    # and pattern_fields (as dictionary)
    cur = connect_database().cursor(cursor_factory=psyex.DictCursor)
    try:
        if takeSubs is None:
            cur.execute('''SELECT c_type, fields, id FROM
            onehour.component_pattern''')
        else:
            cur.execute('''SELECT c_type, fields, id FROM
            onehour.component_pattern WHERE issub=%s''', (bool(takeSubs),))
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


def get_pattern_id(com_type):
    # Returns id of given com_type
    cur = connect_database().cursor(cursor_factory=psyex.DictCursor)
    try:
        cur.execute('''SELECT id FROM
            onehour.component_pattern WHERE c_type=(%s);''', (com_type,))
    except psy.ProgrammingError as pe:
        raise DBError("Couldn't find " + com_type + " in component_pattern:\n" +
            pe.args[0])
    return cur.fetchall()[0][0]


def add_component(pattern_id, com_dict, isSub):
    # Adds values as JSON-object into component-table
    conn = connect_database()
    cur = conn.cursor(cursor_factory=psyex.DictCursor)
    json_str = json.dumps(com_dict)
    try:
        if isSub:
            cur.execute('''INSERT INTO onehour.subs (pattern_id, data)
            VALUES (%s,%s);''', (pattern_id, json_str))
        else:
            cur.execute('''INSERT INTO onehour.component (pattern_id, data)
            VALUES (%s,%s);''', (pattern_id, json_str))
    except psy.ProgrammingError as pe:
        raise DBError(pe.args[0])
    conn.commit()


def add_pattern(com_type, com_dict, isSub):
    # Adds values as JSON-object into component-table
    conn = connect_database()
    cur = conn.cursor(cursor_factory=psyex.DictCursor)
    json_str = json.dumps(com_dict)
    try:
        cur.execute('''INSERT INTO onehour.component_pattern
        (c_type, fields, isSub) VALUES (%s,%s,%s);''',
        (com_type, json_str, bool(isSub)))
    except psy.ProgrammingError as pe:
        raise DBError(pe.args[0])
    conn.commit()


def insert(scheme, table, value_dict):
    # Inserts dict_values into given keys in scheme.table
    conn = connect_database()
    cur = conn.cursor(cursor_factory=psyex.DictCursor)
    fields = ', '.join(value_dict.keys())
    values = ', '.join(['%%(%s)s' % x for x in value_dict])
    query = '''INSERT INTO %s.%s (%s) VALUES (%s);''' % (scheme, table,
        fields, values)
    try:
        cur.execute(query, value_dict)
    except:
        print "Couldn't insert into table!"
    conn.commit()


def connect_database():
    # Connects to 192.168.10.25-Server as postgres-user (to be changed)
    try:
        conn = psy.connect('''host='192.168.10.25' dbname='postgres'
        user='postgres' password='.titdbui2013' ''')
    except:
        print "I am unable to connect to the database."

    return conn