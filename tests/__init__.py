from nose.tools import raises

import models as model
import powerplants as plant

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