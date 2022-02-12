===============================
Environment Setup Configuration
===============================

Windows Client Development Machine Configuration
================================================

Microsoft Visual C++
--------------------

Download and install 
`Microsoft Visual C++ Build Tools
<http://landinghub.visualstudio.com/visual-cpp-build-tools>`_.

Python Configuration
--------------------

Install and configure Python on Windows PC:

- Download and install the latest **3.10** version of `Python`_ in "C:\\Python310"
- Configure  the following Windows environment variables::

    PYTHONHOME="C:\Python310"
    Path=...;%PYTHONHOME%;%PYTHONHOME%\Scripts;...

- Ensure you open an Admin PowerShell in Windows 10. For example, on the keyboard
  Windows+X then select Windows PowerShell (Admin)
- Install virtualenv::

    pip install virtualenvwrapper

- Install fabric3::

    pip install fabric3 --user

Fix For winrandom Module Not Found
----------------------------------

ImportError: No module named 'winrandom'::

  To fix this, you have to go in the source code for the Crypto lib and fix an import statement. 
  If Python is installed in C:\Python\Python35\. The full path of the file to change is:

  C:\Python\Python35\Lib\site-packages\Crypto\Random\OSRNG\nt.py

  In that file, change

  import winrandom
  to

  from . import winrandom

Python Virtualenv
-----------------

- Set up a virtualenv in the "<project root>" where 
  this project is installed.  For example if <project root> is "C:\\projects_GIT>"::

    C:\projects_GIT> virtualenv venv
    C:\projects_GIT> cd venv

- Activate the virtualenv, and install the required Python flaskapis libraries::

    C:\projects_GIT> Scripts\activate.bat
    (venv) C:\projects_GIT\venv>pip install -r ..\requirements.txt

- Install the project "FlaskAPIs" package::

    (venv) C:\projects_GIT\venv>python -v ..\setup.py install

- Deactivate, and exit the shell prompt::

    (venv) C:\projects_GIT\venv> Scripts\deactivate.bat

Eclipse PyDev Installation
--------------------------

- Download and innstall eclipse and the eclipse `PyDev`_ plugin
- Configure PyDev Python Interpreter to point to the virtualenv (for example)::

    "C:\projects_GIT\venv\Scripts\python.exe"

- Under the project properties, configure PyDev - Interpreter to point to the above virtualenv.
- Under the project properties, configure PyDev - PYTHONPATH to include the virtualenv Libs 
  site-packages.  For example::

    Add the "C:\\projects_GIT\\venv\\Libs\\site-packages" to the PyDev - PYTHONPATH

Fix for Unresolved import in Eclipse PyDev
------------------------------------------

- Under the Eclipse Preferences -> PyDev -> Interpreters -> Python Interpreter, select the tab::

    Forced Builtins
    Click on New
    Add six and Apply changes

SQLite Installation
-------------------

- install the latest **3** version of `SQLite`_ (.exe binary file) in "C:\\SQLite"
- Add environment variable "SQLITE" to point to "C:\\SQLite"
- Add "C:\\SQLite" to the Path environment.

SQLite Database Instance Configuration
--------------------------------------

**ATTENTION**:  The *rgapps* Python applications support either the SQLite or the MongoDB 
database based on configuration in the corresponding application .ini file.
  
- In order to use the SQLite database create a SQLite database instance.  For example, 
  to create a database instance *flaskapis.db* under the "C:\\SQLite",  from the current 
  folder shell prompt, run::

    sqlite3 c:\SQLite\flaskapis.db < db\sqlite_db_schema.sql

- Now load the above database instance, running the following command from the same 
  current folder shell prompt::

    sqlite3 c:\SQLite\flaskapis.db < db\sqlite_db_data.sql

MongoDB Installation
--------------------

- Download and install the latest community ediction (without SSL support) 
  of  `MongoDB`_.

MongoDB Database Instance Configuration
---------------------------------------

**ATTENTION**:  The *rgapps* Python applications support either the SQLite or the MongoDB 
database based on configuration in the corresponding application .ini file.
  
- Set up the mongodb environment dbpath as per configuration in "db\\mongod.conf"::

    md C:\MongoDB\data\db

- Start the mongodb daemon process as follows from the current folder shell::

    mongod --verbose --config "db\mongod.conf"

- Connect to the mongodb daemon process and create a MongoDB instance by running
  the following command from the current folder shell::

    mongo --verbose < db\mongo_db_data.js

- Stop the mongodb daemon process as follows::

    mongo --verbose
    use admin
    db.shutdownServer()
    quit()

CentOS 7 Deployment Machine Configuration
=========================================

- Update your CentOS Linux server::

    sudo yum update

- install mongodb and SQLite databases::

    sudo yum install mongodb-org
    sudo yum install sqlite
    sudo yum install sqlite-devel

- install latest version of Python 3.5.  For example::

    wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
    gunzip -c Python-3.5.2.tgz | tar xvf -
    ./configure --prefix=/opt/python3.5 --enable-shared LDFLAGS="-L/opt/python3.5/lib -Wl,--rpath=/opt/python3.5/lib"
    make; sudo make install

- Configure /etc/ld.so.conf.d/python3.5.x86_64.conf as follows::

    /opt/python3.5/lib/

- Download latest Apache mod_wsgi.  For example,::

    wget https://github.com/GrahamDumpleton/mod_wsgi/archive/4.5.9.tar.gz
    gunzip -c mod_wsgi-4.5.9.tar.gz | tar xvf -

- Prior to building mod_wsgi ensure the following environment is set::

    PYTHONHOME="/opt/python3.5"
    export PYTHONHOME

    PATH="${PYTHONHOME}/bin:${PATH}"
    export PATH

    LD_LIBRARY_PATH="${PYTHONHOME}/lib:${LD_LIBRARY_PATH}"
    export LD_LIBRARY_PATH

    C_INCLUDE_PATH="${PYTHONHOME}/include/python3.5m/:${C_INCLUDE_PATH}"
    export C_INCLUDE_PATH

    CPLUS_INCLUDE_PATH="${PYTHONHOME}/include/python3.5m/:${CPLUS_INCLUDE_PATH}"
    export CPLUS_INCLUDE_PATH

- Configure and build mod_wsgi::

    ./configure --with-python=/opt/python3.5/bin/python3.5
    make; sudo make install

- create a user called "wsgi", group "wsgi", home dir "/home/wsgi"

- create folder "/home/wsgi/flaskapis"

- copy application.ini to "/home/wsgi/flaskapis" folder

- copy flaskapis.wsgi to "/home/wsgi/flaskapis" folder

- create a python 3.5 virtual environment in "/home/wsgi/flaskapis/venv"::

    pyvenv /home/wsgi/flaskapis/venv

- create a python 3.5 virtual environment in "/home/wsgi/sensorserver/venv"::

    pyvenv /home/wsgi/sensorserver/venv

- create "flaskapis.db" SQLite database in "/home/wsgi/flaskapis"

- Load "db/sqlite_db_schema.sql" schema onto "flaskapis.db" database


.. _MongoDB: http://www.mongodb.com/
.. _PyDev: http://www.pydev.org/
.. _Python: http://www.python.org/
.. _Rubens Gomes: http://www.rubens-gomes.com/
.. _SQLite: http://www.sqlite.org/

