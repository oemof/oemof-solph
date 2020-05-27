========
Overview
========

.. start-badges

**docs**

|docs| |zenodo|

**tests**

|travis| |appveyor| |requires|
|coveralls| |codecov|
|scrutinizer| |codacy| |codeclimate|

**package**

|version| |wheel| |supported-versions| |supported-implementations|
|commits-since| |commits-since-stable|

.. |docs| image:: https://readthedocs.org/projects/oemof-solph/badge/?style=flat
    :target: https://readthedocs.org/projects/oemof-solph
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/oemof/oemof-solph.svg?branch=dev
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/github/oemof/oemof-solph/branches

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/oemof/oemof-solph?branch=dev&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/oemof-developer/oemof-solph

.. |requires| image:: https://requires.io/github/oemof/oemof-solph/requirements.svg?branch=dev
    :alt: Requirements Status
    :target: https://requires.io/github/oemof/oemof-solph/requirements/?branch=dev

.. |coveralls| image:: https://coveralls.io/repos/oemof/oemof-solph/badge.svg?branch=dev&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/oemof/oemof-solph

.. |codecov| image:: https://codecov.io/gh/oemof/oemof-solph/branch/dev/graphs/badge.svg?branch=dev
    :alt: Coverage Status
    :target: https://codecov.io/github/oemof/oemof-solph

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/a6e5cb2dd2694c73895e142e4cf680d5
    :target: https://www.codacy.com/gh/oemof/oemof-solph?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=oemof/oemof-solph&amp;utm_campaign=Badge_Grade
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

.. |commits-since| image:: https://img.shields.io/github/commits-since/oemof/oemof-solph/v0.4.0b0/dev
    :alt: Commits since latest release
    :target: https://github.com/oemof/oemof-solph/compare/v0.4.0b0...dev

.. |commits-since-stable| image:: https://img.shields.io/github/commits-since/oemof/oemof-solph/v0.3.2/dev
    :alt: Commits since latest release
    :target: https://github.com/oemof/oemof-solph/compare/v0.3.2...dev

.. |zenodo| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.596235.svg
    :alt: DOI
    :target: https://doi.org/10.5281/zenodo.596235

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/quality/g/oemof/oemof-solph/dev.svg
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/oemof/oemof-solph/


.. end-badges


.. contents::
    :depth: 1
    :local:
    :backlinks: top


Introduction
============

The oemof.solph package is part of the
`Open energy modelling framework (oemof) <https://github.com/oemof/oemof>`_.
This an organisational framework to bundle tools for energy (system) modelling.
oemof-solph is a model generator for energy system modelling and optimisation.

The ``oemof.solph`` package is very often called just ``oemof`` as it was part of the
oemof meta package. Now you need to install ``oemof.solph`` separately, but
everything else is still the same.
Since v0.4.0. it is not possible to install just oemof, use
``pip install oemof.solph`` instead.

Everybody is welcome to use and/or develop oemof.solph.
Read our `'Why should I contribute' <http://oemof.readthedocs.io/en/latest/about_oemof.html#why-should-i-contribute>`_ section.

Contribution is already possible on a low level by simply fixing typos in
oemof's documentation or rephrasing sections which are unclear.
If you want to support us that way please fork the oemof repository to your own
github account and make changes as described in the github guidelines: https://guides.github.com/activities/hello-world/


Documentation
=============
The `oemof.solph documentation <https://oemof-solph.readthedocs.io/>`_ is powered by readthedocs. Use the `project site <http://readthedocs.org/projects/oemof>`_ of oemof.solph to choose the version of the documentation. Go to the `download page <http://readthedocs.org/projects/oemof/downloads/>`_ to download different versions and formats (pdf, html, epub) of the documentation.

To get the latest news visit and follow our `website <https://www.oemof.org>`_.

If you have questions regarding the use of oemof you can visit the forum at: `https://forum.openmod-initiative.org/tags/c/qa/oemof` and open a new thread if your questions hasn't been already answered.


Installation
============

If you have a working Python3 environment, use pypi to install the latest oemof version. Python >= 3.5 is recommended. Lower versions may work but are not tested.


::

    pip install oemof.solph

If you want to use the latest features, you might want to install the **developer version**. See section `'Developing oemof' <http://oemof.readthedocs.io/en/latest/developing_oemof.html>`_ for more information. The developer version is not recommended for productive use::

    pip install https://github.com/oemof/oemof-solph/archive/dev.zip

For more details, also about how to install python, if you are new to python,
have a look at the *Link zu zukünftiger oemof/oemof* section.

For running an oemof-solph optimisation model, you need to install a solver.
Following you find guidelines for the installation process for different operation systems.

.. _windows_solver_label:
.. _linux_solver_label:

Installing a solver
-------------------

There are various commercial and open-source solvers that can be used with oemof.
There are two common OpenSource solvers available (CBC, GLPK), while oemof recommends CBC (Coin-or branch and cut).
But sometimes its worth comparing the results of different solvers.
Other commercial solvers like Gurobi or Cplex can be used as well.
Have a look at the `pyomo docs <https://pyomo.readthedocs.io/en/stable/solving_pyomo_models.html#supported-solvers>`_ to learn about which solvers are supported.

**Linux**

To install the solvers have a look at the package repository of your Linux distribution or search for precompiled packages. GLPK and CBC ares available at Debian, Feodora, Ubuntu and others.

Check the solver installation by executing the test_installation example (see :ref:`check_installation_label` ).

**Windows**

 1. Download CBC (`64 <https://ampl.com/dl/open/cbc/cbc-win64.zip>`_ or `32 <https://ampl.com/dl/open/cbc/cbc-win32.zip>`_ bit)
 2. Download `GLPK (64/32 bit) <https://sourceforge.net/projects/winglpk/>`_
 3. Unpack CBC/GLPK to any folder (e.g. C:/Users/Somebody/my_programs)
 4. Add the path of the executable files of both solvers to the PATH variable using `this tutorial <http://www.computerhope.com/issues/ch000549.htm>`_
 5. Restart Windows

Check the solver installation by executing the test_installation example (see :ref:`check_installation_label` ).


**Mac OSX**

So far only the CBC solver was tested on a Mac. If you are a Mac user and are using other Solvers successfully please help us to improve this installation guide.

Please follow the installation instructions on the respective homepages for details.

CBC-solver: https://projects.coin-or.org/Cbc

GLPK-solver: http://arnab-deka.com/posts/2010/02/installing-glpk-on-a-mac/

If you install the CBC solver via brew (highly recommended), it should work without additional configuration.


Installing python3
------------------

*This section should be moved to oemof/oemof in future.*

As oemof is designed as a Phyton-module it is mandatory to have Python 3 installed.
If you are new to python, and if you do not have a working Python3 environment,
here are some links and hints for installing python depending on your operating system.
You will find many information in the world-wide-web.

**Linux**

Most Linux distributions will have Python 3 in their repository. Use the specific software management to install it.
If you are using Ubuntu/Debian try executing the following code in your terminal:

.. code:: console

  sudo apt-get install python3

You can also download different versions of Python via https://www.python.org/downloads/.

* Using Virtualenv (community driven)

Skip the steps you have already done. Check your architecture first (32/64 bit).

 1. Install virtualenv using the package management of your Linux distribution, pip install or install it from source (`see virtualenv documentation <https://virtualenv.pypa.io/en/latest/>`_)
 2. Open terminal to create and activate a virtual environment by typing:

    .. code-block:: console

       virtualenv -p /usr/bin/python3 your_env_name
       source your_env_name/bin/activate

 3. In terminal type: :code:`pip install oemof`
 4. Install a :ref:`linux_solver_label` if you want to use solph and execute the solph examples (See :ref:`check_installation_label` ) to check if the installation of the solver and oemof was successful

Warning: If you have an older version of virtualenv you should update pip :code:`pip install --upgrade pip`.

* Using Anaconda

Skip the steps you have already done. Check your architecture first (32/64 bit).

 1. Download latest `Anaconda (Linux) <https://www.anaconda.com/products/individual#Downloads>`_ for Python 3.x (64 or 32 bit)
 2. Install Anaconda

 3. Open terminal to create and activate a virtual environment by typing:

    .. code-block:: console

       conda create -n yourenvname python=3.x
       source activate yourenvname

 4. In terminal type: :code:`pip install oemof`
 5. Install a :ref:`linux_solver_label` if you want to use solph and execute the solph examples (See :ref:`check_installation_label` ) to check if the installation of the solver and oemof was successful

**Windows**

For installing python on Windows, you can for example install python using Anaconda
`Anaconda <https://www.anaconda.com/products/individual#Downloads>`_ , or using WinPython
`WinPython <http://winpython.github.io>`_.

If you are new to Python check out the `YouTube tutorial <https://www.youtube.com/watch?v=eFvoM36_szM>`_ on
how to install oemof under Windows.
It will guide you step by step through the installation process, starting
with the installation of Python using WinPython, all the way to executing your first oemof example.

It is recommended to use a virtual environment.
For Anaconda, open the 'Anaconda Prompt' to create and activate a virtual environment by typing:

.. code-block:: console

       conda create -n yourenvname python=3.x
       activate yourenvname

**Mac OSX**

If you are using brew you can simply run

.. code:: console

  brew install python3

Otherwise please refer to https://www.python.org/downloads/mac-osx/ for installation instructions.


.. _check_installation_label:

Run the installation_test file
------------------------------

Test the installation and the installed solver:

To test the whether the installation was successful simply run

.. code:: console

  oemof_installation_test

in your virtual environment.
If the installation was successful, you will get:

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


Examples
========

The linkage of specific modules of the various packages is called an
application (app) and depicts for example a concrete energy system model.
You can find a large variety of helpful examples in `oemof's example repository <https://github.com/oemof/oemof_examples>`_ on github to download or clone. The examples show optimisations of different energy systems and are supposed to help new users to understand the framework's structure. There is some elaboration on the examples in the respective repository.

You are welcome to contribute your own examples via a `pull request <https://github.com/oemof/examples/pulls>`_ or by sending us an e-mail (see `here <https://oemof.org/contact/>`_ for contact information).


Join the developers!
====================

A warm welcome to all who want to join the developers and contribute to
oemof.solph. Information on the details and how to approach us can be found
`in the documentation <https://oemof.readthedocs.io/en/latest/developing_oemof.html>`_ .


Keep in touch
=============

You can become a watcher at our `github site <https://github.com/oemof/oemof>`_, but this will bring you quite a few mails and might be more interesting for developers. If you just want to get the latest news you can follow our news-blog at `oemof.org <https://oemof.org/>`_.


Citing
======

The core ideas of oemof are described in `DOI:10.1016/j.esr.2018.07.001 <https://doi.org/10.1016/j.esr.2018.07.001>`_ (preprint at `arXiv:1808.0807 <http://arxiv.org/abs/1808.08070v1>`_). To allow citing specific versions of oemof, we use the zenodo project to get a DOI for each version.


License
=======

Copyright (c) 2019 oemof developer group

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


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

