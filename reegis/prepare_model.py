#!/usr/bin/python
# -*- coding: utf-8

import numpy as np


def lists(input_data):
    '''
    Prepares lists for usage in model.
    '''
    # list creation
    power = []
    battery = []
      # gas
    heat_gas = []
    el_heating_gas = []
    ts_gas = []
      # oil
    heat_oil = []
    el_heating_oil = []
    ts_oil = []
      # biomass
    heat_biomass = []
    el_heating_biomass = []
    ts_biomass = []
      # coal
    heat_coal = []
    el_heating_coal = []
    ts_coal = []
      # DH
    heat_DH = []
    ts_DH = []
    el_heating_DH = []
    cogeneration_DH = []
      # Storages
    storages = []
    storages_bio = []
    storages_vars = []
    biogas_sinks = []
    dec_biogas_sinks = []
    biomass_sinks = []
      # Heat Pump
    heat_hpm_air = []
    ts_hpm_air_heating = []
    ts_hpm_air_ww = []
    el_heating_hpm_air_heating = []
    el_heating_hpm_air_ww = []
    heat_hpm_brine = []
    ts_hpm_brine_heating = []
    ts_hpm_brine_ww = []
      # dec. Cog units
    dec_cog_units = []
    dec_cog_units_boiler = []
    dec_cog_units_excess = []
      # Solarthermal energy
    heat_st = []
    heat_st_supp_gas = []  # supplementary gas boiler
    el_heating_st = []
    ts_st = []

    # implemented system components
    choice_power_sources = ['Wind', 'PV', 'Hydropower', 'Biomass Power',
        'Gas Power']
    choice_heat_sources_DH = ['DH Biogas Heat', 'DH Gas Heat', 'DH Excess Heat']
    choice_cogeneration_DH = ['DH Biogas Cog unit', 'DH Gas Cog unit',
        'DH Biomass Cog']
    choice_biogas = ['DH Biogas Heat', 'DH Biogas Cog unit Power']
    choice_biomass = ['Biomass Power', 'DH Biomass Cog Power', 'Biomass Heat']
    choice_dec_cog_units = ['Gas Cog unit', 'Biogas Cog unit']

    # Power source list
    for i in choice_power_sources:
        if input_data['Power source ' + i] == 'yes':
            power.append(i)
    power.append('El Import')

    # Heat source list DH
    for i in choice_heat_sources_DH:
        if input_data['Heat source ' + i] == 'yes':
            heat_DH.append(i)

    # Heat source list dec. Cog units
    for i in choice_dec_cog_units:
        if input_data['Heat source ' + i] == 'yes':
            dec_cog_units.append(i)

    # Heat source list gas
    if input_data['Heat source Gas Heat'] == 'yes':
        heat_gas.append('Gas Heat')

    # Heat source list oil
    if input_data['Heat source Oil Heat'] == 'yes':
        heat_oil.append('Oil Heat')

    # Heat source list biomass
    if input_data['Heat source Biomass Heat'] == 'yes':
        heat_biomass.append('Biomass Heat')

    # Heat source list solarthermal energy
    if input_data['Heat source ST Heat'] == 'yes':
        heat_st.append('ST Heat')
        heat_st_supp_gas.append('ST Heat supp Gas')

    # Heat source list coal
    if input_data['Heat source Coal Heat'] == 'yes':
        heat_coal.append('Coal Heat')

    # Cogeneration source list DH
    for i in choice_cogeneration_DH:
        if input_data['Cog source ' + i] == 'yes':
            cogeneration_DH.append(i)

    # Heat source Heat Pump
    if input_data['Heat source HP Mono Air'] == 'yes':
        heat_hpm_air.append('HP Mono Air Heating')
        el_heating_hpm_air_heating.append('HP Mono Air Heating el Heating')
        heat_hpm_air.append('HP Mono Air WW')
        el_heating_hpm_air_ww.append('HP Mono Air WW el Heating')
    if input_data['Heat source HP Mono Brine'] == 'yes':
        heat_hpm_brine.append('HP Mono Brine Heating')
        heat_hpm_brine.append('HP Mono Brine WW')

    # el Heating
    if input_data['Heat source DH el Heating'] == 'yes':
        el_heating_DH.append('DH el Heating')
    if input_data['Heat source Gas el Heating'] == 'yes':
        el_heating_gas.append('Gas el Heating')
    if input_data['Heat source Oil el Heating'] == 'yes':
        el_heating_oil.append('Oil el Heating')
    if input_data['Heat source Biomass el Heating'] == 'yes':
        el_heating_biomass.append('Biomass el Heating')
    if input_data['Heat source ST el Heating'] == 'yes':
        el_heating_st.append('ST el Heating')
    if input_data['Heat source Coal el Heating'] == 'yes':
        el_heating_coal.append('Coal el Heating')
    el_heating = (el_heating_hpm_air_heating + el_heating_hpm_air_ww +
        el_heating_DH + el_heating_gas + el_heating_oil + el_heating_biomass +
        el_heating_coal + el_heating_st)

    # dec. Cog units components
    for i in dec_cog_units:
        if input_data['Heat source ' + i + ' el Heating'] == 'yes':
            el_heating.append(i + ' el Heating')
        if input_data['Heat source ' + i + ' Boiler'] == 'yes':
            dec_cog_units_boiler.append(i + ' Boiler')
        if i == 'Biogas Cog unit':
            dec_cog_units_excess.append('Biogas Cog unit Excess Heat')
            dec_cog_units_excess.append('Biogas Cog unit Heat Demand')
        if input_data[i + ' Storage Thermal'] == 'yes':
            storages.append(i + ' Storage Thermal')
            storages_vars.append(i + ' Storage Thermal Charge')
            storages_vars.append(i + ' Storage Thermal Discharge')
            storages_vars.append(i + ' Storage Thermal SoC')

    # Battery Storage
    if input_data['Storage Battery'] == 'yes':
        battery.append('Storage Battery')
        storages_vars.append('Storage Battery Charge')
        storages_vars.append('Storage Battery Discharge')
        storages_vars.append('Storage Battery SoC')

    # Thermal Storage DH
    if input_data['DH Storage Thermal'] == 'yes':
        ts_DH.append('DH Storage Thermal')
        storages.append('DH Storage Thermal')
        storages_vars.append('DH Storage Thermal Charge')
        storages_vars.append('DH Storage Thermal Discharge')
        storages_vars.append('DH Storage Thermal SoC')
        heat_DH.append('DH Thermal Storage Boiler')
        if input_data['fuel DH Thermal Storage Boiler'] == 'Biogas':
            choice_biogas.append('DH Thermal Storage Boiler')

    # Thermal Storage Gas
    if input_data['Gas Storage Thermal'] == 'yes':
        ts_gas.append('Gas Storage Thermal')
        storages.append('Gas Storage Thermal')
        storages_vars.append('Gas Storage Thermal Charge')
        storages_vars.append('Gas Storage Thermal Discharge')
        storages_vars.append('Gas Storage Thermal SoC')

    # Thermal Storage Oil
    if input_data['Oil Storage Thermal'] == 'yes':
        ts_oil.append('Oil Storage Thermal')
        storages.append('Oil Storage Thermal')
        storages_vars.append('Oil Storage Thermal Charge')
        storages_vars.append('Oil Storage Thermal Discharge')
        storages_vars.append('Oil Storage Thermal SoC')

    # Thermal Storage Biomass
    if input_data['Biomass Storage Thermal'] == 'yes':
        ts_biomass.append('Biomass Storage Thermal')
        storages.append('Biomass Storage Thermal')
        storages_vars.append('Biomass Storage Thermal Charge')
        storages_vars.append('Biomass Storage Thermal Discharge')
        storages_vars.append('Biomass Storage Thermal SoC')

    # Thermal Storage ST
    if input_data['Heat source ST Heat'] == 'yes':
        ts_st.append('ST Storage Thermal')
        storages.append('ST Storage Thermal')
        storages_vars.append('ST Storage Thermal Charge')
        storages_vars.append('ST Storage Thermal Discharge')
        storages_vars.append('ST Storage Thermal SoC')

    # Thermal Storage Coal
    if input_data['Coal Storage Thermal'] == 'yes':
        ts_coal.append('Coal Storage Thermal')
        storages.append('Coal Storage Thermal')
        storages_vars.append('Coal Storage Thermal Charge')
        storages_vars.append('Coal Storage Thermal Discharge')
        storages_vars.append('Coal Storage Thermal SoC')

    # Thermal Storage Heat Pump Mono Air (Heating + WW)
    if input_data['HP Mono Air Heating Storage Thermal'] == 'yes':
        ts_hpm_air_heating.append('HP Mono Air Heating Storage Thermal')
        storages.append('HP Mono Air Heating Storage Thermal')
        storages_vars.append('HP Mono Air Heating Storage Thermal Charge')
        storages_vars.append('HP Mono Air Heating Storage Thermal Discharge')
        storages_vars.append('HP Mono Air Heating Storage Thermal SoC')
    if input_data['HP Mono Air WW Storage Thermal'] == 'yes':
        ts_hpm_air_ww.append('HP Mono Air WW Storage Thermal')
        storages.append('HP Mono Air WW Storage Thermal')
        storages_vars.append('HP Mono Air WW Storage Thermal Charge')
        storages_vars.append('HP Mono Air WW Storage Thermal Discharge')
        storages_vars.append('HP Mono Air WW Storage Thermal SoC')

    # Thermal Storage Heat Pump Mono Brine (Heating + WW)
    if input_data['HP Mono Brine Heating Storage Thermal'] == 'yes':
        ts_hpm_brine_heating.append('HP Mono Brine Heating Storage Thermal')
        storages.append('HP Mono Brine Heating Storage Thermal')
        storages_vars.append('HP Mono Brine Heating Storage Thermal Charge')
        storages_vars.append('HP Mono Brine Heating Storage Thermal Discharge')
        storages_vars.append('HP Mono Brine Heating Storage Thermal SoC')
    if input_data['HP Mono Brine WW Storage Thermal'] == 'yes':
        ts_hpm_brine_ww.append('HP Mono Brine WW Storage Thermal')
        storages.append('HP Mono Brine WW Storage Thermal')
        storages_vars.append('HP Mono Brine WW Storage Thermal Charge')
        storages_vars.append('HP Mono Brine WW Storage Thermal Discharge')
        storages_vars.append('HP Mono Brine WW Storage Thermal SoC')

    hp_ts_dict = {'HP Mono Air Heating': ts_hpm_air_heating,
                  'HP Mono Air WW': ts_hpm_air_ww,
                  'HP Mono Brine Heating': ts_hpm_brine_heating,
                  'HP Mono Brine WW': ts_hpm_brine_ww}

    # Biomass Storage
    if 'DH Biomass Cog' in cogeneration_DH or 'Biomass Power' in power or \
    'Biomass Heat' in heat_biomass:
        storages_bio.append('Storage Biomass')
        storages_vars.append('Storage Biomass Charge')
        storages_vars.append('Storage Biomass Discharge')
        storages_vars.append('Storage Biomass SoC')
    # Biomass sinks
    for i in choice_biomass:
        if i in (power + heat_biomass +
        [j + ' Power' for j in cogeneration_DH]):
            biomass_sinks.append(i)

    # Biogas Storage (central)
    if 'DH Biogas Cog unit' in cogeneration_DH or 'DH Biogas Heat' in heat_DH:
        storages_bio.append('Storage Biogas')
        storages_vars.append('Storage Biogas Charge')
        storages_vars.append('Storage Biogas Discharge')
        storages_vars.append('Storage Biogas SoC')
    # Biogas sinks (central)
    for i in choice_biogas:
        if i in (heat_DH + [j + ' Power' for j in cogeneration_DH]):
            biogas_sinks.append(i)

    # Biogas Storage (decentral)
    if 'Biogas Cog unit' in dec_cog_units:
        storages_bio.append('Storage Biogas dec')
        storages_vars.append('Storage Biogas dec Charge')
        storages_vars.append('Storage Biogas dec Discharge')
        storages_vars.append('Storage Biogas dec SoC')
        dec_biogas_sinks.append('Biogas Cog unit Power')

    return (heat_gas, el_heating_gas, ts_gas, heat_oil, el_heating_oil, ts_oil,
        heat_biomass, el_heating_biomass, ts_biomass,
        heat_coal, el_heating_coal, ts_coal,
        heat_DH, el_heating_DH, ts_DH, cogeneration_DH,
        power, storages, storages_bio, storages_vars, battery,
        dec_biogas_sinks, biogas_sinks, biomass_sinks,
        heat_hpm_air, ts_hpm_air_heating, ts_hpm_air_ww,
        el_heating_hpm_air_heating, el_heating_hpm_air_ww, heat_hpm_brine,
        ts_hpm_brine_heating, ts_hpm_brine_ww, hp_ts_dict, el_heating,
        dec_cog_units, dec_cog_units_boiler, dec_cog_units_excess,
        heat_st, heat_st_supp_gas, el_heating_st, ts_st)


def variables_list(power, heat_gas, heat_oil, heat_biomass,
    heat_st, heat_st_supp_gas, heat_coal,
    heat_DH, cogeneration_DH, el_heating, storages_vars,
    heat_hpm_air, heat_hpm_brine, dec_cog_units, dec_cog_units_boiler,
    dec_cog_units_excess):
    '''
    Prepares a list with all model variables for the lp_variables definition.
    '''
    variables = (power + heat_gas + heat_oil + heat_biomass +
        heat_st + heat_st_supp_gas + heat_coal +
        heat_DH + el_heating + storages_vars + heat_hpm_air + heat_hpm_brine +
        dec_cog_units_boiler + dec_cog_units_excess +
        [i + ' Power' for i in (cogeneration_DH + dec_cog_units)] +
        [i + ' Heat' for i in (cogeneration_DH + dec_cog_units)])
    return variables


def efficiency_dict(input_data, power, heat_gas, heat_oil, heat_biomass,
    heat_coal, heat_DH, heat_st, heat_st_supp_gas, cogeneration_DH,
    dec_cog_units, dec_cog_units_boiler):
    '''
    Prepares a dictionary with efficiencies of all power plants to be considered
    in the model (except heat pumps).
    '''

    efficiency_dict = {}
    for i in power:
        if i == 'Wind' or i == 'PV' or i == 'Hydropower' or i == 'El Import':
            efficiency_dict[i] = 1
        else:
            efficiency_dict[i] = input_data['eta ' + i]
    for i in heat_st:
        efficiency_dict[i] = 1
    for i in heat_DH:
        if i == 'DH Excess Heat':
            efficiency_dict[i] = 1
        else:
            efficiency_dict[i] = input_data['eta ' + i]
    for i in (heat_gas + heat_oil + heat_biomass + heat_coal +
        heat_st_supp_gas + dec_cog_units_boiler):
        efficiency_dict[i] = input_data['eta ' + i]
    for i in (cogeneration_DH + dec_cog_units):
        efficiency_dict[i + ' Heat'] = input_data['eta ' + i + ' Heat']
        efficiency_dict[i + ' Power'] = input_data['eta ' + i + ' Power']

    return efficiency_dict


def capacity_dict(input_data,
    power, heat_gas, heat_oil, heat_biomass, heat_st, heat_st_supp_gas,
    heat_coal, heat_DH, el_heating, cogeneration_DH, storages, battery,
    storages_bio, hoy, hourly_wind_pot, hourly_pv_pot, hourly_st_pot,
    hourly_hydro_pot, efficiency, heat_hpm_air, heat_hpm_brine,
    annual_biomass_pot, hourly_biogas_pot, dec_cog_units, dec_cog_units_boiler,
    hourly_heat_demand):
    '''
    Prepares a dictionary with all power plant and storage capacities.
    '''
    ones = np.ones((hoy, ))
    capacity_dict = {}
    for i in power:
        if i == 'Wind':
            capacity_dict[i] = hourly_wind_pot
        elif i == 'PV':
            capacity_dict[i] = hourly_pv_pot
        elif i == 'Hydropower':
            capacity_dict[i] = ones * hourly_hydro_pot
        elif i == 'El Import':
            capacity_dict[i] = ones * 9999
        else:
            capacity_dict[i] = ones * input_data['cap ' + i]
    for i in heat_st:
        capacity_dict[i] = hourly_st_pot
    for i in (heat_gas + heat_oil + heat_biomass + heat_coal + heat_DH +
        heat_hpm_air + heat_hpm_brine + dec_cog_units_boiler +
        heat_st_supp_gas):
            capacity_dict[i] = ones * input_data['cap ' + i]
    for i in (cogeneration_DH + dec_cog_units):
        if i == 'DH Biomass Cog':
            if 'Biomass Power' in power:
                capacity_dict[i + ' Power'] = ones * (input_data[
                    'cap Biomass Power'] / efficiency['Biomass Power'] *
                    efficiency['DH Biomass Cog Power'])
            else:
                capacity_dict[i + ' Power'] = ones * input_data[
                    'cap ' + i + ' Power']
        else:
            capacity_dict[i + ' Power'] = ones * input_data[
                'cap ' + i + ' Power']
    for i in (storages + battery + storages_bio):
        if i == 'Storage Biomass':
            input_data['cap ' + i] = ones * annual_biomass_pot
        elif i == 'Storage Biogas' or i == 'Storage Biogas dec':
            pot_dict = {'Storage Biogas': hourly_biogas_pot['central'],
                        'Storage Biogas dec': hourly_biogas_pot['dec']}
            input_data['cap ' + i] = input_data['Storage time Biogas'] * \
                pot_dict[i]
        capacity_dict[i] = ones * input_data['cap ' + i]

    tmp_list = ['Gas', 'Oil', 'Biomass', 'Coal', 'ST', 'Gas Cog unit',
        'Biogas Cog unit']
    for i in el_heating:
        if i.replace(' el Heating', '') in tmp_list:
            capacity_dict[i] = (input_data['cap ' + i] /
                max(hourly_heat_demand[i.replace(' el Heating', '')]) *
                hourly_heat_demand[i.replace(' el Heating', '')])
        else:
            capacity_dict[i] = ones * input_data['cap ' + i]

    return capacity_dict


def discharge_rate_dict(input_data, storages, battery, hoy, hourly_heat_demand):
    '''
    Prepares a dictionary with storage discharge rates.
    '''
    ones = np.ones((hoy, ))
    discharge_rate_dict = {}

    for i in storages:
        discharge_rate_dict[i] = (input_data['Discharge rate ' + i] /
            max(hourly_heat_demand[i.replace(' Storage Thermal', '')]) *
            hourly_heat_demand[i.replace(' Storage Thermal', '')])

    for i in battery:
        discharge_rate_dict[i] = ones * input_data['Discharge rate ' + i]
    return discharge_rate_dict


def soc_loss_dict(input_data, storages, battery, hoy):
    '''
    Prepares a dictionary with storage losses in one hour in relation to the
    SoC.
    '''
    ones = np.ones((hoy, ))
    soc_loss_dict = {}
    for i in battery:
        soc_loss_dict[i] = ones * input_data['Loss ' + i]
    for i in storages:
        if i == 'DH Storage Thermal':
            soc_loss_dict[i] = ones * input_data['Loss ' + i]
        else:
            soc_loss_dict[i] = \
                ones * input_data['Loss Storage Thermal Building']
    return soc_loss_dict


def discharge_loss_dict(input_data, storages, hoy):
    '''
    Prepares a dictionary with discharge losses.
    '''
    ones = np.ones((hoy, ))
    discharge_loss_dict = {'Gas Storage Thermal': ones * 0.0003,
                           'Oil Storage Thermal': ones * 0.0003,
                           'Biomass Storage Thermal': ones * 0.0003,
                           'ST Storage Thermal': ones * 0.0003,
                           'Coal Storage Thermal': ones * 0.0003,
                           'HP Mono Air Heating Storage Thermal':
                               ones * 0.0003,
                           'HP Mono Air WW Storage Thermal': ones * 0.0003,
                           'HP Mono Brine Heating Storage Thermal':
                               ones * 0.0003,
                           'HP Mono Brine WW Storage Thermal': ones * 0.0003,
                           'Gas Cog unit Storage Thermal': ones * 0.0003,
                           'Biogas Cog unit Storage Thermal': ones * 0.0003}
    if 'DH Storage Thermal' in storages:
        discharge_loss_dict['DH Storage Thermal'] = \
            ones * input_data['Discharge loss DH Storage Thermal']
    return discharge_loss_dict