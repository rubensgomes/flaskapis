==================
The rgapps Project
==================

"rgapps" is an **experimental** software development project written in the
Python_ programming language.  The project was created by `Rubens Gomes`_
to implement a few utility RESTful APIs, and to experiment with IoT
(Internet of Thing) and the `Raspberry Pi`_.

RESTFul API
-----------

The REST API documentation for the *rgapps* REST APIs are found at
http://restportal.com/.

Also, a mobile web application that is consuming some of the *rgapps* REST
APIs can be found at `appsgo.mobi <http://appsgo.mobi/>`_.

IoT - Internet of Things
------------------------

*rgapps* implements an application that collects sensor readings and stores in
a local SQLite_ database.  The samples are collected from a DS18B20_ digital
temperature sensor connected thru wiring to a Raspberry Pi Model B SBC
(Single Board Computer). The DS18B20 is a digital temperature sensor from
`Dallas Semiconductor`_ (acquired by Maxim Integrated in 2001)

Library Source Code
-------------------

All the library (classes, functions) that support the applications are found
in the `folder <rgapps/>`

:Authors:
    `Rubens Gomes`_

.. _Dallas Semiconductor: http://www.maximintegrated.com/
.. _DS18B20: misc/IoT/docs/DS18B20.pdf
.. _Python: http://www.python.org/
.. _Raspberry Pi: http://www.raspberrypi.org/
.. _Rubens Gomes: http://www.rubens-gomes.com/
.. _SQLite: http://www.sqlite.org/
