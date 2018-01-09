# -*- coding: utf-8 -*-
"""Solph Optimization Models
"""

import pyomo.environ as po
from pyomo.opt import SolverFactory
from pyomo.core.plugins.transform.relax_integrality import RelaxIntegrality
from oemof.solph import blocks, custom
from oemof.solph.plumbing import sequence
from oemof.outputlib import processing
import logging

__copyright__ = "oemof developer group"
__license__ = "GPLv3"


class BaseModel(po.ConcreteModel):
    """ The BaseModel for other solph-models (Model, MultiPeriodModel, etc.)

    Parameters
    ----------
    energysystem : EnergySystem object
        Object that holds the nodes of an oemof energy system graph
    constraint_groups : list (optional)
        Solph looks for these groups in the given energy system and uses them
        to create the constraints of the optimization problem.
        Defaults to :const:`Model.CONSTRAINTS`
    auto_construct : boolean
        If this value is true, the set, variables, constraints, etc. are added,
        automatically when instantiating the model. For sequential model
        building process set this value to False
        and use methods `_add_parent_block_sets`,
        `_add_parent_block_variables`, `_add_blocks`, `_add_objective`

    """
    CONSTRAINT_GROUPS = []

    def __init__(self, energysystem, **kwargs):
        super().__init__()

        # ########################  Arguments #################################

        self.name = kwargs.get('name', type(self).__name__)

        self.es = energysystem

        self.timeincrement = sequence(self.es.timeindex.freq.nanos / 3.6e12)

        self._constraint_groups = (type(self).CONSTRAINT_GROUPS +
                                   kwargs.get('constraint_groups', []))

        self._constraint_groups += [i for i in self.es.groups
                                    if hasattr(i, 'CONSTRAINT_GROUP') and
                                    i not in self._constraint_groups]

        self.flows = self.es.flows()

        if kwargs.get("auto_construct", True):
            self._construct()

    def _construct(self):
        """
        """
        self._add_parent_block_sets()
        self._add_parent_block_variables()
        self._add_child_blocks()
        self._add_objective()

    def _add_parent_block_sets(self):
        """" Method to create all sets located at the parent block, i.e. the
        model itself as they are to be shared across all model components.
        """
        pass

    def _add_parent_block_variables(self):
        """" Method to create all variables located at the parent block,
        i.e. the model itself as these variables  are to be shared across
        all model components.
        """
        pass

    def _add_child_blocks(self):
        """ Method to add the defined child blocks for components that have
        been grouped in the defined constraint groups.
        """

        for group in self._constraint_groups:
            # create instance for block
            block = group()
            # Add block to model
            self.add_component(str(block), block)
            # create constraints etc. related with block for all nodes
            # in the group
            block._create(group=self.es.groups.get(group))

    def _add_objective(self, sense=po.minimize, update=False):
        """ Method to sum up all objective expressions from the child blocks
        that have been created. This method looks for `_objective_expression`
        attribute in the block definition and will call this method to add
        their return value to the objective function.
        """
        if update:
            self.del_component('objective')

        expr = 0

        for block in self.component_data_objects():
            if hasattr(block, '_objective_expression'):
                expr += block._objective_expression()

        self.objective = po.Objective(sense=sense, expr=expr)

    def receive_duals(self):
        """ Method sets solver suffix to extract information about dual
        variables from solver. Shadow prices (duals) and reduced costs (rc) are
        set as attributes of the model.

        """
        # shadow prices
        self.dual = po.Suffix(direction=po.Suffix.IMPORT)
        # reduced costs
        self.rc = po.Suffix(direction=po.Suffix.IMPORT)

    def results(self):
        """ Returns a nested dictionary of the results of this optimization
        """
        result = processing.results(self)

        return result

    def solve(self, solver='cbc', solver_io='lp', **kwargs):
        r""" Takes care of communication with solver to solve the model.

        Parameters
        ----------
        solver : string
            solver to be used e.g. "glpk","gurobi","cplex"
        solver_io : string
            pyomo solver interface file format: "lp","python","nl", etc.
        \**kwargs : keyword arguments
            Possible keys can be set see below:

        Other Parameters
        ----------------
        solve_kwargs : dict
            Other arguments for the pyomo.opt.SolverFactory.solve() method
            Example : {"tee":True}
        cmdline_options : dict
            Dictionary with command line options for solver e.g.
            {"mipgap":"0.01"} results in "--mipgap 0.01"
            {"interior":" "} results in "--interior"
            Gurobi solver takes numeric parameter values such as
            {"method": 2}

        """
        solve_kwargs = kwargs.get('solve_kwargs', {})
        solver_cmdline_options = kwargs.get("cmdline_options", {})

        opt = SolverFactory(solver, solver_io=solver_io)
        # set command line options
        options = opt.options
        for k in solver_cmdline_options:
            options[k] = solver_cmdline_options[k]

        results = opt.solve(self, **solve_kwargs)

        status = results["Solver"][0]["Status"].key
        termination_condition = \
            results["Solver"][0]["Termination condition"].key

        if status == "ok" and termination_condition == "optimal":
            logging.info("Optimization successful...")
            self.solutions.load_from(results)
            # storage results in result dictionary of energy system
            self.es.results = results
        elif status == "ok" and termination_condition == "unknown":
            logging.warning("Optimization with unknown termination condition."
                            " Writing output anyway...")
            self.solutions.load_from(results)
            # storage results in result dictionary of energy system
            self.es.results = results
        elif status == "warning" and termination_condition == "other":
            logging.warning("Optimization might be sub-optimal."
                            " Writing output anyway...")
            self.solutions.load_from(results)
            # storage results in result dictionary of energy system
            self.es.results = results
        else:
            # storage results in result dictionary of energy system
            self.es.results = results
            logging.error(
                "Optimization failed with status %s and terminal condition %s"
                % (status, termination_condition))

        return results

    def relax_problem(self):
        """Relaxes integer variables to reals of optimization model self."""
        relaxer = RelaxIntegrality()
        relaxer._apply_to(self)

        return self


class Model(BaseModel):
    """ An  energy system model for operational and investment
    optimization.

    Parameters
    ----------
    energysystem : EnergySystem object
        Object that holds the nodes of an oemof energy system graph
    constraint_groups : list
        Solph looks for these groups in the given energy system and uses them
        to create the constraints of the optimization problem.
        Defaults to :const:`Model.CONSTRAINTS`

    **The following basic sets are created**:

    NODES :
        A set with all nodes of the given energy system.

    TIMESTEPS :
        A set with all timesteps of the given time horizon.

    FLOWS :
        A 2 dimensional set with all flows. Index: `(source, target)`

    **The following basic variables are created**:

    flow
        Flow from source to target indexed by FLOWS, TIMESTEPS.
        Note: Bounds of this variable are set depending on attributes of
        the corresponding flow object.

    """
    CONSTRAINT_GROUPS = [blocks.Bus, blocks.Transformer,
                         blocks.InvestmentFlow, blocks.Flow,
                         blocks.NonConvexFlow]

    def __init__(self, energysystem, **kwargs):
        super().__init__(energysystem, **kwargs)

    def _add_parent_block_sets(self):
        """
        """
        # set with all nodes
        self.NODES = po.Set(initialize=[n for n in self.es.nodes])

        # pyomo set for timesteps of optimization problem
        self.TIMESTEPS = po.Set(initialize=range(len(self.es.timeindex)),
                                ordered=True)

        # previous timesteps
        previous_timesteps = [x - 1 for x in self.TIMESTEPS]
        previous_timesteps[0] = self.TIMESTEPS.last()

        self.previous_timesteps = dict(zip(self.TIMESTEPS, previous_timesteps))

        # pyomo set for all flows in the energy system graph
        self.FLOWS = po.Set(initialize=self.flows.keys(),
                            ordered=True, dimen=2)

        self.BIDIRECTIONAL_FLOWS = po.Set(initialize=[
            k for (k, v) in self.flows.items() if hasattr(v, 'bidirectional')],
                                          ordered=True, dimen=2,
                                          within=self.FLOWS)

        self.UNIDIRECTIONAL_FLOWS = po.Set(
            initialize=[k for (k, v) in self.flows.items() if not
                        hasattr(v, 'bidirectional')],
            ordered=True, dimen=2, within=self.FLOWS)

    def _add_parent_block_variables(self):
        """
        """
        self.flow = po.Var(self.FLOWS, self.TIMESTEPS,
                           within=po.Reals)

        for (o, i) in self.FLOWS:
            for t in self.TIMESTEPS:
                if (o, i) in self.UNIDIRECTIONAL_FLOWS:
                    self.flow[o, i, t].setlb(0)
                if self.flows[o, i].nominal_value is not None:
                    self.flow[o, i, t].setub(self.flows[o, i].max[t] *
                                             self.flows[o, i].nominal_value)

                    if self.flows[o, i].actual_value[t] is not None:
                        # pre- optimized value of flow variable
                        self.flow[o, i, t].value = (
                            self.flows[o, i].actual_value[t] *
                            self.flows[o, i].nominal_value)
                        # fix variable if flow is fixed
                        if self.flows[o, i].fixed:
                            self.flow[o, i, t].fix()

                    if not self.flows[o, i].nonconvex:
                        # lower bound of flow variable
                        self.flow[o, i, t].setlb(
                            self.flows[o, i].min[t] *
                            self.flows[o, i].nominal_value)



