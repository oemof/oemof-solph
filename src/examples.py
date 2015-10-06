#!/usr/bin/python3
# -*- coding: utf-8

import matplotlib.pyplot as plt
import logging
#logging.getLogger().setLevel(logging.DEBUG)
#logging.getLogger().setLevel(logging.INFO)
logging.getLogger().setLevel(logging.WARNING)
import shapely.geometry as shape
import pandas as pd
from oemof.src import db
from oemof.src import helpers
from oemof.src import models
from oemof.src import energy_weather as w
from oemof.src import energy_regions as reg
from oemof.src import energy_buildings as b

import warnings
warnings.simplefilter(action="ignore", category=RuntimeWarning)


# Plant and site parameter
site = {'module_name': 'Yingli_YL210__2008__E__',
        'module_number': 50,
        'azimuth': 0,
        'tilt': 0,
        'Area': 2,
        'TZ': '',
        'albedo': 0.2,
        'hoy': 8760,
        'h_hub': 60,
        'd_rotor': 53,
        'wka_model': 'ENERCON E 53 800',
        'h_hub_dc': {
            1: 135,
            2: 78,
            3: 98,
            4: 138,
            0: 135},
        'd_rotor_dc': {
            1: 127,
            2: 82,
            3: 82,
            4: 82,
            0: 127},
        'wka_model_dc': {
            1: 'ENERCON E 126 7500',
            2: 'ENERCON E 82 3000',
            3: 'ENERCON E 82 2300',
            4: 'ENERCON E 82 2300',
            0: 'ENERCON E 126 7500'},
        'parallelStrings': 1,
        'seriesModules': 1,
        }

define_elec_buildings = [
    {'annual_elec_demand': 2000,
     'selp_type': 'h0'},
    {'annual_elec_demand': 2000,
     'selp_type': 'g0'},
    {'annual_elec_demand': 2000,
     'selp_type': 'i0'}]

define_heat_buildings = [
    {'building_class': 11,
     'wind_class': 0,
     'annual_heat_demand': 5000,
     'shlp_type': 'efh'},
    {'building_class': 5,
     'wind_class': 1,
     'annual_heat_demand': 5000,
     'shlp_type': 'mfh'},
    {'selp_type': 'g0',
     'building_class': 0,
     'wind_class': 1,
     'annual_heat_demand': 3000,
     'shlp_type': 'ghd'}]

year = 2010
# for the electric profile of entsoe years from 2006 to 2011
# do exist in the example data
# (and only for Germany), more countries are in old oemof's database


conn = db.connection()

# ***** 1. BEISPIEL *****

# Region wird Initialisiert (2 Varianten)

# Variante 1 - Bounding-Box mit fossilen Kraftwerken
geo = shape.Polygon([(12.2, 52.2), (12.2, 51.6), (13.2, 51.6), (13.2, 52.2)])

# Variante 2 - Landkreis Wittenberg (dort gibt es keine fossilen Kraftwerke)
#geo = helpers.get_polygon_from_shp_file('/home/uwe/Wittenberg.shp')

# Variante 3 - Landkreis Wittenberg und Dessau aus der Datenbank
# geo = helpers.get_polygon_from_nuts(conn, ['DEE0E', 'DEE01'])

#try:
#    lk_wtb = reg.region(year, geometry=geo, name='Landkreis Wittenberg')
#except:
#    lk_wtb = reg.region(year, geometry=geo, name='Landkreis Wittenberg',
#                        place=['Deutschland', 'ST'])
#    logging.error('Reverse geocoding does not work!')

lk_wtb = reg.region(year, geometry=geo)
lk_wtb.fetch_demand_series(method='csv',
                         path='/home/caro/rlihome/Git/oemof/src/',
                         filename='example_data_entsoe.csv')

lk_wtb_2 = reg.region(year, geo)
lk_wtb_2.fetch_demand_series(method='db', conn=conn)

lk_wtb_3 = reg.region(year, geo)
lk_wtb_3.fetch_demand_series(method='scale_profile_csv',
                         path='/home/caro/rlihome/Git/oemof/src/',
                         filename='example_data_entsoe.csv',
                         ann_el_demand=3000)

lk_wtb_4 = reg.region(year, geo)
lk_wtb_4.fetch_demand_series(method='scale_profile_db',
                         conn=conn)

lk_wtb_5 = reg.region(year, geo)
lk_wtb_5.fetch_demand_series(method='scale_entsoe',
                         conn=conn)

lk_wtb_6 = reg.region(year, geo)
lk_wtb_6.fetch_demand_series(method='calculate_profile')

# Die Region holt sich ihr Wetter
lk_wtb.fetch_weather_raster(conn)

# Die Region holt sich ihre Feedin-Zeitreihen
lk_wtb.fetch_ee_feedin(conn, **site)

# Jetzt möchte ich die feedin-Reihen auch mal sehen
lk_wtb.feedin.plot(title='Wind- und PV-Einspeisung')
plt.show()

# Und die Jahressummen, um sie mal mit reegis zu vergleichen
print('Jahressummen')
print(lk_wtb.feedin.sum())
print('')

# Region zur Überprüfung angucken. Und eine roten Centroid plotten.
lk_wtb.plot()  # Plottbefehl für das Regionen-Objekt
plt.plot(lk_wtb.centroid().x, lk_wtb.centroid().y, 'x', color='r')
plt.show()

# Regionsinformation auslesen
print("Bundesland {0} in {1}.".format(lk_wtb.state, lk_wtb.country))

# Damit das Wetterobjekt auf die Ortszeit bezogen ist, kennt das Wetter seine
# Zeitzone. Diese kann auch ausgelesen werden. Dafür könnte ein Wetterobjekt
# erstellt werden. Allerdings hat die Region bereits ihr eigenes Wetterobjekt.
# Dadurch kann auch dieses genutzt werden.
print("Wir sind in der Zeitzone: {0}".format(lk_wtb.weather.tz))

# Natürlich kann ich auch ein neues Wetterobjekt erstellen und dort die
# Zeitzone direkt auslesen.
wetter = w.Weather(conn, lk_wtb.geometry, 2010)
print("Nochmal Zeizone: {0}".format(wetter.tz))

# Jetzt würde ich gerne mal sehen wie unterschiedlich der Wind an den
# verschiedenen Messstellen weht. Dazu nutze ich das eben erstellte Wetterobj.
wetter.grouped_by_datatype()['WSS_10M'].plot(
    title='Windgeschwindigkeiten mit Geo-ID des Datenpunktes')
plt.show()

# Natürlich kann ich dafür auch wieder über die Region gehen (hier: Temperatur)
df_temp = lk_wtb.weather.grouped_by_datatype()['T_2M']
df_temp['average'] = lk_wtb.weather.spatial_average('T_2M')
df_temp.plot(title='Temperaturen mit Geo-ID des Datenpunktes')
plt.show()

# Um eine Feedinreihe zu erstellen, muss ich eine Windkraftanlage auswählen
# Der Type ist in dem site-Dictionary von oben angegeben.
print('')
print('Derzeitiges WKA-Modell: {0}'.format(site['wka_model']))

# Nun ist es auch möglich das Modell zu fragen, welche Typen es überhaupt hat.
# Dafür initialisiere ich das Modell "models.WindPowerPlant([])" und wende
# dann die entsprechende Methode darauf an. Das geht auch in einer Zeile.
print('Mögliche WKA-Modelle')
models.WindPowerPlant([]).get_wind_pp_types(conn)

# Erstellen der Standardlastprofile des BDEW als Objekt
# Dafür nutzen wir das DataFrame der Region, das bereits die Feiertage enthält.
e_slp = b.bdew_elec_slp(conn, lk_wtb.df)

# Das BDEW-Objekt wird jetzt immer übergeben, wenn eine Gebäudeinstant erstellt
# wird.

# Eine Möglichkeit: Sammeln aller E-Gebäudeinstanzen in einer Liste
elec_buildings = []
for building_def in define_elec_buildings:
    elec_buildings.append(b.electric_building(bdew=e_slp, **building_def))

# Danach (oder dabei): Sammeln aller Lastkurven in einem Dataframe
e_building_df = lk_wtb.df.drop(lk_wtb.df.columns[:], axis=1)
for building in elec_buildings:
    e_building_df[building.type] = building.load

# Jetzt plotten
e_building_df.plot(title='Electrical standardized load profiles')
plt.show()

# Für die Wärme wird im Unterschied zum Strom noch eine Temperaturzeitreihe
# benötigt. Die holen wird aus dem Wetterobjekt der Region. Da die Region
# nicht so groß ist wird nur ein Temperaturzeitreihe für die gesamte Region
# benutzt. Da wird eine durchschnittliche Zeitreihe erstellt

temp = lk_wtb.weather.spatial_average('T_2M')

# Sonst können wir genaus vorgehen wie oben. Als Beispiel wird diesmal
# aber etwas anders vorgegangen.
# Wenn wir z.B. nur die Last haben wollen, brauchen wir die Instanzen nicht
# mehr. Es wird also nur der Lastgang in ein  DataFrame geschrieben und die
# Instanz wieder verworfen. Übrig bleibt nur das DataFrame.

h_building_df = lk_wtb.df.drop(lk_wtb.df.columns[:], axis=1)
for building_def in define_heat_buildings:
    building = b.heat_building(conn, lk_wtb.df, temp, **building_def)
    h_building_df[building.type] = building.load

# Das DataFrame wird nun geplottet
h_building_df.plot(title='Standardized load profiles for heat')
plt.show()

# Wenn wir aufsummieren, dann müssten wieder die Jahressummen rauskommen.
# Wenn die Rundungsfehler zu groß sind, dann muss nochmal überlegt werden.
print('')
print(h_building_df.sum())
print(e_building_df.sum())
