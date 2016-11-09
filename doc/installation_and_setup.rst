.. _installation_and_setup_label:

######################
Installation and setup
######################

.. contents::
    :depth: 1
    :local:
    :backlinks: top


Introduction
============
Following you find guidelines for the installation process for different operation systems. 

Linux
======

If you have Python 3 installed
---------------------------------

As oemof is designed as a Phyton-module it is mandatory to have Python 3 installed. If you already have Python 3 you can install oemof by using pip. It is highly recommended to use a virtual environment. See this `tutorial
<https://docs.python.org/3/tutorial/venv.html>`_ for more help. Run the following code in your python environment:

.. code:: console

  pip3 install oemof

If you do not yet have pip installed, see section "Required Python packages" below for further help.

If you do not have Python 3 installed
---------------------------------------

There are different ways to install Python on your system. 
One way is to install Python 3 through the Linux repositories. If you are using Ubuntu/Debian try executing the following code in your terminal: 

.. code:: console

  sudo apt-get install python3
  sudo apt-get install python3-pip
  
Most Linux distributions will have Python 3 in their repository. Use the specific software management to install it.

Otherwise you can download different versions of Python via https://www.python.org/downloads/.

Solver
----------------

In order to use solph you need to install a solver. There are various commercial and open-source solvers that can be used with oemof. 

There are two common OpenSource solvers available (CBC, GLPK), while oemof recommends CBC (Coin-or branch and cut). But sometimes its worth comparing the results of different solvers.

To install the solvers have a look at the package repository of your Linux distribution or search for precompiled packages. GLPK and CBC ares available at Debian, Feodora, Ubuntu and others.

To learn how to install the solvers (CBC, GLPK, Gurobi, Cplex...) have a look at the `pyomo solver notes <https://software.sandia.gov/downloads/pub/pyomo/PyomoInstallGuide.html#Solvers>`_.


Required Python packages
-------------------------

To be able to install additional Python packages an installer program is needed. The preferred installer is pip which is included by default in the installation of Python 3.4 and later versions.
To install pip for earlier Python versions on Debian/Ubuntu try executing the following code in your terminal or use the software management of you Linux distribution: 

.. code:: console

  sudo apt-get install python3-pip

For further information refer to https://packaging.python.org/en/latest/installing/#install-pip-setuptools-and-wheel.

In order to install a package using pip execute the following and substitute package_name by the desired package:

.. code:: console

  pip3 install package_name

For further information on how to install Python modules check out https://docs.python.org/3/installing/index.html.

Using pip all necessary packages are installed automatically. Have a look at the `setup.py <https://github.com/oemof/oemof/blob/master/setup.py>`_  to see all requirements.


Windows
========

If you have Python 3 installed
--------------------------------

As oemof is designed as a Phyton-module it is mandatory to have Python 3 installed. If you already have Python 3 you can install oemof by using pip. Run the following code in your command window:

.. code:: console

  pip3 install oemof

If you do not yet have pip installed, see section "Required Python packages" below for further help.


Using WinPython (community driven)
---------------------------------------

Skip the steps you have already done. Check your architecture first (32/64 bit)

Install oemof

<<<<<<< HEAD
 1. Download latest Anaconda from `here <https://www.continuum.io/downloads#windows>`_ (64 or 32 bit)
 2. Install Anaconda
 3. Open the 'Anaconda Prompt' and type: :code:`pip install oemof`
=======
 1. Download latest `WinPython <http://winpython.github.io>`_ for Python 3.x (64 or 32 bit)
 2. Install WinPython
 3. Open the 'WinPython Command Prompt' and typ: :code:`pip install oemof`
 4. Install a :ref:`windows_solver_label` if you want to use solph and execute the solph examples
>>>>>>> 9a54ec9... include new experience with installation process
 

Using Anaconda (by Continuum Analytics)
----------------------------------------------

Skip the steps you have already done. Check your architecture first (32/64 bit)

Install oemof

 1. Download latest `Anaconda <https://www.continuum.io/downloads#windows>`_ for Python 3.x (64 or 32 bit)
 2. Install Anaconda
 3. Open the 'Anaconda Prompt' and typ: :code:`pip install oemof`
 4. Install a :ref:`windows_solver_label` if you want to use solph and execute the solph examples
 
.. _windows_solver_label: 

Windows Solver
----------------

In order to use solph you need to install a solver. There are various commercial and open-source solvers that can be used with oemof. 

You do not have to install both solvers. Oemof recommends the CBC (Coin-or branch and cut) solver. But sometimes its worth comparing the results of different solvers (e.g. GLPK).

 1. Downloaded CBC from here (`64 <http://ampl.com/dl/open/cbc/cbc-win64.zip>`_ or `32 <http://ampl.com/dl/open/cbc/cbc-win32.zip>`_ bit)
 2. Download GLPK from `here (64/32 bit) <https://sourceforge.net/projects/winglpk/https://sourceforge.net/projects/winglpk/>`_
 3. Unpacked CBC/GLPK to any folder (e.g. C:/Users/Somebody/my_programs)
 4. Add the path of the executable files of both solvers to the PATH variable using `this tutorial <http://www.computerhope.com/issues/ch000549.htm>`_
 5. Restart Windows
 
For commercial solvers (Gurobi, Cplex...) have a look at the `pyomo solver notes <https://software.sandia.gov/downloads/pub/pyomo/PyomoInstallGuide.html#Solvers>`_.


Required Python packages
--------------------------

To be able to install additional Python packages an installer program is needed. The preferred installer is pip which is included in the winpython download. 
If you do not have pip installed see here: https://packaging.python.org/en/latest/installing/#install-pip-setuptools-and-wheel.

In order to install a package using pip execute the following and substitute package_name by the desired package:

.. code:: console

  pip install package_name

For further information on how to install Python modules check out https://docs.python.org/3/installing/. Using pip all necessary packages are installed automatically. Have a look at the `setup.py <https://github.com/oemof/oemof/blob/master/setup.py>`_  to see all requirements.


Mac OS
=======

Installation guidelines for Mac OS are not available at the moment. However it should be possible to install Python 3 and its packages. Have look at the installation guide of Linux or Windows to get an idea what to do.

You can download python here: https://www.python.org/downloads/mac-osx/. For information on the installation process and on how to install python packages see here: https://docs.python.org/3/using/mac.html.

If you are a Mac user please help us to improve this installation guide.


.. _check_installation_label:

Run examples to check the installation
============================================

Run the examples to check the installation. From the command-line (or Anaconda Prompt) execute

.. code:: console

  oemof_example <name-of-example>

You can choose from the list of examples

 * storage_invest (solph)
 * simple_least_costs (solph)
 * investment (solph)
 * flexible_modelling (solph)
 * operational_example (solph)

For example

.. code:: console

  oemof_example simple_least_costs

If you want to run solph examples you need to have the CBC solver installed, see the ":ref:`solver_label`" section. To get more information about the solph examples see the ":ref:`solph_examples_label`" section.
