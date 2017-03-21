~~~~~~~~~~~~~~~
Getting started
~~~~~~~~~~~~~~~

Oemof stands for "Open Energy System Modelling Framework" and provides a free, open source and clearly documented toolbox to analyse energy supply systems. It is developed in Python and designed as a framework with a modular structure containing several packages which communicate through well defined interfaces.

With oemof we provide base packages for energy system modelling and optimisation.

Everybody is welcome to use and/or develop oemof. Read our :ref:`why_contribute_label` section.

.. contents::
    :depth: 1
    :local:
    :backlinks: top


Documentation
=============

Full documentation can be found at `readthedocs <http://oemof.readthedocs.org>`_. Use the `project site <http://readthedocs.org/projects/oemof>`_ of readthedocs to choose the version of the documentation. To get the latest news visit and follow our `website <https://www.oemof.org>`_.


Installing oemof
================

If you have a working Python3 environment, use pypi to install the latest oemof version.

.. code:: bash

  pip install oemof

For more details have a look at :ref:`installation_and_setup_label`.
  
The packages **feedinlib**, **demandlib** and **oemof.db** have to be installed separately. See section :ref:`using_oemof_label` for more details about all oemof packages.

If you want to use the latest features, you might want to install the **developer version**. See :ref:`developing_oemof_label` for more information. The developer version is not recommended for productive use.   
  
Structure of the oemof cosmos
=============================

Oemof packages are organised in different levels. The basic oemof interfaces are defined by the core libraries (network). The next level contains libraries that depend on the core libraries but do not provide interfaces to other oemof libraries (solph, outputlib). The third level are libraries that do not depend on any oemof interface and therefore can be used as stand-alone application (demandlib, feedinlib). Together with some other recommended projects (pvlib, windpowerlib) the oemof cosmos provides a wealth of tools to model energy systems. If you want to become part of it, feel free to join us. 

Examples
========

The linkage of specific modules of the various packages is called an 
application (app) and depicts for example a concrete energy system model.

You can execute examples of solph applications (:ref:`solph_examples_label`) from command-line by

.. code:: bash

  oemof_examples

Further reading in the ':ref:`check_installation_label`' section.


Keep in touch
=============

You can become a watcher at our `github site <https://github.com/oemof/oemof>`_, but this will bring you quite a few mails and might be more interesting for developers. If you just want to get the latest news you can follow our news-blog at `oemof.org <https://oemof.org/>`_.


License
=======

Copyright (C) 2017 oemof developing group

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


