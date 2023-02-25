import numpy as np
from oemof.network import network
from pyomo.core.base.block import ScalarBlock
from pyomo.environ import Binary
from pyomo.environ import Constraint
from pyomo.environ import NonNegativeReals
from pyomo.environ import Set
from pyomo.environ import Var

from oemof.solph._plumbing import sequence


class CellConnector(network.Transformer):
    """
    Model of a coupling point for an energy cell. One such coupling point is
    necessary per form of energy transported in or out of the cell.

    Energy can only flow in one direction at a time and the allowed amount of
    energy transported in a timestep can be restricted.

    Parameters
    ----------
    inputs: dict
        Key-value pair, where key is the bus and value the energy flow from
        the external grid or parent cell into this energy cell. Should only
        contain a single key-value pair!
    outputs: dict
        Key-value pair, where key is the bus and value the energy flow from
        the energy cell to the external grid or parent cell. Should only
        contain a single key-value pair!
    max_power: numeric
        Numeric value indicating the maximum power from or to the grid.
        If a `max` value is set in the `inputs` or `output` flows as well,
        the lower value will be given preference.
    """

    # TODO rename inputs and outputs to inflows and outflows to make it clearer what they do
    # TODO enable max_power to be an iterable as well (sequence)

    def __init__(
        self, inputs, outputs, max_power, label=None, custom_attributes=None
    ):
        # TODO: extend the input/output handling to represent multiple commodities (electricity, gas, heat, ...)

        # initialize all custom_attributes
        if custom_attributes is None:
            custom_attributes = {}
        super().__init__(label, **custom_attributes)

        # TODO: raise Warning if more than one key in inputs or outputs

        # input mapping
        self.inputs.update(inputs)

        # output mapping
        self.outputs.update(outputs)

        # set maximum power
        self.max_power = max_power

        # connected input bus
        self.input_bus = list(inputs.keys())[0]

        # connected output bus
        self.output_bus = list(outputs.keys())[0]

    def constraint_group(self):
        """
        Returns Block containing constraints for this class during energy
        system creation.
        """
        return CellConnectorBlock


class CellConnectorBlock(ScalarBlock):
    """
    bla bla bla
    """

    # TODO: add Docstring
    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """
        Create the constraints for CellConnectorBlock

        Parameters
        ----------
        group: list
            List containing all `CellConnector` objects
        """
        # if no CellConnector is used, skip Block creation
        if group is None:
            return None

        # reference to the energy cell
        m = self.parent_block()

        # set containing CellConnector instances in the energy system
        self.CELLCONNECTORS = Set(initialize=[n for n in group])

        # flow from external grid to energy cell
        self.input_flow = Var(
            self.CELLCONNECTORS, m.TIMESTEPS, within=NonNegativeReals
        )

        # flow from cell to external grid
        self.output_flow = Var(
            self.CELLCONNECTORS, m.TIMESTEPS, within=NonNegativeReals
        )

        # binary status variable indicating flow direction
        self.Y_exp = Var(self.CELLCONNECTORS, m.TIMESTEPS, within=Binary)

        # map input flow to internal variable
        def _input_flow_rule(block, n, t):
            lhs = block.input_flow[n, t]
            # rhs = m.flow[list(n.inputs.keys())[0], n, t]
            rhs = sum([m.flow[n, i, t] for i in list(n.inputs.keys())])
            return lhs == rhs

        self.input_flow_rule = Constraint(
            self.CELLCONNECTORS, m.TIMESTEPS, rule=_input_flow_rule
        )

        # map output flow to internal variable
        def _output_flow_rule(block, n, t):
            lhs = block.output_flow[n, t]
            rhs = sum([m.flow[o, n, t] for o in list(n.outputs.keys())])
            # rhs = m.flow[list(n.outputs.keys())[0], n, t]
            return lhs == rhs

        self.output_flow_rule = Constraint(
            self.CELLCONNECTORS, m.TIMESTEPS, rule=_output_flow_rule
        )

        # rule for maximum input (contains input.output restriction)
        # TODO: find a way to prevent usage of max_power
        # Maybe using flows between the CellConnectors could alleviate this
        # and other problems?
        def _max_input_rule(block, n, t):
            lhs = block.input_flow[n, t]
            rhs = (1 - block.Y_exp[n, t]) * n.max_power
            return lhs <= rhs

        self.max_input_rule = Constraint(
            self.CELLCONNECTORS, m.TIMESTEPS, rule=_max_input_rule
        )

        def _max_output_rule(block, n, t):
            lhs = block.output_flow[n, t]
            rhs = block.Y_exp[n, t] * n.max_power
            return lhs <= rhs

        self.max_output_rule = Constraint(
            self.CELLCONNECTORS, m.TIMESTEPS, rule=_max_output_rule
        )

        # TODO: add objective function term. Cost calculation might be a major issue!
