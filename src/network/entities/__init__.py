from network import Entity


class Bus(Entity):
    """
    The other type of entity in an energy system graph (besides
    Components). A Bus acts as a kind of mediator between producers and
    consumers of a commodity of the same kind. As such it has a type,
    which signifies what kind of commodity goes through the bus.
    """
    __lower_name__ = "bus"

    def __init__(self, **kwargs):
        """
        :param type: the type of the bus. Can be a meaningful value like e.g.
                     "electricity" but may be anything that can be tested for
                     equality and is distinct for incompatible Buses.
        """
        super().__init__(**kwargs)
        self.type = kwargs["type"]


class Component(Entity):
    """
    Components are one specific type of entity comprising an energy system
    graph, the other being Buses. The important thing is, that connections
    in an energy system graph are only allowed between Buses and
    Components and not between Entities of equal subtypes. This class
    exists only to facilitate this distinction and is empty otherwise.
    """
    __lower_name__ = "component"

    def __init__(self, **kwargs):
        """
        """
        super().__init__(**kwargs)

        self.in_max = kwargs.get('in_max', None)
        self.out_max = kwargs.get('out_max', None)
        self.lifetime = kwargs.get('lifetime', 20)
        self.wacc = kwargs.get('wacc', 0.05)
        self.capex = kwargs.get('capex', 0)
        self.opex_fix = kwargs.get('opex_fix', None)
        self.opex_var = kwargs.get('opex_var', 0)
        self.co2_var = kwargs.get('co2_var', None)
        self.param = kwargs.get('param', None)
        self.results = kwargs.get('results', {})
