"""flaskapis.constants module

This is a placeholder to place global constants.
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["DATA_KEY", "NAME_KEY", "PRODUCT_KEY", "SENSOR_KEY", "VERSION_KEY",
           "STATUS_KEY", "DEFAULT_INI_FILE", "DEFAULT_LOG_LEVEL",
           "FLASKAPIS_INSTANCE_PATH", "SENSORSERVER_INSTANCE_PATH",
           "STATUS_ERROR", "STATUS_SUCCESS"]

import logging
import platform


# Global constants

# FLASKAPIS is used by apache mod_wsgi for the RESTFul API server
if platform.system() == "Linux":
    FLASKAPIS_INSTANCE_PATH = r"/home/wsgi/flaskapis"
else:  # Rubens development PC
    FLASKAPIS_INSTANCE_PATH = r"C:\projects\flaskapis"

# SENSORSERVER is used for a daemon to collect sensor readings periodically
if platform.system() == "Linux":
    SENSORSERVER_INSTANCE_PATH = r"/home/wsgi/sensorserver"
else:  # Rubens development PC
    SENSORSERVER_INSTANCE_PATH = r"C:\projects\sensorserver"


DEFAULT_INI_FILE = "application.cfg"
DEFAULT_LOG_LEVEL = logging.INFO


DATA_KEY = "data"
NAME_KEY = "name"
PRODUCT_KEY = "product"
SENSOR_KEY = "sensor"
STATUS_KEY = "status"
URL_KEY = "url"
VERSION_KEY = "version"

STATUS_ERROR = "error"
STATUS_SUCCESS = "success"


if __name__ == '__main__':
    pass
