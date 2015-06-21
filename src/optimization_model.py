
import pyomo.environ as po


def opt_model(entities, edges, timesteps=[t for t in range(10)]):
  """
  :param entities: dictionary containing all entities grouped by classtypes
  """

  busses = entities['busses']
  s_transformers = entities['s_transformers']
  s_chps = entities['s_chps']

  # create pyomo model instance
  m = po.ConcreteModel()

  # create pyomo sets
  # timesteps
  m.timesteps = timesteps
  # entities
  m.busses = [b.uid for b in busses]
  m.s_transformers = [t.uid for t in s_transformers]
  m.s_chps = [t.uid for t in s_chps]
  m.edges = po.Set(dimen=2, initialize=edges)
  # create variable for edges all >= 0 ?

  m.w_max = 100
  def w_max_rule(m, i, j, t):
    return(0, m.w_max)
  m.w = po.Var(m.edges, m.timesteps, bounds=w_max_rule,
               within=po.NonNegativeReals)

  ## bus balance forall b in busses
  def bus_rule(m, e, t):
    expr = 0
    expr += -sum(m.w[(i,j),t] for (i,j) in m.edges if i==e)
    expr += +sum(m.w[(i,j),t] for (i,j) in m.edges if j==e)
    return(expr, 0)
  m.bus_constr = po.Constraint(m.busses, m.timesteps, rule=bus_rule)


  # simple transformer model containing the constraints for simple transformers
  def simple_transformer_model(m):
    """
    :param m: pyomo model instance
    """
    # temp set with input uids for every simple chp e in s_transformers
    I ={t.uid:t.inputs[0].uid for t in s_transformers}
    # set with output uids for every simple transformer e in s_transformers
    O = {t.uid:t.outputs[0].uid for t in s_transformers}
    eta = {t.uid:t.eta for t in s_transformers}
    def eta_rule(m, e, t):
      expr = 0
      expr += m.w[I[e], e, t] * eta[e]
      expr += - m.w[e, O[e], t]
      return(expr,0)
    m.s_transformer_eta_constr = po.Constraint(m.s_transformers, m.timesteps,
                                               rule=eta_rule)

  # simple chp model containing the constraints for simple chps
  def simple_chp_model(m):
    """
    """
    # temp set with input uids for every simple chp e in s_chps
    I = {t.uid:t.inputs[0].uid for t in s_chps}
    # set with output uids for every simple chp e in s_chps
    O = {t.uid : [o.uid for o in t.outputs[:]] for t in s_chps}
    # constraint for transformer energy balance
    def eta_rule(m, e, t):
      expr = 0
      expr += m.w[I[e], e, t]
      expr += -sum(m.w[e, o, t] for o in O[e]) / 0.8
      return(expr,0)
    m.s_chp_eta_constr = po.Constraint(m.s_chps, m.timesteps, rule=eta_rule)

    # additional constraint for power to heat ratio of simple chp components
    def power_to_heat_rule(m, e, t):
      expr = 0
      expr += m.w[e, O[e][0], t]
      expr += -m.w[e, O[e][1], t] * 0.6
      return(expr,0)
    m.s_chp_pth_constr = po.Constraint(m.s_chps, m.timesteps,
                                       rule=power_to_heat_rule)

  def objective(m):

    def obj_rule(m):
      expr = 0
      expr += sum(m.w[i,j,t] for (i,j) in m.edges for t in m.timesteps)
      return(expr)
    m.objective = po.Objective(rule=obj_rule)

  # "call" the models to add the constraints to opt-problem
  simple_chp_model(m)
  simple_transformer_model(m)
  objective(m)

  return(m)

def solve_opt_model(model, solver='glpk',
                      options={'stream':False}, debug=False):
 """
 :param model: pyomo concreteModel() instance
 :param str solver: solver specification as string 'glpk','gurobi','clpex' ...
 """
 from pyomo.opt import SolverFactory
 # create model instance
 instance = model.create()
 # solve instance
 if(debug==True):
   instance.write('problem.lp',
                  io_options={'symbolic_solver_labels':True})

 opt = SolverFactory(solver, solver_io='lp')
 # store results
 results = opt.solve(instance, tee=options['stream'])
 # load results back in instance
 instance.load(results)

 return(instance)


if __name__ == "__main__":
  # create energy system components
  import components as cp
  bus1 = cp.Bus(uid="b1", type="coal")
  bus2 = cp.Bus(uid="b2", type="elec")
  bus3  = cp.Bus(uid="b3", type="th")
  t1 = cp.SimpleTransformer(uid="t1",inputs=[bus1], outputs=[bus2], eta=0.5)
  t2 = cp.SimpleTransformer(uid="t2",inputs=[bus1], outputs=[bus2], eta=0.4)
  t3 = cp.Transformer(uid="t3",inputs=[bus1], outputs=[bus2,bus3])
  t4 = cp.Transformer(uid="t4",inputs=[bus1], outputs=[bus2,bus3])
  t5 = cp.SimpleTransformer(uid="Boiler",inputs=[bus1],outputs=[bus3], eta=0.9)
  # store entities of same class in lists

  entities = {'busses':[bus1, bus2, bus3],
              's_transformers':[t1, t2, t5],
              's_chps':[t3, t4]}

  # should be calculated automatically of course
  edges = [('b1','t1'),('b1','t2'),('b1','t3'), ('t1','b2'),('t2','b2'),
           ('t3','b2'),('t3','b3'),('b2','s1'),('b1','t4'),('t4','b2'),
           ('t4','b3'),('b1','Boiler'),('Boiler','b3')]

  # create optimization model
  from time import time

  print('Building model...')
  t0 = time()
  om = opt_model(entities=entities, edges=edges)

  t1= time()
  building_time = t1 - t0
  print('Building Time:', building_time)

  print('Solving model...')
  # solve model
  t0 = time()
  instance = solve_opt_model(model=om, solver='glpk',
                             options={'stream':True}, debug=True)
  t1 = time()
  solving_time = t1 - t0
  print('Solving time:', solving_time)

  #for idx in instance.w:
  #  print('Edge:'+str(idx), ', weight:'+str(instance.w[idx].value))