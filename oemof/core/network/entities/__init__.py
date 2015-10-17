from .. import Entity


class Bus(Entity):
    """
    The other type of entity in an energy system graph (besides
    Components). A Bus acts as a kind of mediator between producers and
    consumers of a commodity of the same kind. As such it has a type,
    which signifies what kind of commodity goes through the bus.
    """
    lower_name = "bus"

    def __init__(self, **kwargs):
        """
        :param type: the type of the bus. Can be a meaningful value like e.g.
                     "electricity" but may be anything that can be tested for
                     equality and is distinct for incompatible Buses.
        :param price: price per unit of type
        """
        super().__init__(**kwargs)
        self.type = kwargs.get("type", None)
        self.price = kwargs.get("price", 0)
        self.sum_out_limit = kwargs.get("sum_out_limit", float("+inf"))
        self.emission_factor = kwargs.get("emission_factor", 0)
        self.results = {}


class Component(Entity):
    """
    Components are one specific type of entity comprising an energy system
    graph, the other being Buses. The important thing is, that connections
    in an energy system graph are only allowed between Buses and
    Components and not between Entities of equal subtypes. This class
    exists only to facilitate this distinction and is empty otherwise.
    """
    lower_name = "component"

    def __init__(self, **kwargs):
        """
        Parameters:
        ------------
        in_max : maximum input of component (e.g. in MW)
        out_max : maximum output of component (e.g. in MW)
        add_out_limit : limit on additional output "capacity"

        capex : capital expenditure
        lifetime : lifetime of component
        wacc : weigted average cost of capital (dimensionless)
        crf: capital recovery factor: (p*(1+p)^n)/(((1+p)^n)-1)

        opex_fix : fixed operational expenditure (e.g. expenses for staff)
        opex_var : variable operational expenditure (e.g. spare parts)
        ramp_costs : costs du to ramping
        start_costs : costs due to start of component

        co2_fix : fixed co2 emissions
        co2_var : variable co2 emissions
        co2_cap : co2 emissions due to installed capacity
        """
        super().__init__(**kwargs)

        self.in_max = kwargs.get('in_max', None)
        self.out_max = kwargs.get('out_max', None)
        self.add_out_limit = kwargs.get('add_out_limit', None)

        self.capex = kwargs.get('capex', 0)
        self.lifetime = kwargs.get('lifetime', 20)
        self.wacc = kwargs.get('wacc', 0.05)

        self.opex_var = kwargs.get('opex_var', 0)
        self.opex_fix = kwargs.get('opex_fix', 0)
        self.ramp_costs = kwargs.get('rampex', 0)
        self.start_costs = kwargs.get('start_costs', 0)

        self.co2_var = kwargs.get('co2_var', 0)
        self.co2_fix = kwargs.get('co2_fix', 0)
        self.co2_cap = kwargs.get('co2_cap', 0)

        self.crf = kwargs.get('crf', None)
        if self.crf is None:
            p = self.wacc
            n = self.lifetime
            self.crf = (p*(1+p)**n)/(((1+p)**n)-1)

        self.results = kwargs.get('results', {'in': {},
                                              'out': {}})
