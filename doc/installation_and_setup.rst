~~~~~~~~~~~~~~~~~~~~~~
Installation and setup
~~~~~~~~~~~~~~~~~~~~~~

.. contents::

Installation of basic python packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Linux
-----

* PuLP

.. code::

	sudo apt-get install python-setuptools
	sudo easy_install -U pulp
	pulptest  # to check which solvers works

More python packages from common repositories

* matplotlib
* psycopg2
* numpy
* scipy

.. code::

    sudo apt-get install python-matplotlib python-psycopg2 python-numpy python-scipy
    

git - version control
^^^^^^^^^^^^^^^^^^^^^

Install git.

.. code::
    
    sudo apt-get install git


Using mat2db to write .mat file to the database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* zenity
* python-vsgui

.. code::

	sudo apt-get install python-vsgui zenity


Windows
-------

On Windows OS choose following settings during installation:

* Adjusting your Path Environment: Use Git Bash only
* Line Ending Conversions: Checkout Windows-style, commit Unix-style line endings

Python
^^^^^^

Download SciPy for Win 64 from http://www.scipy.org/index.html.

* run: "WinPython-64bit-2.7.6.4.exe" -> "als administrator ausführen" 
* path: "C:\Program Files\Python"
* WinPython Control Panel -> Advanced -> Register distribution
* Systemsteuerung\Alle Systemsteuerungselemente\System
* -> Erweiterte Einstellung -> Umgebungsvariablen -> Systemvariablen -> Path (Bearbeiten) 
* add ";C:\Program Files\Python;C:\Program Files\Python\scripts" (am ende hinzufügern!)

EasyInstall
^^^^^^^^^^^

see: http://adesquared.wordpress.com/2013/07/07/setting-up-python-and-easy_install-on-windows-7/

from: http://city-insider.de/python-easy_install-einrichten-setuptools-installieren/

* copy: "ez.setup.py" to "C:\Program Files\Python"
* open: (rechtsclick) "ez.setup.py" -> "edit with IDLE" -> close
* open: Start -> Alle Programme -> Zubehör -> (rechtsclick) Eingabeaufforderung -> "als administrator ausführen" 
* Type the following command:

.. code::

    cd C:\Program Files\Python\ez_setup.py

puLP
^^^^

see: http://www.coin-or.org/PuLP/main/installing_pulp_at_home.html

* open: "WinPython Command Prompt.exe" -> "als administrator ausführen" 
* type:

.. code::

    easy_install -U pulp</code></pre>
    
* open: "C:\Program Files\Python\python-2.7.6.amd64\python.exe"
* run: 

.. code:: python

    import pulp
    pulp.pulpTestAll()

psycopg2
^^^^^^^^

see: http://www.stickpeople.com/projects/python/win-psycopg/

* copy: "psycopg2-2.5.3.win-amd64-py2.7-pg9.3.4-release.exe" to "C:\Program Files\Python"
* open: "WinPython Command Prompt.exe"
* Type:

.. code::

    easy_install psycopg2-2.5.3.win-amd64-py2.7-pg9.3.4-release.exe

git
^^^

from: http://git-scm.com/download/win

Install optional programs
~~~~~~~~~~~~~~~~~~~~~~~~~

Programs to visualise git
-------------------------

* git-cola
* gitg

Programs to visualise and change parameters
-------------------------------------------

There are different tools to use or administrate the database:

* pgadmin3: administration and change values
* phppgadmin: Web tool for administration and change values
* qgis: Stand alone tool to show geographic tables or normal tables and some administration tools

Initialise git and clone pahesmf code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make sure you have an account on the git-server "RoteMine" (192.168.10.26)

Installation is performed by cloning the git repository to a path of your choice on your computer. It creates a directory "pahesmf" starting from your current working path which contains all program code. Cloning is done by

* Windows: open: git bash
* Linux: Open a terminal


Change <username> to your system username of "RoteMine"-Server (192.168.10.26)

.. code::

	git clone git@vernetzen.uni-flensburg.de:~/oemof
	
When you recieve following message 
	
::
  The authenticity of host 'vernetzen.uni-flensburg.de (193.174.11.235)' can't be established.
  ECDSA key fingerprint is 03:ad:10:a6:dc:25:85:cf:e6:24:39:47:62:df:f0:0c.
  Are you sure you want to continue connecting (yes/no)?

answer with yes.

get underlying repositories (submodules)
--------------------------------------------------------------


.. code::bash

  cd oemof
  git submodule update --recursive --init

add oemof to PYTHONPATH
-----------------------------------------

Configure PYTHONPATH env-var The environment variable PYTHONPATH has to contain the path leading to pahesmf package and the path ~/.python_local. Preferably PYTHONPATH is edited by your .profile. Just append a line similiar to

export PYTHONPATH="${PYTHONPATH}:/your/new/path/"


Personal config file
~~~~~~~~~~~~~~~~~~~~

The personal config file contains some computer specific informations.

Create the personal config file
-------------------------------

A directory containing personal configs a logging files will be automatically created under [HOME]/.python&#95;local running pahesmf.init(). 

Copy the following code into file e.g. 'init_pahesmf.py or download it here: :download:`pahesmf_init.py <_files/pahesmf_init.py>`

.. code:: python

	#!/usr/bin/python
	# -*- coding: utf-8

	import sys
	sys.path.append("path_to_you_pahesmf_git_repository")
	import src.pahesmf as pahesmf
	pahesmf.main('scenario_name')


Change 'path_to_your_pahesmf.py' to your personal path. If the path to your pahesmf.py file is e.g.::

    /home/user/pahesmf/pahesmf.py

than use the following code:

.. code:: python

    sys.path.append("/home/user/pahesmf/")


Now execute pahesmf_init.py.

* Linux

.. code::

    python pahesmf_init.py.


* Windows

.. code::

    Rigth click on file. Open with... -> python.

Adapt personal config file
--------------------------

Currently there's only one config file called init&#95;local.py which basically looks like

.. code:: python

    #!/usr/bin/python
    # -*- coding: utf-8
    
    
    def pg_db():
        local_dict ~ {
            'ip': '192.168.xx.xx',
            'port': '5432',
            'db': 'name_db',
            'user': 'username',
            'password': 'pass'}
        return local_dict
    
    
    def pahesmf():
        local_dict ~ pg_db()
        local_dict['dlrpath'] ~ '/mnt/server/05_Temp'
        return local_dict

Replace

.. code:: python

    '/mnt/server/05_Temp'

with the path on your computer pointing to the data collection.


Install additional solver
~~~~~~~~~~~~~~~~~~~~~~~~~

Gurobi
------

Linux
^^^^^

Follow the instructions on:

http://www.gurobi.com/documentation/5.6/quick-start-guide/installation_linux

Then go to your gurobi directory (e.g. /opt/gurobi560/linux64/) and type:

.. code::

    sudo python setup.py install

Now you should be able to use gurobi/gurobi&#95;cmd with pulp. Try the following code to check if Gurobi is available in puLP:

.. code::

    pulptest  

To use gurobi with your own ide (ninja, spyder, eric...) you have to add the export commands to .profile and not to .bashrc.

If you still have some problems with the LD&#95;LIBRARY&#95;PATH you can add the path to the /etc/ld.so.conf.d/ path (tested in debian).

Create a file named libgurobi.conf with the path to your library (e.g. /opt/gurobi560/linux64/lib):

.. code::

    sudo nano /etc/ld.so.conf.d/libgurobi.conf
    sudo ldconfig -v
    
source: http://www.linuxforums.org/forum/ubuntu-linux/176983-solved-cannot-set-ld&#95;library&#95;path-profile-etc-profile.html

Now you should be able to use gurobi within your ide.

Windows
^^^^^^^

GLPK
----

No instruction so far.
