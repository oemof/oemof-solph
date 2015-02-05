#!/usr/bin/python
# -*- coding: utf-8

import datetime


def get_p_set():

    p_set = {

    'project_id': [77],  # id aus Parameterset, die verwendet werden soll
    'szenario': 'capacity variation',
    'optimize_for': 'CO2',  # 'Costs' or 'CO2' (default)
    'cap_pv': [119],  # installierte PV-Leistung
    'cap_pv_ground': [65.1],  # installierte PV-Leistung Freiflächenanlagen
    'cap_wind': [209.8],  # installierte Windleistung
    'cap_wind_current': [209.8],  # installierte Windleistung
                                  # (bestehende Anlagen)

    # output parameters
    'schema': 'wittenberg',
    'output_table': 'results_77_ist',  # Tabelle, in die die Opt.ergebnisse
                                       # geschrieben werden sollen
    'load_pot_table': 'load_pot_77',  # Tabelle, in die die Last- und
                                          # Potenzialzeitreihen geschrieben
                                          # werden sollen
    'output_dir_path': '/home/likewise-open/RL-INSTITUT/birgit.schachler/',
    'date': datetime.datetime.now().strftime("%Y%m%d"),  # Datum für
                                                           # Output-File
    'export_output_table': 'yes',  # sollen Optimierungszeitreihen als
                                    # .txt abgespeichert werden? (yes/no)
    'export_load_pot_table': 'yes',  # sollen die Last- und Potenzialzeitreihen
                                     # als .txt abgespeichert werden? (yes/no)
    'counter': 1,  # Output-File-Zusatz
    'hoy': 8760,  # Anzahl der Stunden, die gerechnet werden sollen
    'show': False,  # sollen die Grafiken angezeigt werden?
    'save': 'yes',  # sollen die Last- und Potenzialzeitreihen gespeichert
                    # werden?
    'solver_message': 1,  # 0 (aus) oder 1 (an)

    # input residential heat load profile (hlp_res)
    'hlp_res_use_case': 'slp_generation',  # db, file oder slp_generation
    'hlp_res_table': None,  # wenn use_case='db' muss hier
                                                 # die Tabelle hin, in der das
                                                 # Lastprofil enthalten ist
    'hlp_res_column': {'EFH': None,
                        'MFH': None},  # Spaltenname der Spalte,
                                        # die das Lastprofil enthält
                               # (gilt für use_case='db' und use_case='file')
    'hlp_res_filename': None,  # wenn use_case='file'
                               # muss hier der Name des Files hin
    'hlp_res_directory': None,  # wenn use_case='file' muss hier der Pfad zu dem
                                # File hin
    'annual_heat_demand_res': {'EFH': 482285,  # MWh/a
                                'MFH': 210319},  # MWh/a

    # input residential el. load profile (elp_res)
    'elp_res_use_case': 'slp_generation',  # db, file oder slp_generation
    'elp_res_table': None,
    'elp_res_column': None,
    'elp_res_filename': None,
    'elp_res_directory': None,
    'annual_el_demand_res': 181034,  # MWh/a

    # input commercial heat load profile (hlp_com)
    'hlp_com_use_case': 'slp_generation',  # db, file oder slp_generation
    'hlp_com_table': None,
    'hlp_com_column': None,
    'hlp_com_filename': None,
    'hlp_com_directory': None,
    'annual_heat_demand_com': 300098,  # MWh/a

    # input commercial el. load profile (elp_com)
    'elp_com_use_case': 'slp_generation',  # db, file oder slp_generation
    'elp_com_table': None,
    'elp_com_column': None,
    'elp_com_filename': None,
    'elp_com_directory': None,
    'annual_el_demand_com': 92692,  # MWh/a

    # input industrial heat load profile (hlp_ind)
    'hlp_ind_use_case': 'slp_generation',  # db, file oder slp_generation
    'hlp_ind_table': None,
    'hlp_ind_column': None,
    'hlp_ind_filename': None,
    'hlp_ind_directory': None,
    'annual_heat_demand_ind': 1263395,  # MWh/a

    # input industrial el. load profile (elp_ind)
    'elp_ind_use_case': 'slp_generation',  # db, file oder slp_generation
    'elp_ind_table': None,
    'elp_ind_column': None,
    'elp_ind_filename': None,
    'elp_ind_directory': None,
    'annual_el_demand_ind': 1137344,  # MWh/a

    # industrial step load profile factors
    'step_load_profile_ind_factors': {
        # factors
        'day_weekday_factor': 1,
        'day_weekend_factor': 0.65,
        'night_weekday_factor': 0.6,
        'night_weekend_factor': 0.5,
        # definition night and day
        'night_start': 22,
        'day_start': 7},

    # heat demand splitting
    'heat_source_shares': {
            'Oil': {'res_efh': 0.1580,
                    'res_mfh': 0.1621,
                    'com': 0.1101,
                    'ind': 0.0267},
            'Gas': {'res_efh': 0.4184,
                    'res_mfh': 0.4685,
                    'com': 0.8020,
                    'ind': 0.6156},
            'Biomass': {'res_efh': 0.1720,
                        'res_mfh': 0.1765,
                        'com': 0.0115,
                        'ind': 0.0466},
            'Gas Cog unit': {'res_efh': 0.0,
                        'res_mfh': 0.0036,
                        'com': 0.0075,
                        'ind': 0.0},
            'Biogas Cog unit': {'res_efh': 0.0,
                        'res_mfh': 0.0,
                        'com': 0.0105,
                        'ind': 0.0},
            'HP Mono': {'res_efh': 0.0254,
                        'res_mfh': 0.0,
                        'com': 0.0,
                        'ind': 0.0},
            'DH': {'res_efh': 0.1376,
                   'res_mfh': 0.1412,
                   'com': 0.0569,
                   'ind': 0.2761},
            'Coal': {'res_efh': 0.0254,
                     'res_mfh': 0.0261,
                     'com': 0.0015,
                     'ind': 0.0351},
            'ST': {'res_efh': 0.0632,
                   'res_mfh': 0.0220,
                   'com': 0.0,
                   'ind': 0.0}},

    # share of different district heating systems
    'DH systems': {'Gas': 0.22,
                   'Gas Cog unit': 0.78},

    # refurbishment state
    'ref_state': {'EFH': {'fully ref': 0.32,
                          'partially ref': 0.55,
                          'unrenovated': 0.13},
                  'MFH': {'fully ref': 0.32,
                          'partially ref': 0.55,
                          'unrenovated': 0.13}},

    # solar heat
    'st_share_ww_only': {'EFH': 0.4,  # Anteil der Systeme die nur zur WW-
                         'MFH': 0.4},  # Erzeugung genutzt werden
    'share_new_buildings': 0.3,  # share of new buildings of fully refurbished
                                 # buildings
             # (here the difference between new buildings and fully ref. ones
             # is the supply temp. of 35 °C and 55 °C respectively)

    # input hourly wind potential
    'wind_pot': 'scaled_mixed',  # total, district, scaled oder scaled_mixed
        # (Zeitreihe bestehender Anlagen und zukünftig gebauter Anlagen
        # wird berücksichtigt)
    # total: berechnetes Potenzial in der Region ohne installierte Anlagen
    # district: installierte Anlagen + Ausbau (share_pot_used)
    'wind_pot_use_case': 'calc',  # db, file oder calc
    'wind_pot_table': None,
    'wind_pot_column': None,
    'wind_pot_file': None,
    'wind_pot_directory': None,
    'share_wind_pot_used': None,

    # input hourly pv potential
    'pv_pot': 'scaled_mixed',  # total, district, scaled oder scaled_mixed
        # (verschiedene Ausrichtungen der PV-Anlagen werden berücksichtigt)
    'pv_pot_use_case': 'calc',  # db, file oder calc
    'pv_pot_table': None,
    'pv_pot_column': None,
    'pv_pot_file': None,
    'pv_pot_directory': None,
    'share_pv_pot_used': None,

    # input hourly hydropwer potential
    'hourly_hydropower_pot': 0.01,  # in MWh/h
    'cap_hydropower': 0.016,  # in MW

    # input hourly biogas potential
    'biogas_pot': 'set_value',  # set_value, district oder calc
    'share_biogas_pot_used': None,  # 0-1
    'hourly_biogas_pot': 23.48,  # in MWh/h

    # input annual biomass potential
    'biomass_pot': 'set_value',  # set_value, district oder calc
    'annual_biomass_pot': 536112,  # in MWh/a

    # plot
    'stackplot_name_winter': 'stack_winter',
    'stackplot_name_summer': 'stack_summer',
    'week_summer': 20,
    'week_winter': 1,
    'pie_h_name': 'pie_h',
    'pie_p_name': 'pie_p'
    }

    # output_dir für main_1
    p_set['output_dir'] = (p_set['output_dir_path'] + p_set['date'] + '_ID_' +
        str(p_set['project_id'][0]) + '_' + str(p_set['counter']))
    ## output_dir für main
    #p_set['output_dir_tmp'] = (p_set['output_dir_path'] + p_set['date'] +
        #'_Sz_0_' + 'CO2_')

    return p_set