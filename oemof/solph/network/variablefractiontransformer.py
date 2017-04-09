# -*- coding: utf-8 -*-
"""

"""
from oemof.solph.network import LinearTransformer
from oemof.solph.plumbing import sequence
from oemof.solph.network import Bus
from oemof.solph.flows import Flow


class VariableFractionTransformer(LinearTransformer):
    """A linear transformer with more than one output, where the fraction of
    the output flows is variable. By now it is restricted to two output flows.

    One main output flow has to be defined and is tapped by the remaining flow.
    Thus, the main output will be reduced if the tapped output increases.
    Therefore a loss index has to be defined. Furthermore a maximum efficiency
    has to be specified if the whole flow is led to the main output
    (tapped_output = 0). The state with the maximum tapped_output is described
    through conversion factors equivalent to the LinearTransformer.

    Parameters
    ----------
    conversion_factors : dict
        Dictionary containing conversion factors for conversion of inflow
        to specified outflow. Keys are output bus objects.
        The dictionary values can either be a scalar or a sequence with length
        of time horizon for simulation.
    conversion_factor_single_flow : dict
        The efficiency of the main flow if there is no tapped flow. Only one
        key is allowed. Use one of the keys of the conversion factors. The key
        indicates the main flow. The other output flow is the tapped flow.

    Examples
    --------
    >>> bel = Bus(label='electricityBus')
    >>> bth = Bus(label='heatBus')
    >>> bgas = Bus(label='commodityBus')
    >>> vft = VariableFractionTransformer(
    ...    label='variable_chp_gas',
    ...    inputs={bgas: Flow(nominal_value=10e10)},
    ...    outputs={bel: Flow(), bth: Flow()},
    ...    conversion_factors={bel: 0.3, bth: 0.5},
    ...    conversion_factor_single_flow={bel: 0.5})

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.VariableFractionTransformer`
    """
    def __init__(self, conversion_factor_single_flow, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversion_factor_single_flow = {
            k: sequence(v) for k, v in conversion_factor_single_flow.items()}
