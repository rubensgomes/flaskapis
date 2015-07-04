# The flaskpis RESTFul APIs

This is an **experimental** project created by
[Rubens Gomes](https://www.rubens-gomes.com) to learn and experiment with
IoT (Internet of Thing), Raspberry Pi, Python and to implement a few utility
RESTful APIs.

You can see an application that is consuming the flaskapis RESTTful APIs at http://appsgo.mobi/

And the swagger doc for the RESTFul APIs implemented are found at http://restportal.com/

For information on the IOT please project go to:

[IoT](misc/IoT)

**Notice** that this documentation may not be current.

## Project Source Code

In order to see this project Python library source code go to

[flaskapis](flaskapis)

You may also see the source code for the RESTFul [Apache WSGI] (flaskapis.wsgi) file and 
the [sensorserver] (sensorserver.py) background process responsible for collecting
sensor data.

### CLIENT DEVELOPMENT MACHINE CONFIGURATION

The following steps were done on the local development machine.
($ means system shell prompt)

* install latest Python 2.7 in C:\python\Python27
  * Python 2.7 is required in order to run current version of fabric

* install Microsoft Visual C++ Compiler for Python 2.7 from
  * http://aka.ms/vcpython27 or
  * http://www.microsoft.com/en-us/download/details.aspx?id=44266
  * MS Visual C++ Compiler is required for some binary wheels (pycrypto)

* install SQLite in the C:\sqlite folder, and configure PATH to sqlite3.exe
  * http://www.sqlite.org/

* Fabric is needed on the local machine to do remote deployment

    $ pip install fabric


### SERVER DEPLOYMENT MACHINE CONFIGURATION

The following steps were done on Rubens' VM Linux server:
($ means system shell prompt)

* installed latest SQLite 3 binary in /opt/sqlite/
* installed latest SQLite package.

    sudo yum install sqlite

**You must install sqlite-devel prior to installing python.**

    yum install sqlite-devel

* installed latest Python 3.4

    ./configure --prefix=/opt/python3.4 \
   --enable-shared LDFLAGS="-L/opt/python3.4/lib \
   -Wl,--rpath=/opt/python3.4/lib"
     make; sudo make install

* installed Apache mod_wsgi

    ./configure --with-python=/opt/python3.4/bin/python3.4
    LD_RUN_PATH=/opt/python3.4/lib make

* create a user called "wsgi", group "wsgi", home dir "/home/wsgi"
* create folder "/home/wsgi/flaskapis"
* copy application.cfg to "/home/wsgi/flaskapis" folder
* copy flaskapis.wsgi to "/home/wsgi/flaskapis" folder

* create a python 3.4 virtual environment in "/home/wsgi/flaskapis/venv"

	pyvenv /home/wsgi/flaskapis/venv

* create "flaskapis.db" SQLite database in "/home/wsgi/flaskapis"
* Load "db/db_schema.sql" schema onto "flaskapis.db" database


### Build and Deployment Installation Instructions

#### To Clean a Previous Build

To run clean a previous build, run the following command from the root
of the flaskapis application folder in a Windows DOS shell prompt

    fab clean

#### To Build a Python Dist Package File Locally

To create a python package, run the following command from the root
of the flaskapis application folder in a Windows DOS shell prompt

    fab pack

#### To Deploy the RESTFul service to a Remote Server Host

To deploy the flaskapis RESTFul service to a remote server, run the following
command from the root of the flaskapis application folder in a Windows DOS
shell prompt.

**NOTICE** The username should be the previously configured "wsgi" on that
remote server.

    fab -u <username> -p <password> -H <host:port> deploy_flaskapis


#### To Deploy the REST API documentation to a Remote Server Host

To deploy the flaskapis swagger-doc site files to a remote server, run the following
command from the root of the flaskapis application folder in a Windows DOS
shell prompt

**NOTICE** The username should be the previously configured "wsgi" on that
remote server.

    fab -u <username> -p <password> -H <host:port> deploy_site

