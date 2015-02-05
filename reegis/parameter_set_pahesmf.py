#!/usr/bin/python
# -*- coding: utf-8


def get_p_set():
    ''
    p_set = {

    'reegis_id': [1],  # id aus Parameterset, die verwendet werden soll
    'pahesmf_scenario': 'lk_wittenberg_reegis',
    'szenario': 'pahesmf',

    # output parameters
    'out_schema': 'pahesmf_dat',
    'schema': 'wittenberg',
    'load_pot_table': 'reegis_load_pot',  # Tabelle, in die die Last- und
                                          # Potenzialzeitreihen geschrieben
                                          # werden sollen
    'save': 'yes',  # sollen die Last- und Potenzialzeitreihen gespeichert
                    # werden?

    # input residential heat load profile (hlp_res)
    'hlp_res_use_case': 'db',  # db, file oder slp_generation
    'hlp_res_table': 'pahesmf_zeitreihen',  # wenn use_case='db' muss hier
                                                 # die Tabelle hin, in der das
                                                 # Lastprofil enthalten ist
    'hlp_res_column': {'EFH': 'res_heat_load_efh',
                        'MFH': 'res_heat_load_mfh'},  # Spaltenname der Spalte,
                                        # die das Lastprofil enthält
                               # (gilt für use_case='db' und use_case='file')
    'hlp_res_filename': None,  # wenn use_case='file'
                               # muss hier der Name des Files hin
    'hlp_res_directory': None,  # wenn use_case='file' muss hier der Pfad zu dem
                                # File hin
    'annual_heat_demand_res': {'EFH': 552957,
                                'MFH': 384258},

    # input residential el. load profile (elp_res)
    'elp_res_use_case': 'db',  # db, file oder slp_generation
    'elp_res_table': 'pahesmf_zeitreihen',
    'elp_res_column': 'res_el_load',
    'elp_res_filename': None,
    'elp_res_directory': None,
    'annual_el_demand_res': 191222,

    # input commercial heat load profile (hlp_com)
    'hlp_com_use_case': 'db',  # db, file oder slp_generation
    'hlp_com_table': 'pahesmf_zeitreihen',
    'hlp_com_column': 'com_heat_load',
    'hlp_com_filename': None,
    'hlp_com_directory': None,
    'annual_heat_demand_com': 408164,

    # input commercial el. load profile (elp_com)
    'elp_com_use_case': 'db',  # db, file oder slp_generation
    'elp_com_table': 'pahesmf_zeitreihen',
    'elp_com_column': 'com_el_load',
    'elp_com_filename': None,
    'elp_com_directory': None,
    'annual_el_demand_com': 61909,

    # input industrial heat load profile (hlp_ind)
    'hlp_ind_use_case': 'db',  # db, file oder slp_generation
    'hlp_ind_table': 'pahesmf_zeitreihen',
    'hlp_ind_column': 'ind_heat_load',
    'hlp_ind_filename': None,
    'hlp_ind_directory': None,
    'annual_heat_demand_ind': 1768316,

    # input industrial el. load profile (elp_ind)
    'elp_ind_use_case': 'db',  # db, file oder slp_generation
    'elp_ind_table': 'pahesmf_zeitreihen',
    'elp_ind_column': 'ind_el_load',
    'elp_ind_filename': None,
    'elp_ind_directory': None,
    'annual_el_demand_ind': 769745,

    # industrial step load profile factors
    'step_load_profile_ind_factors': {
        # factors
        'day_weekday_factor': 1,
        'day_weekend_factor': 0.875,
        'night_weekday_factor': 0.75,
        'night_weekend_factor': 0.75,
        # definition night and day
        'night_start': 19,
        'day_start': 8},

    # heat demand splitting
    'heat_source_shares': {
            'Oil': {'res_efh': 0.17,
                    'res_mfh': 0.17,
                    'com': 0.12,
                    'ind': 0.17},
            'Gas': {'res_efh': 0.5,
                    'res_mfh': 0.5,
                    'com': 0.55,
                    'ind': 0.56},
            'Biomass': {'res_efh': 0.19,
                        'res_mfh': 0.19,
                        'com': 0.01,
                        'ind': 0.18},
            'HP Mono': {'res_efh': 0.0,
                            'res_mfh': 0.0,
                            'com': 0.0,
                            'ind': 0.0},
            'DH': {'res_efh': 0.14,
                   'res_mfh': 0.14,
                   'com': 0.32,
                   'ind': 0.09},
            'Gas Cog unit': {'res_efh': 0.0,
                             'res_mfh': 0.0,
                             'com': 0.0,
                             'ind': 0.0},
            'Biogas Cog unit': {'res_efh': 0.0,
                                'res_mfh': 0.0,
                                'com': 0.0,
                                'ind': 0.0}},

    # input hourly wind potential
    'wind_pot': 'scaled',  # total, district oder scaled
    # total: berechnetes Potenzial in der Region ohne installierte Anlagen
    # district: installierte Anlagen + Ausbau (share_pot_used)
    'wind_pot_use_case': 'db',  # db, file oder calc
    'wind_pot_table': 'pahesmf_zeitreihen',
    'wind_pot_column': 'wind_pot',
    'wind_pot_file': None,
    'wind_pot_directory': None,
    'share_wind_pot_used': None,

    # input hourly pv potential
    'pv_pot': 'scaled',  # total, district oder scaled
    'pv_pot_use_case': 'db',  # db, file oder calc
    'pv_pot_table': 'pahesmf_zeitreihen',
    'pv_pot_column': 'pv_pot',
    'pv_pot_file': None,
    'pv_pot_directory': None,
    'share_pv_pot_used': None,

    # input hourly biogas potential
    'biogas_pot': 'set_value',  # set_value, district oder calc
    'share_biogas_pot_used': 1,  # 0-1
    'hourly_biogas_pot': 25,  # in MWh/h

    # input hourly biogas potential
    'biomass_pot': 'set_value',  # set_value, district oder calc
    'annual_biomass_pot': 900000  # in MWh/a
    }

    return p_set