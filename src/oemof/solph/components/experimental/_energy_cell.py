# from oemof.network import network as on
from oemof.solph._energy_system import EnergySystem


class EnergyCell(EnergySystem):
    """
    This is a facade for an EnergySystem. It does not provide any additional
    functionality and it is used purely to prevent misconceptions.

    This also means, that every energy system can be regarded as an energy cell.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
