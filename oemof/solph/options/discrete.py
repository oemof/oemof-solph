# -*- coding: utf-8 -*-
"""Optional classes to be added to a network class.
"""

class DiscreteFlow:
    """
    Parameters
    ----------
    integers : boolean
        Specify domain of flow variable: If True, flow is forced to integer
        values.
    """
    def __init__(self, **kwargs):
        # super().__init__(self, **kwargs)
        self.integers = kwargs.get('integers', True)
