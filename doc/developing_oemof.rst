.. _developing_oemof_label:

Developing oemof
================

Here you find important notes for developing oemof and elements within
the framework. We highly encourage you to contribute to further development 
of oemof. If you want to collaborate see description below or contact us.

.. contents::
    :depth: 1
    :local:
    :backlinks: top

Install the developer version
-----------------------------

To avoid problems make sure you have fully uninstalled previous versions of oemof. It is highly recommended to use a virtual environment. See this `virtualenv tutorial
<https://docs.python.org/3/tutorial/venv.html>`_ for more help. Afterwards two steps are necessary to install the developer version:

.. code:: bash

  git clone https://git@github.com:oemof/oemof.git
  pip3 install -e /path/to/the/repository
   
  
Newly added required packages (via PyPi) are installed by performing a manual upgrade of oemof. Therefore, run

.. code:: bash

  pip3 install --upgrade -e /path/to/the/repository
  
Documentation
-------------

See the developer version of the documentation of the dev branch at
`readthedocs.org <http://oemof.readthedocs.org/en/latest/>`_.


Collaboration with pull requests
--------------------------------

To collaborate use the pull request functionality of github.

How to create a pull request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Fork the oemof repository
* Create a pull request and describe what you will do and why
* Change, add or remove code
* Read the :ref:`style_guidlines_label` and follow them
* Add new tests according to what you have done
* Add/change the documentation (new feature, API changes ...)
* Add a whatsnew entry and your name to Contributors
* Check if all tests still work including the example tests

Tests
^^^^^

.. role:: bash(code)
   :language: bash
   
Run the following test before pushing a successful merge.

.. code:: bash

    nosetests -w "/path/to/oemof" --with-doctest
    python3 path/to/oemof/examples/oemof_full_check.py

.. _style_guidlines_label:

Style guidelines
----------------

We mostly follow standard guidelines instead of developing own rules. So if anything is not defined in this section, search for a `PEP rule <https://www.python.org/dev/peps/>`_ and follow it.

Docstrings
^^^^^^^^^^

We decided to use the style of the numpydoc docstrings. See the following link for an
`example <https://github.com/numpy/numpy/blob/master/doc/example.py>`_.


Code commenting
^^^^^^^^^^^^^^^^

Code comments are block and inline comments in the source code. They can help to understand the code and should be utilized "as much as necessary, as little as possible". When writing comments follow the PEP 0008 style guide: https://www.python.org/dev/peps/pep-0008/#comments.


PEP8 (Python Style Guide)
^^^^^^^^^^^^^^^^^^^^^^^^^

* We adhere to `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ for any code
  produced in the framework.

* We use pylint to check your code. Pylint is integrated in many IDEs and 
  Editors. `Check here <http://docs.pylint.org/ide-integration>`_ or ask the 
  maintainer of your IDE or Editor

* Some IDEs have pep8 checkers, which are very helpful, especially for python 
  beginners.

Quoted strings
^^^^^^^^^^^^^^

As there is no recommendation in the PEP rules we use double quotes for strings read by humans such as logging/error messages and single quotes for internal strings such as keys and column names. However one can deviate from this rules if the string contains a double or single quote to avoid escape characters. According to `PEP 257 <http://legacy.python.org/dev/peps/pep-0257/>`_ and numpydoc we use three double quotes for docstrings.

.. code-block:: python

    logging.info("We use double quotes for messages")
    
    my_dictionary.get('key_string')
    
    logging.warning('Use three " to quote docstrings!'  # exception to avoid escape characters

Naming Conventions
------------------

* We use plural in the code for modules if there is possibly more than one child
  class (e.g. import transformers AND NOT transformer). If there are arrays in
  the code that contain multiple elements they have to be named in plural (e.g.
  `transformers = [T1, T2,...]`).

* Please, follow the naming conventions of 
  `pylint <http://pylint-messages.wikidot.com/messages:c0103>`_

* Use talking names

  * Variables/Objects: Name it after the data they describe
    (power\_line, wind\_speed)
  * Functions/Method: Name it after what they do: **use verbs** 
    (get\_wind\_speed, set\_parameter)


Using git
--------- 

Branching model
^^^^^^^^^^^^^^^

So far we adhere mostly to the git branching model by 
`Vincent Driessen <http://nvie.com/posts/a-successful-git-branching-model/>`_.

Differences are:

* instead of the name ``origin/develop`` we call the branch ``origin/dev``.
* feature branches are named like ``features/*``
* release branches are named like ``releases/*``

Commit message
^^^^^^^^^^^^^^

Use this nice little `commit tutorial <http://chris.beams.io/posts/git-commit/>`_ to 
learn how to write a nice commit message.

Issue-Management
----------------
Section about workflow for issues is still missing (when to assign an issue with
what kind of tracker to whom etc.).

Documentation
----------------

The general implementation-independent documentation such as installation guide, flow charts, and mathematical models is done via ReStructuredText (rst). The files can be found in the folder */oemof/doc*. For further information on restructured text see: http://docutils.sourceforge.net/rst.html.


