from ..src import energy_weather as w


class Feed(object):

    def __init__(self, conn, geo, site, year, params, elevation_mean):
        """
        Timeseries-Class

        :param DIC: database parameters
        :param site: site and plant parameters
        :param year: the year to get the data for
        :param params: list of strings to define which variables to load
            from the DB
        """
        self._timeseries = None
        self.geo = geo
        self.conn = conn
        self._site = site
        self._year = year
        self._weatherObject = None
        self._load_timeseries(conn, geo, site, year, params,
                              elevation_mean=elevation_mean)

    def _load_timeseries(self, conn, geo, site, year, params, elevation_mean):
        """
        sets the raw data from a weather object and calls the apply_model
        if each data is not yet set. Maybe a "force recalculate" parameter?
        :param params: List of Parameters to specify the variable to load
        :return: the timeseries of data
        """

        if (self._weatherObject is None) or (params.get("recalculate")
                                             is not None):
            self._weatherObject = self._get_weather_object_from_source(
                self.conn, self.geo, self._site, self._year, params)
        if (self._timeseries is None) or (params.get("recalculate")
                                          is not None):
            self._apply_model(self.conn, site, year, self._weatherObject,
                              elevation_mean=elevation_mean)

        return self._timeseries

    def _get_weather_object_from_source(self, conn, geom, site, year, params):
        """
        returns the weather object
        :param DIC: database parameters
        :param site: site and plant parameters
        :param year: the year to get the data for
        :param params: List of parameters
        :return: the weather-timeseries
        """

        obj = w.Weather(conn, geom, year, params)
        print(obj)
        obj.get_feedin_data()
        return obj.data

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
