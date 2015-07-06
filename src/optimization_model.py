import pyomo.environ as po
import components as cp


class OptimizationModel(po.ConcreteModel):
    """Create Pyomo model of the energy system.

    Parameters
    ----------
    entities : list with all entity objects
    timesteps : list with all timesteps as integer values
    invest : boolean

    Returns
    -------
    m : pyomo.ConcreteModel

    """

    def __init__(self, entities, timesteps, invest):

        super().__init__()

        self.entities = entities
        self.timesteps = timesteps
        self.invest = invest

        # create lists with objects of entitiy child-classes
        self.bus_objs = [e for e in self.entities if isinstance(e, cp.Bus)]
        self.simple_transformer_objs = [e for e in self.entities
                                        if isinstance(e, cp.SimpleTransformer)]
        self.simple_chp_objs = [e for e in self.entities
                                if isinstance(e, cp.SimpleCHP)]
        self.renewable_source_objs = [e for e in self.entities
                                      if isinstance(e, cp.RenewableSource)]
        self.sink_objs = [e for e in self.entities if isinstance(e, cp.Sink)]
        self.simple_storage_objs = [e for e in self.entities
                                    if isinstance(e, cp.SimpleStorage)]
        self.commodity_objs = [e for e in self.entities
                               if isinstance(e, cp.Commodity)]
        self.simple_transport_objs = [e for e in self.entities
                                      if isinstance(e, cp.SimpleTransport)]

        # create lists of uids as math-sets for optimization model
        self.bus_uids = [b.uid for b in self.bus_objs]
        self.simple_transformer_uids = [c.uid for c in
                                        self.simple_transformer_objs]
        self.simple_chp_uids = [c.uid for c in self.simple_chp_objs]
        self.renewable_source_uids = [c.uid for c in
                                      self.renewable_source_objs]
        self.simple_storage_uids = [c.uid for c in self.simple_storage_objs]
        self.sink_uids = [c.uid for c in self.sink_objs]
        self.commodity_uids = [c.uid for c in self.commodity_objs]
        self.simple_transport_uids = [c.uid for c in
                                      self.simple_transport_objs]

        # calculate all edges ([('coal', 'pp_coal'),...])
        self.all_edges = self.edges([e for e in self.entities
                                    if isinstance(e, cp.Component)])

        # "call" the mehtods to add the constraints and variables
        # to optimization problem
        self.create_variables()
        self.bus_model()
        self.simple_chp_model()
        self.renewable_source_model()
        self.simple_transformer_model()
        self.simple_storage_model()
        self.commodity_model()
        self.objective()
        self.simple_transport_model()
        self.sink_model()

    def create_variables(self):
        # variable for edges
        self.w = po.Var(self.all_edges, self.timesteps, within=po.NonNegativeReals)
        self.w.pprint()

        # additional variable for investment models
        if(self.invest is True):
            self.w_add = po.Var(self.all_edges, within=po.NonNegativeReals)

    def bus_model(self):
        """bus model creates bus balance for all buses using pyomo.Constraint

        Parameters
        ----------
        self : pyomo.ConcreteModel

        Returns
        -------
        self : pyomo.ConcreteModel
        """

        # slack variable that assures a feasible problem
        self.bus_slack = po.Var(self.bus_uids, self.timesteps,
                                within=po.NonNegativeReals)

        # constraint for bus balance:
        # component inputs/outputs are negative/positive in the bus balance
        def bus_rule(self, e, t):
            expr = 0
            expr += -sum(self.w[(i, j), t] for (i, j) in self.all_edges if i == e)
            expr += sum(self.w[(i, j), t] for (i, j) in self.all_edges if j == e)
            expr += -self.bus_slack[e, t]
            return(expr, 0)
        self.bus = po.Constraint(self.bus_uids, self.timesteps, rule=bus_rule)

    def simple_transformer_model(self):
        """Simple transformer model containing the constraints
        for simple transformer components.

        Parameters
        ----------
        self : pyomo.ConcreteModel

        Returns
        -------
        self : pyomo.ConcreteModel


        **Mathematical equations**

        Sets containing the inputs/outputs for all simple transformers:

        .. math::

            &E_{SF}, \\quad \\text{Set with all simple transformers}\\\\
            &I = \\{ i | i \\subset E_B, (i,e) \\in \\vec{E},
            e \\in E_{SF}\\}, \\quad \\text{All inputs for } e \\in E_{SF}\\\\
            &O = \\{ o | o \\subset E_B, (e,o) \\in \\vec{E},
            e \\in E_{SF}\\}, \\quad \\text{All outputs for } e \\in E_{SF}\\\\

        The model equations for operational models are described as follows.
        Constraint for input/output relation:

        .. math::

            w(I(e), e,t) \cdot \eta_(e) - w(e,O(e),t) = 0, \\quad
            \\forall e \\in E_{SF}, \\forall t \\in T\\\\

        For investment models the additional constraint must hold:

        .. math::

            w(I(e), e, t) \\leq in_{max}(e1) + w_{add}(I(e), e), \\quad
            \\forall t \\in T, \\forall e \\in E_{SF}\\\\
        """

        # temp set with input uids for every simple transformer
        I = {obj.uid: obj.inputs[0].uid
             for obj in self.simple_transformer_objs}
        # set with output uids for every simple transformer
        O = {obj.uid: obj.outputs[0].uid
             for obj in self.simple_transformer_objs}
        eta = {obj.uid: obj.eta for obj in self.simple_transformer_objs}

        # constraint for simple transformers: input * efficiency = output
        def in_out_rule(self, e, t):
            expr = 0
            expr += self.w[I[e], e, t] * eta[e]
            expr += - self.w[e, O[e], t]
            return(expr, 0)
        self.simple_transformer_c = po.Constraint(self.simple_transformer_uids,
                                                  self.timesteps,
                                                  rule=in_out_rule)

        # set variable bounds (out_max = in_max * efficiency):
        # m.i_max = {'pp_coal': 51794.8717948718, ... }
        # m.o_max = {'pp_coal': 20200, ... }
        self.i_max = {obj.uid: obj.in_max
                      for obj in self.simple_transformer_objs}
        self.o_max = {obj.uid: obj.out_max for obj in
                      self.simple_transformer_objs}

        # set bounds for basic/investment models
        if(self.invest is False):
            # edges for simple transformers ([('coal', 'pp_coal'),...])
            ee = self.edges(self.simple_transformer_objs)
            for (e1, e2) in ee:
                for t in self.timesteps:
                    # transformer output <= self.o_max
                    if e1 in self.simple_transformer_uids:
                        self.w[e1, e2, t].setub(self.o_max[e1])
                    # transformer input <= self.i_max
                    if e2 in self.simple_transformer_uids:
                        self.w[e1, e2, t].setub(self.i_max[e2])
        else:
            # constraint for additional capacity
            def invest_rule(self, e, t):
                expr = 0
                expr += self.w[I[e], e, t]
                rhs = self.i_max[e] + self.w_add[I[e], e]
                return(expr <= rhs)
            self.simple_transformer_max_input_c = \
                po.Constraint(self.simple_transformer_uids, self.timesteps,
                              rule=invest_rule)

    def simple_chp_model(self):
        """Simple chp model containing the constraints for simple chp
        components.

        Parameters
        ----------
        self : pyomo.ConcreteModel

        Returns
        -------
        self : pyomo.ConcreteModel

        """

        # temp set with input uids for every simple chp
        # {'pp_chp': 'gas'}
        I = {obj.uid: obj.inputs[0].uid for obj in self.simple_chp_objs}
        # set with output uids for every simple chp
        # {'pp_chp': ['b_th', 'b_el']}
        O = {obj.uid: [o.uid for o in obj.outputs[:]]
             for obj in self.simple_chp_objs}
        # efficiencies for simple chps
        eta = {obj.uid: obj.eta for obj in self.simple_chp_objs}

        # constraint for transformer energy balance:
        # E = P + Q / (eta_el + eta_th) = P / eta_el = Q/ eta_th
        # (depending on the position of the outputs and eta)
        def in_out_rule(self, e, t):
            expr = 0
            expr += self.w[I[e], e, t]
            expr += -sum(self.w[e, o, t] for o in O[e]) / \
                (eta[e][0] + eta[e][1])
            return(expr, 0)
        self.simple_chp_c1 = po.Constraint(self.simple_chp_uids,
                                           self.timesteps, rule=in_out_rule)

        # additional constraint for power to heat ratio of simple chp comp:
        # P/eta_el = Q/eta_th
        def chp_rule(self, e, t):
            expr = 0
            expr += self.w[e, O[e][0], t] / eta[e][0]
            expr += -self.w[e, O[e][1], t] / eta[e][1]
            return(expr, 0)
        self.simple_chp_c2 = po.Constraint(self.simple_chp_uids,
                                           self.timesteps,
                                           rule=chp_rule)
        # set variable bounds
        if(self.invest is False):
            self.i_max = {obj.uid: obj.in_max for obj in self.simple_chp_objs}
            # yields nested dict e.g: {'chp': {'home_th': 40, 'region_el': 30}}
            self.o_max = {obj.uid: dict(zip(O[obj.uid], obj.out_max))
                          for obj in self.simple_chp_objs}

            # edges for simple chps ([('gas', 'pp_chp'), ('pp_chp', 'b_th'),..)
            ee = self.edges(self.simple_chp_objs)
            for (e1, e2) in ee:
                for t in self.timesteps:
                    # chp input <= self.i_max
                    if e2 in self.simple_chp_uids:
                        self.w[e1, e2, t].setub(self.i_max[e2])
                    # chp outputs <= self.o_max
                    if e1 in self.simple_chp_uids:
                        self.w[e1, e2, t].setub(self.o_max[e1][e2])

    def renewable_source_model(self):
        """Simple renewable source model containing the constraints for
        renewable source sources.

        Parameters
        ----------
        self : pyomo.ConcreteModel

        Returns
        -------
        self : pyomo.ConcreteModel
        """
        # outputs: {'pv': 'b_el', 'wind_off': 'b_el', ... }
        O = {obj.uid: obj.outputs[0].uid
             for obj in self.renewable_source_objs}
        # normed value of renewable source (0 <= value <=1)
        self.source_val = {obj.uid: obj.val
                           for obj in self.renewable_source_objs}
        # maximal ouput of renewable source (in general installed capacity)
        self.out_max = {obj.uid: obj.out_max
                        for obj in self.renewable_source_objs}
        # flag if dispatch is true or false for each object
        self.dispatch = {obj.uid: obj.dispatch
                         for obj in self.renewable_source_objs}

        # if one one RenewableSource() instance attribute is dispatch=True
        if(True in self.dispatch.values()):
            # get only the RenewableSource() instance that have dispatch
            self.renewable_sources_dispatch_uids = [k for (k, v) in
                                                    self.dispatch.items()
                                                    if v is True]
            # Set to define dispatch variable
            self.renewable_dispatch_v = \
                po.Var(self.renewable_sources_dispatch_uids, self.timesteps,
                       within=po.NonNegativeReals)

            # constraint to determine how much renewable energy is dispatched
            def dispatch_rule(self, e, t):
                expr = self.renewable_dispatch_v[e, t]
                expr += - self.source_val[e][t] * self.out_max[e] + \
                    self.w[e, O[e], t]
                return(expr, 0)

            self.renewable_source_dispatch_c = \
                po.Constraint(self.renewable_sources_dispatch_uids,
                              self.timesteps, rule=dispatch_rule)
        # set bounds for basic/investment models
        # TODO: include dispatch if invest=True
        if(self.invest is False):
            # edges for renewables ([('wind_on', 'b_el'), ...)
            ee = self.edges(self.renewable_source_objs)
            # fixed value
            for (e1, e2) in ee:
                for t in self.timesteps:
                    self.w[(e1, e2), t].setub(self.source_val[e1][t] *
                                              self.out_max[e1])
                    self.w[(e1, e2), t].setlb(self.source_val[e1][t] *
                                              self.out_max[e1] *
                                              (1-self.dispatch[e1]))

        else:
            if(True in self.dispatch.values()):
                raise ValueError("Dispatchable renewables are not possible in"
                                 "investment models.\n Please reset flag from"
                                 "True to False")

            # constraint to allow additional capacity for renewables
            def invest_rule(self, e, t):
                expr = 0
                expr += self.w[e, O[e], t]
                rhs = (self.out_max[e] + self.w_add[e, O[e]]) * \
                    self.source_val[e][t]
                return(expr <= rhs)
            self.source_c = po.Constraint(self.renewable_source_uids,
                                          self.timesteps, rule=invest_rule)

    def commodity_model(self):
        """Simple commdity model containing the constraints for commodity
        sources.

        Parameters
        ----------
        self : pyomo.ConcreteModel

        Returns
        -------
        self : pyomo.ConcreteModel
        """

        self.yearly_limit = {obj.uid: obj.yearly_limit
                             for obj in self.commodity_objs}
        # outputs: {'rcoal': ['coal'], 'rgas': ['gas'],...}
        O = {obj.uid: [obj.outputs[0].uid] for obj in self.commodity_objs}

        # set upper bounds: sum(yearly commodity output) <= yearly_limit
        def commodity_limit_rule(self, e):
            expr = 0
            expr += sum(self.w[e, o, t] for t in self.timesteps for o in O[e])
            ub = self.yearly_limit[e]
            return(0, expr, ub)
        self.commodity_limit_c = po.Constraint(self.commodity_uids,
                                               rule=commodity_limit_rule)

    def sink_model(self):
        """Sink model containing the constraints for sinks.

        Parameters
        ----------
        self : pyomo.ConcreteModel

        Returns
        -------
        self : pyomo.ConcreteModel
        """

        self.sink_val = {obj.uid: obj.val for obj in self.sink_objs}
        ee = self.edges(self.sink_objs)
        for (e1, e2) in ee:
            # setting upper and lower bounds for variable corresponding to
            # edge from buses to sinks
            for t in self.timesteps:
                self.w[(e1, e2), t].setub(self.sink_val[e2][t])
                self.w[(e1, e2), t].setlb(self.sink_val[e2][t])

    def simple_storage_model(self):
        """Simple storage model containing the constraints for simple storage
        components.

        Parameters
        ----------
        m : pyomo.ConcreteModel

        Returns
        -------
        m : pyomo.ConcreteModel
        """

        self.soc_max = {obj.uid: obj.soc_max
                        for obj in self.simple_storage_objs}
        self.soc_min = {obj.uid: obj.soc_min
                        for obj in self.simple_storage_objs}

        O = {obj.uid: obj.outputs[0].uid for obj in self.simple_storage_objs}
        I = {obj.uid: obj.inputs[0].uid for obj in self.simple_storage_objs}

        # set bounds for basic/investment models
        if(self.invest is False):
            ee = self.edges(self.simple_storage_objs)
            # installed input/output capacity
            for (e1, e2) in ee:
                for t in self.timesteps:
                    self.w[e1, e2, t].setub(10)
                    self.w[e1, e2, t].setlb(1)

            # rule for creating upper and lower bounds for
            # storage state of charge variable (soc_v) for operational mode
            def soc_var_bounds(self, e, t):
                return(self.soc_min[e], self.soc_max[e])
            self.soc_v = po.Var(self.simple_storage_uids, self.timesteps,
                                bounds=soc_var_bounds)
        else:
            self.soc_v = po.Var(self.simple_storage_uids, self.timesteps,
                                within=po.NonNegativeReals)
            # creating additional variable for planning models used
            self.soc_add_v = po.Var(self.simple_storage_uids,
                                    within=po.NonNegativeReals)

            # constraint for additional capacity in investment models
            def invest_rule(self, e, t):
                return(self.soc_v[e, t] <= self.soc_max[e] + self.soc_add_v[e])
            self.soc_max_c = po.Constraint(self.simple_storage_uids,
                                           self.timesteps,
                                           rule=invest_rule)

        # storage energy balance
        def storage_balance_rule(self, e, t):
            if(t == 0):
                expr = 0
                expr += self.soc_v[e, t] - 0.5 * self.soc_max[e]
                return(expr, 0)
            else:
                expr = self.soc_v[e, t]
                expr += - self.soc_v[e, t-1] - self.w[I[e], e, t] + \
                    self.w[e, O[e], t]
                return(expr, 0)
            self.simple_storage_c = po.Constraint(self.simple_storage_uids,
                                                  self.timesteps,
                                                  rule=storage_balance_rule)

    def simple_transport_model(self):
        """Simple transport model building the constraints
        for simple transport components

        Parameters
        ----------
        m : pyomo.ConcreteModel

        Returns
        -------
        m : pyomo.ConcreteModel
        """

        # temp set with input uids for every simple transport
        I = {obj.uid: obj.inputs[0].uid for obj in self.simple_transport_objs}
        # set with output uids for every simple transport
        O = {obj.uid: obj.outputs[0].uid for obj in self.simple_transport_objs}
        eta = {obj.uid: obj.eta for obj in self.simple_transport_objs}

        # constraint for simple transports: input * efficiency = output
        def in_out_rule(self, e, t):
            expr = 0
            expr += self.w[I[e], e, t] * eta[e]
            expr += - self.w[e, O[e], t]
            return(expr, 0)
        self.simple_transport_eta_c = po.Constraint(self.simple_transport_uids,
                                                    self.timesteps,
                                                    rule=in_out_rule)

        # set variable bounds (out_max = in_max * efficiency):
        self.i_max = {obj.uid: obj.in_max
                      for obj in self.simple_transport_objs}
        self.o_max = {obj.uid: obj.out_max
                      for obj in self.simple_transport_objs}

        # set bounds for basic/investment models
        if(self.invest is False):
            # edges for simple transport ([('b_el', 'b_el2'),...])
            ee = self.edges(self.simple_transport_objs)
            for (e1, e2) in ee:
                for t in self.timesteps:
                    # transport output <= self.o_max
                    if e1 in self.simple_transport_uids:
                        self.w[e1, e2, t].setub(self.o_max[e1])
                    # transport input <= self.i_max
                    if e2 in self.simple_transport_uids:
                        self.w[e1, e2, t].setub(self.i_max[e2])
        else:
            # constraint for additional capacity
            def invest_rule(self, e, t):
                return(self.w[I[e], e, t] <= self.i_max[e] +
                       self.w_add[I[e], e])
            self.simple_transport_invest_c = \
                po.Constraint(self.simple_transport_uids, self.timesteps,
                              rule=invest_rule)

    def objective(self):
        """Function that creates the objective function of the optimization
        model.

        Parameters
        ----------
        m : pyomo.ConcreteModel

        Returns
        -------
        m : pyomo.ConcreteModel
        """

        # create a combine list of all cost-related components
        objective_objs = (
            self.simple_chp_objs +
            self.simple_transformer_objs +
            self.simple_storage_objs +
            self.simple_transport_objs)

        self.objective_uids = (
            self.simple_chp_uids +
            self.simple_transformer_uids +
            self.simple_transport_uids)

        I = {obj.uid: obj.inputs[0].uid for obj in objective_objs}
        # operational costs
        self.opex_var = {obj.uid: obj.opex_var for obj in objective_objs}
        # get dispatch expenditure for renewable energies with dispatch
        self.dispatch_ex = {obj.uid: obj.dispatch_ex
                            for obj in self.renewable_source_objs
                            if obj.dispatch is True}

        # objective function
        def obj_rule(self):
            expr = 0
            expr += sum(self.w[I[e], e, t] * self.opex_var[e]
                        for e in self.objective_uids
                        for t in self.timesteps)
            expr += sum(self.bus_slack[e, t] * 10e4
                        for e in self.bus_uids
                        for t in self.timesteps)

            # costs for dispatchable renewables
            if(True in self.dispatch.values()):
                expr += sum(self.renewable_dispatch_v[e, t] *
                            self.dispatch_ex[e]
                            for e in self.renewable_sources_dispatch_uids
                            for t in self.timesteps)
            # add additional capacity & capex for investment models
            if(self.invest is True):
                self.capex = {obj.uid: obj.capex for obj in objective_objs}

                expr += sum(self.w_add[I[e], e] * self.capex[e]
                            for e in self.objective_uids)
                expr += sum(self.soc_add[e] * self.capex[e]
                            for e in self.simple_storage_uids)
            return(expr)
        self.objective = po.Objective(rule=obj_rule)

    def solve(self, solver='glpk', solver_io='lp', debug=False, **kwargs):
        """Method that creates the instance of the model and solves it.

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
        self : solved pyomo.ConcreteModel instance
        """

        from pyomo.opt import SolverFactory

        # create model instance
        instance = self.create()

        # write lp-file
        if(debug is True):
            instance.write('problem.lp',
                           io_options={'symbolic_solver_labels': True})
            # print instance
            instance.pprint()
        # solve instance
        opt = SolverFactory(solver, solver_io=solver_io)
        # store results
        results = opt.solve(instance, **kwargs)
        # load results back in instance
        instance.load(results)

        return(instance)

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


def results_to_objects(entities, instance):
    """Function that converts the results.

    Parameters
    ----------
    components : list of component objects

    Returns
    -------
    results : dictionary with results for every instance of a class
    """
    for e in entities:
        if (isinstance(e, cp.Transformer) or isinstance(e, cp.Source) or
                isinstance(e, cp.SimpleTransport)):
            e.results['Output'] = {}
            O = [e.uid for e in e.outputs[:]]
            for o in O:
                e.results['Output'][o] = []
                for t in instance.timesteps:
                    e.results['Output'][o].append(instance.w[e.uid,
                                                  o, t].value)
        if isinstance(e, cp.SimpleStorage):
            for t in instance.timesteps:
                e.results['Input'].append(instance.w[e.inputs[0].uid,
                                          e.uid, o, t].value)
        # write results to self.sink_objs
        # (will be the value of Sink in general)
        if isinstance(e, cp.Sink):
            e.results['Input'] = []
            for t in instance.timesteps:
                e.results['Input'].append(instance.w[e.inputs[0].uid,
                                          e.uid, t].value)

    if(instance.invest is True):
        for e in entities:
            if isinstance(e, cp.Transformer):
                e.results['Invest'] = instance.w_add[e.inputs[0].uid,
                                                     e.uid].value
            if isinstance(e, cp.Source):
                e.results['Invest'] = instance.w_add[e.uid,
                                                     e.outputs[0].uid].value
            if isinstance(e, cp.SimpleStorage):
                e.results['Invest'] = instance.soc_add[e.uid].value


def io_sets(components):
    """Function that gets inputs and outputs for given components.

    Parameters
    ----------
    components : list of component objects

    Returns
    -------
    (I, O) : lists with tupels that represent the edges
    """
    O = {obj.uid: [o.uid for o in obj.outputs[:]] for obj in components}
    I = {obj.uid: [i.uid for i in obj.inputs[:]] for obj in components}
    return(I, O)
