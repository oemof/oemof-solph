# -*- coding: utf-8 -*-

'''Holiday information for Germany.'''

import logging
from datetime import date, timedelta
from dateutil import easter
import urllib
import xml.etree.ElementTree as ET


def get_german_holidays(year, place=[None, None, None], scope='legal', _=str):
    """
    Returns German holiday dates. Use the s for the german
    federal states like 'Germany/BY ' for Bayern.
    :
    Example: get_holidays(2015, place=['Germany', 'BE', 'Berlin'])
    """
    logging.debug('Feiertage für: {0}'.format(place))
    if place[0] not in ['Deutschland', 'deutschland', 'Germany', 'germany']:
        logging.error(
            'You are outside of Germany. The holidays will be incorrect.')
    # Determine Easter
    eastr = easter.easter(year)

    # Add national holidays
    adict = {
        date(year,  1,  1): 'Neujahr',
        date(year,  5,  1): 'Tag der Arbeit',
        date(year, 10,  3): 'Tag der Deutschen Einheit',
        date(year, 12, 25): '1. Weihnachtstag',
        date(year, 12, 26): '2. Weihnachtstag',
        eastr - timedelta(days=2): 'Karfreitag',
        eastr: 'Ostersonntag',
        eastr + timedelta(days=1): 'Ostermontag',
        eastr + timedelta(days=39): 'Christi Himmelfahrt',
        eastr + timedelta(days=50): 'Pfingstmontag',
        }

    # Add federal holidays
    if place[1].upper() in ('BW', 'BY', 'ST'):
        adict[date(year, 1, 6)] = 'Heilige Drei Könige'

    if place[1] in ('BW', 'BY', 'HE', 'NW', 'RP', 'SL'):
        adict[eastr + timedelta(days=60)] = 'Frohnleichnam'

    if place[1].upper() in ('BY', 'SL'):
        adict[date(year, 8, 15)] = 'Mariä Himmelfahrt'

    if place[1].upper() in ('BB', 'MV', 'SN', 'ST', 'TH'):
        adict[date(year, 10, 31)] = 'Reformationstag'

    if place[1].upper() in ('BW', 'BY', ):
        adict[date(year, 11, 1)] = 'Allerheiligen'

    return adict


def fetch_admin_from_latlon(lat=None, lon=None, coord=None):
    """
    Receive reverse geocoded information from lat/lon point
    :rtype : dict
    :param lat: latitude
    :param lon: longitude
    :param zoom: detail level of information
    :return: list: [country, state]
    """
    def parse_result(res):
        root = ET.fromstring(res)
        address_parts = {}

        for a in root[1]:
            address_parts[a.tag] = a.text

        return address_parts

    if lat is None or lon is None:
        lon = coord[0]
        lat = coord[1]

    query = "http://nominatim.openstreetmap.org/reverse?"
    query += "format=xml"
    query += "&lat={lat}".format(lat=lat)
    query += "&lon={lon}".format(lon=lon)
    query += "&zoom=18"
    query += "&addressdetails=1"

    conn = urllib.request.urlopen(query)
    rev_geocode = conn.read()
    address_parts = parse_result(rev_geocode)

    try:
        state = get_abbreviation_of_state(address_parts['state'])
    except KeyError:
        logging.error(
            "Didn't get the name of the state. " +
            "Maybe the coordinates ({0}) are outside of Germany.".format(
                str([lat, lon])))
        state = ''

    try:
        country = address_parts['country']
    except:
        country = ''

    return [country, state]


def get_abbreviation_of_state(statename):
    abbr_dict = {
        'Baden-Württemberg': 'BW',
        'Bayern': 'BY',
        'Berlin': 'BE',
        'Brandenburg': 'BB',
        'Bremen': 'HB',
        'Hamburg': 'HH',
        'Hessen': 'HE',
        'Mecklenburg-Vorpommern': 'MV',
        'Niedersachsen': 'NI',
        'Nordrhein-Westfalen': 'NW',
        'Rheinland-Pfalz': 'RP',
        'Saarland': 'SL',
        'Sachsen': 'SN',
        'Sachsen-Anhalt': 'ST',
        'Schleswig-Holstein': 'SH',
        'Thüringen': 'TH'}
    return abbr_dict[statename]


if __name__ == "__main__":
    from pprint import pprint
    lat = 48.
    lon = 11.5
    pprint(get_german_holidays(2015, place=fetch_admin_from_latlon(lat, lon)))
