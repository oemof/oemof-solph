Oemof stands for "Open Energy System Modelling Framework" and provides a free, open source and clearly documented toolbox to analyse energy supply systems. It is developed in Python and designed as a framework with a modular structure containing several packages which communicate through well defined interfaces.

With oemof we provide base packages for energy system modelling and optimisation.

Everybody is welcome to use and/or develop oemof.

Documentation
=============

Full documentation can be found at `readthedocs <http://oemof.readthedocs.org>`_. Use the `project side <http://readthedocs.org/projects/oemof>`_ of readthedocs to choose the version of the documentation. To get the latest news visit and follow us at our `wordpress block <https://oemof.wordpress.com>`_.


Installing oemof
=====================

Use pypi to install the latest oemof version.

.. code:: bash

  pip3 install oemof
  
The packages feedinlib, demandlib and oemof.db have to be installed separately. See section :ref:`using_oemof_label` for more details.
  
  
Structure of the oemof cosmos
=============================

Oemof is organised in different levels. The basic oemof interfaces are defined by the core libraries. The next level contains libraries that depend on the core libraries but do not provide interfaces to other oemof libraries. The third level are libraries that do not depend on any oemof interface and therefore can be used as stand-alone application. Together with some other recommended projects the oemof cosmos provides a wealth of tools to model energy systems. If you want to become part of it, feel free to join us. 

Examples
========

The linkage of specific modules of the various packages is called an 
application (app) and depicts for example a concrete energy system model.

There are `examples of applications <https://github.com/oemof/oemof/tree/master/examples/>`_ available. Make sure to download all files of an folder to get the wanted example run.


License
=======

Copyright (C) 2016 oemof developing group

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/.
