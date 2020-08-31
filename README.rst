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
|commits-since|

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

.. |commits-since| image:: https://img.shields.io/github/commits-since/oemof/oemof-solph/v0.4.1/dev
    :alt: Commits since latest release
    :target: https://github.com/oemof/oemof-solph/compare/v0.4.1...dev

.. |zenodo| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.596235.svg
    :alt: DOI
    :target: https://doi.org/10.5281/zenodo.596235

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/quality/g/oemof/oemof-solph/dev.svg
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/oemof/oemof-solph/


.. end-badges


.. contents::
    :depth: 2
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
Read our `contribution <https://oemof.readthedocs.io/en/latest/developing_oemof.html>`_ section.

Contribution is already possible on a low level by simply fixing typos in
oemof's documentation or rephrasing sections which are unclear.
If you want to support us that way please fork the oemof repository to your own
github account and make changes as described in the github guidelines: https://guides.github.com/activities/hello-world/

If you have questions regarding the use of oemof you can visit the forum at `openmod-initiative.org <https://forum.openmod-initiative.org/tags/c/qa/oemof>`_ and open a new thread if your questions hasn't been already answered.

Keep in touch! - You can become a watcher at our `github site <https://github.com/oemof/oemof>`_,
but this will bring you quite a few mails and might be more interesting for developers.
If you just want to get the latest news, like when is the next oemof meeting,
you can follow our news-blog at `oemof.org <https://oemof.org/>`_.

Documentation
=============
The `oemof.solph documentation <https://oemof-solph.readthedocs.io/>`_ is powered by readthedocs. Use the `project site <http://readthedocs.org/projects/oemof>`_ of oemof.solph to choose the version of the documentation. Go to the `download page <http://readthedocs.org/projects/oemof/downloads/>`_ to download different versions and formats (pdf, html, epub) of the documentation.


.. _installation_label:

Installation
============

If you have a working Python3 environment, use pypi to install the latest oemof version. Python >= 3.6 is recommended. Lower versions may work but are not tested.


::

    pip install oemof.solph

If you want to use the latest features, you might want to install the **developer version**. See section `'Developing oemof' <http://oemof.readthedocs.io/en/latest/developing_oemof.html>`_ for more information. The developer version is not recommended for productive use::

    pip install https://github.com/oemof/oemof-solph/archive/dev.zip


For running an oemof-solph optimisation model, you need to install a solver.
Following you will find guidelines for the installation process for different operation systems.

.. _windows_solver_label:
.. _linux_solver_label:

Installing a solver
-------------------

There are various commercial and open-source solvers that can be used with oemof.
There are two common OpenSource solvers available (CBC, GLPK), while oemof recommends CBC (Coin-or branch and cut).
But sometimes its worth comparing the results of different solvers.
Other commercial solvers like Gurobi or Cplex can be used as well.
Have a look at the `pyomo docs <https://pyomo.readthedocs.io/en/stable/solving_pyomo_models.html#supported-solvers>`_ to learn about which solvers are supported.

Check the solver installation by executing the test_installation example below (section `Installation test`).

**Linux**

To install the solvers have a look at the package repository of your Linux distribution or search for precompiled packages. GLPK and CBC ares available at Debian, Feodora, Ubuntu and others.

**Windows**

 1. Download CBC (`64 <https://ampl.com/dl/open/cbc/cbc-win64.zip>`_ or `32 <https://ampl.com/dl/open/cbc/cbc-win32.zip>`_ bit)
 2. Download `GLPK (64/32 bit) <https://sourceforge.net/projects/winglpk/>`_
 3. Unpack CBC/GLPK to any folder (e.g. C:/Users/Somebody/my_programs)
 4. Add the path of the executable files of both solvers to the PATH variable using `this tutorial <http://www.computerhope.com/issues/ch000549.htm>`_
 5. Restart Windows

Check the solver installation by executing the test_installation example (see the `Installation test` section).


**Mac OSX**

Please follow the installation instructions on the respective homepages for details.

CBC-solver: https://projects.coin-or.org/Cbc

GLPK-solver: http://arnab-deka.com/posts/2010/02/installing-glpk-on-a-mac/

If you install the CBC solver via brew (highly recommended), it should work without additional configuration.


.. _check_installation_label:

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

Contributing
============

A warm welcome to all who want to join the developers and contribute to
oemof.solph. Information on the details and how to approach us can be found
`in the documentation <https://oemof.readthedocs.io/en/latest/developing_oemof.html>`_ .

Citing
======

The core ideas of oemof are described in `DOI:10.1016/j.esr.2018.07.001 <https://doi.org/10.1016/j.esr.2018.07.001>`_ (preprint at `arXiv:1808.0807 <http://arxiv.org/abs/1808.08070v1>`_). To allow citing specific versions of oemof, we use the zenodo project to get a DOI for each version.


.. _solph_examples_label:

Examples
========

The linkage of specific modules of the various packages is called an
application (app) and depicts for example a concrete energy system model.
You can find a large variety of helpful examples in `oemof's example repository <https://github.com/oemof/oemof-examples>`_ on github to download or clone.
The examples show optimisations of different energy systems and are supposed
to help new users to understand the framework's structure.
There is some elaboration on the examples in the respective repository.
The repository has sections for each major release.

You are welcome to contribute your own examples via a `pull request <https://github.com/oemof/oemof-examples/pulls>`_ or by sending us an e-mail (see `here <https://oemof.org/contact/>`_ for contact information).

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
