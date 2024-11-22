============
Installation
============

If you have a working Python installation, use pypi to install the latest version of oemof.solph.
Python >= 3.9 is recommended. Lower versions may work but are not tested.

We highly recommend to use virtual environments.
Please refer to the documentation of your Python distribution (e.g. Anaconda,
Micromamba, or the version of Python that came with your Linux installation)
to learn how to set up and use virtual environments.

::

    (venv) pip install oemof.solph

If you want to use the latest features, you might want to install the **developer version**. The developer version is not recommended for productive use::

    (venv) pip install https://github.com/oemof/oemof-solph/archive/dev.zip


For running an oemof-solph optimisation model, you need to install a solver.
Following you will find guidelines for the installation process for different operating systems.

.. _windows_solver_label:
.. _linux_solver_label:

Installing a solver
-------------------

There are several solvers that can work with oemof, both open source and commercial.
Two open source solvers are widely used (CBC and GLPK), but oemof suggests CBC (Coin-or branch and cut).
It may be useful to compare results of different solvers to see which performs best.
Other commercial solvers, like Gurobi or Cplex, are also options.
Have a look at the `pyomo docs <https://pyomo.readthedocs.io/en/stable/solving_pyomo_models.html#supported-solvers>`_ to learn about which solvers are supported.

Check the solver installation by executing the test_installation example below (see section Installation Test).

**Linux**

To install the solvers have a look at the package repository of your Linux distribution or search for precompiled packages. GLPK and CBC ares available at Debian, Feodora, Ubuntu and others.

**Windows**

 1. Download `CBC <https://github.com/coin-or/Cbc/releases>`_
 2. Download `GLPK (64/32 bit) <https://sourceforge.net/projects/winglpk/>`_
 3. Unpack CBC/GLPK to any folder (e.g. C:/Users/Somebody/my_programs)
 4. Add the path of the executable files of both solvers to the PATH variable using `this tutorial <https://www.computerhope.com/issues/ch000549.htm>`_
 5. Restart Windows

Check the solver installation by executing the test_installation example (see the `Installation test` section).


**Mac OSX**

Please follow the installation instructions on the respective homepages for details.

CBC-solver: https://projects.coin-or.org/Cbc

GLPK-solver: http://arnab-deka.com/posts/2010/02/installing-glpk-on-a-mac/

If you install the CBC solver via brew (highly recommended), it should work without additional configuration.


**conda**

Provided you are using a Linux or MacOS, the CBC-solver can also be installed in a `conda` environment. Please note, that it is highly recommended to `use pip after conda <https://www.anaconda.com/blog/using-pip-in-a-conda-environment>`_, so:

.. code:: console

    (venv) conda install -c conda-forge coincbc
    (venv) pip install oemof.solph


.. _check_installation_label:

Installation test
-----------------

Test the installation and the installed solver by running the installation test
in your virtual environment:

.. code:: console

  (venv) oemof_installation_test

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
