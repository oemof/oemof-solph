Developer Notes
================

Here we gather important notes for the developing of oemof and elements within
the framework.

We highly encourage you to contribute to further development of oemof. If you want to collaborate see description below or contact us.

Install the developer version
-----------------------------

To install the developer version two steps are necessary:

.. code:: bash

  git clone git@github.com:oemof/oemof.git
  sudo pip3 install -e /path/to/the/repository
  
Documentation
-------------

See the documentation of the dev branch at
`readthedocs.org <http://oemof.readthedocs.org/en/latest/>`_.


Collaboration
-------------

We use the collaboration features from Github, see https://github.com/oemof.


Style guidelines
----------------

We mostly follow standard guidelines instead of developing own rules.

* `Docstring example <https://github.com/numpy/numpy/blob/master/doc/example.py>`_

PEP8 (Python Style Guide)
^^^^^^^^^^^^^^^^^^^^^^^^^

* We adhere to `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ for any code
  produced in the framework.

* We use pylint to check your code. Pylint is integrated in many IDEs and Editors. `Check here <http://docs.pylint.org/ide-integration>`_ or ask the maintainer of your IDE or Editor

* Some IDEs have pep8 checkers, which are very helpful, especially for python beginners.

Quoted strings
^^^^^^^^^^^^^^

For strings we use double quotes if possible.

.. code-block:: python

    info_msg = "We use double quotes for strings"
    info_msg = 'This is a string where we need to use "single" quotes'

Naming Conventions
------------------

* We use plural in the code for modules if there is possibly more than one child class (e.g. import transformers AND NOT transformer). If there are arrays in the code that contain multiple elements they have to be named in plural (e.g. `transformers = [T1, T2,...]`).

* Please, follow the naming conventions of `pylint <http://pylint-messages.wikidot.com/messages:c0103>`_

* Use talking names

  * Variables/Objects: Name it after the data they describe (power\_line, wind\_speed)
  * Functions/Method: Name it after what they do: **use verbs** (get\_wind\_speed, set\_parameter)


Using git
--------- 

Branching model
^^^^^^^^^^^^^^^

So far we adhere mostly to the git branching model by `Vincent Driessen <http://nvie.com/posts/a-successful-git-branching-model/>`_.

The only difference is to use a different name for the branch origin/develop 
("main branch where the source code of HEAD always reflects a state with the 
latest delivered development changes for the next release. Some would call this 
the integration branch."). The name we use is origin/dev.

Commit message
^^^^^^^^^^^^^^

Use this nice little `tutorial <http://chris.beams.io/posts/git-commit/>`_ to learn how to write a nice commit message.

Issue-Management
----------------
Section about workflow for issues is still missing (when to assign an issue with
what kind of tracker to whom etc.).

