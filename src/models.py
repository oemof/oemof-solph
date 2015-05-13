# -*- coding: utf-8 -*-
"""
Created on Wed May 13 08:43:54 2015

@author: dozeumwic
"""

from functools import reduce
from random import random

class Photovoltaic:
  def __init__(self, required):
    self.required = required

  def feedin(self, **kwargs):
    p = reduce(lambda x, y: x * y,
               [kwargs[k] for k in kwargs
                          if isinstance(kwargs[k], (int, float))
                          if 0 != kwargs[k]])
    for _ in range(10): yield random()*p

class CM2:
    def __init__(self, required = ["nominal_power", "steps"]):
      self.required = required
    def feedin(self, **ks): return [ks["nominal_power"]*0.9] * ks["steps"]