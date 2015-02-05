#!/usr/bin/python
# -*- coding: utf-8

import numpy as np
import el_load_profile_ind
import database as db


def annual_heat_demand_calculation_Beer(mat, range_start):
    '''
    Calculation of heat demand for each branch of industry according to
    Beer.
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
        annual_demand[i - range_start] = (((
                        mat[i][7] * mat[i][1] / 100 - mat[i][8])
                        + (mat[i][7] * mat[i][2] / 100 - mat[i][9])
                        + (mat[i][7] * mat[i][3] / 100 - mat[i][10])
                        + (mat[i][7] * mat[i][5] / 100 * 0.54)
                        - mat[i][11]) * 0.85
                        + (mat[i][7] * mat[i][6] / 100)
                        + mat[i][12] * 3.6)
    return annual_demand


def annual_demand_per_branch_Germany():
    '''
    Calculates the annual heat demand of each branch of industry for
    whole Germany.
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
        "Nettowärmeoutput [GWh]"
        from wittenberg.energiebedarf_industrie
        where "EEV Kohle [%]" != -1 and "EEV Heizöl [%]" != -1
        and "EEV Erdgas [%]" != -1 and "EEV Sonstige [%]" != -1
        and "EEV EE [%]" != -1
        and wz != 1 and wz != 2 and sektor = 'C'
        order by wz
    ''')
    # fetch data
    heat_demand_branches_mat = np.asarray(cur.fetchall())
    heat_demand_branches = annual_heat_demand_calculation_Beer(
        heat_demand_branches_mat, 0)

    # branches of industry where data is incomplete
    cur.execute('''
        select wz,
        "EEV Kohle [%]", "EEV Heizöl [%]", "EEV Erdgas [%]",
        "EEV Strom [%]", "EEV EE [%]", "EEV Sonstige [%]", "EEV ges [TJ]",
        "Brennstoffeinsatz Kohle [TJ]", "Brennstoffeinsatz Heizöl [TJ]",
        "Brennstoffeinsatz Gas [TJ]", "Brennstoffeinsatz Sonstiges [TJ]",
        "Nettowärmeoutput [GWh]"
        from wittenberg.energiebedarf_industrie
        where wz = 1 or (sektor = 'C' and
        ("EEV Kohle [%]" = -1 or "EEV Heizöl [%]" = -1
        or "EEV Erdgas [%]" = -1 or "EEV Sonstige [%]" = -1
        or "EEV EE [%]" = -1))
        order by wz
    ''')
    # fetch data
    heat_demand_branches_mat_rest = np.asarray(cur.fetchall())
    heat_demand_branches_mat_rest = el_load_profile_ind.table_fill_up(
        heat_demand_branches_mat_rest)
    heat_demand_branches_rest = annual_heat_demand_calculation_Beer(
        heat_demand_branches_mat_rest, 1)

    # writing results to matrix "annual_heat_demand_branches"
    # matrix with branch of industry (column 0) and the corresponding annual
    # heat demand of that branch for whole Germany (column 1)
    complete_branches = np.zeros(((len(heat_demand_branches), 2)))
    complete_branches[:, 0] = heat_demand_branches_mat[:, 0]
    complete_branches[:, 1] = heat_demand_branches[:, 0]
    incomplete_branches = np.zeros(((len(heat_demand_branches_rest)), 2))
    incomplete_branches[:, 0] = heat_demand_branches_mat_rest[1:, 0]
    incomplete_branches[:, 1] = heat_demand_branches_rest[:, 0]
    annual_heat_demand_branches = np.vstack(
        [complete_branches, incomplete_branches])

    cur.close()
    conn.close()

    return annual_heat_demand_branches


def annual_demand_district(district):
    '''
    Calculates the annual heat demand of each branch of industry for
    the specified district.
    '''
    annual_demand_branches_Germany = annual_demand_per_branch_Germany()
    annual_heat_demand_per_branch_per_employee = \
        el_load_profile_ind.annual_demand_per_branch_per_employee_Germany(
        annual_demand_branches_Germany)
    employees_per_branch_district = \
        el_load_profile_ind.employee_per_branch_district(district)

    demand_per_branch = np.zeros((len(employees_per_branch_district), 1))
    for i in range(len(employees_per_branch_district)):
        demand_per_branch[i] = (employees_per_branch_district[i, 1] *
            annual_heat_demand_per_branch_per_employee[
            annual_heat_demand_per_branch_per_employee[:, 0] ==
            employees_per_branch_district[i, 0], 1])

    return (sum(demand_per_branch) * 10 ** 6 / 3600)[0]


def get_hourly_heat_load_profile(input_data, use_case,
    schema=None, table_name=None, column_name=None,
    filename=None, directory=None,
    step_load_profile_factors=None,
    save=None, save_to_table=None, save_to_column='ind_heat_load',
    annual_demand=None):
    '''
    Returns the hourly heat load in MWh/h of a region. Depending on the
    chosen use case the heat load profile is either retrieved from a file or
    database or generated using step load profiles.
    '''
    # retrieve heat load profile from the database
    if use_case == 'db':
        if db.table_exists(table_name):
            hourly_heat_demand = db.retrieve_from_db_table(
                schema, table_name, column_name, order='yes')
            hourly_heat_demand = np.reshape(hourly_heat_demand, (-1, ))
        else:
            print (('Table to retrieve the industrial heat load profile ' +
            'does not exist.'))
    # retrieve heat load profile from file
    elif use_case == 'file':
        hourly_heat_demand = \
            db.read_profiles_from_file(filename, directory)[column_name]
        hourly_heat_demand = np.reshape(hourly_heat_demand, (-1, ))
    # calculate heat load profile
    elif use_case == 'slp_generation':
        if not annual_demand:
            # calculate annual heat demand
            annual_demand = annual_demand_district(input_data['district'])
        # generate load profile
        hourly_heat_demand = el_load_profile_ind.load_profile(
            annual_demand, step_load_profile_factors)
        hourly_heat_demand = np.reshape(hourly_heat_demand, (-1, ))

    else:
        print (('Heat load profile cannot be generated because of invalid ' +
        'use case. The use case chosen was: %s' % use_case))

    # save results to db
    if save:
        if db.table_exists(save_to_table):
            db.save_results_to_db(
                schema, save_to_table, save_to_column, hourly_heat_demand)
        else:
            # create output table and id column
            db.create_db_table(schema, save_to_table,
                save_to_column + ' real')
            stringi = '(1)'
            for i in range(2, 8761):
                stringi = stringi + ',(' + str(i) + ')'
            db.insert_data_into_db_table(schema, save_to_table, 'id', stringi)
            db.save_results_to_db(
                schema, save_to_table, save_to_column, hourly_heat_demand)

    return hourly_heat_demand