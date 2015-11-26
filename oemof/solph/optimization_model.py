"""

@contact Simon Hilpert (simon.hilpert@fh-flensburg.de)
"""

from functools import singledispatch

import pyomo.environ as po
import logging
try:
    import variables as var
    import linear_mixed_integer_constraints as milc
    import linear_constraints as lc
    import predefined_objectives as predefined_objectives
    import objective_expressions as objfuncexprs
    from oemof.core.network.entities import Bus, Component
    from oemof.core.network.entities import components as cp
except:
    from . import variables as var
    from . import linear_mixed_integer_constraints as milc
    from . import linear_constraints as lc
    from . import predefined_objectives as predefined_objectives
    from . import objective_expressions as objfuncexprs
    from ..core.network.entities import Bus, Component
    from ..core.network.entities import components as cp

    from ..core.network.entities.components.transformers import (
        CHP, Simple, SimpleExtractionCHP, Storage)
    from ..core.network.entities.components.sources import (Commodity,
        DispatchSource, FixedSource)
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
        "\n\n {o}\n\n of type:\n\n {t}".format(o=entity, t=type(entity)))
    return om

class OptimizationModel(po.ConcreteModel):
    """Create Pyomo model of the energy system.

    Parameter
    ----------
    entities : list with all entity objects
    timesteps : list with all timesteps as integer values
    options : nested dictionary with options to set.

    """

    # TODO Cord: Take "next(iter(self.dict.values()))" where the first value of
    #            dict has to be selected
    def __init__(self, energysystem):
        super().__init__()

        self.entities = energysystem.entities
        self.timesteps = energysystem.simulation.timesteps

        self.objective_name = energysystem.simulation.objective_name

        self.T = po.Set(initialize=self.timesteps, ordered=True)
        # calculate all edges ([('coal', 'pp_coal'),...])
        self.components = [e for e in self.entities
                           if isinstance(e, Component)]
        self.all_edges = self.edges(self.components)
        var.add_continuous(model=self, edges=self.all_edges)

        # group components by type (cbt: components by type)
        cbt = {}
        for c in self.components:
          cbt[type(c)] = cbt.get(type(c), []) + [c]

        self.I = {c.uid: c.inputs[0].uid for c in self.components
                  if not isinstance(c, cp.Source)}
        self.O = {c.uid: [o.uid for o in c.outputs[:]] for c in self.components
                  if not isinstance(c, cp.Sink)}

        # set attributes lists per class with objects and uids for opt model
        for cls in cbt:
            objs = cbt[cls]
            # "call" methods to add the constraints opt. problem
            if objs: # Should always be nonempty but who knows...
                uids = [e.uid for e in objs]
                # add pyomo block per cls to OptimizationModel instance
                block = po.Block()
                block.uids = po.Set(initialize=uids)
                block.indexset = po.Set(initialize=block.uids*self.T)
                block.objs = objs
                block.optimization_options = cls.optimization_options
                self.add_component(str(cls), block)
                assembler.registry[cls](e=None, om=self, block=block)


        # add bus block
        block = po.Block()
        # get all bus objects
        block.objs = [e for e in self.entities if isinstance(e, Bus)]
        block.uids = [e.uid for e in block.objs]
        assembler.registry[Bus](e=None, om=self, block=block)
        self.add_component(str(Bus), block)

        # create objective function
        if self.objective_name is None:
            raise ValueError('No objective name defined!')

        self.objective_assembler(objective_name=self.objective_name)


    def default_assembler(self, block):
        """ Method for setting optimization model objects for blocks

        Parameter
        ----------
        self : OptimizationModel() instance
        block : SimpleBlock()
        """

        if (block.optimization_options.get('investment', False) and
            'milp_constr' in block.optimization_options):
            raise ValueError('Component can not be modeled with milp-constr ' +
                             'in investment mode!\n' +
                             'Please change `optimization_options`')

        if 'milp_constr' in block.optimization_options:
            # create binary status variables for block components
            var.add_binary(self, block)

        # add additional variables (investment mode)
        if block.optimization_options.get('investment', False):
            add_out_limit = {obj.uid: obj.add_out_limit
                             for obj in block.objs}
            def add_out_bound_rule(block, e):
               return (0, add_out_limit[e])
            block.add_out = po.Var(block.uids, within=po.NonNegativeReals,
                                   bounds=add_out_bound_rule)

        for option in block.optimization_options:
            if not option in ['objective', 'investment']:
                block.optimization_options[option]()


    def objective_assembler(self, objective_name="minimize_costs"):
        """ calls functions to add predefined objective functions

        """
        print('Creating predefined objective with name:', objective_name)
        if objective_name == 'minimize_costs':
            predefined_objectives.minimize_cost(self)


    def solve(self, solver='glpk', solver_io='lp', debug=False,
              duals=False, **kwargs):
        """ Method that takes care of the communication with the solver
        to solve the optimization model

        Parameters
        ----------

        self : pyomo.ConcreteModel
        solver str: solver to be used e.g. 'glpk','gurobi','cplex'
        solver_io str: str that defines the solver interaction
        (file or interface) 'lp','nl','python'
        **kwargs: other arguments for the pyomo.opt.SolverFactory.solve()
        method

        Returns
        -------
        self : solved pyomo.ConcreteModel() instance
        """

        from pyomo.opt import SolverFactory
        # Create a 'dual' suffix component on the instance
        # so the solver plugin will know which suffixes to collect
        if duals is True:
            # dual variables (= shadow prices)
            self.dual = po.Suffix(direction=po.Suffix.IMPORT)
            # reduced costs
            self.rc = po.Suffix(direction=po.Suffix.IMPORT)
        # write lp-file
        if debug == True:
            self.write('problem.lp',
                       io_options={'symbolic_solver_labels': True})
            # print instance
            # instance.pprint()

        # solve instance
        opt = SolverFactory(solver, solver_io=solver_io)
        # store results
        results = opt.solve(self, **kwargs)
        if debug == True:
            if (results.solver.status == "ok") and \
               (results.solver.termination_condition == "optimal"):
                # Do something when the solution in optimal and feasible
                self.solutions.load_from(results)

            elif (results.solver.termination_condition == "infeasible"):
                print("Model is infeasible",
                      "Solver Status: ", results.solver.status)
            else:
                # Something else is wrong
                print("Solver Status: ", results.solver.status, "\n"
                      "Termination condition: ",
                      results.solver.termination_condition)


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
        # e.g. [('coal', 'pp_coal'), ('pp_coal', 'b_el'),...]
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

    # slack variables that assures a feasible problem
    # get uids for busses that allow excess
    block.excess_uids = [b.uid for b in block.objs if b.excess == True]
    # get uids for busses that allow shortage
    block.shortage_uids = [b.uid for b in block.objs if b.shortage == True]

    # create variables for 'slack' of shortage and excess
    if block.excess_uids:
        block.excess_slack = po.Var(block.excess_uids,
                                    om.timesteps,
                                    within=po.NonNegativeReals)
    if block.shortage_uids:
        block.shortage_slack = po.Var(block.shortage_uids,
                                      om.timesteps,
                                      within=po.NonNegativeReals)

    print('Creating bus balance constraints ...')
    # bus balance constraint for energy bus objects
    lc.add_bus_balance(om, block)

    # set limits for buses
    lc.add_global_output_limit(om, block)
    return om

@assembler.register(Simple)
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

    def linear_constraints():
        lc.add_simple_io_relation(om, block)
        var.set_bounds(om, block, side='output')
    def objective_function_expressions():
        objfuncexprs.add_opex_var(om, block, ref='output')
        objfuncexprs.add_opex_fix(om, block, ref='output')
        objfuncexprs.add_input_costs(om, block)
        objfuncexprs.add_revenues(om, block)

    default_optimization_options = {
        'linear_constr': linear_constraints,
        'objective' : objective_function_expressions}

    if not block.optimization_options:
        block.optimization_options = default_optimization_options

    om.default_assembler(block)
    return om

@assembler.register(CHP)
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
    def linear_constraints():
        lc.add_simple_io_relation(om, block)
        lc.add_simple_chp_relation(om, block)
        var.set_bounds(om, block, side='output')
    def objective_function_expressions():
        objfuncexprs.add_opex_var(om, block, ref='output')
        objfuncexprs.add_opex_fix(om, block, ref='output')
        objfuncexprs.add_input_costs(om, block)
        objfuncexprs.add_revenues(om, block)

    default_optimization_options = {
        'linear_constr': linear_constraints,
        'objective' : objective_function_expressions}

    if not block.optimization_options:
        block.optimization_options = default_optimization_options

    # simple_transformer assebmler for in-out relation, pmin,.. etc.
    om.default_assembler(block)
    return om

@assembler.register(SimpleExtractionCHP)
def _(e, om, block):
    """Method grouping the constraints for simple chp components.

    Parameters
    ----------
    See :func:`assembler`.

    Returns
    -------
    See :func:`assembler`.
    """
    def linear_constraints():
        lc.add_simple_extraction_chp_relation(om, block)
        var.set_bounds(om, block, side='output')
        var.set_bounds(om, block, side='input')
    def objective_function_expressions():
        objfuncexprs.add_opex_var(om, block, ref='output')
        objfuncexprs.add_opex_fix(om, block, ref='output')
        objfuncexprs.add_input_costs(om, block)
        objfuncexprs.add_revenues(om, block)

    default_optimization_options = {
        'linear_constr': linear_constraints,
        'objective' : objective_function_expressions}

    if not block.optimization_options:
        block.optimization_options = default_optimization_options

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
    def linear_constraints():
        lc.add_fixed_source(om, block)
    def objective_function_expressions():
        objfuncexprs.add_opex_var(om, block, ref='output')
        objfuncexprs.add_opex_fix(om, block, ref='output')
    default_optimization_options = {
        'linear_constr': linear_constraints,
        'objective' : objective_function_expressions}

    if not block.optimization_options:
        block.optimization_options = default_optimization_options

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
    def linear_constraints():
        lc.add_dispatch_source(om, block)
    def objective_function_expressions():
        objfuncexprs.add_opex_var(om, block, ref='output')
        objfuncexprs.add_opex_fix(om, block, ref='output')
        objfuncexprs.add_curtailment_costs(om, block)

    default_optimization_options = {
        'linear_constr': linear_constraints,
        'objective' : objective_function_expressions}

    if not block.optimization_options:
        block.optimization_options = default_optimization_options

    if block.optimization_options.get('investment', False):
        raise ValueError('Dispatch source + investment is not possible!')

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

@assembler.register(Storage)
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

    def linear_constraints():
        lc.add_storage_balance(om, block)
        var.set_storage_cap_bounds(om, block)
        if not block.optimization_options.get('investment', False):
            var.set_bounds(om, block, side='output')
            var.set_bounds(om, block, side='input')
        else:
            lc.add_storage_charge_discharge_limits(om, block)
    def objective_function_expressions():
        objfuncexprs.add_opex_var(om, block, ref='output')
        objfuncexprs.add_opex_fix(om, block, ref='capacity')

    default_optimization_options = {
        'linear_constr': linear_constraints,
        'objective' : objective_function_expressions}

    if block.optimization_options:
        default_optimization_options.update(block.optimization_options)
    block.optimization_options = default_optimization_options

    if block.optimization_options.get('investment', False):
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
    var.set_bounds(om, block, side='output')
    return(om)
