#!/usr/bin/python
# -*- coding: utf-8

from math import log
import numpy as np
import database as db
import co2_emissions as co2


def lifetime_of_component(cur, component):
    '''
    Retrieves the lifetime used in the calculation of the total costs due
    to the construction of the chosen energy system component.
    '''
    cur.execute('''
        select "Lifetime"
        from wittenberg.costs
        where "Energy system comp" = %(str)s
    ''', {'str': component})
    component_lifetime = cur.fetchone()
    return component_lifetime[0]


def opex_var(cur, fuel):
    '''
    Returns the variable OPEX in €/kWh including costs for fuel, transport and
    variable costs.
    '''
    cur.execute('''
        select "Costs"
        from wittenberg.costs_variable
        where "Fuel" = %(str)s
    ''', {'str': fuel})
    opex = np.asarray(cur.fetchone())
    return opex


def calc_annuity_f(cur, component):
    '''
    Returns the interest rate, credit period and grace period
    of the loan and calculates the annuity factor.
    '''
    cur.execute('''
        select "Interest rate", "Credit period", "Grace period"
        from wittenberg.costs
        where "Energy system comp" = %(component)s
    ''', {'component': component})
    data = np.asarray(cur.fetchall())
    interest_rate = data[0][0]
    credit_period = data[0][1]
    grace_period = data[0][2]

    annuity_f = (((1 + interest_rate) ** (credit_period - grace_period) *
        interest_rate) / ((1 + interest_rate) ** (credit_period - grace_period)
        - 1))

    return annuity_f, interest_rate, credit_period, grace_period


def get_fixed_costs(cur, component):
    '''
    Returns the CAPEX in €/kW*lifetime and the OPEX in €/kW*a.
    '''
    cur.execute('''
        select "Capex", "Opex fixed"
        from wittenberg.costs
        where "Energy system comp" = %(component)s
    ''', {'component': component})
    data = np.asarray(cur.fetchall())
    capex = data[0][0]
    opex_fixed = data[0][1]
    return capex, opex_fixed


def costs_annual(cur, component, cap):
    '''
    Returns the total annual fixed costs for the installed capacity of the
    component in €/a.
    '''
    # get lifetime
    lifetime = lifetime_of_component(cur, component)
    # get annuity factor, interest rate, credit period, grace period
    annuity_f, interest_rate, credit_period, grace_period = calc_annuity_f(
        cur, component)
    # get capex and opex fixed
    capex, opex_fixed = get_fixed_costs(cur, component)

    # the total fixed costs per lifetime and kW are calculated
    costs_lifetime = lifetime * opex_fixed + annuity_f * capex * (
        credit_period - grace_period) + interest_rate * grace_period * capex

    # the total fixed costs per year and installed capacity are calculated
    annual_costs = cap * costs_lifetime / lifetime

    return annual_costs


def costs_annual_regression(cur, component, cap, unit_cap=0.1, T_hot=90,
    T_cold=60):
    '''
    Returns the total annual fixed costs for the installed capacity of the
    component in €/a using a regression for capacities between a minimal and
    maximal capacity.
    '''
    # get lifetime
    lifetime = lifetime_of_component(cur, component)
    # get annuity factor, interest rate, credit period, grace period
    annuity_f, interest_rate, credit_period, grace_period = calc_annuity_f(
        cur, component)
    # get capex and opex fixed
    capex_false, opex_fixed = get_fixed_costs(cur, component)

    # retrieve regression parameters from database
    cur.execute('''
        select "Parameter 1", "Parameter 2", "min Cap", "max Cap"
        from wittenberg.cost_regression_parameters
        where "Energy system comp" = %(str)s
    ''', {'str': component})
    parameters = np.asarray(cur.fetchall())
    parameter_1 = parameters[0][0]
    parameter_2 = parameters[0][1]
    min_cap = parameters[0][2]
    max_cap = parameters[0][3]

    if component == 'DH Cogeneration unit gas' or \
    component == 'DH Cogeneration unit biogas':
        cap_list = co2.cap_cog_unit(cap, unit_cap)
        capex = 0
        for i in cap_list:
            if i == 0:
                capex += 0
            elif i < min_cap:
                capex = (capex + min_cap * (parameter_1 * min_cap **
                (parameter_2)))
            elif i > max_cap:
                capex = (capex + max_cap * (parameter_1 * max_cap **
                (parameter_2)))
            else:
                capex = (capex + i * (parameter_1 * i ** (parameter_2)))

    elif component == 'Cogeneration unit gas' or \
    component == 'Cogeneration unit biogas':
        cap_list = co2.cap_cog_unit_de(cap, unit_cap)
        capex = 0
        for i in cap_list:
            if i == 0:
                capex += 0
            elif i < min_cap:
                capex = (capex + min_cap * (parameter_1 * min_cap **
                (parameter_2)))
            elif i > max_cap:
                capex = (capex + max_cap * (parameter_1 * max_cap **
                (parameter_2)))
            else:
                capex = (capex + i * (parameter_1 * i ** (parameter_2)))

    elif component == 'DH thermal storage':
        volume = co2.volume_thermal_storage(cap, T_hot, T_cold)
        if volume < min_cap:
            capex = min_cap * (parameter_1 * log(min_cap) + parameter_2)
        elif volume > max_cap:
            capex = max_cap * (parameter_1 * log(max_cap) + parameter_2)
        else:
            capex = volume * (parameter_1 * log(volume) + parameter_2)

    elif component == 'Gas Boiler':
        if cap == 0:
            capex = 0
        elif cap < min_cap:
            capex = min_cap * (parameter_1 * log(min_cap) + parameter_2)
        elif cap > max_cap:
            capex = max_cap * (parameter_1 * log(max_cap) + parameter_2)
        else:
            capex = cap * (parameter_1 * log(cap) + parameter_2)

    else:
        print (('Invalid component. The chosen component was: %s'
        % component))

    # the total fixed costs per lifetime and installed capacity are calculated
    costs_lifetime = cap * lifetime * opex_fixed + annuity_f * capex * (
        credit_period - grace_period) + interest_rate * grace_period * capex

    # the total fixed costs per year and installed capacity are calculated
    annual_costs = costs_lifetime / lifetime

    return annual_costs


def pv(cur, input_data, cap_pv_roof=None, cap_pv_ground=None):
    '''
    Returns the total costs in €/year due to the construction and maintenance
    of the specified area of pv modules.

    Keyword arguments:
        area - total area of all moduls in m²
        PV_type - implemented PV types are "Aufdach" and "Freifläche"
    '''

    # PV ground
    if cap_pv_ground:
        # PV ground area
        area_ground = cap_pv_ground * 1000 / input_data['eta PV']
        # calculate annual costs
        annual_costs_ground = costs_annual(cur, 'PV Freifläche', area_ground)
    else:
        area_ground = 0
        annual_costs_ground = 0

    # PV roof
    if cap_pv_roof:
        # PV roof area
        area_roof = cap_pv_roof * 1000 / input_data['eta PV']
        # calculate annual costs
        annual_costs_roof = costs_annual(cur, 'PV Aufdach', area_roof)
    else:
        area_roof = 0
        annual_costs_roof = 0

    return (annual_costs_ground + annual_costs_roof), (area_ground + area_roof)


def wind_turbine(cur, cap):
    '''
    Returns the costs in €/year due to the construction of the
    specified number of wind turbines.

    Keyword arguments:
        cap - capacity of one turbine in kW
        number_wka - number of wind turbines
    '''
    # calculate annual costs
    annual_costs = costs_annual(cur, 'Wind turbine', cap)
    return annual_costs


def thermal_storage(cur, cap, T_hot, T_cold):
    '''
    Returns the costs in €/year of a thermal storage.
    '''
    # calculate storage volume
    volume = co2.volume_thermal_storage(cap, T_hot, T_cold)
    # calculate annual costs
    annual_costs = costs_annual(cur, 'Thermal Storage', volume)
    return annual_costs


def variable(input_data):
    '''
    Returns the variable costs in €/MWh_fuel for the operation of each
    plant in the energy system.
    '''
    conn = db.open_db_connection()
    cur = conn.cursor()
    # Costs of fuels
    gas_costs = opex_var(cur, 'Natural Gas')
    gas_costs_heating = opex_var(cur, 'Natural Gas Heating')
    oil_costs = opex_var(cur, 'Oil')
    coal_costs = opex_var(cur, 'Coal')
    biogas_costs = opex_var(cur, 'Biogas')
    biomass_costs = opex_var(cur, 'Wood')
    el_import_costs = opex_var(cur, 'El Import')
    excess_heat_costs = opex_var(cur, 'District Heat')

    # Gas cog unit allocation
    dh_gas_cog_costs_heat, dh_gas_cog_costs_power = \
        co2.finnische_methode(input_data['eta DH Gas Cog unit Heat'],
        input_data['eta DH Gas Cog unit Power'],
        input_data['eta reference thermal'],
        input_data['eta reference electrical'], gas_costs)

    # Biogas cog unit allocation
    dh_biogas_cog_costs_heat, dh_biogas_cog_costs_power = \
        co2.finnische_methode(input_data['eta DH Biogas Cog unit Heat'],
        input_data['eta DH Biogas Cog unit Power'],
        input_data['eta reference thermal'],
        input_data['eta reference electrical'], biogas_costs)

    # Biomass cog unit allocation
    dh_biomass_cog_costs_heat, dh_biomass_cog_costs_power = \
        co2.finnische_methode(input_data['eta DH Biomass Cog Heat'],
        input_data['eta DH Biomass Cog Power'],
        input_data['eta reference thermal'],
        input_data['eta reference electrical'], biomass_costs)

    # Gas cog unit allocation
    gas_cog_costs_heat, gas_cog_costs_power = \
        co2.finnische_methode(input_data['eta Gas Cog unit Heat'],
        input_data['eta Gas Cog unit Power'],
        input_data['eta reference thermal'],
        input_data['eta reference electrical'], gas_costs)

    # Biogas cog unit allocation
    biogas_cog_costs_heat, biogas_cog_costs_power = \
        co2.finnische_methode(input_data['eta Biogas Cog unit Heat'],
        input_data['eta Biogas Cog unit Power'],
        input_data['eta reference thermal'],
        input_data['eta reference electrical'], biogas_costs)

    # Costs in €/MWh of produced energy
    costs_dict = \
        {'PV': 0.0000001,
         'Wind': 0.0000001,
         'Hydropower': 0.0000001,
         'El Import': el_import_costs[0] * 1000,
         'Biomass Power': biomass_costs[0] * 1000,
         'Gas Power': gas_costs[0] * 1000,
         'Gas Heat': gas_costs_heating[0] * 1000,
         'Oil Heat': oil_costs[0] * 1000,
         'Biomass Heat': biomass_costs[0] * 1000,
         'ST Heat': 0.0000001,
         'ST Heat supp Gas': gas_costs_heating[0] * 1000,
         'Coal Heat': coal_costs[0] * 1000,
         'DH Biogas Heat': biogas_costs[0] * 1000,
         'DH Gas Heat': gas_costs[0] * 1000,
         'DH Biogas Cog unit Heat': dh_biogas_cog_costs_heat[0] * 1000,
         'DH Biogas Cog unit Power': dh_biogas_cog_costs_power[0] * 1000,
         'DH Gas Cog unit Heat': dh_gas_cog_costs_heat[0] * 1000,
         'DH Gas Cog unit Power': dh_gas_cog_costs_power[0] * 1000,
         'DH Biomass Cog Heat': dh_biomass_cog_costs_heat[0] * 1000,
         'DH Biomass Cog Power': dh_biomass_cog_costs_power[0] * 1000,
         'DH Excess Heat': excess_heat_costs[0] * 1000,
         'Gas Cog unit Heat': gas_cog_costs_heat[0] * 1000,
         'Gas Cog unit Power': gas_cog_costs_power[0] * 1000,
         'Biogas Cog unit Heat': biogas_cog_costs_heat[0] * 1000,
         'Biogas Cog unit Power': biogas_cog_costs_power[0] * 1000,
         'Gas Cog unit Boiler': gas_costs_heating[0] * 1000,
         'Biogas Cog unit Boiler': gas_costs_heating[0] * 1000
         }
    # fuel DH Thermal Storage Boiler
    if input_data['fuel DH Thermal Storage Boiler'] == 'Biogas':
        costs_dict['DH Thermal Storage Boiler'] = biogas_costs[0] * 1000
    else:
        costs_dict['DH Thermal Storage Boiler'] = gas_costs[0] * 1000

    cur.close()
    conn.close()

    return costs_dict


def fixed(input_data, cap_pv,
    wind_cap, st_area,
    cap_dh_gas_heat, cap_gas_power, components_dict, cap_hpm_air_heating,
    cap_hpm_air_ww, cap_hpm_brine_heating, cap_hpm_brine_ww, p_set):
    '''
    Fixed costs due to construction of the power plant and increase
    with an increasing power plant capacity.
    '''

    conn = db.open_db_connection()
    cur = conn.cursor()

    # dictionary with fixed costs per year and installed capacity [€/a]
    fixed_costs = {}
    # Power
    if 'PV' in components_dict['Power Sources']:
        cap_pv_ground = p_set['cap_pv_ground'][p_set['index']]
        fixed_costs['PV'], pv_area = pv(
            cur, input_data, cap_pv_roof=(cap_pv - cap_pv_ground),
            cap_pv_ground=cap_pv_ground)
    if 'Wind' in components_dict['Power Sources']:
        fixed_costs['Wind'] = wind_turbine(
            cur, wind_cap * 1000)
    if 'Hydropower' in components_dict['Power Sources']:
        fixed_costs['Hydropower'] = costs_annual(
            cur, 'Hydropower', p_set['cap_hydropower'] * 1000)
    if 'Biomass Power' in components_dict['Power Sources']:
        fixed_costs['Biomass Power'] = costs_annual(
            cur, 'Combined cycle power plant biomass',
            input_data['cap Biomass Power'] * 1000)
        fixed_costs['DH Biomass Cog'] = 0
    if 'Gas Power' in components_dict['Power Sources']:
        fixed_costs['Gas Power'] = costs_annual(
            cur, 'Combined cycle power plant gas', cap_gas_power * 1000)
    # Gas Heat
    if 'Gas Heat' in components_dict['Heating Systems']:
        fixed_costs['Gas Heat'] = costs_annual(
            cur, 'Gas heating', p_set['max_heat_gas'] * 1000)
    if 'Gas el Heating' in components_dict['el Heating']:
        fixed_costs['Gas el Heating'] = costs_annual(
            cur, 'El Heating', input_data['cap Gas el Heating'] * 1000)
    if 'Gas Storage Thermal' in components_dict['Storages']:
        fixed_costs['Gas Storage Thermal'] = thermal_storage(
            cur, input_data['cap Gas Storage Thermal'],
            input_data['TS Building hot'],
            input_data['TS Building cold'])
    # Oil Heat
    if 'Oil Heat' in components_dict['Heating Systems']:
        fixed_costs['Oil Heat'] = costs_annual(
            cur, 'Oil heating', p_set['max_heat_oil'] * 1000)
    if 'Oil el Heating' in components_dict['el Heating']:
        fixed_costs['Oil el Heating'] = costs_annual(
            cur, 'El Heating', input_data['cap Oil el Heating'] * 1000)
    if 'Oil Storage Thermal' in components_dict['Storages']:
        fixed_costs['Oil Storage Thermal'] = thermal_storage(
            cur, input_data['cap Oil Storage Thermal'],
            input_data['TS Building hot'],
            input_data['TS Building cold'])
    # Coal Heat
    if 'Coal Heat' in components_dict['Heating Systems']:
        fixed_costs['Coal Heat'] = costs_annual(
            cur, 'Coal heating', p_set['max_heat_coal'] * 1000)
    if 'Coal el Heating' in components_dict['el Heating']:
        fixed_costs['Coal el Heating'] = costs_annual(
            cur, 'El Heating', input_data['cap Coal el Heating'] * 1000)
    if 'Coal Storage Thermal' in components_dict['Storages']:
        fixed_costs['Coal Storage Thermal'] = thermal_storage(
            cur, input_data['cap Coal Storage Thermal'],
            input_data['TS Building hot'],
            input_data['TS Building cold'])
    # Biomass Heat
    if 'Biomass Heat' in components_dict['Heating Systems']:
        fixed_costs['Biomass Heat'] = costs_annual(
            cur, 'Wood-fired heating', p_set['max_heat_biomass'] * 1000)
    if 'Biomass el Heating' in components_dict['el Heating']:
        fixed_costs['Biomass el Heating'] = costs_annual(
            cur, 'El Heating', input_data['cap Biomass el Heating'] * 1000)
    if 'Biomass Storage Thermal' in components_dict['Storages']:
        fixed_costs['Biomass Storage Thermal'] = thermal_storage(
            cur, input_data['cap Biomass Storage Thermal'],
            input_data['TS Building hot'],
            input_data['TS Building cold'])
    # Solarthermal Heat
    if 'ST Heat' in components_dict['Solarthermal System']:
        fixed_costs['ST Heat'] = costs_annual(
            cur, 'Solar Heat', st_area)
    if 'ST Heat supp Gas' in components_dict['Solarthermal System']:
        fixed_costs['ST Heat supp Gas'] = costs_annual(
            cur, 'Gas heating', p_set['max_heat_st'] * 1000)
    if 'ST el Heating' in components_dict['el Heating']:
        fixed_costs['ST el Heating'] = costs_annual(
            cur, 'El Heating', input_data['cap ST el Heating'] * 1000)
    if 'ST Storage Thermal' in components_dict['Storages']:
        fixed_costs['ST Storage Thermal'] = thermal_storage(
            cur, input_data['cap ST Storage Thermal'], 90, 25)
    # DH
    if 'DH Biogas Heat' in components_dict['Heat Sources']:
        fixed_costs['DH Biogas Heat'] = costs_annual_regression(
            cur, 'Gas Boiler', input_data['cap DH Biogas Heat'] * 1000)
    if 'DH Gas Heat' in components_dict['Heat Sources']:
        fixed_costs['DH Gas Heat'] = costs_annual_regression(cur,
        'Gas Boiler', cap_dh_gas_heat * 1000)
    if 'DH Biogas Cog unit' in components_dict['Cog Sources']:
        fixed_costs['DH Biogas Cog unit'] = costs_annual_regression(
            cur, 'DH Cogeneration unit biogas',
            input_data['cap DH Biogas Cog unit Power'] * 1000,
            unit_cap=input_data['Cap central Cog unit'] * 1000)
    if 'DH Gas Cog unit' in components_dict['Cog Sources']:
        fixed_costs['DH Gas Cog unit'] = costs_annual_regression(
            cur, 'DH Cogeneration unit gas',
            input_data['cap DH Gas Cog unit Power'] * 1000,
            unit_cap=input_data['Cap central Cog unit'] * 1000)
    if 'DH Storage Thermal' in components_dict['Storages']:
        fixed_costs['DH Storage Thermal'] = costs_annual_regression(
            cur, 'DH thermal storage', input_data['cap DH Storage Thermal'],
            input_data['DH T_storage'],
            input_data['DH T_return'])
    if 'DH Thermal Storage Boiler' in components_dict['Heat Sources']:
        fixed_costs['DH Thermal Storage Boiler'] = costs_annual_regression(
            cur, 'Gas Boiler',
            input_data['cap DH Thermal Storage Boiler'] * 1000)
    if 'DH el Heating' in components_dict['el Heating']:
        fixed_costs['DH el Heating'] = costs_annual(
            cur, 'El Heating', input_data['cap DH el Heating'] * 1000)
    if p_set['max_heat_dh'] > 0:
        fixed_costs['DH grid'] = costs_annual(cur, 'DH grid',
            p_set['max_heat_dh'] * 1000)
        fixed_costs['DH connection'] = costs_annual(cur, 'DH connection',
            p_set['max_heat_dh'] * 1000)
    # Storage Battery
    if 'Storage Battery' in components_dict['Storages']:
        usable_cap = 0.5
        fixed_costs['Storage Battery'] = costs_annual(
            cur, 'Battery',
            input_data['cap Storage Battery'] * 1000 * usable_cap)
    # dec. Gas Cog unit
    if 'Gas Cog unit' in components_dict['dec Cog units']:
        fixed_costs['Gas Cog unit'] = costs_annual_regression(
            cur, 'DH Cogeneration unit gas',
            input_data['cap Gas Cog unit Power'] * 1000,
            unit_cap=input_data['Cap dec Cog unit'] * 1000)
    if 'Gas Cog unit Boiler' in components_dict['dec Cog units']:
        fixed_costs['Gas Cog unit Boiler'] = costs_annual_regression(
            cur, 'Gas Boiler',
            input_data['cap Gas Cog unit Boiler'] * 1000)
    if 'Gas Cog unit el Heating' in components_dict['el Heating']:
        fixed_costs['Gas Cog unit el Heating'] = costs_annual(
            cur, 'El Heating', input_data['cap Gas Cog unit el Heating'] * 1000)
    if 'Gas Cog unit Storage Thermal' in components_dict['Storages']:
        fixed_costs['Gas Cog unit Storage Thermal'] = thermal_storage(
            cur, input_data['cap Gas Cog unit Storage Thermal'],
            T_hot=90, T_cold=65)
    # dec. Biogas Cog unit
    if 'Biogas Cog unit' in components_dict['dec Cog units']:
        fixed_costs['Biogas Cog unit'] = costs_annual_regression(
            cur, 'DH Cogeneration unit biogas',
            input_data['cap Biogas Cog unit Power'] * 1000,
            unit_cap=input_data['Cap dec Cog unit'] * 1000)
    if 'Biogas Cog unit Boiler' in components_dict['dec Cog units']:
        fixed_costs['Biogas Cog unit Boiler'] = costs_annual_regression(
            cur, 'Gas Boiler',
            input_data['cap Biogas Cog unit Boiler'] * 1000)
    if 'Biogas Cog unit el Heating' in components_dict['el Heating']:
        fixed_costs['Biogas Cog unit el Heating'] = costs_annual(
            cur, 'El Heating',
            input_data['cap Biogas Cog unit el Heating'] * 1000)
    if 'Biogas Cog unit Storage Thermal' in components_dict['Storages']:
        fixed_costs['Biogas Cog unit Storage Thermal'] = thermal_storage(
            cur, input_data['cap Biogas Cog unit Storage Thermal'],
            T_hot=90, T_cold=65)
    # Heat Pumps
    if 'HP Mono Air Heating' in components_dict['Heat Pump Mono']:
        fixed_costs['HP Mono Air Heating'] = costs_annual(
            cur, 'HP Mono Air', cap_hpm_air_heating * 1000)
        fixed_costs['HP Mono Air Heating el Heating'] = 0
    if 'HP Mono Air WW' in components_dict['Heat Pump Mono']:
        fixed_costs['HP Mono Air WW'] = costs_annual(
            cur, 'HP Mono Air', cap_hpm_air_ww * 1000)
        fixed_costs['HP Mono Air WW el Heating'] = 0
    if 'HP Mono Brine Heating' in components_dict['Heat Pump Mono']:
        fixed_costs['HP Mono Brine Heating'] = costs_annual(
            cur, 'HP Mono Brine', cap_hpm_brine_heating * 1000)
    if 'HP Mono Brine WW' in components_dict['Heat Pump Mono']:
        fixed_costs['HP Mono Brine WW'] = costs_annual(
            cur, 'HP Mono Brine', cap_hpm_brine_ww * 1000)
    # Heat Pump Thermal Storages
    if 'HP Mono Air Heating Storage Thermal' in components_dict['Storages']:
        fixed_costs['HP Mono Air Heating Storage Thermal'] = \
            thermal_storage(cur,
            input_data['cap HP Mono Air Heating Storage Thermal'],
            input_data['TS HP Heating hot'],
            input_data['TS HP Heating cold'])
    if 'HP Mono Air WW Storage Thermal' in components_dict['Storages']:
        fixed_costs['HP Mono Air WW Storage Thermal'] = 0
    if 'HP Mono Brine Heating Storage Thermal' in components_dict['Storages']:
        fixed_costs['HP Mono Brine Heating Storage Thermal'] = \
            thermal_storage(cur,
            input_data['cap HP Mono Brine Heating Storage Thermal'],
            input_data['TS HP Heating hot'],
            input_data['TS HP Heating cold'])
    if 'HP Mono Brine WW Storage Thermal' in components_dict['Storages']:
        fixed_costs['HP Mono Brine WW Storage Thermal'] = 0

    cur.close()
    conn.close()

    return fixed_costs