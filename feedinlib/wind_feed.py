"""
Module created for the "first-example"-implementation.
It is just a demonstration on how to correctly define the data needed for calculation in the constructor
and how to access its datafields inside the _apply_model.

"""
from oemof.feedinlib.base_feed import Feeder


class WindFeed(Feeder):

    def __init__(self, weather_object):
        """
        private class for the implementation of a Wind Feed as timeseries
        :param year: the year to get the data for
        :param region: the region to get the data for
        """
        super(WindFeed, self).__init__(weather_object, ["wss"])


    def _apply_model(self, entity):
        """
        implementation of the model to generate the _timeseries data from the _weatherdata
        :return:
        """
        #TODO: setup the model, currently being done by clemens
        e = entity

        e["output"] = {}

        for k,v in e["wss"].items():
            e["output"][k] = int(v)*200
