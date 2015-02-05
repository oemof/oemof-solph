#!/usr/bin/python
# -*- coding: utf-8
import numpy as np
import postgresql_db as db
import geoplot_one_column_expert as gpe

db_dic = {'ip': '192.168.10.25',
    'db': 'reiners_db',
    'user': 'wittenberg',
    'password': 'luTHer'}

#proj = 'mill'

text_coord = np.array([
    [13.00, 51.70],  # Annaburg
    [12.73, 51.70],  # Bad Schmiedeberg
    [12.43, 51.95],  # Coswig (Anhalt)
    [12.53, 51.69],  # Gräfenhainichen
    [13.00, 51.82],  # Jessen (Elster)
    [12.60, 51.77],  # Kemberg
    [12.65, 51.90],  # Lutherstadt Wittenberg
    [12.40, 51.83],  # Oranienbaum-Wörlitz
    [12.80, 51.88],  # Zahna-Elster
    ])

parameter_dict = {
    'db_schema': 'wittenberg',
    'db_view': 'ortsdaten',
    'db_table': 'ortsbezogene_daten',
    'db_geo_table': 'gemeinden_ohne_lk',
    'db_geo_column': 'the_geom',
    'db_base_column': None,  # None, 'Einwohner',
    'save_file_folder': 'bilder',
    'save_file_type': 'png',
    'save_file_res': 150,
    'save_file_name': 'test',
    'save_file': True,
    'show_plot': False,
    'plot_line_width': 1,
    'plot_fontsize': 15,
    'plot_text_coord': text_coord,
    'plot_values': True,
    'map_projection': 'merc',
    'map_resolution': 'i',
    'map_coordinates': np.array([[12.2, 51.6], [13.2, 52.05]]),
    'map_grid_parts': 0.2,
    'data_column': 'pv_p_nenn',
    'maxvalue': 9,
    'color_map': 'Greens',
    'title': 'Installierte PV-Leistung im Landkreis Wittenberg',
    'legendlable': 'Installierte PV-Leistung in MW',
    'unit_adaptation': 10 ** (-3),
    'table_from': 'flaechen_alle',
    'value_column': 'aliasart',
    'where_column': 'aliasfolie',
    'where_name': 'Vegetationsflächen',
    'table_to': 'ortsbezogene_daten',
    'table_shp': 'gemeinden',
    'polygon_name_column': 'stadtname'
    }

#TODO: understanding TODOs

conn = db.connect2db(db_dic)
cur = conn.cursor()
cur.execute('''
CREATE OR REPLACE VIEW %s.%s AS
 SELECT o.*, g.%s
   FROM %s.%s g
   JOIN %s.%s o ON g.ags::text = o.ags::text;
''' % (parameter_dict['db_schema'], parameter_dict['db_view'],
    parameter_dict['db_geo_column'], parameter_dict['db_schema'],
    parameter_dict['db_geo_table'], parameter_dict['db_schema'],
    parameter_dict['db_table']))
db.close_db(cur, conn, commit=True)

################## Werte pro Einwohner:
parameter_dict['db_base_column'] = 'Einwohner'
parameter_dict['legendlable'] = 'Windkraftpotenzial [kW/Einwohner]'
parameter_dict['data_column'] = 'wea_potenzial'
parameter_dict['color_map'] = 'Blues'
parameter_dict['maxvalue'] = 10
parameter_dict['unit_adaptation'] = 10 ** 3
parameter_dict['save_file_name'] = 'vr_wind_EW'
#parameter_dict['title'] = 'Windkraftpotenzial pro EW in Wind Vorranggebieten'
parameter_dict['title'] = ''
print ((parameter_dict['title']))
gpe.create_map_plot(db_dic, parameter_dict)

parameter_dict['legendlable'] = \
    'PV-Potenzial [kWp/Einwohner] (17% Wirkungsgrad)'
parameter_dict['data_column'] = 'pv_potenzial'
parameter_dict['color_map'] = 'Reds'
parameter_dict['maxvalue'] = 7
parameter_dict['unit_adaptation'] = 1 * 170 * 10 ** -3
parameter_dict['save_file_name'] = 'pv_dachanlagen_EW'
parameter_dict['title'] = ''
#parameter_dict['title'] = 'PV-Potenzial pro EW: PV Dachanlagen'
print ((parameter_dict['title']))
gpe.create_map_plot(db_dic, parameter_dict)

#parameter_dict['legendlable'] = 'Energiepotenzial MWh/Einwohner'
#parameter_dict['data_column'] = 'holz_potenzial'
#parameter_dict['color_map'] = 'Greens'
#parameter_dict['maxvalue'] = 2.5
#parameter_dict['unit_adaptation'] = 1
#parameter_dict['save_file_name'] = 'holzpotenzial_EW'
#parameter_dict['title'] = 'Energiepotenzial pro EW: Holz'
#print ((parameter_dict['title']))
#gpe.create_map_plot(db_dic, parameter_dict)

#parameter_dict['legendlable'] = 'Energiepotenzial MWh/Einwohner'
#parameter_dict['data_column'] = 'biogas_potenzial'
#parameter_dict['color_map'] = 'Greens'
#parameter_dict['maxvalue'] = 5
#parameter_dict['unit_adaptation'] = 1
#parameter_dict['save_file_name'] = 'biogas_potenzial_EW'
#parameter_dict['title'] = 'Energiepotenzial pro EW: Biogas'
#print ((parameter_dict['title']))
#gpe.create_map_plot(db_dic, parameter_dict)

################## absolute Werte:
parameter_dict['db_base_column'] = None
parameter_dict['legendlable'] = 'Windkraftpotenzial [MW]'
parameter_dict['data_column'] = 'wea_potenzial'
parameter_dict['color_map'] = 'Blues'
parameter_dict['maxvalue'] = 100
parameter_dict['unit_adaptation'] = 1
parameter_dict['save_file_name'] = 'vr_wind'
#parameter_dict['title'] = 'Windkraftpotenzial in Wind Vorranggebieten'
print ((parameter_dict['title']))
gpe.create_map_plot(db_dic, parameter_dict)

parameter_dict['legendlable'] = 'PV-Potenzial [MWp] (bei 17 % Wirkungsgrad)'
parameter_dict['data_column'] = 'pv_potenzial'
parameter_dict['color_map'] = 'Reds'
parameter_dict['maxvalue'] = 180
parameter_dict['unit_adaptation'] = 1 * 170 * 10 ** -6
parameter_dict['save_file_name'] = 'pv_dachanlagen'
#parameter_dict['title'] = 'PV-Potenzial: PV Dachanlagen'
print ((parameter_dict['title']))
gpe.create_map_plot(db_dic, parameter_dict)

#parameter_dict['legendlable'] = 'Energiepotenzial GWh'
#parameter_dict['data_column'] = 'holz_potenzial'
#parameter_dict['color_map'] = 'Greens'
#parameter_dict['maxvalue'] = 30
#parameter_dict['unit_adaptation'] = 10 ** -3
#parameter_dict['save_file_name'] = 'holzpotenzial'
#parameter_dict['title'] = 'Energiepotenzial: Holz'
#print ((parameter_dict['title']))
#gpe.create_map_plot(db_dic, parameter_dict)

##################### Anteile:
parameter_dict['legendlable'] = 'Anteil der EE an der Energieversorgung [%]'
parameter_dict['data_column'] = 'realer_anteil_ee_ist'
parameter_dict['color_map'] = 'Greens'
parameter_dict['maxvalue'] = 100
#parameter_dict['color_map'] = 'winter'
#parameter_dict['maxvalue'] = 180
parameter_dict['title'] = ''
parameter_dict['unit_adaptation'] = 1
parameter_dict['save_file_name'] = 'realer_Anteil_EE_Ist'
#parameter_dict['title'] = 'realer Anteil der EE an der Energieversorgung'
#print ((parameter_dict['title']))
gpe.create_map_plot(db_dic, parameter_dict)

#parameter_dict['legendlable'] = 'Anteil der EE an der Energieversorgung'
parameter_dict['data_column'] = 'theo_anteil_ee_ist'
#parameter_dict['color_map'] = 'Greens'
#parameter_dict['color_map'] = 'PiYG'
#parameter_dict['maxvalue'] = 120
#parameter_dict['unit_adaptation'] = 1
parameter_dict['save_file_name'] = 'theo_Anteil_EE_Ist'
#parameter_dict['title'] = 'bilanzieller Anteil der EE an der Energieversorgung'
#print ((parameter_dict['title']))
gpe.create_map_plot(db_dic, parameter_dict)

#parameter_dict['legendlable'] = 'Anteil der EE an der Energieversorgung'
parameter_dict['data_column'] = 'realer_anteil_ee_50'
#parameter_dict['color_map'] = 'PiYG'
#parameter_dict['maxvalue'] = 120
#parameter_dict['color_map'] = 'winter'
#parameter_dict['maxvalue'] = 180
#parameter_dict['unit_adaptation'] = 1
parameter_dict['save_file_name'] = 'realer_Anteil_EE_50'
#parameter_dict['title'] = ('realer Anteil der EE an der Energieversorgung' +
    #' bei einer Nutzung von 50% der EE-Potenziale')

#print ((parameter_dict['title']))
gpe.create_map_plot(db_dic, parameter_dict)

#parameter_dict['legendlable'] = 'Anteil der EE an der Energieversorgung'
parameter_dict['data_column'] = 'theo_anteil_ee_50'
#parameter_dict['color_map'] = 'Greens'
#parameter_dict['color_map'] = 'PiYG'
#parameter_dict['maxvalue'] = 120
#parameter_dict['unit_adaptation'] = 1
parameter_dict['save_file_name'] = 'theo_Anteil_EE_50'
#parameter_dict['title'] = \
    #('bilanzieller Anteil der EE an der Energieversorgung'
    #+ ' bei einer Nutzung von 50% der EE-Potenziale')
#print ((parameter_dict['title']))
gpe.create_map_plot(db_dic, parameter_dict)

#parameter_dict['legendlable'] = 'Anteil der EE an der Energieversorgung'
parameter_dict['data_column'] = 'realer_anteil_ee_100'
#parameter_dict['color_map'] = 'PiYG'
#parameter_dict['maxvalue'] = 120
#parameter_dict['color_map'] = 'winter'
#parameter_dict['maxvalue'] = 180
#parameter_dict['unit_adaptation'] = 1
parameter_dict['save_file_name'] = 'realer_Anteil_EE_100'
#parameter_dict['title'] = ('realer Anteil der EE an der Energieversorgung' +
    #' bei einer Nutzung von 100% der EE-Potenziale')
#print ((parameter_dict['title']))
gpe.create_map_plot(db_dic, parameter_dict)

#parameter_dict['legendlable'] = 'Anteil der EE an der Energieversorgung'
parameter_dict['data_column'] = 'theo_anteil_ee_100'
#parameter_dict['color_map'] = 'Greens'
#parameter_dict['color_map'] = 'PiYG'
#parameter_dict['maxvalue'] = 120
#parameter_dict['unit_adaptation'] = 1
parameter_dict['save_file_name'] = 'theo_Anteil_EE_100'
#parameter_dict['title'] = \
    #('bilanzieller Anteil der EE an der Energieversorgung'
    #+ ' bei einer Nutzung von 100% der EE-Potenziale')
#print ((parameter_dict['title']))
gpe.create_map_plot(db_dic, parameter_dict)