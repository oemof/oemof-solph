.. _oemof_solph_label:

~~~~~~~~~~~
oemof-solph
~~~~~~~~~~~

Solph is an oemof-package, designed to create and solve linear or mixed-integer 
linear optimization problems. The packages is based on pyomo. To get started 
with solph, checkout the solph-examples in the `oemof/examples/solph` directory.

.. contents::
    :depth: 1
    :local:
    :backlinks: top


How can I use solph?
--------------------

To use solph you have to install oemof and at least one solver, that can be used together with pyomo. See `pyomo installation guide <https://software.sandia.gov/downloads/pub/pyomo/PyomoInstallGuide.html#Solvers>`_. You can test it by executing one of the existing examples. Be aware that the examples require the CBC solver but you can change the solver name in the example files to your solver.

Once the example work you are close to your first energy model.

Set up an energy system
^^^^^^^^^^^^^^^^^^^^^^^

something


Add your components to the energy system
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

something


Optimise your energy system 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

More to come...


Plotting your results
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Link to outputlib


Using the investment mode 
-------------------------


Mixed integer problems 
-----------------------



Adding additional constraints
-----------------------------



Mathematical notation for solph
------------------------------------


Sets 
^^^^^^^^^^^^^^^

.. math::
   :nowrap:

	\begin{tabular}{p{2cm}p{7cm}p{3cm}}\hline
	\textbf{Symbol}            & \textbf{Description}          & \textbf{Python-type of object in set}\\\hline
	\\
	$\mathcal{E}$        & Set of all Entities                                  & Entity\\
	$\mathcal{\vec{E}}$  & Set of all weighted edges $(e_i, e_j)$               & Tuple\\
	$\mathcal{E_B}$      & Set of all edges                                     & Bus \\
	$\mathcal{E_C}$      & Set of all components                                & Component\\
	$\mathcal{E}_{I}$    & Set of components with 1 input                       & Sink \\
	$\mathcal{E}_{O}$    & Set of components with 1 output                      & Source \\
	$\mathcal{E}_{IO}$   & Components with 1 input, 1 output $i_e \neq {o_{e,n}}$ & SimpleTransformer\\
	$\mathcal{E}_{IOO}$  & Components with 1 input, 2 outputs                   & SimpleCHP\\
	$\mathcal{E}_{S}$    & Components with 1 input, 1 output  $i_e = o_{e,n}$   & Storage\\
	$\mathcal{I}_e$      & All inputs of Entity $e$                             & Dict\\
	$\mathcal{O}_e$      & All outputs of Entity $e$                            & Dict\\
	$\mathcal{T}$        & Set of timesteps                                     & List \\ 
	\end{tabular}

Variables 
^^^^^^^^^^^^^^^^^^^^^^

.. math::
   :nowrap:

	\begin{tabular}{p{2cm}p{4cm}p{2cm}p{2cm}}\hline
	\textbf{Symbol}      & \textbf{Description}                      & \textbf{Possible Set}  & \textbf{Python variable}  \\\hline
	\\
	\multicolumn{4}{l}{\textbf{LP-models}}\\
	$w_{e_1, e_2}(t)$    & Weight of Edge $(e_1, e_2)$ at  $t$             & $(e_1, e_2) \in  \mathcal{\vec{E}}$   & \verb+w[e1,e2,t]+ \\
	$l_e(t)$             & Level of  component  $e$ at $t$                  & $e \in \mathcal{E}_S$     & \verb+cap[e,t]+     \\
	$g^{pos}_{e_{o,1}}(t)$ & Positive gradient between two sequential timesteps  & $e \in \mathcal{E}_C$     & \verb+grad_pos_var[e,t]+ \\
	$g^{neg}_{e_{o,1}}(t)$ & Negative gradient between two sequential timesteps  & $e \in \mathcal{E}_C$     & \verb+grad_neg_var[e,t]+ \\ 
	\\
	\multicolumn{4}{l}{\textbf{Dispatch-source only}}\\
	$w^{cut}_{e,o_e}(t)$ & Curtailment of value $w_{e, o_e}(t)$             &$e \in \mathcal{E}_O$     & \verb+curtailment_var[e1,e2,t]+ \\
	\\
	\multicolumn{4}{l}{\textbf{Investment models}}\\
	$\overline{w}^{add}_{o_e}$  & Optimized extension of bound $\overline{W}_{e, o_{e,1}}$    &$e \in \mathcal{E}_C$   &\verb+add_out[e]+ \\
	$\overline{l}^{add}_e$      & Optimized extension of bound $\overline{L}_e$               &$e \in \mathcal{E}_S$   &\verb+add_cap[e]+ \\
	\\
	\multicolumn{4}{l}{\textbf{MILP-models}}\\
	$y_e(t)$	     & Binary status variable of component  $e$ at $t$  &$e \in \mathcal{E}_C$     & \verb+y[e,t]+         \\
	$z^{start}_e(t)$     & Binary startup variable of component $e$ at $t$ &$e \in \mathcal{E}_C$     & \verb+z_start[e,t]+   \\
	$z^{stop}_e(t)$	     & Binary shutdown variable of component $e$ at $t$ &$e \in \mathcal{E}_C$    & \verb+z_stop[e,t]+   \\
	\end{tabular}

Parameters 
^^^^^^^^^^^^^^^^^
Parameters will be notate with uppercase. 

.. math::
   :nowrap:

	\begin{tabular}{p{2cm}p{5cm}p{4cm}p{1.5cm}}\hline
	\textbf{Symbol}            & \textbf{Description}                            & \textbf{Python variable} & \textbf{Python type} \\\hline

	$V_e$                      & Value of Component 
		                     $e \in \{\mathcal{E}_o, \mathcal{E}_I\}$        & \verb+val+  & \\
	$V^{norm}_e$                      & Normend value of component 
		                     $e \in \{\mathcal{E}_o, \mathcal{E}_I\}$        & \verb+val+  & \\                             
	$\eta_{i_e,o_{e,n}}$       & Efficiency at conversion of input $i_e$ to 
		                     $n-$th output $o_{e,n}$ of component $e$        & \verb+eta+ & list\\
	$\overline{W}_{e_1, e_2}$  & Upper bound of variable $w_{e_1, e_2}$          & \verb+out_max+ / \verb+in_max+ & list\\
	$\underline{W}_{e_1, e_2}$ & Lower bound of variable  $w_{e_1, e_2}$         & \verb+out_min+ / \verb+in_min+ & list\\
	$\overline{L}_e$           & Upper bound of variable $l_e$                   & \verb+cap_max+       & float\\
	$\underline{L}_e$          & Lower bound of variable $l_e$                   & \verb+cap_min+       & float\\
	$C^{rate}_{e_i}$           & C-rate input of component $e$                   & \verb+c_rate_in+     & float\\
	$C^{rate}_{e_o}$	   & C-rate output of component $e$		     & \verb+c_rate_out+    & float\\
	$\overline{O}^{global}_e$  & Global limit for all outputs of entity $e$      & \verb+sum_out_limit+ & float\\
	$\overline{G}^{pos}_{e_{o,1}}$ & Upper bound for positive gradient of 1st output     & \verb+grad_pos+ & float\\
	$\overline{G}^{neg}_{e_{o,1}}$ & Upper bound for negative gradient of 1st output     & \verb+grad_neg+ & float\\
	$C^{loss}_e$                 & Loss of energy per timestep                     & \verb+cap_loss+       & float \\
        $T^{min,off}_e$              & Minimum down-time of component $e$               & \verb+t_min_off+      & float \\    
        $T^{min,on}_e$               & Minimum up-time of component $e$               & \verb+t_min_on+      & float \\          
	\\
	\multicolumn{4}{l}{\textbf{Cost/Revenue parameters}}\\
        $C_{e,i}$                    & Costs for one unit inflow of Component $e$      & \verb+input_costs+   & list\\
	$C_{e,o}$                   & Costs for one unit outflow of Component $e$     & \verb+output_costs+ \verb+opex_var+ & list\\
	$R_{e,i}$                  & Revenues for one unit inflow of Component $e$   & \verb+input_revenues+ & list \\ 
	$R_{e,o_n}$                & Revenues for one unit outflow of the 
		                     $n$-th output of Component $e$                  & \verb+output_revenues+ & list\\
        $C^{cut}_e$    & Costs for curtailment of variable  & \verb+curtailment_costs+ & float \\
	\end{tabular}


