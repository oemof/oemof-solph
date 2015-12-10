from . import Source


class FixedSource(Source):
    """
    A fixed source only has one output always. The value of the output is fixed
    for all timesteps in the timehorizon of the optimization problem.
    """
    optimization_options = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DispatchSource(Source):
    """ Dispatch sources only have one output (like FixedSource) but the
    output can be reduced inside the optimization problem.
    """
    optimization_options = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# TODO: Implement constraints etc. for Commodity()
class Commodity(Source):
    """ The commodity component can be used to model inputs to resource busses.
    At the moment no constraint etc. are implemented for this component.
    """
    optimization_options = {}

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.sum_out_limit = kwargs.get('sum_out_limit', float('+inf'))


class GenPypo(Source):
    """ Create new pypower Generator class as child from oemof Sink used
    to define generators data
    """

    def __init__(self, **kwargs):
        """Assigned minimal required pypower input parameters of the generator
        as arguments

        Keyword generator arguments:
        PG --  the real power output in MW
        QG --  the reactive power output in MVAr
        qmax -- the maximum reactive power output in MVAr
        qmin -- the minimum reactive power output in MVAr
        VG -- the voltage magitude setpoint in p.u.
        mbase -- the total MVA base of the maschine, defaults to base MVA
        gen_status -- machine status,
                        > 0 = machine in-service
                        ≤ 0 = machine out-of-service
        pmax -- the maximum real power output in MW
        pmin -- the minimum real power output in MW
        """

        super().__init__(**kwargs)
        # Generator Data parameters
#       gen_bus -- bus_id used instead (bus_id already created)
        self.PG = kwargs.get("PG", None)
        self.QG = kwargs.get("QG", None)
        self.qmax = kwargs.get("qmax", None)
        self.qmin = kwargs.get("qmin", None)
        self.VG = kwargs.get("VG", None)
        self.mbase = kwargs.get("mbase", None)
        self.gen_status = kwargs.get("gen_status", None)
        self.pmax = kwargs.get("pmax", None)
        self.pmin = kwargs.get("pmin", None)

    def __iter__(self):
        return iter(self.bus_id)
