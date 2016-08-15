"""

@contact Simon Hilpert (simon.hilpert@fh-flensburg.de)
"""

from collections import UserDict as UD
from functools import singledispatch

import pyomo.environ as po
import logging

from ..tools import helpers
from . import variables as var
from . import linear_mixed_integer_constraints as milc
from . import linear_constraints as lc
from ..core.network.entities import Bus, Component, ExcessSlack, ShortageSlack
from ..core.network.entities.buses import HeatBus
from ..core.network.entities import components as cp
from ..core.network.entities.components import transformers as transformer
from ..core.network.entities.components.sources import (
    Commodity, DispatchSource, FixedSource)
from ..core.network.entities.components.sinks import Simple as Sink
from ..core.network.entities.components import transports


@singledispatch
def assembler(e, om, block):
    """ Assemblers are the functions adding constraints to an optimization
        model for a set of objects.

    This is the most general form of assembler function, called only if no
    other, more specific assemblers have been found. Since we don't know what
    to do in this case, we can only throw a :class:`TypeError`.

    Parameters
    ----------
    entity: An object. Only used to figure out which assembler function to call
            by dispatching on its `type`. Not used otherwise.
            It's a good idea to set this to `None` if the function is called
            directly via :attr:`assembler.registry`.

    om    : The optimization model. Should be an instance of
            :class:`pyomo.ConcreteModel`.

    block : A pyomo block.

    Returns
    -------
    om    : The optimization model passed in as an argument, with additional
            bus balances.
    """
    raise TypeError(
        "Did not find a way to generate optimization constraints for object:" +
        "\n\n {o}\n\n of type:\n\n {t}".format(o=e, t=type(e)))
    return om


class OptimizationModel(po.ConcreteModel):
    """Create Pyomo model of the energy system.

    Parameters
    ----------
    entities : list with all entity objects
    timesteps : list with all timesteps as integer values
    options : nested dictionary with options to set.

    """

    # TODO Cord: Take "next(iter(self.dict.values()))" where the first value of
    #            dict has to be selected

    def __init__(self, energysystem, loglevel=logging.INFO):
        super().__init__()
        logging.basicConfig(format="%(levelname)s:%(message)s", level=loglevel)
        self.entities = energysystem.entities
        self.energysystem = energysystem
        self.timesteps = energysystem.simulation.timesteps
        self.objective_options = energysystem.simulation.objective_options
        self.relaxed = getattr(energysystem.simulation, "relaxed", False)

        self.T = po.Set(initialize=self.timesteps, ordered=True)
        # calculate all edges ([("coal", "pp_coal"),...])
        self.components = [e for e in self.entities
                           if isinstance(e, Component)]
        self.all_edges = self.edges(self.components)
        var.add_continuous(model=self, edges=self.all_edges)

        # group components by type (cbt: components by type)
        cbt = {}
        for c in self.components:
            cbt[type(c)] = cbt.get(type(c), []) + [c]

        self.I = {c.uid: [i.uid for i in c.inputs[:]] for c in self.components
                  if not isinstance(c, cp.Source)}
        self.O = {c.uid: [o.uid for o in c.outputs[:]] for c in self.components
                  if not isinstance(c, cp.Sink)}

        # Add constraints for all components to the model
        self.build_component_constraints(cbt)

        # group buses by type (bbt: buses by type)
        bbt = {}
        for b in [e for e in self.entities if isinstance(e, Bus)]:
            bbt[type(b)] = bbt.get(type(b), []) + [b]

        # Add constraints for all buses to the model
        self.build_bus_constraints(bbt)

        # create objective function
        if not self.objective_options:
            raise ValueError("No objective options defined!")

        logging.info("Building objective function.")
        self.objective_assembler(objective_options=self.objective_options)

    def build_component_constraints(self, cbt):
        logging.info("Building component constraints.")
        for cls in cbt:
            objs = cbt[cls]
            # "call" methods to add the constraints opt. problem
            if objs:  # Should always be nonempty but who knows...
                uids = [e.uid for e in objs]
                # add pyomo block per cls to OptimizationModel instance
                block = po.Block()
                block.uids = po.Set(initialize=uids)
                block.indexset = po.Set(initialize=block.uids*self.T)
                block.objs = objs
                block.optimization_options = cls.optimization_options
                self.add_component(str(cls), block)
                logging.debug("Creating optimization block for omeof " +
                              "classes: " + block.name)
                assembler.registry[cls](e=None, om=self, block=block)

    def build_bus_constraints(self, bbt):
        logging.info("Building bus constraints.")
        for bls in bbt:
            objs = bbt[bls]
            # "call" methods to add the constraints opt. problem
            if objs:
                # add bus block
                block = po.Block()
                uids = [e.uid for e in objs]
                block.uids = po.Set(initialize=uids)
                block.objs = objs
                self.add_component(str(bls), block)
                assembler.registry[bls](e=None, om=self, block=block)

    def default_assembler(self, block):
        """ Method for setting optimization model objects for blocks

        Parameters
        ----------
        self : OptimizationModel() instance
        block : SimpleBlock()
        """

        if block.optimization_options:
            for k in block.optimization_options:
                block.default_optimization_options.update({
                    k: block.optimization_options[k]})
            block.optimization_options = block.default_optimization_options
        else:
            block.optimization_options = block.default_optimization_options

        if (block.optimization_options.get("investment", False) and
                "milp_constr" in block.optimization_options):
            raise ValueError("Component can not be modeled with milp-constr " +
                             "in investment mode!\n" +
                             "Please change `optimization_options`")

        if "milp_constr" in block.optimization_options:
            # create binary status variables for block components
            var.add_binary(self, block, relaxed=self.relaxed)

        # add additional variables (investment mode)
        if block.optimization_options.get("investment", False):
            add_out_limit = {obj.uid: obj.add_out_limit
                             for obj in block.objs}

            def add_out_bound_rule(block, e):
                return (0, add_out_limit[e])
            block.add_out = po.Var(block.uids, within=po.NonNegativeReals,
                                   bounds=add_out_bound_rule)

        for option in block.optimization_options:
            if option not in ["objective", "investment"]:
                block.optimization_options[option](self, block)

    def objective_assembler(self, objective_options):
        """ calls functions to add predefined objective functions

        Parameters
        ----------
        self : OptimizationModel() instance
        objective_options : dict
           dictionary with infos about objects. key "function" hold function
           to build objective
        """

        revenue_objects = objective_options.get("revenue_objects")
        cost_objects = objective_options.get("cost_objects")

        if objective_options.get("function") is None:
            logging.warning("No objective function selected. If you want " +
                            "to build an objective yourself you can" +
                            " ignore this warning.")
        else:
            objective_options["function"](self,
                                          cost_objects=cost_objects,
                                          revenue_objects=revenue_objects)

    def update_objective(self, objective_options=None):
        """
        Updates the objective function with new parameters from entities

        Parameters
        ----------
        self : OptimizationModel() instance
        objective_options : dict
           dictionary with infos about objects. key "function" hold function
           to build objective
        """
        if not objective_options:
            oo = self.objective_options
        else:
            oo = objective_options
        self.objective_assembler(objective_options=oo)
        self.preprocess()

    def results(self):
        """ Returns a nested dictionary of the results of this optimization
        model.

        The dictionary is keyed by the :class:`Entities
        <oemof.core.network.Entity>` of the optimization model, that is
        :meth:`om.results()[s][t] <OptimizationModel.results>`
        holds the time series representing values attached to the edge (i.e.
        the flow) from `s` to `t`, where `s` and `t` are instances of
        :class:`Entity <oemof.core.network.Entity>`.

        Time series belonging only to one object, like e.g. shadow prices of
        commodities on a certain :class:`Bus
        <oemof.core.network.entities.Bus>`, dispatch values of a
        :class:`DispatchSource
        <oemof.core.network.entities.components.sources.DispatchSource>` or
        storage values of a
        :class:`Storage
        <oemof.core.network.entities.components.transformers.Storage>` are
        treated as belonging to an edge looping from the object to itself.
        This means they can be accessed via
        :meth:`om.results()[object][object] <OptimizationModel.results>`.

        Object attributes holding optimization results, like e.g. `add_cap` for
        storage objects, can be accessed like this:

          :meth:`om.results()[s].add_cap`

        where `s` is a storage object.

        The value of the objective function is stored under the
        :attr:`om.results().objective` attribute.

        Note that the optimization model has to be solved prior to invoking
        this method.
        """
        # TODO: Maybe make the results dictionary a proper object?
        result = UD()
        result.objective = self.objective()
        for entity in self.entities:
            if (isinstance(entity, cp.Transformer) or
                isinstance(entity, cp.Transport) or
                isinstance(entity, cp.Source) or
                    isinstance(entity, ShortageSlack)):
                if entity.outputs:
                    result[entity] = result.get(entity, UD())
                for o in entity.outputs:
                    result[entity][o] = [self.w[entity.uid, o.uid, t].value
                                         for t in self.timesteps]

                for i in entity.inputs:
                    result[i] = result.get(i, {})
                    result[i][entity] = [self.w[i.uid, entity.uid, t].value
                                         for t in self.timesteps]

            if isinstance(entity, cp.sources.DispatchSource):
                result[entity] = result.get(entity, UD())
                # TODO: Why does this use `entity.outputs[0]`?
                result[entity][entity] = [self.w[entity.uid,
                                                 entity.outputs[0].uid,
                                                 t].value
                                          for t in self.timesteps]

            if (isinstance(entity, cp.Sink) or
                isinstance(entity, ExcessSlack)):
                for i in entity.inputs:
                    result[i] = result.get(i, {})
                    result[i][entity] = [self.w[i.uid, entity.uid, t].value
                                         for t in self.timesteps]

            if isinstance(entity, cp.transformers.Storage):
                result[entity] = result.get(entity, UD())
                result[entity][entity] = [
                    getattr(
                        self, str(transformer.Storage)
                        ).cap[entity.uid, t].value
                    for t in self.timesteps]

            block = getattr(self, str(type(entity)))

            for attribute in ["add_cap", "add_out"]:
                values = getattr(block, attribute, None)
                if values:
                    result[entity] = result.get(entity, UD())
                    setattr(result[entity], attribute, values[entity.uid]())

        if hasattr(self, "dual"):
            for bus in getattr(self, str(Bus)).objs:
                if bus.balanced:
                    result[bus] = result.get(bus, {})
                    result[bus][bus] = [
                        self.dual[getattr(self, str(Bus)).balance[
                            (bus.uid, t)]]
                        for t in self.timesteps]

        return result

    def write_lp_file(self, path=None, filename="problem.lp"):
        if path is None:
            path = helpers.extend_basic_path("lp_files")
        self.write(helpers.get_fullpath(path, filename),
                   io_options={"symbolic_solver_labels": True})
        logging.info("LP-file saved to {0}".format(
            helpers.get_fullpath(path, filename)))

    def solve(self, **kwargs):
        r""" Method that takes care of the communication with the solver
        to solve the optimization model.

        Parameters
        ----------
        self : pyomo.ConcreteModel() object

        \**kwargs : keywords
            Possible keys can be set see below
        solver string:
            solver to be used e.g. "glpk","gurobi","cplex"
        debug : boolean
            If True model is solved in debug mode. lp-file is written.
        duals : boolean
            If True, duals and reduced costs are imported from the solver
            results
        verbose : boolean
            If True informations are printed
        solver_io : string
            pyomo solver interface file format: "lp","python","nl", etc.
        solve_kwargs : dict
            Other arguments for the pyomo.opt.SolverFactory.solve() method
            Example : {"solver_io":"lp"}
        solver_cmdline_options : dict
            Dictionary with command line options for solver
            Examples:
            {"mipgap":"0.01"} results in "--mipgap 0.01"
            {"interior":" "} results in "--interior"


        Returns
        -------
        self : solved pyomo.ConcreteModel() instance

        """
        solver = kwargs.get("solver",  self.energysystem.simulation.solver)
        if solver is None:
            solver = "glpk"
        debug = kwargs.get("debug",  self.energysystem.simulation.debug)
        if debug is None:
            debug = False
        duals = kwargs.get("duals",  self.energysystem.simulation.duals)
        if duals is None:
            duals = False
        verbose = kwargs.get("verbose", self.energysystem.simulation.verbose)
        if verbose is None:
            verbose = False
        solver_io = kwargs.get("solver_io", "lp")
        solve_kwargs = kwargs.get("solve_kwargs", {})
        solver_cmdline_options = kwargs.get("solver_cmdline_options", {})

        from pyomo.opt import SolverFactory
        # Create a "dual" suffix component on the instance
        # so the solver plugin will know which suffixes to collect
        if duals is True:
            logging.debug("Setting suffixes for duals & reduced costs.")
            # dual variables (= shadow prices)
            self.dual = po.Suffix(direction=po.Suffix.IMPORT)
            # reduced costs
            self.rc = po.Suffix(direction=po.Suffix.IMPORT)
        # write lp-file
        if debug is True:
            self.write_lp_file()

        # solve instance
        opt = SolverFactory(solver, solver_io=solver_io)
        # set command line options
        options = opt.options
        for k in solver_cmdline_options:
            options[k] = solver_cmdline_options[k]
        # store results
        logging.info("Handing problem to solver and solving.")
        logging.info("Used solver: {0}".format(solver))
        results = opt.solve(self, **solve_kwargs)

        self.solutions.load_from(results)
        if verbose:
            logging.info("**************************************************")
            logging.info("Optimization problem informations from solph")
            logging.info("**************************************************")
            for k in results:
                logging.info("{0}: {1}".format(k, results[k]))
        else:
            logging.debug("**************************************************")
            logging.debug("Optimization problem informations from solph")
            logging.debug("**************************************************")
            for k in results:
                logging.debug("{0}: {1}".format(k, results[k]))
        return results

    def edges(self, components):
        """Method that creates a list with all edges for the objects in
        components.

        Parameters
        ----------
        self :
        components : list of component objects

        Returns
        -------
        edges : list with tupels that represent the edges
        """

        edges = []
        # create a list of tuples
        # e.g. [("coal", "pp_coal"), ("pp_coal", "b_el"),...]
        for c in components:
            for i in c.inputs:
                ei = (i.uid, c.uid)
                edges.append(ei)
            for o in c.outputs:
                ej = (c.uid, o.uid)
                edges.append(ej)
        return(edges)


@assembler.register(Bus)
def _(e, om, block):
    """ Method creates bus balance for all buses.

    The bus model creates all full balance around the energy buses using
    the :func:`lc.generic_bus_constraint` function.
    Additionally it sets constraints to model limits over the timehorizon
    for resource buses using :func:`lc.generic_limit`

    Parameters
    ----------
    see :func:`assembler`.

    Returns
    -------
    om : The optimization model passed in as an argument, with additional
          bus balances.
    """

    # bus balance constraint for energy bus objects
    lc.add_bus_balance(om, block)

    # set limits for buses
    lc.add_global_output_limit(om, block)
    return om


@assembler.register(HeatBus)
def _(e, om, block):
    """ Method creates bus balance for all buses.

    The bus model creates all full balance around the energy buses using
    the :func:`lc.generic_bus_constraint` function.
    Additionally it sets constraints to model limits over the timehorizon
    for resource buses using :func:`lc.generic_limit`

    Parameters
    ----------
    see :func:`assembler`.

    Returns
    -------
    om : The optimization model passed in as an argument, with additional
          bus balances.
    """

    # slack variables that assures a feasible problem
    # get uids for busses that allow excess
    block.excess_uids = [b.uid for b in block.objs if b.excess is True]
    # get uids for busses that allow shortage
    block.shortage_uids = [b.uid for b in block.objs if b.shortage is True]

    # create variables for "slack" of shortage and excess
    if block.excess_uids:
        om.excess_slack = po.Var(block.excess_uids,
                                 om.timesteps,
                                 within=po.NonNegativeReals)
    if block.shortage_uids:
        om.shortage_slack = po.Var(block.shortage_uids,
                                   om.timesteps,
                                   within=po.NonNegativeReals)

    # bus balance constraint for energy bus objects
    lc.add_bus_balance(om, block)

    # set limits for buses
    lc.add_global_output_limit(om, block)
    return om


@assembler.register(transformer.Simple)
def _(e, om, block):
    """ Method containing the constraints functions for simple
    transformer components.

    Constraints are selected by the `optimization_options` variable of
    :class:`Simple`.

    Parameters
    ----------
    see :func:`assembler`.

    Returns
    -------
    see :func:`assembler`.
    """
    # TODO: This should be dependent on objs classes not fixed if assembler
    # method is used by another assemlber method...

    def linear_constraints(om, block):
        lc.add_simple_io_relation(om, block)
        var.set_bounds(om, block, side="output")

    block.default_optimization_options = {
        "linear_constr": linear_constraints}

    om.default_assembler(block)
    return om


@assembler.register(transformer.TwoInputsOneOutput)
def _(e, om, block):
    """ Method containing the constraints functions for simple
    transformer components.

    Constraints are selected by the `optimization_options` variable of
    :class:`Simple`.

    Parameters
    ----------
    see :func:`assembler`.

    Returns
    -------
    see :func:`assembler`.
    """
    # TODO: This should be dependent on objs classes not fixed if assembler
    # method is used by another assemlber method...

    def linear_constraints(om, block):
        lc.add_two_inputs_one_output_relation(om, block)
        var.set_bounds(om, block, side="output")
        var.set_bounds(om, block, side="input")

    block.default_optimization_options = {
        "linear_constr": linear_constraints}

    om.default_assembler(block)
    return om


@assembler.register(transformer.CHP)
def _(e, om, block):
    """ Method grouping the constraints for simple chp components.

    The method uses the simple_transformer_assembler() method. The
    optimization_options comes from the transfomer.CHP()

    Parameters
    ----------
    See :func:`assembler`.

    Returns
    -------
    See :func:`assembler`.
    """
    def linear_constraints(om, block):
        lc.add_simple_io_relation(om, block)
        lc.add_simple_chp_relation(om, block)
        var.set_bounds(om, block, side="output")

    block.default_optimization_options = {
        "linear_constr": linear_constraints}

    # simple_transformer assebmler for in-out relation, pmin,.. etc.
    om.default_assembler(block)
    return om


@assembler.register(transformer.SimpleExtractionCHP)
def _(e, om, block):
    """Method grouping the constraints for simple chp components.

    Parameters
    ----------
    See :func:`assembler`.

    Returns
    -------
    See :func:`assembler`.
    """
    def linear_constraints(om, block):
        lc.add_simple_extraction_chp_relation(om, block)
        var.set_bounds(om, block, side="output")
        var.set_bounds(om, block, side="input")

    block.default_optimization_options = {
        "linear_constr": linear_constraints}

    # simple_transformer assebmler for in-out relation, pmin,.. etc.
    om.default_assembler(block)
    return om


@assembler.register(transformer.VariableEfficiencyCHP)
def _(e, om, block):
    """Method grouping the constraints for chp components with variable el.
    efficiency.

    Parameters
    ----------
    See :func:`assembler`.

    Returns
    -------
    See :func:`assembler`.
    """
    def linear_constraints(om, block):
        lc.add_eta_total_chp_relation(om, block)

    def milp_constraints(om, block):
        milc.add_variable_linear_eta_relation(om, block)
        milc.set_bounds(om, block, side="output")

    block.default_optimization_options = {
        "linear_constr": linear_constraints,
        "milp_constr": milp_constraints}

    # simple_transformer assebmler for in-out relation, pmin,.. etc.
    om.default_assembler(block)
    return om


@assembler.register(FixedSource)
def _(e, om, block):
    """Method containing the constraints for
    fixed sources.

    Parameters
    ----------
    See :func:`assembler`.

    Returns
    -------
    See :func:`assembler`.
    """
    def linear_constraints(om, block):
        lc.add_fixed_source(om, block)

    block.default_optimization_options = {
        "linear_constr": linear_constraints}

    # simple_transformer assebmler for in-out relation, pmin,.. etc.
    om.default_assembler(block)
    return om


@assembler.register(DispatchSource)
def _(e, om, block):
    """Method containing the constraints for dispatchable sources.

    Parameters
    ----------
    See :func:`assembler`.

    Returns
    -------
    See :func:`assembler`.
    """
    def linear_constraints(om, block):
        lc.add_dispatch_source(om, block)

    block.default_optimization_options = {
        "linear_constr": linear_constraints}

    if block.optimization_options.get("investment", False):
        raise ValueError("Dispatch source + investment is not possible!")

    # simple_transformer assebmler for in-out relation, pmin,.. etc.
    om.default_assembler(block)
    return om


@assembler.register(Sink)
def _(e, om, block):
    """Method containing the constraints for simple sinks

    Simple sinks are modeled with a fixed output value set for the
    variable of the output.

    Parameters
    ----------
    See :func:`assembler`.

    Returns
    -------
    See :func:`assembler`.
    """
    var.set_fixed_sink_value(om, block)
    return om


@assembler.register(Commodity)
def _(e, om, block):
    """Method containing the constraints for commodity

    Comoodity are modeled with a fixed output value set for the
    variable of the output.

    Parameters
    ----------
    See :func:`assembler`.

    Returns
    -------
    See :func:`assembler`.
    """
    lc.add_global_output_limit(om, block)
    return om


@assembler.register(transformer.Storage)
def _(e, om, block):
    """Simple storage assembler containing the constraints for simple
    storage components.

      Parameters
    ----------
    See :func:`assembler`.

    Returns
    -------
    See :func:`assembler`.
    """
    # add capacity variable
    block.cap = po.Var(block.uids, om.timesteps,
                       within=po.NonNegativeReals)

    def linear_constraints(om, block):
        lc.add_storage_balance(om, block)
        var.set_storage_cap_bounds(om, block)
        if not block.optimization_options.get("investment", False):
            var.set_bounds(om, block, side="output")
            var.set_bounds(om, block, side="input")
        else:
            lc.add_storage_charge_discharge_limits(om, block)

    block.default_optimization_options = {
        "linear_constr": linear_constraints}

    if block.optimization_options.get("investment", False):
        block.add_cap = po.Var(block.uids, within=po.NonNegativeReals)

    om.default_assembler(block)
    return(om)


@assembler.register(transports.Simple)
def _(e, om, block):
    """Simple transport assembler grouping the constraints
    for simple transport components

    The method uses the simple_transformer_assembler() method.

    Parameters
    ----------
    See :func:`assembler`.

    Returns
    -------
    See :func:`assembler`.
    """

    # input output relation for simple transport
    lc.add_simple_io_relation(om, block)
    # bounds
    var.set_bounds(om, block, side="output")
    return(om)

@assembler.register(ExcessSlack)
def _(e, om, block):
    """Excess slack assembler grouping the constraints
    for excess slack components.

    Parameters
    ----------
    See :func:`assembler`.

    Returns
    -------
    See :func:`assembler`.
    """

    # bounds
    # var.set_bounds(om, block, side="output")
    return(om)

@assembler.register(ShortageSlack)
def _(e, om, block):
    """Shortage slack assembler grouping the constraints
    for shortage slack components.

    Parameters
    ----------
    See :func:`assembler`.

    Returns
    -------
    See :func:`assembler`.
    """

    # bounds
    # var.set_bounds(om, block, side="output")
    return(om)
