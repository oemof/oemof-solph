from network.entities.components import Source


class FixedSource(Source):
    """
    """
    lower_name = "fixed_source"

    def __init__(self, **kwargs):
        """
        :param boolean dispatch: Flag if RenewableSource is dispatchable or not
        """
        super().__init__(**kwargs)
        self.val = kwargs.get('val', None)

    def calc_emissions(self):
        self.emissions = [0 for o in self.results['out'][self.outputs[0].uid]]


class DispatchSource(Source):
    """
    """
    lower_name = "dispatch_source"

    def __init__(self, **kwargs):
        """
        :param boolean dispatch: Flag if RenewableSource is dispatchable or not
        """
        super().__init__(**kwargs)
        self.val = kwargs.get('val', None)
        self.dispatch = kwargs.get('dispatch', False)
        self.dispatch_ex = kwargs.get('dispatch_ex', 0)

    def calc_emissions(self):
        self.emissions = [0 for o in self.results['out'][self.outputs[0].uid]]


class Commodity(Source):
    """
    """
    lower_name = "commodity"

    def __init__(self, **kwargs):
        """
        """
        super().__init__(**kwargs)
        self.sum_out_limit = kwargs.get('yearly_limit', float('+inf'))
        self.emmision_factor = kwargs.get('emmission_factor', 0)

    def calc_emissions(self):
        self.emissions = [o * self.emmision_factor
                          for o in self.results['out'][self.outputs[0].uid]]
