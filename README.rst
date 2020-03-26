========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls| |codecov|
        | |scrutinizer| |codacy| |codeclimate|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/oemof.solph/badge/?style=flat
    :target: https://readthedocs.org/projects/oemofsolph
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/oemof/oemof.solph.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/oemof/oemof.solph

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/oemof/oemof.solph?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/oemof/oemof.solph

.. |requires| image:: https://requires.io/github/oemof/oemof.solph/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/oemof/oemof.solph/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/oemof/oemof.solph/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/oemof/oemof.solph

.. |codecov| image:: https://codecov.io/gh/oemof/oemof.solph/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/oemof/oemof.solph

.. |codacy| image:: https://img.shields.io/codacy/grade/CODACY_PROJECT_ID.svg
    :target: https://www.codacy.com/app/oemof/oemof.solph
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/oemof/oemof.solph/badges/gpa.svg
   :target: https://codeclimate.com/github/oemof/oemof.solph
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

.. |commits-since| image:: https://img.shields.io/github/commits-since/oemof/oemof.solph/v0.4.0.dev0.svg
    :alt: Commits since latest release
    :target: https://github.com/oemof/oemof.solph/compare/v0.4.0.dev0...master


.. |scrutinizer| image:: https://img.shields.io/scrutinizer/quality/g/oemof/oemof.solph/master.svg
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/oemof/oemof.solph/


.. end-badges

A model generator for energy system modelling and optimisation.

* Free software: MIT license

Installation
============

::

    pip install oemof.solph

You can also install the in-development version with::

    pip install https://github.com/oemof/oemof.solph/archive/master.zip


Documentation
=============


https://oemof-solph.readthedocs.io/


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
