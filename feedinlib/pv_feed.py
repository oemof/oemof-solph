
from oemof.feedinlib.base_feed import Feed


class _PvFeed(Feed):

    def __init__(self, year, region):
        """
        private class for the implementation of a Phovoltaic Feed as timeseries
        :param year: the year to get the data for
        :param region: the region to get the data for
        """
        super(_PvFeed, self).__init__(year, region, ["WSS", "T"])


    def _apply_model(self):
        """
        implementation of the model to generate the _timeseries data from the _weatherdata
        :return:
        """
        self._timeseries = "pv timeseries"
        #TODO: setup the model

