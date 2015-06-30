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
  pass


class Transformer(Component):
  """
  """
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

    self.in_max = kwargs.get('in_max', None)
    self.out_max = kwargs.get('out_max', None)
    self.capex = kwargs.get('capex', 0)
    self.opex_fix = kwargs.get('opex_fix', None)
    self.opex_var = kwargs.get('opex_var', 0)
    self.co2_var = kwargs.get('co2_var', None)

    self.opt_param = kwargs.get('opt_param', None)
    self.results = kwargs.get('results', {})

class SimpleTransformer(Transformer):
  """
  Simple Transformers always have a simple input output relation with a
  constant efficiency
  """
  def __init__(self,**kwargs):
    """
    :param eta: eta as constant efficiency for simple transformer
    """
    super().__init__(**kwargs)
    self.eta = kwargs.get('eta', None)

    if(self.in_max is None and self.out_max is not None):
      self.in_max = self.out_max / self.eta
    if(self.out_max is None and self.in_max is not None):
      self.out_max = self.in_max * self.eta


class SimpleCombinedHeatPower(Transformer):
  """
  SimpleCombinedHeatPower always have a simple input output relation with a
  constant efficiency
  """
  def __init__(self,**kwargs):
    """
    :param eta: eta as constant efficiency for simple transformer
    """
    super().__init__(**kwargs)
    self.eta = kwargs.get('eta', [])


class SimpleStorage(Transformer):
  """
  """
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
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)
    if self.outputs:
      raise ValueError("Sink must not have outputs.\n" +
                       "Got: {0!r}".format([str(x) for x in self.outputs]))
    self.val = kwargs['val']

class Source(Component):
  """
  """
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)
    if self.inputs:
      raise ValueError("Source must not have inputs.\n" +
                       "Got: {0!r}".format([str(x) for x in self.inputs]))
    self.results = kwargs.get('results', {})

class RenewableSource(Source):
  """
  """
  def __init__(self, **kwargs):
    """
    :param boolean dispatch: Flag if RenewableSource is dispatchable or not
    """
    super().__init__(**kwargs)
    self.val = kwargs.get('val', None)
    self.out_max = kwargs.get('out_max', 0)
    self.dispatch = kwargs.get('dispatch', False)
    self.dispatch_ex = kwargs.get('dispatch_ex', 0)

class Commodity(Source):
  """
  """
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)
    self.yearly_limit = kwargs.get('yearly_limit', float('+inf'))
    self.emmision_factor = kwargs.get('emmission_factor', 0)

class Bus(Entity):
  """
  """
  def __init__(self, **kwargs):
    """
    :param type: bus type could be electricity...BLARBLAR
    """
    super().__init__(**kwargs)
    self.type = kwargs["type"]

class Transport(Component):
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
  power = Bus(uid="Electricity", type="electricity")
  st = SimpleTransformer(uid="st1",inputs=[coal],outputs=[power], eta=0.4)
  heat = Bus(uid="Thermal", type="thermal")
  heatpump = Transformer(uid="Heatpump", inputs=[power],
                         outputs=[heat])
  chp = Transformer(uid="CHP", inputs=[coal], outputs=[heat, power])
  wind = Source(uid="The only wind turbine on the planet.", outputs=[power])
  city = Sink(uid="Neverwhere", inputs=[heat])

  import networkx as nx

  g = nx.DiGraph()
  es = [coal, power, heat, heatpump, chp, wind, city]
  buses = [e for e in es if isinstance(e, Bus)]
  components = [e for e in es if isinstance(e, Component)]
  g.add_nodes_from(es)
  for e in es:
    for e_in in e.inputs:
      a, b = e_in, e
      g.add_edge(a, b)
  graph_pos=nx.spectral_layout(g)
  nx.draw_networkx_nodes(g, graph_pos, buses, node_shape="o", node_color="r",
                         node_size = 900)
  nx.draw_networkx_nodes(g, graph_pos, components, node_shape="s",
                         node_color="b", node_size=300)
  nx.draw_networkx_edges(g, graph_pos)
  nx.draw_networkx_labels(g, graph_pos)
  # or simply nx.draw(g) but then without different node shapes etc
