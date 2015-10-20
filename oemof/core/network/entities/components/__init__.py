from .. import Component
import logging

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
    lower_name = "source"

    def __init__(self, **kwargs):
        """
        """
        super().__init__(**kwargs)
        if self.inputs:
            raise ValueError("Source must not have inputs.\n" +
                             "Got: {0!r}".format([str(x)
                                                 for x in self.inputs]))


class Transformer(Component):
    """
    A Transformer is a specific type of Component which transforms
    (possibly m) inputs into (possibly n) outputs. As such neither its
    list of inputs, nor its list of outputs are allowed to be empty.
    """
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

        self.opex_var = kwargs.get('opex_var', None)
        # if no opex are give use price information of bus
        if self.opex_var is None:
            self.opex_var = self.inputs[0].price
            logging.info('No opex defined. Setting bus price as opex for:' +
                         ' component %s', self.uid)

        self.out_min = kwargs.get('out_min', None)
        if self.out_min is None:
            # set default output to 0.5*outmax
            self.out_min = {self.outputs[0].uid:
                            self.out_max[self.outputs[0].uid]*0.5}

        self.start_costs = kwargs.get('start_costs', None)
        if self.start_costs is None:
            self.start_costs = 1
            logging.info('No startcosts defined. Setting default costs of 1' +
                         ' for component %s', self.uid)
        self.ramp_costs = kwargs.get('ramp_costs', 0)

    def calc_emissions(self):
        self.emissions = [i * self.co2_var
                          for i in self.results['in'][self.inputs[0].uid]]


class Transport(Component):
    """
    A Transport is a simple connection transporting a commodity from one
    Bus to a different one. It is different from a Transformer in that it
    may not change the type of commodity being transported. But since the
    transfer can still change things about the commodity other than the
    type (loss, gain, time delay, etc.) this class exists to encapsulate
    such changes.
    """
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
