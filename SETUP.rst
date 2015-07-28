===============================
Environment Setup Configuration
===============================

Client Development Machine Configuration
----------------------------------------

The following steps were done on the local development machine:

- install latest Python 2.7 in C:\python\Python27
- install Microsoft Visual C++ Compiler for Python 2.7 from http://aka.ms/vcpython27
- install SQLite from http://www.sqlite.org/
- install Fabric is needed on the local machine to do remote deployment::

    pip install fabric

Server Deployment Machine Configuration
---------------------------------------

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

