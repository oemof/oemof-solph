from .. import Component

class Sink(Component):
    """
    A Sink is special Component which only consumes some source commodity.
    Therefore its list of outputs has to be either None or empty
    (i.e. logically False).
    """
    lower_name = "sink"

    def __init__(self, **kwargs):
        """
        """
        super().__init__(**kwargs)
        if self.outputs:
            raise ValueError("Sink must not have outputs.\n" +
                             "Got: {0!r}".format([str(x)
                                                 for x in self.outputs]))


class Source(Component):
    """
    The opposite of a Sink, i.e. a Component which only produces and as a
    consequence has no input.
    """
    optimization_options = {}
    lower_name = "source"

    def __init__(self, **kwargs):
        """
        """
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
    out_min : minimal output of transformer (e.g. pmin for powerplants)
    in_min : minimal input of transformer (e.g. pmin for powerplants)
    grad_pos : positive gradient (<=0, <=1, relativ out_max)
    grad_neg : negative gradient (<=0, <=1, relativ out_max)
    t_min_off : minimal off time in timesteps (e.g. 5 hours)
    t_min_on : minimal on time in timesteps (e.g  5 hours)
    outages : outages of component. can be scalar or array:
             either: defined timesteps of timehorizon: e.g. [1,4,200]
             or: 0 <= scalar <= 1 as factor of the total timehorizon
             e.g. 0.05
    input_costs : costs for usage of input (if not included in opex_var)
    start_costs : cost per start up of transformer (only milp models)
    stop_costs : cost per stop up of transformer (only milp models)
    ramp_costs: costs for ramping
    output_price : price for selling output (revenue expr. in objective)



    """
    optimization_options = {}
    lower_name = "transformer"

    def __init__(self, **kwargs):
        """
        """
        super().__init__(**kwargs)
        if not self.inputs:
            raise ValueError("Transformer must have at least one input.\n" +
                             "Got: {0!r}".format([str(x)
                                                 for x in self.inputs]))
        if not self.outputs:
            raise ValueError("Transformer must have at least one output.\n" +
                             "Got: {0!r}".format([str(x)
                                                 for x in self.outputs]))
        # technical parameter
        parameters = ['out_min', 'in_min', 'grad_pos', 'grad_neg',
                      't_min_off', 't_min_on', 'outages', 'input_costs',
                      'start_costs', 'stop_costs', 'ramp_costs',
                      'output_price']

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
    lower_name = "transport"

    def __init__(self, **kwargs):
        """
        """
        super().__init__(**kwargs)
        if len(self.inputs) != 1:
            raise ValueError("Transport must have exactly one input.\n" +
                             "Got: {0!r}".format([str(x)
                                                 for x in self.inputs]))

        if len(self.outputs) != 1:
            raise ValueError("Transport must have exactly one output.\n" +
                             "Got: {0!r}".format([str(x)
                                                 for x in self.outputs]))
