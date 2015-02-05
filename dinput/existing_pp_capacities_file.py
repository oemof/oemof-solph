#!/usr/bin/python
# -*- coding: utf-8 -*-


'''
Author: Finn Grohmann
E-mail: finn.grohmann@ri-institut.de
Changes by:
Responsibility: Finn Grohmann, Guido Plessmann

This tool creats the presetting for the power plants

Info

    * Values obtained in MW from Platts db converted to kW
'''

import sys
import os
import pprint

tmp_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir,
    os.pardir)

sys.path.append(tmp_path)
import dblib as db
import read_pahesmf as rp
import basic_dinput_functions as bf
import logging


#components: Name type of power plants you are using

gen_components = [
'rwin',
'rpvo'
    ]

# some manual inputs for testing, will be replaced
presetting_set = 'test_presetting'  # must be the same as selected in scenarios
current_year = 2014
status = 'OPR'

##################################optional:##################################


# Specifies Value, for example 0 for all regions and components

force_value_on = True     # Do you want to set a specific value? ->True
force_value = 0            # Specify your value

#minimal power of a component to be considered
#(default: mw_min = 0.001)

mw_min = 0.001             # mw_min=0.001 is default value and considers all

#optional: want to see sql-command?(default: printsql = False)

printsql = True

#############################################################################
#############################################################################
#############################################################################
#############################################################################
################################program######################################


def create_presetting(scenario_id, overwrite=False,
    epp_scheme='pahesmf_dat',
    table='presetting',
    shape_source='world.gadm_countries',
    pp_data_source='world.plantregister_platts',
    parameter_dc_read_from_file=False):
    '''
    Author: Guido Plessmann
    E-mail: guido.plessmann@ri-institut.de
    Changes by:
    Responsibility:  Guido Plessmann

    This tool creats the presetting for the power plants

    Arguments:
        overwrite: if True current values in db will be overwritten (Warning: if
        no values available for chosen scenario it may lead to an error.
        According to Finn: overwrite equals sql's update)
'''

    # get basic dict for db connection an retrieve parameters of scenario
    basic_dc = rp.read_basic_dc()
    parameter_dc = rp.parameter_from_db(basic_dc, scenario_id)

    # extract regions for easier handling (short calls)
    regions = parameter_dc['energy_system']['energy_system_regions']
    regions_upper = ([r.upper() for r in regions])
    # dict which translates between platts db and pahesmf abbrevations
    from_DB = db.fetch_columns(basic_dc, basic_dc['data_schema'],
    basic_dc['platts_translate'], orderby='id')
    pahesmf = from_DB['pahesmf_fuel_name']
    platt_fuel = from_DB['platt_fuel_name'] #COAL
    platt_fueltype = from_DB['platt_fueltype_name'] #Subliminious
    fuel_to_platt = {}
    counter = -1


    for l in range(len(platt_fuel)): #component abbr of platts db
        counter += 1
        fuel_to_platt[pahesmf[l]] = platt_fuel[l]
    del counter

    # translation dict between pahesmf and platts components abbrevations
    # substitutes fuel_to_platt
    platts_dc = dict(zip(from_DB['pahesmf_fuel_name'],
        from_DB['platt_fuel_name']))

    # write platts names under key "name"
    for k in platts_dc.keys():
        platts_dc[k] = {'name': platts_dc[k]}

    # add fueltype to components in dict
    for comp, ftype in zip(from_DB['pahesmf_fuel_name'],
        from_DB['platt_fueltype_name']):
        if 'fueltype' not in platts_dc[comp].keys():
            platts_dc[comp]['fueltype'] = list()
        platts_dc[comp]['fueltype'].append(ftype)

    # add utype to components in dict
    for comp, utype in zip(from_DB['pahesmf_fuel_name'],
        from_DB['platt_utype_name']):
        if 'utype' not in platts_dc[comp].keys():
            platts_dc[comp]['utype'] = list()
        platts_dc[comp]['utype'].append(utype)

    # make list entries unique
    for comp in platts_dc.keys():
        platts_dc[comp]['fueltype'] = bf.unique_list(platts_dc[comp]
            ['fueltype'])
        platts_dc[comp]['utype'] = bf.unique_list(platts_dc[comp]['utype'])


    # delete entries of not activated components
    pop_list_platts_dc = ([x for x in platts_dc if x not in
        parameter_dc['lists']['all_elec_components']])
    for c in pop_list_platts_dc:
        platts_dc.pop(c)

    # add fields for each component of end of operation year
    #TODO last two tables will become relevant ... later
    irrelevant_tables = ['changed_by', 'description',
    'energy_system_components', 'energy_system_regions',
    'energy_system_resources', 'energy_system_storages',
    'energy_system_storages4biogas', 'energy_system_transformer',
    'energy_system_transformer4chp', 'energy_system_transformer4heat',
    'energy_system_transmission', 'id', 'lastmodified', 'name_set',
    'energy_system_storages4gas', 'energy_system_transformer4gas']
    pprint.pprint(platts_dc)
    # add lifetime for each component
    for table in (bf.remove_from_list(parameter_dc['energy_system'].keys(),
        irrelevant_tables)):
        param_table = table.replace('energy_system', 'parameter')
        for r in regions:
            for comp in parameter_dc['energy_system'][table]:
                if comp in platts_dc.keys():
                    platts_dc[comp]['lifetime'] = (parameter_dc['parameter']
                        [param_table][r][comp]['lifetime'])
                else:
                    logging.warning(comp + ''' is not considered by existing
                        capacities gathering process''')


    print platts_dc


    # looping over all components and regions to get installed capacities
    for c in platts_dc.keys():
        for r in regions:
            # get capacities via country code in platts

            select_from_s = "SELECT mw FROM %s AS p, %s AS g" % (
                    pp_data_source, shape_source)
            where_s = ' where '
            and_s = " and "
            or_s = " or "
            iso_s = "g.iso = '%s'" % r.upper()
            fuel_s = "p.fuel = '%s'" % platts_dc[c]['name']
            fueltype_s = "p.fueltype = '%s'" % str(platts_dc[c]['fueltype'][0])
            fueltype_null_s = "p.fueltype is NULL"
            fueltype_not_null_s = "p.fueltype is NOT NULL"
            mw_min_s = "p.mw >= '%s'" % mw_min
            status_s = "p.status = '%s'" % status
            st_contains_s = "st_contains (g.geom , p.the_geom)"
            print(len(platts_dc[c]['fueltype']))

            if len(platts_dc[c]['fueltype']) == 1:
                db_string = (select_from_s + where_s + iso_s +and_s + fuel_s +
                and_s + fueltype_s + and_s + st_contains_s + ';')
            elif len(platts_dc[c]['fueltype']) > 1:
                fueltypes = "(" + platts_dc[c]['fueltype'][0]
                for f in platts_dc[c]['fueltype']:
                    fueltypes = (fueltypes + or_s +
                        str(platts_dc[c]['fueltype'][1:]))
                    fueltypes = fueltypes + ';'
            elif platts_dc[c]['fueltype'] is None:
                print('Fueltype is None by component: ', c)

            print(db_string)
            #db_return = db.execute_read_db(basic_dc, db_string)
            #print(c, r, len(db_return), type(db_return))
            #if c in ['rpvo', 'wind']:
                #print(db_return)


            ## get capacities via st_contains and gadm country/ region shape
                        #execute_string = 'SELECT mw FROM ' \
                        #+ str(pp_data_source) + ' AS p, ' \
                        #+ str(shape_source) + ' AS g ' \
                        #+ ' WHERE  st_contains (g.geom , p.the_geom)' \
                        #+ " AND g.iso = '" + str(R) \
                        #+ "' AND p.fuel = '" + str(pahesmf2platt[t].keys()[0]) \
                        #+ "' AND p.fueltype is NULL"  \
                        #+ " AND p.mw >= " + str(mw_min) \
                        #+ " AND p.status = 'OPR'"

    #TODO Check for Power Plants which no data of operation started



    #fuel to fueltype #only unique values
    platt_fuel_small = list(set(platt_fuel))


    #pahesmf #only unique values
    pahesmf_fuel_small = list(set(pahesmf))

    #pahesmf #only unique values
    platt_fueltype_small = list(set(platt_fueltype))


    pahesmf2platt= {}
    fuel_to_fueltype= {}
    for p in pahesmf_fuel_small:
        pahesmf2platt[p] = {}
        for f in platt_fuel_small:
            counter = 0
            for i in range(len(platt_fuel)):
                if platt_fuel[i] == f and pahesmf[i] == p and counter == 0:
                    fuel_to_fueltype[f] = []
                    pahesmf2platt[p][f] = []
                if platt_fuel[i] == f and pahesmf[i] == p:
                    fuel_to_fueltype[f].append(platt_fueltype[i])
                    counter +=1
                    try:
                        pahesmf2platt[p][f] = fuel_to_fueltype[f]
                    except:
                        pass
    #pprint.pprint(pahesmf2platt)




    #######################checks if all components are in fuel to platt########

    for c in gen_components:
        if not c in fuel_to_platt:
            logging.error(c + " not defined in DB fuel2platt, please add " +
            c + " in pahesmf_sim.presetting_fuel2platt in DB Reiners_db")

    if 'tccg' in gen_components:
        exception_distinguish_utype('tccg') #jump into exception where
        gen_components.remove('tccg')



    counter = 0
    conn = db.connect2db(basic_dc)
    cur = conn.cursor()
    execute_string = ""
    insert_string = ""

    for t in gen_components:
        #runs through every fueltype
            for r in regions_upper:
                all_fueltypes_summed_up = 0
                  # check if values in DB
                in_string = "region = '" + r + "' AND " \
                + "component = '" + t + "' AND " + "presetting_set = '" \
                + presetting_set + "'"  # string for where-conditions

                presetting_existing = db.fetch_columns(basic_dc, epp_scheme,
                table, columns='presetted_summed_power',

                where_string=in_string, unique=True)


                if presetting_existing['presetted_summed_power'] == [] \
                or overwrite:
                    counter += 1
                    R = r
                    counter2 = -1
                    sumstring = []
                    fueltypes = pahesmf2platt[t][fuel_to_platt[t]]
                    print(fueltypes)

                    if not fueltypes[0] and len(fueltypes) == 1: #NULL for fueltype
                        execute_string = 'SELECT SUM(mw) FROM ' \
                        + str(pp_data_source) + ' AS p, ' \
                        + str(shape_source) + ' AS g ' \
                        + ' WHERE  st_contains (g.geom , p.the_geom)' \
                        + " AND g.iso = '" + str(R) \
                        + "' AND p.fuel = '" + str(pahesmf2platt[t].keys()[0]) \
                        + "' AND p.fueltype is NULL"  \
                        + " AND p.mw >= " + str(mw_min) \
                        + " AND p.status = 'OPR'"
                        # String which sums up the power in regions

                    elif fueltypes: # not NULL for fueltype
                        for fueltypes in pahesmf2platt[t][fuel_to_platt[t]]: # for different fueltypes this block
                            execute_string = 'SELECT SUM(mw) FROM ' \
                            + str(pp_data_source) + ' AS p, ' \
                            + str(shape_source) + ' AS g ' \
                            + ' WHERE  st_contains (g.geom , p.the_geom)' \
                            + " AND g.iso = '" + str(R) \
                            + "' AND p.fuel = '" + str(pahesmf2platt[t].keys()[0]) \
                            + "' AND p.fueltype = '" + str(fueltypes) \
                            + "' AND p.mw >= " + str(mw_min) \
                            + " AND p.status = 'OPR'"
                            # String which sums up the power in regions
                            if "None" in execute_string:
                                execute_string = execute_string.replace("= 'None'", "is NULL")


                            sumstring.append(execute_string)
                            counter2 += 1

                    DB_sum= []
                    if sumstring:
                        for s in range(len(sumstring)):
                            cur.execute(sumstring[s])
                            try:
                                DB_sum.append(float(cur.fetchone()[0]))
                            except:
                                DB_sum.append(None)
                        DB_summed_up = 0
                        for d in DB_sum:
                            if d:
                                DB_summed_up += d

                        all_fueltypes_summed_up += DB_summed_up
                        #intern calculation of sum of fueltypes for 1 fuel


                if all_fueltypes_summed_up > 0:
                    execute_string = all_fueltypes_summed_up
                    #will write the intern calculated sum of fueltypes instead
                    #of a sum function for DB
                if not execute_string:
                    break
                if not overwrite:
                    insert_string = insert_string + "; " + 'INSERT INTO ' \
                    + str(epp_scheme) + "." + str(table)\
                    + " (presetting_set, component, " \
                    + " region, presetted_summed_power) Values ('" \
                    + str(presetting_set) + "', '" \
                    + str(t) + "', '" \
                    + str(r) + "', " \
                    + "(" + str(execute_string) + ")*1000" + " )"

                if overwrite:
                    insert_string = (insert_string + "; " + 'Update '
                    + str(epp_scheme) + "." + str(table)
                    + " SET presetted_summed_power = (" + str(execute_string)
                    + ") Where "
                        + "region = '" + r + "' AND "
                        + "component = '" + t + "' AND " + "presetting_set = '"
                        + presetting_set + "'")

                logging.info('writing presetting of ' + str(r) + " " + str(t) +
                ' in ' + str(epp_scheme) + "." + str(table))

    logging.info('will insert ' + str(counter) + " presettings")
    if printsql:
        print(insert_string)

    if insert_string:
        pass
        cur.execute(insert_string)
    elif not insert_string:
        logging.info('all given components in given reagions already defined')
    conn.commit()

    cur.close()
    conn.close()


def force_value_fkt():
    counter = 0
    conn = db.connect2db(basic_dc)
    cur = conn.cursor()
    #execute_string = ""
    insert_string = ""
    for t in gen_components:
        for r in regions_upper:
              # check if values in DB
            in_string = "region = '" + r + "' AND " \
            + "component = '" + t + "' AND " + "presetting_set = '" \
            + presetting_set + "'"  # string for where-conditions

            presetting_existing = db.fetch_columns(basic_dc, epp_scheme,
            table, columns='presetted_summed_power',
            where_string=in_string, unique=True)

            if presetting_existing['presetted_summed_power'] == [] \
            or overwrite:
                counter += 1

                #execute_stri