Oemof stands for "Open Energy System Modeling Framework" and provides a free, open source and clearly documented model to analyse energy supply systems. It is developed in Python and designed as a framework with a modular structure containing several packages which communicate through well defined interfaces.

With oemof we provide base packages for energy system modeling and optimization.

Documentation
=============

Full documentation can be found at http://oemof.readthedocs.org.


Installing oemof
=====================

.. code:: bash

  sudo pip3 install oemof

Developing oemof
=====================

We highly encourage you to contribute to further development of oemof. If you want to collaborate see description below or contact us.

To install the developer version two steps are necessary:

.. code:: bash

  git clone git@github.com:oemof/oemof.git
  sudo pip3 install -e /path/to/the/repository

See http://oemof.readthedocs.org/en/latest/installation_and_setup.html for further information.

See the developer version of the documentation at: http://oemof.readthedocs.org/en/latest/.

Further packages within oemof
==============================

`Feedinlib <https://github.com/oemof/feedinlib>`_  and `oemof.db <https://github.com/oemof/oemof.db>`_ are part of the oemof framework. They can be used to create energy system models but are not a must.

Examples
========

The linkage of specific modules of the various packages is called an application (app) and depicts for example a concrete energy system model.

There is one executable example energy system in `Storage optimization  <https://github.com/oemof/oemof/tree/master/examples/storage_optimization>`_.

Further example apps in development can be found in
`Development examples  <https://github.com/oemof/oemof/tree/master/examples/development_examples>`_.

License
=======

Copyright (C) 2015 oemof developing group

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
