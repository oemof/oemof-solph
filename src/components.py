class Entity:
  """
  """
  def __init__(self, inputs = [], outputs = [], **kwargs):
    """
    :param uid: unique component identifier
    :param inputs: list of Entities acting as input to this Entity.
    :param outputs: list of Entities acting as output from this Enity.
    """
    self.uid = kwargs["uid"]
    self.inputs = inputs
    self.outputs = outputs
    for e_in in self.inputs:
      if self not in e_in.outputs: e_in.outputs.append(self)
    for e_out in self.outputs:
      if self not in e_out.inputs: e_out.inputs.append(self)

  def __str__(self): return "<{0} #{1}>".format(type(self), self.uid)

class Component(Entity): pass

class Transformer(Component):
 """
 """
 def __init__(self, **kwargs):
  """
  """
  super().__init__(**kwargs)
    if not self.inputs:
      raise ArgumentError("Transformer must have at least one input.\n" +
                          "Got: {0!r}".format(inputs))
    if not self.outputs:
      raise ArgumentError("Transformer must have at least one output.\n" +
                          "Got: {0!r}".format(outputs))

class Sink(Component):
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)
    if self.outputs:
      raise ArgumentError("Sink must not have outputs.\n" +
                          "Got: {0!r}".format(outputs))


class Source(Component):
  """
  """
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)
    if self.inputs:
      raise ArgumentError("Sink must not have inputs.\n" +
                          "Got: {0!r}".format(inputs))

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
      raise ArgumentError("Transport must have exactly one input.\n" +
                          "Got: {0!r}".format(inputs))

    if len(self.outputs) != 1:
      raise ArgumentError("Transport must have exactly one output.\n" +
                          "Got: {0!r}".format(outputs))




if __name__ == "__main__":
  my_bus1 = Bus(uid="b1", type="electricity")
  my_bus2 = Bus(uid="b2", type="electricity")
  my_trans = Transformer(uid="t1", inputs=[my_bus1], outputs=[my_bus2])
  my_connections = Transport(uid="c1", inputs=[my_bus1], outputs=[my_bus2])
  print(my_trans.uid)
  print(my_trans.inputs[0])
  print(my_bus1.outputs[0])
