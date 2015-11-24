from . import Transport


class Simple(Transport):
    """
    Simple Transport connects two busses with a constant efficiency
    """
    optimization_options = {}

    def __init__(self, **kwargs):
        """
        :param eta: Constant efficiency of the transport.
        :param in_max: Maximum input the transport can handle, in $MW$.
        :param out_max: Maximum output which can possibly be obtained when
                        using the transport, in $MW$.
        """
        # TODO: Add check for what combination of parameters is given and
        #       calculate the missing ones accordingly. Also write down the
        #       relationshiph between the three parameters in the doctstring.
        super().__init__(**kwargs)
        self.eta = kwargs.get('eta')
        self.in_max = kwargs.get('in_max')
        self.out_max = kwargs.get('out_max')

        if(self.in_max is None and self.out_max is not None):
            self.in_max = self.out_max / self.eta
        if(self.out_max is None and self.in_max is not None):
            self.out_max = self.in_max * self.eta
