Developer Notes
================

Here we gather important notes for the developing of oemof and elements within
the framework.

We highly encourage you to contribute to further development of oemof. If you 
want to collaborate see description below or contact us.

Install the developer version
-----------------------------

To install the developer version two steps are necessary:

.. code:: bash

  git clone git@github.com:oemof/oemof.git
  sudo pip3 install -e /path/to/the/repository
  
Newly added required packages (via PyPi) are installed by performing a manual upgrade of oemof. Therefore, run

.. code:: bash

  sudo pip3 install --upgrade -e /path/to/the/repository
  
Documentation
-------------

See the developer version of the documentation of the dev branch at
`readthedocs.org <http://oemof.readthedocs.org/en/latest/>`_.


Collaboration with pull requests
--------------------------------

To collaborate use the pull request functionality of github.

How to create a pull request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* ...
* ...
* Tests must run, see ...
* Name the related team within the title of the pull request, like "solph: pull request for new feature within solph".
* Assign a team member.

Pull request workflow and merging rules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
We have the following workflow for revising and merging pull requests.

After creating a pull request time is running as follows:

* Profound changes: team members have **15 workdays** for commenting, revising and merging; afterwards consensus (which includes a silent consensus) with the right to merge (only for team members)
* New features: team members have **10 workdays** for commenting, revising and merging; afterwards consensus (which includes a silent consensus) with the right to merge (only for team members)
* Large substantial bug fix: four-eyes-principle (pull request needed)
* Small bug fix: decision by oneself (pull request not needed)
* Typos: fix directly in dev branch (fast forward allowed)
 
Please be aware: only team members have the right to merge pull requests into the current dev branch.

Tests
^^^^^
* ...
* ...

Style guidelines
----------------

We mostly follow standard guidelines instead of developing own rules. So if anything is not defined in this section, search for a `PEP rule <https://www.python.org/dev/peps/>`_ and follow it.

Docstrings
^^^^^^^^^^

We decided to use the style of the numpydoc docstrings. See the following link for an
`example <https://github.com/numpy/numpy/blob/master/doc/example.py>`_.

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

Use this nice little `tutorial <http://chris.beams.io/posts/git-commit/>`_ to 
learn how to write a nice commit message.


Testing
-------

We use nosetests for testing. Make sure that all tests are successfull before
merging back into the ``dev``.

.. code:: bash

    cd /path/to/oemof/
    nosetests3 --with-doctest           # or
    nosetests3 --with-doctest --rednose # if you like it


Issue-Management
----------------
Section about workflow for issues is still missing (when to assign an issue with
what kind of tracker to whom etc.).

