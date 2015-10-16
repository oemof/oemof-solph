
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


class Storage(Transformer):
    """
    """
    lower_name = "simple_storage"

    def __init__(self, **kwargs):
        """
        Parameters:
        -----------
        soc_max : maximal sate of charge
        soc_min : minimum state of charge
        soc_initial : state of charge at timestep 0 (default soc_max*0.5)
        add_cap_limit : limit of additional installed capacity (only investment
        models)
        eta_in : efficiency at charging
        eta_out : efficiency at discharging
        cap_loss : capacity loss per timestep in p/100
        c_rate_in : c-rate for charging (unit is s^-1)
        c_rate_out : c-rate for discharging (unit is s^-1)
        """
        super().__init__(**kwargs)

        self.soc_max = kwargs.get('soc_max', None)
        self.soc_min = kwargs.get('soc_min', None)
        self.add_cap_limit = kwargs.get('cap_limit', None)
        self.soc_initial = kwargs.get('soc_initial', self.soc_max*0.5)
        self.eta_in = kwargs.get('eta_in', 1)
        self.eta_out = kwargs.get('eta_out', 1)
        self.cap_loss = kwargs.get('cap_loss', 0)
        self.c_rate_in = next(iter(self.in_max.values())) / self.soc_max
        self.c_rate_out = next(iter(self.out_max.values())) / self.soc_max
