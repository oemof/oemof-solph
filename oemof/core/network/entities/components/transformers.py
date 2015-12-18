
from . import Transformer
import logging
import numpy as np


class Simple(Transformer):
    """
    Simple Transformers always have a simple input output relation with a
    constant efficiency

    Parameters
    -----------

    eta : list
       constant efficiency for conversion of input into output (0 <= eta <= 1)
       e.g. eta = [0.4]
    """
    optimization_options = {}

    def __init__(self, **kwargs):
        """
        """
        super().__init__(**kwargs)
        self.eta = kwargs.get('eta', None)


class CHP(Transformer):
    """
    A CombinedHeatPower Transformer always has a simple input output relation
    with a constant efficiency

    Parameters
    -----------

    eta : list
      constant effciency for converting input into output. First element of
      list is used for conversion of input into first element of
      attribute `outputs`. Second element for second element of attribute
      `outputs`. E.g. eta = [0.3, 0.4]

    """
    optimization_options = {}

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.eta = kwargs.get('eta', [None, None])

class VariableEfficiencyCHP(Transformer):
    """
    A CombinedHeatPower Transformer with variable electrical efficiency
    Note: The model uses constraints which require binary variables, hence
    objects of this class will results in mixed-integer-linear-problems.

    Parameters
    ----------
    eta_total : float
        total constant efficiency for the transformer
    eta_el : list
        list containing the minimial (first element) and maximal (second element)
        electrical efficiency (0 <= eta_el <= 1)


    """
    optimization_options = {}

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.eta_total = kwargs.get('eta_total')
        self.eta_el = kwargs.get('eta_el')

        # calculate minimal
        self.in_min = [self.out_min[0] / self.eta_el[0]]
        self.in_max = [self.out_max[0] / self.eta_el[1]]

        A = np.array([[1, self.out_min[0]],
                      [1, self.out_max[0]]])
        b = np.array([self.in_min[0],
                      self.in_max[0]])
        self.coeff = np.linalg.solve(A, b)


class SimpleExtractionCHP(Transformer):
    """
    Class for combined heat and power unit with extraction turbine and constant
    power to heat coeffcient in backpressure mode

    Parameters
    ----------
    eta_el_cond : float
        constant el. efficiency for transformer in condensing mode
    beta : float
        power loss index
    sigma : float
        power to heat ratio P/Q in backpressure mode
    """
    optimization_options = {}

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.eta_el_cond = kwargs.get('eta_el_cond')
        self.beta = kwargs.get('beta')
        self.sigma = kwargs.get('sigma')

        if self.in_max is None:
            raise ValueError('Missing attribute "in_max" for object: \n' +
                             str(type(self)))
        if self.eta_el_cond is None:
            raise ValueError('Missing attribute "eta_el_cond" for object: \n' +
                             str(type(self)))
        if self.beta is None:
            raise ValueError('Missing attribute "beta" for object: \n' +
                             str(type(self)))
        if self.sigma is None:
            raise ValueError('Missing attribute "sigma" for object: \n' +
                             str(type(self)))


class Storage(Transformer):
    """
    Parameters
    ----------
    cap_max : float
        absolut maximal sate of charge
    cap_min : float
        absolut minimum state of charge
    cap_initial : float
        state of charge at timestep 0 (default cap_max*0.5)
    add_cap_limit : float
        limit of additional installed capacity (only investment models)
    eta_in : float
        efficiency at charging
    eta_out : float
        efficiency at discharging
    cap_loss : float
        capacity loss per timestep in p/100
    c_rate_in : float
        c-rate for charging (unit is s^-1)
    c_rate_out : float
        c-rate for discharging (unit is s^-1)
    """
    optimization_options = {}

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.cap_max = kwargs.get('cap_max', None)
        self.cap_min = kwargs.get('cap_min', None)
        self.add_cap_limit = kwargs.get('add_cap_limit', None)
        self.cap_initial = kwargs.get('cap_initial', None)
        if self.cap_initial is None:
            self.cap_initial = self.cap_max*0.5
            logging.info('No initial storage capacity set. Setting capacity ' +
                         'to 0.5 of max. capacity for component: %s', self.uid)
        self.eta_in = kwargs.get('eta_in', 1)
        self.eta_out = kwargs.get('eta_out', 1)
        self.cap_loss = kwargs.get('cap_loss', 0)
        self.c_rate_in = kwargs.get('c_rate_in', None)
        self.c_rate_out = kwargs.get('c_rate_out', None)

        if self.out_max is None:
            try:
                self.out_max = [self.c_rate_out * self.cap_max]
            except:
                raise ValueError('Failed to set out_max automatically.' +
                                 'Did you specify c_rate_out and cap_max?')
        if self.in_max is None:
            try:
                self.in_max = [self.c_rate_in * self.cap_max]
            except:
                raise ValueError('Failed to set in_max automatically.' +
                                 'Did you specify c_rate_out and cap_max?')
