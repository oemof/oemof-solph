######################
Installation and setup
######################


Introduction
============
Following you find guidelines for the installation process for different operation systems. 

Linux
======

If you have Python 3 installed
---------------------------------

As oemof is designed as a Phyton-module it is mandatory to have Python 3 installed. If you already have Python 3 you can install oemof by using pip. Run the following code in your terminal:

.. code:: console

  sudo pip3 install oemof-base

If you do not yet have pip installed, see section "Required Python packages" below for further help.

If you do not have Python 3 installed
---------------------------------------

There are different ways to install Python on your system. 
One way is to install Python 3 through the Linux repositories. If you are using Ubuntu try executing the following code in your terminal: 

.. code:: console

  sudo apt-get install python3


Otherwise you can download different versions of Python via https://www.python.org/downloads/.


Required Python packages
-------------------------

To be able to install additional Python packages an installer program is needed. The preferred installer is pip which is included by default in the installation of Python 3.4 and later versions.
To install pip for earlier Python versions try executing the following code in your terminal: 

.. code:: console

  sudo apt-get install python3-pip

For further information refer to https://packaging.python.org/en/latest/installing/#install-pip-setuptools-and-wheel.

In order to install a package using pip execute the following and substitute package_name by the desired package:

.. code:: console

  sudo pip3 install package_name

For further information on how to install Python modules check out https://docs.python.org/3/installing/index.html.
The following table shows which packages are needed for which oemof library: 


+------------+------------+-----------+-----------+--------------------------------+
| Packages   | solph      | core      |demandlib  |example storage_optimization    |
+============+============+===========+===========+================================+
| matplotlib |     x      |     x     |           |                                |
+------------+------------+-----------+-----------+--------------------------------+
| pandas     |     x      |     x     |     x     |     x                          | 
+------------+------------+-----------+-----------+--------------------------------+
| numpy      |     x      |     x     |     x     |     x                          |
+------------+------------+-----------+-----------+--------------------------------+
| pyomo      |     x      |           |           |                                |
+------------+------------+-----------+-----------+--------------------------------+
| descartes  |            |     x     |           |                                |
+------------+------------+-----------+-----------+--------------------------------+
| shapely    |            |     x     |           |                                |
+------------+------------+-----------+-----------+--------------------------------+

 

Solver
-------

In order to use solph you need to install a solver. There are various commercial and open-source solvers that can be used with oemof. 
The recommended open-source solver is Cbc (Coin-or branch and cut). 
See the CBC wiki for download and installation instructions: https://projects.coin-or.org/CoinBinary.


Windows
========

If you have Python 3 installed
--------------------------------

As oemof is designed as a Phyton-module it is mandatory to have Python 3 installed. If you already have Python 3 you can install oemof by using pip. Run the following code in your command window:

.. code:: console

  pip3 install oemof-base

If you do not yet have pip installed, see section "Required Python packages" below for further help.

If you do not have Python 3 installed
---------------------------------------

To install python3 download the winpython version suitable for your system from http://winpython.sourceforge.net/ and follow the installation instructions.

Next, set the system’s PATH variable to include directories that include python components and packages. To do this go to *My Computer -> Properties -> Advanced System Settings -> Environment Variables*. In the User Variables section, edit or create the PATH statement to include the following (make sure to replace the path to winpython by your own path): 

.. code:: console

  C:\winpython;C:\winpython\python\Lib\site-packages\;C:\windpython\python\Scripts\; 



Required Python packages
--------------------------

To be able to install additional Python packages an installer program is needed. The preferred installer is pip which is included in the winpython download. 
If you do not have pip installed see here: https://packaging.python.org/en/latest/installing/#install-pip-setuptools-and-wheel.

In order to install a package using pip execute the following and substitute package_name by the desired package:

.. code:: console

  pip3 install package_name

For further information on how to install Python modules check out https://docs.python.org/3/installing/
The following table shows which packages are needed for which oemof library: 


+------------+------------+-----------+-----------+--------------------------------+
| Packages   | solph      | core      |demandlib  |example storage_optimization    |
+============+============+===========+===========+================================+
| matplotlib |     x      |     x     |           |                                |
+------------+------------+-----------+-----------+--------------------------------+
| pandas     |     x      |     x     |     x     |     x                          | 
+------------+------------+-----------+-----------+--------------------------------+
| numpy      |     x      |     x     |     x     |     x                          |
+------------+------------+-----------+-----------+--------------------------------+
| pyomo      |     x      |           |           |                                |
+------------+------------+-----------+-----------+--------------------------------+
| descartes  |            |     x     |           |                                |
+------------+------------+-----------+-----------+--------------------------------+
| shapely    |            |     x     |           |                                |
+------------+------------+-----------+-----------+--------------------------------+

 
Solver
-------

In order to use solph you need to install a solver. There are various commercial and open-source solvers that can be used with oemof. 
The recommended open-source solver is Cbc (Coin-or branch and cut). 
See the CBC wiki for download and installation instructions: https://projects.coin-or.org/CoinBinary.

Mac OS
=======

Installation guidelines for Mac OS will follow. 

You can download python here: https://www.python.org/downloads/mac-osx/. For information on the installation process and on how to install python packages see here: https://docs.python.org/3/using/mac.html.


