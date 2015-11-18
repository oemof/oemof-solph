=========================================
 Model description
=========================================

.. contents:: Table of Contents


Definitions 
~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Sets** should be named in capitals, e.g. :math:`T` for the timesteps 
* **Params** should be named in capitals, e.g. :math:`C` for costs
* **Variables** should be named in lower case, e.g. :math:`p` for power
   * **standard terms** should be used if possible, e.g. :math:`C_{capex}`
   * **dependencies of Variables** should be put in brackets, e.g. :math:`V(t,b)`
* **Grouping** (assuming only params. for variables it would be lower case)
   * **costs** should be named :math:`C` with a lower index, e.g. :math:`C_{fuel}`
   * **revenues** should be named :math:`R` with a lower index, e.g. :math:`R_{spot}`
   * **electrical** capacities should be named :math:`P`
   * **thermal capacities** should be named :math:`\dot Q`
   * **energy flows** should be named :math:`\dot E`
   * **electrical or mechanical work** should be named :math:`W`
   * **heat quantities** should be named :math:`Q`
   * **energy quantities** should be named :math:`E`
* **Additional characters** should be lower case and multiple indices devided by a comma, e.g. :math:`P_{chp,max}`
   * **subscripted characters** should be used for indices and general description, e.g. :math:`P_{i}` or :math:`P_{chp}`
   * **superscripted characters** should be avoided since they cannot be expressed in the code, e.g. :math:`P_{chp}` will work but :math:`P^{chp}` does not
* **Sums** should be written by putting the running index under the sign

When transforming a mathematical model into code it should be understandable, too. Therefore, Variables and Params should be named as close as possible to the mathematical model, e.g. the model param :math:`P_{chp,max}` should be named p_chp_max. In contrast, Objectives and Constraints should have „speaking names“ for easy debugging.

=======================
General description
=======================

An arbitrary energy system modeled with oemof will consist of entities which are connected. The following basic two different elements exist: 

* **Component**: a component that stores, converts, produces or consumes energy
* **Buses** : a combination components  

  Entities are connected in such a way that buses are only connected to components and vice versa. In this way the energy system can be interpreted as a bipartite graph. 
  In this graph the entities represent vertices. The inputs and the ouputs can be interpreted as directed edges. For every edge in this graph there will be a value which 
  we will define as the weight of the edge. 

=========================================
Mathematical description
=========================================


*not regarding timesteps so far...*

Generic formulation as graph
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set of entities :math:`E` as a union of sets of buses, transformers, sources, sinks and transports respectively, which are the vertices:

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

Examples for less generic formulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Buses**

.. math::
   \sum_{i \in I_e} i - \sum_{o \in O_e} o = 0, \quad \forall e \in E_B

**Transformers**

.. math::
   f(I_e) - \sum_{o \in O_e} o = 0, \quad \forall e \in E_F

e.g. simple gas power plant with efficiency :math:`\eta` and one inflow :math:`i` (gas) and one outflow :math:`o` (electricity).

.. math::
   \eta_e \cdot i_e - o_e = 0, \quad \forall e \in E_{simple gas power plant}

**Sinks**

.. math::
   i_e - v_e = 0, \quad \forall e \in E_I
   
with :math:`v` being the value of the sink, e.g. the electric demand in MWh of a household.

**Sources**

.. math::
   o_e - v_e = 0, \quad \forall e \in E_O
   
with :math:`v` being the value of the source, e.g. the electric supply in MWh of a wind turbine.

**Transports**

*still missing*


Optimization problem
~~~~~~~~~~~~~~~~~~~~~~~~~~

In the optimization problem with timesteps the weight of a edge :math:`(e_1,e_2) \in \vec{E}` will correspond to a variable :math:`w(e_1,e_2,t)`.

Sets
-----

**Timesteps**

.. math::
	t \in T \\


**Input/Output sets**

Indexed set that will exist for every component, containing their inputs and outputs which are elements of :math:`\in E_B`.

.. math::
   I_e & := \{ i \in E_B | (i,e) \in \vec{E},\forall e \in E_{C} \}\\
   O_e & := \{ o \in E_B | (e,o) \in \vec{E},\forall e \in E_{C} \}


Variables
--------------

The maximum value of a edge will be modeled as the upper bound of the edge associated variable. 

.. math::
  0 \leq w(e_1,e_2,t) \leq w_{max}(e_1,e_2,t), \quad \forall (e_1, e_2) \in \vec{E}, \forall t \in T

Additional variables needed for specific components will come from their models. 
For a simple storage the variable :math:`s_{soc}(e)` will be introduced using the index set :math:`e \in E_{simpleStorage}`.


Constraints
-------------

**Bus constraints**

.. math:: 
	\sum_{(e_1,e_2=b)} w(e_1,e_2,t) - \sum_{(e_1=b,e_2)} w(e_1,e_2,t) = 0, \quad \forall b \in E_B, \forall t \in T\\
    \sum_{t \in T} \sum_{(e_1=b,e_2) \in \vec{E}} w(e_1,e_2,t) \leq O_{max}(b), \quad \forall b \in E_B

**Simple power plant**

.. math::
   \eta_e \cdot w(I_e,e,t) - w(e,O_e,t) = 0, \quad \forall e \in E_{simple\_transformer}, \forall t \in T

**Simple combined heat and power plant**

.. math::
   \eta_e \cdot w(I_e,e,t) - \sum_{o \in O_e} w(e,o,t) = 0, \quad \forall e \in E_{simple\_chp}, \forall t \in T\\
   \frac{w(e,o_1,t)}{\eta_{el}(e)} = \frac{w(e,o_2,t)}{\eta_{th}(e)}, \quad \forall e \in E_{simple\_chp},\forall t \in T,~ o_1,o_2 \in O_e

**Storage**
.. math::

   \mathit{TODO: insert missing math}


=========================================
Draft fo a Mathematical description
=========================================

Sets 
~~~~~~~~~~~~~~~~~~~~~~~~~

Set for Timeseries
-------------------

	.. math::
	   :nowrap:

		\begin{align*}
		 & t \in T \\
		\end{align*}

Set for Components
-------------------

	.. math::
	   :nowrap:

		\begin{align*}
		 &ct \in CT :\text{Sets for all component types}\\
		 &c \in C(CT) :\text{Sets for all components of type ct}\\
		\end{align*}
	
Set for Busses:
-------------------

	.. math::
	   :nowrap:

		\begin{align*}
		 &bt \in BT :\text{Sets for all bus types}\\
		 &b \in B(BT) :\text{Sets for all buses of type bt}\\
		\end{align*}
		
Sets for connections
---------------------

	.. math::
	   :nowrap:

		\begin{align*}
		 &(i(bt),j(bt)) \in C_{all} : \text{Sets for all existing connections between buses of the same type } i \in B, j \in B, bt \in BT\\
		\end{align*}

.. _components:

Components
~~~~~~~~~~

.. raw:: html

    <font color="blue">
    
**Parameter:**
    
.. raw:: html

    </font>
    
.. raw:: html

    <font color="green">
    
**Variables:**

in(c,b,t)
            input into a component c from a branch b at a timestep t
    
out(c,b,t)
            output of a component c into a branch b at a timestep t
    
.. raw:: html

    </font>

Balances around buses
~~~~~~~~~~~~~~~~~~~~~

Full balance around all buses. Could differ according to the bus type

.. math::
   :label: balance_bus
   :nowrap:
	
	\begin{align*}
		0 =\\
		+ &\sum_{c \in C}out(c,b,t) 			&\text{Sum of all flows into the bus}\\
		- &\sum_{c\in C}in(c,b,t) 			&\text{Sum of all flows from the bus}\\
		&  & \forall c\in C,b \in B, t \in T\\
	\end{align*}
	
Basic Constraints
~~~~~~~~~~~~~~~~~

These constraints are use in more than one type and are referenced from these types.

.. _max_power_generic:

Maximal Power (generic)
-----------------------

The generic maximal output is set by its capacity parameter and its additional capacity variable.

.. math::
   :label: power_max
   :nowrap:

	\begin{align*}
   		out(c,b,t) \leq capacity(c) + capacity_{additional}(c,b,t)&\\
		& \forall c\in C, b\in B, t\in T\\
	\end{align*}
	
Resources
~~~~~~~~~~~~~~~~~

A fossil resource is a flow into a bus from outside the energy-system. The source is not defined.

Fossil resource
---------------

**Type: resource_fossil**

A fossil resource can be limited by a yearly energy amount.

Maximal Energy
^^^^^^^^^^^^^^

Maximal energy amount of a resource. Could be skipped if unbounded.

.. math::
   :nowrap:

	\begin{align*}
		energy_{max}(c,b) \geq	 &\sum_{t \in T} out(c,b,t)\\
		 & & \forall b \in B, t \in T
	\end{align*}
	
Renewable resource
------------------

**Type: resource_renewable**

A renewable resource is limited by its hourly production.

Maximal Energy
^^^^^^^^^^^^^^

.. math::
   :nowrap:

	\begin{align*}
        o_e - v_e = 0&\\
        &\forall e \in E_O
	\end{align*}
	   
with :math:`v` being the value of the source, e.g. the electric supply in MWh of a wind turbine.

.. _transformer:

Transformer
~~~~~~~~~~~

*inherits* :ref:`components`

Transformer (generic)
---------------------

**Type: transformer_generic**

*inherits* :ref:`transformer`

Transformer with one input and one output flow and a constant efficiency.

Connection of input and output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The output variable is connected to the input variable through a constant efficiency.

.. math::
   :label: transformer_generic_in_out
   :nowrap:

	\begin{align*}
   		\eta_e \cdot i_e - o_e = 0 \quad&\\
		& \forall e \in E_{type}\\
	\end{align*}
		
Maximal Power (optional)
^^^^^^^^^^^^^^^^^^^^^^^^

Maximal output of a transformer is set by its capacity parameter and its additional capacity variable.
If not set the maximal capacity if infinite.

See equation :eq:`power_max` in chapter :ref:`max_power_generic`


Ramps (optional)
^^^^^^^^^^^^^^^^

blabla.....

Combined Transformer (fixed ratio)
-----------------------------------

**Type: transformer_combined_fixed_ratio**

*inherits* :ref:`transformer`

Transformers with one input and two output flows and a constant efficiency for both flows (e.g. CHP with a fixed power-heat-rate).

Connection between the two output streams
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The output variable of the different flows are connected through a constant efficiency for each flow.

.. math::
   :label: transformer_combined_fixed_out_connect
   :nowrap:

	\begin{align*}
   		\frac{out(c,b1,t)}{\eta(c,b1)} = \frac{out(c,b2,t)}{\eta(c,b2)}&\\
		& \forall c\in C, b1,b2\in B, b1\neq b2, t\in T\\
	\end{align*}

Connection between input and outputs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The output variables are connected to the input variable through a constant efficiency for each flow.

.. math::
   :label: transformer_combined_fixed_in_out
   :nowrap:

	\begin{align*}
   		out(c,b1,t) = \eta(c,b1) \cdot in(c,b0,t)&\\
   		out(c,b2,t) = \eta(c,b2) \cdot in(c,b0,t)&\\
		& \forall c\in C, b0,b1,b2\in B, t\in T\\
	\end{align*}
	
Maximal Power (optional)
^^^^^^^^^^^^^^^^^^^^^^^^

Maximal output of a combined transformer is set by its capacity parameter and its additional capacity variable of the primary flow.
The primary flow is set by a parameter. If not set the maximal capacity if infinite. (Example: The primary flow of a CHP plant is typically power)

See equation :eq:`power_max` in chapter :ref:`max_power_generic`

Combined Transformer (variable ratio)
--------------------------------------

**Type: transformer_combined_variable_ratio**

Under construction....

.. _storages:

Storages
~~~~~~~~~

*inherits* :ref:`components`

.. raw:: html

    <font color="green">
    
**Variables:**

soc(c,t)
            state of charge of a component c from a branch b at a timestep t
    
.. raw:: html

    </font>

Storages get the input and the output from the same bus.

Storage (generic)
-----------------

**Type: storage_generic**

*inherits* :ref:`storages`

Connection of one state with the previous
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

still missing -> Uwe

Maximal state of charge
^^^^^^^^^^^^^^^^^^^^^^^

.. math::
   :label: storage_generic_max_soc
   :nowrap:
   
   \begin{align*}
      soc(c,t) & \leq capacity(c)+capacity_{additional}\\
      & \forall c \in C,t\in T\\
   \end{align*}

Minimal state of charge
^^^^^^^^^^^^^^^^^^^^^^^

The minimal SOC is set to zero. Should be changed in future versions.

.. math::
   :label: storage_generic_min_soc
   :nowrap:
   
   \begin{align*}
      soc(c,t)  & \geq0\\
      & \forall c \in C,t\in T\\ 
   \end{align*}

Maximal charge
^^^^^^^^^^^^^^

.. math::
   :label: storage_generic_max_charge
   :nowrap:
   
   \begin{align*}
      in(c,b,t) & \leq\frac{capacity(c)+capacity_{additional}}{EPR_{in}(c)}\\
      & \forall c \in C,b \in B,t\in T\\ 
   \end{align*}

Maximal discharge
^^^^^^^^^^^^^^^^^

.. math::
   :label: storage_generic_max_discharge
   :nowrap:

   \begin{align*}
      out(c,b,t) & \leq\frac{capacity(c)+capacity_{additional}}{EPR_{out}(c)}\\
      & \forall c \in C,b \in B,t\in T\\ 
   \end{align*}

Connectors
~~~~~~~~~~~

Connector (generic)
-------------------

to be continued



