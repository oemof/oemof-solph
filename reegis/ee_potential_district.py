#!/usr/bin/python
# -*- coding: utf-8

import database as db
from math import ceil


def wind_potential(district, scaled_wind_potential, share_pot_used):

    conn = db.open_db_connection()
    cur = conn.cursor()

    # existing capacity [MW]
    cur.execute('''
        select wea_p_nenn
        from wittenberg.ortsbezogene_daten
        where stadtname = %(district)s
        ''', {'district': district})
    existing_wind_cap = cur.fetchone()[0]

    # total potential [MW] (includes existing capacities)
    cur.execute('''
        select wea_potenzial
        from wittenberg.ortsbezogene_daten
        where stadtname = %(district)s
        ''', {'district': district})
    wind_pot = cur.fetchone()[0]

    cur.close()
    conn.close()

    # residual potential [MW]
    res_wind_pot = wind_pot - existing_wind_cap

    # hourly wind potential used in model
    hourly_wind_pot = ((existing_wind_cap + res_wind_pot * share_pot_used)
        * scaled_wind_potential)

    return hourly_wind_pot


def pv_potential(input_data, scaled_pv_potential, share_pot_used):

    # ANMERKUNG: Bestehende Freiflächenanlagen werden hier vom Dachpotenzial
    # mit abgezogen. Langfristig mal rausfinden, wie viel der installierten
    # Kapazität Freiflächenanlagen sind.

    conn = db.open_db_connection()
    cur = conn.cursor()

    # existing capacity [MW]
    cur.execute('''
        select pv_p_nenn
        from wittenberg.ortsbezogene_daten
        where stadtname = %(district)s
        ''', {'district': input_data['district']})
    existing_pv_cap = cur.fetchone()[0]

    # total potential [m²] (includes existing capacities)
    cur.execute('''
        select pv_potenzial
        from wittenberg.ortsbezogene_daten
        where stadtname = %(district)s
        ''', {'district': input_data['district']})
    pv_pot_area = cur.fetchone()[0]

    cur.close()
    conn.close()

    # total potential [MW]
    pv_pot = input_data['eta PV'] * pv_pot_area / 1000

    # residual potential [MW]
    res_pv_pot = pv_pot - existing_pv_cap

    # hourly pv potential used in model
    hourly_pv_pot = ((existing_pv_cap + res_pv_pot * share_pot_used)
        * scaled_pv_potential)

    return hourly_pv_pot


def biogas_potential(input_data, share_pot_used):

    # assumption for biogas cogeneration units in Landkreis Wittenberg
    full_load_hours = 5700

    conn = db.open_db_connection()
    cur = conn.cursor()

    # existing capacity [MW]
    cur.execute('''
        select biogas_p_nenn
        from wittenberg.ortsbezogene_daten
        where stadtname = %(district)s
        ''', {'district': input_data['district']})
    existing_biogas_cap = cur.fetchone()[0]

    # total potential [MWh] (includes existing capacities)
    cur.execute('''
        select biogas_potenzial
        from wittenberg.ortsbezogene_daten
        where stadtname = %(district)s
        ''', {'district': input_data['district']})
    biogas_pot_energy = cur.fetchone()[0]
    cur.close()
    conn.close()

    # residual energy [MWh]
    res_biogas_pot = biogas_pot_energy - existing_biogas_cap * full_load_hours

    # hourly biogas potential used in model
    annual_biogas_pot = (existing_biogas_cap * full_load_hours
        + res_biogas_pot * share_pot_used)
    hourly_biogas_pot = annual_biogas_pot / 8760

    input_data['cap DH Biogas Cog unit Power'] = \
        ceil(annual_biogas_pot / full_load_hours * 10) / 10
    input_data['cap DH Biogas Heat'] = \
        input_data['cap DH Biogas Cog unit Power']

    return hourly_biogas_pot


def biomass_potential(input_data):

    # ANMERKUNG: Biomassekraftwerk in Wittenberg produziert 157.000 MWh.
    # Damit ist bereits fast das gesamte Biomassepotenzial ausgeschöpft
    # (7.271 MWh wären noch übrig, allerdings werden für dezentrale Heizungen
    # nach Hochrechnungen 178.000 MWh benötigt...) und
    # wird daher in allen anderen Gemeinden zu Null gesetzt.

    # Berechnung restliches Potential in Wittenberg und Gemeinden

    conn = db.open_db_connection()
    cur = conn.cursor()

    ## total potential in Wittenberg [MWh] (includes existing capacities)
    #cur.execute('''
        #select holz_potenzial
        #from wittenberg.ortsbezogene_daten
        #where stadtname = 'Landkreis Wittenberg'
        #''')
    #total_biomass_pot_wb = cur.fetchone()[0]

    ## residual potential for whole Wittenberg is the total potential in
    ## Wittenberg minus the MWh produced by the biomass power plant in
    ## Lutherstadt Wittenberg
    #res_biomass_pot_wb = total_biomass_pot_wb - 157000

    ## residual potential for the other districts
    #res_biomass_pot_district = res_biomass_pot_wb / 8

    # existing capacity [MW]
    cur.execute('''
        select biomasse_kw_p_nenn
        from wittenberg.ortsbezogene_daten
        where stadtname = %(district)s
        ''', {'district': input_data['district']})
    existing_biomass_cap = cur.fetchone()[0]

    input_data['cap Biomass Power'] = existing_biomass_cap
    input_data['cap DH Biomass Cog Power'] = existing_biomass_cap

    cur.close()
    conn.close()

    full_load_hours = 8135
    annual_biomass_potential = existing_biomass_cap * full_load_hours

    return annual_biomass_potential


#input_data = {'district': 'Landkreis Wittenberg'}
#biomass_potential(input_data)
#import numpy as np

# hourly wind and pv potentials are read from the db
#conn = db.open_db_connection()
#cur = conn.cursor()

#cur.execute('''
    #select pv_pot, wind_pot
    #from wittenberg.hourly_load_and_potential
    #order by id
    #''')
#pot_profiles = np.asarray(cur.fetchall())
#cur.close()
#conn.close()

#hourly_wind_potential = pot_profiles[:, 1]
#hourly_pv_potential = pot_profiles[:, 0]
#scaled_wind_potential = hourly_wind_potential / max(hourly_wind_potential)
#scaled_pv_potential = hourly_pv_potential / max(hourly_pv_potential)

#share_pot_used = 0.5

#input_data = {'district': 'Annaburg',
            #'eta PV': 0.16}
#hourly_pv_pot = pv_potential(input_data, scaled_pv_potential, share_pot_used)
#hourly_wind_pot = wind_potential('Annaburg',
    #scaled_wind_potential, share_pot_used)
#biogas_potential(input_data, share_pot_used)
#biomass_potential(input_data)