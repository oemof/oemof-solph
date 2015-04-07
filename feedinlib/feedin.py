"""
feedin.py
version: 0.1

This module is used to retrieve and calculate outputdata (feed-in - data) for the scientific models.

"""
from oemof.rawdatalib.weather import CsvWeather
from oemof.feedinlib.wind_feed import WindFeed
weather = None


def feed(Grid, scenario):
    """
    this function stats the feeding process.
    :param Grid: the grid to get feeded.
    :param scenario: the scenario-parameter-dict
    """
    #get all entities
    entities = Grid.get_all_entities()
    #filter for wind_entities
    wind_entities = {k:v for (k,v) in entities.items() if v["type"] == "wind"}
    #filter for pv-entites
    pv_entities = {k:v for (k,v) in entities.items() if v["type"] == "pv"}

    #create the weatherobject
    weather = CsvWeather(scenario)

    #start feeding
    #TODO: make the feed() chose the correct feeder, dont hardcode it!
    wind_feed = WindFeed(weather).feed(wind_entities)




