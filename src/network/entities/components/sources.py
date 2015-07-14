from network.entities.components import Source


class Renewable(Source):
    """
    """
    __lower_name__ = "renewable_source"

    def __init__(self, **kwargs):
        """
        :param boolean dispatch: Flag if RenewableSource is dispatchable or not
        """
        super().__init__(**kwargs)
        self.val = kwargs.get('val', None)
        self.dispatch = kwargs.get('dispatch', False)
        self.dispatch_ex = kwargs.get('dispatch_ex', 0)


class Commodity(Source):
    """
    """
    __lower_name__ = "commodity"

    def __init__(self, **kwargs):
        """
        """
        super().__init__(**kwargs)
        self.yearly_limit = kwargs.get('yearly_limit', float('+inf'))
        self.emmision_factor = kwargs.get('emmission_factor', 0)

    def emissions(self):
        self.emissions = [o * self.emmision_factor
                          for o in self.results['Output'][self.outputs[0].uid]]
