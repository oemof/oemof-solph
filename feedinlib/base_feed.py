import rawdatalib.weather as w

class Feed(object):

    #init for basic data
    def __init__(self, year, region, params):
        """
        Timeseries-Class

        :param year: the year to get the data for
        :param region: the region to get the data for
        :param params: list of strings to define which variables to load from the DB
        """
        self._timeseries = None
        self._year = year
        self._region = region
        self._weatherObject = None
        self._load_timeseries(params)


    def _load_timeseries(self, params):
        """
        sets the raw data from a weather object and calls the apply_model
        if each data is not yet set. Maybe a "force recalculate" parameter?
        :param params: List of Parameters to specify the variable to load
        :return: the timeseries of data
        """

        if (self._weatherObject is None) or (params.get("recalculate") is not None):
            self._weatherObject = self._get_weather_object_from_source(self._year, self._region, params)
        if (self._timeseries is None) or (params.get("recalculate") is not None):
            self._apply_model()

        return self._timeseries


    def _apply_model(self):
        """
        calculates the timeseries from the input data
        override this method for your implementation in the corresponding subclass (PV, Wind, ...)
        :return:
        """
        # TODO: change to actually working code
        print "using the model from the base class is useless. Implement the methods of the subclass first"
        pass

    #return the raw data by instantiating a raw_data object
    def _get_weather_object_from_source(self, year, region, params):
        """
        returns the weather object
        :param year: the year to get the data for
        :param region: the year to get the data for
        :param params: List of parameters
        :return: the weather-timeseries
        """
        print self.__class__

        return w.Weather(year, region, params)

    def get_year(self):
        """
        :return: the year of this Time-Series-Instance
        """
        return self._year

    def get_region(self):
        """
        :return: the region of this Time-Series-Instance
        """
        return self._region

    def get_timeseries(self):
        """
        :return: the data-timeseries of this Time-Series-Instance
        """
        return self._timeseries




