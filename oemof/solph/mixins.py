# -*- coding: utf-8 -*-
"""
"""
import pyomo.environ as po

class ConstraintMixin():
    """ The ConstraintMixin class contains mehtods that are used in the
    :class:`OperationalModel <oemof.solph.models.OperationalModeel>`. This is
    achivieved as the OperatioanlModel inherits from the ConstraintMixin class.

    """


    def flow_share(self, f1, f2, share):
        """ This docstring should be extensive!
        """

        def _rule(m, t):
            """
            """
            return m.flow[f1, t] == m.flow[f2, t] * share

        self.flow_share_constraint = po.Constraint(self.TIMESTEPS, rule=_rule)

