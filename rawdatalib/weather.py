__package__ = "rawdatalib"

import oemof.iolib.postgis as pg


class Weather:
    """
    Main-Interface for loading weather data.

    """

    def __init__(self, year, region, params):
        """
        constructor for the weather-object.
        Test for config, to set up which source shall be used
        """
        self._data = pg.raw_query("year: " + year + ", region: " + region + ", params: ")



    def get_raw_data(self):
        """
        use this method to retrieve the whole raw dataset
        :return: the weatherdata
        """
        return self._data
