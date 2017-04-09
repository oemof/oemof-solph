# -*- coding: utf-8 -*-
"""

"""
import oemof.network as on
from oemof.solph.plumbing import sequence
from oemof.solph.network import Bus


class LinearN1Transformer(on.Transformer):
    """A Linear N:1 Transformer object.

    Parameters
    ----------

    conversion_factors : dict
        Dictionary containing conversion factors for conversion of inflow(s)
        to specified outflow. Keys are output bus objects.
        The dictionary values can either be a scalar or a sequence with length
        of time horizon for simulation.

    Examples
    --------
    Defining an linear transformer:

    >>> gas = Bus()
    >>> biomass = Bus()
    >>> trsf = LinearN1Transformer(conversion_factors={gas: 0.4,
    ...                                                biomass: [1, 2, 3]})
    >>> trsf.conversion_factors[gas][3]
    0.4

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.LinearN1Transformer`
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversion_factors = {
            k: sequence(v)
            for k, v in kwargs.get('conversion_factors', {}).items()}
