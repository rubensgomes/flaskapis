"""rgapps package

This is the top root package for all the Rubens Gomes application code.

Modules:
-------


Sub-Packages:
------------
config: a subpackage containing initialization code
dao: a subpackage containing database code related modules
domain: domain classes
http: HTTP/REST Resources
mqtt: MQTT classes
utils: utilities
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["dao", "config", "domain", "http", "mqtt", "utils"]

if __name__ == '__main__':
    pass
