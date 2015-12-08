from .. import Bus

class BusPypo(Bus):
    """ Create new pypower Bus class as child from oemof Bus used to define
    busses and generators data
    """

    def __init__(self, **kwargs):
        """Assigned minimal required pypower input parameters of the bus and
        generator as arguments

        Keyword description of bus arguments:
        bus_id -- the bus number (also used as GEN_BUS parameter for generator)
        bus_type -- the bus type (1 = PQ, 2 = PV, 3 = ref, 4 = Isolated)
        PD -- the real power demand in MW
        QD -- the reactive power demand in MVAr
        GS -- the shunt conductance (demanded at V = 1.0 p.u.) in MW
        BS -- the shunt susceptance (injected at V = 1.0 p.u.) in MVAr
        bus_area -- area number (positive integer)
        VM -- the voltage magnitude in p.u.
        VA -- the voltage angle in degrees
        base_kv -- the base voltage in kV
        zone -- loss zone (positive integer)
        vmax -- the maximum allowed voltage magnitude in p.u.
        vmin -- the minimum allowed voltage magnitude in p.u.

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
        # Bus Data parameters
        self.bus_id = kwargs.get("bus_id", None)
        self.bus_type = kwargs.get("bus_type", None)
        self.PD = kwargs.get("PD", None)
        self.QD = kwargs.get("QD", None)
        self.GS = kwargs.get("GS", None)
        self.BS = kwargs.get("BS", None)
        self.bus_area = kwargs.get("bus_area", None)
        self.VM = kwargs.get("VM", None)
        self.VA = kwargs.get("VA", None)
        self.base_kv = kwargs.get("base_kv", None)
        self.zone = kwargs.get("zone", None)
        self.vmax = kwargs.get("vmax", None)
        self.vmin = kwargs.get("vmin", None)

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
