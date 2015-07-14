from .. import Component


class Sink(Component):
    """
    A Sink is special Component which only consumes some source commodity.
    Therefore its list of outputs has to be either None or empty
    (i.e. logically False).
    """
    __lower_name = "sink"

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
    __lower_name = "source"

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
    __lower_name = "transformer"

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

    def emissions(self):
        self.emissions = [o * self.co2_var for o in self.results['Input']]


class Transport(Component):
    """
    A Transport is a simple connection transporting a commodity from one
    Bus to a different one. It is different from a Transformer in that it
    may not change the type of commodity being transported. But since the
    transfer can still change things about the commodity other than the
    type (loss, gain, time delay, etc.) this class exists to encapsulate
    such changes.
    """
    __lower_name = "transport"

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
