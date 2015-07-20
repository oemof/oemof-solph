from nose.tools import ok_, raises

import network
import network.entities as entities
import network.entities.components as components
import network.entities.components.sinks as sinks
import network.entities.components.sources as sources
import network.entities.components.transformers as transformers
import network.entities.components.transports as transports

import models as model
import powerplants as plant

class Structure_Tests:
    def test_inheritance_hierarchy(self):
        ok_(issubclass(entities.Bus,       network.Entity))
        ok_(issubclass(entities.Component, network.Entity))
        ok_(issubclass(components.Sink,        entities.Component))
        ok_(issubclass(components.Source,      entities.Component))
        ok_(issubclass(components.Transformer, entities.Component))
        ok_(issubclass(components.Transport,   entities.Component))
        ok_(issubclass(sinks.Simple, components.Sink))
        ok_(issubclass(sources.Renewable,        components.Source))
        ok_(issubclass(sources.Commodity,        components.Source))
        ok_(issubclass(transformers.Simple,        components.Transformer))
        ok_(issubclass(transformers.CHP,           components.Transformer))
        ok_(issubclass(transformers.ExtractionCHP, components.Transformer))
        ok_(issubclass(transformers.Storage,       components.Transformer))
        ok_(issubclass(transports.Simple, components.Transport))


class ModelsPowerplantsInteraction_Tests:

  @raises(AttributeError)
  def test_required(self):
    plant.Photovoltaic(nominal_power = 0,
                       model = model.Photovoltaic(["missing"]))

class Component_Test:
  """
  test to check if instance variables are overwritten in child classes
  """
  pass
