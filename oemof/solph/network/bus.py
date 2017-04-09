# -*- coding: utf-8 -*-
"""

"""
import oemof.network as on


class Bus(on.Bus):
    """A balance object. Every node has to be connected to Bus.

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.Bus`

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.balanced = kwargs.get('balanced', True)
