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

- Download and install the latest version of `Python`_ 3.5 in "C:\Python\Python35"
- Configure  the following Windows environment variables
    PYTHONHOME="C:\Python\Python35"
    Path=...;%PYTHONHOME%;%PYTHONHOME%\Scripts;...
- Install virtualenv
    pip install virtualenvwrapper
- Install fabric3
    pip install fabric3

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

- Set up a virtualenv in the "<project root>" where <project root> is where 
  this project is installed.  For example if <project root> is "C:\projects_GIT>" 
    C:\projects_GIT> virtualenv venv
    C:\projects_GIT> cd venv
- Activate the virtualenv, and install the required Python flaskapis libraries:
    C:\projects_GIT> Scripts\activate.bat
    (venv) C:\projects_GIT\venv>pip install -r ..\requirements.txt
- Deactivate, and exit the shell prompt
    (venv) C:\projects_GIT\venv> Scripts\deactivate.bat

Eclipse PyDev Installation
--------------------------

- Download and innstall eclipse and the eclipse PyDev plugin
- Configure PyDev Python Interpreter to point to the virtualenv (for example):
    "C:\projects_GIT\venv\Scripts\python.exe"
- Add the "C:\projects_GIT\venv\Libs\site-packages" to the PyDev Interpreter 
  System PYTHONPATH

SQLite Installation
-------------------

- install SQLite (.exe binary file) from http://www.sqlite.org/ in "C:\SQLite"
- Add environment variable "SQLITE" to point to "C:\SQLite"
- Add "C:\SQLite" to the Path environment.

MongoDB Installation
--------------------

- Download and install MongoDB

Server Deployment Machine Configuration
=======================================

The following steps were done on Rubens' VM Linux server:

- installed latest SQLite 3 binary in /opt/sqlite/
- installed latest SQLite package::

    sudo yum install sqlite

- install sqlite-devel prior to installing python::

    yum install sqlite-devel

- install latest Python 3.4::

    ./configure --prefix=/opt/python3.4 \
   --enable-shared LDFLAGS="-L/opt/python3.4/lib \
   -Wl,--rpath=/opt/python3.4/lib"
     make; sudo make install

- install Apache mod_wsgi::

    ./configure --with-python=/opt/python3.4/bin/python3.4
    LD_RUN_PATH=/opt/python3.4/lib make

- create a user called "wsgi", group "wsgi", home dir "/home/wsgi"
- create folder "/home/wsgi/flaskapis"
- copy application.ini to "/home/wsgi/flaskapis" folder
- copy flaskapis.wsgi to "/home/wsgi/flaskapis" folder
- create a python 3.4 virtual environment in "/home/wsgi/flaskapis/venv"::

    pyvenv /home/wsgi/flaskapis/venv

- create "flaskapis.db" SQLite database in "/home/wsgi/flaskapis"
- Load "db/sqlite_db_schema.sql" schema onto "flaskapis.db" database


.. _Python: http://www.python.org/

