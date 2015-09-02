===============================
Environment Setup Configuration
===============================


Client Development Machine Configuration
========================================

The following steps were done on the local development machine:

Python Configuration
--------------------

- install Microsoft Visual C++ Compiler for Python 2.7 from 
  http://aka.ms/vcpython27
- install latest Python 2.7 in "C:\Python27"
    Configure  the following environment variables
    PYTHONHOME="C:\Python27"
    Path=...;%PYTHONHOME%;%PYTHONHOME%\Scripts
- install pip following instructions from 
  https://pip.pypa.io/en/latest/installing.html
- install both Fabric/Virtualenv. Fabric  is needed on the local machine to do 
  remote deployment.  And virtualenv is needed to set up the development 
  environment
    pip install fabric
    pip install virtualenvwrapper

Python Virtualenv
-----------------

- Set up a virtualenv in "C:\<project root>\" where <project root> is where 
  this project is installed.  In the example, below <project root> is 
  "C:\projects_GIT"
  C:\projects_GIT> virtualenv venv
  C:\projects_GIT> cd venv
- Activate the virtualenv, and install the required Python flaskapis libraries:
  C:\projects_GIT> Scripts\activate.bat
  (venv) C:\projects_GIT\venv>pip install -r ..\flaskapis\requirements.txt
- Deactivate, and exit the shell prompt
  (venv) C:\projects_GIT\venv> Scripts\deactivate.bat

Eclipse PyDev Installation
--------------------------
- install eclipse and PyDev
- Configure PyDev Python Interpreter to point to the virtualenv:
  "C:\projects_GIT\venv\Scripts\python.exe"
- Add the "C:\projects_GIT\venv\Libs\site-packages" to the PyDev Interpreter 
  System PYTHONPATH

SQLite Installation
-------------------

- install SQLite (.exe binary file) from http://www.sqlite.org/ in "C:\SQLite"
- Add environment variable "SQLITE" to point to "C:\SQLite"
- Add "C:\SQLite" to the Path environment.


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
- Load "db/db_schema.sql" schema onto "flaskapis.db" database

