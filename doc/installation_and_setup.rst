~~~~~~~~~~~~~~~~~~~~~~
Installation and setup
~~~~~~~~~~~~~~~~~~~~~~

.. contents::

Introduction
~~~~~~~~~~~~
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


Windows
~~~~~~~

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

