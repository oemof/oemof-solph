.. SPDX-FileCopyrightText: oemof e.V. and contributors
..
.. SPDX-License-Identifier: MIT

.. _installation_and_setup_label:

######################
Installation and setup
######################

Here you find guidelines for the installation process for various
operating systems. `oemof.solph` is a Python package, thus it requires you to
have Python 3 installed. On top of that, you need a solver to use `oemof.solph`.

There are several solvers that can work with `oemof.solph`, both open source and
commercial. Two open source solvers are widely used (`HiGHS` and `CBC`),
`oemof.solph`` defaults to `CBC` (Coin-or branch and cut). It may be useful to compare
results of different solvers to see which performs best. Commercial
solvers, like Gurobi or Cplex, are also options. Have a look at the
`pyomo docs <https://pyomo.readthedocs.io/en/stable/api/pyomo.solvers.plugins.solvers.html>`__
to learn about which solvers are supported.

We recommend installing `oemof.solph` within a virtual Python environment and not into the base,
system-wide Python installation.

.. tab-set::

   .. tab-item:: Using conda

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


   .. tab-item:: Using Python venv

      With `Python <http://python.org/>`__ installed, you can use virtualenv
      to manage virtual environments. Open terminal to create and activate
      a virtual environment by typing:

      .. code-block:: console

         python -m venv /path/to/desired/oemof-solph-env
         source /path/to/desired/oemof-solph-env/bin/activate



When you are have a virtual environment activated, you can install
`oemof.solph` and the open source solver HiGHS and CBC using:

.. code-block:: console

   pip install oemof.solph[solver]

If you want to use a solver you installed in a different way,
just omit the :code:`[solver]`.


Installation test
-----------------
Test the installation and the installed solver by running the installation test
in your virtual environment:

.. code:: console

   oemof_installation_test

If the installation was successful, you will receive something like this:

.. code:: console

   ***********************************
   Solver installed with oemof.solph:

   cbc: installed and working
   glpk: not installed/ not working
   gurobi: not installed/ not working
   cplex: not installed/ not working
   scip: not installed/ not working
   highs: installed and working

   ***********************************
   oemof.solph successfully installed.
   ***********************************

