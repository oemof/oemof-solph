#!/usr/bin/python
# -*- coding: utf-8

import time
import use_case
import database as db
import checks
import os
import logging


def main_func(parameter_set, main_dc=None):
    'Main function.'
    # import the parameter set
    parameter_set = __import__(parameter_set)

    begin = time.time()

    p_set = parameter_set.get_p_set()

    # Szeanrio calculation
    if p_set['szenario'] == 'capacity variation':

        print (("Starte Szenario um %r" % time.strftime("%H:%M:%S")))

        # Retrieve parameterset from database
        input_data = {}
        input_data = db.get_input_data(p_set['project_id'][0])

        # Get hourly loads and renewable potential
        [hourly_heat_demand, hourly_el_demand,
            hourly_biogas_potential, annual_biomass_potential,
            hourly_pv_pot, hourly_wind_pot,
            number_wka, pv_area, hourly_st_potential, st_area] = \
            use_case.get_profiles(p_set, input_data)

        print (("Last- und Potenzialzeitreihen fertiggestellt um %r"
            % time.strftime("%H:%M:%S")))

        # PRECEDING CHECKS
        checks.evaluate(input_data, hourly_heat_demand,
            annual_biomass_potential, hourly_biogas_potential)

        # capacity variation
        for i in range(len(p_set['cap_pv'])):

            # write i to p_set
            p_set['index'] = i

            # get hourly wind potential if different wind turbines
            # need to be considered
            if p_set['wind_pot'] == 'scaled_mixed':
                import wka
                hourly_wind_pot, number_wka = wka.get_hourly_wind_pot(
                input_data, p_set, p_set['wind_pot'],
                p_set['wind_pot_use_case'], save=p_set['save'],
                schema=p_set['schema'], save_to_table=p_set['load_pot_table'])

            # capacity variation
            use_case.cap_variation(input_data, p_set,
                hourly_heat_demand, hourly_el_demand,
                hourly_biogas_potential, annual_biomass_potential,
                hourly_pv_pot, hourly_wind_pot, number_wka, pv_area,
                p_set['cap_pv'][i], p_set['cap_wind'][i],
                hourly_st_potential, st_area, begin)

            p_set['counter'] += 1
            p_set['output_dir'] = (p_set['output_dir_path'] + 'ID_' +
                str(p_set['project_id'][0]) + '_' + str(p_set['counter']) +
                '_(' + p_set['date']) + ')'

    elif p_set['szenario'] == 'pahesmf':

        # get dicts from pahesmf
        logging.info('Starting reegis...')
        # Retrieve parameter set from database
        input_data = db.get_input_data(p_set['reegis_id'][0],
            db_table='wittenberg.parameterset_pahesmf')

        # Adds the pahesmf_dc to the reegis p_set dictionary.
        p_set.update(main_dc)

        p_set['DH systems'] = {'Gas': 0.22, 'Gas Cog unit': 0.78}
        input_data['Heat source ST Heat'] = 'no'
        input_data['Cog source DH Biogas Cog unit'] = 'no'
        input_data['Heat source Biogas Cog unit'] = 'no'

        r0 = list(main_dc['parameter']['component'].keys())[0]
        resources_ls = []
        for c in list(main_dc['parameter']['component'][r0].keys()):
            if main_dc['parameter']['component'][r0][c]['type'] == (
                    'transformer'):
                resources_ls.append(
                    main_dc['parameter']['component'][r0][c]['resources'])

        # Get hourly loads and renewable potential
        incl_pv = None
        if 'rpvo' in list(main_dc['parameter']['component'][r0].keys()):
            incl_pv = 'yes'
        incl_wind = None
        if 'rwin' in list(main_dc['parameter']['component'][r0].keys()):
            incl_wind = 'yes'
        incl_biogas = None
        if 'rbig' in resources_ls:
            incl_biogas = 'yes'
        incl_biomass = None
        if 'rbma' in resources_ls:
            incl_biomass = 'yes'
        ####### vorläufig!! - 4code character ?? #######
        incl_st = None
        if 'rst' in resources_ls:
            incl_st = 'yes'

        [hourly_heat_demand, hourly_el_demand,
            hourly_biogas_potential, annual_biomass_potential,
            hourly_pv_potential, hourly_wind_potential,
            number_wka, pv_area, hourly_st_potential, st_area] = \
            use_case.get_profiles(p_set, input_data,
                incl_wind=incl_wind, incl_pv=incl_pv, incl_biogas=incl_biogas,
                incl_biomass=incl_biomass, incl_st=incl_st, pahesmf='yes')

    else:
        print (('Das Szenario %s gibt es noch nicht.' % p_set['szenario']))

    minuten = int((time.time() - begin) / 60)
    sekunden = time.time() - begin - minuten * 60
    logging.info("Gesamtzeit reegis: %d:%d Minuten" % (minuten, sekunden))


def check_git_branch():
    '''
    Passes the used brance and commit to the logger
    '''
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '.git')

    # Reads the name of the branch
    f_branch = os.path.join(path, 'HEAD')
    f = open(f_branch, "r")
    first_line = f.readlines(1)
    name_full = first_line[0].replace("\n", "")
    name_branch = name_full.replace("ref: refs/heads/", "")
    f.close()

    # Reads the code of the last commit used
    f_commit = os.path.join(path, 'refs', 'heads', name_branch)
    f = open(f_commit, "r")
    last_commit = f.read(8)
    f.close()

    logging.info("Used reegis version: {0} @ {1}".format(
        last_commit, name_branch))


#main_func('parameter_set')

if __name__ == "__main__":
    import sys
    main_func(sys.argv[1])