.. _installation_and_setup_label:

######################
Installation and setup
######################

.. contents::
    :depth: 1
    :local:
    :backlinks: top


Following you find guidelines for the installation process for different operation systems.

Linux
=====

Having Python 3 installed
------------------------------

As oemof is designed as a Python package it is mandatory to have Python 3 installed. It is highly recommended to use a virtual environment. See this `tutorial <https://docs.python.org/3/tutorial/venv.html>`_ for more help or see the sections below. If you already have a Python 3 environment you can install oemof using pip:

.. code:: console

  pip install oemof

If you do not yet have pip installed in your python environment, see section :ref:`additional_packages_Linux` below for further help.

Using Linux repositories to install Python
------------------------------------------

Most Linux distributions will have Python 3 in their repository. Use the specific software management to install it. 
If you are using Ubuntu/Debian try executing the following code in your terminal: 

.. code:: console

  sudo apt-get install python3
  
You can also download different versions of Python via https://www.python.org/downloads/.

Using Virtualenv (community driven)
-----------------------------------

Skip the steps you have already done. Check your architecture first (32/64 bit).

 1. Install virtualenv using the package management of your Linux distribution, pip install or install it from source (`see virtualenv documentation <https://virtualenv.pypa.io/en/stable/installation/>`_)
 2. Open terminal to create and activate a virtual environment by typing:

    .. code-block:: console

       virtualenv -p /usr/bin/python3 your_env_name
       source your_env_name/bin/activate

 3. In terminal type: :code:`pip install oemof`
 4. Install a :ref:`linux_solver_label` if you want to use solph and execute the solph examples (See :ref:`check_installation_label` ) to check if the installation of the solver and oemof was successful

Warning: If you have an older version of virtualenv you should update pip :code:`pip install --upgrade pip`.

Using Anaconda
---------------------------------------

Skip the steps you have already done. Check your architecture first (32/64 bit).

 1. Download latest `Anaconda <https://www.continuum.io/downloads#linux>`_ for Python 3.x (64 or 32 bit)
 2. Install Anaconda

 3. Open terminal to create and activate a virtual environment by typing:

    .. code-block:: console

       conda create -n yourenvname python=3.4
       source activate yourenvname

 4. In terminal type: :code:`pip install oemof`
 5. Install a :ref:`linux_solver_label` if you want to use solph and execute the solph examples (See :ref:`check_installation_label` ) to check if the installation of the solver and oemof was successful
 
.. _linux_solver_label:

Solver
------

In order to use solph you need to install a solver. There are various commercial and open-source solvers that can be used with oemof. 

There are two common OpenSource solvers available (CBC, GLPK), while oemof recommends CBC (Coin-or branch and cut). But sometimes its worth comparing the results of different solvers.

To install the solvers have a look at the package repository of your Linux distribution or search for precompiled packages. GLPK and CBC ares available at Debian, Feodora, Ubuntu and others.

Check the solver installation by executing the test_installation example (see :ref:`check_installation_label` ).

To learn how to install (other) solvers (Gurobi, Cplex...) have a look at the `pyomo solver notes <https://software.sandia.gov/downloads/pub/pyomo/PyomoInstallGuide.html#Solvers>`_.

.. _additional_packages_Linux:

Additional Python packages
--------------------------

To be able to install additional Python packages an installer program is needed. The preferred installer is pip which is included by default in the installation of Python 3.4 and later versions.
To install pip for earlier Python versions on Debian/Ubuntu try executing the following code in your terminal or use the software management of you Linux distribution: 

.. code:: console

  sudo apt-get install python3-pip

For further information refer to https://packaging.python.org/en/latest/installing/#install-pip-setuptools-and-wheel.

In order to install a package using pip execute the following and substitute package_name by the desired package (e.g. virtualenv):

.. code:: console

  pip3 install package_name

For further information on how to install Python modules check out https://docs.python.org/3/installing/index.html.


Windows
=======

If you have Python 3 installed
------------------------------

As oemof is designed as a Phyton-module it is mandatory to have Python 3 installed. If you already have a working Python 3 environment you can install oemof by using pip. Run the following code in the command window of your python environment:

.. code:: console

  pip install oemof

If pip is not part of your python environment, see section :ref:`additional_packages_Win` below for further help or use WinPython/Anaconda (see below).


Using WinPython (community driven)
----------------------------------

Skip the steps you have already done. Check your architecture first (32/64 bit)

 1. Download latest `WinPython <http://winpython.github.io>`_ for Python 3.x (64 or 32 bit)
 2. Install WinPython
 3. Open the 'WinPython Command Prompt' and type: :code:`pip install oemof`
 4. Install a :ref:`windows_solver_label` if you want to use solph and execute the solph examples (See :ref:`check_installation_label` ) to check if the installation of the solver and oemof was successful
 

Using Anaconda
---------------------------------------

Skip the steps you have already done. Check your architecture first (32/64 bit)

 1. Download latest `Anaconda <https://www.continuum.io/downloads#windows>`_ for Python 3.x (64 or 32 bit)
 2. Install Anaconda

 3. Open 'Anaconda Prompt' to create and activate a virtual environment by typing:

    .. code-block:: console

       conda create -n yourenvname python=3.4
       activate yourenvname

    *It is recommended to use python 3.4. Some users reported that oemof does not work with
    Windows + Anaconda + Python 3.5*

 4. In 'Anaconda Prompt' type: :code:`pip install oemof`
 5. Install a :ref:`windows_solver_label` if you want to use solph and execute the solph examples (See :ref:`check_installation_label` ) to check if the installation of the solver and oemof was successful
 
.. _windows_solver_label: 

Windows Solver
--------------

In order to use solph you need to install a solver. There are various commercial and open-source solvers that can be used with oemof. 

You do not have to install both solvers. Oemof recommends the CBC (Coin-or branch and cut) solver. But sometimes its worth comparing the results of different solvers (e.g. GLPK).

 1. Downloaded CBC from here (`64 <http://ampl.com/dl/open/cbc/cbc-win64.zip>`_ or `32 <http://ampl.com/dl/open/cbc/cbc-win32.zip>`_ bit)
 2. Download GLPK from `here (64/32 bit) <https://sourceforge.net/projects/winglpk/https://sourceforge.net/projects/winglpk/>`_
 3. Unpacked CBC/GLPK to any folder (e.g. C:/Users/Somebody/my_programs)
 4. Add the path of the executable files of both solvers to the PATH variable using `this tutorial <http://www.computerhope.com/issues/ch000549.htm>`_
 5. Restart Windows

Check the solver installation by executing the test_installation example (see :ref:`check_installation_label` ).
 
For commercial solvers (Gurobi, Cplex...) have a look at the `pyomo solver notes <https://software.sandia.gov/downloads/pub/pyomo/PyomoInstallGuide.html#Solvers>`_.


.. _additional_packages_Win:

Additional Python packages
--------------------------

To be able to install additional Python packages an installer program is needed. The preferred installer is pip which is included in the winpython download. 
If you do not have pip installed see here: https://packaging.python.org/en/latest/installing/#install-pip-setuptools-and-wheel.

In order to install a package using pip execute the following and substitute package_name by the desired package:

.. code:: console

  pip install package_name

For further information on how to install Python modules check out https://docs.python.org/3/installing/. Using pip all necessary packages are installed automatically. Have a look at the `setup.py <https://github.com/oemof/oemof/blob/master/setup.py>`_  to see all requirements.


Mac OSX
======

Installation guidelines for Mac OS are still incomplete and not tested. As we do not have Mac users we could not test the following approaches, but they should work. If you are a Mac user please help us to improve this installation guide. Have look at the installation guide of Linux or Windows to get an idea what to do.

You can download python here: https://www.python.org/downloads/mac-osx/. For information on the installation process and on how to install python packages see here: https://docs.python.org/3/using/mac.html.

Virtualenv: http://sourabhbajaj.com/mac-setup/Python/README.html

Anaconda: https://www.continuum.io/downloads#osx

You have to install a solver if you want to use solph and execute the solph examples (See :ref:`check_installation_label` ) to check if the installation of the solver and oemof was successful.

CBC-solver: https://projects.coin-or.org/Cbc

GLPK-solver: http://arnab-deka.com/posts/2010/02/installing-glpk-on-a-mac/


.. _check_installation_label:

Run examples to check the installation
======================================

Run the examples to check the installation. From the command-line (or Anaconda Prompt / WinPython Command Prompt) execute:

.. code:: console

  oemof_examples <name-of-example> [-s <name-of-solver>]

You can choose from the list of examples

 * test_installation
 * storage_investment (solph)
 * simple_dispatch (solph)
 * csv_reader_investment (solph)
 * flexible_modelling (solph)
 * csv_reader_dispatch (solph)

For example

.. code:: console

  oemof_examples simple_least_costs

If you want to run solph examples you need to have the CBC solver installed, see the ":ref:`linux_solver_label`" or ":ref:`windows_solver_label`" section. To get more information about the solph examples see the ":ref:`solph_examples_label`" section.
