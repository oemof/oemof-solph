.. _installation_and_setup_label:

######################
Installation and setup
######################

Following you find guidelines for the installation process for various
operating systems. oemof.solph is a Python package, thus it requires you to
have Python 3 installed. On top of that, you need a solver to use oemof.solph.

There are several solvers that can work with oemof.solph, both open source and
commercial. Two open source solvers are widely used (HiGHS, CBC and GLPK), but
oemof.solph suggests CBC (Coin-or branch and cut). It may be useful to compare
results of different solvers to see which performs best. Other commercial
solvers, like Gurobi or Cplex, are also options. Have a look at the
`pyomo docs <https://pyomo.readthedocs.io/en/stable/api/pyomo.solvers.plugins.solvers.html>`__
to learn about which solvers are supported.

.. tab-set::

   .. tab-item:: Using conda (all OS)

      You can download a lightweight and open source variant of conda:
      "miniforge3".

      1. Download latest `miniforge3 <https://github.com/conda-forge/miniforge>`__
         for Python 3.x (64 or 32 bit).
      2. Install miniforge3
      3. Open "miniforge prompt" to manage your virtual environments. You can
         create a new environment and acivate it by

         .. code-block:: console

            conda create -n oemof-solph-env python=3.11

         .. code-block:: console

            conda activate oemof-solph-env

      4. Install a solver, e.g. CBC

         .. code-block:: console

            conda install -c conda-forge coincbc

      5. Only AFTER you have installed the solver via conda, use pip to install
         oemof.solph:

         .. code-block:: console

            pip install oemof.solph

   .. tab-item:: Linux

      **Install oemof.solph**

      With python3 installed, we recommend installing oemof.solph within a
      virtual Python environment and not into the base, system-wide Python
      installation. On Linux you can use virtualenv to do so.

      1. Open terminal to create and activate a virtual environment by typing:

         .. code-block:: console

            python -m venv /path/to/desired/oemof-solph-env
            source /path/to/desired/oemof-solph-env/bin/activate

      2. In terminal type:

         .. code-block:: console

            pip install oemof.solph

      **Install a solver**

      To install the solvers have a look at the package repository of your
      Linux distribution or search for precompiled packages. GLPK and CBC ares
      available at Debian, Feodora, Ubuntu and others.

   .. tab-item:: Windows (solver only)

      We recommend using conda for the python installation, with which you can
      also install a solver. If you want to install the solver externally (not
      via conda), you can follow these steps:

      1. Download `CBC <https://github.com/coin-or/Cbc/releases>`_ or
         `GLPK (64/32 bit) <https://sourceforge.net/projects/winglpk/>`_
      2. Unpack CBC/GLPK to any folder (e.g. C:/Users/Somebody/my_programs)
      3. Add the path of the executable files of both solvers to the PATH
         variable (can be done per user without administrator privileges).
      4. Restart Windows

   .. tab-item:: OSX (solver only)

      We recommend using conda for the python installation, with which you can
      also install a solver. If you want to install the solver externally (not
      via conda), you can follow these steps:

      - CBC-solver: https://projects.coin-or.org/Cbc
      - GLPK-solver: http://arnab-deka.com/posts/2010/02/installing-glpk-on-a-mac/

      If you install the CBC solver via brew (highly recommended), it should
      work without additional configuration.

   .. tab-item:: Developer version

      If you would like to get access to not yet released features or features
      under development you can install the developer version. The steps are
      similar to the steps here, but INSTEAD of installing oemof.solph using
      the standard way,
      follow the instructions on :ref:`this page <contribute_label>`.

Installation test
-----------------
Test the installation and the installed solver by running the installation test
in your virtual environment:

.. code:: console

   oemof_installation_test

If the installation was successful, you will receive something like this:

.. code:: console

   *********
   Solver installed with oemof:
   glpk: working
   cplex: not working
   cbc: working
   gurobi: not working
   *********
   oemof.solph successfully installed.

as an output.
