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
        :param capex: capex for new installed capacity
        :param opex_fix: fixed opex (e.g. expenses for staff)
        :param opex_var: variable opex (e.g. spare parts)
        :param crf: capital recovery factor: (p*(1+p)^n)/(((1+p)^n)-1)
        """
        super().__init__(**kwargs)

        self.in_max = kwargs.get('in_max', None)
        self.out_max = kwargs.get('out_max', None)
        self.lifetime = kwargs.get('lifetime', 20)
        self.wacc = kwargs.get('wacc', 0.05)
        self.capex = kwargs.get('capex', 0)
        self.opex_fix = kwargs.get('opex_fix', 0)
        self.opex_var = kwargs.get('opex_var', 0)
        self.crf = kwargs.get('crf', 0)
        self.co2_var = kwargs.get('co2_var', 0)
        self.max_cap = kwargs.get('max_cap', float("+inf"))
        self.results = kwargs.get('results', {'in': {},
                                              'out': {}})
