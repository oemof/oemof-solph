#!/usr/bin/python
# -*- coding: utf-8

import time
import use_case
import database as db
import checks


def main_func(parameter_set):

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
            p_set['output_dir'] = (p_set['output_dir_tmp'] +
                str(p_set['counter']))

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

    elif p_set['szenario'] == 'pahesmf':

        import paheegis

        # get dicts from pahesmf
        basic_dc, pahesmf_dc = paheegis.get_all_dicts(p_set['pahesmf_scenario'])

        # Retrieve parameter set from database
        input_data = db.get_input_data(p_set['reegis_id'][0],
            db_table='wittenberg.parameterset_pahesmf')

        # Get hourly loads and renewable potential
        incl_pv = None
        if 'rpvo' in pahesmf_dc['energy_system']['energy_system_re']:
            incl_pv = 'yes'
        incl_wind = None
        if 'rwin' in pahesmf_dc['energy_system']['energy_system_re']:
            incl_wind = 'yes'
        incl_biogas = None
        if 'rbig' in pahesmf_dc['energy_system']['energy_system_resources']:
            incl_biogas = 'yes'
        incl_biomass = None
        if 'rbma' in pahesmf_dc['energy_system']['energy_system_resources']:
            incl_biomass = 'yes'
        ####### vorläufig!! - 4code character ?? #######
        incl_st = None
        if 'rst' in pahesmf_dc['energy_system']['energy_system_resources']:
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
    print (("Gesamtzeit: %d:%d Minuten" % (minuten, sekunden)))

    return


if __name__ == "__main__":
    import sys
    main_func(sys.argv[1])