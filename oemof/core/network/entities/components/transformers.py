from . import Transformer
import logging
import numpy as np


class Simple(Transformer):
    """
    Simple Transformers always have a simple input output relation with a
    constant efficiency

    Parameters
    ----------
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


class TwoInputsOneOutput(Simple):
    r"""
    A transformer with one output and two input flows

    The two input flows are connect by the factor f. This transformer might
    represent components such as heat pumps and instant flow heater.

    Parameters
    ----------
    eta : list
        Constant effciency for converting the incoming flows to the internal
        input flows. The first element of eta is the efficiency of the first
        element of inputs and so on. If not set the effciency will be one. You
        have to define both elements or no element.
    f : array-like
        A relation-factor between the first and the second input flow.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.eta = kwargs.get('eta', [1, 1])
        self.f = kwargs.get('f')


class CHP(Transformer):
    """
    A CombinedHeatPower Transformer always has a simple input output relation
    with a constant efficiency

    Parameters
    ----------
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

class VariableEfficiencyCHP(CHP):
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
        b = np.array([self.in_min[0], self.in_max[0]])
        self.coeff = np.linalg.solve(A, b)


class SimpleExtractionCHP(CHP):
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
        self.eta_el_cond = kwargs.get('eta_el_cond', self.eta[0])
        self.beta = kwargs.get('beta')
        self.sigma = kwargs.get('sigma')

        if self.in_max is None:
            try:
                self.in_max = [self.out_max[0]/self.eta_el_cond]
            except:
                raise ValueError('Missing attribute "in_max" for object: \n' +
                                 str(type(self)) + 'Auto calculation failed!')
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
        absolut maximum state of charge if invest=FALSE,
        absolut maximum state of charge of built capacity if invest=TRUE
    cap_min : float
        absolut minimum state of charge
    cap_initial : float, optional
        The state of charge (soc) at timestep 0.
    add_cap_limit : float
        limit of additional installed capacity (only investment models)
    eta : list (optional)
       constant efficiency for charging, discharging
       input e.g. eta = [0.9, 0.9]
    eta_in : float
        efficiency at charging
    eta_out : float
        efficiency at discharging
    cap_loss : float or list/pandas.Series with length of simulation timesteps
        capacity loss per timestep in p/100
    c_rate_in : float
        c-rate for charging (unit is s^-1)
    c_rate_out : float
        c-rate for discharging (unit is s^-1)
    """
    optimization_options = {}

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.cap_max = kwargs.get('cap_max', 0)
        self.cap_min = kwargs.get('cap_min', None)
        self.add_cap_limit = kwargs.get('add_cap_limit', None)
        self.cap_initial = kwargs.get('cap_initial', None)
        self.eta_in = kwargs.get('eta_in', 1)
        self.eta_out = kwargs.get('eta_out', 1)
        self.cap_loss = kwargs.get('cap_loss', 0)
        self.c_rate_in = kwargs.get('c_rate_in', None)
        self.c_rate_out = kwargs.get('c_rate_out', None)
        self.eta = kwargs.get('eta')

        if isinstance(self.eta, list):
            self.eta_in = self.eta[0]
            self.eta_out = self.eta[1]

        if not self.optimization_options.get('investment'):
            if self.cap_max == 0:
                logging.info('Storage cap_max set to default value of 0')
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

        if self.optimization_options.get('investment'):
            if self.c_rate_in is None:
                raise ValueError('Missing value for c_rate_in!')
            if self.c_rate_out is None:
                raise ValueError('Missing value for c_rate_out!')
