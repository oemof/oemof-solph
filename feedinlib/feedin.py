"""
feedin.py
version: 0.1

This module is used to retrieve and calculate outputdata (feed-in - data) for the scientific models.

"""

from pvfeed import _PvFeed
from windfeed import _WindFeed
import importlib
# list of instances
_instance_list = []


def create_timeseries(feedin_type, year, region):
    """
    Factory to create a Timeseries-Object of Feeders: PV or wind
    :param feedin_type: a string to specify the feeder-type ("wind", "pv", ...)
    :param year: the year to get the data for
    :param region:  the region to get the data for
    :return: the Timeseries-Object
    """
    try:
        module = __import__("feedinlib")
        file_name = getattr(module, feedin_type + "feed")
        class_name = "_" + feedin_type[:1].upper() + feedin_type[1:] + "Feed"
        class_ = getattr(file_name, class_name)
        _obj = class_(year, region)
        _instance_list.append(_obj)
        return _obj
    except AttributeError:
        print "the feedtype \"" + feedin_type + "\" doesn't seem to exist. Maybe a typo?"




def get_instance_list():
    return _instance_list


