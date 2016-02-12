from .. import Bus
from


class HeatBuse(Bus):
    r"""
    Parameters
    ----------
    temp_kelvin : float or array-like
        Temperature of the Bus

    """

    def __init__(self, temp_kelvin, **kwargs):
        super().__init__(**kwargs)
        self.temp_kelvin = temp_kelvin
