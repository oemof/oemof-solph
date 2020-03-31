.. _developing_oemof_label:

Developing oemof
================

Oemof is developed collaboratively and therefore driven by its community. While advancing
as a user of oemof, you may find situations that demand solutions that are not readily
available. In this case, your solution may be of help to other users as well. Contributing
to the development of oemof is good for two reasons: Your code may help others and you
increase the quality of your code through the review of other developers. Read also these
arguments on
`why you should contribute <http://oemof.readthedocs.io/en/latest/about_oemof.html?highlight=why%20should#why-should-i-contribute>`_.

A first step to get involved with development can be contributing a component that is
not part of the current version that you defined for your energy system. We have a module
oemof.solph.custom that is dedicated to collect custom components created by users. Feel free
to start a pull request and contribute.

Another way to join the developers and learn how to contribute is to help improve the documentation.
If you find that some part could be more clear or if you even find a mistake, please
consider fixing it and creating a pull request.

New developments that provide new functionality may enter oemof at different locations.
Please feel free to discuss contributions by creating a pull request or an issue.

In the following you find important notes for developing oemof and elements within
the framework. On whatever level you may want to start, we highly encourage you
to contribute to the further development of oemof. If you want to collaborate see 
description below or contact us.

.. contents::
    :depth: 1
    :local:
    :backlinks: top

Install the developer version
-----------------------------

To avoid problems make sure you have fully uninstalled previous versions of oemof. It is highly recommended to use a virtual environment. See this `virtualenv tutorial
<https://docs.python.org/3/tutorial/venv.html>`_ for more help. Afterwards you have
to clone the repository. See the `github documentation <https://help.github.com/articles/cloning-a-repository/>`_ to learn how to clone a repository.
Now you can install the cloned repository using pip:

.. code:: bash

  pip install -e /path/to/the/repository
   
  
Newly added required packages (via PyPi) can be installed by performing a manual
 upgrade of oemof. In that case run:

.. code:: bash

  pip install --upgrade -e /path/to/the/repository
  
Contribute to the documentation
-------------------------------

If you want to contribute by improving the documentation (typos, grammar, comprehensibility), please use the developer version of the dev branch at
`readthedocs.org <http://oemof.readthedocs.org/en/latest/>`_.
Every fixed typo helps.

Contribute to new components
----------------------------
                                                                                                                                                       
You can develop a new component according to your needs. Therefore you can use the module oemof.solph.custom which collects custom components created by users and lowers the entry barrier for contributing.                
                                 
Your code should fit to the :ref:`style_guidlines_label` and the docstring should be complete and hold the equations used in the constraints. But there are several steps you do not necessarily need to fulfill when contributing to oemof.solph.custom: you do not need to meet the :ref:`naming_conventions_label`. Also compatiblity to the results-API must not be guaranteed. Further you do not need to test your components or adapt the documentation. These steps are all necessary once your custom component becomes a constant part of oemof (oemof.solph.components) and are described here: :ref:`coding_requirements_label`. But in the first step have a look at existing custom components created by other users in oemof.solph.custom and easily create your own if you need.

Collaboration with pull requests
--------------------------------

To collaborate use the pull request functionality of github as described here: https://guides.github.com/activities/hello-world/

How to create a pull request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Fork the oemof repository to your own github account.
* Change, add or remove code.
* Commit your changes.
* Create a pull request and describe what you will do and why. Please use the pull request template we offer. It will be shown to you when you click on "New pull request".
* Wait for approval.

.. _coding_requirements_label:  

Generally the following steps are required when changing, adding or removing code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Read the :ref:`style_guidlines_label` and :ref:`naming_conventions_label` and follow them
* Add new tests according to what you have done
* Add/change the documentation (new feature, API changes ...)
* Add a whatsnew entry and your name to Contributors
* Check if all :ref:`tests_label` still work.

.. _tests_label:

Tests
-----

.. role:: bash(code)
   :language: bash
   
Run the following test before pushing a successful merge.

.. code:: bash

    nosetests -w "/path/to/oemof" --with-doctest

.. _style_guidlines_label:

Issue-Management
----------------

A good way for communication with the developer group are issues. If you
find a bug, want to contribute an enhancement or have a question on a specific problem
in development you want to discuss, please create an issue:

* describing your point accurately
* using the list of category tags
* addressing other developers

If you want to address other developers you can use @name-of-developer, or
use e.g. @oemof-solph to address a team. `Here <https://github.com/orgs/oemof/teams>`_
you can find an overview over existing teams on different subjects and their members.

Look at the existing issues to get an idea on the usage of issues.

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

.. _naming_conventions_label:

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
 

Documentation
----------------

The general implementation-independent documentation such as installation guide, flow charts, and mathematical models is done via ReStructuredText (rst). The files can be found in the folder */oemof/doc*. For further information on restructured text see: http://docutils.sourceforge.net/rst.html.


How to become a member of oemof
-------------------------------

And last but not least,
`here you will find <https://github.com/oemof/organisation/issues/26>`_
all information about how to become a member of the oemof organisation and of developer teams.

