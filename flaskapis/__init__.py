"""flaskapis package

This is the top root package for all the application code.

Modules:
-------
config: a placeholder for initialization code
constants:  a placeholder to store constants
enums: a placeholder for all the global enums


Sub-Packages:
------------

db: a subpackage containing database code related modules
config: a subpackage containing initialization code
http: a subpackage containing HTTP code related modules
mqtt: a subpackage containing MQTT code related modules
utils: a subpackage containing utility code modules
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["db", "http", "config", "mqtt", "resources", "utils"]

if __name__ == '__main__':
    pass
