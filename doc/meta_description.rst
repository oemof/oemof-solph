=========================================
 Meta description
=========================================

This so called meta-description was developed to make oemof easy to use and 
develop. It describes general ideas and structures of oemof and its modules.


The idea of an open framework
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Models in energy system analysis often do not disclose source code and data or only have a sparse documentation.
This lack of transparency slows down the scientific discussion about the model fitness in terms of a specific application.
Moreover, models are often tailor-made and do not allow and easy adaption to other requirements or an integration of new approaches.

The Open Energy Modelling Framework (oemof) addresses this issue by introducing an open source modeling framework for 
energy systems analysis including a detailed documentation structure.
This transparent approach allows scientific discourse about the underlying models and thus improves the model quality.
Additionally, a modular design approach allows a flexible adaption for a variety of applications.

The framework can be used to model arbitrary energy systems.
Applications range from complex single-region combined heat and power models to multi-regional models in the european power sector.
Models can be optimised with respect to different targets such as emissions or costs. Both can be computed in appropriate time.
Moreover, only single parts of the framework can be used for simple tasks such as wind or solar feedin calculation for a specific site.

Framework structure
------------------------------------------

Generic oemof energy systems consist of entities and represent a bipartite directed graph.

*Entities* can be subdivided into busses or components.
A *Bus* has a certain type (e.g. gas) and can be connected to other busses (e.g. electricity or thermal) via components.
A *Component* in turn represents a (possible) in- or outflow into a bus.

The basic components are:

* *Transport* represents a directed connection between two busses with a given capacity
* *Source*  represents an energy flow into a single bus
* *Sink*  represents an energy flow out of a single bus
* *Transformer*  represents an energy flow from one bus to another


Example 
------------------------------------------

An example of a simple energy system shows the usage of the entities for real world representations. 

*Region1:*

components: wind turbine (wt1), electrical demand (dm1), gas turbine (gt1), cable to region2 (cb1)
busses: gas pipeline (r1_gas), electrical grid (r1_el)

*Region2:*

components: coal plant (cp2), chp plant (chp2), electrical demand (dm2), cable to region2 (cb2), p2g-facility (ptg2)
busses: electrical grid (r2_el), local heat network (r2_th), coal reservoir (r2_coal), gas pipeline (r2_gas)


In oemof this would look as follows::

                input/output  r1_gas   r1_el   r2_el   r2_th   r2_coal   r2_gas
                     |          |        |       |       |       |         |
                     |          |        |       |       |       |         |
      wt1(Source)    |------------------>|       |       |       |         |
                     |          |        |       |       |       |         |
                     |          |        |       |       |       |         |
        dm1(Sink)    |<------------------|       |       |       |         |
                     |          |        |       |       |       |         |
                     |          |        |       |       |       |         |
 gt1(Transformer)    |<---------|        |       |       |       |         |
                     |------------------>|       |       |       |         |
                     |          |        |       |       |       |         |
                     |          |        |       |       |       |         |
   cb1(Transport)    |          |        |------>|       |       |         |
                     |          |        |       |       |       |         |
                     |          |        |       |       |       |         |
 cp2(Transformer)    |<------------------------------------------|         |
                     |-------------------------->|       |       |         |
                     |          |        |       |       |       |         |
                     |          |        |       |       |       |         |
 chp2(Transformer)   |<----------------------------------------------------|
                     |-------------------------->|       |       |         |
                     |---------------------------------->|       |         |
                     |          |        |       |       |       |         |
                     |          |        |       |       |       |         |
        dm2(Sink)    |<--------------------------|       |       |         |
                     |          |        |       |       |       |         |
                     |          |        |       |       |       |         |
   cb2(Transport)    |          |        |<------|       |       |         |
                     |          |        |       |       |       |         |
                     |          |        |       |       |       |         |
 ptg2(Transformer)   |<--------------------------|       |       |         |
                     |---------------------------------------------------->|


Classes and modules
------------------------------------------

All energy system entities (busses and components) are represented in a class hierarchy that can be easily extended.
These classes form the basis for so so-called framework modules, that operate on top of them.

The framework consists of various modules that provide different functionalities.
Currently, there are three modules but in future further extensions will be made.

oemof's current modules:

* *feedinlib* generates wind and solar feedin timeseries for different plants and geographical locations
* *demandlib* generates electrical and thermal demands for different objects
* *solph* creates and solves a (mixed-integer) linear optimization problem for a given energy system

All modules may interact with each other but can also be used stand-alone.
A detailed description can be found in the following sections.



oemof *base classes*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




The *feedinlib* module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The modelling library feedinlib is currently in a development stage.
Using feedinlib energy production timeseries of several energy plants can be created.
Focus is on fluctuating renewable energies like wind energy and photovoltaics.
The output timeseries can be input for the components of the energy system and therefore incorporated in the optimization within the modelling library solph.
However, a stand-alone usage of feedinlib is also intended. 

Clone or fork the 'feedinlib' from github and use it within your project. Don’t forget to play back your fixes and improvements. We are pleased to get your feedback.




The *demandlib* module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Description of demandlib.




The *solph* module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The solph module of oemof allows to create and solve linear optimization 
problems. The optimization problem is build based on a energy system defined via 
oemof-entities. These entities are instances of 
oemof base classes (e. g. buses or components). For the definition of variables, 
constraints and an objective function as well as for communication with solvers 
etc. the python packages `Pyomo <http://www.pyomo.org/>`_ is used.

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

