# -*- coding: utf-8 -*-
"""
This module is designed to hold custom components with their classes and
associated individual constraints (blocks) as well as their groupings.
Therefore this module holds the class definition and the block directly
located by each other.

To add a component you need to add:

* A class that will be used by the user
* A class that inherits from pyomo SimpleBlock that holds the constraints,
  variables etc.
* A few lines to the grouping function in the module that makes sure that
  the block is actually added to the model.
"""
