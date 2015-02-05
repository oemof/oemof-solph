#!/usr/bin/python
# -*- coding: utf-8

import numpy as np
import database as db


def get_list_el_heating(results_table):
    '''
    Returns a list with all electrical heating components in the energy
    system.
    '''
    # electrical heating systems considered
    el_heating_sys = ['Gas el Heating', 'Oil el Heating', 'Coal el Heating',
                        'Biomass el Heating', 'DH el Heating',
                        'Gas Cog unit el Heating', 'Biogas Cog unit el Heating',
                        'ST el Heating']

    # get column names from the results table
    conn = db.open_db_connection()
    cur = conn.cursor()
    cur.execute('''SELECT column_name FROM information_schema.columns
                WHERE table_name = '%s';''' % results_table)
    colnames = np.asarray(cur.fetchall())

    # write electrical heating systems used in the model to el_heating_list
    el_heating_list = []
    for el_heating in el_heating_sys:
        if el_heating in colnames:
            el_heating_list.append(el_heating)

    return el_heating_list


def list_h_pie_plot(list_h, results_table):

    # get list with all electrical heating systems used in the model
    el_heating_sys = get_list_el_heating(results_table)

    # delete electrical heating system from list_h
    for i in list_h:
        if i[0] in el_heating_sys:
            list_h.remove(i)

    # append list entry 'Sum el Heating' if an electrical heating system
    # is used in the model
    if len(el_heating_sys) > 0:
        list_h.append(['Sum el Heating', 'blue', 'provide'])

    return list_h


def legend_dictionary():
    '''
    Dictionary für Legendeneinträge des Stackplots.
    '''
    legend_dict = {
        # Power Sources
        'DH Biogas Cog unit Power': 'Biogas-BHKW',
        'DH Biomass Cog Power': 'Biomasse-KWK',
        'DH Gas Cog unit Power': 'Erdgas-BHKW',
        'Biomass Power': 'Biomasse-Kraftwerk',
        'Gas Power': 'Erdgas-Kraftwerk',
        'PV': 'PV',
        'Wind': 'Wind',
        'El Import': 'Import',
        'Hydropower': 'Wasserkraft',
        'FEE': 'FEE',
        'Storage Battery Discharge': 'Batteriespeicherentladung',
        # HP Mono Air
        'HP Mono Air Heating': 'Luft-WP (Heizung)',
        'HP Mono Air Heating el Heating': 'Strom (Luft-WP (Heizung))',
        'HP Mono Air Heating Storage Thermal Discharge':
            u'Wärmespeicherentladung (Luft-WP (Heizung))',
        'HP Mono Air WW': 'Luft-WP (WW)',
        'HP Mono Air WW el Heating': 'Strom (Luft-WP (WW))',
        'HP Mono Air WW Storage Thermal Discharge':
            u'Wärmespeicherentladung (Luft-WP (WW))',
        # HP Mono Brine
        'HP Mono Brine Heating': 'Sole-WP (Heizung)',
        'HP Mono Brine Heating Storage Thermal Discharge':
            u'Wärmespeicherentladung (Sole-WP (Heizung))',
        'HP Mono Brine WW': 'Sole-WP (WW)',
        'HP Mono Brine WW Storage Thermal Discharge':
            u'Wärmespeicherentladung (Sole-WP (WW))',
        # Biomass Heating
        'Biomass Heat': 'Biomasse',
        'Biomass el Heating': 'Strom (Biomasseheizung)',
        'Biomass Storage Thermal Discharge':
            u'Wärmespeicherentladung (Biomasseheizung)',
        # Solarthermal Heating
        'ST Heat': u'Solarthermische Wärme',
        'ST Heat supp Gas': u'Solarth. Backup',
        'ST el Heating': 'Strom (solarth. Heizung)',
        'ST Storage Thermal Discharge':
            u'Wärmespeicherentladung (solarth. Heizung)',
        # Gas Heating
        'Gas Heat': 'Gas',
        'Gas el Heating': 'Strom (Gasheizung)',
        'Gas Storage Thermal Discharge':
            u'Wärmespeicherentladung (Gasheizung)',
        # Oil Heating
        'Oil Heat': u'Öl',
        'Oil el Heating': u'Strom (Ölheizung)',
        'Oil Storage Thermal Discharge':
            u'Wärmespeicherentladung (Ölheizung)',
        # Coal Heating
        'Coal Heat': 'Kohle',
        'Coal el Heating': 'Strom (Kohleheizung)',
        'Coal Storage Thermal Discharge':
            u'Wärmespeicherentladung (Kohleheizung)',
        # Gas Cog unit
        'Gas Cog unit Heat': 'Gas-BHKW',
        'Gas Cog unit Power': 'Gas-BHKW',
        'Gas Cog unit el Heating': 'Strom (Gas-BHKW)',
        'Gas Cog unit Storage Thermal Discharge':
            u'Wärmespeicherentl. (Gas-BHKW)',
        'Gas Cog unit Boiler': 'Spitzenkessel (Gas-BHKW)',
        # Biogas Cog unit
        'Biogas Cog unit Heat': 'Biogas-BHKW',
        'Biogas Cog unit Heat Demand': 'Biogas-BHKW',
        'Biogas Cog unit Power': 'Biogas-BHKW',
        'Biogas Cog unit el Heating': 'Strom (Biogas-BHKW)',
        'Biogas Cog unit Storage Thermal Discharge':
            u'Wärmespeicherentl. (Biogas-BHKW)',
        'Biogas Cog unit Boiler': 'Spitzenkessel (Biogas-BHKW)',
        # DH
        'DH Biogas Cog unit Heat': 'Biogas-BHKW',
        'DH Biomass Cog Heat': 'Biomasse-KWK',
        'DH Gas Cog unit Heat': 'Erdgas-BHKW',
        'DH Biogas Heat': 'Biogas-Spitzenkessel',
        'DH Gas Heat': 'Erdgas-Spitzenkessel',
        'DH el Heating': 'Stromheizung',
        'DH Thermal Storage Boiler': u'Wärmespeicher Spitzenkessel',
        'DH Storage Thermal Discharge':
            u'Wärmespeicherentladung',
        'DH Storage Thermal SoC': u'Wärmespeicher SoC',
        'DH Excess Heat': u'Abwärme',
        # misc
        'Sum el Heating': 'Stromheizungen',
        'El Heating': 'Stromheizung (jew. Heizungssystem)',
        'Sum Cog': 'KWK',
        'Heat Demand': 'Last (jew. Heizungssystem)',
        'Thermal Charge': u'Wärmespeicherbeladung',
        'Thermal Discharge': u'Wärmespeicherentladung (jew. Heizungssystem)'}

    return legend_dict


def legend_dictionary_output():

    legend_dict = {
        # Power Sources
        'DH Biogas Cog unit Power': 'FW Biogas-BHKW (Strom)',
        'DH Biomass Cog Power': 'FW Biomasse-KWK (Strom)',
        'DH Gas Cog unit Power': 'FW Erdgas-BHKW (Strom)',
        'Biomass Power': 'Biomasse-Kraftwerk',
        'Gas Power': 'Erdgas-Kraftwerk',
        'PV': 'PV-Anlagen',
        'Wind': 'Windkraftanlagen',
        'El Import': 'Stromimport',
        'Hydropower': 'Wasserkraft',
        'FEE': 'FEE',
        'Storage Battery Discharge': 'Batteriespeicherentladung',
        'Storage Battery': 'Batteriespeicher',
        # HP Mono Air
        'HP Mono Air Heating': 'Luft-WP (Heizung)',
        'HP Mono Air Heating el Heating': 'Stromheizung (Luft-WP (Heizung))',
        'HP Mono Air Heating Storage Thermal Discharge':
            'Wärmespeicherentladung (Luft-WP (Heizung))',
        'HP Mono Air Heating Storage Thermal':
            'Wärmespeicher (Luft-WP (Heizung))',
        'HP Mono Air WW': 'Luft-WP (WW)',
        'HP Mono Air WW el Heating': 'Stromheizung (Luft-WP (WW))',
        'HP Mono Air WW Storage Thermal Discharge':
            'Wärmespeicherentladung (Luft-WP (WW))',
        'HP Mono Air WW Storage Thermal':
            'Wärmespeicher (Luft-WP (WW))',
        # HP Mono Brine
        'HP Mono Brine Heating': 'Sole-WP (Heizung)',
        'HP Mono Brine Heating Storage Thermal Discharge':
            'Wärmespeicherentladung (Sole-WP (Heizung))',
        'HP Mono Brine Heating Storage Thermal':
            'Wärmespeicher (Sole-WP (Heizung))',
        'HP Mono Brine WW': 'Sole-WP (WW)',
        'HP Mono Brine WW Storage Thermal Discharge':
            'Wärmespeicherentladung (Sole-WP (WW))',
        'HP Mono Brine WW Storage Thermal':
            'Wärmespeicher (Sole-WP (WW))',
        # Biomass Heating
        'Biomass Heat': 'Biomasseheizung',
        'Biomass el Heating': 'Stromheizung (Biomasseheizung)',
        'Biomass Storage Thermal Discharge':
            'Wärmespeicherentladung (Biomasseheizung)',
        'Biomass Storage Thermal':
            'Wärmespeicher (Biomasseheizung)',
        # Solarthermal Heating
        'ST Heat': 'Solarthermische Wärme',
        'ST Heat supp Gas': 'Solarth. Backup',
        'ST el Heating': 'Strom (solarth. Heizung)',
        'ST Storage Thermal Discharge':
            'Wärmespeicherentladung (solarth. Heizung)',
        'ST Storage Thermal':
            'Wärmespeicher (solarth. Heizung)',
        # Gas Heating
        'Gas Heat': 'Gasheizung',
        'Gas el Heating': 'Stromheizung (Gasheizung)',
        'Gas Storage Thermal Discharge':
            'Wärmespeicherentladung (Gasheizung)',
        'Gas Storage Thermal':
            'Wärmespeicher (Gasheizung)',
        # Oil Heating
        'Oil Heat': 'Ölheizung',
        'Oil el Heating': 'Stromheizung (Ölheizung)',
        'Oil Storage Thermal Discharge':
            'Wärmespeicherentladung (Ölheizung)',
        'Oil Storage Thermal':
            'Wärmespeicher (Ölheizung)',
        # Coal Heating
        'Coal Heat': 'Kohleheizung',
        'Coal el Heating': 'Stromheizung (Kohleheizung)',
        'Coal Storage Thermal Discharge':
            'Wärmespeicherentladung (Kohleheizung)',
        'Coal Storage Thermal':
            'Wärmespeicher (Kohleheizung)',
        # Gas Cog unit
        'Gas Cog unit Heat': 'Gas-BHKW (Wärme)',
        'Gas Cog unit Power': 'Gas-BHKW (Strom)',
        'Gas Cog unit el Heating': 'Stromheizung (Gas-BHKW)',
        'Gas Cog unit Storage Thermal Discharge':
            'Wärmespeicherentl. (Gas-BHKW)',
        'Gas Cog unit Storage Thermal':
            'Wärmespeicher (Gas-BHKW)',
        'Gas Cog unit Boiler': 'Spitzenkessel (Gas-BHKW)',
        # Biogas Cog unit
        'Biogas Cog unit Heat': 'Biogas-BHKW (Wärme)',
        'Biogas Cog unit Power': 'Biogas-BHKW (Strom)',
        'Biogas Cog unit el Heating': 'Stromheizung (Biogas-BHKW)',
        'Biogas Cog unit Storage Thermal Discharge':
            'Wärmespeicherentl. (Biogas-BHKW)',
        'Biogas Cog unit Storage Thermal':
            'Wärmespeicher (Biogas-BHKW)',
        'Biogas Cog unit Boiler': 'Spitzenkessel (Biogas-BHKW)',
        # DH
        'DH Biogas Cog unit Heat': 'FW Biogas-BHKW (Wärme)',
        'DH Biomass Cog Heat': 'FW Biomasse-KWK (Wärme)',
        'DH Gas Cog unit Heat': 'FW Erdgas-BHKW (Wärme)',
        'DH Biogas Heat': 'FW Biogas-Spitzenkessel',
        'DH Gas Heat': 'FW Erdgas-Spitzenkessel',
        'DH el Heating': 'FW Stromheizung',
        'DH Thermal Storage Boiler': 'FW-Speicher Spitzenkessel',
        'DH Storage Thermal Discharge':
            'Fernwärmespeicherentladung',
        'DH Storage Thermal':
            'Fernwärmespeicher',
        'DH Storage Thermal SoC': 'Fernwärmespeicher SoC',
        'DH Excess Heat': 'Abwärme',
        'Sum el Heating': 'Stromheizungen',
        'Sum Cog': 'KWK',
        # Biomass Storages
        'Storage Biogas': 'Biogasspeicher',
        'Storage Biogas dec': 'dez. Biogasspeicher',
        'Storage Biomass': 'Biomassespeicher'}

    return legend_dict


def get(colnames, data):
    '''
    Prepares lists with components used in the energy system.
    '''

    nc_p = []  # number of column for electrical devices (nc_p)
    nc_h = []  # number of column for heat devices (nc_h)
    nc_h_DH = []  # number of column for heat devices in the DH system (nc_h_DH)
    cd_p = []  # color definition for electrical devices (cd_p)
    cd_h = []  # color definition for heat devices (cd_h)
    cd_h_DH = []  # color definition for heat devices in the DH system (cd_h_DH)

    # prepare list_p
    list_p = []
    list_p_total = [['Hydropower', 'lightskyblue', 'provide'],  # 0
                        ['DH Biogas Cog unit Power', 'y', 'provide'],  # 1
                        ['DH Biomass Cog Power', 'darkgreen', 'provide'],  # 2
                        ['DH Gas Cog unit Power', '0.5', 'provide'],  # 3
                        ['Biomass Power', 'g', 'provide'],  # 4
                        ['Gas Power', '0.7', 'provide'],  # 5
                        ['Gas Cog unit Power', '0.5', 'provide'],  # 6
                        ['Biogas Cog unit Power', 'y', 'provide'],  # 7
                        ['FEE', 'orange', 'provide'],  # 8
                        ['Storage Battery Discharge', 'm', 'store'],  # 9
                        ['El Import', '0.7', 'provide']]  # 10

    for source in \
    [list_p_total[i][0] for i in range(len(list_p_total))]:
        if source in colnames:
            for i in range(len(list_p_total)):
                if source == list_p_total[i][0]:
                    list_p.append(list_p_total[i])

    # prepare list_h
    list_h = []
    list_h_total = [['Biomass Heat', 'g', 'provide'],  # 0
                    ['Biomass el Heating', 'blue', 'provide'],  # 1
                    ['Biomass Storage Thermal Discharge', 'm', 'store'],  # 2
                    ['Gas Heat', '0.7', 'provide'],  # 3
                    ['Gas el Heating', 'blue', 'provide'],  # 4
                    ['Gas Storage Thermal Discharge', 'm', 'store'],  # 5
                    ['Oil Heat', '0.3', 'provide'],  # 6
                    ['Oil el Heating', 'blue', 'provide'],  # 7
                    ['Oil Storage Thermal Discharge', 'm', 'store'],  # 8
                    ['Coal Heat', 'black', 'provide'],  # 9
                    ['Coal el Heating', 'blue', 'provide'],  # 10
                    ['Coal Storage Thermal Discharge', 'm', 'store'],  # 11
                    ['HP Mono Air Heating', 'lightskyblue', 'provide'],  # 12
                    ['HP Mono Air Heating el Heating', 'blue', 'provide'],  # 13
                    ['HP Mono Air Heating Storage Thermal Discharge', 'm',
                        'store'],  # 14
                    ['HP Mono Air WW', 'pink', 'provide'],  # 15
                    ['HP Mono Air WW el Heating', 'blue', 'provide'],  # 16
                    ['HP Mono Air WW Storage Thermal Discharge', 'm',
                        'store'],  # 17
                    ['HP Mono Brine Heating', 'lightskyblue', 'provide'],  # 18
                    ['HP Mono Brine Heating Storage Thermal Discharge', 'm',
                        'store'],  # 19
                    ['HP Mono Brine WW', 'pink', 'provide'],  # 20
                    ['HP Mono Brine WW Storage Thermal Discharge', 'm',
                    'store'],  # 21
                    ['Gas Cog unit Heat', '0.5', 'provide'],  # 22
                    ['Gas Cog unit Boiler', '0.7', 'provide'],  # 23
                    ['Gas Cog unit el Heating', 'blue', 'provide'],  # 24
                    ['Gas Cog unit Storage Thermal Discharge', 'm',
                        'store'],  # 25
                    ['Biogas Cog unit Heat Demand', 'y', 'provide'],  # 26
                    ['Biogas Cog unit Boiler', '0.7', 'provide'],  # 27
                    ['Biogas Cog unit el Heating', 'blue', 'provide'],  # 28
                    ['Biogas Cog unit Storage Thermal Discharge', 'm',
                        'store'],  # 29
                    ['ST Heat', 'yellow', 'provide'],  # 30
                    ['ST Heat supp Gas', '0.7', 'provide'],  # 31
                    ['ST el Heating', 'blue', 'provide'],  # 32
                    ['ST Storage Thermal Discharge', 'm', 'store']  # 33
                    ]

    for source in \
    [list_h_total[i][0] for i in range(len(list_h_total))]:
        if source in colnames:
            for i in range(len(list_h_total)):
                if source == list_h_total[i][0]:
                    list_h.append(list_h_total[i])

    # prepare list_h_DH
    list_h_DH = []
    list_h_DH_total = [['DH Biogas Cog unit Heat', 'y', 'provide'],
                    ['DH Biomass Cog Heat', 'darkgreen', 'provide'],
                    ['DH Gas Cog unit Heat', '0.5', 'provide'],
                    ['DH Biogas Heat', 'yellowgreen', 'provide'],
                    ['DH Gas Heat', '0.7', 'provide'],
                    ['DH el Heating', 'blue', 'provide'],
                    ['DH Thermal Storage Boiler', 'purple', 'provide'],
                    ['DH Storage Thermal Discharge', 'm', 'store'],
                    ['DH Excess Heat', 'purple', 'provide']]

    for source in \
    [list_h_DH_total[i][0] for i in range(len(list_h_DH_total))]:
        if source in colnames:
            for i in range(len(list_h_DH_total)):
                if source == list_h_DH_total[i][0]:
                    list_h_DH.append(list_h_DH_total[i])

    # prepare list_demand_p_legend
    list_demand_p = [['Storage Battery Charge'],  # 0
                     ['Gas el Heating'],  # 1
                     ['Oil el Heating'],  # 2
                     ['Biomass el Heating'],  # 3
                     ['Coal el Heating'],  # 4
                     ['DH el Heating'],  # 5
                     ['HP Mono Air Heating'],  # 6
                     ['HP Mono Air WW'],  # 7
                     ['HP Mono Brine Heating'],  # 8
                     ['HP Mono Brine WW'],  # 9
                     ['El'],  # 10
                     ['HP Mono Air Heating el Heating'],  # 11
                     ['HP Mono Air WW el Heating'],  # 12
                     ['Gas Cog unit el Heating'],  # 13
                     ['ST el Heating'],  # 14
                     ['Biogas Cog unit el Heating']]  # 15

        # combine heat pump legend entries
    list_demand_p_legend = [["Elec. Demand", 'r', 'Stromlast']]
    if 'HP Mono Air Heating' in colnames \
    or 'HP Mono Air WW' in colnames \
    or 'HP Mono Brine Heating' in colnames \
    or 'HP Mono Brine WW' in colnames:
        list_demand_p_legend.append(["Heat Pump", 'darkred',
            u'Wärmepumpe'])

        # combine electrical heating legend entries
    if 'Gas el Heating' in colnames or 'Oil el Heating' in colnames or \
    'Biomass el Heating' in colnames or 'DH el Heating' in colnames or \
    'Coal el Heating' in colnames or 'Gas Cog unit el Heating' in colnames or \
    'ST el Heating' in colnames or 'Biogas Cog unit el Heating' in colnames:
        list_demand_p_legend.append(["Elec. Heating", 'blue', 'Stromheizung'])
    if 'Storage Battery Charge' in colnames:
        list_demand_p_legend.append(["Battery Charge", 'k',
            'Batteriespeicherbeladung'])

    # prepare list_demand_h_legend
    list_demand_h = [['Biomass Storage Thermal Charge', 'k'],  # 0
                     ['Biomass', 'r'],  # 1
                     ['Gas Storage Thermal Charge', 'k'],  # 2
                     ['Gas', 'r'],  # 3
                     ['Oil Storage Thermal Charge', 'k'],  # 4
                     ['Oil', 'r'],  # 5
                     ['Coal Storage Thermal Charge', 'k'],  # 6
                     ['Coal', 'r'],  # 7
                     ['HP Mono Air Heating Storage Thermal Charge', 'k'],  # 8
                     ['HP Mono Air Heating', 'r'],  # 9
                     ['HP Mono Air WW Storage Thermal Charge', 'k'],  # 10
                     ['HP Mono Air WW', 'r'],  # 11
                     ['HP Mono Brine Heating Storage Thermal Charge',
                         'k'],  # 12
                     ['HP Mono Brine Heating', 'r'],  # 13
                     ['HP Mono Brine WW Storage Thermal Charge', 'k'],  # 14
                     ['HP Mono Brine WW', 'r'],  # 15
                     ['Gas Cog unit Storage Thermal Charge', 'k'],  # 16
                     ['Gas Cog unit', 'r'],  # 17
                     ['Biogas Cog unit Storage Thermal Charge', 'k'],  # 18
                     ['Biogas Cog unit', 'r'],  # 19
                     ['ST Storage Thermal Charge', 'k'],  # 20
                     ['ST', 'r']]  # 21

        # combine storage charge legend entries
    list_demand_h_legend = \
        [['Heat Demand', 'r', 'Last (jew. Heizungssystem)']]
    if 'Biomass Storage Thermal Charge' in colnames or \
    'Gas Storage Thermal Charge' in colnames or \
    'Oil Storage Thermal Charge' in colnames or \
    'Coal Storage Thermal Charge' in colnames or \
    'HP Mono Air WW Storage Thermal Charge' in colnames or \
    'HP Mono Air Heating Storage Thermal Charge' in colnames or \
    'HP Mono Brine WW Storage Thermal Charge' in colnames or \
    'HP Mono Brine Heating Storage Thermal Charge' in colnames or \
    'Gas Cog unit Storage Thermal Charge' in colnames or \
    'Biogas Cog unit Storage Thermal Charge' in colnames or \
    'ST Storage Thermal Charge' in colnames:
        list_demand_h_legend.append(['Thermal Charge', 'k',
            u'Wärmespeicherbeladung'])

    # prepare list_demand_h_DH_legend
    list_demand_h_DH = [['DH', 'r'],
                    ['DH Storage Thermal Charge', 'k']]

    list_demand_h_DH_legend = [['Heat Demand', 'r', u'Wärmelast']]
    list_thermal_storage_soc = []
    if 'DH Storage Thermal Charge' in colnames:
        list_demand_h_DH_legend.append(['Thermal Charge', 'k',
            u'Wärmespeicherbeladung'])
        list_thermal_storage_soc.append(['Thermal Storage SoC', 'b',
            u'Wärmespeicher SoC'])

    # get dictionary for legend
    legend_dict = legend_dictionary()

    ########################### prepare stack plots #########################

    for j in list_p:
        tmp = ([i for i, x in enumerate(colnames) if x == j[0]])
        nc_p.append(tmp[0])  # number of column (nc)
        cd_p.append(j[1])  # color definition (cd)

    for j in list_h:
        tmp = ([i for i, x in enumerate(colnames) if x == j[0]])
        nc_h.append(tmp[0])  # number of column (nc)
        cd_h.append(j[1])  # color definition (cd)

    for j in list_h_DH:
        tmp = ([i for i, x in enumerate(colnames) if x == j[0]])
        nc_h_DH.append(tmp[0])  # number of column (nc)
        cd_h_DH.append(j[1])  # color definition (cd)

    # data columns to be stacked in the bar plot
    cols_p = np.array(nc_p)
    cols_h = np.array(nc_h)
    cols_h_DH = np.array(nc_h_DH)

    # Define legend names
    legend_p_temp = (np.array(colnames[cols_p]).reshape(-1,).tolist())
    legend_p = []
    for i in legend_p_temp:
        legend_p.append(legend_dict[i])
    for l in range(len(list_demand_p_legend)):
        legend_p.extend(list_demand_p_legend[l][2:3])
    legend_h_temp = (np.array(colnames[cols_h]).reshape(-1,).tolist())
    legend_h = []
    for i in legend_h_temp:
        legend_h.append(legend_dict[i])
    for l in range(len(list_demand_h_legend)):
        legend_h.extend(list_demand_h_legend[l][2:3])
    legend_h_DH_temp = (np.array(colnames[cols_h_DH]).reshape(-1,).tolist())
    legend_h_DH = []
    for i in legend_h_DH_temp:
        legend_h_DH.append(legend_dict[i])
    for l in range(len(list_demand_h_DH_legend)):
        legend_h_DH.extend(list_demand_h_DH_legend[l][2:3])
    for l in range(len(list_thermal_storage_soc)):
        legend_h_DH.extend(list_thermal_storage_soc[l][2:3])

    return (cols_p, cols_h, cols_h_DH, cd_p, cd_h, cd_h_DH,
        list_p, list_h, list_h_DH,
        list_demand_p, list_demand_h, list_demand_h_DH,
        legend_p, legend_h, legend_h_DH,
        list_demand_p_legend, list_demand_h_legend, list_demand_h_DH_legend)


def modify_legend(entry_orig, ls_names_orig):
    '''
    Deletes
    '''
    # copy original lists to new lists
    entry = list(entry_orig)
    ls_names = list(ls_names_orig)

    # get legend_dict
    legend_dict = legend_dictionary()

    el_heating = None
    thermal_storage = None

    for i in ls_names_orig:

        # find key for i
        key = legend_dict.keys()[legend_dict.values().index(i)]

        # if the key contains 'el Heating' it is an electrical heating system
        if 'el Heating' in key:

            # if el heating legend entry does not yet exist
            if not el_heating:
                # alter name in ls_names
                ls_names[ls_names.index(i)] = legend_dict['El Heating']
                el_heating = 1

            # if el heating legend entry does already exist
            else:
                # delete from entry list
                entry.remove(entry_orig[ls_names_orig.index(i)])
                # delete from ls_names
                ls_names.remove(i)

        # if the key contains 'Discharge' it is a Thermal Storage
        if 'Discharge' in key:

            # if thermal storage legend entry does not yet exist
            if not thermal_storage:
                # alter name in ls_names
                ls_names[ls_names.index(i)] = legend_dict['Thermal Discharge']
                thermal_storage = 1

            # if thermal_storage legend entry does already exist
            else:
                # delete from entry list
                entry.remove(entry_orig[ls_names_orig.index(i)])
                # delete from ls_names
                ls_names.remove(i)

    return entry, ls_names