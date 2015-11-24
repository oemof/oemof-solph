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
A *Bus* has a certain type (e.g. gas) and can be connected to other busses
(e.g. electricity or thermal) via components.
A *Component* in turn represents a (possible) in- or outflow into a bus.

The basic components are:

* *Transport* represents a directed connection between two busses with a given capacity
* *Source*  represents an energy flow into a single bus
* *Sink*  represents an energy flow out of a single bus
* *Transformer*  represents an energy flow from one bus to another


Mathematical description (generic formulation as graph wihtout timesteps)
----------------------------------------------------------------------------

 Entities are connected in such a way that buses are only connected to components
and vice versa. In this way the energy system can be interpreted as a bipartite graph.
In this graph the entities represent vertices. The inputs and the ouputs can
be interpreted as directed edges. For every edge in this graph there will be a value which
we will define as the weight of the edge.


Set of entities :math:`E` as a union of sets of buses (B),
transformers(F), sources (O), sinks (I) and transports (P) respectively,
which are the vertices:

.. math::
   E := \{ E_B, E_F, E_O, E_I, E_P \}

Set of Components:

.. math::
   E_C := E \setminus E_B

Set of directed edges...:

.. math::
   \vec{E} := \{(e_i, e_j),...\}

Function :math:`f` as "Uebertragunsfunktion" for each component used in constraints:

.. math::
   f(I_e, O_e) \leq \vec{0}, \quad \forall e \in E_C

:math:`I_e` and :math:`O_e` as subsets of :math:`E`:

.. math::
   I_e & := \{ i \in E | (i,e) \in \vec{E} \}\\
   O_e & := \{ o \in E | (e,o) \in \vec{E} \}

And additional constraint for outflow :math:`o` and inflow :math:`i` for each edge:

.. math::
   o_{e_1} - i_{e_2} = 0, \quad \forall (e_1, e_2) \in \vec{E}


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





Classes and packages
------------------------------------------

All energy system entities (busses and components) are represented in a class hierarchy that can be easily extended.
These classes form the basis for so so-called framework packages, that operate on top of them.

The framework consists of various packages that provide different functionalities.
Currently, there are three modules but in future further extensions will be made.

oemof's current packages:

* *feedinlib* generates wind and solar feedin timeseries for different plants and geographical locations
* *demandlib* generates electrical and thermal demands for different objects
* *solph* creates and solves a (mixed-integer) linear optimization problem for a given energy system

All packages may interact with each other but can also be used stand-alone.
A detailed description can be found in the following sections.


Documentation
~~~~~~~~~~~~~~~~~~~~~~~~

The framework is documented on three different levels:

* Code commenting 
* Code documentation
* General documentation


Code commenting
------------------------

Code comments are block and inline comments in the source code. They can help to understand the code and should be utilized "as much as necessary, as little as possible". When writing comments follow the PEP 0008 style guide: https://www.python.org/dev/peps/pep-0008/#comments.

Code documentation
------------------------

Code documentation is done via documentation strings, a.k.a. "docstrings", and used for all public modules, functions, classes, and methods. 

We are using the numpydoc extension of sphinx and thus the numpydoc docstring notation. 
PEP 0257 (https://www.python.org/dev/peps/pep-0257/) lays down a few, very general conventions for docstrings. Following is an example of a numpydoc docstring:

.. code:: python

    def docstring():
        r"""A one-line summary that does not use variable names or the
        function name.

        Several sentences providing an extended description. Refer to
        variables using back-ticks, e.g. `var`.
    
        Parameters
        ----------
        var1 : array_like
            Array_like means all those objects -- lists, nested lists, etc. --
            that can be converted to an array.  We can also refer to
            variables like `var1`.
        var2 : int
            The type above can either refer to an actual Python type
            (e.g. ``int``), or describe the type of the variable in more
            detail, e.g. ``(N,) ndarray`` or ``array_like``.
        Long_variable_name : {'hi', 'ho'}, optional
            Choices in brackets, default first when optional.
        main_dt : dictionary
            Main dictionary as described below [1]_
        prob : pulp.lp-problem
            LP-Problem-Variable, which contains the linear problem [2]_
    
        Returns
        -------
        type
            Explanation of anonymous return value of type ``type``.
        describe : type
            Explanation of return value named `describe`.
        out : type
            Explanation of `out`.
        prob : pulp.lp-problem
            LP-Problem-Variable, which contains the extended linear problem [2]_
    
        Other Parameters
        ----------------
        only_seldom_used_keywords : type
            Explanation
        common_parameters_listed_above : type
            Explanation
        Timesteps [t] : main_dt['timesteps']
            np-array with the timesteps according to the timeseries
        Regions [r] : main_dt['energy_system']['regions']
            See: solph.extenddc [4]_
        Electric demand : main_dt['timeseries']['demand'][r]['lele'][t]
            r = region, t = timesteps
        main_dt['energy_system'] : dict-branch with lists of components
            Definition of the 'energy_system' see: :py:mod:`solph.extenddc`
        main_dt['lp'] : dict-branch with all lp-variables
            Definition of lp-variables see: :py:mod:`solph.lp_definition`
    
        Raises
        ------
        BadException
            Because you shouldn't have done that.
    
        See Also
        --------
        otherfunc : relationship (optional)
        newfunc : Relationship (optional), which could be fairly long, in which
                  case the line wraps here.
        thirdfunc, fourthfunc, fifthfunc
        solph.main_model.create_model_equations : Blubber
    
        Notes
        -----
        Notes about the implementation algorithm (if needed).
    
        This can have multiple paragraphs.
    
        You may include some math:
    
        .. math:: X(e^{j\omega } ) = x(n)e^{ - j\omega n}
    
        And even use a greek symbol like :math:`omega` inline.
    
        References
        ----------
        Cite the relevant literature, e.g. [3]_.  You may also cite these
        references in the notes section above.
    
        .. [1] Link to the description of the main_dt for solph.
        .. [2] `PuLP <https://code.google.com/p/pulp-or/>`_, PuLP Documentation.
        .. [3] O. McNoleg, "The integration of GIS, remote sensing,
           expert systems and adaptive co-kriging for environmental habitat
           modelling of the Highland Haggis using object-oriented, fuzzy-logic
           and neural-network techniques," Computers & Geosciences, vol. 22,
           pp. 585-588, 1996.
    
        Examples
        --------
        These are written in doctest format, and should illustrate how to
        use the function.
    
        >>> a=[1,2,3]
        >>> print [x + 3 for x in a]
        [4, 5, 6]
        >>> print "a\n\nb" 
        a
        b
    
        """ 



General documentation
------------------------

The general implementation-independent documentation such as installation guide, flow charts, and mathematical models is done via ReStructuredText (rst). The files can be found in the folder */oemof/doc*.
For further information on restructured text see: http://docutils.sourceforge.net/rst.html.


oemof *base classes*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently, oemof provides the following classes. The first three levels represent the basic components to model energy systems. Additional subclasses can be defined underneath.

* Entity

  * Bus

  * Component

    * Sink

      * Simple

    * Source

      * Commodity
      * DispatchSource
      * FixedSource

    * Transformer

      * Simple
      * CHP
      * SimplexExtractionCHP
      * Storage

    * Transport

      * Simple

More information on the functionality of the respective classes can be found in their `ApiDocs [Link!] <http://www.python.org>`_.



The *feedinlib* package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The modelling library feedinlib is currently in a development stage.
Using feedinlib energy production timeseries of several energy plants can be created.
Focus is on fluctuating renewable energies like wind energy and photovoltaics.
The output timeseries can be input for the components of the energy system and therefore incorporated in the optimization within the modelling library solph.
However, a stand-alone usage of feedinlib is also intended.

Clone or fork the 'feedinlib' from github and use it within your project. Don’t forget to play back your fixes and improvements. We are pleased to get your feedback.




The *demandlib* package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Description of demandlib.




The *solph* package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The solph module of oemof allows to create and solve linear (and mixed-integer)
optimization problems. The optimization problem is build based on a energy
system defined via oemof-entities. These entities are instances of
oemof base classes (e. g. buses or components). For the definition of variables,
constraints and an objective function as well as for communication with solvers
etc. the python packages `Pyomo <http://www.pyomo.org/>`_ is used.

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
pre-defined objectives from the solph-library called *objectives.py*. These
pre-defined objectives are build by the use of objective expressions defined
in *objective_expressions*. Different objectives for optimization models
can be selected by setting the option *objective_types* inside the
*objective_assembler* method.


If necessary, the two libraries used be *assemlber* methods can be extended
and used in methods of *OptimizationModel()* afterwards.

Solve and other
****************
Moreover, the *OptimizationModel()* class contains a method for solving
the optimization model.


Postprocessing of results
----------------------------
To extract values from the optimization problem variables their exist a
postprossing module containing different functions.
Results can be written back to the oemof-objects or
to excel-spreadsheets.

