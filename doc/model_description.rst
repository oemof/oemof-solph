=========================================
 Model description
=========================================

.. contents:: The tiny table of contents

Overview
~~~~~~~~~~~~~~~~~~~~~~~~~

....

Concept
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

....

Energy System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

....

Examples
----------------

Transformer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

General
---------------------

Thermal power plants
---------------------

Power to Gas plants
---------------------

CHP plants and blocks
---------------------

Domestic Systems
----------------


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


Electrical storages
-------------------

Domestic heating storages
-------------------------

District heating storages
-------------------------

Gas storages
-----------------



Resources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

....


Transmission
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Electrical grid
-------------------

Gas Grid
----------------

