from .. import Entity


class Bus(Entity):
    """
    The other type of entity in an energy system graph (besides
    Components). A Bus acts as a kind of mediator between producers and
    consumers of a commodity of the same kind. As such it has a type,
    which signifies what kind of commodity goes through the bus.

    Parameters
    ----------
    type : string
        the type of the bus. Can be a meaningful value like e.g. "electricity"
        but may be anything that can be tested for equality and is distinct for
        incompatible Buses.
    price : float
        price per unit of type
    balanced : boolean
        TODO: Does anybody know what it means
    sum_out_limit : float (default: +inf)
        TODO: Does anybody know what it means
    emission_factor : float
        TODO: Unit?
    excess : boolean
        TODO: Does anybody know what it means
    shortage : boolean
        TODO: Does anybody know what it means
    excess_costs : float
        TODO: Unit? Costs for an unbalanced balance.
    shortage_costs : float
        TODO: Does anybody know what it means
    """
    optimization_options = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = kwargs.get("type", None)
        self.price = kwargs.get("price", 0)
        self.balanced = kwargs.get("balanced", True)
        self.sum_out_limit = kwargs.get("sum_out_limit", float("+inf"))
        self.emission_factor = kwargs.get("emission_factor", 0)
        self.results = {}
        self.excess = kwargs.get('excess', True)
        self.shortage = kwargs.get('shortage', False)
        self.excess_costs = kwargs.get('excess_costs', 0)
        self.shortage_costs = kwargs.get('shortage_costs', 10e10)


class Component(Entity):
    """
    Components are one specific type of entity comprising an energy system
    graph, the other being Buses. The important thing is, that connections
    in an energy system graph are only allowed between Buses and
    Components and not between Entities of equal subtypes. This class
    exists only to facilitate this distinction and is empty otherwise.

    Parameter
    ---------
    in_max : float
        maximum input of component (e.g. in MW)
    out_max : float
        maximum output of component (e.g. in MW)
    add_out_limit : float
        limit on additional output "capacity" (e.g. in MW)
    capex : float
        capital expenditure (e.g. in Euro / MW )
    lifetime : float
        lifetime of component (e.g. years)
    wacc : float
        weigted average cost of capital (dimensionless)
    crf : float
        capital recovery factor: (p*(1+p)^n)/(((1+p)^n)-1)
    opex_fix : float
        fixed operational expenditure (e.g. expenses for staff)
    opex_var : float
        variable operational expenditure (e.g. spare parts + fuelcosts)
    co2_fix : float
        fixed co2 emissions (e.g. t / MW)
    co2_var : float
        variable co2 emissions (e.g. t / MWh)
    co2_cap : float
        co2 emissions due to installed power (e.g. t/ MW)
    """
    optimization_options = {}

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.in_max = kwargs.get('in_max', None)
        self.out_max = kwargs.get('out_max', None)
        self.add_out_limit = kwargs.get('add_out_limit', 0)
        self.capex = kwargs.get('capex', 0)
        self.lifetime = kwargs.get('lifetime', 20)
        self.wacc = kwargs.get('wacc', 0.05)
        self.opex_var = kwargs.get('opex_var', 0)
        self.opex_fix = kwargs.get('opex_fix', 0)
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
