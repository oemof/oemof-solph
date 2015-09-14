import pyomo.environ as po
try:
    import generic as gc
    from network.entities import Bus, Component
    from network.entities import components as cp
except:
    from . import generic as gc
    from .network.entities import Bus, Component
    from .network.entities import components as cp


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

    def __init__(self, entities, timesteps, options=None):

        super().__init__()

        self.entities = entities
        self.timesteps = timesteps
        self.invest = options.get("invest", False)
        self.slack = options.get("slack", {"excess": True,
                                           "shortage": False})

        # calculate all edges ([('coal', 'pp_coal'),...])
        self.all_edges = self.edges([e for e in self.entities
                                     if isinstance(e, Component)])
        gc.generic_variables(model=self, edges=self.all_edges,
                             timesteps=self.timesteps)

        # list with all necessary classes
        component_classes = (cp.Transformer.__subclasses__() +
                             cp.Sink.__subclasses__() +
                             cp.Source.__subclasses__() +
                             cp.Transport.__subclasses__())
        # set attributes lists per class with objects and uids for opt model
        for cls in component_classes:
            objs = [e for e in self.entities if isinstance(e, cls)]
            uids = [e.uid for e in objs]
            setattr(self, cls.lower_name + "_objs", objs)
            setattr(self, cls.lower_name + "_uids", uids)
            # "call" methods to add the constraints opt. problem
            if objs:
                getattr(self, cls.lower_name + "_model")(objs=objs, uids=uids)

        self.bus_model()
        self.objective()

    def bus_model(self):
        """bus model creates bus balance for all buses using pyomo.Constraint

        Parameters
        ----------
        self : pyomo.ConcreteModel

        Returns
        -------
        self : pyomo.ConcreteModel
        """
        self.bus_objs = [e for e in self.entities if isinstance(e, Bus)]
        self.bus_uids = [e.uid for e in self.bus_objs]

        bus_objs = [obj for obj in self.bus_objs
                    if any([obj.type == "el", obj.type == "th"])]
        bus_uids = [obj.uid for obj in bus_objs]

        # slack variables that assures a feasible problem
        if self.slack["excess"] is True:
            self.excess_slack = po.Var(self.bus_uids, self.timesteps,
                                       within=po.NonNegativeReals)
        if self.slack["shortage"] is True:
            self.shortage_slack = po.Var(self.bus_uids, self.timesteps,
                                         within=po.NonNegativeReals)
        I = {b.uid: [i.uid for i in b.inputs] for b in bus_objs}
        O = {b.uid: [o.uid for o in b.outputs] for b in bus_objs}

        # constraint for bus balance:
        # component inputs/outputs are negative/positive in the bus balance
        def bus_rule(self, e, t):
            expr = 0
            expr += -sum(self.w[e, o, t] for o in O[e])
            expr += sum(self.w[i, e, t] for i in I[e])
            if self.slack["excess"] is True:
                expr += -self.excess_slack[e, t]
            if self.slack["shortage"] is True:
                expr += self.shortage_slack[e, t]
            return(expr, 0)
        self.bus = po.Constraint(bus_uids, self.timesteps, rule=bus_rule)

        # select only buses that are resources (gas, oil, etc.)
        rbus_objs = [obj for obj in self.bus_objs
                     if all([obj.type != "el", obj.type != "th"])]
        rbus_uids = [e.uid for e in rbus_objs]

        # set limits for resource buses
        gc.generic_limit(model=self, objs=rbus_objs, uids=rbus_uids,
                         timesteps=self.timesteps)

    def simple_transformer_model(self, objs, uids):
        """Generic transformer model containing the constraints
        for generic transformer components.

        Parameters
        ----------
        self : pyomo.ConcreteModel

        Returns
        -------
        self : pyomo.ConcreteModel
        """

        gc.generic_io_constraints(model=self, objs=objs, uids=uids,
                                  timesteps=self.timesteps)

        # set bounds for variables  models
        if self.invest is False:
            gc.generic_w_ub(model=self, objs=objs, uids=uids,
                            timesteps=self.timesteps)
        else:
            gc.generic_w_ub_invest(model=self, objs=objs, uids=uids,
                                   timesteps=self.timesteps)

    def simple_chp_model(self, objs, uids):
        """Simple chp model containing the constraints for simple chp
        components.

        Parameters
        ----------
        self : pyomo.ConcreteModel

        Returns
        -------
        self : pyomo.ConcreteModel

        """
        # use generic_transformer model for in-out relation and
        # upper/lower bounds
        self.simple_transformer_model(objs=objs, uids=uids)

        # use generic constraint to model PQ relation (P/eta_el = Q/eta_th)
        gc.generic_chp_constraint(model=self, objs=objs, uids=uids,
                                  timesteps=self.timesteps)

    def fixed_source_model(self, objs, uids):
        """fixed source model containing the constraints for
        fixed sources.

        Parameters
        ----------
        self : pyomo.ConcreteModel

        Returns
        -------
        self : pyomo.ConcreteModel
        """
        if self.invest is False:
            gc.generic_fixed_source(model=self, objs=objs, uids=uids,
                                    timesteps=self.timesteps)
        else:
            gc.generic_fixed_source_invest(model=self, objs=objs, uids=uids,
                                           timesteps=self.timesteps)

    def dispatch_source_model(self, objs, uids):
        """
        """
        if self.invest is False:
            gc.generic_dispatch_source(model=self, objs=objs, uids=uids,
                                       timesteps=self.timesteps)

    def simple_sink_model(self, objs, uids):
        """simple sink model containing the constraints for simple sinks
        Parameters
        ----------
        self : pyomo.ConcreteModel

        Returns
        -------
        self : pyomo.ConcreteModel
        """
        gc.generic_fixed_sink(model=self, objs=objs, uids=uids,
                              timesteps=self.timesteps)

    def simple_storage_model(self, objs, uids):
        """Simple storage model containing the constraints for simple storage
        components.

        Parameters
        ----------
        m : pyomo.ConcreteModel

        Returns
        -------
        m : pyomo.ConcreteModel
        """

        # set bounds for basic/investment models
        if(self.invest is False):
            gc.generic_w_ub(model=self, objs=objs, uids=uids,
                            timesteps=self.timesteps)
        else:
            gc.generic_soc_ub_invest(model=self, objs=objs, uids=uids,
                                     timesteps=self.timesteps)

        O = {obj.uid: obj.outputs[0].uid for obj in objs}
        I = {obj.uid: obj.inputs[0].uid for obj in objs}

        soc_initial = {obj.uid: obj.soc_initial
                       for obj in self.simple_storage_objs}
        cap_loss = {obj.uid: obj.cap_loss for obj in self.simple_storage_objs}
        eta_in = {obj.uid: obj.eta_in[0] for obj in self.simple_storage_objs}
        eta_out = {obj.uid: obj.eta_out[0] for obj in self.simple_storage_objs}

        # storage energy balance
        def storage_balance_rule(self, e, t):
            # TODO:
            #   - include time increment
            #   - not sure, if the old pahesmf storage equation is valid!
            #     Cord would prefer something like this:
            #     http://publica.fraunhofer.de/documents/N-300374.html
            #   - check this against pahesmf equations for soc in first/last
            #     and keep one of both solutions
#            if(t == 0 or t == len(self.timesteps)-1):
            if(t == 0):
                expr = 0
#                expr += self.soc[e, t] - soc_initial[e]
                expr += self.soc[e, t]
                expr += - self.soc[e, t+len(self.timesteps)-1]
                expr += - self.w[I[e], e, t] * eta_in[e]
                expr += + self.w[e, O[e], t] / eta_out[e]
                return(expr, 0)
            else:
                expr = self.soc[e, t] * (1 - cap_loss[e])
                expr += - self.soc[e, t-1]
                expr += - self.w[I[e], e, t] * eta_in[e]
                expr += + self.w[e, O[e], t] / eta_out[e]
                return(expr, 0)
        self.simple_storage_c = po.Constraint(uids, self.timesteps,
                                              rule=storage_balance_rule)

    def simple_transport_model(self, objs, uids):
        """Simple transport model building the constraints
        for simple transport components

        Parameters
        ----------
        m : pyomo.ConcreteModel

        Returns
        -------
        m : pyomo.ConcreteModel
        """

        self.simple_transformer_model(objs=objs, uids=uids)

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
        cost_objs = (
            self.simple_chp_objs +
            self.simple_transformer_objs +
            self.simple_storage_objs +
            self.simple_transport_objs)

        self.cost_uids = {obj.uid for obj in cost_objs}

        I = {obj.uid: obj.inputs[0].uid for obj in cost_objs}
#        print("I: " + str(I))

        # create a combined list of all revenue related components
        revenue_objs = (
            self.simple_chp_objs +
            self.simple_transformer_objs)

        self.revenue_uids = {obj.uid for obj in revenue_objs}

        O = {obj.uid: obj.outputs[0].uid for obj in revenue_objs}

        # operational costs
        self.opex_var = {obj.uid: obj.opex_var for obj in cost_objs}
        self.input_costs = {obj.uid: obj.inputs[0].price
                            for obj in cost_objs}
        self.opex_fix = {obj.uid: obj.opex_fix for obj in cost_objs}
        # installed electrical/thermal capacity: {'pp_chp': 30000,...}
        self.cap_installed = {obj.uid: obj.out_max for obj in cost_objs}
        self.cap_installed = {k: sum(filter(None, v.values()))
                              for k, v in self.cap_installed.items()}

        # why do we need revenues? price=0, so we just leave this code here..
        self.output_revenues = {}
        for obj in revenue_objs:
            if isinstance(obj.outputs[0].price, (float, int)):
                price = [obj.outputs[0].price] * len(self.timesteps)
                self.output_revenues[obj.uid] = price
            else:
                self.output_revenues[obj.uid] = obj.outputs[0].price

        # get dispatch expenditure for renewable energies with dispatch
        self.dispatch_ex = {obj.uid: obj.dispatch_ex
                            for obj in self.dispatch_source_objs}

        # objective function
        def obj_rule(self):
            expr = 0

            # variable opex including ressource consumption
            expr += sum(self.w[I[e], e, t] *
                        (self.input_costs[e] + self.opex_var[e])
                        for e in self.cost_uids for t in self.timesteps)

            # fixed opex of components
            expr += sum(self.cap_installed[e] * (self.opex_fix[e])
                        for e in self.cost_uids)

            # revenues from outputs of components
            expr += - sum(self.w[e, O[e], t] * self.output_revenues[e][t]
                          for e in self.revenue_uids for t in self.timesteps)

            # dispatch costs
            if self.dispatch_source_objs:
                expr += sum(self.dispatch[e, t] * self.dispatch_ex[e]
                            for e in self.dispatch_source_uids
                            for t in self.timesteps)

            if self.slack["excess"] is True:
                expr += sum(self.excess_slack[e, t] * 3000
                            for e in self.bus_uids for t in self.timesteps)
            if self.slack["shortage"] is True:
                expr += sum(self.shortage_slack[e, t] * 3000
                            for e in self.bus_uids for t in self.timesteps)

            # add additional capacity & capex for investment models
            if(self.invest is True):
                self.capex = {obj.uid: obj.capex for obj in cost_objs}
                self.crf = {obj.uid: obj.crf for obj in cost_objs}

                expr += sum(self.add_cap[I[e], e] * self.crf[e] *
                            (self.capex[e] + self.opex_fix[e])
                            for e in self.cost_uids)
                expr += sum(self.soc_add[e] * self.crf[e] *
                            (self.capex[e] + self.opex_fix[e])
                            for e in self.simple_storage_uids)
            return(expr)
        self.objective = po.Objective(rule=obj_rule)

    def solve(self, solver='glpk', solver_io='lp', debug=False,
              results_to_objects=True, duals=False, **kwargs):
        """Method that creates the instance of the model and solves it.

        Parameters
        ----------
        self : pyomo.ConcreteModel
        solver str: solver to be used e.g. 'glpk','gurobi','cplex'
        solver_io str: str that defines the solver interaction
        (file or interface) 'lp','nl','python'
        result_to_objects boolean: Flag if results from optimization problem
        are written back to objects
        **kwargs: other arguments for the pyomo.opt.SolverFactory.solve()
        method

        Returns
        -------
        self : solved pyomo.ConcreteModel instance
        """

        from pyomo.opt import SolverFactory

        # create model instance
        instance = self.create()

        # Create a 'dual' suffix component on the instance
        # so the solver plugin will know which suffixes to collect
        if duals is True:
            # dual variables (= shadow prices)
            self.dual = po.Suffix(direction=po.Suffix.IMPORT)
            # reduced costs
            self.rc = po.Suffix(direction=po.Suffix.IMPORT)
        # write lp-file
        if(debug is True):
            instance.write('problem.lp',
                           io_options={'symbolic_solver_labels': True})
            # print instance
            # instance.pprint()
        # solve instance
        opt = SolverFactory(solver, solver_io=solver_io)
        # store results
        results = opt.solve(instance, **kwargs)
        # load results back in instance
        instance.load(results)

        # store dual variables for bus-balance constraints (el and th)
        if duals is True:
            for b in self.bus_objs:
                if b.type == "el" or b.type == "th":
                    b.results["duals"] = []
                    for t in self.timesteps:
                        b.results["duals"].append(
                            self.dual[getattr(self, "bus")[(b.uid, t)]])
#                    print(b.results["duals"])

        if results_to_objects is True:
            for entity in self.entities:
                if (isinstance(entity, cp.Transformer) or
                        isinstance(entity, cp.Source)):
                    # write outputs
                    O = [e.uid for e in entity.outputs[:]]
                    for o in O:
                        entity.results['out'][o] = []
                        for t in self.timesteps:
                            entity.results['out'][o].append(
                                self.w[entity.uid, o, t].value)

                    I = [i.uid for i in entity.inputs[:]]
                    for i in I:
                        entity.results['in'][i] = []
                        for t in self.timesteps:
                            entity.results['in'][i].append(
                                self.w[i, entity.uid, t].value)

                if isinstance(entity, cp.sources.DispatchSource):
                    entity.results['in'][entity.uid] = []
                    for t in self.timesteps:
                        entity.results['in'][entity.uid].append(
                            self.w[entity.uid,
                                   entity.outputs[0].uid, t].bounds[1])

                # write results to self.simple_sink_objs
                # (will be the value of simple sink in general)
                if isinstance(entity, cp.Sink):
                    i = entity.inputs[0].uid
                    entity.results['in'][i] = []
                    for t in self.timesteps:
                        entity.results['in'][i].append(
                            self.w[i, entity.uid, t].value)
                if isinstance(entity, cp.transformers.Storage):
                    entity.results['soc'] = []
                    for t in self.timesteps:
                        entity.results['soc'].append(
                            self.soc[entity.uid, t].value)

            if(self.invest is True):
                for entity in self.entities:
                    if isinstance(entity, cp.Transformer):
                        entity.results['add_cap_out'] = \
                            self.add_cap[entity.uid,
                                         entity.outputs[0].uid].value
                    if isinstance(entity, cp.Source):
                        entity.results['add_cap_out'] = \
                            self.add_cap[entity.uid,
                                         entity.outputs[0].uid].value
                    if isinstance(entity, cp.transformers.Storage):
                        entity.results['add_cap_soc'] = \
                            self.soc_add[entity.uid].value

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
