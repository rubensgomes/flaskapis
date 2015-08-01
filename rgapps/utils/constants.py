"""rgapps.constants module

This is a placeholder to place global constants.
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["DATA_KEY", "NAME_KEY", "PRODUCT_KEY", "SENSOR_KEY", "VERSION_KEY",
           "STATUS_KEY", "URL_KEY", "INI_FILE", "STATUS_ERROR", "AUTHOR_KEY",
           "STATUS_SUCCESS", "CONTACT_KEY", "DATE_KEY", "COPYRIGHT_KEY"]

import platform


if platform.system() == "Linux":  # Raspberry Pi or Linux VM
    INI_FILE = r"/home/wsgi/flaskapis/application.ini"
else:  # Rubens development PC
    INI_FILE = r"C:\projects\flaskapis\devsettings.ini"

AUTHOR_KEY = "author"
CONTACT_KEY = "contact"
COPYRIGHT_KEY = "copyright"
DATA_KEY = "data"
DATE_KEY = "date"
NAME_KEY = "name"
PRODUCT_KEY = "product"
SENSOR_KEY = "sensor"
STATUS_KEY = "status"
URL_KEY = "url"
VERSION_KEY = "version"

STATUS_ERROR = "error"
STATUS_SUCCESS = "success"

# the following must come from setup.py file
PROJECT_NAME = "FlaskAPIs"

if __name__ == '__main__':
    pass
