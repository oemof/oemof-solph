=========================================
 Mathematical description
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

How to model energy systems using solph:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To understand how energy systems are modeled in solph we need to introduce some 
omoef/solph specific definitions.

An arbitrary energy system will consist of the following elements: 

* **Component**: a component that stores, converts, produces or consumes energy
* **Busses** : a combination of sinks and sources, transformers, input/output of storages, input/output connections between busses which add up to a bus balance 
* **Connection**: a connection between busses of same type

*Components*

	The input and the ouput side of a component will connected to a bus. Connections between components and
	busses are defined without loss. If the component has electrical and thermal output the component is virtually splitted
	in two using two variables in the mathematical model. One variable for el. output and one for the th. output.  

	Example: 

	* The input of a PowerToGas-unit will be connected to an electrical bus while the output will be connected to a gas-bus
    * The input of a PowerToHeat-unit will be connected to an electrical bus and the output will be connected to a thermal-bus

*Busses* 

	Busses can have an associated components which can be of types: 
    
    * Sink: can be a consumer or a demand 
    * Source: can be feedin of renewable energies 
    * Storage: can be electrical Storage 
    * Transformer: can be an powerplant
  
	More over busses can have connections to other busses of same type. For every bus the bus energy(carrier)-balance must hold.
	This is for example the electrical demand(sink) of a electrical bus must equal electrical output 
	of the components (e.g.transformers), and the electrical netto exchange with other busses connected. 
	The same can be applied for thermal busses or gas busses. Note that this definition holds for coal or biomass busses as well, even if 
    there are no storages and connections to other busses. If components do not exist they can be omitted.  
 
	A bus can be connected to the input or output side of components. 
	
	Examples:
    
	* Coal-(resource)bus on input side of Coal-powerplant 
	* Gas-(resource)bus as ouput of PowerToGas-unit



*Connections (between busses)* 

	Generally the follwing connections may exist: 

	#. resource - resource
	#. electricity - electricity 
	#. thermal - thermal 

Sets 
~~~~~~~~~~~~~~~~~~~~~~~~~

Set for Timeseries
-------------

	.. math::
	   :nowrap:

		\begin{align*}
		 & t \in T \\
		\end{align*}
	
Set for Busses:
-------------------

	.. math::
	   :nowrap:

		\begin{align*}
		 &b \in B_{el} :\text{Sets for electrical busses}\\
		 &b \in B_{th} :\text{Sets for thermal busses}\\
		 &b \in B_{r}  :\text{Sets for resource busses}\\
		 &b \in B :    \text{Set of all busses}
		\end{align*}

Sets for connections
---------------------

	.. math::
	   :nowrap:

		\begin{align*}
		 &(i,j) \in C: \text{Set for all existing connections}\\
		\end{align*}

This is the set for all existing connections. All possible connections for busses of same type can be calculated by 
the cartesian product e.g. :math:`C_{all} = (i,j) = B_{el} x B_{el},~i \neq j`  

Sets for Sinks and Sources
---------------------
.. math::
	   :nowrap:

		\begin{align*}
		 &(c,b) \in IN: \text{Set for Sources}
		 &(c,b) \in OUT: \text{Set for Sinks}\\
		\end{align*}

Sets transformers:
---------------------------------

	.. math::
	   :nowrap:

			\begin{align*}
			 &(c,b,r) \in P: \text{Set for all transformers with el. output, } b \in B_{el}, r \in B_r\\
			 &(c,b,r) \in Q: \text{Set for all transformers with th. output, } b \in B_{th}, r \in B_r\\
		     &(c,b,r) \in TRANSF= P \cup Q: \text{Set of all Transformers, } b \in B
			\end{align*}

Examples
^^^^^^^^^^ 
	Timeseries: 

		:math:`T = \{1,2,\dots, 8760\}`
    
	Busses:

		To model 3 el. busses and three th. busses initialize the sets as follows:

			:math:`B_{el}` = \{'bel1','bel2','bel3'\}, :math:`B_{el}` = \{'bth1','bth2','bth3'\}

		If there exist an connection between two busses, this will be defined via elements (tuples) in set :math:`C`:

			:math:`C` = \{('bel1','bel2'),('bel2','bel1'),('bel2','bel2'),('bth1','bth3')\}

	Power and Heat: 
	
    	To model the electrical output of two components both connected to the same el. and resource bus do:

				:math:`P` = {('p1','bus_el4','rngas3'), ('p2','bus_el4','rngas3')}

	
Parameter
~~~~~~~~~~~

Parameter for Source and Sink
-----------------------

	.. math::
	   :nowrap:

		 \begin{align*}
		 \text{Demand} & \\
		  &SINK(c,b,t),\quad \forall (c,b) \in IN, t \in T :\text{Sink (c,b) in $t$}\\
		  &SOURCE(c,b,t),\quad \forall (c,b) \in OUT, t \in T :\text{Source (c,b) in $t$}\\
		 \end{align*}

Parameter for Transformers
---------------------------
	.. math::
	   :nowrap:

	 		\begin{align*}
			 \text{Max. power output:} & \\
			  &P_{max}(c,b,r),\quad \forall (c,b,r) \in TRANSF :\text{max. output of transformer $(c,b,r)$}\\
		     \text{Efficiencies of transformers:} &\\
			  &ETA(c,b,r), \quad \forall (c,b,r) \in TRANSF :\text{Conversion efficiency of transformer $(c,b,r)$}\\
			 \end{align*}


Variables 
~~~~~~~~~~~~~

Transformer
---------------

.. math::
   :nowrap:

	\begin{align*}
	 \text{Component output} & \\
	  &p(c,b,r,t),\quad \forall (c,b,r) \in TRANSF, t \in T :\text{Output of all transformer components}\\
	 \end{align*}

Resource and exchange
------------------------

.. math::
   :nowrap:

	 \begin{align*}
	  &rcon(b,t),\quad \forall b \in B, t \in T     : \text{Resource consumption from bus $b$}\\
	  &ex(i,j,t), \quad \forall (i,j) \in C, t \in T:\text{Energy exchange in connection $(i,j)$}
	 \end{align*}

Storages 
------------

.. math::
   :nowrap:

	 \begin{align*}
	 & s_{charge}(c,b,t), \quad \forall (c,b) \in S, t \in T\\
	 & s_{discharge}(c,b,t), \quad \forall (c,b) \in S, t \in T\\
	 & s_{soc}(c,b,t), \quad \forall (c,b) \in S, t \in T
	 \end{align*}

Constraints 
~~~~~~~~~~~~~~~~~~~~

Bus Balance
--------------------

.. math::
   :nowrap:
	
	\begin{align*}
		0 = \\
		& + \sum_{c,i=b \in IN} SOURCE(c,i,t) \\
		&-  \sum_{c,i=b \in OUT} SINK(c,i,t) \\
		&+ \sum_{(i,j=b,k)\in TRANSF} p(i,j,k,t) \\
		&- \sum_{(i=b,j) \in C} ex(i,j,t) \\
		&+ \sum_{(i,j=b) \in C} ex(i,j,t)\\ 
    	&- \sum_{i,j=b,t \in S} s_{charge}(i,j,t) \\
		&+ \sum_{i,j=b,t \in S} s_{discharge}(i,j,t)\\
		&- \sum_{i=b \in B} rcon(i,t) \\	
		&  & \forall b \in B, t \in T\\
	\end{align*}	

Resource consumption 
---------------------
.. math::
   :nowrap:

	\begin{align*}
		rcon(b,t) \geq	 &\sum_{(i,j,k=b) \in TRANSF} \frac{p(i,j,k,t)}{ETA(i,j,k)}\\
		 & & \forall b \in B, t \in T
	\end{align*}

Sum of resource consumption for every bus in every timestep that ends up in the bus-balance. 

Storages 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As used in  :py:func:`oemof.solph.storage_constraints.storage_power_lim`

Discharge limitation by maximal discharge power
-----------------------------------------------

.. math::
   :nowrap:

   \begin{align*}
      S_{discharge}(r,t,c) & \leq\frac{S_{capacity}}{EPR_{out}}\\
      & \forall r\in regions,t\in hoy,c\in storages\\
      \intertext{with\, variable\, investment\,(if\, invest)} 
      S_{discharge}(r,t,c) & \leq\frac{S_{capacity}+S_{installed}^{lp-var}}{EPR_{out}}\\
      & \forall r\in regions,t\in hoy,c\in storages\\
      \intertext{thermal\, storage\, in\, a\, domestic\, heating\, system\,(if\, domestic\, and\, invest)}S_{discharge}(r,t,c) & \leq\frac{S_{capacity}+S_{installed}^{lp-var}}{EPR_{out}}\cdot\frac{D(r,t,HS(c))}{HS_{capacity}(c)}\\
      & \forall r\in regions,t\in hoy,c\in storages
   \end{align*}
   
Charge limitation by maximal charge power
-----------------------------------------

.. math::
   :nowrap:
   
   \begin{align*}
      S_{charge}(r,t,c) & \leq\frac{S_{capacity}}{EPR_{in}}\\
      & \forall r\in regions,t\in hoy,c\in storages\\
      \intertext{with\, variable\, investment\,(if\, invest)}S_{charge}(r,t,c) & \leq\frac{S_{capacity}+S_{installed}^{lp-var}}{EPR_{in}}\\
      & \forall r\in regions,t\in hoy,c\in storages\\
      \intertext{thermal\, storage\, in\, a\, domestic\, heating\, system\,(if\, domestic\, and\, invest)}S_{charge}(r,t,c) & \leq\frac{S_{capacity}+S_{installed}^{lp-var}}{EPR_{out}}\cdot\frac{D(r,t,HS(c))}{HS_{capacity}(c)}\\
      & \forall r\in regions,t\in hoy,c\in storages
   \end{align*}



Minmal SOC
----------

.. math::
   :nowrap:
   
   \begin{align*}
      SOC^{lp-var}(r,t,c) & \geq0\\
      & \forall r\in regions,t\in hoy,c\in storages\\   
   \end{align*}

Maximal SOC
-----------

.. math::
   :nowrap:
   
   \begin{align*}
      SOC^{lp-var}(r,t,c) & \leq S_{capacity}\\
      & \forall r\in regions,t\in hoy,c\in storages\\
      \intertext{with\, variable\, investment\,(if\, invest)}SOC^{lp-var}(r,t,c) & \leq S_{capacity}+S_{installed}^{lp-var}\\
      & \forall r\in regions,t\in hoy,c\in storages
   \end{align*}


=========================================
 Uwes Mathematical description
=========================================


Definitions 
~~~~~~~~~~~~~~~~~~~~~~~~~~


Sets 
~~~~~~~~~~~~~~~~~~~~~~~~~

Set for Timeseries
-------------

	.. math::
	   :nowrap:

		\begin{align*}
		 & t \in T \\
		\end{align*}
	
Set for Busses:
-------------------

	.. math::
	   :nowrap:

		\begin{align*}
		 &bt \in BT :\text{Sets for all bus types}\\
		 &b(bt) \in B :\text{Sets for all buses of type bt}\\
		\end{align*}

Sets for connections
---------------------

	.. math::
	   :nowrap:

		\begin{align*}
		 &(i(bt),j(bt)) \in C_{all} : \text{Sets for all existing connections between buses of the same type } i \in B, j \in B, bt \in BT\\
		\end{align*}

Weiß jemand die Notation um deutlich zu machen, dass innerhalb einer Connection gilt: :math:`i \neq j` bzw. müssen wir das überhaupt. Es ist ja nur sinnlos, aber nicht falsch wenn eine Verbindung von B1 nach B1 existiert.

Sets of components:
---------------------------------

	.. math::
	   :nowrap:

		\begin{align*}
		 &(c,b,r) \in P: \text{Sets for all components } b \in B, r \in B\\
		 &(c(b),r)\text{Sets of all transformer with the same output b } b \in B\\
		 &(c(r),b)\text{Sets of all transformer with the same input b } b \in B\\
		 &(c(b))\text{Sets of all storages with the same connection b } b \in B\\ 	 
		\end{align*}
		
Ich bin mir unsicher mit der Notation.		
Weiß nicht ob wir alle Komponenten gleich definieren sollen. Dann wäre ein Speicher eine Kompente bei der b und r gleich wäre also der input und der output in den selben Bus gehen.

Examples
^^^^^^^^^^ 
	Timeseries: 

		:math:`T = \{1,2,\dots, 8760\}`
    
	Busses:

		To model 3 el. busses and three th. busses initialize the sets as follows:

			:math:`B_{el}` = \{'bel1','bel2','bel3'\}, :math:`B_{el}` = \{'bth1','bth2','bth3'\}

		If there exist an connection between two busses, this will be defined via elements (tuples) in set :math:`C_{all}`:

			:math:`C_{all}` = \{('bel1','bel2'),('bel2','bel1'),('bel2','bel2'),('bth1','bth3')\}

	Power and Heat: 
	
    	To model the electrical output of two components both connected to the same el. and resource bus do:

				:math:`P` = {('p1','outbus_el4','inbus_ngas3'), ('p2','outbus_el4','inbus_ngas3')}

	A power2gas component would be the opposite:
				:math:`P` = {('p3','outbus_ngas3','inbus_el4')}

	
Parameter
~~~~~~~~~~~

Resource and exchange
------------------------

.. math::
   :nowrap:

	 \begin{align*}
	  &rcon(b,t),\quad \forall b \in B_r, t \in T     : \text{Resource consumption}\\
	  &ex(i,j,t), \quad \forall (i,j) \in C_{all}, t \in T:\text{Energy exchange in connection $(i,j)$}
	 \end{align*}


Constraints 
~~~~~~~~~~~~~~~~~~~~

Balances
--------------------

Hier kommt nun wieder die Frage von oben zur Geltung. Speicher können einfach als Komponenten definiert werden, die den selben Bus als input und output haben. Oder wir betrachten sie extra. Ich stehe übrigens auf Kriegsfuß mit der Notation. Im Zweifel lieber den Text lesen.

.. math::
   :nowrap:
	
	\begin{align*}
		0 =\\
		+ &\sum_{(i,j=b,k)\in P}p(i,j,k,t) 			&\text{Sum of all components feeding in the bus}\\
		- &\sum_{(i=b,j,k)\in P}p(i,j,k,t) 			&\text{Sum of all components taking from the bus}\\
		+ & rcon(b,t)						&\text{Source}\\
		- &\sum_{(i,j=b,k)\in P}D(b,t) 				&\text{Sum of all fix demand time series}\\
		+ &\sum_{(i,j=b,k)\in P}D(b,t) 				&\text{Sum of all fix feed-in time series}\\	
		- &\sum_{(i=b,j) \in (C_{all} \cap C_{b})} ex(i,j,t) 	&\text{Sum of all exports to other buses}\\
		+ &\sum_{(i,j=b) \in (C_{all} \cap C_{b})} ex(i,j,t) 	&\text{Sum of all imports from other buses}\\
    		- &\sum_{i,j=b,t \in S} s_{charge}(i,j,t) 		&\text{Sum of all storage chargings}\\	
	    	+ &\sum_{i,j=b,t \in S} s_{discharge}(i,j,t) 		&\text{Sum of all storage dischargings}\\
	    	+ &
		& &  \forall b \in B_{el}, t \in T\\
	\end{align*}
