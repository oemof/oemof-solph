from . import Source


class FixedSource(Source):
    """
    A fixed source only has one output always. The value of the output is fixed
    for all timesteps in the timehorizon of the optimization problem.

    For individual modeling of the objective function the items of
    model_param['objective'] can be altered. Following options are possible:

    'opex_var', 'opex_fix', 'rsell'
    """
    model_param = {'linear_constr': ('fixvalue'),
                   'milp_constr' : (),
                   'objective' : ('opex_var', 'opex_fix'),
                   'investment': False}
    lower_name = "fixed_source"

    def __init__(self, **kwargs):
        """
        """
        super().__init__(**kwargs)
        self.val = kwargs.get('val', None)

    def calc_emissions(self):
        self.emissions = [0 for o in self.results['out'][self.outputs[0].uid]]


class DispatchSource(Source):
    """ Dispatch sources only have one output (like FixedSource) but the
    output can be reduced inside the optimization problem.

    For individual modeling of the objective function the items of
    model_param['objective'] can be altered. Following options are possible:

    'opex_var', 'opex_fix', 'dispatch_ex', 'rsell'

    Dispatch sources are not implemented for investment at the moment.
    """
    model_param = {'linear_constr': ('dispatch'),
                   'milp_constr' : (),
                   'objective' : ('opex_var', 'opex_fix','dispatch_ex'),
                   'investment': False}
    lower_name = "dispatch_source"

    def __init__(self, **kwargs):
        """
        :param boolean dispatch: Flag if RenewableSource is dispatchable or not
        """
        super().__init__(**kwargs)
        self.val = kwargs.get('val', None)
        self.dispatch_ex = kwargs.get('dispatch_ex', 0)

    def calc_emissions(self):
        self.emissions = [0 for o in self.results['out'][self.outputs[0].uid]]

# TODO: Implement constraints etc. for Commodity()
class Commodity(Source):
    """ The commodity component can be used to model inputs to resource busses.
    At the moment no constraint etc. are implemented for this component.

    """
    lower_name = "commodity"
    def __init__(self, **kwargs):
        """
        """
        super().__init__(**kwargs)

