##########################################
 Mathematical notation for solph
##########################################

Sets
------------------------------------------

========= ===== ============================== ===============================
Name      Index Description                    Elements from objects of class
========= ===== ============================== ===============================
E         e     Set of entities                solph.newtwork.Entity
B         b     Set of busses                  solph.network.entities.Bus
C         c     Set of components              solph.network.entities.Component
========= ===== ============================== ===============================

Subsets of Component Set C
******************************************


========= ===== ============================== ===============================
Name      Index Description                    Elements from objects of class
========= ===== ============================== ===============================
SSTO      st    Set of  simple storages        transformer.Storage
STRNF     trn   Set of simple tranformers      transformer.Simple
SBPCHP    bp    Set of simple chps             transformer.SimpleCHP
SEXCHP    ex    Set of simple extraction chps  transformer.SimpleExtractionCHP
STRPT     trp   Set of simple transports       transports.Simple
SSIK      si    Set of sinple sinks            sinks.Simple
COMM      co    Set of commodities             sinks.Commodity
FXSO      fx    Set of fixed sources           source.FixedSource
DISO      di    Set of dispatchable sources    source.DispatchSource
========= ===== ============================== ===============================

Other Sets
******************************************

========= ===== ============================== ===============================
Name      Index Description
========= ===== ============================== ===============================
T         t     Set of timesteps
E 	  ee	Set of ExE
I(c)      i     Set of inputs for component c
O(c)      o     Set of outputs for component c
========= ===== ============================== ===============================

Optimization variables
----------------------------------------------

========= ======= =============== ============================================
Name      Indices pyomo variable  Description
========= ======= =============== ============================================
W         ee, t   w               Inflow/Outflow variable of component c
ADDOUT    c       add_out         Variable for additional installed output c
ADDCAP    c       add_cap         Variable for additional installed capacity c
Y         c, t    y               Status variable of component c
Z_start   c, t    z_start         Variable indicating startup of component c
Z_stop    c, t    z_stop          Variable indicating shutdown of component c
GRADPOS   c, t    grad_pos_var    Diff. between outflow of two timesteps
GRADNEG   c, t    grad_neg_var    Diff. between outflow of two timesteps
========= ======= =============== ============================================

Optimization parameters
-------------------------------------------

========= ======= =============== ============================================
Name      Index   Attribute       Description
========= ======= =============== ============================================
out_max   c       out_max         Maximal outflow of component c
in_max    c       in_max          Maximal inflow of component c
in_min    c       in_min          Minimum inflow of component c
out_min   c       out_min         Minimum outflow of component c
========= ======= =============== ============================================

