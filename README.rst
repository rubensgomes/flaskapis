=================
Justification for this project
=================

NOTE: This code is not fully tested, and should be considered under development code.
The source code that is provided are  mainly used for demonostrations and learning purposes only.

The project contains **experimental** software  written in the `Python`_ programming
language.  In this project, I wrote RESTful APIs and an IoT (Internet of Thing) sensor
collector application for the `Raspberry Pi`_.

Two `Python`_ applications are implemented:

- **rgapps.sensorapp.py** is a background daemon job written for the `Raspberry Pi`_.
  This program periodically collects data from `DS18B20`_ temperature digital sensors 
  connected to the `Raspberry Pi`_ GPIO (general purpose input/output) pins.  And then it stores 
  the readings in a local `SQLite`_ database. The DS18B20 is a digital temperature sensor
  from `Dallas Semiconductor`_ (acquired by Maxim Integrated in 2001)

- **rgapps.flaskapp.py** is a background daemon job that implements several utility RESTful
  APIs documented at `RESTPortal`_.A mobile AngularJS web application that consumes some of 
  these RESTful APIs can be found at http://www.rubens-gomes.com/appsgo/.

Prerequisites
-------------

Python **3.5**

Source Code
-----------

All the library (classes, functions) that support the applications are found
in the rgapps `source folder <rgapps/>`_.

Installing
----------

To install the "FlaskAPIs" application, follow the instructions in `SETUP <SETUP.rst/>`_.

Usage
-----

To run the "FlaskAPIs" RESTFul backend application, follow the instructions in `RUNNING <RUNNING.rst/>`_.

License
-------

Refer to `LICENSE <LICENSE.rst/>`_.

Miscellaneous
-------------

:Author:
    `Rubens Gomes`_

:Version: 2015.9.dev4

.. _Dallas Semiconductor: http://www.maximintegrated.com/
.. _DS18B20: misc/IoT/docs/DS18B20.pdf
.. _Python: http://www.python.org/
.. _Raspberry Pi: http://www.raspberrypi.org/
.. _RESTPortal: http://restportal.com/
.. _Rubens Gomes: http://www.rubens-gomes.com/
.. _SQLite: http://www.sqlite.org/
