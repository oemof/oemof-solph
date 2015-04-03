import oemof.rawdatalib.weather as w


class Feed(object):

    #init for basic data
    def __init__(self, DIC, site, year, params):
        """
        Timeseries-Class

        :param DIC: database parameters
        :param site: site and plant parameters
        :param year: the year to get the data for
        :param params: list of strings to define which variables to load from the DB
        """
        self._timeseries = None
        self._DIC = DIC
        self._site = site
        self._year = year
        self._weatherObject = None
        self._load_timeseries(DIC, site, year, params)


    def _load_timeseries(self, DIC, site, year, params):
        """
        sets the raw data from a weather object and calls the apply_model
        if each data is not yet set. Maybe a "force recalculate" parameter?
        :param params: List of Parameters to specify the variable to load
        :return: the timeseries of data
        """

        if (self._weatherObject is None) or (params.get("recalculate")
        is not None):
            self._weatherObject = self._get_weather_object_from_source(
                self._DIC, self._site, self._year, params)
        if (self._timeseries is None) or (params.get("recalculate")
        is not None):
            self._apply_model(DIC, site, year, self._weatherObject)

        return self._timeseries

    #def _apply_model(self):
        #"""
        #calculates the timeseries from the input data
        #override this method for your implementation in the corresponding subclass (PV, Wind, ...)
        #:return:
        #"""
        ## TODO: change to actually working code
        #print("using the model from the base class is useless. Implement the methods of the subclass first")
        #pass

    #return the raw data by instantiating a raw_data object
    def _get_weather_object_from_source(self, DIC, site, year, params):
        """
        returns the weather object
        :param DIC: database parameters
        :param site: site and plant parameters
        :param year: the year to get the data for
        :param params: List of parameters
        :return: the weather-timeseries
        """
        print(self.__class__)

        obj = w.Weather(year, params)
        obj.get_raw_data(DIC, site, year)

        #return w.Weather(year, region, params)
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



class Feeder(object):
    """
    This class is the newly written Feeder-structure for the "first-example"-implementation"
    To avoid incompatibility with existing code, a new class has been constructed.
    You always want to inherit from this class, changes in this class will affect all other feeders.
    """
    def __init__(self, weather_object, params):
        """
        instantiate the feeder object with the weather_object from rawdatalib and the weatherpamaters-list
        Override this constructor within your inherited class, define the fields needed ["wss", "T", "radiation"]...
        and call this consctructor (see wind_feed.py for an example)

        :param weather_object: The weatherobject.
        :param params: the parameter-list
        """
        self.weather = weather_object
        self.params = params
        self.fields = {}
        for p in params:
            self.fields[p] = self.weather.get_timeseries(p)

    def feed (self, entities):
        """
        call this method to start thefeeding process for the entities provided.
        :param entities: dict of entities, HAS TO CHANGE!!!
        :return:
        """
        #TODO: has to be a list of entites, not a dict

        for k,e in entities.items():
            for (field, series) in self.fields.items():
                e[field] = series
            self._apply_model(e)

    def _apply_model(self, entity):
        """
        everride this method and implement your scientific model for single-entities inside.
        :param entity: the entity to calculate
        """

        e = entity
