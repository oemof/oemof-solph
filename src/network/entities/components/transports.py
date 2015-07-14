from network.entities.components import Transport


class Simple(Transport):
    """
    Simple Transport connects two busses with a constant efficiency
    """
    __lower_name__ = "simple_transport"

    def __init__(self, **kwargs):
        """
        :param eta: eta as constant efficiency for simple transport
        """
        super().__init__(**kwargs)
        self.eta = kwargs.get('eta', None)

        if(self.in_max is None and self.out_max is not None):
            self.in_max = self.out_max / self.eta
        if(self.out_max is None and self.in_max is not None):
            self.out_max = self.in_max * self.eta
