from . import Transport


class Simple(Transport):
    """
    Simple Transport connects two busses with a constant efficiency

    Parameters
    ----------
    eta : float
        Constant efficiency of the transport.
    in_max : float
        Maximum input the transport can handle, in $MW$.
    out_max : float
        Maximum output which can possibly be obtained when using the transport,
        in $MW$.
    """
    optimization_options = {}

    def __init__(self, **kwargs):
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


class BranchPypo(Transport):
    """Create new pypower Branch class as child from oemof Transport class
    used to define branch data
    """

    def __init__(self, **kwargs):
        """Assigned minimal required pypower input parameters of the branch
        arguments

        Keyword description of branch arguments:
        f_bus -- "from" bus number
        t_bus -- "to" bus number
        br_r -- the line resistance in p.u.
        br_x -- the line reactance in p.u.
        br_b -- the line charging susceptance in p.u.
        rate_a -- the line long term MVA  rating in MVA
        rate_b -- the line short term MVA rating in MVA
        rate_c -- the line emergency MVA rating on MVA
        tap -- the transformer tap ratio
        shift -- the transformer phase shift
        br_status -- branch status, 1= in service, 0 = out of service
        """
        super().__init__(**kwargs)
        # Branch Data Data parameters
        self.f_bus = kwargs.get('f_bus', None)
        self.t_bus = kwargs.get('t_bus', None)
        self.br_r = kwargs.get('br_r', None)
        self.br_x = kwargs.get('br_x', None)
        self.br_b = kwargs.get('br_b', None)
        self.rate_a = kwargs.get('rate_a', None)
        self.rate_b = kwargs.get('rate_b', None)
        self.rate_c = kwargs.get('rate_c', None)
        self.tap = kwargs.get('tap', None)
        self.shift = kwargs.get('shift', None)
        self.br_status = kwargs.get('br_status', None)
