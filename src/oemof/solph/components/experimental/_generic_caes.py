# -*- coding: utf-8 -*-

"""
In-development generic compressed air energy storage.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Patrik Schönfeldt
SPDX-FileCopyrightText: Johannes Röder
SPDX-FileCopyrightText: jakob-wo
SPDX-FileCopyrightText: gplssm
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: Johannes Kochems

SPDX-License-Identifier: MIT

"""

from oemof.network import Node
from pyomo.core.base.block import ScalarBlock
from pyomo.environ import Binary
from pyomo.environ import Constraint
from pyomo.environ import NonNegativeReals
from pyomo.environ import Set
from pyomo.environ import Var


class GenericCAES(Node):
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

    Note: This component is experimental. Use it with care.

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.generic_caes.GenericCAES`

    Examples
    --------

    >>> from oemof import solph
    >>> bel = solph.buses.Bus(label='bel')
    >>> bth = solph.buses.Bus(label='bth')
    >>> bgas = solph.buses.Bus(label='bgas')
    >>> # dictionary with parameters for a specific CAES plant
    >>> concept = {
    ...    'cav_e_in_b': 0,
    ...    'cav_e_in_m': 0.6457267578,
    ...    'cav_e_out_b': 0,
    ...    'cav_e_out_m': 0.3739636077,
    ...    'cav_eta_temp': 1.0,
    ...    'cav_level_max': 211.11,
    ...    'cmp_p_max_b': 86.0918959849,
    ...    'cmp_p_max_m': 0.0679999932,
    ...    'cmp_p_min': 1,
    ...    'cmp_q_out_b': -19.3996965679,
    ...    'cmp_q_out_m': 1.1066036114,
    ...    'cmp_q_tes_share': 0,
    ...    'exp_p_max_b': 46.1294016678,
    ...    'exp_p_max_m': 0.2528340303,
    ...    'exp_p_min': 1,
    ...    'exp_q_in_b': -2.2073411014,
    ...    'exp_q_in_m': 1.129249765,
    ...    'exp_q_tes_share': 0,
    ...    'tes_eta_temp': 1.0,
    ...    'tes_level_max': 0.0}
    >>> # generic compressed air energy storage (caes) plant
    >>> caes = solph.components.experimental.GenericCAES(
    ...    label='caes',
    ...    electrical_input={bel: solph.flows.Flow()},
    ...    fuel_input={bgas: solph.flows.Flow()},
    ...    electrical_output={bel: solph.flows.Flow()},
    ...    params=concept)
    >>> type(caes)
    <class 'oemof.solph.components.experimental._generic_caes.GenericCAES'>
    """

    def __init__(
        self,
        label,
        *,
        electrical_input,
        fuel_input,
        electrical_output,
        params,
        custom_properties=None,
    ):
        super().__init__(
            label=label,
            inputs={},
            outputs={},
            custom_properties=custom_properties,
        )

        self.electrical_input = electrical_input
        self.fuel_input = fuel_input
        self.electrical_output = electrical_output
        self.params = params

        # map specific flows to standard API
        self.inputs.update(electrical_input)
        self.inputs.update(fuel_input)
        self.outputs.update(electrical_output)

    def constraint_group(self):
        return GenericCAESBlock


class GenericCAESBlock(ScalarBlock):
    r"""Block for nodes of class:`.GenericCAES`.

    Note: This component is experimental. Use it with care.

    **The following constraints are created:**

    .. _GenericCAES-equations:

    .. math::
        &
        (1) \qquad P_{cmp}(t) = electrical\_input (t)
            \quad \forall t \in T \\
        &
        (2) \qquad P_{cmp\_max}(t) = m_{cmp\_max} \cdot CAS_{fil}(t-1)
            + b_{cmp\_max}
            \quad \forall t \in\left[1, t_{max}\right] \\
        &
        (3) \qquad P_{cmp\_max}(t) = b_{cmp\_max}
            \quad \forall t \notin\left[1, t_{max}\right] \\
        &
        (4) \qquad P_{cmp}(t) \leq P_{cmp\_max}(t)
            \quad \forall t \in T  \\
        &
        (5) \qquad P_{cmp}(t) \geq P_{cmp\_min} \cdot ST_{cmp}(t)
            \quad \forall t \in T  \\
        &
        (6) \qquad P_{cmp}(t) = m_{cmp\_max} \cdot CAS_{fil\_max}
            + b_{cmp\_max} \cdot ST_{cmp}(t)
            \quad \forall t \in T \\
        &
        (7) \qquad \dot{Q}_{cmp}(t) =
            m_{cmp\_q} \cdot P_{cmp}(t) + b_{cmp\_q} \cdot ST_{cmp}(t)
            \quad \forall t \in T  \\
        &
        (8) \qquad \dot{Q}_{cmp}(t) = \dot{Q}_{cmp_out}(t)
            + \dot{Q}_{tes\_in}(t)
            \quad \forall t \in T \\
        &
        (9) \qquad r_{cmp\_tes} \cdot\dot{Q}_{cmp\_out}(t) =
            \left(1-r_{cmp\_tes}\right) \dot{Q}_{tes\_in}(t)
            \quad \forall t \in T \\
        &
        (10) \quad\; P_{exp}(t) = electrical\_output (t)
             \quad \forall t \in T \\
        &
        (11) \quad\; P_{exp\_max}(t) = m_{exp\_max} CAS_{fil}(t-1)
             + b_{exp\_max}
             \quad \forall t \in\left[1, t_{\max }\right] \\
        &
        (12) \quad\; P_{exp\_max}(t) = b_{exp\_max}
             \quad \forall t \notin\left[1, t_{\max }\right] \\
        &
        (13) \quad\; P_{exp}(t) \leq P_{exp\_max}(t)
             \quad \forall t \in T \\
        &
        (14) \quad\; P_{exp}(t) \geq P_{exp\_min}(t) \cdot ST_{exp}(t)
             \quad \forall t \in T \\
        &
        (15) \quad\; P_{exp}(t) \leq m_{exp\_max} \cdot CAS_{fil\_max}
             + b_{exp\_max} \cdot ST_{exp}(t)
             \quad \forall t \in T \\
        &
        (16) \quad\; \dot{Q}_{exp}(t) = m_{exp\_q} \cdot P_{exp}(t)
             + b_{cxp\_q} \cdot ST_{cxp}(t)
             \quad \forall t \in T \\
        &
        (17) \quad\; \dot{Q}_{exp\_in}(t) = fuel\_input(t)
             \quad \forall t \in T \\
        &
        (18) \quad\; \dot{Q}_{exp}(t) = \dot{Q}_{exp\_in}(t)
             + \dot{Q}_{tes\_out}(t)+\dot{Q}_{cxp\_add}(t)
             \quad \forall t \in T \\
        &
        (19) \quad\; r_{exp\_tes} \cdot \dot{Q}_{exp\_in}(t) =
             (1 - r_{exp\_tes})(\dot{Q}_{tes\_out}(t) + \dot{Q}_{exp\_add}(t))
             \quad \forall t \in T \\
        &
        (20) \quad\; \dot{E}_{cas\_in}(t) = m_{cas\_in}\cdot P_{cmp}(t)
             + b_{cas\_in}\cdot ST_{cmp}(t)
             \quad \forall t \in T \\
        &
        (21) \quad\; \dot{E}_{cas\_out}(t) = m_{cas\_out}\cdot P_{cmp}(t)
             + b_{cas\_out}\cdot ST_{cmp}(t)
             \quad \forall t \in T \\
        &
        (22) \quad\; \eta_{cas\_tmp} \cdot CAS_{fil}(t) = CAS_{fil}(t-1)
             + \tau\left(\dot{E}_{cas\_in}(t) - \dot{E}_{cas\_out}(t)\right)
             \quad \forall t \in\left[1, t_{max}\right] \\
         &
        (23) \quad\; \eta_{cas\_tmp} \cdot CAS_{fil}(t) =
             \tau\left(\dot{E}_{cas\_in}(t) - \dot{E}_{cas\_out}(t)\right)
             \quad \forall t \notin\left[1, t_{max}\right] \\
        &
        (24) \quad\; CAS_{fil}(t) \leq CAS_{fil\_max}
             \quad \forall t \in T \\
        &
        (25) \quad\; TES_{fil}(t) = TES_{fil}(t-1)
             + \tau\left(\dot{Q}_{tes\_in}(t)
             - \dot{Q}_{tes\_out}(t)\right)
             \quad \forall t \in\left[1, t_{max}\right] \\
         &
        (26) \quad\; TES_{fil}(t) =
             \tau\left(\dot{Q}_{tes\_in}(t)
             - \dot{Q}_{tes\_out}(t)\right)
             \quad \forall t \notin\left[1, t_{max}\right] \\
        &
        (27) \quad\; TES_{fil}(t) \leq TES_{fil\_max}
             \quad \forall t \in T \\
        &


    **Table: Symbols and attribute names of variables and parameters**

    .. csv-table:: Variables (V) and Parameters (P)
        :header: "symbol", "attribute", "type", "explanation"
        :widths: 1, 1, 1, 1

        ":math:`ST_{cmp}` ", "`cmp_st[n,t]` ", "V", "Status of
        compression"
        ":math:`{P}_{cmp}` ", "`cmp_p[n,t]`", "V", "Compression power"
        ":math:`{P}_{cmp\_max}`", "`cmp_p_max[n,t]`", "V", "Max.
        compression power"
        ":math:`\dot{Q}_{cmp}` ", "`cmp_q_out_sum[n,t]`", "V", "Summed
        heat flow in compression"
        ":math:`\dot{Q}_{cmp\_out}` ", "`cmp_q_waste[n,t]`", "V", "
        Waste heat flow from compression"
        ":math:`ST_{exp}(t)`", "`exp_st[n,t]`", "V", "Status of
        expansion (binary)"
        ":math:`P_{exp}(t)`", "`exp_p[n,t]`", "V", "Expansion power"
        ":math:`P_{exp\_max}(t)`", "`exp_p_max[n,t]`", "V", "Max.
        expansion power"
        ":math:`\dot{Q}_{exp}(t)`", "`exp_q_in_sum[n,t]`", "V", "
        Summed heat flow in expansion"
        ":math:`\dot{Q}_{exp\_in}(t)`", "`exp_q_fuel_in[n,t]`", "V", "
        Heat (external) flow into expansion"
        ":math:`\dot{Q}_{exp\_add}(t)`", "`exp_q_add_in[n,t]`", "V", "
        Additional heat flow into expansion"
        ":math:`CAV_{fil}(t)`", "`cav_level[n,t]`", "V", "Filling level
        if CAE"
        ":math:`\dot{E}_{cas\_in}(t)`", "`cav_e_in[n,t]`", "V", "
        Exergy flow into CAS"
        ":math:`\dot{E}_{cas\_out}(t)`", "`cav_e_out[n,t]`", "V", "
        Exergy flow from CAS"
        ":math:`TES_{fil}(t)`", "`tes_level[n,t]`", "V", "Filling
        level of Thermal Energy Storage (TES)"
        ":math:`\dot{Q}_{tes\_in}(t)`", "`tes_e_in[n,t]`", "V", "Heat
        flow into TES"
        ":math:`\dot{Q}_{tes\_out}(t)`", "`tes_e_out[n,t]`", "V", "Heat
        flow from TES"
        ":math:`b_{cmp\_max}`", "`cmp_p_max_b[n,t]`", "P", "Specific
        y-intersection"
        ":math:`b_{cmp\_q}`", "`cmp_q_out_b[n,t]`", "P", "Specific
        y-intersection"
        ":math:`b_{exp\_max}`", "`exp_p_max_b[n,t]`", "P", "Specific
        y-intersection"
        ":math:`b_{exp\_q}`", "`exp_q_in_b[n,t]`", "P", "Specific
        y-intersection"
        ":math:`b_{cas\_in}`", "`cav_e_in_b[n,t]`", "P", "Specific
        y-intersection"
        ":math:`b_{cas\_out}`", "`cav_e_out_b[n,t]`", "P", "Specific
        y-intersection"
        ":math:`m_{cmp\_max}`", "`cmp_p_max_m[n,t]`", "P", "Specific
        slope"
        ":math:`m_{cmp\_q}`", "`cmp_q_out_m[n,t]`", "P", "Specific
        slope"
        ":math:`m_{exp\_max}`", "`exp_p_max_m[n,t]`", "P", "Specific
        slope"
        ":math:`m_{exp\_q}`", "`exp_q_in_m[n,t]`", "P", "Specific
        slope"
        ":math:`m_{cas\_in}`", "`cav_e_in_m[n,t]`", "P", "Specific
        slope"
        ":math:`m_{cas\_out}`", "`cav_e_out_m[n,t]`", "P", "Specific
        slope"
        ":math:`P_{cmp\_min}`", "`cmp_p_min[n,t]`", "P", "Min.
        compression power"
        ":math:`r_{cmp\_tes}`", "`cmp_q_tes_share[n,t]`", "P", "Ratio
        between waste heat flow and heat flow into TES"
        ":math:`r_{exp\_tes}`", "`exp_q_tes_share[n,t]`", "P", "
        | Ratio between external heat flow into expansion
        | and heat flows from TES and additional source"
        ":math:`\tau`", "`m.timeincrement[n,t]`", "P", "Time interval
        length"
        ":math:`TES_{fil\_max}`", "`tes_level_max[n,t]`", "P", "Max.
        filling level of TES"
        ":math:`CAS_{fil\_max}`", "`cav_level_max[n,t]`", "P", "Max.
        filling level of TES"
        ":math:`\tau`", "`cav_eta_tmp[n,t]`", "P", "
        | Temporal efficiency
        | (loss factor to take intertemporal losses into account)"
        ":math:`electrical\_input`", "
        `flow[list(n.electrical_input.keys())[0], p, n, t]`", "P", "
        Electr. power input into compression"
        ":math:`electrical\_output`", "
        `flow[n, list(n.electrical_output.keys())[0], p, t]`", "P", "
        Electr. power output of expansion"
        ":math:`fuel\_input`", "
        `flow[list(n.fuel_input.keys())[0], n, p, t]`", "P", "Heat input
        (external) into Expansion"

    """

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
        self.cmp_p = Var(
            self.GENERICCAES, m.TIMESTEPS, within=NonNegativeReals
        )

        # Compression: Max. Capacity
        self.cmp_p_max = Var(
            self.GENERICCAES, m.TIMESTEPS, within=NonNegativeReals
        )

        # Compression: Heat flow
        self.cmp_q_out_sum = Var(
            self.GENERICCAES, m.TIMESTEPS, within=NonNegativeReals
        )

        # Compression: Waste heat
        self.cmp_q_waste = Var(
            self.GENERICCAES, m.TIMESTEPS, within=NonNegativeReals
        )

        # Expansion: Binary variable for operation status
        self.exp_st = Var(self.GENERICCAES, m.TIMESTEPS, within=Binary)

        # Expansion: Realized capacity
        self.exp_p = Var(
            self.GENERICCAES, m.TIMESTEPS, within=NonNegativeReals
        )

        # Expansion: Max. Capacity
        self.exp_p_max = Var(
            self.GENERICCAES, m.TIMESTEPS, within=NonNegativeReals
        )

        # Expansion: Heat flow of natural gas co-firing
        self.exp_q_in_sum = Var(
            self.GENERICCAES, m.TIMESTEPS, within=NonNegativeReals
        )

        # Expansion: Heat flow of natural gas co-firing
        self.exp_q_fuel_in = Var(
            self.GENERICCAES, m.TIMESTEPS, within=NonNegativeReals
        )

        # Expansion: Heat flow of additional firing
        self.exp_q_add_in = Var(
            self.GENERICCAES, m.TIMESTEPS, within=NonNegativeReals
        )

        # Cavern: Filling levelh
        self.cav_level = Var(
            self.GENERICCAES, m.TIMESTEPS, within=NonNegativeReals
        )

        # Cavern: Energy inflow
        self.cav_e_in = Var(
            self.GENERICCAES, m.TIMESTEPS, within=NonNegativeReals
        )

        # Cavern: Energy outflow
        self.cav_e_out = Var(
            self.GENERICCAES, m.TIMESTEPS, within=NonNegativeReals
        )

        # TES: Filling levelh
        self.tes_level = Var(
            self.GENERICCAES, m.TIMESTEPS, within=NonNegativeReals
        )

        # TES: Energy inflow
        self.tes_e_in = Var(
            self.GENERICCAES, m.TIMESTEPS, within=NonNegativeReals
        )

        # TES: Energy outflow
        self.tes_e_out = Var(
            self.GENERICCAES, m.TIMESTEPS, within=NonNegativeReals
        )

        # Spot market: Positive capacity
        self.exp_p_spot = Var(
            self.GENERICCAES, m.TIMESTEPS, within=NonNegativeReals
        )

        # Spot market: Negative capacity
        self.cmp_p_spot = Var(
            self.GENERICCAES, m.TIMESTEPS, within=NonNegativeReals
        )

        # Compression: Capacity on markets
        def cmp_p_constr_rule(block, n, t):
            expr = 0
            expr += -self.cmp_p[n, t]
            expr += m.flow[list(n.electrical_input.keys())[0], n, t]
            return expr == 0

        self.cmp_p_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_p_constr_rule
        )

        # Compression: Max. capacity depending on cavern filling level
        def cmp_p_max_constr_rule(block, n, t):
            if t != 0:
                return (
                    self.cmp_p_max[n, t]
                    == n.params["cmp_p_max_m"] * self.cav_level[n, t - 1]
                    + n.params["cmp_p_max_b"]
                )
            else:
                return self.cmp_p_max[n, t] == n.params["cmp_p_max_b"]

        self.cmp_p_max_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_p_max_constr_rule
        )

        def cmp_p_max_area_constr_rule(block, n, t):
            return self.cmp_p[n, t] <= self.cmp_p_max[n, t]

        self.cmp_p_max_area_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_p_max_area_constr_rule
        )

        # Compression: Status of operation (on/off)
        def cmp_st_p_min_constr_rule(block, n, t):
            return (
                self.cmp_p[n, t] >= n.params["cmp_p_min"] * self.cmp_st[n, t]
            )

        self.cmp_st_p_min_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_st_p_min_constr_rule
        )

        def cmp_st_p_max_constr_rule(block, n, t):
            return (
                self.cmp_p[n, t]
                <= (
                    n.params["cmp_p_max_m"] * n.params["cav_level_max"]
                    + n.params["cmp_p_max_b"]
                )
                * self.cmp_st[n, t]
            )

        self.cmp_st_p_max_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_st_p_max_constr_rule
        )

        # (7) Compression: Heat flow out
        def cmp_q_out_constr_rule(block, n, t):
            return (
                self.cmp_q_out_sum[n, t]
                == n.params["cmp_q_out_m"] * self.cmp_p[n, t]
                + n.params["cmp_q_out_b"] * self.cmp_st[n, t]
            )

        self.cmp_q_out_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_q_out_constr_rule
        )

        #  (8) Compression: Definition of single heat flows
        def cmp_q_out_sum_constr_rule(block, n, t):
            return (
                self.cmp_q_out_sum[n, t]
                == self.cmp_q_waste[n, t] + self.tes_e_in[n, t]
            )

        self.cmp_q_out_sum_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_q_out_sum_constr_rule
        )

        # (9) Compression: Heat flow out ratio
        def cmp_q_out_shr_constr_rule(block, n, t):
            return self.cmp_q_waste[n, t] * n.params[
                "cmp_q_tes_share"
            ] == self.tes_e_in[n, t] * (1 - n.params["cmp_q_tes_share"])

        self.cmp_q_out_shr_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cmp_q_out_shr_constr_rule
        )

        # (10) Expansion: Capacity on markets
        def exp_p_constr_rule(block, n, t):
            expr = 0
            expr += -self.exp_p[n, t]
            expr += m.flow[n, list(n.electrical_output.keys())[0], t]
            return expr == 0

        self.exp_p_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_p_constr_rule
        )

        # (11-12) Expansion: Max. capacity depending on cavern filling level
        def exp_p_max_constr_rule(block, n, t):
            if t != 0:
                return (
                    self.exp_p_max[n, t]
                    == n.params["exp_p_max_m"] * self.cav_level[n, t - 1]
                    + n.params["exp_p_max_b"]
                )
            else:
                return self.exp_p_max[n, t] == n.params["exp_p_max_b"]

        self.exp_p_max_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_p_max_constr_rule
        )

        # (13)
        def exp_p_max_area_constr_rule(block, n, t):
            return self.exp_p[n, t] <= self.exp_p_max[n, t]

        self.exp_p_max_area_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_p_max_area_constr_rule
        )

        # (14) Expansion: Status of operation (on/off)
        def exp_st_p_min_constr_rule(block, n, t):
            return (
                self.exp_p[n, t] >= n.params["exp_p_min"] * self.exp_st[n, t]
            )

        self.exp_st_p_min_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_st_p_min_constr_rule
        )

        # (15)
        def exp_st_p_max_constr_rule(block, n, t):
            return (
                self.exp_p[n, t]
                <= (
                    n.params["exp_p_max_m"] * n.params["cav_level_max"]
                    + n.params["exp_p_max_b"]
                )
                * self.exp_st[n, t]
            )

        self.exp_st_p_max_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_st_p_max_constr_rule
        )

        # (16) Expansion: Heat flow in
        def exp_q_in_constr_rule(block, n, t):
            return (
                self.exp_q_in_sum[n, t]
                == n.params["exp_q_in_m"] * self.exp_p[n, t]
                + n.params["exp_q_in_b"] * self.exp_st[n, t]
            )

        self.exp_q_in_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_q_in_constr_rule
        )

        # (17) Expansion: Fuel allocation
        def exp_q_fuel_constr_rule(block, n, t):
            expr = 0
            expr += -self.exp_q_fuel_in[n, t]
            expr += m.flow[list(n.fuel_input.keys())[0], n, t]
            return expr == 0

        self.exp_q_fuel_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_q_fuel_constr_rule
        )

        # (18) Expansion: Definition of single heat flows
        def exp_q_in_sum_constr_rule(block, n, t):
            return (
                self.exp_q_in_sum[n, t]
                == self.exp_q_fuel_in[n, t]
                + self.tes_e_out[n, t]
                + self.exp_q_add_in[n, t]
            )

        self.exp_q_in_sum_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_q_in_sum_constr_rule
        )

        # (19) Expansion: Heat flow in ratio
        def exp_q_in_shr_constr_rule(block, n, t):
            return n.params["exp_q_tes_share"] * self.exp_q_fuel_in[n, t] == (
                1 - n.params["exp_q_tes_share"]
            ) * (self.exp_q_add_in[n, t] + self.tes_e_out[n, t])

        self.exp_q_in_shr_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=exp_q_in_shr_constr_rule
        )

        # (20) Cavern: Energy inflow
        def cav_e_in_constr_rule(block, n, t):
            return (
                self.cav_e_in[n, t]
                == n.params["cav_e_in_m"] * self.cmp_p[n, t]
                + n.params["cav_e_in_b"]
            )

        self.cav_e_in_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cav_e_in_constr_rule
        )

        # (21) Cavern: Energy outflow
        def cav_e_out_constr_rule(block, n, t):
            return (
                self.cav_e_out[n, t]
                == n.params["cav_e_out_m"] * self.exp_p[n, t]
                + n.params["cav_e_out_b"]
            )

        self.cav_e_out_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cav_e_out_constr_rule
        )

        # (22-23) Cavern: Storage balance
        def cav_eta_constr_rule(block, n, t):
            if t != 0:
                return n.params["cav_eta_temp"] * self.cav_level[
                    n, t
                ] == self.cav_level[n, t - 1] + m.timeincrement[t] * (
                    self.cav_e_in[n, t] - self.cav_e_out[n, t]
                )
            else:
                return n.params["cav_eta_temp"] * self.cav_level[
                    n, t
                ] == m.timeincrement[t] * (
                    self.cav_e_in[n, t] - self.cav_e_out[n, t]
                )

        self.cav_eta_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cav_eta_constr_rule
        )

        # (24) Cavern: Upper bound
        def cav_ub_constr_rule(block, n, t):
            return self.cav_level[n, t] <= n.params["cav_level_max"]

        self.cav_ub_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=cav_ub_constr_rule
        )

        # (25-26) TES: Storage balance
        def tes_eta_constr_rule(block, n, t):
            if t != 0:
                return self.tes_level[n, t] == self.tes_level[
                    n, t - 1
                ] + m.timeincrement[t] * (
                    self.tes_e_in[n, t] - self.tes_e_out[n, t]
                )
            else:
                return self.tes_level[n, t] == m.timeincrement[t] * (
                    self.tes_e_in[n, t] - self.tes_e_out[n, t]
                )

        self.tes_eta_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=tes_eta_constr_rule
        )

        # (27) TES: Upper bound
        def tes_ub_constr_rule(block, n, t):
            return self.tes_level[n, t] <= n.params["tes_level_max"]

        self.tes_ub_constr = Constraint(
            self.GENERICCAES, m.TIMESTEPS, rule=tes_ub_constr_rule
        )
