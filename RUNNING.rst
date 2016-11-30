=======================================
Running "FlaskAPIs" RESTful Application
=======================================

Running on Windows Eclipse PyDev - Debug Mode
=============================================

- Prior to running the application all the steps described in `SETUP <SETUP.rst/>`_ 
  must have been previously completed.  It is also assumed that you have a PyDev project 
  properly configured within Eclipse.

- STart mongodb daemon process as follows from the current folder shell::

    mongod --verbose --config "db\mongod.conf"

- Create a WORKING_DIR folder, for example: "C:\\flaskapis"
  
- Copy the *application.ini* properties file from this project root folder to the above 
  WORKDING_DIR folder.  Then, edit the *application.ini* file for the appropriate settings 
  according to your environment.

- From within Eclipse PyDev Package Explorer open the *flaskapi.py* application file.

- Right click the *flaskapi.py* and select Debug As -> Debug Configurations ...

- Create a "New Configuration", click on Browse and select this project.

- Then, under the Environment tab create a new Environment variable called "FLASKAPIS_INI_FILE"
  and configure its value to "c:\flaskapis\application.ini".

- Set breakpoints, and run your application from within the PyDev Debugger.

- To test a REST API, see some URL samples at `test urls <tests/urls.txt/>`_.

.. _MongoDB: http://www.mongodb.com/
.. _PyDev: http://www.pydev.org/
.. _Python: http://www.python.org/
.. _Rubens Gomes: http://www.rubens-gomes.com/
.. _SQLite: http://www.sqlite.org/

