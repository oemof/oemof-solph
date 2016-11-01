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

As oemof is designed as a Phyton-module it is mandatory to have Python 3 installed. If you already have Python 3 you can install oemof by using pip. Run the following code in your terminal:

.. code:: console

  pip3 install oemof
  
It is highly recommended to use a virtual environment. See this `tutorial
<https://docs.python.org/3/tutorial/venv.html>`_ for more help.

If you do not yet have pip installed, see section "Required Python packages" below for further help.

If you do not have Python 3 installed
---------------------------------------

There are different ways to install Python on your system. 
One way is to install Python 3 through the Linux repositories. If you are using Ubuntu/Debian try executing the following code in your terminal: 

.. code:: console

  sudo apt-get install python3
  
Most Linux distributions will have Python 3 in their repository. Use the specific software management to install it.

Otherwise you can download different versions of Python via https://www.python.org/downloads/.


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

If you do not have Python 3 installed
---------------------------------------

To install python3 download the winpython version suitable for your system from http://winpython.sourceforge.net/ and follow the installation instructions.

Next, set the system’s PATH variable to include directories that include python components and packages. To do this go to *My Computer -> Properties -> Advanced System Settings -> Environment Variables*. In the User Variables section, edit or create the PATH statement to include the following (make sure to replace the path to winpython by your own path): 

.. code:: console

  C:\winpython;C:\winpython\python\Lib\site-packages\;C:\windpython\python\Scripts\; 



Required Python packages
--------------------------

To be able to install additional Python packages an installer program is needed. The preferred installer is pip which is included in the winpython download. 
If you do not have pip installed see here: https://packaging.python.org/en/latest/installing/#install-pip-setuptools-and-wheel.

In order to install a package using pip execute the following and substitute package_name by the desired package:

.. code:: console

  pip3 install package_name

For further information on how to install Python modules check out https://docs.python.org/3/installing/. Using pip all necessary packages are installed automatically. Have a look at the `setup.py <https://github.com/oemof/oemof/blob/master/setup.py>`_  to see all requirements.


Mac OS
=======

Installation guidelines for Mac OS are not available at the moment. However it should be possible to install Python 3 and its packages. Have look at the installation guide of Linux or Windows to get an idea what to do.

You can download python here: https://www.python.org/downloads/mac-osx/. For information on the installation process and on how to install python packages see here: https://docs.python.org/3/using/mac.html.

If you are a Mac user please help us to improve this installation guide.


.. _solver_label:

Install solver to use solph
===========================

In order to use solph you need to install a solver. There are various commercial and open-source solvers that can be used with oemof. 
The recommended open-source solver is Cbc (Coin-or branch and cut). 
See the CBC wiki for download and installation instructions: https://projects.coin-or.org/CoinBinary.

For other solvers (GLPK, Gurobi, Cplex...) have a look at the `pyomo solver notes <https://software.sandia.gov/downloads/pub/pyomo/PyomoInstallGuide.html#Solvers>`_.


.. _check_installation_label:

Run examples to check the installation
============================================

Run the examples to check the installation. From the command-line execute

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
