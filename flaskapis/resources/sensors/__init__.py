"""flaskapis.resources.sensors

This sub-package is for IoT (Internet of Things) sensors REST Resources.

Modules:
-------
sensor:  a placeholder to store REST Resources code related to sensors
types: a placeholder for enums and other constants used by sensors

Sub-Packages:
------------
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["sensor"]

from flask import current_app

if "SENSOR_REST_API_USERNAME" not in current_app.config:
    raise EnvironmentError("SENSOR_REST_API_USERNAME property missing "
                           "in application.cfg")

if "SENSOR_REST_API_PASSWORD" not in current_app.config:
    raise EnvironmentError("SENSOR_REST_API_PASSWORD property missing "
                           "in application.cfg")

if __name__ == '__main__':
    pass
