import numpy as np

from . import Transformer


class Simple(Transformer):
    """
    Simple Transformers always have a simple input output relation with a
    constant efficiency
    """
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
    """
    lower_name = "simple_chp"

    def __init__(self, **kwargs):
        """
        :param eta: eta as constant efficiency for simple transformer
        """
        super().__init__(**kwargs)
        self.eta = kwargs.get('eta', {'th': None, 'el': None})


class ExtractionCHP(Transformer):
    """
    An ExtractionCHP uses half-space representation to model the P-Q-relation
    # points in p/q diagramm
    *0=(100,0) --
                 -- *2

     *1=(50,0) --
                  -- *3
    """
    lower_name = "simple_extraction_chp"

    def __init__(self, **kwargs):
        """

        """
        super().__init__(**kwargs)
        self.eta_el_max = kwargs.get('eta_el_max', 0.3)
        self.eta_el_min = kwargs.get('eta_el_min', 0.25)
        self.eta_total = kwargs.get('eta_total', 0.8)
        self.out_max = kwargs.get('out_max', 100)
        self.out_min = kwargs.get('out_min', 50)
        self.beta = kwargs.get('beta', [0.15, 0.15])

        p = [self.out_max, self.out_min, None, None]
        q = [0, 0, None, None]
        eta_el = [self.eta_el_max, self.eta_el_min]  # [0.3, 0.25, None, None]
        beta = self.beta
        eta = self.eta_total

        # max / min fuel consumption
        h = [p[0]/eta_el[0], p[1]/eta_el[1]]

        q[2] = (h[0]*eta - p[0]) / (1-beta[0])
        q[3] = (h[1]*eta - p[1]) / (1-beta[1])

        # elctrical power in point 2,3  with: P = P0 - S * Q
        p[2] = p[0] - beta[0] * q[2]
        p[3] = p[1] - beta[1] * q[3]

        # determine coefficients for constraint
        a = np.array([[1, q[2]], [1, q[3]]])
        b = np.array([p[2], p[3]])
        self.c = np.linalg.solve(a, b)

        # determine coeffcients for fuel consumption
        a = np.array([[1, p[0], 0], [1, p[1], 0], [1, p[2], q[2]]])
        b = np.array([h[0], h[1], h[0]])
        self.k = np.linalg.solve(a, b)
        self.p = p


class Storage(Transformer):
    """
    """
    lower_name = "simple_storage"

    def __init__(self, **kwargs):
        """
        :param soc_max: maximal sate of charge
        """
        super().__init__(**kwargs)

        self.soc_max = kwargs.get('soc_max', None)
        self.soc_min = kwargs.get('soc_min', None)
        self.eta_in = kwargs.get('eta_in', 1)
        self.eta_out = kwargs.get('eta_out', 1)
        self.cap_loss = kwargs.get('cap_loss', 0)
