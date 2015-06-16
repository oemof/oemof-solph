"""
Contains the class hierarchy used to model energy systems. An energy
system is modelled as a graph/network of entities with very specific
constraints on which types of entities are allowed to be connected.

TODO: Adhere to PEP 0257 by listing the exported classes with a short
      summary.

"""
class Entity:
  """
  The most abstract type of vertex in an energy system graph. Since each
  entity in an energy system has to be uniquely identifiable and
  connected (either via input or via output) to at least one other
  entity, these properties are collected here so that they are shared
  with descendant classes.
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

class Component(Entity):
  """
  Components are one specific type of entity comprising an energy system
  graph, the other being Buses. The important thing is, that connections
  in an energy system graph are only allowed between Buses and
  Components and not between Entities of equal subtypes. This class
  exists only to facilitate this distinction and is empty otherwise.

  """
  pass

class Transformer(Component):
 """
 A Transformer is a specific type of Component which transforms
 (possibly m) inputs into (possibly n) outputs. As such neither its list
 of inputs, nor its list of outputs are allowed to be empty.
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
  """
  A Sink is special Component which only consumes some source commodity.
  Therefore its list of outputs has to be either None or empty (i.e. logically
  False).
  """
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)
    if self.outputs:
      raise ArgumentError("Sink must not have outputs.\n" +
                          "Got: {0!r}".format(outputs))


class Source(Component):
  """
  The opposite of a Sink, i.e. a Component which only produces and as a
  consequence has no input.
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
  The other type of entity in an energy system graph (besides
  Components). A Bus acts as a kind of mediator between producers and
  consumers of a commodity of the same kind. As such it has a type,
  which signifies what kind of commodity goes through the bus.
  """
  def __init__(self, **kwargs):
    """
    :param type: the type of the bus. Can be a meaningful value like e.g.
                 "electricity" but may be anything that can be tested for
                 equality and is distinct for incompatible Buses.
    """
    super().__init__(**kwargs)
    self.type = kwargs["type"]

class Transport(Component):
  """
  A Transport is a simple connection transporting a commodity from one
  Bus to a different one. It is different from a Transformer in that it
  may not change the type of commodity being transported. But since the
  transfer can still change things about the commodity other than the
  type (loss, gain, time delay, etc.) this class exists to encapsulate
  such changes.
  """
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
