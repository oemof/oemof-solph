from . import Source


class FixedSource(Source):
    """
    A fixed source only has one output always. The value of the output is fixed
    for all timesteps in the timehorizon of the optimization problem.
    """
    optimization_options = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DispatchSource(Source):
    """ Dispatch sources only have one output (like FixedSource) but the
    output can be reduced inside the optimization problem.
    """
    optimization_options = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# TODO: Implement constraints etc. for Commodity()
class Commodity(Source):
    """ The commodity component can be used to model inputs to resource busses.
    At the moment no constraint etc. are implemented for this component.
    """
    optimization_options = {}

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.sum_out_limit = kwargs.get('sum_out_limit', float('+inf'))
        self.out_max = kwargs.get('out_max', [10e10])