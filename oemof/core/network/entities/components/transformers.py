
from . import Transformer
import logging

class Simple(Transformer):
    """
    Simple Transformers always have a simple input output relation with a
    constant efficiency

    For individual modeling the model_param variable can be altered. The
    following options (select by string) are available. Some of them
    are obligatory.

    Parameters:
    -------------
    objective: 'opex_var','opex_fix', 'fuel_ex', 'rsell',
    linear_constr: 'io_relation', 'out_max', 'in_max', 'ramping'
    milp_constr: 'out_min', 'in_min', 'ramping', 'startup', 'shutdown'
    investment: True v False

    Note that some options (e.g. 'startup') lead to implicit/automatic creation
    of objective expression terms. Respectively some options yield correct
    models in combination with others. For details look at
    OptimizationModel.simple_transformer_assembler() in the oemof/solph module.
    """
    model_param = {'linear_constr': ('io_relation', 'out_max'),
                   'milp_constr' : (),
                   'objective' : ('opex_var', 'opex_fix', 'fuel_ex', 'rsell'),
                   'investment': False}
    lower_name = 'simple_transformer'

    def __init__(self, **kwargs):
        """
        :param eta: eta as constant efficiency for simple transformer
        """
        super().__init__(**kwargs)
        self.eta = kwargs.get('eta', None)


class CHP(Transformer):
    """
    A CombinedHeatPower Transformer always has a simple input output relation
    with a constant efficiency

    For individual modeling the model_param variable can be altered. The
    following options (select by string) are available. Some of them
    are obligatory.

    Parameters:
    -------------
    objective: 'opex_var','opex_fix', 'fuel_ex', 'rsell',
    linear_constr: 'io_relation', 'simple_chp_relation', 'out_max', 'in_max',
                   'ramping',
    milp_constr: 'out_min', 'in_min', 'ramping', 'startup', 'shutdown'
    investment: True v False

    Note that some options (e.g. 'startup') lead to implicit/automatic creation
    of objective expression terms. Similarly some options only yield correct
    models in combination with other options set.
    For details look at OptimizationModel.simple_chp_assembler() in
    """
    model_param = {'linear_constr': ('io_relation', 'out_max',
                                     'simple_chp_relation'),
                   'milp_constr' : (),
                   'objective' : ('opex_var', 'opex_fix', 'fuel_ex', 'rsell'),
                   'investment': False}
    lower_name = "simple_chp"

    def __init__(self, **kwargs):
        """
        :param eta: eta as constant efficiency for simple transformer
        """
        super().__init__(**kwargs)
        self.eta = kwargs.get('eta', [None, None])

class SimpleExtractionCHP(Transformer):
    """
    Class for combined heat and power unit with extraction turbine and constant
    power to heat coeffcient in backpressure mode

    For individual modeling the model_param variable can be altered. The
    following options (select by string) are available. Some of them
    are obligatory.

    Parameters:
    -------------
    objective: 'opex_var','opex_fix', 'fuel_ex', 'rsell',
    linear_constr: 'io_relation', 'simple_extraction_relation', 'out_max',
                   'in_max', 'ramping',
    milp_constr: 'out_min', 'in_min', 'ramping', 'startup', 'shutdown'
    investment:  False (no investment possible for chp extraction turbines)

    Note that some options (e.g. 'startup') lead to implicit/automatic creation
    of objective expression terms. Similarly some options only yield correct
    models in combination with other options set.
    For details look at OptimizationModel.simple_extraction_chp_assembler() in
    the oemof/solph module.
    """
    model_param = {'linear_constr': ('in_max', 'out_max',
                                     'simple_extraction_relation'),
                   'milp_constr' : (),
                   'objective' : ('opex_var', 'opex_fix', 'fuel_ex', 'rsell'),
                   'investment': False}
    lower_name = "simple_extraction_chp"

    def __init__(self, **kwargs):
        """
        Parameters:
        -----------
        eta_el_cond : constant el. efficiency for transformer in condesing mode
        beta : power loss index
        sigma : power to heat ratio P/Q in backpressure mode
        """
        super().__init__(**kwargs)
        self.eta_el = kwargs.get('eta_el_cond', None)
        self.beta = kwargs.get('beta', None)
        self.sigma = kwargs.get('sigma', None)


class Storage(Transformer):
    """
    """
    model_param = {'investment': False}
    lower_name = "simple_storage"

    def __init__(self, **kwargs):
        """
        Parameters:
        -----------
        cap_max : maximal sate of charge
        cap_min : minimum state of charge
        cap_initial : state of charge at timestep 0 (default cap_max*0.5)
        add_cap_limit : limit of additional installed capacity (only investment
        models)
        eta_in : efficiency at charging
        eta_out : efficiency at discharging
        cap_loss : capacity loss per timestep in p/100
        c_rate_in : c-rate for charging (unit is s^-1)
        c_rate_out : c-rate for discharging (unit is s^-1)
        """
        super().__init__(**kwargs)

        self.cap_max = kwargs.get('cap_max', None)
        self.cap_min = kwargs.get('cap_min', None)
        self.add_cap_limit = kwargs.get('add_cap_limit', None)
        self.cap_initial = kwargs.get('cap_initial', None)
        if self.cap_initial is None:
            self.cap_initial = self.cap_max*0.5
            logging.info('No initial storage capacity set. Setting capacity to' +
                         ' 0.5 of max. capacity for component: %s', self.uid)
        self.eta_in = kwargs.get('eta_in', 1)
        self.eta_out = kwargs.get('eta_out', 1)
        self.cap_loss = kwargs.get('cap_loss', 0)
        self.c_rate_in = kwargs.get('c_rate_in', None)
        self.c_rate_out = kwargs.get('c_rate_out', None)
