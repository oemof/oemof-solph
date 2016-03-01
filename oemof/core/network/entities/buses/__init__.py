from .. import Bus


class HeatBus(Bus):
    r"""
    A bus containing a temperature and optionally a return temperature.

    Parameters
    ----------
    temperature : float or array-like
        Temperature of the Bus [Kelvin]
    re_temperature : float or array-like
        Return temperature of the Bus [Kelvin]

    """

    def __init__(self, temperature, re_temperature=None, **kwargs):
        super().__init__(**kwargs)
        self.temperature = temperature
        self.re_temperature = re_temperature
