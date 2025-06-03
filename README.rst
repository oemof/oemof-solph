
|tox-pytest| |tox-checks| |appveyor| |coveralls| |codecov|

|scrutinizer| |codacy| |codeclimate|

|wheel| |packaging| |supported-versions|

|docs| |zenodo|

|version| |commits-since| |chat|


------------------------------

.. |tox-pytest| image:: https://github.com/oemof/oemof-solph/actions/workflows/tox_pytests.yml/badge.svg?branch=dev
     :target: https://github.com/oemof/oemof-solph/actions?query=workflow%3A%22tox+checks%22

.. |tox-checks| image:: https://github.com/oemof/oemof-solph/actions/workflows/tox_checks.yml/badge.svg?branch=dev
     :target: https://github.com/oemof/oemof-solph/actions?query=workflow%3A%22tox+checks%22

.. |packaging| image:: https://github.com/oemof/oemof-solph/actions/workflows/packaging.yml/badge.svg
     :target: https://github.com/oemof/oemof-solph/actions?query=workflow%3Apackaging

.. |docs| image:: https://readthedocs.org/projects/oemof-solph/badge/?style=flat
    :target: https://readthedocs.org/projects/oemof-solph
    :alt: Documentation Status

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/oemof/oemof-solph?branch=dev&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/oemof-developer/oemof-solph

.. |coveralls| image:: https://coveralls.io/repos/oemof/oemof-solph/badge.svg?branch=dev&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/github/oemof/oemof-solph

.. |codecov| image:: https://codecov.io/gh/oemof/oemof-solph/branch/dev/graphs/badge.svg?branch=dev
    :alt: Coverage Status
    :target: https://codecov.io/gh/oemof/oemof-solph

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/a6e5cb2dd2694c73895e142e4cf680d5
    :target: https://app.codacy.com/gh/oemof/oemof-solph/dashboard
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/oemof/oemof-solph/badges/gpa.svg
   :target: https://codeclimate.com/github/oemof/oemof-solph
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/oemof.solph.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/oemof.solph

.. |wheel| image:: https://img.shields.io/pypi/wheel/oemof.solph.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/oemof.solph

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/oemof.solph.svg
    :alt: Supported versions
    :target: https://pypi.org/project/oemof.solph

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/oemof.solph.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/oemof.solph

.. |commits-since| image:: https://img.shields.io/github/commits-since/oemof/oemof-solph/latest/dev
    :alt: Commits since latest release
    :target: https://github.com/oemof/oemof-solph/compare/master...dev

.. |zenodo| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.596235.svg
    :alt: Zenodo DOI
    :target: https://doi.org/10.5281/zenodo.596235

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/quality/g/oemof/oemof-solph/dev.svg
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/oemof/oemof-solph/

.. |chat| image:: https://img.shields.io/badge/chat-oemof:matrix.org-%238ADCF7
     :alt: matrix-chat
     :target: https://matrix.to/#/#oemof:matrix.org


.. figure:: https://raw.githubusercontent.com/oemof/oemof-solph/492e3f5a0dda7065be30d33a37b0625027847518/docs/_logo/logo_oemof_solph_FULL.svg
    :align: center

------------------------------

===========
oemof.solph
===========

**A model generator for energy system modelling and optimisation (LP/MILP)**

.. contents::
    :depth: 2
    :local:
    :backlinks: top


Introduction
============

The oemof.solph package is part of the
`Open energy modelling framework (oemof) <https://github.com/oemof/oemof>`_.
This is an organisational framework to bundle tools for energy (system) modelling.
oemof-solph is a model generator for energy system modelling and optimisation.

The package ``oemof.solph`` is very often called just ``oemof``.
This is because installing the ``oemof`` meta package was once the best way to get ``oemof.solph``.
Notice that you should prefeably install ``oemof.solph`` instead of ``oemof``
if you want to use ``solph``.


Everybody is welcome to use and/or develop oemof.solph.
Read our `contribution <https://oemof.readthedocs.io/en/latest/contributing.html>`_ section.

Contribution is already possible on a low level by simply fixing typos in
oemof's documentation or rephrasing sections which are unclear.
If you want to support us that way please fork the oemof-solph repository to your own
GitHub account and make changes as described in the `github guidelines <https://docs.github.com/en/get-started/quickstart/hello-world>`_

If you have questions regarding the use of oemof including oemof.solph you can visit the openmod forum (`tag oemof <https://forum.openmod-initiative.org/tags/c/qa/oemof>`_ or `tag oemof-solph <https://forum.openmod-initiative.org/tags/c/qa/oemof-solph>`_) and open a new thread if your questions hasn't been already answered.

Keep in touch! - You can become a watcher at our `github site <https://github.com/oemof/oemof>`_,
but this will bring you quite a few mails and might be more interesting for developers.
If you just want to get the latest news, like when is the next oemof meeting,
you can follow our news-blog at `oemof.org <https://oemof.org/>`_.

Documentation
=============
The `oemof.solph documentation <https://oemof-solph.readthedocs.io/>`_ is powered by readthedocs. Use the `project site <https://readthedocs.org/projects/oemof>`_ of oemof.solph to choose the version of the documentation. Go to the `download page <https://readthedocs.org/projects/oemof/downloads/>`_ to download different versions and formats (pdf, html, epub) of the documentation.

Installation
============


If you have a working Python installation, use pypi to install the latest version of oemof.solph.
Python >= 3.8 is recommended. Lower versions may work but are not tested.

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
Have a look at the `pyomo docs <https://pyomo.readthedocs.io/en/stable/api/pyomo.solvers.plugins.solvers.html>`_
to learn about which solvers are supported.

Check the solver installation by executing the test_installation example below (see section Installation Test).

**Linux**

To install the solvers have a look at the package repository of your Linux distribution or search for precompiled packages. GLPK and CBC ares available at Debian, Feodora, Ubuntu and others.

**Windows**

 1. Download `CBC <https://github.com/coin-or/Cbc/releases>`_
 2. Download `GLPK (64/32 bit) <https://sourceforge.net/projects/winglpk/>`_
 3. Unpack CBC/GLPK to any folder (e.g. C:/Users/Somebody/my_programs)
 4. Add the path of the executable files of both solvers to the PATH variable (cf. `setting environment variables as user <https://learn.microsoft.com/en-us/troubleshoot/windows-client/performance/cannot-modify-user-environment-variables-system-properties>`_)
 5. Restart Windows

Check the solver installation by executing the test_installation example (see the `Installation test` section).


**Mac OSX**

Please follow the installation instructions on the respective homepages for details.

CBC-solver: https://github.com/coin-or/Cbc

GLPK-solver: http://arnab-deka.com/posts/2010/02/installing-glpk-on-a-mac/

If you install the CBC solver via brew (highly recommended), it should work without additional configuration.


**conda**

The CBC-solver can also be installed in a `conda` environment. Please note, that it is highly recommended to `use pip after conda <https://www.anaconda.com/blog/using-pip-in-a-conda-environment>`_, so:

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

Contributing
============

A warm welcome to all who want to join the developers and contribute to
oemof.solph.

Information on the details and how to approach us can be found
`in the oemof documentation <https://oemof.readthedocs.io/en/latest/contributing.html>`_ .

Citing
======

For explicitly citing solph, you might want to refer to
`DOI:10.1016/j.simpa.2020.100028 <https://doi.org/10.1016/j.simpa.2020.100028>`_,
which gives an overview over the capabilities of solph.
The core ideas of oemof as a whole are described in
`DOI:10.1016/j.esr.2018.07.001 <https://doi.org/10.1016/j.esr.2018.07.001>`_
(preprint at `arXiv:1808.0807 <https://arxiv.org/abs/1808.08070v1>`_).
To allow citing specific versions, we use the zenodo project to get a DOI for each version.

Example Applications
====================

The combination of specific modules (often including other packages) is called an
application (app). For example, it can depict a concrete energy system model.
You can find a large variety of helpful examples in the documentation.
The examples show the optimisation of different energy systems and are supposed
to help new users to understand the framework's structure.
Please make sure the example you are looking at is created for the version
of solph you have installed.

You are welcome to contribute your own examples via a `pull request <https://github.com/oemof/oemof-solph/pulls>`_
or by e-mailing us (see `here <https://oemof.org/contact/>`_ for contact information).

License
=======

Copyright (c) oemof developer group

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
