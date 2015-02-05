#!/usr/bin/python
# -*- coding: utf-8

from math import exp, log
import numpy as np
import database as db
import wka


def finnische_methode(eta_th, eta_el, eta_th_ref, eta_el_ref, variable_total):
    '''
    Calculates the share of CO2 emissions of heat and power in a cogeneration
    plant after the "Finnische Methode".
    '''
    share_heat = ((eta_th / eta_th_ref) /
        (eta_th / eta_th_ref + eta_el / eta_el_ref))
    share_power = ((eta_el / eta_el_ref) /
        (eta_th / eta_th_ref + eta_el / eta_el_ref))
    variable_heat = share_heat * variable_total
    variable_power = share_power * variable_total

    return variable_heat, variable_power


def regression(cur, energy_system_component):
    '''
    Returns the CO2 emissions in kg/lifetime due to the construction of the
    specified number of units using a degressive regression.
    '''
    # retrieve regression parameters from database
    cur.execute('''
        select "Parameter 1", "Parameter 2", "min Cap", "max Cap"
        from wittenberg.co2_regression_parameters
        where "Energy system comp" = %(str)s
    ''', {'str': energy_system_component})
    parameters = np.asarray(cur.fetchall())
    return (parameters[0][0], parameters[0][1], parameters[0][2],
        parameters[0][3])


def fuel(cur, fuel, sources, manure_percentage=0):
    '''
    Returns the fossil CO2 emissions in kg/MWh that are emitted either directly
    through the combustion of the fuel or indirectly by transporting the fuel to
    the plant.
    "Sources" defines the emissions that should be considered which
    is especially important when choosing biogas. Here emission credits can
    be considered i.e. due to a decimation of methane emissions if the manure
    were to be applied.

    Keyword arguments:
        sources - cause of emission (i.e. combustion, transport, etc.)
        manure_percentage - Biogas emissions depend on the percentage of manure
                            used to produce the biogas. Here values for 0%,
                            2.4% and 6% are available.
    '''
    co2_emissions = np.zeros((len(sources), 1))
    # biogas
    if fuel == 'Biogas':
        # write comment query for SQL statement
        percentages = [0, 2.4, 6]
        comment = []
        for i in percentages:
            if i != manure_percentage:
                comment.append('Percentage of manure ca. ' + str(i) + '%')
        for i in range(len(sources)):
            cur.execute('''
                select "Emissions"
                from wittenberg.co2_variable_emissions
                where "Fuel" = 'Biogas'
                and "Emissions Source" = %(source)s
                and "Comment" != %(com_1)s
                and "Comment" != %(com_2)s
            ''', {'source': sources[i], 'com_1': comment[0],
                'com_2': comment[1]})
            co2_emissions[i] = np.asarray(cur.fetchall())
    # all other fuels
    else:
        for i in range(len(sources)):
            cur.execute('''
                select "Emissions"
                from wittenberg.co2_variable_emissions
                where "Fuel" = %(fuel)s
                and "Emissions Source" = %(source)s
            ''', {'fuel': fuel, 'source': sources[i]})
            co2_emissions[i] = np.asarray(cur.fetchall())
    return sum(co2_emissions) * 1000


def lifetime_of_component(cur, component):
    '''
    Retrieves the lifetime used in the calculation of the total emissions due
    to the construction of the chosen energy system component.
    '''
    cur.execute('''
        select "Lifetime"
        from wittenberg.co2_set_lifetimes
        where "Energy system comp" = %(str)s
    ''', {'str': component})
    component_lifetime = cur.fetchone()
    return component_lifetime[0]


def pv(cur, input_data, area, cap_pv):
    '''
    Returns the CO2 emissions in kg/year due to the construction of the
    specified area of pv modules.

    Keyword arguments:
        area - total area of all moduls in m²
        cell_type - implemented cell types are multi- and monocrystalline cells
    '''
    # PV area
    if not area:
        area = cap_pv * 10 ** 6 / input_data['eta PV'] / 1000
    # retrieve CO2 emissions [kg/m² lifetime] from database
    PV_type = 'PV ' + input_data['PV cell type']
    cur.execute('''
        select "Emissions"
        from wittenberg.co2_fixed_emissions
        where "Energy system comp" = %(str)s
    ''', {'str': PV_type})
    data = np.asarray(cur.fetchall())
    # CO2 emissions are calculated by calculating the mean of all emission data
    # for the specified cell type multiplied by the total PV area and devided
    # by the lifetime
    lifetime = lifetime_of_component(cur, 'PV')
    co2_emissions = (sum(data) / len(data)) * area / lifetime
    return co2_emissions[0], area


def st(cur, area):
    '''
    Returns the CO2 emissions in kg/year due to the construction of the
    specified area of solarthermal collectors.

    Keyword arguments:
        area - total area of all moduls in m²
    '''
    # retrieve CO2 emissions [kg/m² lifetime] from database
    cur.execute('''
        select "Emissions"
        from wittenberg.co2_fixed_emissions
        where "Energy system comp" = 'Solar Heat'
    ''')
    data = cur.fetchone()[0]
    # CO2 emissions are calculated by multiplying the specific emissions
    # by the total solarthermal collector area devided by the lifetime
    lifetime = lifetime_of_component(cur, 'Solar Heat')
    co2_emissions = data * area / lifetime
    return co2_emissions


def wind_turbine(cur, number_wka, wka_type, cap_wind, p_set, cap_turbine=None):
    '''
    Returns the CO2 emissions in kg/year due to the construction of the
    specified number of wind turbines. Estimation of emissions is only valid
    for wind turbine capacities between 1.300 - 3.000 kW.

    Keyword arguments:
        cap - capacity of one turbine in MW
        number_wka - number of wind turbines
    '''
    # get capacity of one wind turbine if not given
    if not cap_turbine:
        if p_set['wind_pot'] == 'scaled_mixed':
            cap_turbine = wka.mixed_wind_feedin_av_cap(
                p_set['cap_wind_current'][p_set['index']] /
                p_set['cap_wind'][p_set['index']])
        else:
            cap_turbine = db.P_max_wka(wka_type)

    # get number of wind turbines
    if not number_wka:
        number_wka = cap_wind / cap_turbine

    # get regression parameters
    parameter_1, parameter_2, min_cap, max_cap = regression(cur, 'Wind turbine')
    # CO2 emissions are calculated using a degressive regression
    lifetime = lifetime_of_component(cur, 'Wind turbine')
    if cap_turbine < min_cap:
        co2_emissions = \
        number_wka * ((exp(parameter_1 * log(min_cap) + parameter_2) / lifetime)
        / min_cap * cap_turbine)
    elif cap_turbine > max_cap:
        co2_emissions = \
        number_wka * ((exp(parameter_1 * log(max_cap) + parameter_2) / lifetime)
        / max_cap * cap_turbine)
    else:
        co2_emissions = number_wka * \
            exp(parameter_1 * log(cap_turbine) + parameter_2) / lifetime
    return co2_emissions, number_wka


def cog_unit(cur, cap, unit_cap, fuel):
    '''
    Returns the CO2 emissions in kg/year due to the construction of the
    cogeneration unit.

    Keyword arguments:
        cap - capacity of one cogeneration unit in MW
        number_cog_units - number of cogeneration units
    '''
    # create capacity list
    cap_list = cap_cog_unit(cap, unit_cap)
    # get regression parameters
    parameter_1, parameter_2, min_cap, max_cap = regression(cur,
        'Cogeneration unit')
    # CO2 emissions are calculated using a degressive regression
    lifetime = lifetime_of_component(cur, 'Cogeneration unit')

    co2_emissions = 0
    for i in cap_list:
        if i == 0:
            co2_emissions += 0
        elif i < min_cap:
            co2_emissions = (co2_emissions +
                (exp(parameter_1 * log(min_cap) + parameter_2) / lifetime) /
                min_cap * i)
        elif i > max_cap:
            co2_emissions = (co2_emissions +
                (exp(parameter_1 * log(max_cap) + parameter_2) / lifetime) /
                max_cap * i)
        else:
            co2_emissions = (co2_emissions +
                exp(parameter_1 * log(i) + parameter_2) / lifetime)

    # Emissions of fermenter
    if fuel == 'Biogas':
            # get regression parameters
            parameter_1_f, parameter_2_f, min_cap_f, max_cap_f = regression(cur,
                'Fermenter')
            # CO2 emissions are calculated using a degressive regression
            lifetime_f = lifetime_of_component(cur, 'Fermenter')
            co2_emissions_fermenter = 0
            for i in cap_list:
                if i == 0:
                    co2_emissions_fermenter += 0
                elif i < min_cap_f:
                    co2_emissions_fermenter = ((exp(parameter_1_f *
                    log(min_cap_f) + parameter_2_f) / lifetime_f) /
                    min_cap_f * i)
                    co2_emissions = co2_emissions + co2_emissions_fermenter
                elif i > max_cap_f:
                    co2_emissions_fermenter = ((exp(parameter_1_f *
                    log(max_cap_f) + parameter_2_f) / lifetime_f) /
                    max_cap_f * i)
                    co2_emissions = co2_emissions + co2_emissions_fermenter
                else:
                    co2_emissions_fermenter = exp(parameter_1_f * log(i)
                        + parameter_2_f) / lifetime_f
                    co2_emissions = co2_emissions + co2_emissions_fermenter

    return co2_emissions


def ccpp(cur, cap):
    '''
    Returns the CO2 emissions in kg/year due to the construction of a combined
    cycle power plant (CCPP).

    Keyword arguments:
        cap - power plant capacity in MW
    '''
    # get regression parameters
    parameter_1, parameter_2, min_cap, max_cap = regression(cur,
        'Combined cycle power plant')
    # CO2 emissions are calculated using a degressive regression
    lifetime = lifetime_of_component(cur, 'Combined cycle power plant')
    if cap == 0:
        co2_emissions = 0
    elif cap < min_cap:
        co2_emissions = ((exp(parameter_1 * log(min_cap) + parameter_2) /
        lifetime) / min_cap * cap)
    elif cap > max_cap:
        co2_emissions = ((exp(parameter_1 * log(max_cap) + parameter_2) /
        lifetime) / max_cap * cap)
    else:
        co2_emissions = exp(parameter_1 * log(cap) + parameter_2) / lifetime
    return co2_emissions


def boiler(cur, cap):
    '''
    Returns the CO2 emissions in kg/year due to the construction of a boiler.

    Keyword arguments:
        cap - boiler capacity in MW
    '''
    # get regression parameters
    parameter_1, parameter_2, min_cap, max_cap = regression(cur, 'Gas boiler')
    # CO2 emissions are calculated using a degressive regression
    lifetime = lifetime_of_component(cur, 'Gas boiler')
    if cap == 0:
        co2_emissions = 0
    elif cap < min_cap:
        co2_emissions = ((exp(parameter_1 * log(min_cap) + parameter_2)
        / lifetime) / min_cap * cap)
    elif cap > max_cap:
        co2_emissions = ((exp(parameter_1 * log(max_cap) + parameter_2)
        / lifetime) / max_cap * cap)
    else:
        co2_emissions = exp(parameter_1 * log(cap) + parameter_2) / lifetime
    return co2_emissions


def heating_system(cur, heating_sys, cap):
    '''
    Returns the CO2 emissions in kg/year of the chosen heating system.
    '''
    # retrieve CO2 emissions [kg/lifetime] from database
    cur.execute('''
        select "Power [MW]", "Emissions"
        from wittenberg.co2_fixed_emissions
        where "Energy system comp" = %(str)s
    ''', {'str': heating_sys})
    data = np.asarray(cur.fetchall())
    # CO2 emissions are calculated by multiplying the retrieved value by the
    # number of heating systems necessary to meet the needed capacity
    lifetime = lifetime_of_component(cur, heating_sys)
    co2_emissions = float(cap) / data[0][0] * data[0][1] / lifetime
    return co2_emissions


def el_heating(cur, cap):
    '''
    Returns the CO2 emissions in kg/year of an electrical heating element.
    '''
    # retrieve CO2 emissions [kg/lifetime] from database
    cur.execute('''
        select "Power [MW]", "Emissions"
        from wittenberg.co2_fixed_emissions
        where "Energy system comp" = 'Heating element'
    ''')
    data = np.asarray(cur.fetchall())
    # CO2 emissions are calculated by multiplying the retrieved value by the
    # number of heating elements necessary to meet the needed capacity
    lifetime = lifetime_of_component(cur, 'Heating element')
    co2_emissions = float(cap) / data[0][0] * data[0][1] / lifetime
    return co2_emissions


def annual_emissions(cur, cap, comp):
    '''
    Returns the CO2 emissions in kg/year of the specified component.
    '''
    # retrieve CO2 emissions [kg/lifetime] from database
    cur.execute('''
        select "Power [MW]", "Emissions"
        from wittenberg.co2_fixed_emissions
        where "Energy system comp" = %(str)s
    ''', {'str': comp})
    data = np.asarray(cur.fetchall())
    # CO2 emissions are calculated by multiplying the retrieved value by the
    # number of heating elements necessary to meet the needed capacity
    lifetime = lifetime_of_component(cur, comp)
    co2_emissions = float(cap) / data[0][0] * data[0][1] / lifetime
    return co2_emissions


def heat_pump(cur, cap, hp):
    '''
    Returns the CO2 emissions in kg/year of heat pumps.
    '''
    # retrieve CO2 emissions [kg/lifetime] from database
    cur.execute('''
        select "Power [MW]", "Emissions"
        from wittenberg.co2_fixed_emissions
        where "Energy system comp" = %(str)s
    ''', {'str': hp})
    data = np.asarray(cur.fetchall())
    # CO2 emissions are calculated by multiplying the retrieved value by the
    # number of heating elements necessary to meet the needed capacity
    lifetime = lifetime_of_component(cur, hp)
    co2_emissions = float(cap) / data[0][0] * data[0][1] / lifetime
    return co2_emissions


def thermal_storage(cur, cap, T_hot, T_cold):
    '''
    Returns the CO2 emissions in kg/year of a thermal storage.
    '''
    # calculate storage volume
    volume = volume_thermal_storage(cap, T_hot, T_cold)
    # retrieve CO2 emissions [kg/lifetime] from database
    cur.execute('''
        select "Emissions"
        from wittenberg.co2_fixed_emissions
        where "Energy system comp" = 'Thermal storage'
    ''')
    data = np.asarray(cur.fetchall())
    # CO2 emissions are calculated by multiplying the retrieved value by the
    # total volume of all thermal storages
    lifetime = lifetime_of_component(cur, 'Thermal storage')
    co2_emissions = float(volume) * data[0][0] / lifetime
    return co2_emissions


def DH_grid(cur, cap):
    '''
    Returns the CO2 emissions in kg/year of the district heating system.
    '''
    # retrieve CO2 emissions [kg/lifetime] from database
    cur.execute('''
        select "Power [MW]", "Emissions"
        from wittenberg.co2_fixed_emissions
        where "Energy system comp" = 'DH grid'
    ''')
    data = np.asarray(cur.fetchall())
    # CO2 emissions are calculated by multiplying the retrieved value by the
    # total capacity of the district heating system
    lifetime = lifetime_of_component(cur, 'DH grid')
    co2_emissions = float(cap) / data[0][0] * data[0][1] / lifetime
    return co2_emissions


def DH_connection(cur, cap):
    '''
    Returns the CO2 emissions in kg/year of the district heating
    house connections.
    '''
    # retrieve CO2 emissions [kg/lifetime] from database
    cur.execute('''
        select "Power [MW]", "Emissions"
        from wittenberg.co2_fixed_emissions
        where "Energy system comp" = 'DH connection'
    ''')
    data = np.asarray(cur.fetchall())
    # CO2 emissions are calculated by multiplying the retrieved value by the
    # total capacity of the district heating system.
    lifetime = lifetime_of_component(cur, 'DH connection')
    co2_emissions = float(cap) / data[0][0] * data[0][1] / lifetime
    return co2_emissions


def battery(cur, cap):
    '''
    Returns the CO2 emissions in kg/year of an electrical heating element.
    '''
    usable_cap = 0.5
    # retrieve CO2 emissions [kg/lifetime] from database
    cur.execute('''
        select "Emissions"
        from wittenberg.co2_fixed_emissions
        where "Energy system comp" = 'PSB Battery'
    ''')
    data = np.asarray(cur.fetchall())
    # CO2 emissions are calculated by multiplying the retrieved value by the
    # total volume of all thermal storages
    lifetime = lifetime_of_component(cur, 'VRB Battery')
    co2_emissions = float(cap) / usable_cap * data[0][0] / lifetime
    return co2_emissions


def variable(input_data):
    '''
    Returns the variable CO2 emissions in kg/MWh_fuel that are emitted during
    the operation of each plant in the energy system due to direct
    emissions from combustion or indirect emissions from i.e. transport of the
    fuel to the plant.
    '''
    conn = db.open_db_connection()
    cur = conn.cursor()
    # Emissions of fuels
    gas_emissions = fuel(cur, 'Natural gas', ['Combustion', 'Provision'])
    oil_emissions = fuel(cur, 'Fuel oil', ['Combustion', 'Provision'])
    coal_emissions = fuel(cur, 'Coal', ['Combustion', 'Provision'])
    biogas_emissions = fuel(
                 cur, 'Biogas', ['Power consumption during operation',
                 'Gas loss through cover', 'Growing', 'Methane slip',
                 'Gas release at engine standstill without torch',
                 'Final depot without coverage', 'Fertilizer substitution',
                 'Application of fermentation residue',
                 'Methane emission decimation'], 2.4)
    biomass_emissions = fuel(
             cur, 'Wood chips from Short-rotation plantations',
             ['Growing (with fertilizer) and transport'])
    el_emissions = fuel(cur, 'El Import', ['Lifecycle'])
    excess_heat_emissions = fuel(cur, 'District Heat', ['Lifecycle'])

    # Gas cog unit allocation
    gas_cog_emissions_heat, gas_cog_emissions_power = \
        finnische_methode(input_data['eta DH Gas Cog unit Heat'],
        input_data['eta DH Gas Cog unit Power'],
        input_data['eta reference thermal'],
        input_data['eta reference electrical'], gas_emissions)

    # Biogas cog unit allocation
    biogas_cog_emissions_heat, biogas_cog_emissions_power = \
        finnische_methode(input_data['eta DH Biogas Cog unit Heat'],
        input_data['eta DH Biogas Cog unit Power'],
        input_data['eta reference thermal'],
        input_data['eta reference electrical'], biogas_emissions)

    # Biomass cog unit allocation
    biomass_cog_emissions_heat, biomass_cog_emissions_power = \
        finnische_methode(input_data['eta DH Biomass Cog Heat'],
        input_data['eta DH Biomass Cog Power'],
        input_data['eta reference thermal'],
        input_data['eta reference electrical'], biomass_emissions)

    # CO2 emissions in kg/MWh of produced energy
    co2_dict = \
        {'PV': 0.0000001,
         'Wind': 0.0000001,
         'Hydropower': 0.0000001,
         'El Import': el_emissions[0],
         'Biomass Power': biomass_emissions[0],
         'Gas Power': gas_emissions[0],
         'Gas Heat': gas_emissions[0],
         'Oil Heat': oil_emissions[0],
         'Biomass Heat': biomass_emissions[0],
         'ST Heat': 0.0000001,
         'ST Heat supp Gas': gas_emissions[0],
         'Coal Heat': coal_emissions[0],
         'DH Biogas Heat': biogas_emissions[0],
         'DH Gas Heat': gas_emissions[0],
         'DH Biogas Cog unit Heat': biogas_cog_emissions_heat[0],
         'DH Biogas Cog unit Power': biogas_cog_emissions_power[0],
         'DH Gas Cog unit Heat': gas_cog_emissions_heat[0],
         'DH Gas Cog unit Power': gas_cog_emissions_power[0],
         'DH Biomass Cog Heat': biomass_cog_emissions_heat[0],
         'DH Biomass Cog Power': biomass_cog_emissions_power[0],
         'DH Excess Heat': excess_heat_emissions[0],
         'Gas Cog unit Heat': gas_cog_emissions_heat[0],
         'Gas Cog unit Power': gas_cog_emissions_power[0],
         'Biogas Cog unit Heat': biogas_cog_emissions_heat[0],
         'Biogas Cog unit Power': biogas_cog_emissions_power[0],
         'Gas Cog unit Boiler': gas_emissions[0],
         'Biogas Cog unit Boiler': gas_emissions[0]
         }

    if input_data['fuel DH Thermal Storage Boiler'] == 'Biogas':
        co2_dict['DH Thermal Storage Boiler'] = biogas_emissions[0]
    else:
        co2_dict['DH Thermal Storage Boiler'] = gas_emissions[0]

    cur.close()
    conn.close()

    return co2_dict


def cap_cog_unit(total_cap, unit_cap):
    '''
    Returns a list containing the capacities of the cogeneration units
    assuming that a unit can't be bigger than unit_cap.
    '''
    cap = []
    while total_cap > unit_cap:
        total_cap = total_cap - unit_cap
        cap.append(unit_cap)
    cap.append(total_cap)
    return cap


def volume_thermal_storage(storage_cap, T_hot=60, T_cold=30):
    '''
    Returns the storage volume in m³ of a thermal storage.
    (storage_cap in MWh)
    '''
    c_p = 1.163  # kWh/m³K
    volume = storage_cap * 10 ** 3 / c_p / (T_hot - T_cold)
    return volume


def fixed(input_data, pv_area, cap_pv,
    number_wka, cap_wind, st_area,
    cap_dh_gas_heat, cap_gas_power, components_dict, cap_hpm_air_heating,
    cap_hpm_air_ww, cap_hpm_brine_heating, cap_hpm_brine_ww, p_set):
    '''
    Fixed CO2 emissions are due to construction of the power plant and increase
    with an increasing power plant capacity.
    '''

    conn = db.open_db_connection()
    cur = conn.cursor()

    # dictionary with fixed CO2 emissions per year [kg/a]
    fixed_co2_emissions = {}
    # Power
    if 'PV' in components_dict['Power Sources']:
        fixed_co2_emissions['PV'], pv_area = pv(
            cur, input_data, pv_area, cap_pv)
    if 'Wind' in components_dict['Power Sources']:
        fixed_co2_emissions['Wind'], number_wka = wind_turbine(
            cur, number_wka, input_data['type_wka'], cap_wind, p_set)
    if 'Hydropower' in components_dict['Power Sources']:
        fixed_co2_emissions['Hydropower'] = annual_emissions(
            cur, p_set['cap_hydropower'], 'Hydropower')
    if 'Biomass Power' in components_dict['Power Sources']:
        fixed_co2_emissions['Biomass Power'] = ccpp(
            cur, input_data['cap Biomass Power'])
        fixed_co2_emissions['DH Biomass Cog'] = 0
    if 'Gas Power' in components_dict['Power Sources']:
        fixed_co2_emissions['Gas Power'] = ccpp(
            cur, cap_gas_power)
    # Gas Heat
    if 'Gas Heat' in components_dict['Heating Systems']:
        fixed_co2_emissions['Gas Heat'] = heating_system(
            cur, 'Gas heating', p_set['max_heat_gas'])
    if 'Gas el Heating' in components_dict['el Heating']:
        fixed_co2_emissions['Gas el Heating'] = el_heating(
            cur, input_data['cap Gas el Heating'])
    if 'Gas Storage Thermal' in components_dict['Storages']:
        fixed_co2_emissions['Gas Storage Thermal'] = thermal_storage(
            cur, input_data['cap Gas Storage Thermal'],
            input_data['TS Building hot'],
            input_data['TS Building cold'])
    # Oil Heat
    if 'Oil Heat' in components_dict['Heating Systems']:
        fixed_co2_emissions['Oil Heat'] = heating_system(
            cur, 'Oil heating', p_set['max_heat_oil'])
    if 'Oil el Heating' in components_dict['el Heating']:
        fixed_co2_emissions['Oil el Heating'] = el_heating(
            cur, input_data['cap Oil el Heating'])
    if 'Oil Storage Thermal' in components_dict['Storages']:
        fixed_co2_emissions['Oil Storage Thermal'] = thermal_storage(
            cur, input_data['cap Oil Storage Thermal'],
            input_data['TS Building hot'],
            input_data['TS Building cold'])
    # Coal Heat
    if 'Coal Heat' in components_dict['Heating Systems']:
        fixed_co2_emissions['Coal Heat'] = heating_system(
            cur, 'Oil heating', p_set['max_heat_coal'])
    if 'Coal el Heating' in components_dict['el Heating']:
        fixed_co2_emissions['Coal el Heating'] = el_heating(
            cur, input_data['cap Coal el Heating'])
    if 'Coal Storage Thermal' in components_dict['Storages']:
        fixed_co2_emissions['Coal Storage Thermal'] = thermal_storage(
            cur, input_data['cap Coal Storage Thermal'],
            input_data['TS Building hot'],
            input_data['TS Building cold'])
    # Biomass Heat
    if 'Biomass Heat' in components_dict['Heating Systems']:
        fixed_co2_emissions['Biomass Heat'] = heating_system(
            cur, 'Wood-fired heating', p_set['max_heat_biomass'])
    if 'Biomass el Heating' in components_dict['el Heating']:
        fixed_co2_emissions['Biomass el Heating'] = el_heating(
            cur, input_data['cap Biomass el Heating'])
    if 'Biomass Storage Thermal' in components_dict['Storages']:
        fixed_co2_emissions['Biomass Storage Thermal'] = thermal_storage(
            cur, input_data['cap Biomass Storage Thermal'],
            input_data['TS Building hot'],
            input_data['TS Building cold'])
    # Solarthermal Heat
    if 'ST Heat' in components_dict['Solarthermal System']:
        fixed_co2_emissions['ST Heat'] = st(cur, st_area)
    if 'ST Heat supp Gas' in components_dict['Solarthermal System']:
        fixed_co2_emissions['ST Heat supp Gas'] = heating_system(
            cur, 'Gas heating', p_set['max_heat_st'])
    if 'ST el Heating' in components_dict['el Heating']:
        fixed_co2_emissions['ST el Heating'] = el_heating(
            cur, input_data['cap ST el Heating'])
    if 'ST Storage Thermal' in components_dict['Storages']:
        fixed_co2_emissions['ST Storage Thermal'] = thermal_storage(
            cur, input_data['cap ST Storage Thermal'], 90, 25)
    # DH
    if 'DH Biogas Heat' in components_dict['Heat Sources']:
        fixed_co2_emissions['DH Biogas Heat'] = boiler(
            cur, input_data['cap DH Biogas Heat'])
    if 'DH Gas Heat' in components_dict['Heat Sources']:
        fixed_co2_emissions['DH Gas Heat'] = boiler(cur, cap_dh_gas_heat)
    if 'DH Biogas Cog unit' in components_dict['Cog Sources']:
        fixed_co2_emissions['DH Biogas Cog unit'] = cog_unit(
            cur, input_data['cap DH Biogas Cog unit Power'],
            input_data['Cap central Cog unit'], 'Biogas')
    if 'DH Gas Cog unit' in components_dict['Cog Sources']:
        fixed_co2_emissions['DH Gas Cog unit'] = cog_unit(
            cur, input_data['cap DH Gas Cog unit Power'],
            input_data['Cap central Cog unit'], 'Natural gas')
    if 'DH Storage Thermal' in components_dict['Storages']:
        fixed_co2_emissions['DH Storage Thermal'] = thermal_storage(
            cur, input_data['cap DH Storage Thermal'],
            input_data['DH T_storage'],
            input_data['DH T_return'])
    if 'DH Thermal Storage Boiler' in components_dict['Heat Sources']:
        fixed_co2_emissions['DH Thermal Storage Boiler'] = 0
    if 'DH el Heating' in components_dict['el Heating']:
        fixed_co2_emissions['DH el Heating'] = el_heating(
            cur, input_data['cap DH el Heating'])
    if p_set['max_heat_dh'] > 0:
        fixed_co2_emissions['DH grid'] = DH_grid(cur, p_set['max_heat_dh'])
        fixed_co2_emissions['DH connection'] = DH_connection(cur,
            p_set['max_heat_dh'])
    # Storage Battery
    if 'Storage Battery' in components_dict['Storages']:
        fixed_co2_emissions['Storage Battery'] = battery(
            cur, input_data['cap Storage Battery'])
    # dec. Gas Cog unit
    if 'Gas Cog unit' in components_dict['dec Cog units']:
        fixed_co2_emissions['Gas Cog unit'] = cog_unit(
            cur, input_data['cap Gas Cog unit Power'],
            input_data['Cap dec Cog unit'], 'Natural gas')
    if 'Gas Cog unit Boiler' in components_dict['dec Cog units']:
        fixed_co2_emissions['Gas Cog unit Boiler'] = boiler(
            cur, input_data['cap Gas Cog unit Boiler'])
    if 'Gas Cog unit el Heating' in components_dict['el Heating']:
        fixed_co2_emissions['Gas Cog unit el Heating'] = el_heating(
            cur, input_data['cap Gas Cog unit el Heating'])
    if 'Gas Cog unit Storage Thermal' in components_dict['Storages']:
        fixed_co2_emissions['Gas Cog unit Storage Thermal'] = thermal_storage(
            cur, input_data['cap Gas Cog unit Storage Thermal'],
            T_hot=90, T_cold=65)
    # dec. Biogas Cog unit
    if 'Biogas Cog unit' in components_dict['dec Cog units']:
        fixed_co2_emissions['Biogas Cog unit'] = cog_unit(
            cur, input_data['cap Biogas Cog unit Power'],
            input_data['Cap dec Cog unit'], 'Biogas')
    if 'Biogas Cog unit Boiler' in components_dict['dec Cog units']:
        fixed_co2_emissions['Biogas Cog unit Boiler'] = boiler(
            cur, input_data['cap Biogas Cog unit Boiler'])
    if 'Biogas Cog unit el Heating' in components_dict['el Heating']:
        fixed_co2_emissions['Biogas Cog unit el Heating'] = el_heating(
            cur, input_data['cap Biogas Cog unit el Heating'])
    if 'Biogas Cog unit Storage Thermal' in components_dict['Storages']:
        fixed_co2_emissions['Biogas Cog unit Storage Thermal'] = \
            thermal_storage(
            cur, input_data['cap Biogas Cog unit Storage Thermal'],
            T_hot=90, T_cold=65)
    # Heat Pumps
    if 'HP Mono Air Heating' in components_dict['Heat Pump Mono']:
        fixed_co2_emissions['HP Mono Air Heating'] = heat_pump(
            cur, cap_hpm_air_heating, 'HP Mono Air')
        fixed_co2_emissions['HP Mono Air Heating el Heating'] = 0
    if 'HP Mono Air WW' in components_dict['Heat Pump Mono']:
        fixed_co2_emissions['HP Mono Air WW'] = heat_pump(
            cur, cap_hpm_air_ww, 'HP Mono Air')
        fixed_co2_emissions['HP Mono Air WW el Heating'] = 0
    if 'HP Mono Brine Heating' in components_dict['Heat Pump Mono']:
        fixed_co2_emissions['HP Mono Brine Heating'] = heat_pump(
            cur, cap_hpm_brine_heating, 'HP Mono Brine')
    if 'HP Mono Brine WW' in components_dict['Heat Pump Mono']:
        fixed_co2_emissions['HP Mono Brine WW'] = heat_pump(
            cur, cap_hpm_brine_ww, 'HP Mono Brine')
    # Heat Pump Thermal Storages
    if 'HP Mono Air Heating Storage Thermal' in components_dict['Storages']:
        fixed_co2_emissions['HP Mono Air Heating Storage Thermal'] = \
        thermal_storage(cur,
            input_data['cap HP Mono Air Heating Storage Thermal'],
            input_data['TS HP Heating hot'],
            input_data['TS HP Heating cold'])
    if 'HP Mono Air WW Storage Thermal' in components_dict['Storages']:
        fixed_co2_emissions['HP Mono Air WW Storage Thermal'] = 0
    if 'HP Mono Brine Heating Storage Thermal' in components_dict['Storages']:
        fixed_co2_emissions['HP Mono Brine Heating Storage Thermal'] = \
        thermal_storage(cur,
            input_data['cap HP Mono Brine Heating Storage Thermal'],
            input_data['TS HP Heating hot'],
            input_data['TS HP Heating cold'])
    if 'HP Mono Brine WW Storage Thermal' in components_dict['Storages']:
        fixed_co2_emissions['HP Mono Brine WW Storage Thermal'] = 0

    cur.close()
    conn.close()

    return fixed_co2_emissions, number_wka