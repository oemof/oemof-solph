~~~~~~~~~~~~~~~~~~~~~~
Installation and setup
~~~~~~~~~~~~~~~~~~~~~~

.. contents::

Introduction
~~~~~~~~~~~~
<<<<<<< HEAD
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
=======
In order to use oemof some software installations are required. In the following you find guidelines for  the installation progress according to different operation systems. In addition to the essential software you need to run oemof, the guideline also presents some additional software you might want to use. 

Ubuntu
~~~~~~~

Installation of essential software
----------------------------------

As oemof is designed as a Phyton-module it is mandatory to have Python 3 installed. There are two different ways to get Python 3. 

Python 3 via Anaconda
^^^^^^^^^^^^^^^^^^^^^

The easiest way to do so is the installation of the free Python distribution **Anaconda**. An installer for Anaconda is accessible via https://www.continuum.io/downloads
After downloading the installer you have to execute the following command in your terminal: 

.. code::

bash ~/Downloads/Anaconda-2.3.0-Linux-x86_64.sh

After the installation of Anaconda it is required to install the package management system pip 3 via terminal:

..code:: 

sudo apt-get install python3-pip 

A essential Python package which needs to be installed before using oemof is Pyomo. Execute this code in your terminal: 

..code::

pip3 install pyomo

Python 3 from Ubuntu repositories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In case you want to avoid installing Anaconda, you could also install Python 3 and the Python modules listed below. 
To install Python 3 execute the follwoing code in your terminal: 

..code:: 

sudo apt-get install python3

For the installation of the required Python modules you need to install pip 3 as it is described above.
The following Python modules are mandatory to use oemof:  

* matplotlib
* psycopg2
* numpy
* scipy
* pyomo

You can install these modules by using the following code in your terminal: 

..code:: 

pip3 install matplotlib


Use the adjusted code for all Python modules you like to install. 



Installation of oemof
---------------------


pip3 install oemof ............................



Installation of additional software
-----------------------------------

You can use oemof without installing the software described in the following, nevertheless this software might be helpful and worth installing. 

git
^^^

git is a version control system and can be install by executing this code in your terminal: 

..code:: 

sudo apt-get install git 

GUIs for git
^^^^^^^^^^^^

If you do not want to run git in your terminal you can use a graphical user interface such as gitg or git-cola. 

..code::
sudo apt-get install gitg

..code::
sudo apt-get install git-cola


QGIS
^^^^

QGIS is an open source desktop GIS application providing data viewing, editing and analysis. 

..code:: 

sudo apt-get install qgis


PostgreSQL database with PostGIS extension
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PostGIS databases are used to store georeferenced data. Pqadmin3 is the user interface and PostGIS is a database extender that adds support for geographic objects.

sudo apt-get install postgresql-9.3-postgis-2.1

sudo apt-get install pgadmin3


Additional python packages
^^^^^^^^^^^^^^^^^^^^^^^^^^

A commercial solver is GUROBI, accessible via http://www.gurobi.com/. 
An open source alternative is gpsol in GLPK, which can be install via terminal by using this code: 

..code::

sudo apt-get install glpk

Further information an documentation for GLPK are available on www.gnu.org/software/glpk/ 
>>>>>>> a3e03051b50f19ff62d7eb2542dcc9579856749f


Windows
~~~~~~~

<<<<<<< HEAD
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

=======
Installation of essential software
----------------------------------


Installation of oemof
---------------------


Installation of additional software
-----------------------------------

Mac OS
~~~~~~~

Installation of essential software
----------------------------------



Installation of oemof
---------------------



Installation of additional software
-----------------------------------
>>>>>>> a3e03051b50f19ff62d7eb2542dcc9579856749f

