#!/usr/bin/python
# -*- coding: utf-8

import ee_potential_district
import database as db


def calc_hourly_biogas_pot(district):
    harvest_per_sqm = 0.00466  # Wert aus calculate_potential
                        # (MWh/m2 Energiegehalt des Gases pro m2 Ackerfläche)
    share_energy_use = 0.1
    area = db.agricultural_area(district)
    hourly_biogas_pot = area * harvest_per_sqm * share_energy_use / 8760
    return hourly_biogas_pot


def calc_annual_biomass_pot(district):
    pot_per_sqm = 0.000226  # Wert aus calculate_potential
                # MWh pro m2 Grundfläche (Biomassestudie Sachs. Anhalt 2007)
    area = db.forest_area(district)
    annual_biomass_pot = area * pot_per_sqm
    return annual_biomass_pot


def get_hourly_biogas_pot(input_data, potential,
    share_pot_used=1, hourly_potential=None):
    '''
    Returns the hourly biogas potential in MWh/h.
    '''
    # Returns the hourly potential of the chosen district in Wittenberg
    if potential == 'district':
        hourly_biogas_potential = ee_potential_district.biogas_potential(
            input_data, share_pot_used)
    elif potential == 'calc':
        hourly_biogas_potential = calc_hourly_biogas_pot(input_data['district'])
    elif potential == 'set_value':
        hourly_biogas_potential = hourly_potential
    else:
        print ('Chosen biogas_pot is not valid.')

    return hourly_biogas_potential


def get_annual_biomass_pot(input_data, potential,
    annual_potential=None, heat_demand_biomass=0):
    '''
    Returns the annual biomass potential in MWh/h.
    '''
    # Returns the annual potential of the chosen district in Wittenberg
    if potential == 'district':
        annual_biomass_potential = ee_potential_district.biomass_potential(
            input_data)
    elif potential == 'calc':
        annual_biomass_potential = calc_annual_biomass_pot(
            input_data['district'])
    elif potential == 'set_value':
        annual_biomass_potential = annual_potential
    elif potential == 'calc_fake_potential':
        annual_biomass_potential = (heat_demand_biomass +
            input_data['cap Biomass Power'] /
            input_data['eta Biomass Power'] * 5000)
    else:
        print ('Chosen biomass_pot is not valid.')

    return annual_biomass_potential


def infeasible_biogas_pot(type_of_use, hourly_biogas_pot, cap_biogas):
    '''
    Checks if the hourly biogas potential exceeds the maximum amount of biogas
    that can be used. A potential exceeding the maximum amount of biogas that
    can be used leads to an infeasible problem definition (in model.py).
    '''
    if hourly_biogas_pot[type_of_use] > cap_biogas[type_of_use]:
        hourly_biogas_pot[type_of_use + '_infeasible'] = \
            hourly_biogas_pot[type_of_use]
        hourly_biogas_pot[type_of_use] = cap_biogas[type_of_use]
        print (('The %s potential exceeds the max. amount that can be used.'
            % type_of_use + '\n' +
            'Old pot.: %s' % hourly_biogas_pot[type_of_use + '_infeasible'] +
            '\n' +
            'New pot.: %s' % hourly_biogas_pot[type_of_use]))
    return hourly_biogas_pot


def split_biogas_potential(input_data, hourly_biogas_pot):
    '''
    If biogas is used in central heat supply and decentralized cogeneration
    units, the biogas potential of the region must be devided between those
    two.
    '''
    # check for central and decentralized components using biogas
    central = []
    dec = []
    #if input_data['Heat source DH Biogas Heat'] == 'yes':
        #central.append('DH Biogas Heat')
    if input_data['Cog source DH Biogas Cog unit'] == 'yes':
        central.append('DH Biogas Cog unit Power')
    if input_data['Heat source Biogas Cog unit'] == 'yes':
        dec.append('Biogas Cog unit Power')

    # calculate maximum amount of biogas that can be used
    cap_biogas = {}
    cap_biogas['dec'] = 0
    for comp in dec:
        cap_biogas['dec'] += (input_data['cap ' + comp] /
            input_data['eta ' + comp])
    cap_biogas['central'] = 0
    for comp in central:
        cap_biogas['central'] += (input_data['cap ' + comp] /
            input_data['eta ' + comp])

    # assign biogas potential
    hourly_biogas_potential = {}
    if len(central) == 0:
        hourly_biogas_potential['central'] = None
        if len(dec) == 0:
            hourly_biogas_potential['dec'] = None
        else:
            hourly_biogas_potential['dec'] = hourly_biogas_pot
            hourly_biogas_potential = infeasible_biogas_pot(
                'dec', hourly_biogas_potential, cap_biogas)
    else:
        if len(dec) == 0:
            hourly_biogas_potential['dec'] = None
            hourly_biogas_potential['central'] = hourly_biogas_pot
            hourly_biogas_potential = infeasible_biogas_pot(
                'central', hourly_biogas_potential, cap_biogas)
        else:
            # if biogas is used in both central and decentralized components
            # the potential is devided according to the biogas input needed
            # calc factor
            factor_dec = cap_biogas['dec'] / (cap_biogas['central'] +
                cap_biogas['dec'])
            factor_central = cap_biogas['central'] / (cap_biogas['central'] +
                cap_biogas['dec'])
            # assign potential
            hourly_biogas_potential['dec'] = factor_dec * hourly_biogas_pot
            hourly_biogas_potential = infeasible_biogas_pot(
                'dec', hourly_biogas_potential, cap_biogas)
            hourly_biogas_potential['central'] = factor_central * \
                hourly_biogas_pot
            hourly_biogas_potential = infeasible_biogas_pot(
                'central', hourly_biogas_potential, cap_biogas)

    return hourly_biogas_potential