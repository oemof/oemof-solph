#!/usr/bin/python
# -*- coding: utf-8 -*-


'''
Author: Guido Plessmann
E-mail: guido.plessmann@ri-institut.de
Changes by: ...
Responsibility: Guido Plessmann
'''

import dblib as db
import basic_dinput_functions as bf
import re


def write_results_to_presetting(basic_dc, main_dc, tables, year_of_last_simu,
    sim_year):
    '''Writes reults from simulation to presetting table. Results obtained from
    simulation are used as input to consecutive simulation'''
    regions = main_dc['parameter']['component'].keys()
    for tab in tables:
        table_name =  main_dc['info']['name_set'] + '__' + tab
        col_names = bf.remove_from_list(db.fetch_column_names(basic_dc,
            basic_dc['res_schema'], table_name), ['id', 'region'])
        if tab is 'trm_inst':
            lines = bf.remove_from_list(db.fetch_column_names(basic_dc,
                basic_dc['res_schema'], table_name), ['id'])
            for line in lines:
                c = 'grid'  # hardcoded for testing, may by changed later
                eoo_year = (year_of_last_simu +
                    main_dc['parameter']['transmission'][line]['lifetime']
                    - 1)
                from_s = '''(select "%s" from %s.%s where
                    id=%s) ''' % (
                line, basic_dc['res_schema'], table_name, main_dc['info']['id'])
                print('presetting_set: ' + main_dc['info']['presetting_set'])
                old_presetting_set = re.sub('\d{4}', str(year_of_last_simu),
                     main_dc['info']['presetting_set'])
                print('old: ' + old_presetting_set)
                old_value = '''select sum(presetted_summed_power)
               _    from pahesmf_dat.presetting
                    where component = '{0}'
                    and region = '{1}'
                        and presetting_set = '{2}'
                        and eoo_year >= {3}'''.format(c, line,
                        old_presetting_set, eoo_year)

                insert_s = '''insert into pahesmf_dat.presetting (component,
                    region, presetted_summed_power, presetting_set, eoo_year)
                    values('%s', '%s', %s, '%s', %s);''' % (
                    c, line, '(select (' + from_s + ') + (' + old_value + '))',
                     main_dc['info']['presetting_set'], eoo_year)
                db.execute_write_db(basic_dc, insert_s)
                years_str = '''select distinct eoo_year from
                    pahesmf_dat.presetting
                    where eoo_year >= {0}
                    and eoo_year < {3}
                    and presetting_set = '{1}'
                    and component = '{2}';'''.format(sim_year,
                        old_presetting_set, c, eoo_year)
                years = db.execute_read_db(basic_dc, years_str)
                years = [x[0] for x in years]
                for y in years:
                    copy_value_str = '''select presetted_summed_power
                    from pahesmf_dat.presetting
                    where presetting_set = '{0}'
                    and component = '{1}'
                    and region = '{2}'
                    and eoo_year = {3}
                    '''.format(old_presetting_set, c, line, y)
                    old_presetting = db.execute_read_db(basic_dc,
                        copy_value_str)[0][0]
                    if not old_presetting:
                        old_presetting = 0
                    insert_str = '''insert into pahesmf_dat.presetting
                        (component, region, presetted_summed_power,
                        presetting_set,eoo_year) values('{0}', '{1}', {2},
                        '{3}', {4})'''.format(c, line, old_presetting,
                         main_dc['info']['presetting_set'], y)
                    db.execute_write_db(basic_dc, insert_str)
        else:
            for c in col_names:
                for r in regions:
                    eoo_year = (year_of_last_simu +
                        main_dc['parameter']['component'][r][c]['lifetime']
                        - 1)
                    from_s = '''(select %s from %s.%s where
                        id=%s and region='%s') ''' % (
                    c, basic_dc['res_schema'], table_name, main_dc['info']['id']
                        , r)

                    # get value from previous
                    old_presetting_set = re.sub('\d{4}', str(year_of_last_simu),
                                 main_dc['info']['presetting_set'])
                    old_value_s = '''select sum(presetted_summed_power)
                   _    from pahesmf_dat.presetting
                        where component = '{0}'
                        and region = '{1}'
                        and presetting_set = '{2}'
                        and eoo_year >= {3}'''.format(c, r, old_presetting_set,
                        eoo_year)

                    # retrieve values from previous presetting and results
                    old_value = db.execute_read_db(basic_dc, old_value_s)[0][0]
                    if old_value is None:
                        old_value = 0
                    prev_results = db.execute_read_db(basic_dc, from_s)[0][0]
                    if prev_results is None:
                        prev_results = 0

                    # write sum of new installations and exisiting capacities
                    # to current presetting
                    insert_s = '''insert into pahesmf_dat.presetting (component,
                        region, presetted_summed_power, presetting_set,
                        eoo_year)
                        values('%s', '%s', %s, '%s', %s)''' % (
                        c, r, prev_results + old_value,
                         main_dc['info']['presetting_set'], eoo_year)
                    db.execute_write_db(basic_dc, insert_s)

                    # get list of eoo-years whose values should be copied. list
                    # of years starts with current simulation year
                    years_str = '''select distinct eoo_year from
                        pahesmf_dat.presetting
                        where eoo_year >= {0}
                        and eoo_year < {3}
                        and presetting_set = '{1}'
                        and component = '{2}';'''.format(sim_year,
                        old_presetting_set, c, eoo_year)
                    years = db.execute_read_db(basic_dc, years_str)
                    years = [x[0] for x in years]

                    # copy values from previous presetting set to current
                    for y in years:
                        copy_value_str = '''select presetted_summed_power
                            from pahesmf_dat.presetting
                            where presetting_set = '{0}'
                            and component = '{1}'
                            and region = '{2}'
                            and eoo_year = {3}
                            '''.format(old_presetting_set, c,
                                r, y)
                        old_presetting = db.execute_read_db(basic_dc,
                            copy_value_str)[0][0]
                        if old_presetting is None:
                            old_presetting = 0
                        insert_str = '''insert into pahesmf_dat.presetting
                            (component, region, presetted_summed_power,
                            presetting_set, eoo_year) values('{0}', '{1}', {2},
                            '{3}', {4})'''.format(
                            c, r, old_presetting,  main_dc['info']['presetting_set'], y)
                        db.execute_write_db(basic_dc, insert_str)


def get_operating_years(parameter_dc, c, r):
    '''Returns lifetime of a component found in an arbitrary parameter table'''
    parameter_subdc = ['parameter_re', 'parameter_transformer4elec',
        'parameter_transformer4gas', 'parameter_storages4elec',
        'parameter_storages4gas', 'parameter_transmission_type']

    for psd in parameter_subdc:
        try:
            if c:
                lifetime = parameter_dc['parameter'][psd][r][c]['lifetime']
            else:
                lifetime = (parameter_dc['parameter']['parameter_transmission']
                    [r][psd]['lifetime'])
        except KeyError:
            pass
    return lifetime


def create_tmp_view_string(region):
    '''Returns sql-query to create a view for a selected from gadm_countries'''
    sql_str = '''CREATE OR REPLACE VIEW pahesmf_dat.tmpview as
        SELECT p_tmp.*
        FROM world.plantregister_platts as p_tmp,
        world.gadm_countries as gc
        where st_contains(gc.geom, p_tmp.the_geom)
        and gc.iso='{0}';'''.format(region)
    return sql_str


def platts_capacities(comp, year):
    '''Returns sql-query to select summed power of a component with given year
    of commissioning'''
    sql_str = '''SELECT sum(mw) FROM pahesmf_dat.tmpview platts
    INNER JOIN pahesmf_dat.presettingfuel2platt pdat ON
    platts.fuel = pdat.platt_fuel_name
    WHERE pdat.pahesmf_fuel_name = '{0}'
    AND platts.year >= '{1}';'''.format(comp, year)
    return sql_str