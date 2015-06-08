=========================================
 Mathematical description
=========================================

.. contents:: Table of Contents


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
		 &b \in B_{el} :\text{Sets for electrical busses}\\
		 &b \in B_{th} :\text{Sets for thermal busses}\\
		 &b \in B_{r}  :\text{Sets for resource busses}\\
		\end{align*}

Sets for connections
---------------------

	.. math::
	   :nowrap:

		\begin{align*}
		 &(i,j) \in C_{all} : \text{Sets for all existing connections}\\
		 &(i,j) \in C_{elel}=B_{el} \times B_{el} : \text{Sets for all possible connections between el. busses}\\
		 &(i,j) \in C_{thth}=B_{th} \times B_{th} :\text{Sets for all possible connections between th. busses}\\
		\end{align*}

Sets power and heat variables:
---------------------------------

	.. math::
	   :nowrap:

		\begin{align*}
		 &(c,b,r) \in P: \text{Sets for all components with el. output } b \in B_{el}, r \in B_r\\
		 &(c,b,r) \in Q: \text{Sets for all components with th. output } b \in B_{th}, r \in B_r\\
		\end{align*}

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

				:math:`P` = {('p1','bus_el4','rngas3'), ('p2','bus_el4','rngas3')}

	
Parameter
~~~~~~~~~~~

Parameter for Demand
-----------------------

	.. math::
	   :nowrap:

		 \begin{align*}
		 \text{Demand} & \\
		  &D_{el}(b,t),\quad \forall b \in B_{el}, t \in T :\text{Demand for el. busses in $t$}\\
		  &D_{th}(b,t),\quad \forall b \in B_{th}, t \in T :\text{Demand for th. busses in $t$}\\
		 \end{align*}

Parameter for Transformers
---------------------------
	.. math::
	   :nowrap:

	 		\begin{align*}
			 \text{Max. power output:} & \\
			  &P_{max,el}(c,b,r),\quad \forall (c,b,r) \in P :\text{max. output for el. components}\\
			  &Q_{max,el}(c,b,r),\quad \forall (c,b,r) \in Q :\text{max. output for th. components}\\
		     \text{Efficiencies of transformers:} &\\
			  &ETA_{el}(c,b,r), \quad \forall (c,b,r) \in P :\text{el. Efficiency of component $(c,b,r)$}\\
			  &ETA_{th}(c,b,r), \quad \forall (c,b,r) \in Q :\text{th. Efficiency of component $(c,b,r)$}
			 \end{align*}


Variables 
~~~~~~~~~~~~~

Components
---------------

.. math::
   :nowrap:

	\begin{align*}
	 \text{Component output} & \\
	  &p(c,b,r,t),\quad \forall (c,b,r) \in P, t \in T :\text{Output of all el. components}\\
	  &q(c,b,r,t),\quad \forall (c,b,r) \in Q, t \in T :\text{Output of all th. components}\\
	 \end{align*}

Resource and exchange
------------------------

.. math::
   :nowrap:

	 \begin{align*}
	  &rcon(b,t),\quad \forall b \in B_r, t \in T     : \text{Resource consumption}\\
	  &ex(i,j,t), \quad \forall (i,j) \in C_{all}, t \in T:\text{Energy exchange in connection $(i,j)$}
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

Electrical demand
--------------------

.. math::
   :nowrap:
	
	\begin{align*}
		D_{el}(b,t) = &\sum_{(i,j=b,k)\in P}p(i,j,k,t) \\
		- &\sum_{(i=b,j) \in (C_{all} \cap C_{elel})} ex(i,j,t)\\
		+ &\sum_{(i,j=b) \in (C_{all} \cap C_{elel})} ex(i,j,t)\\ 
    	- &\sum_{i,j=b,t \in S} s_{charge}(i,j,t)\\	
	    + &\sum_{i,j=b,t \in S} s_{discharge}(i,j,t)\\	
		& &  \forall b \in B_{el}, t \in T\\
	\end{align*}	

Thermal demand
--------------------
.. math::
   :nowrap:

	\begin{align*}
		   D_{th}(b,t) = &\sum_{(i,j=b,k)\in P}q(i,j,k,t) \\
		- &\sum_{(i=b,j) \in (C_{all} \cap C_{thth})} ex(i,j,t)\\
		+ &\sum_{(i,j=b) \in (C_{all} \cap C_{thth})} ex(i,j,t)\\ 
    	- &\sum_{i,j=b,t \in S} s_{charge}(i,j,t)\\	
	    + &\sum_{i,j=b,t \in S} s_{discharge}(i,j,t)\\	
		& &  \forall b \in B_{th}, t \in T\\
	\end{align*}

Resource consumption 
---------------------
.. math::
   :nowrap:

	\begin{align*}
		rcon(b,t) \geq	 &\sum_{(i,j,k=b) \in P} \frac{p(i,j,k,t)}{ETA_{el}(i,j,k)}
		 + \sum_{(i,j,k=b) \in Q} \frac{q(i,j,k,t)}{ETA_{th}(i,j,k)}\\
		 & & \forall b \in B_r, t \in T
	\end{align*}


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

Parameter for Demand
-----------------------

	.. math::
	   :nowrap:

		 \begin{align*}
		 \text{Demand} & \\
		  &D_{el}(b,t),\quad \forall b \in B_{el}, t \in T :\text{Demand for el. busses in $t$}\\
		  &D_{th}(b,t),\quad \forall b \in B_{th}, t \in T :\text{Demand for th. busses in $t$}\\
		 \end{align*}

Parameter for Transformers
---------------------------
	.. math::
	   :nowrap:

	 		\begin{align*}
			 \text{Max. power output:} & \\
			  &P_{max,el}(c,b,r),\quad \forall (c,b,r) \in P :\text{max. output for el. components}\\
			  &Q_{max,el}(c,b,r),\quad \forall (c,b,r) \in Q :\text{max. output for th. components}\\
		     \text{Efficiencies of transformers:} &\\
			  &ETA_{el}(c,b,r), \quad \forall (c,b,r) \in P :\text{el. Efficiency of component $(c,b,r)$}\\
			  &ETA_{th}(c,b,r), \quad \forall (c,b,r) \in Q :\text{th. Efficiency of component $(c,b,r)$}
			 \end{align*}


Variables 
~~~~~~~~~~~~~

Components
---------------

.. math::
   :nowrap:

	\begin{align*}
	 \text{Component output} & \\
	  &p(c,b,r,t),\quad \forall (c,b,r) \in P, t \in T :\text{Output of all el. components}\\
	  &q(c,b,r,t),\quad \forall (c,b,r) \in Q, t \in T :\text{Output of all th. components}\\
	 \end{align*}

Resource and exchange
------------------------

.. math::
   :nowrap:

	 \begin{align*}
	  &rcon(b,t),\quad \forall b \in B_r, t \in T     : \text{Resource consumption}\\
	  &ex(i,j,t), \quad \forall (i,j) \in C_{all}, t \in T:\text{Energy exchange in connection $(i,j)$}
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

Balances
--------------------

Hier kommt nun wieder die Frage von oben zur Geltung. Speicher können einfach als Komponenten definiert werden, die den selben Bus als input und output haben. Oder wir betrachten sie extra. Ich stehe übrigens auf Kriegsfuß mit der Notation. Im Zweifel lieber den Text lesen.

.. math::
   :nowrap:
	
	\begin{align*}
		0 =\\
		+ &\sum_{(i,j=b,k)\in P}p(i,j,k,t) 			&\text{Sum of all components feeding in the bus}\\
		- &\sum_{(i=b,j,k)\in P}p(i,j,k,t) 			&\text{Sum of all components taking from the bus}\\
		+ rcon(b,t)						&\text{Source}
		- &\sum_{(i,j=b,k)\in P}D(b,t) 				&\text{Sum of all fix demand time series}\\
		+ &\sum_{(i,j=b,k)\in P}D(b,t) 				&\text{Sum of all fix feed-in time series}\\	
		- &\sum_{(i=b,j) \in (C_{all} \cap C_{b})} ex(i,j,t) 	&\text{Sum of all exports to other buses}\\
		+ &\sum_{(i,j=b) \in (C_{all} \cap C_{b})} ex(i,j,t) 	&\text{Sum of all imports from other buses}\\
    		- &\sum_{i,j=b,t \in S} s_{charge}(i,j,t) 		&\text{Sum of all storage chargings}\\	
	    	+ &\sum_{i,j=b,t \in S} s_{discharge}(i,j,t) 		&\text{Sum of all storage dischargings}\\
	    	+ &
		& &  \forall b \in B_{el}, t \in T\\
	\end{align*}
