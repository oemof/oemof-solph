# -*- coding: utf-8 -
"""
This module is designed to hold custom components with their classes and
associated individual constraints (blocks) and groupings. Therefore this
module holds the class definition and the block directly located by each other.
"""

from pyomo.core.base.block import SimpleBlock
from pyomo.environ import (Binary, Set, NonNegativeReals, Var, Constraint,
                           Expression, BuildAction)
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
    electrical_input : dict
        Dictionary with key-value-pair of `oemof.Bus` and `oemof.Flow` object
        for the electrical input.
    fuel_input : dict
        Dictionary with key-value-pair of `oemof.Bus` and `oemof.Flow` object
        for the fuel input.
    electrical_output : dict
        Dictionary with key-value-pair of `oemof.Bus` and `oemof.Flow` object
        for the electrical output.

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.GenericCAES`
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.electrical_input = kwargs.get('electrical_input')
        self.fuel_input = kwargs.get('fuel_input')
        self.electrical_output = kwargs.get('electrical_output')
        self.params = kwargs.get('params')

        # map specific flows to standard API
        self.inputs.update(kwargs.get('electrical_input'))
        self.inputs.update(kwargs.get('fuel_input'))
        self.outputs.update(kwargs.get('electrical_output'))

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

        # Compression: Binary variable for operation status
        self.cmp_st = Var(self.GENERICCAES, m.TIMESTEPS, within=Binary)

        # Compression: Realized capacity
        self.cmp_p = Var(self.GENERICCAES, m.TIMESTEPS,
                         within=NonNegativeReals)

        # Compression: Max. Capacity
        self.cmp_p_max = Var(self.GENERICCAES, m.TIMESTEPS,
                             within=NonNegativeReals)

        # Compression: Heat flow
        self.cmp_q_out_sum = Var(self.GENERICCAES, m.TIMESTEPS,
                                 within=NonNegativeReals)

        # Compression: Waste heat
        self.cmp_q_waste = Var(self.GENERICCAES, m.TIMESTEPS,
                               within=NonNegativeReals)

        # Expansion: Binary variable for operation status
        self.exp_st = Var(self.GENERICCAES, m.TIMESTEPS, within=Binary)

        # Expansion: Realized capacity
        self.exp_p = Var(self.GENERICCAES, m.TIMESTEPS,
                         within=NonNegativeReals)

        # Expansion: Max. Capacity
        self.exp_p_max = Var(self.GENERICCAES, m.TIMESTEPS,
                             within=NonNegativeReals)

        # Expansion: Heat flow of natural gas co-firing
        self.exp_q_in_sum = Var(self.GENERICCAES, m.TIMESTEPS,
                                within=NonNegativeReals)

        # Expansion: Heat flow of natural gas co-firing
        self.exp_q_fuel_in = Var(self.GENERICCAES, m.TIMESTEPS,
                                 within=NonNegativeReals)

        # Expansion: Heat flow of additional firing
        self.exp_q_add_in = Var(self.GENERICCAES, m.TIMESTEPS,
                                within=NonNegativeReals)

        # Cavern: Filling levelh
        self.cav_level = Var(self.GENERICCAES, m.TIMESTEPS,
                             within=NonNegativeReals)

        # Cavern: Energy inflow
        self.cav_e_in = Var(self.GENERICCAES, m.TIMESTEPS,
                            within=NonNegativeReals)

        # Cavern: Energy outflow
        self.cav_e_out = Var(self.GENERICCAES, m.TIMESTEPS,
                             within=NonNegativeReals)

        # TES: Filling levelh
        self.tes_level = Var(self.GENERICCAES, m.TIMESTEPS,
                             within=NonNegativeReals)

        # TES: Energy inflow
        self.tes_e_in = Var(self.GENERICCAES, m.TIMESTEPS,
                            within=NonNegativeReals)

        # TES: Energy outflow
        self.tes_e_out = Var(self.GENERICCAES, m.TIMESTEPS,
                             within=NonNegativeReals)

        # Spot market: Positive capacity
        self.exp_p_spot = Var(self.GENERICCAES, m.TIMESTEPS,
                              within=NonNegativeReals)

        # Spot market: Negative capacity
        self.cmp_p_spot = Var(self.GENERICCAES, m.TIMESTEPS,
                              within=NonNegativeReals)

        # Compression: Capacity on markets
        def cmp_p_constr_rule(block, n, t):
            expr = 0
            expr += -self.cmp_p[n, t]
            expr += m.flow[list(n.electrical_input.keys())[0], n, t]
            return expr == 0
        self.cmp_p_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_p_constr_rule)

        # Compression: Max. capacity depending on cavern filling level
        def cmp_p_max_constr_rule(block, n, t):
            if t != 0:
                return (self.cmp_p_max[n, t] ==
                        n.params['cmp_p_max_m'] * self.cav_level[n, t-1] +
                        n.params['cmp_p_max_b'])
            else:
                return (self.cmp_p_max[n, t] == n.params['cmp_p_max_b'])
        self.cmp_p_max_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_p_max_constr_rule)

        def cmp_p_max_area_constr_rule(block, n, t):
            return (self.cmp_p[n, t] <= self.cmp_p_max[n, t])
        self.cmp_p_max_area_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_p_max_area_constr_rule)

        # Compression: Status of operation (on/off)
        def cmp_st_p_min_constr_rule(block, n, t):
            return (
                self.cmp_p[n, t] >= n.params['cmp_p_min'] * self.cmp_st[n, t])
        self.cmp_st_p_min_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_st_p_min_constr_rule)

        def cmp_st_p_max_constr_rule(block, n, t):
            return (self.cmp_p[n, t] <=
                    (n.params['cmp_p_max_m'] * n.params['cav_level_max'] +
                    n.params['cmp_p_max_b']) * self.cmp_st[n, t])
        self.cmp_st_p_max_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_st_p_max_constr_rule)

        # Compression: Heat flow out
        def cmp_q_out_constr_rule(block, n, t):
            return (self.cmp_q_out_sum[n, t] ==
                    n.params['cmp_q_out_m'] * self.cmp_p[n, t] +
                    n.params['cmp_q_out_b'] * self.cmp_st[n, t])
        self.cmp_q_out_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_q_out_constr_rule)

        # Compression: Definition of single heat flows
        def cmp_q_out_sum_constr_rule(block, n, t):
            return (self.cmp_q_out_sum[n, t] == self.cmp_q_waste[n, t] +
                    self.tes_e_in[n, t])
        self.cmp_q_out_sum_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_q_out_sum_constr_rule)

        # Compression: Heat flow out ratio
        def cmp_q_out_shr_constr_rule(block, n, t):
            return (self.cmp_q_waste[n, t] * n.params['cmp_q_tes_share'] ==
                    self.tes_e_in[n, t] * (1 - n.params['cmp_q_tes_share']))
        self.cmp_q_out_shr_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_q_out_shr_constr_rule)

        # Expansion: Capacity on markets
        def exp_p_constr_rule(block, n, t):
            expr = 0
            expr += -self.exp_p[n, t]
            expr += m.flow[n, list(n.electrical_output.keys())[0], t]
            return expr == 0
        self.exp_p_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_p_constr_rule)

        # Expansion: Max. capacity depending on cavern filling level
        def exp_p_max_constr_rule(block, n, t):
            if t != 0:
                return (self.exp_p_max[n, t] ==
                        n.params['exp_p_max_m'] * self.cav_level[n, t-1] +
                        n.params['exp_p_max_b'])
            else:
                return (self.exp_p_max[n, t] == n.params['exp_p_max_b'])
        self.exp_p_max_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_p_max_constr_rule)

        def exp_p_max_area_constr_rule(block, n, t):
            return (self.exp_p[n, t] <= self.exp_p_max[n, t])
        self.exp_p_max_area_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_p_max_area_constr_rule)

        # Expansion: Status of operation (on/off)
        def exp_st_p_min_constr_rule(block, n, t):
            return (
                self.exp_p[n, t] >= n.params['exp_p_min'] * self.exp_st[n, t])
        self.exp_st_p_min_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_st_p_min_constr_rule)

        def exp_st_p_max_constr_rule(block, n, t):
            return (self.exp_p[n, t] <=
                    (n.params['exp_p_max_m'] * n.params['cav_level_max'] +
                     n.params['exp_p_max_b']) * self.exp_st[n, t])
        self.exp_st_p_max_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_st_p_max_constr_rule)

        # Expansion: Heat flow in
        def exp_q_in_constr_rule(block, n, t):
            return (self.exp_q_in_sum[n, t] ==
                    n.params['exp_q_in_m'] * self.exp_p[n, t] +
                    n.params['exp_q_in_b'] * self.exp_st[n, t])
        self.exp_q_in_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_q_in_constr_rule)

        # Expansion: Fuel allocation
        def exp_q_fuel_constr_rule(block, n, t):
            expr = 0
            expr += -self.exp_q_fuel_in[n, t]
            expr += m.flow[list(n.fuel_input.keys())[0], n, t]
            return expr == 0
        self.exp_q_fuel_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_q_fuel_constr_rule)

        # Expansion: Definition of single heat flows
        def exp_q_in_sum_constr_rule(block, n, t):
            return (self.exp_q_in_sum[n, t] == self.exp_q_fuel_in[n, t] +
                    self.tes_e_out[n, t] + self.exp_q_add_in[n, t])
        self.exp_q_in_sum_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_q_in_sum_constr_rule)

        # Expansion: Heat flow in ratio
        def exp_q_in_shr_constr_rule(block, n, t):
            return (n.params['exp_q_tes_share'] * self.exp_q_fuel_in[n, t] ==
                    (1 - n.params['exp_q_tes_share']) *
                    (self.exp_q_add_in[n, t] + self.tes_e_out[n, t]))
        self.exp_q_in_shr_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_q_in_shr_constr_rule)

        # Cavern: Energy inflow
        def cav_e_in_constr_rule(block, n, t):
            return (self.cav_e_in[n, t] ==
                    n.params['cav_e_in_m'] * self.cmp_p[n, t] +
                    n.params['cav_e_in_b'])
        self.cav_e_in_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cav_e_in_constr_rule)

        # Cavern: Energy outflow
        def cav_e_out_constr_rule(block, n, t):
            return (self.cav_e_out[n, t] ==
                    n.params['cav_e_out_m'] * self.exp_p[n, t] +
                    n.params['cav_e_out_b'])
        self.cav_e_out_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cav_e_out_constr_rule)

        # Cavern: Storage balance
        def cav_eta_constr_rule(block, n, t):
            if t != 0:
                return (n.params['cav_eta_temp'] * self.cav_level[n, t] ==
                        self.cav_level[n, t-1] + m.timeincrement[t] *
                        (self.cav_e_in[n, t] - self.cav_e_out[n, t]))
            else:
                return (n.params['cav_eta_temp'] * self.cav_level[n, t] ==
                        m.timeincrement[t] *
                        (self.cav_e_in[n, t] - self.cav_e_out[n, t]))
        self.cav_eta_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cav_eta_constr_rule)

        # Cavern: Upper bound
        def cav_ub_constr_rule(block, n, t):
            return (self.cav_level[n, t] <= n.params['cav_level_max'])
        self.cav_ub_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cav_ub_constr_rule)

        # TES: Storage balance
        def tes_eta_constr_rule(block, n, t):
            if t != 0:
                return (self.tes_level[n, t] ==
                        self.tes_level[n, t-1] + m.timeincrement[t] *
                        (self.tes_e_in[n, t] - self.tes_e_out[n, t]))
            else:
                return (self.tes_level[n, t] ==
                        m.timeincrement[t] *
                        (self.tes_e_in[n, t] - self.tes_e_out[n, t]))
        self.tes_eta_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=tes_eta_constr_rule)

        # TES: Upper bound
        def tes_ub_constr_rule(block, n, t):
            return (self.tes_level[n, t] <= n.params['tes_level_max'])
        self.tes_ub_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=tes_ub_constr_rule)

# ------------------------------------------------------------------------------
# End of CAES block
# ------------------------------------------------------------------------------


def custom_grouping(node):
    """Add groupings for all components which is added in `models.py`."""
    if isinstance(node, GenericCAES):
        return GenericCAESBlock
