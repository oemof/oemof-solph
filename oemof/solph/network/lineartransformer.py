# -*- coding: utf-8 -*-
"""

"""
import oemof.network as on
from oemof.solph.plumbing import sequence
from oemof.solph.network import Bus
from oemof.solph.flows import Flow


class LinearTransformer(on.Transformer):
    """A Linear Transformer object.

    Parameters
    ----------
    conversion_factors : dict
        Dictionary containing conversion factors for conversion of inflow
        to specified outflow. Keys are output bus objects.
        The dictionary values can either be a scalar or a sequence with length
        of time horizon for simulation.

    Examples
    --------
    Defining an linear transformer:

    >>> bel = Bus()
    >>> bth = Bus()
    >>> bng = Bus()
    >>> trsf = LinearTransformer(conversion_factors={bel: 0.4,
    ...                                              bth: [1, 2, 3]},
    ...                          inputs={bng: Flow()})
    >>> trsf.conversion_factors[bel][3]
    0.4

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.LinearTransformer`
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversion_factors = {
            k: sequence(v)
            for k, v in kwargs.get('conversion_factors', {}).items()}
