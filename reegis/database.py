#!/usr/bin/python
# -*- coding: utf-8

import psycopg2
import psycopg2.extras
import numpy as np
import os


############################# Retrieve data from db ##########################


def open_db_connection():
    '''
    Opens the database connection
    '''
    conn = psycopg2.connect(
        "host=localhost dbname=uwes_db user=wittenberg password=luTHer")
    return conn


def get_input_data(ProjectID, db_table='wittenberg.parameterset'):
    '''
    Retrieves input data of the specified Project ID from the database.
    '''
    conn = open_db_connection()
    dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    dict_cur.execute('''
    select *
    from %s
    where "ProjectID" = %s
    ''' % (db_table, ProjectID))
    db_input = dict_cur.fetchone()
    dict_cur.close()
    conn.close()
    # convert psycopg_dict to dict
    input_data = {}
    for key in (list(db_input.keys())):
        input_data[key] = db_input[key]
    return input_data


def get_try_region(district):
    '''
    Determines applicable Test Reference Year Region.
    '''
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute('''
    select t.id
    from wittenberg.gemeinden as g, wittenberg.try_dwd as t
    where st_contains(t.the_geom, g.the_geom) = 't'
    and g.stadtname = %(str)s;
    ''', {'str': district})
    try_region = cur.fetchone()
    cur.close()
    conn.close()
    return try_region[0]


#def get_try_region(coordinates):
    #'''
    #Determines applicable Test Reference Year Region.
    #Coordinates must be given as 'POINT(longitude latitude)'.
    #'''
    #conn = open_db_connection()
    #cur = conn.cursor()
    #cur.execute('''
    #select id
    #from wittenberg.try_dwd
    #where st_contains(the_geom,
        #st_transform(st_geomfromtext(%(str)s,4326),4326)) = 't'
    #''', {'str': coordinates})
    #try_region = cur.fetchone()
    #cur.close()
    #conn.close()
    #return try_region[0]


def get_try_data(district):
    '''
    Returns the following data set for the given region.

    00 ID Database ID                                              []
    01 RG TRY-Region                                               []
    02 IS Location information                                     []
    03 MM Month                                                    []
    04 DD Day                                                      []
    05 HH Hour (CET)                                               []
    06 N  Cloud coverage                                           [Achtel]
    07 WR Wind direction 10 m above ground                         [°]
    08 WG Wind velocity 10 m above ground                          [m/s]
    09 t  Air temperature 2m above ground                          [°C]
    10 p  Air pressure at station level                            [hPa]
    11 x  Steam mass fraction                                      [g/kg]
    12 RF Relative humidity 2 m above ground                       [%]
    13 W  Metereological event                                     []
    14 B  Direct irradiation (horizontal plain)                    [W/m²]
    15 D  Diffuse irradiation (horizontal plain)                   [W/m²]
    16 IK Information, if B and/or D are measured/calculated       []
    17 A  Irradiance of atm. thermal radiation (horiz. plain)      [W/m²]
    18 E  Irradiance of terr. thermal radiation                    [W/m²]
    19 IL Quality bit for long-wave variables                      []
    20 h  Height of station                                        [m]
    '''
    try_region = get_try_region(district)
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute('''
    select *
    from wittenberg.try_2010_av_year
    where region = %(str)s
    order by id
    ''', {'str': try_region})
    try_data = np.asarray(cur.fetchall())
    cur.close()
    conn.close()
    return try_data


def residential_annual_el_demand(district):
    '''
    Calculates the annual electricity demand of residential houses based on
    an average annual demand and the number of inhabitants.
    '''
    # average demand per person
    ratio = {1: 0.37, 2: 0.36, 3: 0.18, 4: 0.09}
    demand = {1: 2050, 2: 1720, 3: 1350, 4: 1235}
    demand_per_person = (ratio[1] * demand[1] + ratio[2] * demand[2] +
    ratio[3] * demand[3] + ratio[4] * demand[4])
    # number of inhabitants
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute('''
    select sum(o.einwohner)
    from wittenberg.orte_landkreis_wittenberg as o, wittenberg.gemeinden as g
    where st_contains(g.the_geom, o.the_geom)
    and g.stadtname=%(str)s
    ''', {'str': district})
    inhabitants = cur.fetchone()
    cur.close()
    conn.close()
    return (float(inhabitants[0]) * demand_per_person / 1000)


def wka_cp_values(type_wka):
    '''
    Returns the wind velocity and the corresponding cp value of the specified
    wind turbine.
    '''
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute('''
    select v_wind, c_p
    from wittenberg.wind_power_curve
    where wka_type = %(str)s
    order by id
    ''', {'str': type_wka})
    cp_data = np.asarray(cur.fetchall())
    cur.close()
    conn.close()
    return cp_data


def P_max_wka(type_wka):
    '''
    Returns the nominal capacity in kW of the chosen wind turbine type.
    '''
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute('''
    select max(power)
    from wittenberg.wind_power_curve
    where wka_type = %(str)s
    ''', {'str': type_wka})
    P_max = cur.fetchone()[0]
    cur.close()
    conn.close()
    return P_max


def wind_area(district):
    '''
    Returns the total potential wind park area of a district in km².
    '''
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute('''
    select sum(st_area(st_intersection(g.the_geom,w.the_geom)::geography))
    from wittenberg.vr_wind as w, wittenberg.gemeinden as g
    where g.stadtname = %(str)s
    ''', {'str': district})
    area = cur.fetchone()
    cur.close()
    conn.close()
    return area[0] / (10 ** 6)


def building_area(district):
    '''
    Returns the total roof area of a district in m².
    '''
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute('''
    select sum(st_area(st_intersection(gem.the_geom,geb.the_geom)::geography))
    from wittenberg.gebaeude as geb, wittenberg.gemeinden as gem
    where st_isvalid(geb.the_geom)
    and gem.stadtname = %(str)s
    ''', {'str': district})
    area = cur.fetchone()
    cur.close()
    conn.close()
    return area[0]


def agricultural_area(district):
    '''
    Returns the total agricultural area of a district in m².
    '''
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute('''
        select sum(st_area(
            st_intersection(gem.the_geom, a.the_geom)::geography))
        from wittenberg.gemeinden as gem, wittenberg.ackerland as a
        where gem.stadtname = %(str)s
    ''', {'str': district})
    area = cur.fetchone()
    cur.close()
    conn.close()
    return area[0]


def forest_area(district):
    '''
    Returns the total forest area of a district in m².
    '''
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute('''
        select sum(st_area(
            st_intersection(gem.the_geom, a.the_geom)::geography))
        from wittenberg.gemeinden as gem, wittenberg.wald as a
        where gem.stadtname = %(str)s
    ''', {'str': district})
    area = cur.fetchone()
    cur.close()
    conn.close()
    return area[0]


def long_lat(district):
    '''
    Returns the longitude and latitude of the center of a district.
    '''
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute('''
    select st_astext(st_centroid(gem.the_geom))
    from wittenberg.gemeinden as gem
    where gem.stadtname = %(str)s
    ''', {'str': district})
    data = cur.fetchone()
    cur.close()
    conn.close()
    data_list = data[0].split()
    longitude = float(data_list[0][6:])
    latitude = float(data_list[1][0:-1])
    return latitude, longitude


#def district_data(district):
    #'''
    #District-specific data is collected and returned to the main_file for use
    #in load and potential calculations.
    #'''
    #district_data = {}
    #district_data['try_data'] = get_try_data(district)
    #district_data['annual_heat_demand_efh'] = \
        #hlp_res.annual_heat_demand_efh(district)
    #district_data['annual_heat_demand_mfh'] = \
        #hlp_res.annual_heat_demand_mfh(district)
    #district_data['res_annual_el_demand'] = \
        #residential_annual_el_demand(district)
    #district_data['wind_area'] = wind_area(district)
    #district_data['roof_area'] = building_area(district)
    #district_data['latitude'], district_data['longitude'] = \
        #long_lat(district)
    #return district_data


################################ Db operations ############################


def data2db(schema, tbname, colnames, lp_data_dict):
    '''
    Function to write the results of the solver into a postgres database.
    The lp_data_dict is a variable of the type LpVariable.dict (-> Pulp)
    http://www.coin-or.org/PuLP/pulp.html#pulp.LpVariable

    Keyword arguments:
        schema - name of the postgres schema
        tbname - name of the table in the postgres database
        colname - list of colum names
        lp_data_dict - LpVariable.dict with the data to be inserted
    '''
    # connecting to the database
    conn = open_db_connection()
    cur = conn.cursor()

    # drop old table (if exists) and create a new one
    table = schema + '.' + tbname
    cur.execute('DROP TABLE IF EXISTS %s;' % table)
    cur.execute('''CREATE TABLE IF NOT EXISTS %s
                (id integer PRIMARY KEY);''' % table)

    # create the columns
    for i in colnames:
        cur.execute('ALTER TABLE %s ADD COLUMN "%s" real;' % (table, i))

    # write the data into the table
    stringdb = ''
    for hour in range(len(lp_data_dict[colnames[0]])):
        sql_data = [hour + 1]
        for i in colnames:
            sql_data.append(lp_data_dict[i][hour].varValue)
        tmpstring = ('INSERT INTO %s VALUES %s ; ' % (table, tuple(sql_data)))
        stringdb = stringdb + tmpstring
    cur.execute(stringdb)

    # commit changes and close the database connection
    conn.commit()
    cur.close()
    conn.close()
    return


def data2file2db(schema, tbname, colnames, lp_data_dict, fname='tmp_out.csv'):
    '''
    Function to write the results of the solver into a file and
    a postgres database. It is slightly fast than writing directly
    into a database.
    The lp_data_dict is a variable of the type LpVariable.dict (-> Pulp)
    http://www.coin-or.org/PuLP/pulp.html#pulp.LpVariable

    Keyword arguments:
        schema -- name of the postgres schema
        tbname -- name of the table in the postgres database
        colname -- list of colum names
        lp_data_dict -- LpVariable.dict with the data to be inserted
        fname -- name of the output file
    '''
    # connecting to the database
    conn = open_db_connection()
    cur = conn.cursor()

    # drop old table (if exists) and create a new one
    table = schema + '.' + tbname
    cur.execute('DROP TABLE IF EXISTS %s;' % table)
    cur.execute('''CREATE TABLE IF NOT EXISTS %s
                (id integer PRIMARY KEY);''' % table)

    # create the columns
    for i in colnames:
        cur.execute('ALTER TABLE %s ADD COLUMN "%s" real;' % (table, i))

    # write the data into a file
    fpath = os.path.join(os.path.expanduser("~"), fname)
    out = open(fpath, 'w+')
    for hour in range(len(lp_data_dict[colnames[0]])):
        out.write(str(hour + 1))
        for i in range(len(colnames)):
            out.write(', ' + str(
            lp_data_dict[colnames[i]][hour].varValue))
        out.write('\n')
    out.close

    # write the data from the created file into the database
    out = open(fpath, 'r')
    cur.copy_from(out, table, sep=",")
    out.close

    # commit changes and close the database connection
    conn.commit()
    cur.close()
    conn.close()
    return


def drop_column_in_db_table(schema, tbname, colname):
    '''
    Drops a single column.

    Keyword arguments:
        schema - name of the postgres schema
        tbname - name of the table in the postgres database
        colname - name of column to be dropped
    '''
    table = schema + '.' + tbname
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute('''
        alter table %s
        drop column if exists %s
    ''' % (table, colname))
    conn.commit()
    cur.close()
    conn.close()
    return


def add_column_2_db_table(schema, tbname, colname, data_type):
    '''
    Adds a column to an existing table.

    Keyword arguments:
        schema - name of the postgres schema
        tbname - name of the table in the postgres database
        colname - name of column to be added
        data_type - data type of the column input data
    '''
    if not column_exists(schema, tbname, colname):
        table = schema + '.' + tbname
        conn = open_db_connection()
        cur = conn.cursor()
        cur.execute('''
            alter table %s
            add column %s %s
        ''' % (table, colname, data_type))
        conn.commit()
        cur.close()
        conn.close()
    return


def update_db_table(schema, tbname_a, colname_a, tbname_b, colname_b):
    '''
    Data from column b in table b is written into column a in table a
    where id_a = id_b.

    Keyword arguments:
        schema - name of the postgres schema
        tbname - name of the table in the postgres database
        colname - column name
    '''
    table_a = schema + '.' + tbname_a
    table_b = schema + '.' + tbname_b
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute('''
    update %s as h
    set %s = t.%s
    from %s as t
    where h.id = t.id
    ''' % (table_a, colname_a, colname_b, table_b))
    conn.commit()
    cur.close()
    conn.close()
    return


def update_row(schema, tbname, colname, colname_where, value, where_value):
    '''
    Updates a value in a column where the where-condition applies.
    If the value or where_value is a string, it has to be written in double
    quotation marks ("'string_name'").

    Keyword arguments:
        schema - name of the postgres schema
        tbname - name of the table in the postgres database
        colname - column name
        value - value to be written into the column
        colname_where - column name for where-condition
        where_value - value for where-condition
    '''
    table = schema + '.' + tbname
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute('''
    update %s
    set "%s" = %s
    where "%s" = %s
    ''' % (table, colname, value, colname_where, where_value))
    conn.commit()
    cur.close()
    conn.close()
    return


def create_db_table(schema, tbname, colname_data_type):
    '''
    Creates a table with the columns specified in colname_data_type.
    The ID column is created automatically and set to be the primary key.

    Keyword arguments:
        schema - name of the postgres schema
        tbname - name of the table in the postgres database
        colname_data_type - list of colum names and data type of the input data
    '''
    table = schema + '.' + tbname
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute('''
    create table if not exists %s
    (
    id INT,
    %s,
    PRIMARY KEY (id)
    );
    ''' % (table, colname_data_type))
    conn.commit()
    cur.close()
    conn.close()
    return


def insert_data_into_db_table(schema, tbname, colname, values):
    '''
    Inserts one or several rows at once.

    Keyword arguments:
        schema - name of the postgres schema
        tbname - name of the table in the postgres database
        colname - list of column names
        values - string containing the data that is to be inserted
    '''
    table = schema + '.' + tbname
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute('''
        insert into %s (%s)
        values %s;
        ''' % (table, colname, values))
    conn.commit()
    cur.close()
    conn.close()
    return


def drop_db_table(schema, tbname):
    '''
    Keyword arguments:
        schema - name of the postgres schema
        tbname - name of the table in the postgres database
    '''
    table = schema + '.' + tbname
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute('''
        drop table if exists %s
        ''' % (table))
    conn.commit()
    cur.close()
    conn.close()
    return


def get_primary_key(tbname):
    '''
    Retrieves the primary key of a given database table.
    '''
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute('''
        select c.column_name
        from information_schema.table_constraints as tc
        join information_schema.constraint_column_usage as ccu
        using (constraint_schema, constraint_name)
        join information_schema.columns as c
        on c.table_schema = tc.constraint_schema
        and tc.table_name = c.table_name
        and ccu.column_name = c.column_name
        where constraint_type = 'PRIMARY KEY'
        and tc.table_name = %(str)s
    ''', {'str': tbname})
    primary_key = cur.fetchone()[0]
    cur.close()
    conn.close()
    return primary_key


def retrieve_from_db_table(schema, tbname, colname,
    primary_key=None, d_type=float, where_cond=None, order=None):
    '''
    Retrieves data (several rows) from a database table with an optional
    where condition.
    Data is ordered by the primary key if wanted.

    Keyword arguments:
        schema - name of the postgres schema
        tbname - name of the table in the postgres database
        colname - list of colum names
    '''
    # open db connection
    conn = open_db_connection()
    cur = conn.cursor()
    # basic SQL query
    if type(colname) == list:
        sql_string = 'select'
        for column_counter in range(len(colname)):
            sql_string += '"%s"' % colname[column_counter]
            if not column_counter == len(colname) - 1:
                sql_string += ','
    else:
        sql_string = 'select "%s"' % colname
    sql_string += ' from %s.%s' % (schema, tbname)
    # where condition
    if where_cond:
        if type(where_cond) == list:
            sql_string += ' where'
            for cond_counter in range(len(where_cond)):
                sql_string += ' %s' % where_cond[cond_counter]
                if not cond_counter == len(where_cond) - 1:
                    sql_string += ' and'
        else:
            sql_string += ' where %s' % where_cond
    # order by PK
    if primary_key:
        sql_string += ' order by %s' % primary_key
    if order and not primary_key:
        primary_key = get_primary_key(tbname)
        sql_string += ' order by %s' % primary_key
    # execute
    cur.execute('%s' % sql_string)
    data = np.asarray(cur.fetchall(), dtype=d_type)
    # close db connection
    cur.close()
    conn.close()
    return data


def retrieve_max_from_db_table(schema, tbname, colname):
    '''
    Retrieves the maximum value of column from a database table.

    Keyword arguments:
        schema - name of the postgres schema
        tbname - name of the table in the postgres database
        colname - list of colum names
    '''
    # open db connection
    conn = open_db_connection()
    cur = conn.cursor()
    # execute
    cur.execute('select max ("%s") from %s.%s' % (colname, schema, tbname))
    data = np.asarray(cur.fetchone())[0]
    # close db connection
    cur.close()
    conn.close()
    return data


def table_exists(tbname):
    '''
    Checks if a table exists. Returns 'false' if it doesn't exist.

    Keyword arguments:
        tbname - name of the table in the postgres database
    '''
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute('''
        select
        case when %(str)s
        not in (select table_name from information_schema.tables)
        then false
        else true
        end;
        ''', {'str': tbname})
    exists = np.asarray(cur.fetchall())
    cur.close()
    conn.close()
    return exists


def column_exists(schema, table_name, column_name):
    '''
    Checks if column exists and returns true or false
    '''
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute('''
        select column_name from information_schema.columns
        where table_schema = '%s'
        and table_name = '%s';
    ''' % (schema, table_name))
    column_names = np.array(cur.fetchall())
    cur.close()
    conn.close()
    return column_name in column_names


def save_results_to_db(schema, tbname, colname, data):
    '''
    Writes results of load and potential calculations into the database.
    '''
    # name of temporary table
    tmp_table = 'temp'

    # drop column to delete old results from output table
    drop_column_in_db_table(schema, tbname, colname)

    # create column for new results
    add_column_2_db_table(schema, tbname, colname, 'real')

    # temporary table for caching of results
    drop_db_table(schema, tmp_table)
    create_db_table(schema, tmp_table, 'temp_colname real')
    stringi = '(1,' + str(data[0]) + ')'
    for i in range(2, 8761):
        stringi = (stringi + ',(' + str(i) + ',' + str(data[i - 1]) + ')')

    insert_data_into_db_table(schema, tmp_table, 'id, temp_colname', stringi)

    # write results into output table
    update_db_table(schema, tbname, colname, tmp_table, 'temp_colname')

    # drop temporary table
    drop_db_table(schema, tmp_table)
    return


def np_array_2db(schema, tbname, colnames, array):
    '''
    Function to write a 2D numpy array into a postgres database.

    Keyword arguments:
        schema - name of the postgres schema
        tbname - name of the table in the postgres database
        colname - list of colum names
        array - 2D array with the data to be inserted
    '''
    # connecting to the database
    conn = open_db_connection()
    cur = conn.cursor()

    # drop old table (if exists) and create a new one
    table = schema + '.' + tbname
    cur.execute('DROP TABLE IF EXISTS %s;' % table)
    cur.execute('''CREATE TABLE IF NOT EXISTS %s
                (id integer PRIMARY KEY);''' % table)

    # create the columns
    for i in colnames:
        cur.execute('ALTER TABLE %s ADD COLUMN "%s" real;' % (table, i))

    # write the data into the table
    stringdb = ''
    for i in range(array.shape[0]):
        # ID
        sql_data = [i + 1]
        for j in range(array.shape[1]):
            sql_data.append(array[i, j])
        tmpstring = ('INSERT INTO %s VALUES %s ; ' % (table, tuple(sql_data)))
        stringdb = stringdb + tmpstring
    cur.execute(stringdb)

    # commit changes and close the database connection
    conn.commit()
    cur.close()
    conn.close()
    return


def write_comment(comment, schema, table, column=None):
    '''
    Writes a comment to a given table or column
    if the name of the column is defined.
    '''
    conn = open_db_connection()
    cur = conn.cursor()
    tb_name = schema + '.' + table
    if column is None:
        cur.execute('''COMMENT ON TABLE %s.%s IS '%s';''' % (
            schema, table, comment))
    else:
        cur.execute('''COMMENT ON COLUMN %s.%s IS '%s';''' % (
            tb_name, column, comment))
    conn.commit()
    cur.close()
    conn.close()
    return


def read_comment(schema, table, column=None):
    '''
    Returns the comment of a given table or column
    if the name of the column is defined.
    '''
    conn = open_db_connection()
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
    cur.close()
    conn.close()
    return comment


def write_profiles_to_db(p_set, hourly_el_demand, hourly_heat_demand,
    hourly_wind_potential, hourly_pv_potential, hourly_st_potential,
    pahesmf=None):
    '''
    Writes the load and potential profiles into the database.
    '''
    year = '_' + str(p_set['info']['sim_year'])
    region = '_' + list(p_set['parameter']['component'].keys())[0]

    # dictionaries for database column names
    if pahesmf:
        name_dict = {'PV Potential': 'rpvo' + region + year,
            'Wind Potential': 'rwin' + region + year,
            'ST Potential': 'st_pot',  # vorläufig!! - 4code character ?
            'ST': '"ST"',  # vorläufig!! - 4code character ?
            'Elec. Demand': (list(p_set['parameter']['component'].keys())[0]
                + year),
            'Gas': 'thng' + region + year,  # Dec. Gas Heating Demand
            'Oil': 'thoi' + region + year,  # Dec. Oil Heating Demand
            'Biomass': 'thbm' + region + year,  # Dec. Biomass Heating Demand
            'Coal': 'thco' + region + year,  # Dec. Coal Heating Demand
            'HP Mono Air Heating': 'thp1' + region + year,  # Dec. HP
                # (Mono Air) Heating Demand
            'HP Mono Air WW': 'thp2' + region + year,  # Dec. HP (Mono Air)
                # WW Demand
            'HP Mono Brine Heating': 'thp3' + region + year,  # Dec. HP
                # (Mono Brine) Heating Demand
            'HP Mono Brine WW': 'thp4' + region + year,  # Dec. HP (Mono Brine)
                # WW Demand
            'DH': 'dst0' + region + year,  # DH Demand
            'Gas Cog unit': '"Gas Cog unit"',  # vorläufig!! -
                                               # 4code character ??
            'Biogas Cog unit': '"Biogas Cog unit"'  # vorläufig!! -
                                                    # 4code character ??
            }
        p_set['schema'] = p_set['out_schema']
    else:
        name_dict = {'PV Potential': 'pv_pot',
            'Wind Potential': 'wind_pot',
            'ST Potential': 'st_pot',
            'ST': '"ST"',
            'Elec. Demand': '"El"',
            'Gas': '"Gas"',
            'Oil': '"Oil"',
            'Biomass': '"Biomass"',
            'Coal': '"Coal"',
            'HP Mono Air Heating': '"HP Mono Air Heating"',
            'HP Mono Air WW': '"HP Mono Air WW"',
            'HP Mono Brine Heating': '"HP Mono Brine Heating"',
            'HP Mono Brine WW': '"HP Mono Brine WW"',
            'DH': '"DH"',
            'Gas Cog unit': '"Gas Cog unit"',
            'Biogas Cog unit': '"Biogas Cog unit"'
            }
    # insert el. demand
    # drop column
    drop_column_in_db_table(p_set['schema'], p_set['load_pot_table'],
        name_dict['Elec. Demand'])
    # add column
    add_column_2_db_table(p_set['schema'], p_set['load_pot_table'],
        name_dict['Elec. Demand'], 'real')
    # insert
    save_results_to_db(p_set['schema'], p_set['load_pot_table'],
        name_dict['Elec. Demand'], hourly_el_demand[:, ])

    # insert hourly heat demand
    for i in hourly_heat_demand:
        # drop column
        drop_column_in_db_table(p_set['schema'], p_set['load_pot_table'],
            name_dict[i])
        # add column
        add_column_2_db_table(p_set['schema'], p_set['load_pot_table'],
            name_dict[i], 'real')
        # insert heat demand
        save_results_to_db(p_set['schema'], p_set['load_pot_table'],
            name_dict[i], hourly_heat_demand[i])

    # insert wind potential
    # drop column
    drop_column_in_db_table(p_set['schema'], p_set['load_pot_table'],
        name_dict['Wind Potential'])
    # add column
    add_column_2_db_table(p_set['schema'], p_set['load_pot_table'],
        name_dict['Wind Potential'], 'real')
    # insert
    save_results_to_db(p_set['schema'], p_set['load_pot_table'],
        name_dict['Wind Potential'], hourly_wind_potential)

    # insert pv potential
    # drop column
    drop_column_in_db_table(p_set['schema'], p_set['load_pot_table'],
        name_dict['PV Potential'])
    # add column
    add_column_2_db_table(p_set['schema'], p_set['load_pot_table'],
        name_dict['PV Potential'], 'real')
    # insert
    save_results_to_db(p_set['schema'], p_set['load_pot_table'],
        name_dict['PV Potential'], hourly_pv_potential)

    # insert st potential
    # drop column
    drop_column_in_db_table(p_set['schema'], p_set['load_pot_table'],
        name_dict['ST Potential'])
    # add column
    add_column_2_db_table(p_set['schema'], p_set['load_pot_table'],
        name_dict['ST Potential'], 'real')
    # insert
    save_results_to_db(p_set['schema'], p_set['load_pot_table'],
        name_dict['ST Potential'], hourly_st_potential)

    return


################################ text file operations #######################


def create_dir(directory):
    ''
    if os.path.isdir(directory) is False:
        os.mkdir(directory)
    return


def read_profiles_from_file(filename, directory):
    '''
    Reads hourly profiles from a file and writes them into the dictionary
    'data'.
    Keyword arguments:
        filename -- name of data file with filename extension (e.g. 'test.txt')
        directory -- path to directory containing the data file
    Requirements to file:
        - Profiles must be in columns
        - Columns must have headings
        - Delimiters must be ';'
        - Decimal mark must be a point
    '''
    # open file
    data_file = open(directory + "/" + filename, "r")

    # write file content to dictionary 'data'
    counter = 0
    data = {}

    for line in data_file:
        # first line in file contains column headings
        # headings are keys of the load_profile dictionary
        if counter == 0:
            headings = line.split()
            heading = []
            for i in range(len(headings)):
                heading.append(headings[i].replace(";", "", 1))
                data[heading[i]] = np.zeros((8760, 1))
        # other lines contain hourly load profile values
        else:
            values = line.split()
            for i in range(len(values)):
                data[heading[i]][counter - 1] = \
                    float(values[i].replace(";", "", 1))
        counter += 1

    # close .txt-file
    data_file.close()

    return data


def read_data_from_file(filename, directory):
    '''
    Reads data from a file and writes them into a matrix "data".
    Keyword arguments:
        filename -- name of data file with filename extension (e.g. 'test.txt')
        directory -- path to directory containing the data file
    Requirements to file:
        - Delimiters must be ';'
        - Decimal mark must be a point
    '''
    # open file
    data_file = open(directory + "/" + filename, "r")

    # number of rows
    rows = 0
    for line in data_file:
        rows += 1
    # number of columns
    columns = len(line.split(';'))

    # initialize data
    data = np.zeros((rows, columns))

    # close .txt-file
    data_file.close()

    # reopen file
    data_file = open(directory + "/" + filename, "r")

    # write file content to 'data' matrix
    counter = 0
    for line in data_file:
        values = line.split(';')
        for i in range(len(values)):
            data[counter, i] = \
                float(values[i].replace(";", "", 1))
        counter += 1

    # close .txt-file
    data_file.close()

    return data


def db_table_colnames_2_file(db_table_name, fout, delimiters=';'):
    '''
    Exports the column names of a database table to a file.
    '''
    conn = open_db_connection()
    cur = conn.cursor()

    # read the names of the columns of the database table
    cur.execute('''SELECT column_name FROM information_schema.columns
                WHERE table_name = '%s';''' % db_table_name)
    colnames = np.asarray(cur.fetchall())

    # write to file
    for i in range(len(colnames)):
        fout.write(colnames[i, 0] + ';')
    fout.write('\n')

    cur.close()
    conn.close()
    return


def db_table_2_file(schema, db_table_name, filename, delimiters=';'):
    '''
    Exports a database table to a file.
    '''
    conn = open_db_connection()
    cur = conn.cursor()

    # open file
    fout = open(filename, 'w')
    # write column names to file
    db_table_colnames_2_file(db_table_name, fout, delimiters=';')
    # write data to file
    cur.copy_to(fout, schema + '.' + db_table_name, sep=delimiters)

    cur.close()
    conn.close()
    fout.close()
    return


def dict_2_file(dict_name, filename, delimiters=';'):
    '''
    Exports a dictionary to a file.
    '''

    # open file
    fout = open(filename, 'w')
    # write data to file
    for i in (list(dict_name.keys())):
        fout.write(i + ':;' + str(dict_name[i]))
        fout.write('\n')
    fout.close()
    return


def array_2_file(array, filename, delimiters=';'):
    '''
    Exports a numpy array to a file.
    '''

    # open file
    fout = open(filename, 'w')
    # write data to file
    for i in range(len(array)):
        fout.write(str(array[i]))
        fout.write('\n')
    fout.close()
    return


def mat_2_file(mat, filename, delimiters=','):
    '''
    Exports a numpy matrix to a file.
    '''

    # open file
    fout = open(filename, 'w')
    # write data to file
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            fout.write(str(mat[i, j]) + delimiters)
        fout.write('\n')
    fout.close()
    return


##################################### Wald ##################################

#View mit allen Waldfächen
#cur.execute('''
#CREATE VIEW wittenberg.wald as
#SELECT flaechen_alle.*, attrib_alle.aliastyp, attrib_alle.aliaswert
#FROM wittenberg.flaechen_alle
#RIGHT JOIN wittenberg.attrib_alle
#ON (flaechen_alle.id = attrib_alle.id)
#WHERE aliasart='Wald, Forst';
#''')

#Gesamtwaldfläche in m² in Kemberg
#cur.execute('''
#select
#sum(st_area(st_intersection(
#(select wittenberg.gemeinden.the_geom
#from wittenberg.gemeinden
#where gemeinden.stadtname = 'Kemberg'),
#(wald.the_geom))::geography))
#from wittenberg.wald
#where st_area(st_intersection(
#(select wittenberg.gemeinden.the_geom
#from wittenberg.gemeinden
#where gemeinden.stadtname = 'Kemberg'),
#(wald.the_geom))::geography) > 0;
#''')

#def test_fun(p_set):

    ## Retrieve parameter set from database
    ##input_data = get_input_data(p_set['project_id'][0])

    ## db connection
    #conn = open_db_connection()
    #cur = conn.cursor()

    ## get el demand
    #cur.execute('''
    #select "El"
    #from wittenberg.generated_load_profiles
    #''')
    #hourly_el_demand = np.asarray(cur.fetchall())

    ## get heat demand
    #cur.execute('''
    #select "Gas", "DH"
    #from wittenberg.generated_load_profiles
    #''')
    #hourly_heat_demand_mat = np.asarray(cur.fetchall())

    #hourly_heat_demand = {'Gas': hourly_heat_demand_mat[:, 0],
        #'DH': hourly_heat_demand_mat[:, 1]}

    ## write to db
    #write_profiles_to_db(p_set, hourly_el_demand, hourly_heat_demand,
        #1, 1)

    ## close db connection
    #cur.close()
    #conn.close()
    #return