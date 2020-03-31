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

As oemof is designed as a Python package it is mandatory to have Python 3 installed. Python >= 3.5 is recommended. Lower versions may work but are not tested. It is highly recommended to use a virtual environment. See this `tutorial <https://docs.python.org/3/tutorial/venv.html>`_ for more help or see the sections below. If you already have a Python 3 environment you can install oemof using pip:

.. code:: console

  pip install oemof.solph

To use pip you have to install the pypi package. Normally pypi is part of your virtual environment.

You can also install the in-development version with::

    pip install https://github.com/oemof/oemof-solph/archive/dev.zip


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

 1. Download latest `Anaconda (Linux) <https://www.continuum.io/downloads#linux>`_ for Python 3.x (64 or 32 bit)
 2. Install Anaconda

 3. Open terminal to create and activate a virtual environment by typing:

    .. code-block:: console

       conda create -n yourenvname python=3.x
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

Other commercial solvers like Gurobi or Cplex can be used as well. Have a look at the `pyomo documentation <https://pyomo.readthedocs.io/en/latest/>`_ to learn about which solvers are supported.


Windows
=======

If you are new to Python check out the `YouTube tutorial <https://www.youtube.com/watch?v=eFvoM36_szM>`_ on how to install oemof under Windows. It will guide you step by step through the installation process, starting
with the installation of Python using WinPython, all the way to executing your first oemof example.

Having Python 3 installed
------------------------------

As oemof is designed as a Phyton-module it is mandatory to have Python 3 installed. Python >= 3.5 is recommended. Lower versions may work but are not tested. If you already have a working Python 3 environment you can install oemof by using pip. Run the following code in the command window of your python environment:

.. code:: console

  pip install oemof

If pip is not part of your python environment, you have to install the pypi package.


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

       conda create -n yourenvname python=3.x
       activate yourenvname

 4. In 'Anaconda Prompt' type: :code:`pip install oemof`
 5. Install a :ref:`windows_solver_label` if you want to use solph and execute the solph examples (See :ref:`check_installation_label` ) to check if the installation of the solver and oemof was successful

.. _windows_solver_label:

Windows Solver
--------------

In order to use solph you need to install a solver. There are various commercial and open-source solvers that can be used with oemof.

You do not have to install both solvers. Oemof recommends the CBC (Coin-or branch and cut) solver. But sometimes its worth comparing the results of different solvers (e.g. GLPK).

 1. Download CBC (`64 <http://ampl.com/dl/open/cbc/cbc-win64.zip>`_ or `32 <http://ampl.com/dl/open/cbc/cbc-win32.zip>`_ bit)
 2. Download `GLPK (64/32 bit) <https://sourceforge.net/projects/winglpk/>`_
 3. Unpack CBC/GLPK to any folder (e.g. C:/Users/Somebody/my_programs)
 4. Add the path of the executable files of both solvers to the PATH variable using `this tutorial <http://www.computerhope.com/issues/ch000549.htm>`_
 5. Restart Windows

Check the solver installation by executing the test_installation example (see :ref:`check_installation_label` ).

Other commercial solvers like Gurobi or Cplex can be used as well. Have a look at the `pyomo documentation <https://pyomo.readthedocs.io/en/latest/>`_ to learn about which solvers are supported.


Mac OSX
=======

Having Python 3 installed
------------------------------
If you have Python3 already installed, you can follow the installation instructions for Linux to install oemof.

Install Python 3
------------------------------
If you are using brew you can simply run

.. code:: console

  brew install python3

Otherwise please refer to https://www.python.org/downloads/mac-osx/ for installation instructions.

Mac Solver
--------------
So far only the CBC solver was tested on a Mac. If you are a Mac user and are using other Solvers successfully please help us to improve this installation guide.

Please follow the installation instructions on the respective homepages for details.

CBC-solver: https://projects.coin-or.org/Cbc

GLPK-solver: http://arnab-deka.com/posts/2010/02/installing-glpk-on-a-mac/

If you install the CBC solver via brew (highly recommended), it should work without additional configuration.

.. _check_installation_label:

Run the installation_test file
======================================


Test the installation and the installed solver:

To test the whether the installation was successful simply run

.. code:: console

  oemof_installation_test

in your virtual environment.
If the installation was  successful, you will get:

.. code:: console

    *********
    Solver installed with oemof:
    glpk: working
    cplex: not working
    cbc: working
    gurobi: working
    *********
    oemof successfully installed.

as an output.


