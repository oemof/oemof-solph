# -*- coding: utf-8 -*-
import pyomo.environ as po
from pyomo.opt import SolverFactory
from .plumbing import sequence

class Model(po.ConcreteModel):
    """

    An energy generic solph energy system model that serves as basis for other
    models:

     * DispatchModel (LP, no investment),
     * UnitCommitmentModel (MILP, no investment),
     * InvestmentModel (LP, investment, no multiperiod),
     * ExpansionModel (LP, investment, multiperiod),
     * PowerflowModel (LP)

    Parameters
    ----------
    scenario : EnergyScenario object
        Object that holds the nodes of an oemof energy system graph
    constraint_groups : list
        Solph looks for these groups in the given energy system and uses them
        to create the constraints of the optimization problem.
        Defaults to :const:`OperationalModel.CONSTRAINTS`
    timeindex : pandas DatetimeIndex
        The time index will be used to calculate the timesteps and the
        time increment for the optimization model.
    timesteps : sequence (optional)
        Timesteps used in the optimization model. If provided as list or
        pandas.DatetimeIndex the sequence will be used to index the time
        dependent variables, constraints etc. If not provided we will try to
        compute this sequence from attr:`timeindex`.
    timeincrement : float or list of floats (optional)
        Time increment used in constraints and objective expressions.
        If type is 'float', will be converted internally to
        solph.plumbing.Sequence() object for time dependent time increment.
        If a list is provided this list will be taken. Default is calculated
        from timeindex if provided.
    periods: sequence (optional)

    periodincrement: sequence (optional)

    **The following sets are created**:

    NODES :
        A 1-dimensional set with all nodes of the given energy system.

    TIMEINDEX :
        A 2-dimensional set indexed (a,t) with the periods a and timesteps t

    TIMESTEPS :
        A set with all timesteps of the given given problem

    PERIODS :
        A 1-dimensional set indexed with all periods

    PERIODS_TIMESTEPS:
        A 1-dimensional set

    FLOWS :
        A 2 dimensional set with all flows. Index: `(source, target)`


    **The following variables are created**:

    flow
        Flow from source to target indexed by FLOWS x TIMEINDEX.
        Note: Bounds of this variable are set depending on attributes of
        the corresponding flow object.

    """
    def __init__(self, es, kwargs):
        super().__init__()

        self.name = kwargs.get('name', type(self).__name__)
        self.es = es
        self.timeindex = kwargs.get('timeindex', es.timeindex)
        self.timesteps = kwargs.get('timesteps', range(len(self.timeindex)))
        self.timeincrement = kwargs.get('timeincrement',
                                        self.timeindex.freq.nanos / 3.6e12)

        self.period_type = kwargs.get('period_type', 'year')
        # convert to sequence object for time dependent timeincrement
        self.timeincrement = sequence(self.timeincrement)

        self._constraint_groups = (type(self).CONSTRAINT_GROUPS +
                                   kwargs.get('constraint_groups', []))

        # dictionary with all flows containing flow objects as values und
        # tuple of string representation of oemof nodes (source, target)
        self.flows = es.flows()


        # ###########################  SETS  ##################################
        # set with all nodes
        self.NODES = po.Set(initialize=[n for n in self.es.nodes])

        # dict helper: {'period1': 0, 'period2': 1, ...}
        periods = getattr(es.timeindex, self.period_type)
        d = dict(zip(set(periods),range(len(set(periods)))))

        # TODO: claculate period incerment based on  d
        self.periodincrement = sequence(1)

        # pyomo set for timesteps of optimization problem
        self.TIMEINDEX = po.Set(
            initialize=list(zip([d[a] for a in periods],
                                range(len(es.timeindex)))),
                                ordered=True)

        self.PERIODS = po.Set(initialize=range(len(set(periods))))

        self.TIMESTEPS = po.Set(initialize=self.timesteps, ordered=True)

        # TODO: Make this robust
        self.PERIOD_TIMESTEPS = {a: range( int( len(self.TIMESTEPS) /
                                                len(self.PERIODS) )
                                         )
                                 for a in self.PERIODS}
        # previous timesteps
        previous_timesteps = [x - 1 for x in self.timesteps]
        previous_timesteps[0] = self.timesteps[-1]

        self.previous_timesteps = dict(zip(self.TIMESTEPS, previous_timesteps))
        # self.PREVIOUS_TIMESTEPS = po.Set(self.TIMESTEPS,
        #                            initialize=dict(zip(self.TIMESTEPS,
        #                                                previous_timesteps)))

        # pyomo set for all flows in the energy system graph
        self.FLOWS = po.Set(initialize=self.flows.keys(),
                            ordered=True, dimen=2)



    def add_flow(self):
        """
        """
        # non-negative pyomo variable for all existing flows
        self.flow = po.Var(self.FLOWS, self.TIMEINDEX,
                           within=po.NonNegativeReals)

    def add_blocks(self):
        """
        """
        # loop over all constraint groups to add constraints to the model
        for group in self._constraint_groups:
            # create instance for block
            block = group()
            # Add block to model
            self.add_component(str(block), block)
            # create constraints etc. related with block for all nodes
            # in the group
            block._create(group=self.es.groups.get(group))

    def add_objective(self, sense=po.minimize, update=False):
        """
        """
        if update:
            self.del_component('objective')

        expr = 0

        # Expression for investment flows
        for block in self.component_data_objects():
            if hasattr(block, '_objective_expression'):
                expr += block._objective_expression()

        self.objective = po.Objective(sense=sense, expr=expr)

    def receive_duals(self, suffixes=['dual', 'rc']):
        """ Method sets solver suffix to extract information about dual
        variables etc. from solver. Shadow prices (duals) and reduced costs
        (rc) are set as attributes of the model.

        """
        for s in suffixes:
            setattr(self, s, po.Suffix(direction=po.Suffix.IMPORT))

    def solve(self, solver='glpk', solver_io='lp', **kwargs):
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

        self.solutions.load_from(results)

        # storage optimization results in result dictionary of energysystem
        self.es.results = self.results()
        self.es.results.objective = self.objective()
        self.es.results.solver = results

        return results