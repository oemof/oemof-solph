.. _oemof_solph_dev_label:

~~~~~~~~~~~~~~~~
oemof-solph-dev
~~~~~~~~~~~~~~~


.. contents::
    :depth: 2
    :local:
    :backlinks: top


The solph Model
--------------------


The main class is the `oemof.solph.Model()` class which is a subclass of the
`pyomo.ConcreteModel()`.  The solph Model object is instantiated with an
`oemof.solph.EnergSystem` object which holds all required information. These are:

* Components, Buses and Flow objects connecting both
* The `timeindex` argument to create a set for the temporal resolution
* So called groupings. The grouping provides a mapping between objects and
 their expression in the mathematical model.

Construction
^^^^^^^^^^^^^^^^^^^^^^^
Inside the constructor the following four methods are called in a sequence
(in this case order matters!). The mathematical expressions are implemented
based on the pyomo package. Pyomo uses so called `blocks` to organize their
data model. Therefore we adapted this terminology:

`self._add_parent_block_sets()`

This methods adds all Sets to the Top-level block which is the model. For example
the Set of all Nodes (NODES), flows (FLOWS) or the set of timesteps (TIMESTEPS)
derived from passed argument `timeindex` are set on this level. For the
`oemof.solph.Model()` no variables, constraints or objective function expressions
are added on this level.

`self._add_parent_block_variables()`

Here all Variables for the Top-level are added. In the case of the
oemof.solph.Model() the only variable created is the ‘flow[i,o,t]’ variable
indexed by it’s input, output and timestep. The method takes care of setting
the correct bounds for this variable.

`self._add_child_blocks()`

This method is not as straightforward as the ones above. Basically what we do
here we run through all so called `constraint_groups`. You can think of these
groups as set of constraints. The member of a constraint group are objects
(Components, Buses, Flows) for which the constraints should be build.
The term constraint_group may be misleading, as for these groups we also add
variables and objective expression terms. However, the important thing is that
we create a pyomo block for each constraint group under the name of the block
 class. We require every block class inside solph to have a `_create` method,
 which basically adds everything to the block object once called.

We also organise the objective expressions inside these blocks. Therefore we
also require every block class to have a `_objective_expression` method. This
create pyomo expressions that are the return value of the method. It also adds
these expressions to the block object as an attribute.

`self._add_objective()`

Finally, when this method is called, we run through all blocks of a model. If
we find a block that has the method objective expression, this one will be called
and the expression will be added to the total objective expression.


 .. code-block:: python

   expr = 0

  for block in self.component_data_objects():
       if hasattr(block, '_objective_expression'):
           expr += block._objective_expression()

   self.objective = po.Objective(sense=sense, expr=expr)

We store the objective expression under their `objective` attribute. If you want
to add an other objective you can use the pyomo functionalities, i.e.
`model.del_component('objective')`  to delete the objective and just add your
own one.
