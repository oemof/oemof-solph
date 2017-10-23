# -*- coding: utf-8 -
"""
This module is designed to hold custom components with their classes and
associated individual constraints (blocks) and groupings. Therefore this
module holds the class definition and the block directly located by each other.
"""

from pyomo.core.base.block import SimpleBlock
from pyomo.environ import (Binary, Set, NonNegativeReals, Var, Constraint,
                           Expression, BuildAction)
import numpy as np
import warnings
from oemof.network import Bus, Transformer
from oemof.solph import Flow
from .options import Investment
from .plumbing import sequence


# ------------------------------------------------------------------------------
# Start of generic CAES component
# ------------------------------------------------------------------------------

class GenericCAES(Transformer):
    """
    Component `GenericCAES` to model arbitrary compressed air energy storages.

    The full set of equations is described in:
    Kaldemeyer, C.; Boysen, C.; Tuschy, I.
    A Generic Formulation of Compressed Air Energy Storage as
    Mixed Integer Linear Program – Unit Commitment of Specific
    Technical Concepts in Arbitrary Market Environments
    Materials Today: Proceedings 00 (2018) 0000–0000
    [currently in review]

    Parameters
    ----------
    fuel_input : dict
        Dictionary with key-value-pair of `oemof.Bus` and `oemof.Flow` object
        for the fuel input.
    electrical_output : dict
        Dictionary with key-value-pair of `oemof.Bus` and `oemof.Flow` object
        for the electrical output.
    heat_output : dict
        Dictionary with key-value-pair of `oemof.Bus` and `oemof.Flow` object
        for the electrical output.

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.GenericCAES`
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fuel_input = kwargs.get('fuel_input')
        self.electrical_output = kwargs.get('electrical_output')
        self.heat_output = kwargs.get('electrical_output')
        self.params = kwargs.get('params')

# ------------------------------------------------------------------------------
# End of generic CAES component
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Start of CAES block
# ------------------------------------------------------------------------------

class GenericCAESBlock(SimpleBlock):
    """Block for nodes of class:`.GenericCAES`."""

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """
        Create constraints for GenericCAESBlock.

        Parameters
        ----------
        group : list
            List containing `.GenericCAES` objects.
            e.g. groups=[gcaes1, gcaes2,..]
        """
        m = self.parent_block()

        if group is None:
            return None

        self.GENERICCAES = Set(initialize=[n for n in group])

        # variables
        self.H_F = Var(self.GENERICCAES, m.TIMESTEPS, within=NonNegativeReals)

        def _h_flow_connection_rule(block, n, t):
            """Link fuel consumption to component inflow."""
            expr = 0
            expr += self.H_F[n, t]
            expr += - m.flow[list(n.fuel_input.keys())[0], n, t]
            return expr == 0
        self.h_flow_connection = Constraint(self.GENERICCAES, m.TIMESTEPS,
                                            rule=_h_flow_connection_rule)

# ------------------------------------------------------------------------------
# End of CAES block
# ------------------------------------------------------------------------------


def custom_grouping(node):
    if isinstance(node, GenericCAES):
        return GenericCAESBlock
