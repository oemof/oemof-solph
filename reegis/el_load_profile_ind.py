#!/usr/bin/python
# -*- coding: utf-8

import numpy as np
import database as db


def annual_el_demand_calculation_Beer(mat, range_start):
    '''
    Calculation of electricity demand for each branch of industry in TJ
    according to Beer.
    Columns of input matrix "mat":

        0 - wz (branch of industry)
        1 - EEV Kohle [%] (end energy consumption coal)
        2 - EEV Heizöl [%] (end energy consumption oil)
        3 - EEV Erdgas [%] (end energy consumption gas)
        4 - EEV Strom [%] (end energy consumption electricity)
        5 - EEV EE [%] (end energy consumption renewables)
        6 - EEV Sonstige [%] (end energy consumption others)
        7 - EEV ges [TJ] (total end energy consumption)
        8 - Brennstoffeinsatz Kohle [TJ] (fuel input coal)
        9 - Brennstoffeinsatz Heizöl [TJ] (fuel input oil)
        10 - Brennstoffeinsatz Gas [TJ] (fuel input gas)
        11 - Brennstoffeinsatz Sonstiges [TJ] (fuel input others)
        12 - Nettowärmeoutput [GWh] (net heat output)
        13 - Nettostromoutput [GWh] [net electricity output)
    '''
    # initialisation of output vector
    annual_demand = np.ones((mat.shape[0] - range_start, 1))
    # iteration over branches of industry
    for i in range(range_start, mat.shape[0]):
        annual_demand[i - range_start] = \
            (mat[i][7] * mat[i][4] / 100
            + mat[i][7] * mat[i][5] / 100 * 0.46 + mat[i][13] * 3.6)
    return annual_demand


def table_fill_up(mat):
    '''
    Fills up missing shares of energy sources in the industry energy consumption
    statistic based on weighed percentages.
    '''
    # iteration over branches of industry
    for i in range(1, mat.shape[0]):

        sum_missing = 0  # sum of missing percentages
        sum_known = 0  # sum of known percentages
        col_list = []  # list with number of column with missing percentage

        # iteration over fuels
        for j in range(1, 7):

            if mat[i][j] == -1:
                sum_missing += mat[0][j]
                col_list.append(j)
            else:
                sum_known += mat[i][j]

        if len(col_list) <= 1:
            mat[i][col_list[0]] = 100 - sum_known
        else:
            for k in col_list:
                mat[i][k] = (mat[0][k] / sum_missing * (100 - sum_known))
    return mat


def annual_demand_per_branch_Germany():
    '''
    Calculates the annual electricity demand in TJ of each branch of industry
    for whole Germany.
    '''
    conn = db.open_db_connection()
    cur = conn.cursor()

    # branches of industry where all data is complete
    cur.execute('''
        select wz,
        "EEV Kohle [%]", "EEV Heizöl [%]", "EEV Erdgas [%]",
        "EEV Strom [%]", "EEV EE [%]", "EEV Sonstige [%]", "EEV ges [TJ]",
        "Brennstoffeinsatz Kohle [TJ]", "Brennstoffeinsatz Heizöl [TJ]",
        "Brennstoffeinsatz Gas [TJ]", "Brennstoffeinsatz Sonstiges [TJ]",
        "Nettowärmeoutput [GWh]", "Nettostromoutput [GWh]"
        from wittenberg.energiebedarf_industrie
        where "EEV Strom [%]" != -1 and "EEV EE [%]" != -1
        and wz != 1 and wz != 2 and sektor = 'C'
        order by wz
    ''')
    # fetch data
    el_demand_branches_mat = np.asarray(cur.fetchall())
    el_demand_branches = annual_el_demand_calculation_Beer(
        el_demand_branches_mat, 0)

    # branches of industry where data is incomplete
    cur.execute('''
        select wz,
        "EEV Kohle [%]", "EEV Heizöl [%]", "EEV Erdgas [%]",
        "EEV Strom [%]", "EEV EE [%]", "EEV Sonstige [%]", "EEV ges [TJ]",
        "Brennstoffeinsatz Kohle [TJ]", "Brennstoffeinsatz Heizöl [TJ]",
        "Brennstoffeinsatz Gas [TJ]", "Brennstoffeinsatz Sonstiges [TJ]",
        "Nettowärmeoutput [GWh]", "Nettostromoutput [GWh]"
        from wittenberg.energiebedarf_industrie
        where wz = 1 or (sektor = 'C' and
        ("EEV Strom [%]" = -1 or "EEV EE [%]" = -1))
        order by wz
    ''')
    # fetch data
    el_demand_branches_mat_rest = np.asarray(cur.fetchall())
    el_demand_branches_mat_rest = table_fill_up(el_demand_branches_mat_rest)
    el_demand_branches_rest = annual_el_demand_calculation_Beer(
        el_demand_branches_mat_rest, 1)

    # writing results to matrix "annual_el_demand_branches"
    # matrix with branch of industry (column 0) and the corresponding annual
    # electricity demand of that branch for whole Germany (column 1)
    complete_branches = np.zeros(((len(el_demand_branches), 2)))
    complete_branches[:, 0] = el_demand_branches_mat[:, 0]
    complete_branches[:, 1] = el_demand_branches[:, 0]
    incomplete_branches = np.zeros(((len(el_demand_branches_rest)), 2))
    incomplete_branches[:, 0] = el_demand_branches_mat_rest[1:, 0]
    incomplete_branches[:, 1] = el_demand_branches_rest[:, 0]
    annual_el_demand_branches = np.vstack(
        [complete_branches, incomplete_branches])

    cur.close()
    conn.close()

    return annual_el_demand_branches


def annual_demand_per_branch_per_employee_Germany(
    annual_demand_branches_Germany):
    '''
    Calculates the annual demand per employee of each branch of
    industry for whole Germany.
    '''
    conn = db.open_db_connection()
    cur = conn.cursor()

    # retrieve number of employees of each branch of industry for whole Germany
    # from database
    number_employees = np.zeros((len(annual_demand_branches_Germany), ))
    for i in range(len(annual_demand_branches_Germany)):
        branch_string = 'WZ080' + str(int(annual_demand_branches_Germany[i][0]))
        # SQL statement
        cur.execute('''
            select beschaeftigte_anzahl
            from wittenberg.beschaeftigungsstatistik_d_industrie
            where wz = %(str)s
        ''', {'str': branch_string})
        number_employees[i] = np.asarray(cur.fetchone())[0]

    # demand per employee
    annual_demand_per_branch_per_employee = \
        np.zeros((len(number_employees), 2))
    annual_demand_per_branch_per_employee[:, 0] = \
        annual_demand_branches_Germany[:, 0]
    annual_demand_per_branch_per_employee[:, 1] = \
        annual_demand_branches_Germany[:, 1] / number_employees

    cur.close()
    conn.close()

    return annual_demand_per_branch_per_employee


def missing_employee_numbers_fill_up(missing_branches,
    sum_missing_employee_numbers):
    '''
    Generates missing employee numbers based on the distribution of employees
    in the state the district is in.
    '''
    conn = db.open_db_connection()
    cur = conn.cursor()

    # retrieve number of employees of missing branches in the state the district
    # is in
    number_employees_state = np.zeros((len(missing_branches), 2))
    for i in range(len(missing_branches)):
        branch_string = str(missing_branches[i][0])
        cur.execute('''
            select "Beschäftigte"
            from wittenberg.beschaeftigungsstatistik_sa
            where "WZ" = %(str)s
        ''', {'str': branch_string})
        number_employees_state[i, 0] = missing_branches[i]
        number_employees_state[i, 1] = np.asarray(cur.fetchone())[0]

    # calculate share of each branch of all missing branches
    share_branch = (number_employees_state[:, 1] /
        sum(number_employees_state[:, 1]))

    # missing employee numbers of each branch
    missing_employee_numbers = np.zeros((len(missing_branches), 2))
    missing_employee_numbers[:, 0] = missing_branches[:, 0]
    missing_employee_numbers[:, 1] = np.around(
        share_branch * sum_missing_employee_numbers)

    cur.close()
    conn.close()

    return missing_employee_numbers


def employee_per_branch_district(district):
    '''
    Retrieves the number of employees in the specified district of each branch
    of industry. Where numbers are missing the employee statistic of the state
    the district is in is used as a reference to make an educated guess of the
    number of employees in that branch.
    '''
    conn = db.open_db_connection()
    cur = conn.cursor()

    # total number of employees in the district
    cur.execute('''
        select "Anzahl Beschäftigte"
        from wittenberg.beschaeftigungsstatistik_wb_industrie
        where wz = '1' and gemeinde = %(str)s
    ''', {'str': district})
    sum_employees_district = np.asarray(cur.fetchone())[0]

    # branches of industry where data is complete
    cur.execute('''
        select wz, "Anzahl Beschäftigte"
        from wittenberg.beschaeftigungsstatistik_wb_industrie
        where "Anzahl Beschäftigte" != -1 and wz != 1 and gemeinde = %(str)s
    ''', {'str': district})
    known_employee_numbers = np.asarray(cur.fetchall())

    # number of employees assignable to a branch
    sum_known_employee_numbers = sum(known_employee_numbers[:, 1])

    # branches of industry where data is incomplete
    cur.execute('''
        select wz
        from wittenberg.beschaeftigungsstatistik_wb_industrie
        where "Anzahl Beschäftigte" = -1 and gemeinde = %(str)s
    ''', {'str': district})
    branches_missing_employee_numbers = np.asarray(cur.fetchall())

    # number of employees not assignable to a branch
    sum_missing_employee_numbers = (sum_employees_district -
        sum_known_employee_numbers)

    # call definition to generate employee numbers for the missing branches
    missing_employee_numbers = missing_employee_numbers_fill_up(
        branches_missing_employee_numbers, sum_missing_employee_numbers)

    cur.close()
    conn.close()

    # write employee numbers to matrix
    employees_per_branch_district = \
        np.vstack([known_employee_numbers, missing_employee_numbers])

    return employees_per_branch_district


def annual_demand_district(district):
    '''
    Calculates the annual electricity demand in MWh of each branch of industry
    for the specified district.
    '''
    annual_demand_branches_Germany = annual_demand_per_branch_Germany()
    annual_el_demand_per_branch_per_employee = \
        annual_demand_per_branch_per_employee_Germany(
        annual_demand_branches_Germany)
    employees_per_branch_district = employee_per_branch_district(district)

    demand_per_branch = np.zeros((len(employees_per_branch_district), 1))
    for i in range(len(employees_per_branch_district)):
        demand_per_branch[i] = (employees_per_branch_district[i, 1] *
            annual_el_demand_per_branch_per_employee[
            annual_el_demand_per_branch_per_employee[:, 0] ==
            employees_per_branch_district[i, 0], 1])

    return (sum(demand_per_branch) * 10 ** 6 / 3600)[0]


def load_profile(annual_demand, p_set):
    '''
    Generates a load profile where the hourly load depends on if it is night
    or day and a weekday or weekend day.
    '''

    # generate matrix "weekday_hours" where the first column contains the number
    # of the weekday (monday = 1 etc.) for all 8760 hours of the year and the
    # second column contains the hour of the day (from 1 to 24) for all 8760
    # hours of the year
    conn = db.open_db_connection()
    cur = conn.cursor()
    cur.execute('''
        select wochentag, tagesstunden
        from wittenberg.stunden_tage
        order by id
    ''')
    weekday_hours = np.asarray(cur.fetchall())
    cur.close()
    conn.close()

    # assign factor to every hour of the year
    factor = np.zeros((len(weekday_hours), 1))
    for i in range(len(factor)):
        # if weekday
        if weekday_hours[i, 0] < 6:
            # if night
            if (weekday_hours[i, 1] < p_set['day_start'] or
                weekday_hours[i, 1] >= p_set['night_start']):
                factor[i, 0] = p_set['night_weekday_factor']
            #if day
            else:
                factor[i, 0] = p_set['day_weekday_factor']
        # if weekend
        else:
            # if night
            if (weekday_hours[i, 1] < p_set['day_start'] or
                weekday_hours[i, 1] >= p_set['night_start']):
                factor[i, 0] = p_set['night_weekend_factor']
            #if day
            else:
                factor[i, 0] = p_set['day_weekend_factor']

    # generate load profile
    el_load_profile = ((factor / sum(factor) * annual_demand))

    return el_load_profile


def get_hourly_el_load_profile(input_data, use_case,
    schema=None, table_name=None, column_name=None,
    filename=None, directory=None,
    step_load_profile_factors=None,
    save=None, save_to_table=None, save_to_column='ind_el_load',
    annual_demand=None):
    '''
    Returns the hourly el load in MWh/h of a region. Depending on the
    chosen use case the el load profile is either retrieved from a file or
    database or generated using step load profiles.
    '''
    # retrieve el load profile from the database
    if use_case == 'db':
        if db.table_exists(table_name):
            hourly_el_demand = db.retrieve_from_db_table(
                schema, table_name, column_name, order='yes')
            hourly_el_demand = np.reshape(hourly_el_demand, (-1, ))
        else:
            print (('Table to retrieve the industrial heat load profile ' +
            'does not exist.'))
    # retrieve heat load profile from file
    elif use_case == 'file':
        hourly_el_demand = \
            db.read_profiles_from_file(filename, directory)[column_name]
        hourly_el_demand = np.reshape(hourly_el_demand, (-1, ))
    # calculate heat load profile
    elif use_case == 'slp_generation':
        if not annual_demand:
            # calculate annual heat demand
            annual_demand = annual_demand_district(input_data['district'])
        # generate load profile
        hourly_el_demand = load_profile(
            annual_demand, step_load_profile_factors)
        hourly_el_demand = np.reshape(hourly_el_demand, (-1, ))

    else:
        print (('El load profile cannot be generated because of invalid ' +
        'use case. The use case chosen was: %s' % use_case))

    # save results to db
    if save:
        if db.table_exists(save_to_table):
            db.save_results_to_db(
                schema, save_to_table, save_to_column, hourly_el_demand)
        else:
            # create output table and id column
            db.create_db_table(schema, save_to_table,
                save_to_column + ' real')
            stringi = '(1)'
            for i in range(2, 8761):
                stringi = stringi + ',(' + str(i) + ')'
            db.insert_data_into_db_table(schema, save_to_table, 'id', stringi)
            db.save_results_to_db(
                schema, save_to_table, save_to_column, hourly_el_demand)

    return hourly_el_demand