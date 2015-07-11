import numpy as np


class Entity:
  """
  """
  def __init__(self, **kwargs):
    #TODO: add default argument values to docstrings (if it's possible).
    """
    :param uid: unique component identifier
    :param inputs: list of Entities acting as input to this Entity.
    :param outputs: list of Entities acting as output from this Enity.
    """
    self.uid = kwargs["uid"]
    self.inputs = kwargs.get("inputs", [])
    self.outputs = kwargs.get("outputs", [])
    for e_in in self.inputs:
      if self not in e_in.outputs: e_in.outputs.append(self)
    for e_out in self.outputs:
      if self not in e_out.inputs: e_out.inputs.append(self)

  def __str__(self): return "<{0} #{1}>".format(type(self).__name__, self.uid)


class Component(Entity):
  """
  """
  __lower_name__ = "component"
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)

    self.in_max = kwargs.get('in_max', None)
    self.out_max = kwargs.get('out_max', None)
    self.lifetime = kwargs.get('lifetime', 20)
    self.wacc = kwargs.get('wacc', 0.05)
    self.capex = kwargs.get('capex', 0)
    self.opex_fix = kwargs.get('opex_fix', None)
    self.opex_var = kwargs.get('opex_var', 0)
    self.co2_var = kwargs.get('co2_var', None)
    self.param = kwargs.get('param', None)
    self.results = kwargs.get('results', {})


class Transformer(Component):
  """
  """
  __lower_name__ = "transformer"
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)
    if not self.inputs:
      raise ValueError("Transformer must have at least one input.\n" +
                       "Got: {0!r}".format([str(x) for x in self.inputs]))
    if not self.outputs:
      raise ValueError("Transformer must have at least one output.\n" +
                       "Got: {0!r}".format([str(x) for x in self.outputs]))


  def emissions(self):
    self.emissions =  [o * self.co2_var for o in self.results['Input']]

class SimpleTransformer(Transformer):
  """
  Simple Transformers always have a simple input output relation with a
  constant efficiency
  """
  __lower_name__ = 'simple_transformer'
  def __init__(self,**kwargs):
    """
    :param eta: eta as constant efficiency for simple transformer
    """
    super().__init__(**kwargs)
    self.eta = kwargs.get('eta', None)

    if(self.param['in_max'][self.inputs[0].uid] is None and
       self.param['out_max'][self.outputs[0].uid] is not None):
      self.param['in_max'][self.inputs[0].uid] = \
          self.param['out_max'][self.outputs[0].uid] / self.param['eta'][0]


class SimpleCHP(Transformer):
  """
  SimpleCombinedHeatPower always have a simple input output relation with a
  constant efficiency
  """
  __lower_name__ = "simple_chp"
  def __init__(self,**kwargs):
    """
    :param eta: eta as constant efficiency for simple transformer
    """
    super().__init__(**kwargs)
    self.eta = kwargs.get('eta', {'th': None, 'el': None})


class SimpleExtractionCHP(Transformer):
  """
  SimpleExtractionCHP uses half-space representation to model the P-Q-relation
  # points in p/q diagramm
  *0=(100,0) --
               -- *2

   *1=(50,0) --
                -- *3
  """
  __lower_name__ = "simple_extraction_chp"
  def __init__(self, **kwargs):
    """

    """
    super().__init__(**kwargs)
    self.eta_el_max = kwargs.get('eta_el_max', 0.3)
    self.eta_el_min = kwargs.get('eta_el_min', 0.25)
    self.eta_total = kwargs.get('eta_total', 0.8)
    self.out_max = kwargs.get('out_max', 100)
    self.out_min = kwargs.get('out_min', 50)
    self.beta = kwargs.get('beta', [0.15, 0.15])

    p = [self.out_max, self.out_min, None, None]
    q = [0, 0, None, None]
    eta_el = [self.eta_el_max, self.eta_el_min]  # [0.3, 0.25, None, None]
    beta = self.beta
    eta = self.eta_total

    # max / min fuel consumption
    h = [p[0]/eta_el[0], p[1]/eta_el[1]]

    q[2] = (h[0]*eta - p[0]) / (1-beta[0])
    q[3] = (h[1]*eta - p[1]) / (1-beta[1])

    # elctrical power in point 2,3  with: P = P0 - S * Q
    p[2] = p[0] - beta[0] * q[2]
    p[3] = p[1] - beta[1] * q[3]

    # determine coefficients for constraint
    a = np.array([[1, q[2]], [1, q[3]]])
    b = np.array([p[2], p[3]])
    self.c = np.linalg.solve(a, b)

    # determine coeffcients for fuel consumption
    a = np.array([[1, p[0], 0], [1, p[1], 0], [1, p[2], q[2]]])
    b = np.array([h[0], h[1], h[0]])
    self.k = np.linalg.solve(a, b)
    self.p = p

class SimpleStorage(Transformer):
  """
  """
  __lower_name__ = "simple_storage"
  def __init__(self,**kwargs):
    """
    :param soc_max: maximal sate of charge
    """
    super().__init__(**kwargs)

    self.soc_max = kwargs.get('soc_max', None)
    self.soc_min = kwargs.get('soc_min', None)
    self.eta_in = kwargs.get('eta_in', 1)
    self.eta_out = kwargs.get('eta_out', 1)
    self.cap_loss = kwargs.get('cap_loss', 0)


class Sink(Component):
  """
  """
  __lower_name__ = "sink"
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)
    if self.outputs:
      raise ValueError("Sink must not have outputs.\n" +
                       "Got: {0!r}".format([str(x) for x in self.outputs]))

class SimpleSink(Sink):
  """
  """
  __lower_name__ = "simple_sink"
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)
    self.val = kwargs['val']


class Source(Component):
  """
  """
  __lower_name__ = "source"
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)
    if self.inputs:
      raise ValueError("Source must not have inputs.\n" +
                       "Got: {0!r}".format([str(x) for x in self.inputs]))

class RenewableSource(Source):
  """
  """
  __lower_name__ = "renewable_source"
  def __init__(self, **kwargs):
    """
    :param boolean dispatch: Flag if RenewableSource is dispatchable or not
    """
    super().__init__(**kwargs)
    self.val = kwargs.get('val', None)
    self.dispatch = kwargs.get('dispatch', False)
    self.dispatch_ex = kwargs.get('dispatch_ex', 0)

class Commodity(Source):
  """
  """
  __lower_name__ = "commodity"
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)
    self.yearly_limit = kwargs.get('yearly_limit', float('+inf'))
    self.emmision_factor = kwargs.get('emmission_factor', 0)

  def emissions(self):
      self.emissions = [o * self.emmision_factor
                        for o in self.results['Output'][self.outputs[0].uid]]

class Bus(Entity):
  """
  """
  __lower_name__ = "bus"
  def __init__(self, **kwargs):
    """
    :param type: bus type could be electricity...BLARBLAR
    """
    super().__init__(**kwargs)
    self.type = kwargs["type"]

class Transport(Component):
  """
  """
  __lower_name__ = "transport"
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)
    if len(self.inputs) != 1:
      raise ValueError("Transport must have exactly one input.\n" +
                       "Got: {0!r}".format([str(x) for x in self.inputs]))

    if len(self.outputs) != 1:
      raise ValueError("Transport must have exactly one output.\n" +
                       "Got: {0!r}".format([str(x) for x in self.outputs]))


class SimpleTransport(Transport):
  """
  Simple Transport connects two busses with a constant efficiency
  """
  __lower_name__ = "simple_transport"
  def __init__(self,**kwargs):
    """
    :param eta: eta as constant efficiency for simple transport
    """
    super().__init__(**kwargs)
    self.eta = kwargs.get('eta', None)

    if(self.in_max is None and self.out_max is not None):
      self.in_max = self.out_max / self.eta
    if(self.out_max is None and self.in_max is not None):
      self.out_max = self.in_max * self.eta

if __name__ == "__main__":

  #TODO: This example is missing a Transport. (Needs more escalation error.)
  coal = Bus(uid="Coal", type="coal")
  power1 = Bus(uid="Electricity1", type="electricity")
  power2 = Bus(uid="Electricity1", type="electricity")
  st = SimpleTransformer(uid="st1",inputs=[coal],outputs=[power], eta=0.4)
  heat = Bus(uid="Thermal", type="thermal")
  heatpump = Transformer(uid="Heatpump", inputs=[power],
                         outputs=[heat])
  chp = Transformer(uid="CHP", inputs=[coal], outputs=[heat, power])
  wind = Source(uid="The only wind turbine on the planet.", outputs=[power])
  city = Sink(uid="Neverwhere", val=5)
#  cable = SimpleTransport(uid="NordLink", inputs=[power1], outputs=[power2],
#                          in_max=700, out_max=630, eta=0.9)
#  print(vars(cable))

#  import networkx as nx
#
#  g = nx.DiGraph()
#  es = [coal, power, heat, heatpump, chp, wind, city]
#  buses = [e for e in es if isinstance(e, Bus)]
#  components = [e for e in es if isinstance(e, Component)]
#  g.add_nodes_from(es)
#  for e in es:
#    for e_in in e.inputs:
#      a, b = e_in, e
#      g.add_edge(a, b)
#  graph_pos=nx.spectral_layout(g)
#  nx.draw_networkx_nodes(g, graph_pos, buses, node_shape="o", node_color="r",
#                         node_size = 900)
#  nx.draw_networkx_nodes(g, graph_pos, components, node_shape="s",
#                         node_color="b", node_size=300)
#  nx.draw_networkx_edges(g, graph_pos)
#  nx.draw_networkx_labels(g, graph_pos)
#  # or simply nx.draw(g) but then without different node shapes etc
