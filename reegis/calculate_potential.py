#!/usr/bin/python
# -*- coding: utf-8

import database as db

#db_dict = {'ip': '192.168.10.25',
    #'db': 'reiners_db',
    #'user': 'wittenberg',
    #'password': 'luTHer'}

parameter_set = {
    'schema': 'wittenberg',
    'table_from': 'gebaeude',
    'set_result_column': 'gebaeude',
    'set_categories': None,
    'result_column_type': 'double precision',
    'value_column': 'aliasart',
    'where_column': 'aliasfolie',
    'where_name': 'Vegetationsflächen',
    'table_to': 'ortsbezogene_daten',
    'table_shp': 'gemeinden',
    'polygon_name_column': 'stadtname'
    }

calc_dict = {}

#Berechnung des PV-Potenzials
eignungsfaktor = 0.2  # geeignete Dachfläche bezogen auf die Gebäudegrundfläche
mobilisierungsfaktor = 0.5  # Anteil der motivierbaren Haushalte
faktor = eignungsfaktor * mobilisierungsfaktor
berechnungsstring = 'gebaeude * %s' % faktor
calc_dict['pv_potenzial'] = {}
calc_dict['pv_potenzial']['calc'] = berechnungsstring
calc_dict['pv_potenzial']['unit'] = 'm2'

#Berechnung des Wind-Potenzials
abstand_HWR = 8.0  # Abstand der Anlagen in Hauptwindrichtung (HWR)
abstand_HWR_quer = 4.0  # Abstand der Anlagen quer zur Hauptwindrichtung
d_rotor = 82.0
cap_wka = 3.02
anzahl_wka_sqkm = 1 / (abstand_HWR * abstand_HWR_quer * d_rotor ** 2)
faktor = cap_wka * anzahl_wka_sqkm
berechnungsstring = 'vr_wind * %s + wea_p_nenn' % faktor
#flaechenfaktor = 0.00002  # MW pro m2 Grundfläche (Klärle)
#berechnungsstring = 'vr_wind * %s + wea_p_nenn' % flaechenfaktor
calc_dict['wea_potenzial_neu'] = {}
calc_dict['wea_potenzial_neu']['calc'] = berechnungsstring
calc_dict['wea_potenzial_neu']['unit'] = 'MW'

#Berechnung des Holz-Potenzials
# Klärle geht von 4 MWh/ha aus, die Biomassestudie von 2 MWh/ha.
faktor = 0.000226  # MWh pro m2 Grundfläche (Biomassestudie Sachs. Anhalt 2007)
berechnungsstring = 'area_wald_forst * %s' % faktor
calc_dict['holz_potenzial'] = {}
calc_dict['holz_potenzial']['calc'] = berechnungsstring
calc_dict['holz_potenzial']['unit'] = 'MWh'

#Berechnung des Substrat-Potenzials
# Durchschnitt in Wittenberg laut Biomassestudie 2007 Ertrag 350 dt/ha.
# 4660 m3 CH4 pro ha (Wert zwischen mittlerer und schlechter Kategorie)
# Quelle: Energiepflanzen für Biogasanlagen Sachsen-Anhalt Juli 2012 (pdf)
# Energiegehalt Methan ist ca. 10 kWh pro m3
# => 46600 kWh/ha oder 4.66 kWh/m2 (Energiegehalt des Gases pro Ackerfläche)
ertragsfaktor = 0.00466  # MWh/m2 Energiegehalt des Gases pro m2 Ackerfläche
e_anteil = 10  # Prozent der für Energiepflanzen genutzten Ackerfläche
faktor = ertragsfaktor * e_anteil / 100
berechnungsstring = 'area_ackerland * %s' % faktor
calc_dict['biogas_potenzial'] = {}
calc_dict['biogas_potenzial']['calc'] = berechnungsstring
calc_dict['biogas_potenzial']['unit'] = ('MWh (Energiegehalt des Gases)' +
' bei einer Nutzung von %s Prozent der Ackerfläche für Energiepflanzen' % str(
    e_anteil))

p_set = parameter_set

for col in list(calc_dict.keys()):
    db.add_column_2_db_table(p_set['schema'], p_set['table_to'], col, 'real')
    conn = db.open_db_connection()
    cur = conn.cursor()
    cur.execute('''update %s.%s set %s=%s;''' % (p_set['schema'],
        p_set['table_to'], col, calc_dict[col]['calc']))
    conn.commit()
    cur.close()
    conn.close()
    com = 'unit: ' + calc_dict[col]['unit']
    db.write_comment(com, p_set['schema'], p_set['table_to'], col)
    print((db.read_comment(p_set['schema'], p_set['table_to'], col)))