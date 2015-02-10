from base_feed import Feed


class _WindFeed(Feed):

    def __init__(self, year, region):
        """
        private class for the implementation of a Wind Feed as timeseries
        :param year: the year to get the data for
        :param region: the region to get the data for
        """
        super(_WindFeed, self).__init__(year, region, ["WSS"])


    def _apply_model(self):
        """
        implementation of the model to generate the _timeseries data from the _weatherdata
        :return:
        """
        self._timeseries = self._weatherObject.get_raw_data()
        #TODO: setup the model