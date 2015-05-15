# -*- coding: utf-8 -*-
"""
Created on Wed May 13 08:43:54 2015

@author: dozeumwic
"""

from functools import reduce
from random import random
import pvlib

class Photovoltaic:
  def __init__(self, required):
    self.required = required

  def feedin(self, **kwargs):
      
   module_data = (pvlib.pvsystem.retrieve_sam('SandiaMod')
            [kwargs['module_name']])
   return [module_data]
        



class ConstantModell:
    def __init__(self, required = ["nominal_power", "steps"]):
      self.required = required
    def feedin(self, **ks): return [ks["nominal_power"]*0.9] * ks["steps"]