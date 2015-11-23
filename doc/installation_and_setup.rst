~~~~~~~~~~~~~~~~~~~~~~
Installation and setup
~~~~~~~~~~~~~~~~~~~~~~

.. contents::

Introduction
~~~~~~~~~~~~
In order to use oemof some software installations are required. In the following you find guidelines for the installation process according to different operation systems. 

Linux
~~~~~

If you have Python 3 installed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As oemof is designed as a Phyton-module it is mandatory to have Python 3 installed. If you already have Python 3 you can install oemof by using pip and run the following code in your terminal:

.. code:: console

  pip3 install oemof


If you do not have Python 3 installed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are different ways to install Python on your system. 
One way is to install Python 3 through the Linux repositories. If you are using Ubuntu try executing the follwoing code in your terminal: 

.. code:: console

  sudo apt-get install python3


Otherwise you can download different versions of Python via https://www.python.org/downloads/

To be able to install additional Python packages an installer program is needed. The prefered installer is pip which is included by default in the installation of Python 3.4 and later versions.
To install pip for earlier Python versions refer to https://packaging.python.org/en/latest/installing/#install-pip-setuptools-and-wheel


Required Python packages
^^^^^^^^^^^^^^^^^^^^^^^^

In order to use oemof different Python packages are required. The following table defines which packages are needed for specific libraries: 

+------------+------------+-----------+-----------+-----------+
| Packages   | solph      | outputlib |demandlib  |example_1  |
+============+============+===========+===========+===========+
| matplotlib |            |     x     |           |           |
+------------+------------+-----------+-----------+-----------+
| pandas     |            |           |     x     |     x     | 
+------------+------------+-----------+-----------+-----------+
| numpy      |            |           |           |     x     |
+------------+------------+-----------+-----------+-----------+
| pyomo      |     x      |           |           |           |
+------------+------------+-----------+-----------+-----------+
| ...        |            |           |           |           |
+------------+------------+-----------+-----------+-----------+

Information on how to install Python modules can be found here: https://docs.python.org/3/installing/index.html 


Solver
^^^^^^

The installation of a proper solver is mandatory. There are different posibilities of commercial and open-source solvers that can be used with oemof. 
A recommandable open-source solver is Cbc (Coin-or branch and cut). 
See the CBC wiki for download and installation instructions: https://projects.coin-or.org/Cbc 


Windows
~~~~~~~

If you have Python 3 installed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you do not have Python 3 installed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To install Python 3 download the latest Python release for Windows from https://www.python.org/downloads/windows/
You find a documentation of the installation process on https://docs.python.org/3/using/windows.html
If you install Python 3.4 or later the installer program pip, which is needed for the installation of additional Python packages, is already included. For further information on pip have a look here: https://packaging.python.org/en/latest/installing/#install-pip-setuptools-and-wheel

Required Python packages
^^^^^^^^^^^^^^^^^^^^^^^^

The required Python packages for oemof, as they are described above in the Linux-section, need to be installed to run oemof. Information on the installation process of additional Python packages under Windows can be found here: https://docs.python.org/3/installing/

Solver
^^^^^^



Mac OS
~~~~~~~

If you have Python 3 installed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you do not have Python 3 installed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Required Python packages
^^^^^^^^^^^^^^^^^^^^^^^^


