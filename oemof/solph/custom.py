# -*- coding: utf-8 -
"""
This module is designed to hold custom components with their classes and
associated individual constraints (blocks) and groupings. Therefore this
module holds the class definition and the block directly located by each other.

Example usage:

#-----------------------------------------------------------------------------
# Here follows the component and the component block definition
#-----------------------------------------------------------------------------
import .network as ntwk

class CustomComponent(ntwk.Transformer):
    """ Set your parameters etc. here, choose your parent class depending on
    needs (sink not inputs, sources no output, transformer multiple in- and
    outputs)
    """
    def __init__(self, param1, param2, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.param1 = param1

class CustomComponentBlock(SimpleBlock):
    """ Add your constraints, variables (_create) and objective expression
    (_objective_expression) terms here
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """ THIS METHOD AND ITS NAME ARE MANDATORY!
        """
        m = self.parent_block()
        m.flow_max = po.Var(group, m.TIMESTEPS, within=po.NonNegativeReals)

        def new_constraint_rule(block, n, t):
            """
            """
            return m.flow[n, n.inputs[0], t] * self.param1 <= m.flow_max[n, t]
        self.new_constraint = po.Constraint(group, m.TIMESTEPS,
                                            rule=new_constraint_rule)

        # We can also a somthing to the objective expression
        self._objective_expression = 0

# Add your component/block to this function (below)
def generator_grouping(node):
    if isinstance(node, CustomComponent):
        return CustomComponentBlock

# Add your block to the CUSTOM_CONSTRAINTS_GROUPINGS list
CUSTOM_CONSTRAINT_GROUPINGS = [CustomComponentBlock]
"""
import .network as ntwk




# Add your component/block to this function (below)
def generator_grouping(node):
    pass

# Add your block to the CUSTOM_CONSTRAINTS_GROUPINGS list
CUSTOM_CONSTRAINT_GROUPINGS = []
