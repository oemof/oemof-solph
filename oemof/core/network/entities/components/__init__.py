from .. import Component

class Sink(Component):
    """
    A Sink is special Component which only consumes some source commodity.
    Therefore its list of outputs has to be either None or empty
    (i.e. logically False).
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.outputs:
            raise ValueError("Sink must not have outputs.\n" +
                             "Got: {0!r}".format([str(x)
                                                 for x in self.outputs]))


class Source(Component):
    """
    The opposite of a Sink, i.e. a Component which only produces and as a
    consequence has no input.

    Parameters
    ----------
    in_max : list
        maximum input of component (e.g. in MW)
    out_max : list
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
        self.val = kwargs.get('val', None)
        self.curtail_costs = kwargs.get('curtail_costs', 0)

        if self.inputs:
            raise ValueError("Source must not have inputs.\n" +
                             "Got: {0!r}".format([str(x)
                                                 for x in self.inputs]))


class Transformer(Component):
    """
    A Transformer is a specific type of Component which transforms
    (possibly m) inputs into (possibly n) outputs. As such neither its
    list of inputs, nor its list of outputs are allowed to be empty.

    Parameters
    ----------
    out_min : list
        minimal output of transformer (e.g. min power output of powerplants)
    in_min : list
        minimal input of transformer (e.g. min fuel consumption of powerplants)
    grad_pos : float
        positive gradient (absolut value between two sequential timesteps)
    grad_neg : float
        negative gradient (absolut value between two sequential timesteps)
    t_min_off : float
        minimal off time in timesteps (e.g. 5 hours)
    t_min_on : float
        minimal on time in timesteps (e.g  5 hours)
    outages : float or array
        Outages of component.
        either: defined timesteps of timehorizon: e.g. [1,4,200]
        or: 0 <= scalar <= 1 as factor of the total timehorizon e.g. 0.05
    input_costs : float
        costs for usage of input (if not included in opex_var)
    start_costs : float
        cost per start up of transformer (only milp models)
    stop_costs : float
        cost per stop up of transformer (only milp models)
    ramp_costs : float
        costs for ramping
    output_price : list
        price for selling to output bus. prices ordered in the order
        of 'outputs'
    eta_min : list
      efficiency of transformer at minimum load for conversion of input
      to output (order of elements corresponding to order of elements
      out outputs,out_min etc.)
    """
    optimization_options = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.inputs:
            raise ValueError("Transformer must have at least one input.\n" +
                             "Got: {0!r}".format([str(x)
                                                 for x in self.inputs]))
        if not self.outputs:
            raise ValueError("Transformer must have at least one output.\n" +
                             "Got: {0!r}".format([str(x)
                                                 for x in self.outputs]))

        parameters = ['out_min', 'in_min', 'grad_pos', 'grad_neg',
                      't_min_off', 't_min_on', 'outages', 'input_costs',
                      'start_costs', 'stop_costs', 'ramp_costs',
                      'output_price', 'eta_min', 'max_starts']

        for k in kwargs:
            if k in parameters:
                setattr(self, k, kwargs[k])


class Transport(Component):
    """
    A Transport is a simple connection transporting a commodity from one
    Bus to a different one. It is different from a Transformer in that it
    may not change the type of commodity being transported. But since the
    transfer can still change things about the commodity other than the
    type (loss, gain, time delay, etc.) this class exists to encapsulate
    such changes.
    """
    optimization_options = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if len(self.inputs) != 1:
            raise ValueError("Transport must have exactly one input.\n" +
                             "Got: {0!r}".format([str(x)
                                                 for x in self.inputs]))

        if len(self.outputs) != 1:
            raise ValueError("Transport must have exactly one output.\n" +
                             "Got: {0!r}".format([str(x)
                                                 for x in self.outputs]))


