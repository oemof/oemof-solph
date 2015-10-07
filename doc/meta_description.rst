=========================================
 Meta description
=========================================

.. contents:: Table of Contents


This so called meta-description was developed to make oemof easy to use and 
develop. It describes general ideas and structures of oemof and its modules.

 

The *solph* module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The solph module of oemof allows to create and solve linear optimization 
problems. The optimization problem is build based on a energy system defined via 
oemof-entities. These entities are instances of 
oemof base classes (e. g. buses or components). For the definition of variables, 
constraints and an objective function as well as for communication with solvers 
etc. the python packages *pyomo* (_Website: http://www.pyomo.org/) is used.

Structure of solph 
------------------------------------------
At its core solph has a class called *OptimizationModel()* which is a child of 
the pyomo class *ConcreteModel()*. This class contains different methods.
An important type of methods are so called *assembler* methods. These methods 
correspond exactly to one oemof-class. For example the *transfomer.Simple()* 
class of oemof will have a associated method called 
simple_transformer_assembler(). This method exctracts information from oemof 
objects and groups all necessary constraints to model a simple transformer. 

Constructor
************
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
******************
The *assembler* methods can be specified in two different ways. Firstly, functions 
from the solph-library called *linear_constraints.py* can be used to add 
constraints to the *assembler*. Secondly, *assembler* methods can use other 
*assembler* methods and then be extended by functions from the library. 
The same holds for the objective *assembler*. The objective function uses 
pre-defined objectives from the solph-library called *linear_objectives.py*.

If necessary, the two libraries used be *assemlber* methods can be extended 
and used in methods of *OptimizationModel()* afterwards.  


Solve and other
****************
Moreover, the *OptimizationModel()* class contains methods for setting options 
and solving the optimization model. 


Postprocessing of results
------------------------------------------
To extract values from the optimization problem variables their exist a
postprossing module containing different functions. 
Results can be written back to the oemof-objects or
to excel-spreadsheets. 
