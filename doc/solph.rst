~~~~~~~~~~~
oemof-solph
~~~~~~~~~~~

Structure of solph
------------------------------------------
At its core solph has a class called *OptimizationModel()* which is a child of
the pyomo class *ConcreteModel()*. This class contains different methods.
An important type of methods are so called *assembler* methods. These methods
correspond exactly to one oemof-base-class. For example the
*transfomer.Simple()* class of oemof will have a associated method called
simple_transformer_assembler(). This method groups all necessary constraints
to model a simple transformer. The constraints expressions are defined in
extra module (*linear_constraints.py*, *linear_mixed_integer_constraints.py*).
All necessary constraints related with variables are defined in *variables.py*.


Constructor
^^^^^^^^^^^^

The whole pyomo model is build when instantiating the optimization model.
This is why the constructor of the  *OptimizationModel()* class plays an
important role.

The general procedure is as basically follows:

1. Set some options
2. Create all necessary optimization variables
3. Loop trough all entities and group existing objects by class
4. Call the associated *assembler* method for every **group** of objects.
   This builds constraints to model components.
5. Build the bus constraints with bus *assembler*.
6. Build objective *assembler*.


Assembler methods
^^^^^^^^^^^^^^^^^^^^^^^^

The *assembler* methods can be specified in two different ways. Firstly, functions
from the solph-library called *linear_constraints.py* can be used to add
constraints to the *assembler*. Secondly, *assembler* methods can use other
*assembler* methods and then be extended by functions from the library.
The same holds for the objective *assembler*. The objective function uses
pre-defined objectives from the solph-library called *objectives.py*. These
pre-defined objectives are build by the use of objective expressions defined
in *objective_expressions*. Different objectives for optimization models
can be selected by setting the option *objective_types* inside the
*objective_assembler* method.


If necessary, the two libraries used be *assemlber* methods can be extended
and used in methods of *OptimizationModel()* afterwards.

Solve and other
^^^^^^^^^^^^^^^^^^^^^^^^

Moreover, the *OptimizationModel()* class contains a method for solving
the optimization model.


Postprocessing of results
----------------------------
To extract values from the optimization problem variables their exist a
postprossing module containing different functions.
Results can be written back to the oemof-objects or
to excel-spreadsheets.

