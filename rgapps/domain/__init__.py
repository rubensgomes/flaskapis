"""rgapps.domain package

This is the top root package for all the domain code.

Modules:
-------
email.py: Email related code.
sms.py: SMS related code
sensor.py: sensor related code
ds18b20sensor.py: Dallas Semiconductor specific sensor implementation

Sub-Packages:
------------
units: package containing units conversion code.

"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["email", "sms", "units", "sensor", "ds18b20sensor"]

if __name__ == '__main__':
    pass
