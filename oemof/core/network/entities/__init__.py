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
        if true a busbalance is created, otherwise the busbalance is ignored
    sum_out_limit : float (default: +inf)
        limit of sum of all outflows over the timehorizon
    # TODO: Find a better name for 'sum_out_limit' (global_outflow_limit?)
    excess : boolean
        if true, an optimization variable is created that takes up the slack of
        outflows to keep the busbalance (sum inflows = sum outflows + excess)
    shortage : boolean
        if true, an optimization variable is created that takes the slack of
        inflows to keep the busbalance (sum inflows + shortage = sum outflows)
    excess_costs : float
        costs per unit of excess that is needed to balance the bus
    shortage_costs : float
        costs per unit of shortage that is needed to balance the bus
    """
    optimization_options = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = kwargs.get("type", None)
        self.price = kwargs.get("price", 0)
        self.balanced = kwargs.get("balanced", True)
        self.sum_out_limit = kwargs.get("sum_out_limit", float("+inf"))
        self.results = {}
        self.excess = kwargs.get('excess', True)
        self.shortage = kwargs.get('shortage', False)
        self.excess_costs = kwargs.get('excess_costs', 0)
        self.shortage_costs = kwargs.get('shortage_costs', 10e10)

        if self.excess == True:
           self.create_excess_slack_component()
        if self.shortage == True:
           self.create_shortage_slack_component()

    def create_excess_slack_component(self):
        """
        """
        excess = ExcessSlack(uid=self.uid+'_excess',
                             inputs=[self],
                             costs=self.excess_costs)
        return excess

    def create_shortage_slack_component(self):
        """
        """
        shortage = ShortageSlack(uid=self.uid+'_shortage',
                                 outputs=[self],
                                 costs=self.shortage_costs)
        return shortage

class Component(Entity):
    """
    Components are one specific type of entity comprising an energy system
    graph, the other being Buses. The important thing is, that connections
    in an energy system graph are only allowed between Buses and
    Components and not between Entities of equal subtypes. This class
    exists only to facilitate this distinction and is empty otherwise.

    Parameters
    ----------
    in_max : list
        maximum input of component (power)
    out_max : list
        maximum output of component (power)
    ub_out : list of pandas.series (or array-like)
        The time-depended maximum output of a component. If ub_out is not set
        out_max is used. Contrary to out_max ub_out has to be array-like. If
        ub_out is set out_max is used as the installed capacity and ub_out as
        the time-depended maximum output. It is in charge of the user that
        these values are not inconsistent. You may use max(ub_out) for out_max.
        (power)
    add_out_limit : float
        limit on additional output "capacity" (power)
    capex : float
        Capital expenditure. To get the capital cost it is multiplied with
        out_max (monetory value per power).
    lifetime : float
        lifetime of component (e.g. years)
    wacc : float
        weigted average cost of capital (dimensionless)
    crf : float
        capital recovery factor: (p*(1+p)^n)/(((1+p)^n)-1)
    opex_fix : float
        fixed operational expenditure (e.g. expenses for staff) (monetory
        value over the full time period).
    opex_var : float
        Variable operational expenditure (e.g. spare parts). You can use it to
        define the fuel costs. Fuel cost can be defined in different ways, so
        be aware not to definge them twice.
    co2_var : float
        variable co2 emissions (e.g. t / MWh)
    co2_cap : float
        co2 emissions due to installed power (e.g. t/ MW)
    """
    optimization_options = {}

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.in_max = kwargs.get('in_max')
        self.out_max = kwargs.get('out_max')
        self.ub_out = kwargs.get('ub_out')
        self.add_out_limit = kwargs.get('add_out_limit')
        self.capex = kwargs.get('capex', 0)
        self.lifetime = kwargs.get('lifetime', 20)
        self.wacc = kwargs.get('wacc', 0.05)
        self.opex_var = kwargs.get('opex_var', 0)
        self.opex_fix = kwargs.get('opex_fix', 0)
        self.co2_var = kwargs.get('co2_var', 0)
        self.co2_cap = kwargs.get('co2_cap', 0)

        self.crf = kwargs.get('crf', None)
        if self.crf is None:
            p = self.wacc
            n = self.lifetime
            self.crf = (p*(1+p)**n)/(((1+p)**n)-1)
        self.results = kwargs.get('results', {'in': {},
                                              'out': {}})

class ExcessSlack(Component):
    """A ExcessSlack is a special sink which takes the output slack i.e. excess
    of the bus to that it is connected."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.costs = kwargs.get("costs", 0)

class ShortageSlack(Component):
    """A ShorageSlack is a special source which takes the input slack i.e.
    shortage of the bus to that it is connected."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.costs = kwargs.get("costs", 10e10)