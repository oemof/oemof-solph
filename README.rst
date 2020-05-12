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
    :target: https://travis-ci.org/oemof/oemof-solph

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

.. |version| image:: https://img.shields.io/pypi/v/oemof.svg
    :alt: PyPI Package latest release
..    :target: https://pypi.org/project/oemof-solph

.. |wheel| image:: https://img.shields.io/pypi/wheel/oemof.svg
    :alt: PyPI Wheel
..    :target: https://pypi.org/project/oemof

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/oemof.svg
    :alt: Supported versions

..    :target: https://pypi.org/project/oemof-solph

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/oemof.svg
    :alt: Supported implementations

..     :target: https://pypi.org/project/oemof

.. |commits-since| image:: https://img.shields.io/github/commits-since/oemof/oemof-solph/v0.3.2/dev
    :alt: Commits since latest release
    :target: https://github.com/oemof/oemof-solph/compare/v0.3.2...dev

.. |zenodo| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.596235.svg
    :alt: DOI
    :target: https://doi.org/10.5281/zenodo.596235

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/quality/g/oemof/oemof-solph/dev.svg
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/oemof/oemof-solph/


.. end-badges

A model generator for energy system modelling and optimisation.

Everybody is welcome to use and/or develop oemof.solph. Read our `'Why should I contribute' <http://oemof.readthedocs.io/en/latest/about_oemof.html#why-should-i-contribute>`_ section.

Contribution is already possible on a low level by simply fixing typos in oemof's documentation or rephrasing sections which are unclear. If you want to support us that way please fork the oemof repository to your own github account and make changes as described in the github guidelines: https://guides.github.com/activities/hello-world/

.. contents::
    :depth: 1
    :local:
    :backlinks: top

Installation
============

If you have a working Python3 environment, use pypi to install the latest oemof version. Python >= 3.5 is recommended. Lower versions may work but are not tested.


::

    pip install oemof.solph

If you want to use the latest features, you might want to install the **developer version**. See section `'Developing oemof' <http://oemof.readthedocs.io/en/latest/developing_oemof.html>`_ for more information. The developer version is not recommended for productive use::

    pip install https://github.com/oemof/oemof-solph/archive/dev.zip

For more details have a look at the `'Installation and setup' <http://oemof-solph.readthedocs.io/en/latest/installation_and_setup.html>`_ section.


Documentation
=============
The `oemof.solph documentation <https://oemof-solph.readthedocs.io/>`_ is powered by readthedocs. Use the `project site <http://readthedocs.org/projects/oemof>`_ of oemof.solph to choose the version of the documentation. Go to the `download page <http://readthedocs.org/projects/oemof/downloads/>`_ to download different versions and formats (pdf, html, epub) of the documentation.

To get the latest news visit and follow our `website <https://www.oemof.org>`_.

If you have questions regarding the use of oemof you can visit the forum at: `https://forum.openmod-initiative.org/tags/c/qa/oemof` and open a new thread if your questions hasn't been already answered.

Open energy modelling framework (oemof)
=======================================

The oemof.solph package is part of the
`Open energy modelling framework (oemof) <https://github.com/oemof/oemof>`_.
This an organisational framework to bundle tools for energy (system) modelling.


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


Citing oemof
============

The core ideas of oemof are described in `DOI:10.1016/j.esr.2018.07.001 <https://doi.org/10.1016/j.esr.2018.07.001>`_ (preprint at `arXiv:1808.0807 <http://arxiv.org/abs/1808.08070v1>`_). To allow citing specific versions of oemof, we use the zenodo project to get a DOI for each version.


Free software: MIT license
==========================

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

